# Skyscrapers Solver

Ce programme résout le jeu Skyscrapers de taille N. Le jeu Skyscrapers est un puzzle dans lequel le joueur doit placer des gratte-ciels de différentes hauteurs dans une grille de taille N de manière à respecter certaines contraintes visibles depuis les côtés de la grille.

## Installation

Assurez-vous d'avoir Python installé sur votre machine.

1. Clonez ce dépôt :
```git clone https://github.com/DinohRatiarisandy/Skyscrapers_Game_AI.git```

2. Accédez au répertoire du projet :
```cd skyscrapers-solver```

3. Exécutez le script principal :
```python main.py```

## Comment jouer
Le script principal (```main.py```) utilise deux classes principales : ```Game``` pour initialiser et afficher le jeu, et ```SolveBoard``` pour résoudre le jeu Skyscrapers.

### Classe Game
La classe Game initialise un jeu Skyscrapers avec des indices horizontaux et verticaux donnés. Elle affiche le plateau initial et la solution obtenue après résolution.

### Classe SolveBoard
La classe SolveBoard est responsable de la résolution du jeu Skyscrapers. Elle utilise une approche récursive pour explorer les différentes combinaisons possibles et sélectionne la meilleure solution qui respecte les règles du jeu.

### Fonctionnalités
Résolution automatique du jeu Skyscrapers de taille N avec des indices donnés.
Affichage du plateau initial et de la solution obtenue.

