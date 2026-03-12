import json
import os

def load_all_data():

    homes = {
        "home1": json.load("data/home1.json"),
        "home2": json.load("data/home2.json"),
        "home3": json.load("data/home3.json")
    }

    sensors = json.load("data/sensors.json")
    commands = json.load("data/commands.json")

    return homes, sensors, commands