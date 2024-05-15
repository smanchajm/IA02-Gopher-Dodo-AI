## Algorithmes 
* alpha-beta pruning with functiun evaluation
* MonteCarlo

## Optimisations
* Multithreading
* tricher en ayant une base de best move au début pour gagner en complexité (à l'image d'une ouverture aux échecs)
* développer  une fonction d'évaluation --> exemples:
  * Nombre de mouvements disponibles : Un joueur ayant plus de mouvements disponibles pourrait être en meilleure position.
  * Position des pièces : La position des pièces sur le plateau peut indiquer la force relative des joueurs.
  * Proximité de la victoire : Évaluer la distance des pièces des joueurs à la condition de victoire (avoir aucun mouvement disponible).
  * Blocage de l'adversaire : Évaluer dans quelle mesure les mouvements des pièces du joueur peuvent bloquer les mouvements de l'adversaire.
  * Contrôle du centre : Donner un avantage aux joueurs qui contrôlent le centre du plateau, car cela peut leur permettre de mieux se déplacer.
* les pondérations des critères pour la fonction d'évaluations peuvent êtres ajustés avec du reinforcement learning
* possible d'implémenter des méthode mixtes : en utilisant Alpha-Bêta pour les premiers coups lorsque le facteur de branchement est élevé, puis en passant à MCTS pour des recherches plus profondes lorsque le temps le permet
* Gestion des symétries
* Gestion du câche (mémoïsation)

  ## heuristiques :
  *  helpful heuristics to be found, for instance splitting your pieces is typically unfavourable.
  *  premier coup légal
  *  
