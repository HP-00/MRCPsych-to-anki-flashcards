# MRCPsych-to-Anki Flashcards

Automated workflow for converting MRCPsych exam question bank images into high-quality Anki flashcards.

## Required Context (Auto-Loaded)

**ALWAYS follow these when creating flashcards:**
- Quality standards: @.claude/rules/flashcard-quality.md
- Topic classification: @.claude/rules/mrcpsych-topics.md

## Quick Start

When the user provides MRCPsych exam content (image, text, or question details), immediately:
1. Analyze the content (exam question, explanation, or clinical scenario)
2. Extract key learning points using medical education principles
3. Generate optimized flashcards following the 20 rules of formulating knowledge
4. Add flashcards to Anki via AnkiConnect API (localhost:8765)

**Supported input methods:**
- Paste an image (screenshot of exam question)
- Paste text (copy/paste question details)
- Use `/flashcard` command
- Add a prompt with content (e.g., "create flashcards from this")

## Target Exams

### MRCPsych Paper A (3 hours, 150 questions)
- **Focus**: Basic sciences - neuroscience, psychology, pharmacology fundamentals
- **Format**: Single-best-answer MCQs and EMIs
- **Topics**: Neuroanatomy, neurophysiology, psychopharmacology, psychology, genetics

### MRCPsych Paper B (3 hours, 150 questions)
- **Question Types**: ~100 MCQs + ~50 EMIs
- **Clinical Topics**:
  - General Adult Psychiatry (20%/30 marks)
  - Old Age Psychiatry (9%/14 marks)
  - Child & Adolescent Psychiatry (9%/14 marks)
  - Psychotherapy (5.5%/8 marks)
  - Service Organization (5.5%/8 marks)
- **Critical Review** (~33.5%/50 marks): Statistics, research methods, epidemiology

## Question Bank Sources

### SPMM Course (spmmcourse.com)
- 8,000+ questions with evidence-based explanations
- Mock exams following exam blueprint
- Paper B e-Crashclass (19 hrs content)

### MRCPsychMentor (mrcpsychmentor.com)
- 5,500+ questions based on previous exams
- Best Answer 1 of 5 MCQs & EMIs format
- Performance tracking and comparison
- Detailed exam-relevant explanations

## Flashcard Creation Principles

### The 20 Rules Applied to MRCPsych

1. **Understand First**: Know the mechanism before memorizing drug names
2. **Build the Picture**: Study pathophysiology before creating cards
3. **Master Basics**: Anatomy, biochemistry before complex pathology
4. **Minimum Information**: One fact per card
   - BAD: "What are features of schizophrenia?"
   - GOOD: "What is the first-rank symptom of thought insertion?"
5. **Use Cloze**: "Risperidone is a ...(class) antipsychotic" → Answer: "atypical/D2 antagonist"
6. **Include Images**: Neuroanatomy diagrams, ECG patterns, brain scans
7. **Use Mnemonics**: Create memory aids for criteria (e.g., "DIGFAST" for mania)
8. **Avoid Sets**: Never "List all symptoms of X" - split into individual cards
9. **Avoid Enumerations**: Use overlapping clozes for ordered processes
10. **Combat Interference**: Distinguish similar terms with context
11. **Optimize Wording**: Direct questions with single-concept answers
12. **Link Knowledge**: Connect new info to established concepts
13. **Personalize**: Use clinical examples
14. **Emotional States**: Associate with clinical consequences
15. **Context Cues**: Prefix cards (e.g., "Psychopharm:", "CBT:")
16. **Redundancy**: Create both active and passive recall cards
17. **Include Sources**: Reference guidelines (NICE, BAP, Maudsley)
18. **Date Stamp**: Mark guideline-dependent content with year
19. **Prioritize**: Focus on high-yield exam topics

### Card Format for MRCPsych

**Front (Question)**:
- Clear, single-concept question
- Context prefix when helpful (Paper A/B, Topic)
- Clinical vignette if testing application

**Back (Answer)**:
- Concise primary answer (1-2 lines)
- Key explanation point
- Source/guideline reference if applicable
- Related high-yield fact (optional)

## Anki Configuration

### Required Setup
1. Install AnkiConnect add-on: Tools → Add-ons → Get Add-ons → Code: **2055492159**
2. Restart Anki
3. Verify: `curl localhost:8765 -X POST -d '{"action": "version", "version": 6}'`

### Target Deck Structure
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

### Note Types
- **Basic**: Front/Back for simple Q&A
- **Cloze**: For fill-in-the-blank
- **Basic (with Extra)**: For cards needing extended explanation

## Workflow Commands

- `/flashcard` - Analyze image and create flashcards from it
- `/anki-sync` - Sync pending flashcards to Anki
- `/flashcard-review` - Review and edit generated flashcards before sync

## AnkiConnect API

**Endpoint**: `http://127.0.0.1:8765`

**Add Note**:
```json
{
  "action": "addNote",
  "version": 6,
  "params": {
    "note": {
      "deckName": "MRCPsych::Paper A::Neuroscience",
      "modelName": "Basic",
      "fields": {"Front": "Question", "Back": "Answer"},
      "tags": ["mrcpsych", "paper-a", "neuroscience"]
    }
  }
}
```

## Important Files

- `scripts/anki_connect.py` - AnkiConnect API wrapper
- `.claude/commands/flashcard.md` - Main flashcard creation command
- `.claude/agents/flashcard-creator.md` - Specialized flashcard agent
- `.claude/skills/flashcard-generator/SKILL.md` - Flashcard generation skill

## Tags Strategy

Use consistent tags for organization:
- Source: `spmm`, `mrcpsychmentor`
- Paper: `paper-a`, `paper-b`
- Topic: `neuroscience`, `pharmacology`, `adult-psych`, etc.
- Type: `mcq`, `emi`, `critical-review`
- Priority: `high-yield`, `detail`
