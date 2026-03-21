import json
import random
from urllib import response

import sys

from prompt_builder_improved import build_prompt
#from prompt_builder import build_prompt

from llm_runner import run_llm
from plan_executor import (
    parse_text_response,
    parse_action_plan,
    validate_action_plan,
    execute_plan
)


# ------------------------------------------------
# Utilities
# ------------------------------------------------

def load_json(path):
    """Load JSON file."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None


def print_section(title):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


# ------------------------------------------------
# Main Pipeline
# ------------------------------------------------

def run_command(command, devices, sensors):

    print_section("USER")
    print(command["command"])
    print("Type:", command["type"])

    # --------------------------------------------
    # Build prompt
    # --------------------------------------------
    prompt = build_prompt(command, devices, sensors)

    # --------------------------------------------
    # Run LLM
    # --------------------------------------------
    response = run_llm(prompt)

    print_section("LLM OUTPUT")
    print(response)

    # --------------------------------------------
    # Parse response
    # --------------------------------------------
    text_response = parse_text_response(response)

    print_section("SASHA")
    print(text_response)

    action_plan = parse_action_plan(response)

    if action_plan is None:
        print("\n Could not parse action plan.")
        return

    print_section("ACTION PLAN")
    print(json.dumps(action_plan, indent=2))

    # --------------------------------------------
    # Handle failure
    # --------------------------------------------
    if action_plan["status"] == "failure":
        print("\n Command rejected by LLM.")
        return

    # --------------------------------------------
    # Validate devices
    # --------------------------------------------
    if not validate_action_plan(devices, action_plan):
        print("\n Invalid action plan (device does not exist).")
        return

    # --------------------------------------------
    # Execute plan
    # --------------------------------------------
    #execute_plan(devices, action_plan)

    #print_section("UPDATED DEVICES STATE")
    #print(json.dumps(devices, indent=2))

# ------------------------------------------------
# Entry Point
# ------------------------------------------------

def main():
    # Default values
    command_index = 0
    home_file = "data/home1.json"

    # --------------------------------------------
    # Parse CLI arguments
    # --------------------------------------------
    if len(sys.argv) > 1:
        try:
            command_index = int(sys.argv[1])
        except ValueError:
            print(f"Invalid command index '{sys.argv[1]}', using 0")

    if len(sys.argv) > 2:
        home_file = sys.argv[2]

    # --------------------------------------------
    # Load data
    # --------------------------------------------
    devices = load_json(home_file)
    sensors = load_json("data/sensors.json")
    commands = load_json("data/commands.json")

    if not devices or not sensors or not commands:
        print("Error loading data files.")
        return

    # --------------------------------------------
    # Validate command index
    # --------------------------------------------
    if command_index < 0 or command_index >= len(commands):
        print(f"Index {command_index} out of range, using 0")
        command_index = 0

    command = commands[command_index]

    # --------------------------------------------
    # Run pipeline
    # --------------------------------------------
    run_command(command, devices, sensors)


if __name__ == "__main__":
    main()