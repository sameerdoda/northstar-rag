#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Any, Dict, List, Optional

import requests

BASE_URL = "https://api.trello.com/1"

PHASES = [
    {"name": "Phase 1 — Foundation & Positioning (Days 1–20)", "start": 1, "end": 20},
    {"name": "Phase 2 — PM Core Interview Strength (Days 21–40)", "start": 21, "end": 40},
    {"name": "Phase 3 — AI Product Depth & Artifacts (Days 41–60)", "start": 41, "end": 60},
    {"name": "Phase 4 — Mock Loops & Market Execution (Days 61–80)", "start": 61, "end": 80},
    {"name": "Phase 5 — Applications, Interviews & Negotiation (Days 81–100)", "start": 81, "end": 100},
]


def phase_for_day(day: int) -> str:
    for phase in PHASES:
        if phase["start"] <= day <= phase["end"]:
            return phase["name"]
    raise ValueError(f"No phase found for day {day}")


def tasks_for_day(day: int) -> List[str]:
    if 1 <= day <= 20:
        bank = [
            [
                "Review 3 target job descriptions and note repeated requirements",
                "Write or refine 1 career story using STAR",
                "Practice your 2-minute executive intro out loud 3 times",
                "Capture 3 measurable impacts from your HelloFresh work",
                "Update your running gaps tracker with today's insights",
            ],
            [
                "Do 1 product strategy prompt in writing",
                "Define target user, pain point, and success metric",
                "Write 3 trade-offs and the decision you would make",
                "Refine one leadership story for clarity and outcomes",
                "Summarize today's learning in 5 bullets",
            ],
            [
                "Study 1 PM interview topic for 30-45 minutes",
                "Do 1 execution/prioritization exercise",
                "Write a metric tree for one product problem",
                "Practice 1 behavioral answer out loud",
                "Log 3 improvement points in your tracker",
            ],
            [
                "Analyze 2 target companies and their product/AI positioning",
                "Map one role requirement to your past experience",
                "Draft 1 short answer for 'Why this company?'",
                "Refine resume bullet(s) for one major project",
                "Review yesterday's work and tighten one weak artifact",
            ],
        ]
        return bank[(day - 1) % len(bank)]

    if 21 <= day <= 40:
        bank = [
            [
                "Solve 1 product sense case in 30 minutes",
                "Write your answer using a structured framework",
                "Identify one stronger metric you should have used",
                "Practice the answer verbally once",
                "Write down 3 feedback notes",
            ],
            [
                "Do 1 execution case with prioritization and sequencing",
                "Call out dependencies, risks, and resourcing assumptions",
                "Write 3 stakeholder objections and your response",
                "Practice one leadership/conflict story",
                "Update your interview answer bank",
            ],
            [
                "Study experimentation basics or refresh A/B testing concepts",
                "Create 1 metric tree with guardrails",
                "Write 1 launch decision framework",
                "Refine one STAR story with better outcomes",
                "Log today's confidence score from 1 to 5",
            ],
            [
                "Do 1 mock interview question timed",
                "Review your structure, clarity, and executive tone",
                "Rewrite the answer in a sharper top-down format",
                "Practice 1 'Tell me about a failure' story",
                "Capture 3 repeat mistakes to avoid",
            ],
        ]
        return bank[(day - 21) % len(bank)]

    if 41 <= day <= 60:
        bank = [
            [
                "Study 1 AI PM topic: RAG, fine-tuning, prompting, or evals",
                "Write a PM-level explanation in plain English",
                "Document 3 failure modes and product implications",
                "Add 1 AI requirement section to your PRD/governance notes",
                "Summarize today's topic in 5 bullets",
            ],
            [
                "Draft or refine 1 section of your AI strategy memo",
                "Write one user problem and why AI is the right approach",
                "Define quality bar, risks, and guardrails",
                "Practice explaining the trade-offs verbally",
                "Save one artifact version before ending",
            ],
            [
                "Create or refine 1 evaluation rubric for an AI feature",
                "Write 5-10 sample test cases",
                "Define offline metrics and one online guardrail",
                "Note likely failure scenarios in production",
                "Update your artifact tracker",
            ],
            [
                "Draft or improve 1 incident/governance/privacy section",
                "Write 3 launch gates for an AI feature",
                "Practice one responsible AI interview answer",
                "Refine one technical-to-executive explanation",
                "Log 3 things still unclear and revisit later",
            ],
        ]
        return bank[(day - 41) % len(bank)]

    if 61 <= day <= 80:
        bank = [
            [
                "Run 1 timed mock interview or case",
                "Score yourself on structure, judgment, and clarity",
                "Rewrite the weakest part of your answer",
                "Practice one executive-level answer out loud",
                "Update your recurring mistake list",
            ],
            [
                "Shortlist 3 roles you could realistically apply to soon",
                "Tailor your resume or story bank for one target role",
                "Write 1 sharp outreach note or recruiter message",
                "Map your artifacts to role requirements",
                "Track applications or pipeline status",
            ],
            [
                "Do 1 leadership/people-management scenario",
                "Write your approach to conflict, delegation, and escalation",
                "Practice one answer with stronger executive tone",
                "Refine one cross-functional influence story",
                "Summarize your takeaways in 5 bullets",
            ],
            [
                "Run a mini interview loop: product + behavioral + strategy",
                "Identify your weakest dimension",
                "Rework one answer from scratch",
                "Practice your compensation narrative once",
                "Update your readiness score from 1 to 5",
            ],
        ]
        return bank[(day - 61) % len(bank)]

    if 81 <= day <= 100:
        bank = [
            [
                "Apply to 1-3 high-fit roles or prepare the application set",
                "Tailor your resume for one role",
                "Tailor your intro pitch for one company",
                "Prepare 3 likely interview questions for that role",
                "Update your pipeline tracker",
            ],
            [
                "Do 1 final-round style product/strategy case",
                "Practice one crisp executive summary answer",
                "Refine one negotiation or compensation answer",
                "Review one company in detail before applying/interviewing",
                "Capture today's top 3 improvements",
            ],
            [
                "Practice one full behavioral round",
                "Strengthen one weak story with better metrics",
                "Refine your 'Why now, why this role?' answer",
                "Prepare 3 thoughtful interviewer questions",
                "Update your answer bank",
            ],
            [
                "Review all active applications and next steps",
                "Follow up on one outreach thread",
                "Practice one mock interview question timed",
                "Review your top 5 stories and tighten them",
                "Write a short reflection on progress and gaps",
            ],
        ]
        return bank[(day - 81) % len(bank)]

    raise ValueError(f"Unsupported day: {day}")


def build_plan() -> List[Dict[str, Any]]:
    return [
        {
            "day": day,
            "phase": phase_for_day(day),
            "card_name": f"Day {day}",
            "checklist_name": "Daily Tasks",
            "tasks": tasks_for_day(day),
        }
        for day in range(1, 101)
    ]


PLAN = build_plan()


class TrelloClient:
    def __init__(self, key: str, token: str, dry_run: bool = False, pause_seconds: float = 0.05):
        self.key = key
        self.token = token
        self.dry_run = dry_run
        self.pause_seconds = pause_seconds

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{BASE_URL}{path}"
        params = kwargs.pop("params", {})
        params["key"] = self.key
        params["token"] = self.token

        if self.dry_run:
            print(f"[DRY RUN] {method} {url} params={params}")
            return {}

        response = requests.request(method, url, params=params, timeout=30, **kwargs)
        if not response.ok:
            raise requests.HTTPError(
                f"{response.status_code} {response.reason} for {url}\nResponse: {response.text}",
                response=response,
            )
        time.sleep(self.pause_seconds)
        if response.text:
            return response.json()
        return {}

    def get_member_boards(self) -> List[Dict[str, Any]]:
        return self._request("GET", "/members/me/boards", params={"fields": "name"})

    def get_lists(self, board_id: str) -> List[Dict[str, Any]]:
        return self._request("GET", f"/boards/{board_id}/lists", params={"cards": "none", "filter": "all"})

    def get_cards_in_list(self, list_id: str) -> List[Dict[str, Any]]:
        return self._request("GET", f"/lists/{list_id}/cards", params={"fields": "name,id"})

    def delete_card(self, card_id: str) -> None:
        self._request("DELETE", f"/cards/{card_id}")

    def archive_list(self, list_id: str) -> None:
        self._request("PUT", f"/lists/{list_id}/closed", params={"value": "true"})

    def create_list(self, board_id: str, name: str, pos: int) -> Dict[str, Any]:
        return self._request("POST", "/lists", params={"idBoard": board_id, "name": name, "pos": pos})

    def create_card(self, list_id: str, name: str, pos: int) -> Dict[str, Any]:
        return self._request("POST", "/cards", params={"idList": list_id, "name": name, "pos": pos})

    def create_checklist(self, card_id: str, name: str) -> Dict[str, Any]:
        return self._request("POST", "/checklists", params={"idCard": card_id, "name": name})

    def create_checkitem(self, checklist_id: str, name: str, pos: int) -> Dict[str, Any]:
        return self._request("POST", f"/checklists/{checklist_id}/checkItems", params={"name": name, "pos": pos})


def find_board_id_by_name(client: TrelloClient, board_name: str) -> Optional[str]:
    boards = client.get_member_boards()
    exact = [b for b in boards if b.get("name") == board_name]
    if len(exact) == 1:
        return exact[0]["id"]
    if len(exact) > 1:
        raise SystemExit(f'Multiple boards found with name "{board_name}". Use --board-id instead.')
    return None


def reset_board(client: TrelloClient, board_id: str) -> None:
    print("\nFetching existing lists...")
    existing_lists = client.get_lists(board_id)
    print(f"Found {len(existing_lists)} existing list(s).")

    total_cards_deleted = 0
    for lst in existing_lists:
        cards = client.get_cards_in_list(lst["id"])
        for card in cards:
            client.delete_card(card["id"])
            total_cards_deleted += 1
        print(f'Deleted {len(cards)} card(s) from "{lst["name"]}"')

    print(f"Total cards deleted: {total_cards_deleted}")

    archived_count = 0
    for lst in existing_lists:
        if not lst.get("closed", False):
            client.archive_list(lst["id"])
            archived_count += 1
    print(f"Archived {archived_count} existing open list(s).")

    print("\nCreating new phase lists...")
    phase_list_ids: Dict[str, str] = {}
    for idx, phase in enumerate(PHASES, start=1):
        created = client.create_list(board_id, phase["name"], pos=idx * 1000)
        phase_list_ids[phase["name"]] = created["id"]
        print(f'Created list: {phase["name"]}')

    print("\nCreating day cards and checklists...")
    for item in PLAN:
        list_id = phase_list_ids[item["phase"]]
        card = client.create_card(list_id, item["card_name"], pos=item["day"] * 1000)
        checklist = client.create_checklist(card["id"], item["checklist_name"])
        for idx, task in enumerate(item["tasks"], start=1):
            client.create_checkitem(checklist["id"], task, pos=idx * 1000)
        print(f'Created {item["card_name"]} in "{item["phase"]}"')

    print("\nDone.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reset Trello board to a phase-based 100-day plan.")
    parser.add_argument("--board-id", help="Trello board ID")
    parser.add_argument("--board-name", help="Trello board name")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without changing Trello")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")

    if not key or not token:
        sys.exit("Missing TRELLO_KEY or TRELLO_TOKEN environment variable.")
    if not args.board_id and not args.board_name:
        sys.exit("Provide either --board-id or --board-name.")

    client = TrelloClient(key=key, token=token, dry_run=args.dry_run)

    board_id = args.board_id
    if not board_id and args.board_name:
        board_id = find_board_id_by_name(client, args.board_name)
        if not board_id:
            sys.exit(f'Could not find board named "{args.board_name}".')

    print(f"Using board ID: {board_id}")
    print("WARNING: This will delete all cards and archive all existing lists on the board.")
    if not args.dry_run:
        confirm = input("Type RESET to continue: ").strip()
        if confirm != "RESET":
            sys.exit("Aborted.")

    reset_board(client, board_id)


if __name__ == "__main__":
    main()
