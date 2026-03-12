import json
import re

def parse_text_response(llm_output):
    """
    Extract the assistant message before BEGIN_JSON.
    """

    parts = llm_output.split("BEGIN_JSON")

    if len(parts) == 0:
        return ""

    return parts[0].strip()

def parse_action_plan(llm_output):
    """
    Extract JSON action plan between BEGIN_JSON and END_JSON.
    """

    pattern = r"BEGIN_JSON\s*(.*?)\s*END_JSON"
    match = re.search(pattern, llm_output, re.DOTALL)

    if not match:
        return None

    json_str = match.group(1)

    return json.loads(json_str)


def validate_action_plan(home, action_plan):
    """
    Ensure all rooms and devices in the action plan exist in the home template.
    """

    device_updates = action_plan.get("devices", {})

    for room, devices in device_updates.items():

        # check room exists
        if room not in home:
            return False

        for device in devices:

            # check device exists in that room
            if device not in home[room]:
                return False

    return True


def execute_plan(home, action_plan):
    """
    Apply device changes directly to the devices JSON.
    """

    device_updates = action_plan.get("devices", {})

    for room, devices in device_updates.items():

        for device, settings in devices.items():

            for key, value in settings.items():
                home[room][device][key] = value