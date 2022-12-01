# Space-invadeur
Gabriel Paulet-Duprat Victor Maschio

https://github.com/GabrielPaulet/Space-invadeur

Dans ce space invaders nous pouvons nous déplacer grâce à 'q' et 'd' et tirer en même temps avec la touche 'espace'. Les enemies sont créer à partir d'un fichier de niveau et 
apparaisent à l'infini. Ceux-ci tirent aléatoirement à intervale régulier mais le joueur est protégé par des astéroïdes. Si un enemie descend trop bas le joueur perd la partie, de même si ses vies tombent
à zéro. Le score s'incrémente de 50 à chaque enemie tué.

Le bouton quitter ferme la fenêtre et le bouton nouvelle partie commence une nouvelle partie.

Notre space invadeurs est composé d'un fichier classe qui contient les classes l'éxecution de la majorité des éléments du programme tel que la fenetre principale,
les objets du canvas, ext. D'un fichier qui contient des fonction de lancement et de création d'objet et d'un fichier main à partir duquel on lance le projet.

After est une méthode récurssive multi-thread qui est utilisée dans nombreuse fontion tel que le tire, le déplacement enemie, le déplacement alliée, ect.
Il y à une implémentation d'une liste avec les déplacement des enemies ainsi que le chargement du niveau qui turne en boucle.


