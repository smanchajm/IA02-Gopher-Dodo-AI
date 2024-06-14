# Board Game AI Challenge: Dodo and Gopher AI

The aim of this project is to create artificial Gopher and Dodo players capable of playing in an AI competition. 
This project was carried out as part of the IA02 (Problem-Solving and Logic Programming) course at the Compiègne University of Technology (UTC).

These two games were created by Mark Steere.

## ToDo

- [ ] Implémentation du jeu 
  - [x] Grille
  - [x] Dodo rules
  - [x] Gopher rules
  - [x] Environnement
  - [x] Création des stratégies de jeu 
  - [ ] Serveur 
- [ ] différentes stratégies
  - [x] minmax simple
  - [x] alpha-beta simple
  - [x] fonction d'évaluation
  - [x] MCTS
  - [x] stratégie copie joueur adverse / librairie first moves
- [ ] optimisations
  - [ ] multithreading
  - [ ] symétries
  - [x] cache
  - [ ] profondeur adaptative ~
  - [x] voir si optimisation des structures (dico ?)
- [ ] mémoisation qui store l'action optimale pour une grille donnée 


**Cleaning, cleaning, cleaning** : black, pylint, mypy, isort, etc.
  


## Rules 
Both games are played on a hexagonal board. The implementation is freely inspired by *Red Blob Games [Implementation of hex Grid](https://www.redblobgames.com/grids/hexagons/).

* **[Dodo Rules](https://www.redblobgames.com/grids/hexagons/)**.
* **[Gopher Rules](https://www.marksteeregames.com/Dodo_rules.pdf)**.

## Contributors
* Paul Clément 
* Samuel Manchajm

## License
[MIT](https://choosealicense.com/licenses/mit/)
