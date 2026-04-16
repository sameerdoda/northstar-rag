#!/usr/bin/env python3
"""
Upload a 100-day checklist into Trello as:
- 1 board
- 15 lists (Week 1 ... Week 15)
- 100 cards (Day 1 ... Day 100)
- 1 checklist per card
- 5 checklist items per card

Official Trello REST API docs used:
- API intro / auth
- Boards
- Lists
- Cards
- Checklists

Required environment variables:
  TRELLO_KEY=your_api_key
  TRELLO_TOKEN=your_api_token

Examples:
  python upload_to_trello.py --board-name "100 Day PM AI Plan"
  python upload_to_trello.py --board-id <existing_board_id>
  python upload_to_trello.py --board-name "100 Day PM AI Plan" --dry-run

Optional:
  --workspace-id <idOrganization>   Create the board inside a Trello workspace
  --json-file trello_100_day_pm_ai_plan.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import requests

BASE_URL = "https://api.trello.com/1"


def env_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def trello_request(
    method: str,
    path: str,
    key: str,
    token: str,
    *,
    params: Dict[str, Any] | None = None,
    timeout: int = 30,
    dry_run: bool = False,
) -> Dict[str, Any]:
    params = dict(params or {})
    params["key"] = key
    params["token"] = token
    url = f"{BASE_URL}{path}"

    if dry_run:
        print(f"[dry-run] {method} {url} params={params}")
        return {}

    response = requests.request(method, url, params=params, timeout=timeout)
    if response.status_code >= 400:
        raise RuntimeError(
            f"Trello API error {response.status_code} for {method} {path}\n"
            f"Response: {response.text}"
        )

    if response.text.strip():
        return response.json()
    return {}


def load_plan(json_file: Path) -> List[Dict[str, Any]]:
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not data:
        raise ValueError("JSON plan file must contain a non-empty list")
    return data


def create_board(key: str, token: str, board_name: str, workspace_id: str | None, dry_run: bool) -> str:
    params: Dict[str, Any] = {"name": board_name, "defaultLists": "false"}
    if workspace_id:
        params["idOrganization"] = workspace_id
    data = trello_request("POST", "/boards", key, token, params=params, dry_run=dry_run)
    return data.get("id", "dry-run-board-id")


def create_list(key: str, token: str, board_id: str, name: str, dry_run: bool) -> str:
    data = trello_request("POST", f"/boards/{board_id}/lists", key, token, params={"name": name}, dry_run=dry_run)
    return data.get("id", f"dry-run-list-{name}")


def create_card(key: str, token: str, list_id: str, name: str, desc: str, dry_run: bool) -> str:
    data = trello_request(
        "POST",
        "/cards",
        key,
        token,
        params={"idList": list_id, "name": name, "desc": desc},
        dry_run=dry_run,
    )
    return data.get("id", f"dry-run-card-{name}")


def create_checklist(key: str, token: str, card_id: str, name: str, dry_run: bool) -> str:
    data = trello_request(
        "POST",
        "/checklists",
        key,
        token,
        params={"idCard": card_id, "name": name},
        dry_run=dry_run,
    )
    return data.get("id", f"dry-run-checklist-{name}")


def create_checkitem(key: str, token: str, checklist_id: str, name: str, dry_run: bool) -> None:
    trello_request(
        "POST",
        f"/checklists/{checklist_id}/checkItems",
        key,
        token,
        params={"name": name},
        dry_run=dry_run,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-file", default="trello_100_day_pm_ai_plan.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--board-name")
    group.add_argument("--board-id")
    parser.add_argument("--workspace-id")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--sleep-seconds", type=float, default=0.08)
    args = parser.parse_args()

    key = env_required("TRELLO_KEY")
    token = env_required("TRELLO_TOKEN")
    plan = load_plan(Path(args.json_file))

    board_id = args.board_id
    if not board_id:
        board_id = create_board(key, token, args.board_name, args.workspace_id, args.dry_run)
        print(f"Created board: {board_id}")
    else:
        print(f"Using existing board: {board_id}")

    week_to_list_id: Dict[int, str] = {}

    # Create lists first
    weeks = sorted({int(item["week"]) for item in plan})
    for week in weeks:
        list_id = create_list(key, token, board_id, f"Week {week}", args.dry_run)
        week_to_list_id[week] = list_id
        print(f"Created list Week {week}: {list_id}")
        time.sleep(args.sleep_seconds)

    # Create cards + checklists
    for item in plan:
        list_id = week_to_list_id[int(item["week"])]
        tasks = item["tasks"]
        if not isinstance(tasks, list) or not tasks:
            raise ValueError(f"Day {item.get('day')} has no tasks")

        desc = (
            f"Phase: {item['phase']}\n"
            f"Week: {item['week']}\n"
            f"Day: {item['day']}\n\n"
            f"Created by upload_to_trello.py"
        )
        card_id = create_card(key, token, list_id, item["card_title"], desc, args.dry_run)
        checklist_id = create_checklist(key, token, card_id, item.get("checklist_name", "Daily Tasks"), args.dry_run)

        for task in tasks:
            create_checkitem(key, token, checklist_id, task, args.dry_run)
            time.sleep(args.sleep_seconds)

        print(f"Created card {item['day']}: {item['card_title']}")
        time.sleep(args.sleep_seconds)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
