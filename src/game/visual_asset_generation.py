import os
import logging
from pathlib import Path
from flask import Flask, send_file, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import random
import json
from dotenv import load_dotenv
from openai import OpenAI
import requests
from io import BytesIO
import magic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
if not client.api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize Flask app
app = Flask(__name__)

# Asset directories
ASSET_DIR = Path(__file__).parent / 'assets'
BACKGROUND_DIR = ASSET_DIR / 'backgrounds'
CHARACTER_DIR = ASSET_DIR / 'characters'
CARD_DIR = ASSET_DIR / 'cards'

# Create directories if they don't exist
for directory in [BACKGROUND_DIR, CHARACTER_DIR, CARD_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

class VisualAssetGenerator:
    """Handles generation and caching of visual assets"""
    
    def __init__(self):
        self.client = client
        self.background_dir = BACKGROUND_DIR
        self.character_dir = CHARACTER_DIR
        self.card_dir = CARD_DIR
        
    def generate_ai_image(self, prompt: str, size: str = "1024x1024", style: str = "natural") -> Image.Image:
        """Generate an image using DALL-E 3"""
        try:
            # Check cache first
            cache_key = f"{prompt}_{size}_{style}".replace(" ", "_").lower()
            cache_path = self.background_dir / f"cache_{cache_key}.png"
            
            if cache_path.exists():
                logger.info(f"Using cached image: {cache_path}")
                return Image.open(cache_path)

            logger.info(f"Generating new image with prompt: {prompt}")
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                style=style,
                n=1
            )
            image_url = response.data[0].url
            
            # Download and cache the image
            try:
                response = requests.get(image_url, timeout=10)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                image.save(cache_path)
                logger.info(f"Image generated and cached: {cache_path}")
                return image
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to download image: {e}")
                return self._generate_fallback_image(prompt, size)
                
        except Exception as e:
            logger.error(f"AI image generation failed: {e}")
            return self._generate_fallback_image(prompt, size)

    def generate_background(self, theme: str) -> Image.Image:
        """Generate a background image"""
        cache_path = self.background_dir / f"{theme}.png"
        
        if cache_path.exists():
            return Image.open(cache_path)
            
        prompt = f"A detailed {theme} background for a fantasy game, dark and atmospheric, suitable for a dungeon crawler"
        image = self.generate_ai_image(prompt, size="1792x1024")
        
        if image:
            image.save(cache_path)
            return image
        else:
            return self._generate_procedural_background(theme)

    def generate_character_sprite(self, character_type: str) -> Image.Image:
        """Generate a character sprite"""
        cache_path = self.character_dir / f"{character_type}.png"
        
        if cache_path.exists():
            return Image.open(cache_path)
            
        prompt = f"A detailed {character_type} character sprite for a fantasy game, suitable for a dungeon crawler"
        image = self.generate_ai_image(prompt, size="512x512")
        
        if image:
            image.save(cache_path)
            return image
        else:
            return self._generate_procedural_character(character_type)

    def generate_card_art(self, card_name: str, card_type: str) -> Image.Image:
        """Generate card artwork"""
        cache_path = self.card_dir / f"{card_name}.png"
        
        if cache_path.exists():
            return Image.open(cache_path)
            
        prompt = f"A detailed {card_type} card artwork for {card_name} in a fantasy game, suitable for a card game"
        image = self.generate_ai_image(prompt, size="512x512")
        
        if image:
            image.save(cache_path)
            return image
        else:
            return self._generate_procedural_card(card_name, card_type)

    def _generate_procedural_background(self, theme: str) -> Image.Image:
        """Fallback procedural background generation"""
        img = Image.new('RGB', (1792, 1024), color='#2c2c2c')
        draw = ImageDraw.Draw(img)
        
        # Add some basic patterns
        for i in range(50):
            x = random.randint(0, 1791)
            y = random.randint(0, 1023)
            size = random.randint(2, 5)
            color = random.randint(40, 60)
            draw.ellipse([x, y, x+size, y+size], fill=(color, color, color))
            
        return img

    def _generate_procedural_character(self, character_type: str) -> Image.Image:
        """Fallback procedural character generation"""
        img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw basic character shape
        draw.rectangle([10, 10, 54, 54], fill='#4a4a4a')
        draw.rectangle([20, 20, 44, 44], fill='#666666')
        
        return img

    def _generate_procedural_card(self, card_name: str, card_type: str) -> Image.Image:
        """Fallback procedural card generation"""
        img = Image.new('RGB', (512, 512), color='#1a1a1a')
        draw = ImageDraw.Draw(img)
        
        # Draw card frame
        draw.rectangle([10, 10, 502, 502], outline='#gold')
        
        # Add card name
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        draw.text((20, 20), card_name, font=font, fill='white')
        
        return img

    def _generate_fallback_image(self, prompt: str, size: str) -> Image.Image:
        """Generate a fallback image when AI generation fails"""
        logger.info(f"Generating fallback image for: {prompt}")
        width, height = map(int, size.split('x'))
        img = Image.new('RGB', (width, height), color='#2c2c2c')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
            
        # Add text to indicate fallback
        draw.text((width//2 - 100, height//2), f"Fallback Image: {prompt}", font=font, fill='white')
        
        # Add some visual interest
        for i in range(50):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            size = random.randint(2, 5)
            color = random.randint(40, 60)
            draw.ellipse([x, y, x+size, y+size], fill=(color, color, color))
            
        return img

# Initialize asset generator
asset_generator = VisualAssetGenerator()

@app.route('/generate_background/<theme>')
def generate_background(theme):
    """Generate and serve a background image"""
    try:
        image = asset_generator.generate_background(theme)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        logger.error(f"Background generation failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate_character/<character_type>')
def generate_character(character_type):
    """Generate and serve a character sprite"""
    try:
        image = asset_generator.generate_character_sprite(character_type)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        logger.error(f"Character generation failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate_card/<card_name>')
def generate_card(card_name):
    """Generate and serve card artwork"""
    try:
        card_type = request.args.get('type', 'spell')
        image = asset_generator.generate_card_art(card_name, card_type)
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        logger.error(f"Card generation failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 