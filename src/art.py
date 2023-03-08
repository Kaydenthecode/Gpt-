import os
import json
import openai
from pathlib import Path
from base64 import b64decode
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# generate 512x512 image and save to a file
# return the path of the image as a str
async def draw(prompt) -> str:
    DATA_DIR = Path.cwd() / "json_files"
    DATA_DIR.mkdir(exist_ok=True)
    
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="b64_json",
    )

    file_name = DATA_DIR / f"{prompt[:5]}-{response['created']}.json"

    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)
    
    path = str(convert(file_name))

    buy_image()

    return path

 
 # tracks remaining free credit in openai account
def count_remaining_images():
    with open("remaining_images.txt", "r") as f:
        remaining_images = f.read()
    return int(remaining_images)

# decreases value in "remaining_images" file
def buy_image():
    remaining_images = count_remaining_images()
    
    with open("remaining_images.txt", "w") as f:
        f.write(str(remaining_images-1))


# code stolen from https://realpython.com/generate-images-with-dalle-openai-api/
def convert(path):
    DATA_DIR = Path.cwd() / "responses"
    JSON_FILE = DATA_DIR / path
    IMAGE_DIR = Path.cwd() / "images"
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(JSON_FILE, mode="r", encoding="utf-8") as file:
        response = json.load(file)
        
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
    
        with open(image_file, mode="wb") as png:
            png.write(image_data)
    return image_file