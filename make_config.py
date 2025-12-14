import os
import json

def get_base_path():
    # Folder where this script is located
    return os.path.dirname(os.path.abspath(__file__))

def create_config():
    base_path = get_base_path()
    config_path = os.path.join(base_path, "config.json")

    if os.path.exists(config_path):
        print("config.json already exists.")
        return

    config_data = {
        "username": "",
        "password": "",
        "pin": "",
        "created_at": None
    }

    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=4)

    print(f"config.json created at: {config_path}")

if __name__ == "__main__":
    create_config()