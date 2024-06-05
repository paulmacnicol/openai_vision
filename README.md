To configure, first, go to platform.openai.com and get an api key, enter it with your Homeassistant URL and Long Lived Token into settings.yaml in custom_components/openai_vision;

settings:
  HA_URL: "https://<your-homeassistant-url>"
  RESPONSE_DIR: "/config/custom_components/openai_vision/responses"
  MEDIA_DIR: "/config/custom_components/openai_vision/responses"
  HASS_TOKEN: "<long-lived-hass-token>"
  OPENAI_API_KEY: "openai-api-key>"
  MODEL_CHOICES:
    - gpt-3.5-turbo
    - gpt-4
    - gpt-4o
    - gpt4-turbo
    - gpt-3.5-turbo-16k

You can add/remove models to the list according to your package with OpenAI

Next, add the following to your configuration.yaml:

shell_command:
  run_openai_weather: "python3 /config/custom_components/openai_vision/image2text.py  --camera camera.webcam --prompt Weather --style BBC --model gpt-4o"
  run_openai_kitchen: "python3 /config/custom_components/openai_vision/image2text.py  --camera camera.kitchen_camera --prompt Kitchen --style Gordon_Ramsey --model gpt-4o"
  run_openai_grouphoto: "python3 /config/custom_components/openai_vision/image2text.py  --camera camera.living_room_camera --prompt GroupPhoto --style David_Attenborough --model gpt-4o"

openai_vision:
  sensors:
    - name: Kitchen
    - name: Weather
    - name: GroupPhoto

This sets up both the input (the shell command, with settings for model, prompt, style and camera entity) and the output sensor,
The "Prompt" name must match a prompt in prompts.yaml, and this must be the same name as in the shell_command, run_openai_<promptname> (without capitalisation) 

    
