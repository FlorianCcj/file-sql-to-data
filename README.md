# file-sql-to-data

## Prerequis
 * python
 * pip

## Install
 * `pip install -r requirements`

## Exemple
 * Creation de schema : `python ./main.py -if '../sql-file/cuisine.sql'`
 * Creation de data : `python ./main.py -jf './data-schema.json'`


## Utilisation général
Cette application permet a partir d'un fichier SQL de generer de la donnee.
  * Premiere etape : generer un schema correspondant a la base
  	`python ./main.py -if '{{chemin/vers/le/fichier/sql/fichier.sql}}'`
  	va generer un resumer de votre base avec le type, la taille, le nom des colonnes, etc
  	ceci va vous permettre de modifier la generation,
  	* numberToCreate : nombre de donnée qui va etre généré
  	* type : permet de choisir des type particulier
  * Deuxieme etape : generer de la donnee a partir du json modifié
  	`python ./main.py -jf '{{chemin/vers/le/fichier/json/fichier.json}}'`
  	va genener la data

### type suporter

	* 'varchar', 
	* 'longtext', 
	* 'boolean', 
	* 'tinyint', 
	* 'int', 
	* 'name', 
	* 'first_name', 
	* 'last_name',
	* 'adress', 
	* 'credit_card_number', 
	* 'military_ship', 
	* 'catch_phrase_verb', 
	* 'company',
	* 'color',

## Note
 * Generer le requirements.txt automatiquement : pip freeze > requirements.txt
 * https://pythontips.com/2013/07/30/20-python-libraries-you-cant-live-without/