#!/usr/bin/env python3
"""
Flashcard validation script for MRCPsych cards.

Validates cards against quality rules before syncing to Anki.
Returns errors for non-compliant cards so they can be regenerated.

Usage:
    from validate_flashcard import validate_card, validate_cards

    errors = validate_card(front, back, tags, deck)
    if errors:
        print(f"Card failed validation: {errors}")
"""

import re
from typing import List, Dict, Optional


# Enumeration phrases that indicate a card should be split
ENUMERATION_PHRASES = [
    'list all',
    'list the',
    'name all',
    'name the',
    'what are the',
    'what are all',
    'enumerate',
    'give all',
    'describe all',
    'mention all',
]

# Valid context prefixes
VALID_PREFIXES = [
    r'\[Paper A',
    r'\[Paper B',
    r'\[Critical Review\]',
]

# Valid deck patterns
VALID_DECKS = [
    'MRCPsych::Paper A::Neuroscience',
    'MRCPsych::Paper A::Psychology',
    'MRCPsych::Paper A::Pharmacology',
    'MRCPsych::Paper A::Genetics',
    'MRCPsych::Paper B::General Adult',
    'MRCPsych::Paper B::Old Age',
    'MRCPsych::Paper B::Child & Adolescent',
    'MRCPsych::Paper B::Psychotherapy',
    'MRCPsych::Paper B::Critical Review',
    'MRCPsych::Paper B::Service Organization',
]

# Required tags
REQUIRED_TAGS = ['mrcpsych']
PAPER_TAGS = ['paper-a', 'paper-b']


def validate_card(
    front: str,
    back: str,
    tags: List[str],
    deck: str,
    is_cloze: bool = False
) -> List[str]:
    """
    Validate a single flashcard against quality rules.

    Args:
        front: Front of card (question) or cloze text
        back: Back of card (answer) or extra field
        tags: List of tags
        deck: Target deck name
        is_cloze: Whether this is a cloze card

    Returns:
        List of error messages. Empty list = card is valid.
    """
    errors = []

    # Rule 1: Context prefix required (for non-cloze cards)
    if not is_cloze:
        has_prefix = any(re.search(prefix, front) for prefix in VALID_PREFIXES)
        if not has_prefix:
            errors.append("MISSING_PREFIX: Card must start with [Paper A - Topic] or [Paper B - Topic]")

    # Rule 2: No enumeration (single concept only)
    front_lower = front.lower()
    for phrase in ENUMERATION_PHRASES:
        if phrase in front_lower:
            errors.append(f"ENUMERATION: Contains '{phrase}' - split into atomic cards")
            break

    # Rule 3: Answer length check (primary answer ≤25 words)
    if back:
        # Get first line as primary answer
        primary_answer = back.split('\n')[0].strip()
        # Remove bullet points and formatting
        primary_answer = re.sub(r'^[•\-\*]\s*', '', primary_answer)
        word_count = len(primary_answer.split())
        if word_count > 25:
            errors.append(f"ANSWER_TOO_LONG: Primary answer has {word_count} words (max 25)")

    # Rule 4: Required tags
    tags_lower = [t.lower() for t in tags]

    if 'mrcpsych' not in tags_lower:
        errors.append("MISSING_TAG: Must include 'mrcpsych' tag")

    has_paper_tag = any(t in tags_lower for t in PAPER_TAGS)
    if not has_paper_tag:
        errors.append("MISSING_TAG: Must include 'paper-a' or 'paper-b' tag")

    # Rule 5: Valid deck
    if deck not in VALID_DECKS:
        errors.append(f"INVALID_DECK: '{deck}' is not a valid deck. Use one of: {', '.join(VALID_DECKS)}")

    # Rule 6: Cloze format check
    if is_cloze:
        if '{{c' not in front:
            errors.append("INVALID_CLOZE: Cloze card must contain {{c1::...}} deletions")

    # Rule 7: Empty content check
    if not front.strip():
        errors.append("EMPTY_FRONT: Card front cannot be empty")
    if not back.strip() and not is_cloze:
        errors.append("EMPTY_BACK: Card back cannot be empty (except for cloze cards)")

    return errors


def validate_cards(cards: List[Dict]) -> Dict[int, List[str]]:
    """
    Validate multiple cards.

    Args:
        cards: List of card dicts with keys: front, back, tags, deck, is_cloze (optional)

    Returns:
        Dict mapping card index to list of errors. Only includes cards with errors.
    """
    results = {}

    for i, card in enumerate(cards):
        errors = validate_card(
            front=card.get('front', ''),
            back=card.get('back', ''),
            tags=card.get('tags', []),
            deck=card.get('deck', ''),
            is_cloze=card.get('is_cloze', False)
        )
        if errors:
            results[i] = errors

    return results


def format_validation_report(cards: List[Dict], errors: Dict[int, List[str]]) -> str:
    """
    Format a human-readable validation report.

    Args:
        cards: List of card dicts
        errors: Dict from validate_cards()

    Returns:
        Formatted report string
    """
    if not errors:
        return f"✓ All {len(cards)} cards passed validation"

    lines = [f"✗ {len(errors)}/{len(cards)} cards failed validation:\n"]

    for idx, card_errors in errors.items():
        card = cards[idx]
        front_preview = card.get('front', '')[:50] + '...' if len(card.get('front', '')) > 50 else card.get('front', '')
        lines.append(f"Card {idx + 1}: {front_preview}")
        for error in card_errors:
            lines.append(f"  - {error}")
        lines.append("")

    return '\n'.join(lines)


# Quick test
if __name__ == "__main__":
    # Test valid card
    valid_errors = validate_card(
        front="[Paper A - Pharmacology] What is the mechanism of action of clozapine?",
        back="D2 antagonist with high 5-HT2A affinity",
        tags=["mrcpsych", "paper-a", "pharmacology"],
        deck="MRCPsych::Paper A::Pharmacology"
    )
    print(f"Valid card errors: {valid_errors}")

    # Test invalid card
    invalid_errors = validate_card(
        front="List all the side effects of lithium",
        back="This is a very long answer that goes on and on and on with many many words that exceed the twenty five word limit for primary answers on flashcards",
        tags=["pharmacology"],
        deck="Wrong Deck"
    )
    print(f"Invalid card errors: {invalid_errors}")
