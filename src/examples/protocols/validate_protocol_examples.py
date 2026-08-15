"""Validate the JSON examples used by the A2A and A2UI lessons."""

from __future__ import annotations

import json
from pathlib import Path


EXAMPLE_DIR = Path(__file__).parent


def validate_agent_card() -> None:
    card = json.loads((EXAMPLE_DIR / "a2a_agent_card.json").read_text(encoding="utf-8"))
    assert card["supportedInterfaces"][0]["protocolVersion"] == "1.0"
    assert card["securityRequirements"]
    assert card["skills"][0]["id"] == "check-disruption-care"


def validate_a2ui_stream() -> None:
    messages = [
        json.loads(line)
        for line in (EXAMPLE_DIR / "a2ui_passenger_options.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    assert [next(key for key in message if key != "version") for message in messages] == [
        "createSurface",
        "updateComponents",
        "updateDataModel",
    ]
    assert all(message["version"] == "v0.9.1" for message in messages)
    components = messages[1]["updateComponents"]["components"]
    assert any(component["id"] == "root" for component in components)


if __name__ == "__main__":
    validate_agent_card()
    validate_a2ui_stream()
    print("Protocol examples are valid JSON and pass their contract checks.")
