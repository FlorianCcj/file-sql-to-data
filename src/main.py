# -*- coding: utf-8 -*-
#!/usr/bin/python

# extraction du schema
# mis dans l'ordre pour creation
# generation des data

import re
import json
import argparse
import random
from lxml import etree
from faker import Faker
fake = Faker()

import sys
sys.path.append('./modules/')
from ArrayToFile import * 
import FileReader
import FileCreator
from SchemaExtractorFromSqlFile import * 
from FromSchemaToData import * 
import tools

parser = argparse.ArgumentParser()
parser.add_argument('-if','--inputFile', help = 'SQL file schema to generate data')
parser.add_argument('-of','--outputFile', help = 'json file which resume the schema')
parser.add_argument('-jf','--jsonFile', help = 'json file which resume the schema to generate data')
parser.add_argument('-y','--yes', help = 'permit to ignore the json verification and use default value')
args = parser.parse_args()

class Test:
	def __init__(self):
		self.request = ''
		self.inputFile = '../sql-file/cuisine.sql'
		self.schemaExtractor = SchemaExtractor()
		self.dataGenerator = DataGenerator()
		self.launcher()

	def launcher(self):
		self.request = FileReader.readFileSql(self.inputFile)
		self.schemaExtractor.autoExtract(self.request)
		self.dataGenerator.launcher(self.schemaExtractor.columnsDataByTable, self.schemaExtractor)
		formatedData = tools.fromDataToObjectToPrint(self.dataGenerator.data)
		FileCreator.generateJsonFile(self.schemaExtractor.columnsDataByTable, './data-schema.json')
		FileCreator.generateJsonFile(self.dataGenerator.schema_to_work, './data-schema-to-work.json')
		FileCreator.generateTxtFileFromObject(formatedData, './data.json')
		# ordonnancer
		# ajouter le nombre de data a creer
		# ajouter les referentiels dans la DB
		# creer les fichier

Test()

if __name__ == '__main__':
	#if (args.jsonFile):
	#	outputFile = args.outputFile if args.outputFile else './data.json'
	#	launcher = DataGenerator(jsonFile = args.jsonFile)
	#	data = launcher.launch()
	#	maker = FileCreator(data = data, outputFile = outputFile)
	#elif (args.inputFile):
	#	outputFile = args.outputFile if args.outputFile else './data-schema.json'
	#	launcher = DataGenerator(inputFile = args.inputFile)
	#	dataSchema = launcher.launch()
	#	maker = FileCreator(data = dataSchema, outputFile = outputFile)
	#else:
	#	parser.print_help()
	pass
