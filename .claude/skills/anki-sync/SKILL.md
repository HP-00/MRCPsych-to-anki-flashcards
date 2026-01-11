---
name: anki-sync
description: Syncs flashcards to local Anki installation via AnkiConnect API. Use when adding cards to Anki, checking Anki connection, or managing Anki decks.
allowed-tools: Bash, Read
---

# Anki Sync Skill

This skill handles all interactions with the local Anki installation via the AnkiConnect API.

## Prerequisites

1. **Anki must be running** on the local machine
2. **AnkiConnect add-on installed**: Tools → Add-ons → Get Add-ons → Code: `2055492159`
3. AnkiConnect listening on `localhost:8765`

## Verifying Connection

```bash
curl -s localhost:8765 -X POST -d '{"action": "version", "version": 6}'
```

Expected response: `{"result": 6, "error": null}`

## Using the Python Wrapper

```python
from scripts.anki_connect import AnkiConnect

anki = AnkiConnect()

# Check connection
if anki.is_connected():
    print("Connected to Anki")
else:
    print("ERROR: Anki not running")
```

## Common Operations

### List All Decks
```python
decks = anki.get_decks()
print(decks)
# ['Default', 'MRCPsych::Paper A::Neuroscience', ...]
```

### Create a Deck
```python
anki.create_deck("MRCPsych::Paper A::Pharmacology")
# Creates nested deck structure automatically
```

### Add a Basic Card
```python
note_id = anki.add_note(
    deck_name="MRCPsych::Paper A::Pharmacology",
    front="[Paper A] What is the half-life of lithium?",
    back="12-27 hours (longer in elderly)\n• Steady state reached in 5-7 days",
    tags=["mrcpsych", "paper-a", "pharmacology", "lithium"]
)
print(f"Created note: {note_id}")
```

### Add a Cloze Card
```python
note_id = anki.add_cloze_note(
    deck_name="MRCPsych::Paper A::Pharmacology",
    text="Lithium has a narrow therapeutic index: {{c1::0.6-1.0}} mmol/L",
    extra="Check levels 12 hours post-dose. Toxicity >1.5 mmol/L",
    tags=["mrcpsych", "paper-a", "pharmacology", "lithium"]
)
```

### Add Multiple Cards
```python
cards = [
    {
        "deck_name": "MRCPsych::Paper A::Pharmacology",
        "front": "Question 1",
        "back": "Answer 1",
        "tags": ["tag1"]
    },
    {
        "deck_name": "MRCPsych::Paper A::Pharmacology",
        "front": "Question 2",
        "back": "Answer 2",
        "tags": ["tag2"]
    }
]
note_ids = anki.add_notes(cards)
print(f"Created {len([n for n in note_ids if n])} notes")
```

### Add Card with Image
```python
note_id = anki.add_note_with_image(
    deck_name="MRCPsych::Paper A::Neuroscience",
    front="[Paper A] Label this brain structure:",
    back="Hippocampus - key role in memory consolidation",
    image_path="/path/to/brain_diagram.png",
    tags=["mrcpsych", "paper-a", "neuroscience", "neuroanatomy"]
)
```

## Deck Naming Convention

Use nested decks with `::` separator:
```
MRCPsych::Paper A::Neuroscience
MRCPsych::Paper A::Psychology
MRCPsych::Paper A::Pharmacology
MRCPsych::Paper A::Genetics
MRCPsych::Paper B::General Adult
MRCPsych::Paper B::Old Age
MRCPsych::Paper B::Child & Adolescent
MRCPsych::Paper B::Psychotherapy
MRCPsych::Paper B::Critical Review
MRCPsych::Paper B::Service Organization
```

## Error Handling

```python
from scripts.anki_connect import AnkiConnect, AnkiConnectError

try:
    anki = AnkiConnect()
    note_id = anki.add_note(...)
except AnkiConnectError as e:
    print(f"Anki error: {e}")
    # Common errors:
    # - "cannot create note because it is a duplicate"
    # - "model was not found"
    # - Connection refused (Anki not running)
```

## Troubleshooting

### "Connection refused"
- Ensure Anki is running
- Check AnkiConnect is installed and enabled
- Restart Anki after installing AnkiConnect

### "Model was not found"
- Use built-in note types: "Basic", "Cloze", "Basic (and reversed card)"
- Or create custom note type in Anki first

### Duplicate detection
```python
# Allow duplicates if needed
anki.add_note(..., allow_duplicate=True)

# Check if note can be added
can_add = anki._invoke("canAddNotes", notes=[note_data])
```

## Direct API Calls

For advanced operations, use the raw API:

```python
# Find notes by query
note_ids = anki.find_notes("deck:MRCPsych tag:high-yield")

# Get deck statistics
stats = anki.get_deck_stats("MRCPsych::Paper A")

# Trigger sync
anki.sync()
```
