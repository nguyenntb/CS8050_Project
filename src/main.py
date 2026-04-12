import json
import os
import time

from prompt_builder_improved import build_prompt
from llm_runner import run_llm


MODEL_TAG = "gwen"   # change to "llama"
OUTPUT_FILE = "/content/drive/MyDrive/llm_results/results_gwen.json"
#create folder if it doesn't exist
import os
os.makedirs("/content/drive/MyDrive/llm_results", exist_ok=True)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def main():
    
    
    # Load data
    commands = load_json("data/commands.json")
    sensors = load_json("data/sensors.json")

    homes = [
        ("home_1", load_json("data/home1.json")),
        ("home_2", load_json("data/home2.json")),
        ("home_3", load_json("data/home3.json"))
    ]

    # Resume support
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            results = json.load(f)
        print(f"Resuming from {len(results)} results")
    else:
        results = []

    completed = set(
        (r["command"], r.get("home"))
        for r in results
    )

    total_runs = len(commands) * len(homes)
    current_run = len(results)

    for home_name, devices in homes:
        print(f"\n===== Testing with home : {home_name} =====")

        for cmd in commands:

            key = (cmd["command"], home_name)
            if key in completed:
                continue

            print(f"\nCommand: {cmd['command']}")

            # ----------------------------------------
            # Run LLM
            # ----------------------------------------
            start_time = time.time()
            try:
                prompt = build_prompt(cmd, devices, sensors)
                response = run_llm(prompt)

            except Exception as e:
                response = f"ERROR: {str(e)}"

            latency = time.time() - start_time

            # ----------------------------------------
            # Save results
            # ----------------------------------------
            result = {
                "command": cmd["command"],
                "type": cmd.get("type"),
                "home": home_name,   # needed for resume correctness
                "raw_output": response,
                "latency": latency
            }

            results.append(result)
            completed.add(key)

            # Save after every run
            with open(OUTPUT_FILE, "w") as f:
                json.dump(results, f, indent=2)

            current_run += 1
            print(f"Progress: {current_run}/{total_runs}")

    print("\n All runs completed!")


if __name__ == "__main__":
    main()