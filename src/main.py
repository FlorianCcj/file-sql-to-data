# -*- coding: utf-8 -*-
#!/usr/bin/python

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
parser.add_argument('-sf','--sqlFile', help = 'SQL file schema to generate data')
parser.add_argument('-of','--outputFile', help = 'json file which resume the schema')
parser.add_argument('-schf','--schemaFile', help = 'json file which resume the schema to generate data')
parser.add_argument('-y','--yes', help = 'permit to ignore the json verification and use default value', action='store_true')
args = parser.parse_args()

class App:
	def __init__(self):
		self.request = ''
		self.inputFile = '../sql-file/cuisine.sql'
		self.schemaExtractor = SchemaExtractor()
		self.dataGenerator = DataGenerator()

	def fromSqlFileToSchema(self, sqlFile, outputFile):
		self.request = FileReader.readFileSql(self.inputFile)
		#self.schemaExtractor.autoExtract(self.request)
		self.schemaExtractor.autoExtractWithSqlParse(self.request)
		self.dataGenerator.completeSchema(self.schemaExtractor.columnsDataByTable, self.schemaExtractor)
		FileCreator.generateJsonFile(self.dataGenerator.schema_to_work, outputFile)

	def fromSchemaToData(self, schemaFile, outputFile):
		schema = FileReader.readJsonFile(schemaFile)
		orderOfTable = self.dataGenerator.fromSchemaToOrder(schema)
		self.dataGenerator.generateDatas(schema, self.schemaExtractor)
		# todo : je balance la data mais pas l'ordre
		formatedData = tools.fromDataToOrderedObjectToPrint(self.dataGenerator.data, orderOfTable)
		FileCreator.generateTxtFileFromObject(formatedData, outputFile)

# referenciel

print(args)
if __name__ == '__main__':
	launcher = App()
	if (args.schemaFile):
		outputFile = args.outputFile if args.outputFile else './data.sql'
		launcher.fromSchemaToData(args.schemaFile, outputFile)
	elif (args.sqlFile):
		if args.yes:
			outputFile = './data-schema.json'
			launcher.fromSqlFileToSchema(args.sqlFile, outputFile)
			dataFile = args.outputFile if args.outputFile else './data.sql'
			launcher.fromSchemaToData(outputFile, dataFile)
		else:
			outputFile = (args.outputFile if args.outputFile else './data-schema.json')
			launcher.fromSqlFileToSchema(args.sqlFile, outputFile)
	else:
		parser.print_help()
	