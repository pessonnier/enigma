"""Small Enigma module extracted from the notebook."""

from __future__ import annotations

ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

ROT1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
ROT2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
ROT3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
ROT4 = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
ROT5 = list("VZBRGITYUPSDNHLXAWMJQOFECK")
ROT6 = list("JPGVOUMFYQBENHZRDKASXLICTW")
ROT7 = list("NZJHGRCXMYSWBOUFAIVLPEKQDT")
ROT8 = list("FKQHTLXOCBJSPDZRAMEWNIUYGV")
BETA = list("LEYJVCNIXWPBQMDRTAKZGFUHOS")
GAMMA = list("FSOKANUERHMBTIYCWLQPZXVGJD")

ROTORS = {
    "I": (ROT1, ["Q"]),
    "II": (ROT2, ["E"]),
    "III": (ROT3, ["V"]),
    "IV": (ROT4, ["J"]),
    "V": (ROT5, ["Z"]),
    "VI": (ROT6, ["Z", "M"]),
    "VII": (ROT7, ["Z", "M"]),
    "VIII": (ROT8, ["Z", "M"]),
    "beta": (BETA, ["Z", "M"]),
    "gamma": (GAMMA, ["Z", "M"]),
}

REFLECTOR_A = list("EJMZALYXVBWFCRQUONTSPIKHGD")

# Plugboard mapping used by the notebook.
_PLUGBOARD_LEFT = list("ADHJLX")
_PLUGBOARD_RIGHT = list("VEOKSQ")
PLUGBOARD = dict(
    zip(_PLUGBOARD_LEFT + _PLUGBOARD_RIGHT, _PLUGBOARD_RIGHT + _PLUGBOARD_LEFT)
)


def cable(letter: str) -> str:
    """Apply plugboard substitution for a single character."""

    return PLUGBOARD.get(letter, letter)


def enigma(
    message: str,
    choice_rotors: tuple[str, str, str] = ("I", "II", "III"),
    ring_position: str = "AAA",
    rotor_position: str = "AAA",
    reflector: list[str] = REFLECTOR_A,
) -> str:
    """Encode message characters using the notebook's Enigma wiring model."""

    positions = [
        ALPHABET.index(ring) + ALPHABET.index(rotor)
        for ring, rotor in zip(ring_position, rotor_position)
    ]
    (rotor1, notch1) = ROTORS[choice_rotors[0]]
    (rotor2, notch2) = ROTORS[choice_rotors[1]]
    (rotor3, _notch3) = ROTORS[choice_rotors[2]]

    output: list[str] = []
    for plain_char in message:
        c1 = cable(plain_char)

        c2 = rotor1[(ALPHABET.index(c1) + positions[0]) % 26]
        c3 = rotor2[(ALPHABET.index(c2) + positions[1]) % 26]
        c4 = rotor3[(ALPHABET.index(c3) + positions[2]) % 26]

        c5 = reflector[ALPHABET.index(c4)]

        c6 = ALPHABET[(rotor3.index(c5) - positions[2]) % 26]
        c7 = ALPHABET[(rotor2.index(c6) - positions[1]) % 26]
        c8 = ALPHABET[(rotor1.index(c7) - positions[0]) % 26]

        output.append(cable(c8))

        positions[0] = (positions[0] + 1) % 26
        if ALPHABET[positions[0]] in notch1:
            positions[1] = (positions[1] + 1) % 26
            if ALPHABET[positions[1]] in notch2:
                positions[2] = (positions[2] + 1) % 26

    return "".join(output)
