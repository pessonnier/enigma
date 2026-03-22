# Enigma – Spécification fonctionnelle et technique

Ce projet vise à réaliser une simulation fidèle de la machine de chiffrement **Enigma** en Python. La spécification couvre les attentes fonctionnelles, les contraintes techniques et les règles de calcul associées aux rotors, au réflecteur, aux anneaux (ring settings), à la position initiale, au câblage d'entrée (plugboard) et au mécanisme d'avancement des rotors.
Implémentation d'une simulation **Enigma M3** en Python, à partir des éléments de configuration présents dans le notebook.

## Objectifs
- **Chiffrement et déchiffrement symétriques** : tout message chiffré avec une configuration donnée doit être déchiffrable en rejouant exactement la même configuration.
- **Fidélité historique** : supporter les rotors I à VIII ainsi que les réflecteurs A, B, C (et variantes fines B-thin, C-thin) et les rotors de l'Uhrwerk (beta, gamma) présents dans le notebook.
- **Configurer la machine par paramètres** : choix des rotors (ordre et orientation), réglage des notches, positions initiales, réglage des anneaux, câblage du plugboard et choix du réflecteur.
- **Traçabilité** : exposer les étapes intermédiaires du parcours d'une lettre (entrée → plugboard → rotors → réflecteur → retour) pour faciliter le débogage et la vérification.

## Périmètre fonctionnel
1. **Configuration**
   - Sélection de trois rotors parmi `I…VIII`, `beta`, `gamma` avec leurs notches respectifs.
   - Paramétrage des positions d'anneaux (`Ringstellung`) via trois lettres A–Z.
   - Paramétrage des positions initiales (`Grundstellung`) via trois lettres A–Z.
   - Choix du réflecteur parmi `A`, `B`, `C`, `B-thin`, `C-thin`.
   - Définition d'un plugboard (Steckerbrett) sous forme de paires de lettres (A–Z). Les lettres non renseignées sont laissées en passe‑plat.

2. **Chiffrement d'un message**
   - Parcours lettre par lettre, avec avancement des rotors entre chaque caractère selon le mécanisme de *double stepping*.
   - Validation et nettoyage d'entrée : accepter uniquement A–Z (ou convertir en majuscule et ignorer les caractères non alphabétiques si souhaité).
   - Retourner la sortie sous la même longueur que l'entrée après passage dans les rotors, le réflecteur, puis en sortie par le plugboard.

3. **Traçage optionnel**
   - Mode verbeux affichant, pour chaque lettre, la chaîne des transformations (exemple issu du notebook : `A -> A -> E -> ...`).
   - Informations sur l'état des rotors avant et après l'incrément.

## Contraintes et règles de calcul
- **Alphabets** : utiliser `ABCDEFGHIJKLMNOPQRSTUVWXYZ` comme alphabet de base.
- **Câblage des rotors** : utiliser les séquences déjà présentes dans `enigma.ipynb` (`rot1…rot8`, `beta`, `gamma`). Chaque rotor est modélisé par une permutation de l'alphabet et une ou plusieurs positions de notch.
- **Notches** : déclenchent l'avance du rotor suivant lorsque la lettre du rotor courant correspond à un notch (ex. rotor I : notch `Q`). Les rotors VI, VII, VIII ont deux notches (`Z` et `M`).
- **Ring setting** : décale le câblage interne du rotor avant application, via un offset appliqué sur l'index de la lettre. Le réglage s'applique dans les deux sens (aller et retour) et modifie la position des notches.
- **Position initiale** : définit l'offset dynamique pour le premier caractère. L'offset augmente pendant le chiffrement via le mécanisme de stepping.
- **Stepping** :
  - Le rotor rapide (droite) avance d'un cran à chaque lettre.
  - *Double stepping* : si le rotor rapide atteint son notch, le rotor médian avance ; si le rotor médian est sur son notch, il entraîne aussi le rotor lent.
- **Plugboard** : application d'un mapping symétrique avant l'entrée dans le premier rotor et après la sortie du dernier rotor.
- **Réflecteur** : permutation fixe et involutive ; renvoie le signal dans le sens inverse.

## Interface logicielle attendue
- Une fonction ou classe `EnigmaMachine` exposant :
  - `encrypt(message: str) -> str` (utilisable aussi pour déchiffrer).
  - Des attributs/paramètres d'initialisation pour les rotors, positions, anneaux, plugboard et réflecteur.
  - Une option `verbose` pour retourner ou afficher le tracé intermédiaire.
- Des helpers pour :
  - Charger les rotors et notches à partir des constantes du notebook.
  - Construire un plugboard à partir d'une liste de paires.
  - Valider les entrées et normaliser les lettres.

## Cas de test recommandés
- **Boucle identité** : chiffrer puis rechiffrer avec la même configuration doit renvoyer le message d'origine.
- **Cas unitaires rotors** : vérifier que chaque rotor est une permutation bijective de l'alphabet et que le décodage inverse fonctionne.
- **Stepping** : contrôler le double stepping sur des séquences déclenchant les notches (ex. positions `Q`, `E`, `V`).
- **Plugboard** : vérifier que chaque paire est inversible et qu'une lettre non câblée ressort inchangée.
- **Réflecteur** : s'assurer que chaque lettre est mappée de façon involutive.

## Architecture technique suggérée
- **Module des données** : tables de câblage (`rot1…rot8`, `beta`, `gamma`, réflecteurs, alphabet) isolées dans un fichier de constantes.
- **Module machine** : classe/fonction gérant l'état des rotors, le stepping et le parcours aller/retour.
- **Module utilitaires** : validation, normalisation, construction du plugboard.
- **Notebook de démonstration** : conserver `enigma.ipynb` pour illustrer les flux et expérimenter les formules avant intégration dans les modules Python.

## Livrables
- Code Python structuré selon l'architecture ci-dessus.
- Suite de tests automatisés couvrant les cas listés.
- Documentation succincte (exemples d'usage, options de configuration) dérivée de la présente spécification.

## Fonctionnalités implémentées à verifier

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