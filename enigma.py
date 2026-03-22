"""Simulation simplifiée d'une machine Enigma M3.

Implémente:
- rotors historiques I à VIII (+ beta, gamma)
- réflecteurs A, B, C, Bthin, Cthin
- plugboard (câblage)
- position de bague (ring setting)
- position initiale des rotors
- mécanisme de rotation avec double-step
"""

from __future__ import annotations

from dataclasses import dataclass
from string import ascii_uppercase

ALPHABET = ascii_uppercase

ROTOR_SPECS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
    "VI": ("JPGVOUMFYQBENHZRDKASXLICTW", "ZM"),
    "VII": ("NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"),
    "VIII": ("FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"),
    "beta": ("LEYJVCNIXWPBQMDRTAKZGFUHOS", ""),
    "gamma": ("FSOKANUERHMBTIYCWLQPZXVGJD", ""),
}

REFLECTORS = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    "Bthin": "ENKQAUYWJICOPBLMDXZVFTHRGS",
    "Cthin": "RDOBJNTKVEHMLFCWZAXGYIPSUQ",
}


@dataclass
class Rotor:
    wiring: str
    notches: str
    position: int = 0
    ring_setting: int = 0

    def step(self) -> None:
        self.position = (self.position + 1) % 26

    def at_notch(self) -> bool:
        return ALPHABET[self.position] in self.notches

    def encode_forward(self, c: str) -> str:
        i = (ALPHABET.index(c) + self.position - self.ring_setting) % 26
        mapped = self.wiring[i]
        o = (ALPHABET.index(mapped) - self.position + self.ring_setting) % 26
        return ALPHABET[o]

    def encode_backward(self, c: str) -> str:
        i = (ALPHABET.index(c) + self.position - self.ring_setting) % 26
        mapped_index = self.wiring.index(ALPHABET[i])
        o = (mapped_index - self.position + self.ring_setting) % 26
        return ALPHABET[o]


class EnigmaMachine:
    def __init__(
        self,
        rotors: tuple[str, str, str] = ("I", "II", "III"),
        ring_position: str = "AAA",
        rotor_position: str = "AAA",
        reflector: str = "B",
        plugboard: dict[str, str] | None = None,
    ) -> None:
        if len(rotors) != 3:
            raise ValueError("Enigma M3 attend exactement 3 rotors")
        if len(ring_position) != 3 or len(rotor_position) != 3:
            raise ValueError("ring_position et rotor_position doivent avoir 3 lettres")

        self.rotors = [
            Rotor(
                ROTOR_SPECS[name][0],
                ROTOR_SPECS[name][1],
                position=ALPHABET.index(rotor_position[i].upper()),
                ring_setting=ALPHABET.index(ring_position[i].upper()),
            )
            for i, name in enumerate(rotors)
        ]

        try:
            self.reflector = REFLECTORS[reflector]
        except KeyError as exc:
            raise ValueError(f"Réflecteur inconnu: {reflector}") from exc

        self.plugboard = self._normalize_plugboard(plugboard or {})

    @staticmethod
    def _normalize_plugboard(pb: dict[str, str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for a, b in pb.items():
            a = a.upper()
            b = b.upper()
            if a == b:
                raise ValueError("Un câble plugboard doit connecter 2 lettres distinctes")
            if a in normalized or b in normalized:
                raise ValueError("Une lettre ne peut être câblée qu'une seule fois")
            normalized[a] = b
            normalized[b] = a
        return normalized

    def _plug(self, c: str) -> str:
        return self.plugboard.get(c, c)

    def _step_rotors(self) -> None:
        left, middle, right = self.rotors

        middle_should_step = right.at_notch() or middle.at_notch()
        left_should_step = middle.at_notch()

        right.step()
        if middle_should_step:
            middle.step()
        if left_should_step:
            left.step()

    def encode_char(self, c: str) -> str:
        if c not in ALPHABET:
            return c

        self._step_rotors()

        c = self._plug(c)

        right, middle, left = self.rotors[2], self.rotors[1], self.rotors[0]
        c = right.encode_forward(c)
        c = middle.encode_forward(c)
        c = left.encode_forward(c)

        c = self.reflector[ALPHABET.index(c)]

        c = left.encode_backward(c)
        c = middle.encode_backward(c)
        c = right.encode_backward(c)

        return self._plug(c)

    def encode(self, message: str) -> str:
        message = message.upper()
        return "".join(self.encode_char(c) for c in message)


def enigma(
    message: str,
    choix_rotor: tuple[str, str, str] = ("I", "II", "III"),
    ring_position: str = "AAA",
    rotor_position: str = "AAA",
    reflecteur: str = "B",
    cablage: dict[str, str] | None = None,
) -> str:
    machine = EnigmaMachine(
        rotors=choix_rotor,
        ring_position=ring_position,
        rotor_position=rotor_position,
        reflector=reflecteur,
        plugboard=cablage,
    )
    return machine.encode(message)
