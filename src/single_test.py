import json
import random

from prompt_builder import build_prompt
from llm_runner import run_llm
from plan_executor import (
    parse_text_response,
    parse_action_plan,
    validate_action_plan,
    execute_plan
)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def main():   

    # ----------------------------
    # Load data
    # ----------------------------
    devices = load_json("data/home3.json")
    sensors = load_json("data/sensors.json")
    commands = load_json("data/commands.json")


    # ----------------------------
    # Pick one command
    # ----------------------------
    command = random.choice(commands)

    print("Command:")
    print(command["command"])
    print("Command type:", command["type"])
    print()

    # ----------------------------
    # Build prompt
    # ----------------------------
    prompt = build_prompt(command, devices, sensors)

    # ----------------------------
    # Run LLM
    # ----------------------------
    response = run_llm(prompt)

    print("\nLLM OUTPUT")
    print("-----------------------------------")
    print(response)
    print("-----------------------------------")

    text_response = parse_text_response(response)

    print("\nSASHA:")
    print(text_response)

    action_plan = parse_action_plan(response)
    if action_plan is None:
        print("Could not parse action plan.")
        return
    
    print("\nACTION PLAN")
    print(action_plan)
    
    if action_plan["status"] == "failure":
        print("\nCommand rejected by LLM.")
        return

    if not validate_action_plan(devices, action_plan):
        print("\nInvalid action plan (device does not exist).")
        return

    execute_plan(devices, action_plan)

    print("\nUPDATED DEVICES STATE")
    print(json.dumps(devices, indent=2))
    

if __name__ == "__main__":
    main()