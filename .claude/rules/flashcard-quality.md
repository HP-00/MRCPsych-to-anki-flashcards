---
paths: "**/*.md"
---

# Flashcard Quality Standards

These rules ensure all generated flashcards meet evidence-based quality standards for effective spaced repetition learning.

## Mandatory Quality Checks

### 1. Single Concept Rule
Each flashcard MUST test exactly ONE concept. If you find yourself using "and" or listing multiple items, SPLIT the card.

**REJECT**:
- "What are the side effects of lithium?"
- "Name the first-rank symptoms of schizophrenia"

**ACCEPT**:
- "What GI side effect is common with lithium?" → Nausea, diarrhea
- "Which first-rank symptom involves hearing voices discussing the patient?" → Third-person auditory hallucinations

### 2. No Enumerations
Never ask to "list" or "name all" items. Each item becomes its own card.

**REJECT**: "List the components of CBT"
**ACCEPT**:
- "What is the cognitive component of CBT?" → Identifying and challenging negative automatic thoughts
- "What is the behavioral component of CBT?" → Behavioral experiments and activity scheduling

### 3. Maximum Answer Length
Back of card should be ≤25 words for the primary answer. Additional context can follow with bullet points.

### 4. Context Prefix Required
Every card front MUST start with context in brackets:
- `[Paper A - Neuroscience]`
- `[Paper A - Pharmacology]`
- `[Paper B - Adult]`
- `[Paper B - Critical Review]`
- etc.

### 5. Clinical Relevance
Where applicable, include:
- Clinical significance
- When this knowledge matters in practice
- Common exam scenarios

### 6. Source Attribution
For guideline-based answers, include the source:
- `(NICE CG90)` for depression guidelines
- `(BAP 2019)` for psychopharmacology
- `(Maudsley)` for prescribing guidance
- `(DSM-5)` / `(ICD-11)` for diagnostic criteria

## Cloze Deletion Rules

### Use Cloze For:
- Numerical values: `therapeutic lithium level is {{c1::0.6-1.0}} mmol/L`
- Diagnostic criteria: `MDD requires {{c1::5}} symptoms for {{c2::2 weeks}}`
- Drug classes: `{{c1::Clozapine}} is the only antipsychotic licensed for {{c2::treatment-resistant}} schizophrenia`
- Time periods: `antidepressant response typically takes {{c1::2-4 weeks}}`

### Cloze Formatting:
- Use `{{c1::text}}` for deletions
- Number sequentially for related deletions in same card
- Keep deletions to key terms, not entire phrases
- Include meaningful "Extra" field for context

## Tagging Requirements

### Mandatory Tags:
- `mrcpsych`
- Paper: `paper-a` OR `paper-b`
- Topic area (see list below)

### Topic Tags:
**Paper A**: `neuroscience`, `psychology`, `pharmacology`, `genetics`
**Paper B**: `adult-psych`, `old-age`, `child-psych`, `psychotherapy`, `critical-review`, `services`

### Optional Tags:
- Source: `spmm`, `mrcpsychmentor`
- Priority: `high-yield`
- Specific: condition names, drug names

## Card Type Selection

### Use Basic Q&A For:
- Definitions
- Mechanisms of action
- Clinical presentations
- Management steps

### Use Cloze For:
- Numerical facts
- Diagnostic criteria
- Drug doses/levels
- Time courses

### Use Basic (Reversed) For:
- Important bidirectional associations
- Drug-condition pairs
- Symptom-diagnosis pairs

## Deck Assignment

Assign to most specific applicable deck:
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

## Pre-Sync Validation (MANDATORY)

**Every card MUST pass ALL checks before syncing.**

### Validation Checks (Pass/Fail)

| Check | PASS | FAIL | Action on Fail |
|-------|------|------|----------------|
| **Context Prefix** | Front starts with `[Paper A - Topic]` or `[Paper B - Topic]` | Missing or malformed prefix | Add correct prefix |
| **Single Concept** | Tests ONE fact only | Contains "list all", "name the", "what are the" | Split into atomic cards |
| **Answer Length** | Primary answer ≤25 words | >25 words in first line | Shorten answer |
| **Required Tags** | Has `mrcpsych` AND (`paper-a` OR `paper-b`) | Missing required tags | Add tags |
| **Valid Deck** | Uses approved deck path (see below) | Invalid or missing deck | Fix deck name |
| **Cloze Format** | Cloze cards have `{{c1::...}}` | Missing cloze deletions | Add deletions |
| **Non-Empty** | Front and back have content | Empty field | Add content |

### Enumeration Detection

**FAIL immediately if front contains:**
- "list all"
- "list the"
- "name all"
- "name the"
- "what are the"
- "what are all"
- "enumerate"
- "give all"
- "describe all"
- "mention all"

### Valid Deck Paths

Only these decks are valid:
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

### Validation Loop

```
FOR each generated card:
    1. Run all validation checks
    2. IF any check fails:
        - Log the failure reason
        - Regenerate card to fix issue
        - Re-validate
    3. Maximum 3 regeneration attempts
    4. IF still fails → flag for manual review
    5. IF passes → add to sync queue

ONLY sync cards that pass ALL checks.
```

### Pre-Sync Checklist

Before syncing to Anki, verify:
- [ ] All cards follow single-concept rule
- [ ] No enumeration cards
- [ ] Context prefixes present on ALL cards
- [ ] Primary answers ≤25 words
- [ ] Tags include: mrcpsych, paper-a/paper-b, topic
- [ ] Deck assignment uses valid path
- [ ] Cloze cards have proper `{{c1::}}` format
- [ ] No duplicate content from previous sessions
