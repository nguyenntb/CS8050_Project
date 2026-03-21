import json
import textwrap


def build_prompt(command, devices, sensors):

    if command["type"] == "immediate":
        return build_immediate_prompt(command["command"], devices)

    return build_persistent_prompt(command["command"], devices, sensors)


def build_immediate_prompt(command_text, devices):

    prompt = f"""
You are an AI that controls a smart home with ONLY the following devices:

Devices:
{devices}

You receive a user command and assign settings to devices in response.
Command:
{command_text}

Strictly follow these intructions:
- Use devices with its common functions. For example, use robot vacumn to clean, 
use thermostat to change temperature.
- If a device is not listed, it DOES NOT EXIST. Do not invent devices.
- If the room does NOT have the device, do not add devices to the room.
- If multiple devices help, include them.
- Only include devices and the room they are in in the JSON action plan. 
DO NOT include devices that remain unchanged.
- JSON must be valid, fully closed and contain NO trailing commas.
- If no listed device can achieve the goal, return failure. Do not force other devices to perform functions
that they are not supposed to do.

Your response must contain TWO parts:

1) A natural language response to the user in the following format:
TEXT_RESPONSE
<message>
END_TEXT

2) A JSON action plan for the smart home system. 

BEGIN_JSON
<your JSON matching the template>
END_JSON

You MUST follow the exact JASON SCHEMA template.

JSON SCHEMA:

BEGIN_JSON
{{
  "status": "success",
  "devices": {{
      "<room>": {{
          "<device>": {{
          }}
      }}
  }},
  "explanation": "<string describing why devices were set this way>"
}}
END_JSON

An Example (user turns on a lamp):

TEXT_RESPONSE
The living room lamp has been turned on.
END_TEXT

BEGIN_JSON
{{"status":"success","devices":{{"livingroom":{{"lamp":{{"on":true,"brightness":100}}}}}},"explanation":"Lamp turned on."}}
END_JSON

If no device can perform the action:

TEXT_RESPONSE
Sorry, I cannot perform that action with the available devices.
END_TEXT

BEGIN_JSON
{{"status":"failure"}}
END_JSON
"""

    return textwrap.dedent(prompt)


def build_persistent_prompt(command_text, devices, sensors):

    prompt = f"""
You are an AI that controls a smart home with ONLY the following devices and sensors:

Devices:
{devices}

Sensors:
{sensors}

Your task is to create automation routines from user commands.

Command:
{command_text}

Strictly follow these intructions:
- Use devices with its common functions. For example, use robot vacumn to clean, 
use thermostat to change temperature.
- If a device is not listed, it DOES NOT EXIST. Do not invent devices.
- If the room does NOT have the device, do not add devices to the room.
- Triggers MUST use ONLY sensors listed above. Do not invent sensors.
- If multiple devices/sensors help, include them.
- Only include devices and the room they are in in the JSON action plan. 
DO NOT include devices that remain unchanged.
- JSON must be valid, fully closed and contain NO trailing commas.
- If no listed device can achieve the goal, return failure. Do not force other devices to perform functions
that they are not supposed to do.

Your response must contain TWO parts:

1) A natural language response to the user in the following format:
TEXT_RESPONSE
<your human-readable message explaining the automation>
END_TEXT

2) A JSON action plan for the smart home system. 

BEGIN_JSON
<your JSON matching the template>
END_JSON

You MUST follow the exact JASON SCHEMA template below.
JSON SCHEMA:

BEGIN_JSON
{{
  "status": "success",
  "trigger": {{
      "<room>": {{
          "<sensor>": true | false
      }}
  }},
  "devices": {{
      "<room>": {{
          "<device>": {{
            "<setting>":<value>
          }}
      }}
  }},
  "explanation": "<string describing why these devices were set this way>"
}}
END_JSON

Example automation:

TEXT_RESPONSE
Lights will turn off when motion is detected.
END_TEXT

BEGIN_JSON
{{"status":"success","trigger":{{"livingroom":{{"motion":true}}}},"devices":{{"livingroom":{{"lamp":{{"on":false,"brightness":0}}}}}},"explanation":"Turn off lamp when motion detected."}}
END_JSON


If no device can perform the action:

TEXT_RESPONSE
Sorry, I cannot perform that action with the available devices.
END_TEXT

BEGIN_JSON
{{"status":"failure"}}
END_JSON
"""

    return textwrap.dedent(prompt)