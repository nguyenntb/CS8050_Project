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
    Immediate prompts produce action plans that can be executed immediately.
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
1. Only include devices that CHANGE because of the command.
2. DO NOT include devices that remain unchanged.
3. DO NOT output every device in the home.
4. JSON must be valid and fully closed.
5. Do not invent devices.
6. Use BEGIN_JSON and END_JSON exactly.

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

Your response must contain TWO parts:

1) A natural language response to the user in the following format:
TEXT_RESPONSE
<message>
END_TEXT

2) A JSON action plan for the smart home system. You MUST follow the exact JASON SCHEMA template above.

BEGIN_JSON
<your JSON matching the schema above>
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
    """
    Build a persistent prompt for automation routines with compact JSON output.
    """

    # Use compact JSON for available devices and sensors
    devices_json = json.dumps(devices, separators=(',', ':'))
    sensors_json = json.dumps(sensors, separators=(',', ':'))

    prompt = f"""
You are an AI that controls a smart home and creates automation routines from user commands.

User command:
{command_text}

Available devices (only use affected devices):
{devices_json}

Available sensors:
{sensors_json}

Instructions:
1. Only include devices that CHANGE because of the command.
2. DO NOT include devices that remain unchanged.
3. DO NOT output every device in the home.
4. JSON must be valid and fully closed.
5. Do not invent devices or sensors.
6. Use BEGIN_JSON and END_JSON exactly.

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

If no device can perform the action:

TEXT_RESPONSE
Sorry, I cannot perform that action with the available devices.
END_TEXT

BEGIN_JSON
{{"status":"failure"}}
END_JSON
"""

    return textwrap.dedent(prompt)


