import asyncio
from random import randint
from PIL import Image
import requests
import os
from dotenv import dotenv_values
from time import sleep

# Load API key
env_vars = dotenv_values(".env")
HuggingFaceAPIKey = env_vars.get("HuggingFaceAPIKey")

# Define the folder for generated images
BASE_FOLDER = "Generated_Images"
os.makedirs(BASE_FOLDER, exist_ok=True)

def open_images(prompt):
    folder_path = os.path.join(BASE_FOLDER, prompt.replace(" ", "_"))
    files = [os.path.join(folder_path, f"{prompt.replace(' ', '_')}{i}.jpg") for i in range(1, 5)]
    
    for image_path in files:
        try:
            img = Image.open(image_path)
            print(f"Opening Image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open image: {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_image(prompt: str):
    folder_path = os.path.join(BASE_FOLDER, prompt.replace(" ", "_"))
    os.makedirs(folder_path, exist_ok=True)
    
    tasks = []
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    
    image_bytes_list = await asyncio.gather(*tasks)
    
    for i, image_bytes in enumerate(image_bytes_list):
        with open(os.path.join(folder_path, f"{prompt.replace(' ', '_')}{i + 1}.jpg"), "wb") as f:
            f.write(image_bytes)

def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)

while True:
    try:
        with open(r"Frontend/Files/ImageGeneration.data", "r") as f:
            data = f.read().strip()
        
        if not data:
            sleep(1)
            continue
        
        Prompt, Status = data.split(",")
        
        if Status.strip().lower() == "true":
            print(f"Generating images for: {Prompt}")
            GenerateImages(Prompt)
            
            with open(r"Frontend/Files/ImageGeneration.data", "w") as f:
                f.write("False, False")
            break
        else:
            sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        sleep(1)
