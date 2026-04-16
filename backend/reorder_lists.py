import requests
import re
import os

# 🔐 Set your credentials
API_KEY = os.getenv("TRELLO_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")

BOARD_ID = "YyxjjVi5"  # replace this

BASE_URL = "https://api.trello.com/1"


def get_lists(board_id):
    url = f"{BASE_URL}/boards/{board_id}/lists"
    params = {
        "key": API_KEY,
        "token": TOKEN
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_week_number(name):
    match = re.search(r"Week\s*(\d+)", name, re.IGNORECASE)
    return int(match.group(1)) if match else float("inf")


def reorder_lists(lists):
    # Sort by week number
    sorted_lists = sorted(lists, key=lambda x: extract_week_number(x["name"]))

    for index, lst in enumerate(sorted_lists):
        new_pos = (index + 1) * 1000  # spacing helps avoid conflicts

        url = f"{BASE_URL}/lists/{lst['id']}"
        params = {
            "key": API_KEY,
            "token": TOKEN,
            "pos": new_pos
        }

        res = requests.put(url, params=params)
        res.raise_for_status()

        print(f"Moved {lst['name']} → position {new_pos}")


if __name__ == "__main__":
    lists = get_lists(BOARD_ID)
    reorder_lists(lists)
