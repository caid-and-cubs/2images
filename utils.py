import os
import requests
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

def get_available_models():
    """Return list of available Hugging Face models for text-to-image generation"""
    return [
        {
            'id': 'stabilityai/stable-diffusion-3-medium-diffusers',
            'name': 'Stable Diffusion 3 Medium',
            'description': 'Latest high-quality model (Recommended)'
        },
        {
            'id': 'black-forest-labs/FLUX.1-schnell',
            'name': 'FLUX.1 Schnell',
            'description': 'Ultra-fast generation, commercial use allowed'
        },
        {
            'id': 'stabilityai/stable-diffusion-xl-base-1.0',
            'name': 'Stable Diffusion XL',
            'description': 'High-resolution image generation'
        },
        {
            'id': 'stable-diffusion-v1-5/stable-diffusion-v1-5',
            'name': 'Stable Diffusion 1.5',
            'description': 'Most popular and reliable model'
        },
        {
            'id': 'CompVis/stable-diffusion-v1-4',
            'name': 'Stable Diffusion 1.4',
            'description': 'Original stable diffusion model'
        },
        {
            'id': 'dreamlike-art/dreamlike-diffusion-1.0',
            'name': 'Dreamlike Diffusion',
            'description': 'Artistic and dreamy style images'
        },
        {
            'id': 'prompthero/openjourney',
            'name': 'OpenJourney',
            'description': 'Midjourney-style artistic model'
        },
        {
            'id': 'wavymulder/Analog-Diffusion',
            'name': 'Analog Diffusion',
            'description': 'Vintage analog photography style'
        }
    ]

def generate_image_from_text(prompt, model_name, output_path):
    """
    Generate image from text using Hugging Face Inference API
    
    Args:
        prompt (str): Text prompt for image generation
        model_name (str): Hugging Face model identifier
        output_path (str): Path to save the generated image
    
    Returns:
        tuple: (success: bool, result: str/error_message)
    """
    try:
        # Get API key from environment
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not api_key:
            return False, "Hugging Face API key is required. Please add your API key in Secrets."
        
        logger.info(f"Generating image with model: {model_name}, prompt: {prompt[:100]}...")
        
        # Try the new Inference Providers API first
        providers_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Simple payload for text-to-image
        payload = {
            "inputs": prompt
        }
        
        # Make request to Hugging Face API
        response = requests.post(providers_url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            # Check if response is an image
            content_type = response.headers.get('content-type', '')
            if content_type.startswith('image/') or len(response.content) > 1000:
                # Save image directly
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                # Verify image was saved correctly
                try:
                    with Image.open(output_path) as img:
                        # Convert to RGB if needed and save as PNG
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        img.save(output_path, 'PNG')
                    
                    logger.info(f"Image successfully generated and saved to {output_path}")
                    return True, "Image generated successfully"
                    
                except Exception as e:
                    logger.error(f"Error processing generated image: {str(e)}")
                    return False, "Error processing generated image"
            else:
                # Try to parse JSON response for error
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', 'Unknown error from API')
                    logger.error(f"API returned error: {error_message}")
                    return False, f"API Error: {error_message}"
                except:
                    logger.error(f"Unexpected response format: {response.text[:200]}")
                    return False, "Unexpected response from API"
        
        elif response.status_code == 503:
            # Model is loading
            return False, "Model is currently loading. Please try again in a few moments."
        
        elif response.status_code == 429:
            # Rate limit exceeded
            return False, "Rate limit exceeded. Please wait before making another request."
        
        elif response.status_code == 401:
            # Unauthorized
            return False, "Invalid API key. Please check your Hugging Face API key."
        
        elif response.status_code == 404:
            # Model not found, try alternative models
            logger.warning(f"Model {model_name} not found, trying alternative...")
            
            # Try with a known working model
            fallback_models = [
                "runwayml/stable-diffusion-v1-5",
                "CompVis/stable-diffusion-v1-4",
                "stabilityai/stable-diffusion-2-1"
            ]
            
            for fallback_model in fallback_models:
                if fallback_model != model_name:
                    fallback_url = f"https://api-inference.huggingface.co/models/{fallback_model}"
                    fallback_response = requests.post(fallback_url, headers=headers, json=payload, timeout=120)
                    
                    if fallback_response.status_code == 200:
                        content_type = fallback_response.headers.get('content-type', '')
                        if content_type.startswith('image/') or len(fallback_response.content) > 1000:
                            with open(output_path, 'wb') as f:
                                f.write(fallback_response.content)
                            
                            try:
                                with Image.open(output_path) as img:
                                    if img.mode != 'RGB':
                                        img = img.convert('RGB')
                                    img.save(output_path, 'PNG')
                                
                                logger.info(f"Image generated with fallback model: {fallback_model}")
                                return True, f"Image generated successfully (using {fallback_model})"
                            except:
                                continue
            
            return False, "Model not available. Please try a different model."
        
        else:
            logger.error(f"API request failed with status {response.status_code}: {response.text}")
            return False, f"API request failed with status {response.status_code}"
    
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return False, "Request timed out. The model might be busy, please try again."
    
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
        return False, "Connection error. Please check your internet connection."
    
    except Exception as e:
        logger.error(f"Unexpected error in generate_image_from_text: {str(e)}")
        return False, f"Unexpected error: {str(e)}"
