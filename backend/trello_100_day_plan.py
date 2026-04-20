#!/usr/bin/env python3
"""
Create a Trello board for a 100-day AI plan.

What it does:
- Creates a new Trello board
- Creates one Trello list per phase
- Creates one card per day
- Adds a checklist to each card

Setup:
1) Create a Trello API key + token
2) Export them:
   export TRELLO_KEY="your_key"
   export TRELLO_TOKEN="your_token"

Run:
   python trello_100_day_plan.py

Optional:
   python trello_100_day_plan.py --board-name "100-Day AI Mastery Plan"
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass
from typing import Any

import requests


BASE_URL = "https://api.trello.com/1"
REQUEST_TIMEOUT = 30


@dataclass
class DayCard:
    title: str
    checklist_name: str
    items: list[str]


@dataclass
class Phase:
    name: str
    cards: list[DayCard]


class TrelloClient:
    def __init__(self, key: str, token: str) -> None:
        self.key = key
        self.token = token
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        merged_params = {"key": self.key, "token": self.token}
        if params:
            merged_params.update(params)

        url = f"{BASE_URL}{path}"
        response = self.session.request(
            method=method,
            url=url,
            params=merged_params,
            json=json,
            timeout=REQUEST_TIMEOUT,
        )

        if not response.ok:
            raise RuntimeError(
                f"Trello API error {response.status_code} for {method} {path}: "
                f"{response.text}"
            )

        return response.json()

    def create_board(self, name: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "/boards",
            params={
                "name": name,
                "defaultLists": "false",
                "prefs_permissionLevel": "private",
            },
        )

    def create_list(self, board_id: str, name: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "/lists",
            params={
                "idBoard": board_id,
                "name": name,
            },
        )

    def create_card(
        self,
        list_id: str,
        name: str,
        desc: str = "",
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            "/cards",
            params={
                "idList": list_id,
                "name": name,
                "desc": desc,
            },
        )

    def create_checklist(self, card_id: str, name: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "/checklists",
            params={
                "idCard": card_id,
                "name": name,
            },
        )

    def add_checkitem(self, checklist_id: str, name: str) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/checklists/{checklist_id}/checkItems",
            params={"name": name},
        )


def make_day(day_num: int, title: str, items: list[str]) -> DayCard:
    return DayCard(
        title=f"Day {day_num} — {title}",
        checklist_name="Checklist",
        items=items,
    )


def build_plan() -> list[Phase]:
    phase_1 = Phase(
        name="Phase 1 — Foundation (Days 1–14)",
        cards=[
            make_day(1, "Repo + Setup", [
                "Create GitHub repo `northstar-rag`",
                "Set up folder structure",
                "Set up Python env in `/backend`",
                "Install pytest",
                "Create `docs/learning-log.md`",
                "Complete AI Fluency intro lesson",
                "Write 5 bullets: capability, limitation, risk, best practice, product implication",
                "Commit and merge first PR",
            ]),
            make_day(2, "First API + CI", [
                "Install FastAPI",
                "Create `/v1/health` endpoint",
                "Run server locally",
                "Add a test for the endpoint",
                "Set up GitHub Actions CI",
                "Merge PR",
            ]),
            make_day(3, "Database Setup", [
                "Set up Docker",
                "Run Postgres locally",
                "Create DB connection file",
                "Create `Document` model",
                "Connect backend to DB",
            ]),
            make_day(4, "File Upload", [
                "Build upload endpoint",
                "Save file locally",
                "Store metadata in DB",
                "Test via Postman or curl",
            ]),
            make_day(5, "Extraction + Chunking", [
                "Extract text from `.txt` files",
                "Build chunking function",
                "Store chunks in DB",
                "Add unit tests",
            ]),
            make_day(6, "UI (Light)", [
                "Create simple UI stub",
                "Upload file via UI",
                "Show preview",
            ]),
            make_day(7, "Documentation", [
                "Write PRD v0.1",
                "Update README",
                "Add architecture doc",
                "Write weekly reflection",
            ]),
            make_day(8, "LLM Basics", [
                "Learn LLM API basics",
                "Make first API call",
            ]),
            make_day(9, "LLM Integration", [
                "Send document text to LLM",
                "Get summary output",
            ]),
            make_day(10, "Structured Output", [
                "Convert output to JSON",
                "Create prompt template",
            ]),
            make_day(11, "Persistence + Logging", [
                "Store LLM outputs",
                "Add logging",
            ]),
            make_day(12, "Improve Ingestion", [
                "Improve chunking",
                "Handle larger files",
            ]),
            make_day(13, "Refactor", [
                "Clean folder structure",
                "Refactor code",
            ]),
            make_day(14, "Demo", [
                "Record 2-minute demo",
                "Push clean repo updates",
            ]),
        ],
    )

    phase_2 = Phase(
        name="Phase 2 — RAG System (Days 15–35)",
        cards=[
            make_day(15, "Embeddings Intro", [
                "Learn embeddings concept",
                "Generate embeddings for sample text",
            ]),
            make_day(16, "Vector DB Setup", [
                "Set up pgvector",
                "Store embeddings",
            ]),
            make_day(17, "Retrieval", [
                "Retrieve similar chunks",
                "Validate retrieval quality manually",
            ]),
            make_day(18, "Query API", [
                "Build query endpoint",
                "Return top retrieved chunks",
            ]),
            make_day(19, "RAG Pipeline", [
                "Combine retrieval and LLM",
                "Return grounded answer",
            ]),
            make_day(20, "Citations", [
                "Add citations to responses",
                "Format sources clearly",
            ]),
            make_day(21, "Improve Retrieval", [
                "Tune similarity search",
                "Test with good and bad queries",
            ]),
            make_day(22, "Metadata Filtering", [
                "Add metadata filters",
                "Test filtered retrieval",
            ]),
            make_day(23, "Prompt Tuning", [
                "Improve system prompt",
                "Reduce irrelevant responses",
            ]),
            make_day(24, "Latency Logging", [
                "Log latency end to end",
                "Capture slow steps",
            ]),
            make_day(25, "Error Handling", [
                "Handle empty query",
                "Handle missing docs",
                "Handle model failures gracefully",
            ]),
            make_day(26, "Q&A UI", [
                "Build basic Q&A UI",
                "Connect it to the backend",
            ]),
            make_day(27, "Multi-Document Support", [
                "Handle multiple documents",
                "Return source-aware answers",
            ]),
            make_day(28, "Pipeline Refactor", [
                "Clean RAG pipeline structure",
                "Separate services cleanly",
            ]),
            make_day(29, "Test Cases", [
                "Add retrieval test cases",
                "Add answer quality spot checks",
            ]),
            make_day(30, "Reduce Hallucinations", [
                "Tighten prompt instructions",
                "Refuse when context is insufficient",
            ]),
            make_day(31, "UX Improvements", [
                "Improve UI flow",
                "Improve empty and loading states",
            ]),
            make_day(32, "Structured Logs", [
                "Add structured logging",
                "Log query, retrieval count, and latency",
            ]),
            make_day(33, "Optimization", [
                "Improve performance",
                "Reduce unnecessary calls",
            ]),
            make_day(34, "Stability", [
                "Fix bugs",
                "Retest ingestion and query flow",
            ]),
            make_day(35, "RAG Demo", [
                "Record demo",
                "Push update to GitHub",
            ]),
        ],
    )

    phase_3 = Phase(
        name="Phase 3 — Real Products (Days 36–60)",
        cards=[
            make_day(36, "Project 1 Start (Recipe AI)", [
                "Set up project structure",
                "Define MVP scope",
            ]),
            make_day(37, "Recipe Parsing", [
                "Parse recipe input",
                "Handle messy input",
            ]),
            make_day(38, "Ingredient Extraction", [
                "Extract ingredients",
                "Normalize units where possible",
            ]),
            make_day(39, "Structured Output", [
                "Convert recipe output to structured format",
                "Validate fields",
            ]),
            make_day(40, "Substitutions", [
                "Suggest ingredient alternatives",
                "Test with common substitutions",
            ]),
            make_day(41, "Pricing Logic", [
                "Add mock pricing logic",
                "Return estimated basket",
            ]),
            make_day(42, "Recipe UI Setup", [
                "Build basic UI",
                "Connect user input to backend",
            ]),
            make_day(43, "Recipe Integration", [
                "Connect backend and UI fully",
                "Test full flow",
            ]),
            make_day(44, "Recipe UX Improve", [
                "Clean the user flow",
                "Improve outputs and labels",
            ]),
            make_day(45, "Recipe AI Demo", [
                "Record demo",
                "Write short project summary",
            ]),
            make_day(46, "Project 2 Start (Research AI)", [
                "Set up project structure",
                "Define user flow",
            ]),
            make_day(47, "Multi-Doc Upload", [
                "Handle multiple document uploads",
                "Store them cleanly",
            ]),
            make_day(48, "Search System", [
                "Build search across uploaded docs",
                "Return ranked results",
            ]),
            make_day(49, "Summarization", [
                "Add summarization",
                "Support summary by doc and cross-doc",
            ]),
            make_day(50, "Session Memory", [
                "Save sessions",
                "Restore previous context",
            ]),
            make_day(51, "Research UI", [
                "Build UI",
                "Connect search and answer views",
            ]),
            make_day(52, "Research UX Improve", [
                "Clean UI flow",
                "Improve source visibility",
            ]),
            make_day(53, "Research Testing", [
                "Add tests",
                "Run realistic usage checks",
            ]),
            make_day(54, "Research Optimization", [
                "Improve performance",
                "Reduce duplicate retrieval",
            ]),
            make_day(55, "Research AI Demo", [
                "Record demo",
                "Write project notes",
            ]),
            make_day(56, "Project 3 Start", [
                "Choose domain",
                "Define MVP",
            ]),
            make_day(57, "Core Feature", [
                "Implement core feature",
                "Test base use case",
            ]),
            make_day(58, "UI", [
                "Build basic UI",
                "Connect to backend",
            ]),
            make_day(59, "Output Quality", [
                "Refine outputs",
                "Improve prompt quality",
            ]),
            make_day(60, "Project 3 Demo", [
                "Record demo",
                "Publish progress update",
            ]),
        ],
    )

    phase_4 = Phase(
        name="Phase 4 — Advanced (Days 61–80)",
        cards=[
            make_day(61, "Agents Intro", [
                "Learn agent basics",
                "Write notes on when agents are useful",
            ]),
            make_day(62, "Tool Calling", [
                "Implement tool use",
                "Test one tool successfully",
            ]),
            make_day(63, "Multi-Step Reasoning", [
                "Add multi-step flow",
                "Log each step",
            ]),
            make_day(64, "Agent Memory", [
                "Add memory",
                "Test follow-up behavior",
            ]),
            make_day(65, "Agent Refinement", [
                "Improve flow",
                "Handle obvious failure cases",
            ]),
            make_day(66, "Eval System Intro", [
                "Learn evaluation basics",
                "Define what good output means",
            ]),
            make_day(67, "Output Comparison", [
                "Compare outputs across prompts",
                "Store examples",
            ]),
            make_day(68, "Scoring System", [
                "Build scoring rubric",
                "Score sample outputs",
            ]),
            make_day(69, "Eval Pipeline", [
                "Automate evaluation pipeline",
                "Run on sample set",
            ]),
            make_day(70, "Quality Improvement", [
                "Refine outputs based on evals",
                "Document changes",
            ]),
            make_day(71, "Cost Tracking", [
                "Track usage",
                "Estimate per-request cost",
            ]),
            make_day(72, "Latency Tracking", [
                "Track latency",
                "Find slowest step",
            ]),
            make_day(73, "Prompt Versioning", [
                "Version prompts",
                "Track prompt changes",
            ]),
            make_day(74, "System Design Notes", [
                "Document architecture",
                "Capture tradeoffs",
            ]),
            make_day(75, "Advanced Refactor", [
                "Clean architecture",
                "Improve modularity",
            ]),
            make_day(76, "Bug Fixing", [
                "Fix bugs",
                "Retest critical flows",
            ]),
            make_day(77, "UX Polish", [
                "Improve UX",
                "Tighten wording and states",
            ]),
            make_day(78, "System Optimization", [
                "Optimize system",
                "Reduce wasteful work",
            ]),
            make_day(79, "Repo Cleanup", [
                "Clean repositories",
                "Remove dead code",
            ]),
            make_day(80, "Advanced Demo", [
                "Record demos",
                "Summarize learnings",
            ]),
        ],
    )

    phase_5 = Phase(
        name="Phase 5 — Job Execution (Days 81–100)",
        cards=[
            make_day(81, "Portfolio Setup", [
                "Clean GitHub repos",
                "Pin best projects",
            ]),
            make_day(82, "README Upgrade", [
                "Improve docs",
                "Sharpen project positioning",
            ]),
            make_day(83, "Screenshots", [
                "Add screenshots",
                "Add visuals to READMEs",
            ]),
            make_day(84, "Demo Videos", [
                "Record videos",
                "Link demos in repos",
            ]),
            make_day(85, "Final Portfolio Polish", [
                "Clean everything",
                "Check portfolio from recruiter perspective",
            ]),
            make_day(86, "Resume Draft", [
                "Write AI-focused resume",
                "Lead with product plus technical credibility",
            ]),
            make_day(87, "Resume Improve", [
                "Add metrics",
                "Tighten wording",
            ]),
            make_day(88, "LinkedIn Update", [
                "Update profile headline",
                "Add project highlights",
            ]),
            make_day(89, "Applications Day 1", [
                "Apply to 5 roles",
                "Track applications",
                "Reach out to 2 hiring managers",
            ]),
            make_day(90, "Applications Day 2", [
                "Apply to 5 roles",
                "Track applications",
                "Reach out to 2 hiring managers",
            ]),
            make_day(91, "Applications Day 3", [
                "Apply to 5 roles",
                "Track applications",
                "Reach out to 2 hiring managers",
            ]),
            make_day(92, "Applications Day 4", [
                "Apply to 5 roles",
                "Track applications",
                "Reach out to 2 hiring managers",
            ]),
            make_day(93, "Applications Day 5", [
                "Apply to 5 roles",
                "Track applications",
                "Reach out to 2 hiring managers",
            ]),
            make_day(94, "Applications Day 6", [
                "Apply to 5 roles",
                "Track applications",
                "Reach out to 2 hiring managers",
            ]),
            make_day(95, "Applications Day 7", [
                "Apply to 5 roles",
                "Track applications",
                "Reach out to 2 hiring managers",
            ]),
            make_day(96, "Interview Prep: System Design", [
                "Practice system design",
                "Prepare one strong architecture story",
            ]),
            make_day(97, "Interview Prep: AI Questions", [
                "Practice AI product questions",
                "Prepare 10 strong answers",
            ]),
            make_day(98, "Project Walkthroughs", [
                "Practice demos",
                "Prepare concise project walkthroughs",
            ]),
            make_day(99, "Mock Interviews", [
                "Do mock interviews",
                "Note weak spots",
            ]),
            make_day(100, "Final Push", [
                "Apply broadly",
                "Follow up on prior applications",
                "Write reflection and next 30-day plan",
            ]),
        ],
    )

    return [phase_1, phase_2, phase_3, phase_4, phase_5]


def create_board_from_plan(client: TrelloClient, board_name: str, phases: list[Phase]) -> str:
    board = client.create_board(board_name)
    board_id = board["id"]
    print(f"Created board: {board['name']} ({board_id})")

    for phase in phases:
        trello_list = client.create_list(board_id, phase.name)
        list_id = trello_list["id"]
        print(f"  Created list: {phase.name}")

        for card in phase.cards:
            desc = (
                f"{card.title}\n\n"
                f"Auto-created by script.\n"
                f"Phase: {phase.name}"
            )
            trello_card = client.create_card(list_id, card.title, desc=desc)
            card_id = trello_card["id"]
            print(f"    Created card: {card.title}")

            checklist = client.create_checklist(card_id, card.checklist_name)
            checklist_id = checklist["id"]

            for item in card.items:
                client.add_checkitem(checklist_id, item)

            # Small pause to be gentle with the API.
            time.sleep(0.05)

    return board.get("url", "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a 100-day AI plan board in Trello.")
    parser.add_argument(
        "--board-name",
        default="100-Day AI Mastery Plan",
        help="Name of the Trello board to create.",
    )
    args = parser.parse_args()

    key = os.getenv("TRELLO_KEY")
    token = os.getenv("TRELLO_TOKEN")

    if not key or not token:
        print("Missing TRELLO_KEY or TRELLO_TOKEN environment variables.", file=sys.stderr)
        print('Example:', file=sys.stderr)
        print('  export TRELLO_KEY="your_key"', file=sys.stderr)
        print('  export TRELLO_TOKEN="your_token"', file=sys.stderr)
        return 1

    phases = build_plan()
    total_cards = sum(len(phase.cards) for phase in phases)
    if total_cards != 100:
        print(f"Plan sanity check failed: expected 100 cards, got {total_cards}.", file=sys.stderr)
        return 1

    client = TrelloClient(key, token)
    try:
        board_url = create_board_from_plan(client, args.board_name, phases)
    except Exception as exc:
        print(f"Failed: {exc}", file=sys.stderr)
        return 1

    print("\nDone.")
    if board_url:
        print(f"Board URL: {board_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
