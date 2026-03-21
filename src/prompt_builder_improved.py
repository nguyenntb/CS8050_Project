import json
import textwrap


DEVICE_CAPABILITIES = """
Device settings reference:
light -> {"on": true/false, "brightness": 0-100}
curtains -> {"open": true/false}
thermostat -> {"temperature": 65-80}
speaker -> {"on": true/false, "volume": 0-100}
tv -> {"on": true/false, "channel": number, "volume": 0-100}
vacuum -> {"on": true/false}
humidifier -> {"on": true/false, "humidity": 0-100}
microwave -> {"on": true/false, "time": seconds}
lock -> {"locked": true/false}
camera -> {"on": true/false}
"""




def build_device_inventory(devices):

    inventory = []

    for room, devs in devices.items():
        for name, info in devs.items():
            inventory.append({
                "room": room,
                "device": name,
                "type": info["type"]
            })

    return json.dumps(inventory, indent=2)


def build_prompt(command, devices, sensors):

    if command["type"] == "immediate":
        return build_immediate_prompt(command["command"], devices)

    return build_persistent_prompt(command["command"], devices, sensors)


def build_immediate_prompt(command_text, devices):

    inventory = build_device_inventory(devices)

    prompt = f"""
You are an AI that controls a smart home with the following devices:
{devices}

You receive a user command and assign settings to devices in response.
Command:
{command_text}


Your response must contain TWO parts:

1) A natural language response to the user in the following format:
TEXT_RESPONSE
<message>
END_TEXT

2) A JSON action plan for the smart home system. You MUST follow the exact JASON SCHEMA template.

BEGIN_JSON
<your JSON matching the specified schema>
END_JSON

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


Strictly follow these intructions:
- If a device is not listed, it DOES NOT EXIST. Do not invent devices.
- Only use the devices that can meet the user's intended goal. For example, use robot vacumn to clean, 
use thermostat to change temperature.
- Only include devices that CHANGE because of the command in the JSON action plan. 
DO NOT include devices that remain unchanged.
- JSON must be valid, fully closed and contain NO trailing commas.
- If no listed device can achieve the goal, return failure.


"""

    return textwrap.dedent(prompt)


def build_persistent_prompt(command_text, devices, sensors):

    sensors_json = json.dumps(sensors, indent=2)
    inventory = build_device_inventory(devices)


    prompt = f"""
You are an AI that controls a smart home and creates automation routines from user commands.

Command:
{command_text}

Sensors:
{sensors_json}

Device inventory (ONLY these devices exist in the home):
{inventory}

{DEVICE_CAPABILITIES}

Guidelines:
- Identify the user's goal.
- Choose devices that help achieve the goal.
- If multiple devices help, include them.
- ONLY use devices from the inventory above. Do not invent devices.
- Only include devices that CHANGE because of the command. DO NOT include devices that remain unchanged.
- TEXT_RESPONSE must mention the devices used.
- JSON must be valid, fully closed and contain NO trailing commas..
- Use BEGIN_JSON and END_JSON exactly.
- If no listed device can achieve the goal, return failure.

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

Your response must contain TWO parts:

1) A natural language response to the user in the following format:
TEXT_RESPONSE
<your human-readable message explaining the automation>
END_TEXT

2) A JSON action plan for the smart home system. You MUST follow the exact JASON SCHEMA template above.

BEGIN_JSON
<your JSON matching the compact schema above>
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