#!/usr/bin/env python3
"""
Setup script to create the MRCPsych deck structure in Anki.

Run this once to initialize all required decks:
    python3 scripts/setup_anki_decks.py
"""

from anki_connect import AnkiConnect, AnkiConnectError

DECK_STRUCTURE = [
    "MRCPsych",
    "MRCPsych::Paper A",
    "MRCPsych::Paper A::Neuroscience",
    "MRCPsych::Paper A::Psychology",
    "MRCPsych::Paper A::Pharmacology",
    "MRCPsych::Paper A::Genetics",
    "MRCPsych::Paper B",
    "MRCPsych::Paper B::General Adult",
    "MRCPsych::Paper B::Old Age",
    "MRCPsych::Paper B::Child & Adolescent",
    "MRCPsych::Paper B::Psychotherapy",
    "MRCPsych::Paper B::Critical Review",
    "MRCPsych::Paper B::Service Organization",
]


def setup_decks():
    """Create all MRCPsych decks in Anki."""
    print("Setting up MRCPsych deck structure in Anki...")
    print("-" * 50)

    try:
        anki = AnkiConnect()

        if not anki.is_connected():
            print("\nERROR: Cannot connect to Anki")
            print("\nPlease ensure:")
            print("  1. Anki is running")
            print("  2. AnkiConnect add-on is installed (code: 2055492159)")
            print("  3. AnkiConnect is listening on localhost:8765")
            return False

        print("Connected to AnkiConnect")

        existing_decks = anki.get_decks()
        created = 0
        skipped = 0

        for deck in DECK_STRUCTURE:
            if deck in existing_decks:
                print(f"  [exists] {deck}")
                skipped += 1
            else:
                anki.create_deck(deck)
                print(f"  [created] {deck}")
                created += 1

        print("-" * 50)
        print(f"Setup complete: {created} decks created, {skipped} already existed")

        # Verify note types
        print("\nAvailable note types:")
        for model in anki.get_model_names():
            print(f"  - {model}")

        print("\nSetup complete! You can now use /flashcard to create cards.")
        return True

    except AnkiConnectError as e:
        print(f"\nERROR: {e}")
        return False


def add_sample_cards():
    """Add sample cards to verify setup works."""
    print("\nAdding sample cards to verify setup...")

    try:
        anki = AnkiConnect()

        # Sample Basic card
        note_id = anki.add_note(
            deck_name="MRCPsych::Paper A::Pharmacology",
            front="[Paper A - Pharmacology] [SAMPLE] What class of drug is clozapine?",
            back="Atypical (second-generation) antipsychotic\n• D2/5-HT2A antagonist\n• Only drug licensed for treatment-resistant schizophrenia",
            tags=["mrcpsych", "paper-a", "pharmacology", "sample", "clozapine"]
        )
        print(f"  Created sample Basic card: {note_id}")

        # Sample Cloze card
        note_id = anki.add_cloze_note(
            deck_name="MRCPsych::Paper A::Pharmacology",
            text="[SAMPLE] Clozapine requires {{c1::weekly}} blood monitoring for the first {{c2::18 weeks}} due to risk of {{c3::agranulocytosis}}",
            extra="Risk highest in first 6 months. ANC must be >1500/mm³ to continue.",
            tags=["mrcpsych", "paper-a", "pharmacology", "sample", "clozapine"]
        )
        print(f"  Created sample Cloze card: {note_id}")

        print("\nSample cards created! Check Anki to verify.")
        print("(You can delete cards tagged 'sample' after verification)")
        return True

    except AnkiConnectError as e:
        print(f"\nERROR creating sample cards: {e}")
        return False


if __name__ == "__main__":
    import sys

    success = setup_decks()

    if success and "--with-samples" in sys.argv:
        add_sample_cards()

    sys.exit(0 if success else 1)
