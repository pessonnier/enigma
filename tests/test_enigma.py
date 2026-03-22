from enigma import enigma


def test_enigma_single_character_with_deterministic_defaults():
    """Matches the deterministic single-letter notebook example."""

    assert enigma("A") == "W"
