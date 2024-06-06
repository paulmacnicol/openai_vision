OpenAI Vision Integration for Home Assistant

OpenAI Vision Integration for Home Assistant
============================================

Overview
--------

The OpenAI Vision Integration is a custom component for Home Assistant that leverages OpenAI's GPT models to analyze images captured by your home cameras. This integration can generate insightful descriptions, identify objects, and even add a touch of humor to your snapshots. The results are saved in JSON format and can be used to update Home Assistant sensors.

Features
--------

*   **Image Analysis**: Automatically captures images from your cameras and analyzes them using OpenAI's GPT models.
*   **Flexible Prompts and Styles**: Customize the analysis with various prompts and styles defined in a YAML file.
*   **Home Assistant Integration**: Updates sensors in Home Assistant with the analyzed data.
*   **JSON Response Handling**: Outputs responses in JSON format for easy integration with other Home Assistant components.

Installation
------------

1.  **Clone the Repository**:
    
        git clone https://github.com/paulmacnicol/openai_vision.git
    
2.  **Copy Custom Component**:
    
        mv openai_vision /config/custom_components/
    
3.  **Alternatively, Download the ZIP File**:
    *   Download the ZIP file from the [GitHub repository](https://github.com/paulmacnicol/openai_vision.git).
    *   Extract the contents and move the `openai_vision` directory to your Home Assistant's custom components directory:
        
            mv openai_vision /config/custom_components/
        
4.  **Install Dependencies**:
    
        pip install requests pyyaml
    

Configuration
-------------

### Edit Settings

Configure your settings in `/config/custom_components/openai_vision/settings.yaml`:

    settings:
      HA_URL: "https://<your-homeassistant-url>"
      RESPONSE_DIR: "/config/custom_components/openai_vision/responses"
      MEDIA_DIR: "/config/custom_components/openai_vision/responses"
      HASS_TOKEN: "<long-lived-hass-token>"
      OPENAI_API_KEY: "<openai-api-key>"
      MODEL_CHOICES:
        - gpt-3.5-turbo
        - gpt-4
        - gpt-4o
        - gpt4-turbo
        - gpt-3.5-turbo-16k

### Prompts and Styles

Define your prompts and styles in `/config/custom_components/openai_vision/prompts.yaml`:

    models:
      - gpt-4o
      - gpt-4-turbo
      - gpt-4
      - gpt-3.5-turbo
    
    prompts:
      Weather:
        description: "Summarize the weather in the picture."
      Curtains:
        description: "Identify if the curtains are open or closed."
      Kitchen:
        description: "Rate the cleanliness of the kitchen from 1 to 10 and describe it."
      LivingRoom:
        description: "Describe the ambience of the room and suggest 3 appropriate songs."
      Garage:
        description: "List all items you see in the picture."
      GroupPhoto:
        description: "Humorously describe the people in the group photo."
      Aircon:
        description: "Check if the air conditioner is on or off."
      LivingroomSensor:
        description: "Identify and count items in the room and present the data in JSON."
      wherearemyglasses:
        description: "Find the glasses in the photo."
      bedstatus:
        description: "Check if the bed is made or identify the person's activity."
      lightsensor_livingroom:
        description: "Determine the status of ceiling and DJ lights in JSON."
    
    styles:
      BBC:
        description: "Formal and correct, suitable for reading aloud."
      Gordon_Ramsey:
        description: "Cheeky and candid, in the style of the famous chef."
      Snoop_Dogg:
        description: "Written in the character of Snoop Dogg."
      David_Attenborough:
        description: "In the style of David Attenborough."
      Jarvis:
        description: "In the style of Jarvis from Ironman."
      json:
        description: "Response in simple JSON format with no additional comments."

### Add to `configuration.yaml`

Register the custom component and configure its settings in your Home Assistant `configuration.yaml`:

    shell_command:
      run_openai_weather: "python3 /config/custom_components/openai_vision/image2text.py --camera camera.webcam --prompt Weather --style BBC --model gpt-4o"
    
    openai_vision:
      sensors:
        - name: Weather

### Explanation of `configuration.yaml` Components

*   **`shell_command`**: Defines shell commands to run the image processing script with various prompts and styles. The `run_openai_weather` command uses the `Weather` prompt from `prompts.yaml`, `camera.webcam` as the camera entity, `BBC` as the style, and `gpt-4o` as the model. The name `Weather` must match the `--prompt` argument and the prompt defined in `prompts.yaml`.
*   **`openai_vision`**: Defines the sensors that will be created by the integration. The `name` of the sensor must match the `--prompt` value used in the shell command.

### Detailed Configuration Options

*   **Camera**: Specify the camera entity ID (e.g., `camera.webcam`).
*   **Model**: Select the OpenAI model to use (e.g., `gpt-4o`).
*   **Style**: Choose the style for the response (e.g., `BBC`).
*   **Prompt**: Define the prompt from `prompts.yaml` (e.g., `Weather`).

Usage
-----

Run the script with the desired parameters by invoking the shell commands defined in the `configuration.yaml` from the Home Assistant Developer Tools screen, an automation, or a Lovelace button.

Example shell command invocation:

    shell_command:
      run_openai_weather: "python3 /config/custom_components/openai_vision/image2text.py --camera camera.webcam --prompt Weather --style BBC --model gpt-4o"

Trigger this command from the Developer Tools screen, an automation, or a Lovelace button to run the image processing script.

Required Tokens and Information
-------------------------------

### Home Assistant Long-Lived Access Token

1.  Go to your Home Assistant user profile.
2.  Scroll down to the "Long-Lived Access Tokens" section.
3.  Click on "Create Token", provide a name, and copy the token.

### Home Assistant URL

The URL of your Home Assistant instance (e.g., `https://your-home-assistant-url`). This URL does not require external access.

### OpenAI API Key

1.  Sign up for an OpenAI account at [OpenAI](https://platform.openai.com/).
2.  Go to the API keys section and generate a new API key.
3.  Note that using OpenAI's API might require credits, so ensure your account has sufficient balance.

Sensor Integration
------------------

The OpenAI Vision integration updates Home Assistant sensors with the analyzed data. Depending on whether the