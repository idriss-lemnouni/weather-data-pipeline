# Pipeline météo et qualité de l’air

Ingestion de 153 observations quotidiennes réelles à New York, de mai à septembre 1973. Le pipeline construit une date ISO, convertit le vent en m/s et la température en °C, conserve les valeurs manquantes sous forme de NULL et rejette les dates dupliquées.

## Source et exécution

La [documentation du jeu airquality de R](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/airquality.html) indique les unités et la provenance des mesures. Le [CSV provient de Rdatasets](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/airquality.csv).

Télécharger le CSV lié ci-dessus sous le nom airquality.csv, dans le même dossier que pipeline.py. Exécuter ensuite `python pipeline.py` avec Python 3. Le script produit `observations.sqlite` et `quality.json`. Relancer le script remplace les observations en une transaction et conserve 153 lignes.

Le jeu couvre une seule période historique et associe des observations de qualité de l’air et de météo recueillies à des endroits différents de la région new-yorkaise.

