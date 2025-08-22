from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import ImageDescription
import os
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from urllib.parse import urlparse
import re

# Initialize the Generative AI model
# Ensure your GOOGLE_API_KEY is set as an environment variable
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def _pil_image_to_data_url(pil_image, format="JPEG"):
    buffer = BytesIO()
    pil_image.convert("RGB").save(buffer, format=format)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    mime = "image/jpeg" if format.upper() == "JPEG" else f"image/{format.lower()}"
    return f"data:{mime};base64,{encoded}"


@csrf_exempt
def convert_image_to_text(request):
    description = None
    image_description_obj = None
    error_message = None
    image_url = None
    image_local_path = None

    if request.method == 'POST':
        image_file = request.FILES.get('image_file')
        image_url = request.POST.get('image_url')
        image_local_path = request.POST.get('image_local_path')

        image = None

        try:
            if image_file:
                image = Image.open(image_file)
                image_description_obj = ImageDescription(image_file=image_file)
            elif image_url:
                # Sanitize common user mistakes (double-pasted URL, missing slash, leading/trailing spaces)
                raw_url = (image_url or '').strip()
                # Cut off if multiple "http" occurrences (accidental concatenation)
                second_http = raw_url.find('http', 1)
                if second_http != -1:
                    raw_url = raw_url[:second_http]
                # Fix single slash after scheme (https:/example → https://example)
                raw_url = re.sub(r'^(https?:)/([^/])', r'\1//\2', raw_url, flags=re.IGNORECASE)
                # Prepend scheme if missing
                if raw_url.lower().startswith('www.'):
                    raw_url = 'https://' + raw_url

                image_url = raw_url
                # Validate URL
                parsed = urlparse(image_url)
                if parsed.scheme not in ("http", "https") or not parsed.netloc:
                    error_message = "Please enter a valid http(s) image URL."
                else:
                    headers = {"User-Agent": "Mozilla/5.0 (compatible; ImageToTextBot/1.0)"}
                    resp = requests.get(image_url, timeout=12, headers=headers)
                    resp.raise_for_status()
                    content_type = resp.headers.get("Content-Type", "")
                    if not content_type.startswith("image/") and not image_url.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif")):
                        error_message = "The provided URL does not point to an image."
                    else:
                        image = Image.open(BytesIO(resp.content))
                        image_description_obj = ImageDescription(image_url=image_url)
            elif image_local_path:
                if os.path.exists(image_local_path):
                    image = Image.open(image_local_path)
                    image_description_obj = ImageDescription(image_local_path=image_local_path)
                else:
                    error_message = "Local image path does not exist."
            else:
                error_message = "Please provide an image file, URL, or local path."

            if image:
                # Always send a base64 data URL to the model for reliability
                prepared_image_url = _pil_image_to_data_url(image)
                # Generate description using LangChain Google Generative AI
                message = HumanMessage(
                    content=[
                        {"type": "text", "text": "Describe this image."},
                        {"type": "image_url", "image_url": prepared_image_url},
                    ]
                )
                response = llm.invoke([message])
                description = response.content or None
                if not description:
                    error_message = "No description generated. Try another image or method."
                
                if image_description_obj:
                    image_description_obj.description = description
                    image_description_obj.save()

        except UnidentifiedImageError:
            error_message = "Could not identify the image. Please try a different file/URL."
        except requests.Timeout:
            error_message = "Fetching the image timed out. Please try again or download the image and upload it."
        except requests.RequestException as e:
            error_message = f"Failed to fetch image URL: {e}"
        except Exception as e:
            error_message = f"Error: {e}"

    return render(request, 'image_converter/index.html', {
        'description': description,
        'error_message': error_message,
        'input_image_url': image_url,
        'input_image_local_path': image_local_path,
    })
