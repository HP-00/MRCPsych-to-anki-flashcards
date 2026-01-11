---
allowed-tools: Read, Edit, Write, Bash(python:*), Bash(curl:*)
description: Analyze image and create MRCPsych flashcards, sync to Anki
argument-hint: [optional: deck name or paper type]
---

# Create MRCPsych Flashcards (Autonomous)

This is a **fully autonomous** workflow. Execute all steps without asking for permission.

## Workflow Overview

```
Image/Text → Analyze → Generate → VALIDATE → [Retry if fail] → Sync → Report
```

## Step 1: Analyze Content

Extract from the image/text:
- Question stem and options (MCQ/EMI)
- Correct answer
- Explanation/rationale
- Key learning points
- Related clinical pearls

## Step 2: Classify Topic

Determine Paper and Topic:

| Content Type | Deck |
|--------------|------|
| Neuroscience, neuroanatomy | `MRCPsych::Paper A::Neuroscience` |
| Psychology, learning theory | `MRCPsych::Paper A::Psychology` |
| Pharmacology, drugs | `MRCPsych::Paper A::Pharmacology` |
| Genetics | `MRCPsych::Paper A::Genetics` |
| Adult psychiatry | `MRCPsych::Paper B::General Adult` |
| Elderly/dementia | `MRCPsych::Paper B::Old Age` |
| Child/ADHD/autism | `MRCPsych::Paper B::Child & Adolescent` |
| CBT/DBT/therapy | `MRCPsych::Paper B::Psychotherapy` |
| Statistics/research | `MRCPsych::Paper B::Critical Review` |
| MHA/services | `MRCPsych::Paper B::Service Organization` |

Override with $ARGUMENTS if specified.

## Step 3: Generate Cards

Create multiple cards per question:

1. **Core Concept** - Main learning point
2. **Mechanism** - Why/how it works
3. **Clinical Application** - Practice scenario
4. **Cloze** - For criteria/numbers/definitions

### Format Requirements

**Basic Card:**
```
Front: [Paper A - Pharmacology] What is the mechanism of clozapine?
Back: D2/5-HT2A antagonist (atypical antipsychotic)
• Also blocks muscarinic, histaminic, alpha receptors
```

**Cloze Card:**
```
Text: Clozapine requires {{c1::weekly}} monitoring for first {{c2::18 weeks}}
Extra: Risk of agranulocytosis ~1%
```

## Step 4: VALIDATE (Mandatory)

**Before syncing, EVERY card must pass:**

| Check | Requirement | If Fail |
|-------|-------------|---------|
| Prefix | `[Paper X - Topic]` at start | Add it |
| Single concept | No "list all", "name the" | Split card |
| Answer length | ≤25 words primary | Shorten |
| Tags | `mrcpsych` + `paper-x` + topic | Add them |
| Deck | Valid deck path | Fix it |

**Validation Loop:**
```
FOR each card:
    errors = validate(card)
    IF errors:
        regenerate card to fix errors
        re-validate (max 3 attempts)
    IF still fails after 3 attempts:
        flag for manual review
```

## Step 5: Sync to Anki

Only sync validated cards:

```python
from scripts.anki_connect import AnkiConnect

anki = AnkiConnect()

# Check connection
if not anki.is_connected():
    print("ERROR: Start Anki and ensure AnkiConnect is installed")
    return

# Add each validated card
cards_created = []
for card in validated_cards:
    if card['type'] == 'basic':
        note_id = anki.add_note(
            deck_name=card['deck'],
            front=card['front'],
            back=card['back'],
            tags=card['tags']
        )
    else:  # cloze
        note_id = anki.add_cloze_note(
            deck_name=card['deck'],
            text=card['front'],
            extra=card['back'],
            tags=card['tags']
        )
    cards_created.append((card['front'][:50], note_id))

print(f"Synced {len(cards_created)} cards")
```

## Step 6: Report

Output after completion:

```
**X cards synced to Anki**

1. [Card front preview] ✓
2. [Card front preview] ✓
...

**Deck**: MRCPsych::Paper A::Topic
**Tags**: mrcpsych, paper-a, topic, specific-tags
```

## Tag Requirements

**Always include:**
- `mrcpsych`
- `paper-a` OR `paper-b`
- Topic: `pharmacology`, `neuroscience`, `adult-psych`, etc.

**Add when relevant:**
- Source: `spmm`, `mrcpsychmentor`
- Condition: `schizophrenia`, `depression`, `dementia`
- Drug: `lithium`, `clozapine`, `ssri`
- Priority: `high-yield`

---

**This workflow is autonomous. Execute without asking for confirmation.**
