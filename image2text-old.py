import requests
import json
import base64
import os
import argparse
import yaml

# Load settings from YAML
with open('/config/custom_components/openai_vision/settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

HA_URL = settings['settings']['HA_URL']
RESPONSE_DIR = settings['settings']['RESPONSE_DIR']
MEDIA_DIR = settings['settings']['MEDIA_DIR']
HASS_TOKEN = settings['settings']['HASS_TOKEN']
OPENAI_API_KEY = settings['settings']['OPENAI_API_KEY']
MODEL_CHOICES = settings['settings']['MODEL_CHOICES']

# Headers for authentication
headers = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "content-type": "application/json",
}

def take_snapshot(camera_entity_id, image_path):
    """Take a snapshot from the specified camera."""
    snapshot_url = f"{HA_URL}/api/services/camera/snapshot"
    data = {
        "entity_id": camera_entity_id,
        "filename": image_path
    }
    response = requests.post(snapshot_url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
#    print(f"Snapshot saved to {image_path}")

def encode_image(image_path):
    """Encode the image as base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_prompt_and_style(prompt_name, style_name):
    """Get the prompt and style text from the YAML file."""
    with open('/config/custom_components/openai_vision/prompts.yaml', 'r') as f:
        data = yaml.safe_load(f)
    prompt_text = data['prompts'][prompt_name]['description']
    style_text = data['styles'][style_name]['description']
    return f"{prompt_text} {style_text}"

def get_response(image_path, model, prompt_text):
    """Send the snapshot to the OpenAI API and get the response."""
    base64_image = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    response_data = response.json()
    return response_data['choices'][0]['message']['content']

def write_response(response, file_path):
    """Write the response to a file."""
    with open(file_path, "w") as file:
        file.write(response)

def main():
    """Main function to process the image."""
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--model', choices=MODEL_CHOICES, default='gpt-4o', help='Model to use for OpenAI API')
    parser.add_argument('--camera', required=True, help='Camera entity ID')
    parser.add_argument('--prompt', required=True, help='Prompt name')
    parser.add_argument('--style', required=True, help='Style name')

    args = parser.parse_args()

    combined_text = get_prompt_and_style(args.prompt, args.style)

    image_path = os.path.join(MEDIA_DIR, f"{args.prompt}.jpg")
    response_path = os.path.join(RESPONSE_DIR, f"{args.prompt}.txt")

    take_snapshot(args.camera, image_path)
    response = get_response(image_path, args.model, combined_text)
    write_response(response, response_path)
#    print(f"Response saved to {response_path}")
#    print("Response:\n")
    print(response)

if __name__ == "__main__":
    main()
