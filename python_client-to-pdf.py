# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:36:06 2024

@author: ugona Adrien UGON <adrien.ugon@esiee.fr>
"""

#!/usr/bin/env python3

import requests
import json
from matplotlib import pyplot

from reportlab.lib import utils
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image
from reportlab.lib.styles import getSampleStyleSheet

# Paramètres de la requête HTTP
Id_Etudiant = 'all'
Code_Unite = "SEV-5106E"

uri = "https://www.gaalactic.fr/~ugona/ws/2024-2025/SEV-5106E/notes.py?Id_Etudiant={}&Code_Unite=SEV-5106E" . format(Id_Etudiant, Code_Unite)

# Exécution de la requête HTTP
httpReturn = requests.get(uri)
# Déserialization de la réponse HTTP
structuredHttpReturn = json.loads(httpReturn.text)
print(structuredHttpReturn)


if isinstance(structuredHttpReturn['data'], list):
    # Traitement du retour du web service pour une liste d'etudiant
    notes = {}
    for element in structuredHttpReturn['data']:
        cle = '{} {}' . format(element['Nom_Etudiant'], element['Prenom_Etudiant'])
        notes[cle] = element['Note']
else:
    #un seul étudiant
    notes = {}
    element = structuredHttpReturn['data']
    cle = '{} {}'.format(element['Nom_Etudiant'], element['Prenom_Etudiant'])
    notes[cle] = element['note']

# Construction de l'histogramme des notes avec matplotlib
image_filename = 'histogramme.png'

pyplot.figure(figsize=(20,10))
pyplot.bar(x=notes.keys(), height=notes.values(), color = 'blue')
pyplot.xlabel('Etudiants')
pyplot.ylabel('Note')
pyplot.title("Notes obtenues à l'unté {}" . format(Code_Unite))
pyplot.savefig(image_filename)
pyplot.close()


# Création d'un objet PDF
doc = SimpleDocTemplate("Rapport.pdf", pagesize=A4)

# setting the title of the document 
doc.title = "Rapport sur l'unité {}" . format(Code_Unite)

# Liste des éléments à ajouter au rapport PDF
pdf_elements = []

# Ajout du logo ESIEE Paris au PDF
logo_filename = "ESIEE_Paris_RVB.jpg"
img = utils.ImageReader(logo_filename)
img_width, img_height = img.getSize()
ratio_img = img_height / float(img_width)
logo = Image(logo_filename, width=200, height=200*ratio_img)
pdf_elements.append(logo)
  
# Ajout des titres au PDF
title = "Rapport sur l'unité {}" . format(Code_Unite)
subTitle = element['Libelle_Unite']

styles = getSampleStyleSheet()
pdf_elements.append(Paragraph(title, styles['Heading1']))
pdf_elements.append(Paragraph(subTitle, styles['Heading2']))
pdf_elements.append(Paragraph("Tableau des notes obtenues par tous les étudiants", styles['Heading3']))

# Ajout du tableau de notes au PDF
tableau_notes = []
for etudiant in notes: 
    note = notes[etudiant]
    tableau_notes.append([etudiant, note])
t =Table(tableau_notes)
pdf_elements.append(t)
 
# Ajout de l'histogramme au PDF
image = Image(image_filename, width=200*mm,height=100*mm)
pdf_elements.append(image)
  
# Sauvegarde du PDF
doc.build(pdf_elements)
