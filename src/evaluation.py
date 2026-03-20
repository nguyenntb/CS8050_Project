def extract_home_devices(home):

    devices = set()

    for room in home:
        for device in home[room]:
            devices.add(f"{room}.{device}")

    return devices

def extract_plan_devices(action_plan):

    devices = set()

    if action_plan["status"] != "success":
        return devices

    for room in action_plan["devices"]:
        for device in action_plan["devices"][room]:
            devices.add(f"{room}.{device}")

    return devices

def false_positive(plan_devices, home_devices):

    for d in plan_devices:
        if d not in home_devices:
            return 1

    return 0

def false_negative(plan_devices, home_devices):

    for d in home_devices:
        if d not in plan_devices:
            return 1

    return 0    

def success(plan_devices, home_devices):

    if len(plan_devices) == 0:
        return 0

    for d in plan_devices:
        if d not in home_devices:
            return 0

    return 1

def evaluate(commands, home):

    home_devices = extract_home_devices(home)

    FP = 0
    FN = 0
    SR = 0

    for command in commands:

        prompt = build_prompt(command, home, sensors)
        response = run_llm(prompt)

        action_plan = parse_action_plan(response)

        plan_devices = extract_plan_devices(action_plan)

        FP += false_positive(plan_devices, home_devices)
        SR += success(plan_devices, home_devices)

        if action_plan["status"] == "failure":
            FN += 1

    n = len(commands)

    return {
        "FPR": FP / n,
        "FNR": FN / n,
        "SR": SR / n
    }

