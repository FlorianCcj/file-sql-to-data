# file-sql-to-data

## Prerequis
 * python
 * pip

## Install
 * `pip install -r requirements`

## Lancement
 * Creation de schema : `python ./main.py -if '../sql-file/cuisine.sql'`
 * Creation de data : `python ./main.py -jf './data-schema.json'`

## Note
 * Generer le requirements.txt automatiquement : pip freeze > requirements.txt
