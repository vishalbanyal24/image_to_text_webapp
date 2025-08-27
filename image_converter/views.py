from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
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
from .genai_client import generate_text


# --- Helpers ---

def get_llm():
    """Return a Gemini LLM instance with current API key"""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
    )


def _pil_image_to_data_url(pil_image, format="JPEG"):
    """Convert PIL image to base64 data URI"""
    buffer = BytesIO()
    pil_image.convert("RGB").save(buffer, format=format)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{encoded}"


def _try_fetch_image_bytes(image_url: str) -> bytes:
    """Fetch image bytes from URL with fallback headers and fixes."""
    parsed = urlparse(image_url)
    origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else None

    candidates = [image_url]
    if image_url.endswith("?"):
        candidates.append(image_url.rstrip("?"))

    header_sets = [
        {
            "User-Agent": "Mozilla/5.0",
            "Accept": "image/*,*/*;q=0.8",
        },
        {"User-Agent": "curl/8.5.0", "Accept": "*/*"},
    ]

    if origin:
        header_sets = [{**h, "Referer": origin} for h in header_sets] + header_sets

    last_error = None
    for url in candidates:
        for headers in header_sets:
            try:
                resp = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
                resp.raise_for_status()
                return resp.content
            except requests.RequestException as e:
                last_error = e
                continue

    raise last_error or requests.RequestException("Failed to fetch image from URL")


# --- Views ---

def my_view(request):
    """Simple test view"""
    text = generate_text("Describe this image...")
    return HttpResponse(text)


def test_api(request):
    """Check if Gemini API is working"""
    try:
        llm = get_llm()
        response = llm.invoke([HumanMessage(content="Say 'Hello, API is working!'")])
        return JsonResponse({
            "status": "success",
            "message": "API is working",
            "response": response.content,
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
def convert_image_to_text(request):
    description = None
    error_message = None
    image_url = None
    image_local_path = None

    if request.method == "POST":
        image_file = request.FILES.get("image_file")
        image_url = request.POST.get("image_url")
        image_local_path = request.POST.get("image_local_path")

        image = None
        image_description_obj = None

        try:
            # File upload
            if image_file:
                image = Image.open(image_file)
                image_description_obj = ImageDescription(image_file=image_file)

            # Remote URL
            elif image_url and image_url.strip():
                raw_url = image_url.strip()
                if raw_url.lower().startswith("www."):
                    raw_url = "https://" + raw_url

                parsed = urlparse(raw_url)
                if parsed.scheme not in ("http", "https") or not parsed.netloc:
                    error_message = "Invalid URL. Please enter a valid http(s) image URL."
                else:
                    try:
                        content = _try_fetch_image_bytes(raw_url)
                        image = Image.open(BytesIO(content))
                        image_url = raw_url.rstrip("?")
                        image_description_obj = ImageDescription(image_url=image_url)
                    except UnidentifiedImageError:
                        error_message = "The URL does not point to a valid image."
                    except Exception as e:
                        error_message = f"Failed to fetch image: {str(e)}"

            # Local path
            elif image_local_path and image_local_path.strip():
                if os.path.exists(image_local_path):
                    image = Image.open(image_local_path)
                    image_description_obj = ImageDescription(image_local_path=image_local_path)
                else:
                    error_message = "Local image path does not exist."

            else:
                error_message = "Please provide an image file, URL, or local path."

            # Generate description
            if image and not error_message:
                try:
                    llm = get_llm()
                    prepared_image_url = _pil_image_to_data_url(image)

                    message = HumanMessage(
                        content=[
                            {"type": "text", "text": "Describe this image in detail."},
                            {"type": "image_url", "image_url": prepared_image_url},
                        ]
                    )
                    response = llm.invoke([message])
                    description = response.content

                    if description and image_description_obj:
                        image_description_obj.description = description
                        image_description_obj.save()
                except Exception as api_error:
                    error_message = f"Gemini API Error: {str(api_error)}"

        except UnidentifiedImageError:
            error_message = "Could not identify the image. Try another file/URL."
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"

    return render(request, "image_converter/index.html", {
        "description": description,
        "error_message": error_message,
        "input_image_url": image_url,
        "input_image_local_path": image_local_path,
    })
