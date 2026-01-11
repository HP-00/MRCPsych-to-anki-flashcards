# Quick Start Guide

Get up and running in 5 minutes.

## Prerequisites

- **Python 3.8+** - Check: `python3 --version`
- **Anki Desktop** - Download: https://apps.ankiweb.net/
- **Claude Code** - Install: `npm install -g @anthropic-ai/claude-code`

## Step 1: Install AnkiConnect (2 minutes)

1. Open Anki
2. Go to **Tools** → **Add-ons** → **Get Add-ons...**
3. Enter code: `2055492159`
4. Click OK, then **restart Anki**

**Verify it works:**
```bash
curl -s localhost:8765 -X POST -d '{"action": "version", "version": 6}'
# Should return: {"result": 6, "error": null}
```

## Step 2: Clone & Setup (1 minute)

```bash
# Clone the repo
git clone https://github.com/HP-00/MRCPsych-to-anki-flashcards.git
cd MRCPsych-to-anki-flashcards

# Create deck structure in Anki (Anki must be running)
python3 scripts/setup_anki_decks.py
```

## Step 3: Start Creating Flashcards (1 minute)

```bash
# Start Claude Code in the project directory
claude
```

Now you can:
1. **Paste an image** - screenshot of any MRCPsych question
2. **Paste text** - copy/paste question text directly
3. **Use `/flashcard`** - command with image or text
4. **Add a prompt** - paste content with "create flashcards from this"

All methods produce the same high-quality flashcards. Claude will:
- Analyze the question
- Create optimized flashcards (following spaced repetition best practices)
- Sync them directly to your Anki

## Example Usage

```
You: [paste screenshot of SPMM question about lithium]

Claude: I've analyzed this Paper A Pharmacology question about lithium monitoring.

Creating flashcards:

1. [Paper A - Pharmacology] What is the therapeutic range for serum lithium?
   → 0.6-1.0 mmol/L

2. [Paper A - Pharmacology] At what level does lithium toxicity occur?
   → >1.5 mmol/L

3. Cloze: Lithium levels should be checked {{c1::12 hours}} post-dose

**3 cards synced to MRCPsych::Paper A::Pharmacology**
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to Anki" | Make sure Anki is running |
| "AnkiConnect not found" | Restart Anki after installing the add-on |
| Cards not appearing | Check the MRCPsych deck in Anki's browser |

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [.claude/rules/flashcard-quality.md](.claude/rules/flashcard-quality.md) for card quality standards
- See [.claude/rules/mrcpsych-topics.md](.claude/rules/mrcpsych-topics.md) for topic classification
