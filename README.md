# enigma

Implémentation d'une simulation **Enigma M3** en Python, à partir des éléments de configuration présents dans le notebook.

## Fonctionnalités implémentées

- Rotors historiques `I` à `VIII` + `beta`, `gamma`
- Réflecteurs `A`, `B`, `C`, `Bthin`, `Cthin`
- Plugboard (câblage) bidirectionnel
- Réglages de bague (`ring_position`)
- Position initiale des rotors (`rotor_position`)
- Mécanisme de rotation des rotors avec **double-step**
- Interface simple via la fonction `enigma(...)`

## Utilisation

```python
from enigma import enigma

cipher = enigma(
    message="HELLOWORLD",
    choix_rotor=("I", "IV", "III"),
    ring_position="AZE",
    rotor_position="QSD",
    reflecteur="B",
    cablage={"A": "V", "D": "E", "H": "O", "J": "K", "L": "S", "X": "Q"},
)
print(cipher)
```

## Propriété de symétrie

Avec la **même configuration** et la même position initiale, chiffrer deux fois redonne le texte original.
