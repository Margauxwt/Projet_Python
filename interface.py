# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:31:15 2022

@author: marga
"""
from TPs import main
import praw
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


# Identification
reddit = praw.Reddit(client_id='qfGg1ZCyWvsU9etXwc1uzA', client_secret='qVMQes3UvGw0LL3rnaPsiFWcpdv-nA', user_agent='Projet Python', check_for_async=False)

app = QApplication([])

def clickme(self):
    # récupération du choix de subreddit
    value = comboBox.currentText()
    # appel à la fonction main 
    main(value, reddit, nbsubs, heure, frequence, graphique, postasucces, pourcentageup, pourcentagedown)

# Mise en place de la fenêtre avec sa taille et son nom
w = QMainWindow()
w.resize(800, 500)
w.setWindowTitle("Caractéristiques des top posts sur Reddit")

# Liste des 10 meilleurs subreddits 
list=[]
for subreddit in reddit.subreddits.popular(limit=10):
    list.append(subreddit.display_name)

label = QLabel("Veuillez sélectionner un subreddit",w)

# Liste déroulante
comboBox = QComboBox(w)
comboBox.addItems(list) 

# Bouton OK
pushButton = QPushButton("OK", w)
pushButton.clicked.connect(clickme)

# Zone de texte
nbsubs = QLabel("",w)
frequence = QLabel("",w)
heure = QLabel("",w)
postasucces = QLabel("",w)
pourcentageup = QLabel("",w)
pourcentagedown = QLabel("",w)

# Mise en place du graphique 
fig = Figure(figsize=(5, 4), dpi=100)
graphique = FigureCanvasQTAgg(fig)
graphique.axes = fig.add_subplot(111)
# On enlève les axes inutiles
graphique.axes.set_axis_off()

# Remplissage des zones de texte avec le contenu passé en paramètre
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(comboBox)
layout.addWidget(pushButton)
layout.addWidget(nbsubs)
layout.addWidget(heure)
layout.addWidget(pourcentageup)
layout.addWidget(pourcentagedown)
layout.addWidget(postasucces)
layout.addWidget(frequence)
layout.addWidget(graphique)

# ajout sur la page
widget = QWidget()
widget.setLayout(layout)
w.setCentralWidget(widget)

# affichage de la fenêtre
w.show()
app.exec_()