---
name: mrcpsych-flashcard-generator
description: Generates high-quality MRCPsych flashcards from exam content using evidence-based spaced repetition principles. Use when analyzing exam questions, creating study materials, or converting learning content into Anki cards.
allowed-tools: Read, Write, Edit, Bash
---

# MRCPsych Flashcard Generator

This skill creates optimized flashcards for MRCPsych Paper A and Paper B exams following the 20 rules of formulating knowledge.

## When to Use

- User pastes an image of an exam question
- User provides text from question banks (SPMM, MRCPsychMentor)
- User asks to create flashcards from study material
- Converting clinical scenarios into learning cards

## Core Principles

### 1. Minimum Information
Each card tests ONE concept. Never ask "What are the features of X?" - split into individual cards.

### 2. Atomic Cards
```
BAD: "List the symptoms of neuroleptic malignant syndrome"
GOOD: "What is the characteristic muscle finding in NMS?" → Rigidity (lead-pipe)
```

### 3. Cloze for Criteria/Numbers
```
Text: NMS typically presents within {{c1::2 weeks}} of starting antipsychotics
Extra: Most cases within first week; risk increases with high-potency agents
```

### 4. Context Prefixes
Always prefix with paper and topic:
- `[Paper A - Pharmacology]`
- `[Paper B - Adult]`
- `[Critical Review]`

### 5. Bidirectional When Valuable
Create both:
- "Drug X treats condition Y" → Y
- "Condition Y is treated by drug X" → X

## Card Templates

### Basic Q&A
```
Front: [Paper A - Neuroscience] What neurotransmitter is primarily affected in Parkinson's disease?
Back: Dopamine
• Degeneration of dopaminergic neurons in substantia nigra
• Leads to motor symptoms: tremor, rigidity, bradykinesia
```

### Clinical Vignette
```
Front: [Paper B - Adult] A 45-year-old man presents with 2 weeks of low mood, anhedonia, weight loss, and early morning wakening. He denies suicidal ideation. What is the most appropriate first-line treatment?
Back: SSRI antidepressant (e.g., sertraline, fluoxetine)
• First-line for moderate depression per NICE guidelines
• Combine with psychological therapy if available
```

### Cloze Deletion
```
Text: NICE recommends {{c1::SSRI (sertraline)}} as first-line for GAD, {{c2::SNRI}} as second-line, and {{c3::pregabalin}} if SSRIs/SNRIs not tolerated
Extra: Per NICE CG113. Pregabalin is third-line, not an equal alternative. CBT also effective.
```

### Mechanism Card
```
Front: [Paper A - Pharmacology] How do SSRIs improve depression symptoms?
Back: Block serotonin reuptake transporter (SERT), increasing synaptic 5-HT
• Therapeutic effect takes 2-4 weeks due to receptor downregulation
• Initially may increase anxiety before improvement
```

## Classification Guide

### Paper A Topics
- **Neuroscience**: Neuroanatomy, neurophysiology, neuropathology
- **Psychology**: Learning theory, cognitive psychology, developmental psychology
- **Pharmacology**: Drug mechanisms, pharmacokinetics, side effects
- **Genetics**: Inheritance patterns, genetic disorders, epigenetics

### Paper B Topics
- **General Adult** (20%): Schizophrenia, mood disorders, anxiety, personality disorders
- **Old Age** (9%): Dementia, delirium, depression in elderly
- **Child & Adolescent** (9%): ADHD, autism, conduct disorders
- **Psychotherapy** (5.5%): CBT, DBT, psychodynamic, group therapy
- **Critical Review** (33.5%): Statistics, study design, evidence appraisal
- **Services** (5.5%): Mental Health Act, service models, MDT working

## Output Format

Generate cards as structured data for Anki sync:

```python
cards = [
    {
        "deck": "MRCPsych::Paper A::Pharmacology",
        "type": "Basic",
        "front": "[Paper A - Pharmacology] Question text",
        "back": "Answer with explanation",
        "tags": ["mrcpsych", "paper-a", "pharmacology", "specific-topic"]
    },
    {
        "deck": "MRCPsych::Paper A::Pharmacology",
        "type": "Cloze",
        "front": "Cloze text with {{c1::deletions}}",
        "back": "Extra information",
        "tags": ["mrcpsych", "paper-a", "pharmacology"]
    }
]
```

## Quality Checklist

Before finalizing each card:
- [ ] Tests a single concept
- [ ] Clear, unambiguous question
- [ ] Concise answer (<25 words ideal)
- [ ] Context prefix included
- [ ] Appropriate tags
- [ ] No enumeration (lists split)
- [ ] Source cited if guideline-based
