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
            'id': 'stabilityai/stable-diffusion-2-1',
            'name': 'Stable Diffusion 2.1',
            'description': 'High-quality general purpose model'
        },
        {
            'id': 'runwayml/stable-diffusion-v1-5',
            'name': 'Stable Diffusion 1.5',
            'description': 'Classic stable diffusion model'
        },
        {
            'id': 'CompVis/stable-diffusion-v1-4',
            'name': 'Stable Diffusion 1.4',
            'description': 'Original stable diffusion model'
        },
        {
            'id': 'prompthero/openjourney',
            'name': 'OpenJourney',
            'description': 'Midjourney-style artistic model'
        },
        {
            'id': 'wavymulder/Analog-Diffusion',
            'name': 'Analog Diffusion',
            'description': 'Analog photography style'
        },
        {
            'id': 'hakurei/waifu-diffusion',
            'name': 'Waifu Diffusion',
            'description': 'Anime and manga style images'
        },
        {
            'id': 'nitrosocke/Arcane-Diffusion',
            'name': 'Arcane Diffusion',
            'description': 'Arcane TV series art style'
        },
        {
            'id': 'dreamlike-art/dreamlike-diffusion-1.0',
            'name': 'Dreamlike Diffusion',
            'description': 'Dreamy, artistic style'
        },
        {
            'id': 'prompthero/midjourney-v4-diffusion',
            'name': 'Midjourney v4',
            'description': 'High-quality artistic generation'
        },
        {
            'id': 'nitrosocke/redshift-diffusion',
            'name': 'Redshift Diffusion',
            'description': '3D rendered style images'
        },
        {
            'id': 'wavymulder/portraitplus',
            'name': 'Portrait Plus',
            'description': 'Professional portrait photography'
        },
        {
            'id': 'dallinmackay/Van-Gogh-diffusion',
            'name': 'Van Gogh Diffusion',
            'description': 'Van Gogh painting style'
        },
        {
            'id': 'nitrosocke/spider-verse-diffusion',
            'name': 'Spider-Verse',
            'description': 'Spider-Man animated movie style'
        },
        {
            'id': 'wavymulder/collage-diffusion',
            'name': 'Collage Diffusion',
            'description': 'Collage art style'
        },
        {
            'id': 'stabilityai/stable-diffusion-xl-base-1.0',
            'name': 'Stable Diffusion XL',
            'description': 'Latest high-resolution model'
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
        api_key = os.getenv("HUGGINGFACE_API_KEY", "hf_demo_key")
        
        if not api_key or api_key == "hf_demo_key":
            logger.warning("Using demo API key - may have rate limits")
        
        # Hugging Face Inference API endpoint
        api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 50,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }
        
        logger.info(f"Generating image with model: {model_name}, prompt: {prompt[:100]}...")
        
        # Make request to Hugging Face API
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            # Check if response is an image
            if response.headers.get('content-type', '').startswith('image/'):
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
