# file-sql-to-data

## Prerequis
 * python
 * pip

## Install
 * `pip install -r requirements` (pour installer sqlparse, faker)

## Exemple
 * Creation de schema : `python ./main.py -sf ../sql-file/cuisine.sql`
 * Creation de data : `python ./main.py -sch ./data-schema.json`


## Utilisation général
Cette application permet a partir d'un fichier SQL de generer de la donnee.
  * Premiere etape : generer un schema correspondant a la base
  	`python ./main.py -sf '{{chemin/vers/le/fichier/sql/fichier.sql}}'`
  	va generer un resumer de votre base avec le type, la taille, le nom des colonnes, etc
  	ceci va vous permettre de modifier la generation,
  	* numberToCreate : nombre de donnée qui va etre généré
  	* type : permet de choisir des type particulier
  * Deuxieme etape : generer de la donnee a partir du json modifié
  	`python ./main.py -schf '{{chemin/vers/le/fichier/json/fichier.json}}'`
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
 * Documentation : http://sametmax.com/les-docstrings/

## Todo
 * documentation du fichier modules/Key.py
 * documentation du fichier modules/SchemaExtractorFromSqlFile.py
 * documentation du fichier modules/tools.py
 * ajout de cle a la place de string dans FileCreator
