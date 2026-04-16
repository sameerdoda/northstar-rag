# Trello phase reset script

This script resets a Trello board from any existing structure to a new phase-based 100-day plan.

## What it does
- deletes all cards from the selected board
- archives all existing lists
- creates 5 new phase lists
- creates Day 1 to Day 100 cards
- adds a `Daily Tasks` checklist to each card

## Setup
```bash
pip install requests
export TRELLO_KEY="your_key"
export TRELLO_TOKEN="your_token"
```

## Dry run
```bash
python reset_trello_to_phases.py --board-name "100 Day PM AI Plan" --dry-run
```

## Real run
```bash
python reset_trello_to_phases.py --board-name "100 Day PM AI Plan"
```

or

```bash
python reset_trello_to_phases.py --board-id "your_board_id"
```

The script will ask you to type `RESET` before it makes changes.
