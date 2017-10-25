##### ACCÉDER À UN ENDROIT PRÉCIS d’un fichier

try:
	with open('fichier.txt', 'r') as fic:
		fic.seek(6)
		print(fic.read(4))
		fic.seek(21)
		print(fic.read(5))
	except FileNotFoundError as e:
		print('Le fichier {} n\'existe pas !'.format(e.filename))
		exit(1)
	# gestions des autres exceptions

##### LIRE UN FICHIER TEXTE ligne à ligne

try:
	with open('fichier.txt', 'r') as fic:
		for line in fic:
			print(line, end='')
	except FileNotFoundError as e:
		print('Le fichier {} n\'existe pas !'.format(e.filename))
		exit(1)
	except PermissionError as e:
		print('Droit de lecture absent sur le fichier {} !'.format(e.filename))
		exit(2)
	except Exception as e:
		print('Une erreur a empêché l\'ouverture du fichier : {}'.format(e.strerror))
		exit(3)


##### CREER UN FICHIER XML

from lxml import etree

root = etree.Element('series')

serie = etree.SubElement(root, 'nom')
serie.set('lang', 'fr')
serie.set('titre', 'Docteur_who')

personnages = ['Docteur Who', 'Rose Tyler', 'Mickey Smith']

for perso in personnages:
	personnage = etree.SubElement(serie, 'personnage')
	personnage.text = perso

try:
	with open('series.xml', 'w') as fic:
		fic.write(etree.tostring(root, pretty_print=True).decode('utf-8'))
except IOError:
	print('Problème rencontré lors de l\'écriture...')
	exit(1)

##### CRÉER UN FICHIER json

import json

data = {
	'series': {
		'Docteur Who': {
			'personnages': [
				'Docteur Who',
				'Rose Tyler',
				'Mickey Smith'
			]
		}
	}
}

try:
	with open('series.json', 'w') as fic:
		fic.write(json.dumps(data, indent=4))
except:
	print('Erreur lors de la création du fichier')
	exit(1)

##### LIRE UN FICHIER json

try:
	with open('series.json', 'r') as fic:
		series = json.load(fic)
	except:
		print('Erreur lors de la lecture du fichier')
		exit(1)

print(series)

##### CRÉER UN FICHIER ini

import configparser

config = configparser.ConfigParser()
config['personnages'] = {'chapeau_melon': 'John Steed, Emma Peel', 'amicalement_votre': 'Brett Sinclair, Danny Wilde'}
config['saisons'] = {'chapeau_Melon': 6, 'amicalement_votre': 1}

with open('series.ini', 'w') as fic:
	config.write(fic)