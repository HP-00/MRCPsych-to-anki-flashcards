# MRCPsych-to-Anki Flashcards

An AI-powered workflow that converts MRCPsych exam questions into high-quality Anki flashcards using Claude Code. Built on evidence-based spaced repetition principles (the "20 rules of formulating knowledge").

## Features

- **Content-to-Flashcard**: Paste exam questions (images or text) directly into Claude Code
- **Automatic Topic Classification**: Cards are sorted into Paper A/B subdeck structure
- **Quality Validation**: Built-in checks ensure cards follow spaced repetition best practices
- **Direct Anki Sync**: Cards sync instantly to local Anki via AnkiConnect API
- **Smart Card Generation**: Creates multiple card types (Basic Q&A, Cloze deletions, Clinical vignettes)

> **New here?** Check out the [Quick Start Guide](QUICK_START.md) to get running in 5 minutes.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Flashcard Quality Standards](#flashcard-quality-standards)
- [Card Types & Formats](#card-types--formats)
- [Topic Classification](#topic-classification)
- [Tagging System](#tagging-system)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Resources](#resources)

---

## Requirements

### System Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | 3.8+ | For AnkiConnect scripts |
| **Anki** | 2.1.x+ | Desktop application |
| **Claude Code** | Latest | Anthropic's CLI tool |
| **AnkiConnect** | Add-on 2055492159 | Anki add-on for API access |

### Dependencies

This project uses Python's standard library only - no external packages required:
- `json` - API communication
- `urllib` - HTTP requests
- `base64` - Media file encoding
- `re` - Validation patterns
- `pathlib` - File path handling

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/HP-00/MRCPsych-to-anki-flashcards.git
cd MRCPsych-to-anki-flashcards
```

### Step 2: Install Anki

Download and install Anki from: https://apps.ankiweb.net/

Supported platforms:
- macOS
- Windows
- Linux

### Step 3: Install AnkiConnect Add-on

1. Open Anki
2. Go to **Tools** → **Add-ons** → **Get Add-ons...**
3. Enter add-on code: `2055492159`
4. Click **OK** and restart Anki

**Alternative (manual installation):**
```bash
# macOS
cd ~/Library/Application\ Support/Anki2/addons21/
git clone https://git.sr.ht/~foosoft/anki-connect 2055492159

# Linux
cd ~/.local/share/Anki2/addons21/
git clone https://git.sr.ht/~foosoft/anki-connect 2055492159

# Windows
cd %APPDATA%\Anki2\addons21\
git clone https://git.sr.ht/~foosoft/anki-connect 2055492159
```

### Step 4: Verify AnkiConnect Installation

With Anki running, test the connection:

```bash
curl -s localhost:8765 -X POST -d '{"action": "version", "version": 6}'
```

Expected response:
```json
{"result": 6, "error": null}
```

### Step 5: Create Deck Structure

Run the setup script to create all MRCPsych decks:

```bash
python3 scripts/setup_anki_decks.py
```

Optional: Add sample cards to verify everything works:
```bash
python3 scripts/setup_anki_decks.py --with-samples
```

### Step 6: Install Claude Code

Follow the official installation guide: https://github.com/anthropics/claude-code

```bash
# macOS/Linux
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

---

## Quick Start

### 1. Start Anki
Ensure Anki is running (AnkiConnect requires Anki to be open).

### 2. Open the Project in Claude Code

```bash
cd MRCPsych-to-anki-flashcards
claude
```

### 3. Create Flashcards

**Method A: Paste content directly**
Paste an image (screenshot) or text (copy/paste question) into Claude Code. The workflow will automatically:
1. Analyze the content
2. Extract key learning points
3. Generate optimized flashcards
4. Sync them to Anki

**Method B: Use the slash command**
```
/flashcard
```
Then paste your image or text.

**Method C: Add a prompt**
Paste content with instructions like "create flashcards from this question".

### Example Interaction

```
User: [pastes image of question about lithium monitoring]

Claude: Analyzing the exam question...

I've identified this as a Paper A Pharmacology question about lithium monitoring.

Creating flashcards:

1. Core concept card:
   Front: [Paper A - Pharmacology] What is the therapeutic range for serum lithium?
   Back: 0.6-1.0 mmol/L
   • Levels should be measured 12 hours post-dose

2. Clinical card:
   Front: [Paper A - Pharmacology] At what serum level does lithium toxicity typically occur?
   Back: >1.5 mmol/L
   • Signs: coarse tremor, GI symptoms, ataxia, confusion

3. Cloze card:
   Text: Lithium levels should be checked {{c1::weekly}} for the first month, then every {{c2::3 months}} once stable

**3 cards synced to MRCPsych::Paper A::Pharmacology**
Tags: mrcpsych, paper-a, pharmacology, lithium, high-yield
```

---

## Usage

### Available Commands

| Command | Description |
|---------|-------------|
| `/flashcard` | Main command - analyze content (image or text) and create flashcards |
| `/anki-sync` | Manually sync pending flashcards to Anki |

### Workflow Options

#### Option 1: Automatic (Recommended)
Paste any exam content directly - images (screenshots) or text (copy/paste). Claude will automatically create flashcards.

#### Option 2: With Command
Use `/flashcard` followed by your content for explicit control.

#### Option 3: With Prompt
Paste content with instructions like "create flashcards from this".

### Python API Usage

You can also use the scripts directly:

```python
from scripts.anki_connect import AnkiConnect

anki = AnkiConnect()

# Check connection
if not anki.is_connected():
    print("Start Anki first!")
    exit()

# Add a basic card
note_id = anki.add_note(
    deck_name="MRCPsych::Paper A::Pharmacology",
    front="[Paper A - Pharmacology] What is the mechanism of SSRIs?",
    back="Block serotonin reuptake transporter (SERT), increasing synaptic 5-HT",
    tags=["mrcpsych", "paper-a", "pharmacology", "ssri"]
)

# Add a cloze card
note_id = anki.add_cloze_note(
    deck_name="MRCPsych::Paper A::Pharmacology",
    text="SSRIs take {{c1::2-4 weeks}} to show therapeutic effect",
    extra="Due to receptor downregulation and neuroplastic changes",
    tags=["mrcpsych", "paper-a", "pharmacology", "ssri"]
)
```

---

## Project Structure

```
MRCPsych-to-anki-flashcards/
├── README.md                        # This file
├── CLAUDE.md                        # Project context for Claude Code
├── scripts/
│   ├── anki_connect.py              # AnkiConnect API wrapper
│   ├── validate_flashcard.py        # Card quality validation
│   └── setup_anki_decks.py          # Deck structure setup
└── .claude/
    ├── commands/
    │   └── flashcard.md             # /flashcard slash command
    ├── agents/
    │   └── flashcard-creator.md     # Specialized flashcard agent
    ├── skills/
    │   ├── flashcard-generator/
    │   │   └── SKILL.md             # Flashcard generation skill
    │   └── anki-sync/
    │       └── SKILL.md             # Anki synchronization skill
    ├── rules/
    │   ├── flashcard-quality.md     # Quality standards
    │   └── mrcpsych-topics.md       # Topic classification reference
    └── hooks/                       # (reserved for future use)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Auto-loaded context for Claude Code sessions |
| `scripts/anki_connect.py` | Python wrapper for AnkiConnect API |
| `scripts/validate_flashcard.py` | Validates cards before sync |
| `scripts/setup_anki_decks.py` | Creates deck hierarchy in Anki |
| `.claude/commands/flashcard.md` | Defines `/flashcard` command workflow |
| `.claude/agents/flashcard-creator.md` | Specialized agent for flashcard creation |
| `.claude/rules/flashcard-quality.md` | Quality standards and validation rules |
| `.claude/rules/mrcpsych-topics.md` | Topic classification reference |

---

## Flashcard Quality Standards

This workflow implements the **20 Rules of Formulating Knowledge** for effective spaced repetition.

### Mandatory Quality Checks

Every card must pass these validation checks before syncing:

| Check | Requirement | Fail Action |
|-------|-------------|-------------|
| **Context Prefix** | Starts with `[Paper A - Topic]` or `[Paper B - Topic]` | Auto-add prefix |
| **Single Concept** | Tests ONE fact only | Split into atomic cards |
| **No Enumeration** | No "list all", "name the", "what are the" | Split card |
| **Answer Length** | Primary answer ≤25 words | Shorten |
| **Required Tags** | Has `mrcpsych` + `paper-a` or `paper-b` | Add tags |
| **Valid Deck** | Uses approved deck path | Fix deck name |
| **Cloze Format** | Cloze cards have `{{c1::...}}` syntax | Add deletions |

### Enumeration Detection

Cards are automatically rejected if the front contains:
- "list all" / "list the"
- "name all" / "name the"
- "what are the" / "what are all"
- "enumerate" / "give all"
- "describe all" / "mention all"

### Examples

**REJECT** (multiple concepts):
```
Front: What are the side effects of lithium?
```

**ACCEPT** (atomic):
```
Front: [Paper A - Pharmacology] What GI side effect is common with lithium?
Back: Nausea and diarrhea
• Usually dose-related and transient
```

---

## Card Types & Formats

### 1. Basic Q&A Card

Best for: Definitions, mechanisms, clinical presentations

```
Front: [Paper A - Neuroscience] What neurotransmitter is depleted in Parkinson's disease?
Back: Dopamine
• Degeneration of dopaminergic neurons in substantia nigra
• Leads to motor symptoms: tremor, rigidity, bradykinesia
```

### 2. Cloze Deletion Card

Best for: Numerical values, criteria, time periods, drug doses

```
Text: The therapeutic range for lithium is {{c1::0.6-1.0}} mmol/L; toxicity occurs above {{c2::1.5}} mmol/L
Extra: Check levels 12 hours post-dose. Symptoms of toxicity: coarse tremor, ataxia, confusion.
```

### 3. Clinical Vignette Card

Best for: Applying knowledge to scenarios, testing diagnosis/management

```
Front: [Paper B - Adult] A 35-year-old woman presents with 3 weeks of low mood,
       poor concentration, insomnia, and suicidal thoughts. She has no past
       psychiatric history. What is the first-line pharmacological treatment?
Back: SSRI antidepressant (e.g., sertraline)
• First-line per NICE guidelines for moderate-severe depression
• Start at low dose and titrate
```

### 4. Mechanism Card

Best for: Understanding "why" and "how"

```
Front: [Paper A - Pharmacology] Why does lithium cause nephrogenic diabetes insipidus?
Back: Reduces aquaporin-2 expression in collecting ducts, impairing water reabsorption
• Presents as polyuria, polydipsia
• May be irreversible with long-term use
```

---

## Topic Classification

### Paper A (Basic Sciences)

| Topic | Coverage | Examples |
|-------|----------|----------|
| **Neuroscience** | Neuroanatomy, neurophysiology, neuropathology | Brain structures, neurotransmitters, pathways |
| **Psychology** | Learning theory, cognitive, developmental, social | Conditioning, Piaget stages, attachment |
| **Pharmacology** | Pharmacokinetics, pharmacodynamics, drug classes | Drug mechanisms, side effects, interactions |
| **Genetics** | Basic genetics, psychiatric genetics | Heritability, chromosomal disorders |

### Paper B (Clinical)

| Topic | Weight | Coverage |
|-------|--------|----------|
| **General Adult** | 20% | Schizophrenia, mood disorders, anxiety, personality |
| **Critical Review** | 33.5% | Statistics, study design, evidence appraisal |
| **Old Age** | 9% | Dementia, delirium, elderly psychiatry |
| **Child & Adolescent** | 9% | ADHD, autism, developmental disorders |
| **Psychotherapy** | 5.5% | CBT, DBT, psychodynamic, group therapy |
| **Service Organization** | 5.5% | Mental Health Act, service models, forensic |

---

## Tagging System

### Required Tags (every card)

- `mrcpsych`
- `paper-a` OR `paper-b`
- Topic tag: `neuroscience`, `psychology`, `pharmacology`, `genetics`, `adult-psych`, `old-age`, `child-psych`, `psychotherapy`, `critical-review`, `services`

### Optional Tags

| Category | Examples |
|----------|----------|
| **Source** | `spmm`, `mrcpsychmentor` |
| **Priority** | `high-yield`, `detail` |
| **Condition** | `schizophrenia`, `depression`, `dementia`, `bipolar` |
| **Drug** | `lithium`, `clozapine`, `ssri`, `antipsychotic` |
| **Concept** | `mechanism`, `diagnosis`, `management`, `epidemiology` |

---

## Deck Structure

Cards are automatically sorted into this hierarchy:

```
MRCPsych/
├── Paper A/
│   ├── Neuroscience
│   ├── Psychology
│   ├── Pharmacology
│   └── Genetics
└── Paper B/
    ├── General Adult
    ├── Old Age
    ├── Child & Adolescent
    ├── Psychotherapy
    ├── Critical Review
    └── Service Organization
```

**Valid deck paths:**
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

---

## Troubleshooting

### Connection Issues

#### "Cannot connect to Anki" / "Connection refused"

1. **Ensure Anki is running** - AnkiConnect requires the Anki application to be open
2. **Verify AnkiConnect is installed**:
   - Go to Tools → Add-ons
   - Should see "AnkiConnect" in the list
3. **Restart Anki** after installing AnkiConnect
4. **Check firewall** - ensure localhost:8765 is not blocked
5. **Test manually**:
   ```bash
   curl localhost:8765 -X POST -d '{"action": "version", "version": 6}'
   ```

#### "Model was not found"

Use built-in note types only:
- `Basic`
- `Cloze`
- `Basic (and reversed card)`

Or create the required note type in Anki first (Tools → Manage Note Types).

### Card Issues

#### Cards not appearing in Anki

1. Check the correct deck (Browse → select deck)
2. Verify the sync succeeded (no error messages)
3. Try Anki sync if using AnkiWeb (click sync button)

#### Duplicate detection errors

By default, duplicates are rejected. To allow duplicates:

```python
anki.add_note(..., allow_duplicate=True)
```

### Validation Failures

#### "ENUMERATION: Contains 'list all'"

Split the card into individual atomic cards:

```
# BAD
"List all symptoms of NMS"

# GOOD
"What is the characteristic temperature finding in NMS?" → Hyperthermia (>38°C)
"What is the characteristic muscle finding in NMS?" → Rigidity (lead-pipe)
```

#### "ANSWER_TOO_LONG"

Keep primary answer ≤25 words. Use bullet points for extra context:

```
# BAD
Back: "Serotonin syndrome is caused by excessive serotonergic activity and presents
       with altered mental status, autonomic instability, and neuromuscular abnormalities
       such as hyperreflexia, clonus, and tremor, which can be life-threatening."

# GOOD
Back: Excessive serotonergic activity causing neuromuscular, autonomic, and mental status changes
      • Hyperreflexia, clonus, tremor
      • Hyperthermia, diaphoresis
      • Can be life-threatening
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Quality Standards**: All flashcard-related changes must maintain the quality standards in `.claude/rules/flashcard-quality.md`
2. **Testing**: Test any script changes with actual Anki sync
3. **Documentation**: Update README for any new features

### Development Setup

```bash
# Clone repo
git clone https://github.com/HP-00/MRCPsych-to-anki-flashcards.git
cd MRCPsych-to-anki-flashcards

# Test scripts
python3 scripts/anki_connect.py  # Tests connection
python3 scripts/validate_flashcard.py  # Tests validation
```

---

## Resources

### MRCPsych Exam Information

- [Royal College of Psychiatrists - Exams](https://www.rcpsych.ac.uk/training/exams)
- [MRCPsych Paper A Syllabus](https://www.rcpsych.ac.uk/training/exams/mrcpsych-written-exams)
- [MRCPsych Paper B Syllabus](https://www.rcpsych.ac.uk/training/exams/mrcpsych-written-exams)

### Question Banks

- [SPMM Course](https://spmmcourse.com/) - 8,000+ questions with explanations
- [MRCPsychMentor](https://www.mrcpsychmentor.com/) - 5,500+ exam-style questions

### Anki & Spaced Repetition

- [Anki Download](https://apps.ankiweb.net/)
- [AnkiConnect Documentation](https://git.sr.ht/~foosoft/anki-connect)
- [20 Rules of Formulating Knowledge](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge)

### Claude Code

- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)

---

## License

MIT License - see LICENSE file for details.

---

## Acknowledgments

- Built with [Claude Code](https://github.com/anthropics/claude-code) by Anthropic
- Uses [AnkiConnect](https://git.sr.ht/~foosoft/anki-connect) for Anki integration
- Flashcard principles based on [SuperMemo's 20 Rules](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge)
