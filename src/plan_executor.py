import json
import re

def parse_text_response(response):

    match = re.search(r"TEXT_RESPONSE\s*(.*?)\s*END_TEXT", response, re.S)

    if match:
        return match.group(1).strip()

    return None

def balance_braces(text):
    open_braces = text.count("{")
    close_braces = text.count("}")

    if close_braces < open_braces:
        text += "}" * (open_braces - close_braces)

    return text

def parse_action_plan(response):

    match = re.search(
        #r"BEGIN_JSON\s*(\{.*)",
        r"BEGIN_JSON\s*(\{.*?\})\s*END_JSON",
        response,
        re.DOTALL
    )

    if match:
        json_text = match.group(1)

        # remove END_JSON if present
        json_text = re.sub(r"END_JSON.*", "", json_text)

        # fix trailing commas
        json_text = re.sub(r",\s*}", "}", json_text)
        json_text = re.sub(r",\s*]", "]", json_text)

        # auto-close braces
        json_text = balance_braces(json_text)

        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            print("JSON parse error:", e)

    return None


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


def execute_plan(devices, action_plan):

    device_actions = action_plan.get("devices", {})

    for room, devs in device_actions.items():

        if room not in devices:
            continue

        for device, settings in devs.items():

            if device not in devices[room]:
                continue

            for key, value in settings.items():
                devices[room][device][key] = value