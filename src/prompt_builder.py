import json
import textwrap


def build_prompt(command, devices, sensors):
    """
    Build the correct prompt depending on goal.
    """

    if command["type"] == "immediate":
        return build_immediate_prompt(command["command"], devices)

    else:
        return build_persistent_prompt(command["command"], devices, sensors)


def build_immediate_prompt(command_text, devices):
    """
    Prompt for immediate goal.
    Immediate prompts produce action plans that can be execuated immediately.
    """

    devices_json = json.dumps(devices, indent=2)

    prompt = f"""
You are an AI that controls a smart home.

You receive a user command and assign settings to devices in response.

User command:
{command_text}

Available devices:
{devices_json}

Instructions:
- Only use devices that exist in the device list.
- Do not invent devices.
- Return ONLY the response in the format specified below.
- Do not add any additional text outside the specified sections.
- Devices must always be nested inside their room.

Correct format:
devices -> room -> device -> settings

Your response must contain TWO parts:

1) A natural language response to the user.

2) A JSON action plan for the smart home system.

Format:

TEXT_RESPONSE
<your message to the user>
END_TEXT

If there are devices relevant to the user command, respond exactly in the format:

BEGIN_JSON
{{
    "status": "success",
    "devices": {{}},
    "explanation": "Explain briefly why these devices satisfy the command."
}}
END_JSON

If no relevant devices exist, respond exactly in the format:

BEGIN_JSON
{{ "status": "failure" }}
END_JSON
"""

    return textwrap.dedent(prompt)


def build_persistent_prompt(command_text, devices, sensors):
    """
    Prompt for persistent goal.
    Persistent prompts produce automation routines.
    """

    devices_json = json.dumps(devices, indent=2)
    sensors_json = json.dumps(sensors, indent=2)

    prompt = f"""
You are an AI that controls a smart home.

You receive a user command and create an automation routine in response.

User command:
{command_text}

Available devices:
{devices_json}

Available sensors:
{sensors_json}

Instructions:
- Only use devices listed in the devices JSON.
- Only use sensors listed in the sensors JSON.
- Do not invent devices or sensors.
- Return ONLY the response in the format specified below.
- Do not add any additional text outside the specified sections.
- Devices must always be nested inside their room.

Correct format:
devices -> room -> device -> settings

Your response must contain TWO parts:

1) A natural language response to the user. The response must be exactly in the format:

TEXT_RESPONSE
<your message to the user>
END_TEXT

2) A JSON action plan for the smart home system.

If there are devices relevant to the user command, response with a JSON object that 
describes a sensor trigger and how you would change the devices based on that trigger.
Respond exactly in the format:

BEGIN_JSON
{{
    "status": "success",
    "trigger": {{}},
    "devices": {{}},
    "explanation": "Explain briefly why these devices satisfy the command."
}}
END_JSON

If there are no devices relevant to the user command, respond exactly in the format:

BEGIN_JSON
{{ "status": "failure" }}
END_JSON
"""

    return textwrap.dedent(prompt)


