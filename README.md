Modélisation thermo-hydraulique d’un échangeur tubulaire

Description du projet

Ce projet présente le développement progressif d’un modèle thermo-hydraulique d’un échangeur tubulaire contre-courant sous Python.

L’objectif est de coupler les phénomènes thermiques et hydrauliques afin d’étudier les performances énergétiques de l’échangeur et leurs dépendances aux conditions d’écoulement.

Le projet repose sur :

- une discrétisation 1D de l’échangeur ;
- un solveur matriciel couplé ;
- une modélisation des pertes de charge ;
- des corrélations convectives de type Dittus-Boelter ;
- une étude d’optimisation énergétique ;
- une prise en compte des propriétés thermophysiques variables ;
- une résolution non-linéaire itérative ;
- une analyse NTU / effectiveness.

Objectifs du projet

Ce projet vise à :

- développer un solveur thermo-hydraulique couplé ;
- analyser les performances thermiques d’un échangeur ;
- étudier l’influence du nombre de Reynolds ;
- mettre en évidence les compromis thermo-hydrauliques ;
- introduire une démarche d’optimisation énergétique ;
- construire un projet d’ingénierie réaliste et interprétable.

Méthodologie:
Le projet a été développé en plusieurs phases :

Phase 1 — Modélisation thermique
discrétisation spatiale ;
résolution des profils de température ;
validation énergétique.

Phase 2 — Modélisation hydraulique
calcul des pertes de charge ;
calcul de la puissance de pompage ;
introduction du nombre de Reynolds.

Phase 3 — Couplage thermo-hydraulique
calcul des coefficients convectifs ;
calcul du coefficient global d’échange ;
développement du solveur matriciel couplé.

Phase 4 — Optimisation énergétique
étude paramétrique en débit ;
évolution de U ;
évolution des pertes de charge ;
compromis thermo-hydraulique ;
identification d’un point de fonctionnement optimal.

Phase 5 — Modèle avancé
propriétés thermophysiques variables ;
solveur non-linéaire ;
méthode de Picard ;
analyse NTU/effectiveness.
Résultats principaux

Les simulations mettent en évidence :

- l’influence majeure du nombre de Reynolds sur les échanges convectifs ;
- l’augmentation des performances thermiques avec le débit ;
- l’augmentation rapide des pertes de charge ;
- l’existence d’un compromis thermo-hydraulique ;
- l’impact des propriétés variables sur les coefficients d’échange.

Le solveur non-linéaire converge en quelques itérations, traduisant un couplage non-linéaire modéré.

Exemple de résultats
Profil de température

Ajouter ici une figure du profil de température.

![Profil température](docs/figures/profil_temperature.png)

Coefficient global d’échange
![U vs Re](docs/figures/U_vs_Re.png)

Compromis thermo-hydraulique
![U vs Ppompe](docs/figures/U_vs_Ppompe.png)

Lancer le projet
Installation
pip install -r requirements.txt

Exécution du solveur principal
python src/thermo_hydraulic_solver.py

Étude d’optimisation
python src/optimization_study.py

Solveur non-linéaire
python src/nonlinear_solver.py


Compétences mobilisées:
-Thermique industrielle
-Mécanique des fluides
-Échangeurs thermiques
-Analyse énergétique
-Résolution numérique
-Méthodes matricielles
-Python scientifique
-Modélisation thermo-hydraulique

Perspectives d’amélioration:
-prise en compte de géométries multitubulaires ;
-propriétés thermophysiques avancées ;
-corrélations turbulentes plus complexes ;
-optimisation multi-objectifs ;
-validation expérimentale ;
-comparaison avec des outils CFD.

Auteur:

Francis Uribe Casilimas



