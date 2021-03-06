# file-sql-to-data

## Prerequis
 * python
 * pip

## Install
 * `pip install -r requirements` (pour installer sqlparse, faker)

## Exemple
 * Creation de schema : `python ./main.py -sql ../sql-file/cuisine.sql`
 * Creation de schema avec schema preparee : `python ./main.py -sql ../sql-file/cuisine.sql -psch ./prepared-schema.json`
 * Creation de data : `python ./main.py -sch ./data-schema.json`
 * Creation de data avec schema generee et preparee: `python ./main.py -sch ./data-schema.json -psch ./prepared-schema.json`


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
 * Type classique
   * varchar
   * longtext
   * tinyint
   * boolean
   * int
 * Name
   * name
   * name_male
   * name_female
   * first_name_female
   * first_name
   * last_name
 * Personnal Data
   * job
   * credit_card_number
   * military_ship
   * catch_phrase_verb
   * company
 * Place
   * state
   * postalcode
   * zipcode
   * address
   * street_address
   * country
   * city
 * color
   * color
   * color_name
 * Time
   * year
   * month
   * month_name
   * day_of_week
   * time
   * am_pm
   * day_of_month
   * date
 * File
   * file_extension
   * file_name

## Note
 * Generer le requirements.txt automatiquement : pip freeze > requirements.txt
 * https://pythontips.com/2013/07/30/20-python-libraries-you-cant-live-without/
 * Documentation : http://sametmax.com/les-docstrings/

## Todo
 * documentation du fichier modules/Key.py
 * avec le prepared fichier si on met un order dedans ca risque de planter 
