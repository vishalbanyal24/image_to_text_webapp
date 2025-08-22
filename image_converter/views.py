from django.shortcuts import render
from django.http import JsonResponse
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


def get_llm():
    """Get LLM instance with current API key"""
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)


def _pil_image_to_data_url(pil_image, format="JPEG"):
    buffer = BytesIO()
    pil_image.convert("RGB").save(buffer, format=format)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def _try_fetch_image_bytes(image_url: str) -> bytes:
    """Fetch image bytes from a URL with multiple strategies.

    - Strips a trailing '?' (common copy/paste artifact that can cause 400)
    - Tries multiple header sets (User-Agent/Accept/Referer) to bypass hotlinking
    - Follows redirects
    """
    parsed = urlparse(image_url)
    origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else None

    # Candidate URLs: original and without trailing '?'
    candidates = [image_url]
    if image_url.endswith('?'):
        candidates.append(image_url.rstrip('?'))

    # Header variations
    header_sets = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        },
        {
            "User-Agent": "curl/8.5.0",
            "Accept": "*/*",
        },
    ]

    # If we have an origin, also try with a Referer header
    if origin:
        header_sets = [
            {**h, "Referer": origin} for h in header_sets
        ] + header_sets

    last_error = None
    for url in candidates:
        for headers in header_sets:
            try:
                resp = requests.get(url, timeout=20, headers=headers, allow_redirects=True)
                resp.raise_for_status()
                # Some sites don't set image Content-Type properly; try to open anyway
                return resp.content
            except requests.RequestException as e:
                last_error = e
                continue

    if last_error is None:
        raise requests.RequestException("Failed to fetch image from URL")
    raise last_error


def test_api(request):
    """Test endpoint to check if Google API key is working"""
    try:
        llm = get_llm()
        message = HumanMessage(content="Say 'Hello, API is working!'")
        response = llm.invoke([message])
        return JsonResponse({
            'status': 'success',
            'message': 'API is working',
            'response': response.content
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'API test failed: {str(e)}'
        })


@csrf_exempt
def convert_image_to_text(request):
    description = None
    error_message = None
    image_url = None
    image_local_path = None

    if request.method == 'POST':
        image_file = request.FILES.get('image_file')
        image_url = request.POST.get('image_url')
        image_local_path = request.POST.get('image_local_path')

        image = None

        try:
            # Handle file upload
            if image_file:
                image = Image.open(image_file)
                image_description_obj = ImageDescription(image_file=image_file)

            # Handle URL
            elif image_url and image_url.strip():
                raw_url = image_url.strip()

                # Fix common URL issues
                if raw_url.lower().startswith('www.'):
                    raw_url = 'https://' + raw_url

                # Validate URL
                parsed = urlparse(raw_url)
                if parsed.scheme not in ("http", "https") or not parsed.netloc:
                    error_message = "Please enter a valid http(s) image URL."
                else:
                    try:
                        # Robust fetch with retries and header variations
                        content = _try_fetch_image_bytes(raw_url)
                        image = Image.open(BytesIO(content))
                        image_url = raw_url.rstrip('?')
                        image_description_obj = ImageDescription(image_url=image_url)
                    except UnidentifiedImageError:
                        error_message = "The URL does not point to a valid image file."
                    except requests.RequestException as e:
                        # Provide actionable guidance for hotlink-protected hosts
                        hint = ""
                        hostname = parsed.netloc.lower()
                        if any(x in hostname for x in ["istockphoto.com", "gettyimages.com", "adobe.com", "alamy.com"]):
                            hint = " This host may block direct downloads. Please download the image and upload it instead."
                        if raw_url.endswith('?'):
                            hint += " Tip: remove the trailing '?' from the URL."
                        error_message = f"Failed to fetch image: {str(e)}.{hint}"

            # Handle local path
            elif image_local_path and image_local_path.strip():
                local_path = image_local_path.strip()
                if os.path.exists(local_path):
                    image = Image.open(local_path)
                    image_local_path = local_path
                    image_description_obj = ImageDescription(image_local_path=local_path)
                else:
                    error_message = "Local image path does not exist."

            else:
                error_message = "Please provide an image file, URL, or local path."

            # Process image if we have one
            if image and not error_message:
                try:
                    # Check API key
                    api_key = os.environ.get('GOOGLE_API_KEY')
                    if not api_key:
                        error_message = "Google API key not configured. Please set GOOGLE_API_KEY environment variable."
                    else:
                        # Generate description
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

                        if description:
                            if image_description_obj:
                                image_description_obj.description = description
                                image_description_obj.save()
                        else:
                            error_message = "No description generated. Please try again."

                except ValueError as ve:
                    error_message = f"Configuration Error: {str(ve)}"
                except Exception as api_error:
                    error_message = f"API Error: {str(api_error)}"

        except UnidentifiedImageError:
            error_message = "Could not identify the image. Please try a different file/URL."
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"

    return render(request, 'image_converter/index.html', {
        'description': description,
        'error_message': error_message,
        'input_image_url': image_url,
        'input_image_local_path': image_local_path,
    })
