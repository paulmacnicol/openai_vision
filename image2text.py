import requests
import json
import base64
import os
import argparse
import yaml
import logging

# Configure logging
log_file = '/config/custom_components/openai_vision/openai-vision.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

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

def encode_image(image_path):
    """Encode the image as base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_prompt_and_style(prompt_name, style_name=None):
    """Get the prompt and style text from the YAML file."""
    with open('/config/custom_components/openai_vision/prompts.yaml', 'r') as f:
        data = yaml.safe_load(f)
    prompt_text = data['prompts'].get(prompt_name, {}).get('description', '')
    style_text = data['styles'].get(style_name, {}).get('description', '') if style_name else ""
    logging.info(f"Loaded prompt for {prompt_name}: {prompt_text}")  # Log the loaded prompt
    if style_name:
        logging.info(f"Loaded style for {style_name}: {style_text}")  # Log the loaded style
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
    logging.info(f"Sending prompt to OpenAI API: {prompt_text}")  # Add logging for the prompt
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    response_data = response.json()
    logging.info(f"Received response from OpenAI API: {response_data}")  # Add logging for the response
    return response_data['choices'][0]['message']['content']

def write_response(response, file_path, prompt_text=None, image_path=None, settings=None, is_json=False):
    """Write the response to a JSON file."""
    if is_json:
        json_data = response
    else:
        image_link = f"{HA_URL}/local/{os.path.basename(image_path)}"
        json_data = {
            "response": response,
            "prompt": prompt_text,
            "image": image_link,
            "settings": settings
        }
    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)

def update_sensor(entity_id, state, attributes):
    """Update the sensor in Home Assistant with the given state and attributes."""
    url = f"{HA_URL}/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {HASS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "state": state,
        "attributes": attributes
    }
    try:
        response = requests.post(url, headers=headers, json=payload)  # Use json parameter to ensure proper JSON encoding
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"Failed to update sensor: {e}\nResponse: {response.text}")
        logging.error(f"Payload: {json.dumps(payload, indent=4)}")  # Add payload logging

def strip_code_blocks(response):
    """Strip code block formatting from the response."""
    if response.startswith("```json") and response.endswith("```"):
        response = response[7:-3].strip()
    elif response.startswith("```") and response.endswith("```"):
        response = response[3:-3].strip()
    return response

def extract_state_and_attributes_from_json(response):
    """Extract the state and attributes from the JSON response."""
    try:
        response = strip_code_blocks(response)  # Strip code block formatting if present
        response_json = json.loads(response)
        # Determine state and attributes based on the number of key-value pairs
        if len(response_json) == 1:
            state_key = list(response_json.keys())[0]
            state_value = response_json[state_key]
            return state_value, {"response": response_json}
        else:
            state = "Updated"
            attributes = response_json
            return state, attributes
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return "Unknown", {}

def main():
    """Main function to process the image."""
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--model', choices=MODEL_CHOICES, default='gpt-4o', help='Model to use for OpenAI API')
    parser.add_argument('--camera', required=True, help='Camera entity ID')
    parser.add_argument('--prompt', required=True, help='Prompt name')
    parser.add_argument('--style', help='Style name')
    parser.add_argument('--json', action='store_true', help='Indicate if the response is already in JSON format')

    args = parser.parse_args()

    logging.info(f"Command line arguments: model={args.model}, camera={args.camera}, prompt={args.prompt}, style={args.style}, json={args.json}")

    if args.json:
        image_path = os.path.join(MEDIA_DIR, f"{args.prompt}.jpg")
        response_path = os.path.join(RESPONSE_DIR, f"{args.prompt}.json")
        
        prompt_text = get_prompt_and_style(args.prompt, args.style).strip()
        take_snapshot(args.camera, image_path)
        response = get_response(image_path, args.model, prompt_text)
        state, attributes = extract_state_and_attributes_from_json(response)  # Extract state and attributes from JSON response
        update_sensor(f"sensor.openai_vision_{args.prompt.lower()}_response", state, attributes)  # Update sensor state and attributes
        print(response)  # Print only the response content
    else:
        combined_text = get_prompt_and_style(args.prompt, args.style)

        if not combined_text.strip():
            logging.error(f"Prompt '{args.prompt}' or style '{args.style}' not found in prompts.yaml")
            print(f"Prompt '{args.prompt}' or style '{args.style}' not found in prompts.yaml")
            return

        image_path = os.path.join(MEDIA_DIR, f"{args.prompt}.jpg")
        response_path = os.path.join(RESPONSE_DIR, f"{args.prompt}.json")

        take_snapshot(args.camera, image_path)
        logging.info(f"Combined prompt text: {combined_text}")  # Add logging for combined text
        response = get_response(image_path, args.model, combined_text)
        response = strip_code_blocks(response)

        settings = {
            "model": args.model,
            "style": args.style,
            "camera_entity": args.camera
        }

        write_response(response, response_path, combined_text, image_path, settings)
        json_data = {
            "response": response,
            "prompt": combined_text,
            "image": f"{HA_URL}/local/{os.path.basename(image_path)}",
            "settings": settings
        }
        update_sensor(f"sensor.openai_vision_{args.prompt.lower()}_response", "updated", json_data)  # Keep "updated" state for non-JSON responses
        print(json.dumps(json_data, indent=4))

if __name__ == "__main__":
    main()
