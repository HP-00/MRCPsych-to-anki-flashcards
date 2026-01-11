#!/usr/bin/env python3
"""
AnkiConnect API wrapper for MRCPsych flashcard automation.

Requires:
- Anki running with AnkiConnect add-on (code: 2055492159)
- AnkiConnect listening on localhost:8765

Usage:
    from anki_connect import AnkiConnect
    anki = AnkiConnect()
    anki.add_flashcard("What is X?", "Answer", deck="MRCPsych::Paper A")
"""

import json
import urllib.request
import urllib.error
import base64
from pathlib import Path
from typing import Optional


class AnkiConnectError(Exception):
    """Custom exception for AnkiConnect errors."""
    pass


class AnkiConnect:
    """Wrapper for AnkiConnect API operations."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.url = f"http://{host}:{port}"
        self.version = 6

    def _invoke(self, action: str, **params) -> any:
        """Make a request to AnkiConnect API."""
        request_data = {
            "action": action,
            "version": self.version,
            "params": params
        }

        try:
            request = urllib.request.Request(
                self.url,
                data=json.dumps(request_data).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            response = urllib.request.urlopen(request, timeout=30)
            result = json.loads(response.read().decode("utf-8"))

            if result.get("error"):
                raise AnkiConnectError(result["error"])

            return result.get("result")

        except urllib.error.URLError as e:
            raise AnkiConnectError(
                f"Cannot connect to Anki. Is Anki running with AnkiConnect? Error: {e}"
            )

    def is_connected(self) -> bool:
        """Check if AnkiConnect is available."""
        try:
            version = self._invoke("version")
            return version is not None
        except:
            return False

    def get_decks(self) -> list:
        """Get all deck names."""
        return self._invoke("deckNames")

    def create_deck(self, deck_name: str) -> int:
        """Create a new deck. Returns deck ID."""
        return self._invoke("createDeck", deck=deck_name)

    def ensure_deck_exists(self, deck_name: str) -> int:
        """Create deck if it doesn't exist."""
        decks = self.get_decks()
        if deck_name not in decks:
            return self.create_deck(deck_name)
        return None

    def get_model_names(self) -> list:
        """Get all note type (model) names."""
        return self._invoke("modelNames")

    def add_note(
        self,
        deck_name: str,
        front: str,
        back: str,
        model_name: str = "Basic",
        tags: Optional[list] = None,
        allow_duplicate: bool = False
    ) -> Optional[int]:
        """
        Add a single flashcard note.

        Args:
            deck_name: Target deck (e.g., "MRCPsych::Paper A::Neuroscience")
            front: Front side content (question)
            back: Back side content (answer)
            model_name: Note type ("Basic", "Cloze", "Basic (and reversed card)")
            tags: List of tags
            allow_duplicate: Whether to allow duplicate notes

        Returns:
            Note ID if successful, None if duplicate and not allowed
        """
        self.ensure_deck_exists(deck_name)

        # Determine field names based on model
        if model_name == "Cloze":
            fields = {"Text": front, "Extra": back}
        else:
            fields = {"Front": front, "Back": back}

        note = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields,
            "tags": tags or [],
            "options": {
                "allowDuplicate": allow_duplicate,
                "duplicateScope": "deck"
            }
        }

        return self._invoke("addNote", note=note)

    def add_notes(self, notes: list) -> list:
        """
        Add multiple notes at once.

        Args:
            notes: List of dicts with keys: deck_name, front, back,
                   and optional model_name, tags

        Returns:
            List of note IDs (None for failed notes)
        """
        anki_notes = []
        for note in notes:
            deck_name = note["deck_name"]
            self.ensure_deck_exists(deck_name)

            model_name = note.get("model_name", "Basic")
            if model_name == "Cloze":
                fields = {"Text": note["front"], "Extra": note.get("back", "")}
            else:
                fields = {"Front": note["front"], "Back": note["back"]}

            anki_notes.append({
                "deckName": deck_name,
                "modelName": model_name,
                "fields": fields,
                "tags": note.get("tags", []),
                "options": {
                    "allowDuplicate": note.get("allow_duplicate", False),
                    "duplicateScope": "deck"
                }
            })

        return self._invoke("addNotes", notes=anki_notes)

    def add_cloze_note(
        self,
        deck_name: str,
        text: str,
        extra: str = "",
        tags: Optional[list] = None
    ) -> Optional[int]:
        """
        Add a cloze deletion card.

        Args:
            deck_name: Target deck
            text: Cloze text with {{c1::answer}} format
            extra: Additional info shown on back
            tags: List of tags

        Returns:
            Note ID if successful
        """
        return self.add_note(
            deck_name=deck_name,
            front=text,
            back=extra,
            model_name="Cloze",
            tags=tags
        )

    def store_media(
        self,
        filename: str,
        data: Optional[bytes] = None,
        path: Optional[str] = None,
        url: Optional[str] = None
    ) -> str:
        """
        Store a media file in Anki's media folder.

        Args:
            filename: Target filename in media folder
            data: Raw bytes of file content
            path: Local file path
            url: URL to download from

        Returns:
            Stored filename
        """
        params = {"filename": filename, "deleteExisting": True}

        if data:
            params["data"] = base64.b64encode(data).decode("utf-8")
        elif path:
            params["path"] = str(Path(path).resolve())
        elif url:
            params["url"] = url
        else:
            raise ValueError("Must provide data, path, or url")

        return self._invoke("storeMediaFile", **params)

    def add_note_with_image(
        self,
        deck_name: str,
        front: str,
        back: str,
        image_path: str,
        tags: Optional[list] = None
    ) -> Optional[int]:
        """
        Add a note with an embedded image.

        Args:
            deck_name: Target deck
            front: Front side content (can include <img> tag)
            back: Back side content
            image_path: Path to image file
            tags: List of tags

        Returns:
            Note ID if successful
        """
        # Store the image
        image_path = Path(image_path)
        stored_name = self.store_media(
            filename=f"mrcpsych_{image_path.name}",
            path=str(image_path)
        )

        # Add image tag if not already in front
        if "<img" not in front:
            front = f'{front}<br><img src="{stored_name}">'

        return self.add_note(
            deck_name=deck_name,
            front=front,
            back=back,
            tags=tags
        )

    def find_notes(self, query: str) -> list:
        """
        Find notes matching a query.

        Args:
            query: Anki search query (e.g., "deck:MRCPsych tag:high-yield")

        Returns:
            List of note IDs
        """
        return self._invoke("findNotes", query=query)

    def sync(self) -> None:
        """Trigger Anki sync."""
        self._invoke("sync")

    def get_deck_stats(self, deck_name: str) -> dict:
        """Get statistics for a deck."""
        return self._invoke("getDeckStats", decks=[deck_name])


def test_connection():
    """Test AnkiConnect connection and print status."""
    anki = AnkiConnect()

    if anki.is_connected():
        print("Connected to AnkiConnect")
        print(f"Available decks: {anki.get_decks()}")
        print(f"Available note types: {anki.get_model_names()}")
        return True
    else:
        print("ERROR: Cannot connect to AnkiConnect")
        print("Make sure:")
        print("  1. Anki is running")
        print("  2. AnkiConnect add-on is installed (code: 2055492159)")
        print("  3. AnkiConnect is listening on localhost:8765")
        return False


if __name__ == "__main__":
    test_connection()
