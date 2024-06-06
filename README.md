OpenAI Vision Integration for Home Assistant

OpenAI Vision Integration for Home Assistant
============================================

Overview
--------

The OpenAI Vision Integration is a custom component for Home Assistant that leverages OpenAI's GPT models to analyze images captured by your home cameras. This integration can generate insightful descriptions, identify objects, and even add a touch of humor to your snapshots. The results are saved in JSON format and can be used to update Home Assistant sensors.
This integration allows you to add hundreds of sensors to your home assistant installation, using existing security cameras or cheap webcams. Add a sensor to check if the beds are made and the dishes are done, and cut off the kids internet until they are. Remind me if I havent got my Rubbish bins out on collection day. Let me know if I have clothes on the line and its going to rain. And so on - theres a huge number of opportunities we can exploit with this software, so I've tried to keep it as straightforward as possible to modify, and I look forward to hearing your suggestions and implementations. 

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

Define your prompts and styles in `/config/custom_components/openai_vision/prompts.yaml. Below are just examples,the actual prompts.yaml has much longer prompts. Customise them to suit your environment`:

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

Trigger this command from the Developer Tools screen, an automation, or a Lovelace button to run the image processing script. The output is a weather report in the style of a BBC reporter, based on the photo from the camera specified.

The response is then saved as an attribute in sensor.openai_vision_weather_response. The response includes the prompt, model, camera, and style in the json attributes, making it easy to present the results or process further

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

The OpenAI Vision integration updates Home Assistant sensors with the analyzed data. Depending on whether the `--json` flag is used, the sensor output differs:

*   **Without `--json` Flag**: The response is treated as plain text, suitable for notifications, TTS, or display on a dashboard. The text is saved directly in the sensor's state.
*   **With `--json` Flag**: The response is treated as a JSON object. If it reports a single entity (e.g., a light bulb), the sensor's state will show "on" or "off", matching the current state of the light bulb. If multiple objects are being monitored, the information is saved as attributes in the sensor.

### Example Sensor Template Configuration

The following template sensor configuration extracts specific attributes from the JSON response and presents them as individual entities in Home Assistant:

    sensor:
      - platform: template
        sensors:
          lightsensor_livingroom_response:
            friendly_name: "Lightsensor Livingroom Response"
            value_template: "{{ states.sensor.openai_vision_lightsensor_livingroom_response.state }}"
            attribute_templates:
              dj_lights: "{{ state_attr('sensor.openai_vision_lightsensor_livingroom_response', 'lightsensor_livingroom.dj_lights') }}"
              ceiling_lights: "{{ state_attr('sensor.openai_vision_lightsensor_livingroom_response', 'lightsensor_livingroom.ceiling_lights') }}"

*   **`value_template`**: Extracts the main state from the JSON response.
*   **`attribute_templates`**: Extracts specific attributes from the JSON response and presents them as key-value pairs.

Logging
-------

Logs are stored in `/config/custom_components/openai_vision/openai-vision.log`. The logging includes information about prompts, API responses, and errors.

Prompts and Styles
------------------

The `prompts.yaml` file contains various prompts and styles that define how the images should be analyzed. Here are the main categories that are included, you can create your own or modify these to suit your requirements. Just remember that the prompt name must match in prompts.yaml, and the --prompt in the shell command, and the name of the sensor that receives the data  - see the examples included

### Prompts

*   **Weather**: Summarize the weather in the picture.
*   **Curtains**: Identify if the curtains are open or closed.
*   **Kitchen**: Rate the cleanliness of the kitchen from 1 to 10 and describe it.
*   **LivingRoom**: Describe the ambience of the room and suggest 3 appropriate songs.
*   **Garage**: List all items you see in the picture.
*   **GroupPhoto**: Humorously describe the people in the group photo.
*   **Aircon**: Check if the air conditioner is on or off.
*   **LivingroomSensor**: Identify and count items in the room and present the data in JSON.
*   **wherearemyglasses**: Find the glasses in the photo.
*   **bedstatus**: Check if the bed is made or identify the person's activity.
*   **lightsensor\_livingroom**: Determine the status of ceiling and DJ lights in JSON.

### Styles

*   **BBC**: Formal and correct, suitable for reading aloud.
*   **Gordon\_Ramsey**: Cheeky and candid, in the style of the famous chef.
*   **Snoop\_Dogg**: Written in the character of Snoop Dogg.
*   **David\_Attenborough**: In the style of David Attenborough.
*   **Jarvis**: In the style of Jarvis from Ironman.
*   **json**: Response in simple JSON format with no additional comments.
