import json

from prompt_builder import build_prompt
from llm_runner import run_llm


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def main():

    homes = [
        load_json("../data/home1.json"),
        load_json("../data/home2.json"),
        load_json("../data/home3.json")
    ]

    sensors = load_json("../data/sensors.json")
    commands = load_json("../data/commands.json")

    results = []

    for i, home in enumerate(homes):

        for command in commands:

            prompt = build_prompt(command, home, sensors)

            response = run_llm(prompt)

            results.append({
                "home": i + 1,
                "command": command["command"],
                "type": command["type"],
                "response": response
            })

    # save results
    with open("../results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()