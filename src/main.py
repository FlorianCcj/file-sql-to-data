# -*- coding: utf-8 -*-
#!/usr/bin/python

# sudo pip install Faker

# actuellement lance via 
# `python ./main.py -if '../sql-file/film.sql'`
# `python ./main.py -jf './data-schema.json'`
import re
import json
import argparse
import random
from faker import Faker
fake = Faker()

# fake.seed(12) # avec une meme seed on a les meme valeur random
# fake.name()
# fake.adress()
# fake.first_name()
# fake.last_name()
# fake.text()
# fake.sentence()
# fake.credit_card_number()
# fake.military_ship()
# fake.hex_color()
# fake.catch_phrase_verb()
# fake.company()

parser = argparse.ArgumentParser()
parser.add_argument('-if','--inputFile', help = 'SQL file schema to generate data')
parser.add_argument('-of','--outputFile', help = 'json file which resume the schema')
parser.add_argument('-jf','--jsonFile', help = 'json file which resume the schema to generate data')
parser.add_argument('-y','--yes', help = 'permit to ignore the json verification and use deffault value')
args = parser.parse_args()

class DataGenerator:
	def __init__(self, inputFile = None, jsonFile = None, outputFile = None, type = 'csv'):
		self.inputFile = inputFile
		self.jsonFile = jsonFile
		self.outputFile = outputFile
		self.request = ''
		self.createRequest = {}
		self.dataSchema = {}
		self.data = {}

	def launch(self):
		if (self.jsonFile):
			self.dataSchema = self.readJsonFile(self.jsonFile)
			self.data = self.generateDatas(self.dataSchema)
			# print(self.dataSchema)
		elif (self.inputFile):
			self.request = self.readFileSql(self.inputFile)
			self.dataSchema = self.extractCreateRequests(self.request)
			if (not self.dataSchema):
				print ('fichier impossible a parser, verifier qu\'il sagit bien d\'un fichier sql en entree')
			else:
				self.generateJson(self.outputFile, self.dataSchema)
		# print(self.dataSchema)

	def readFileSql(self, inputFile):
		totalRequest = ''
		try:
			with open(inputFile, 'r') as file:
				for line in file:
					totalRequest += line 
					# WIP
					# print(line)
		except FileNotFoundError as e:
			print('Le fichier {} n\'existe pas !'.format(e.filename))
			exit(1)
		except PermissionError as e:
			print('Droit de lecture absent sur le fichier {} !'.format(e.filename))
			exit(2)
		except Exception as e:
			print('Une erreur a empêché l\'ouverture du fichier : {}'.format(e.strerror))
			exit(3)
		return totalRequest

	def readJsonFile(self, jsonFile):
		try:
			with open(jsonFile, 'r') as file:
				dataSchema = json.load(file)
		except Exception as e:
			print('Erreur lors de la lecture du fichier')
			print(e)
			exit(1)
		return dataSchema

	def extractCreateRequests(self, request):
		data = {}
		tablePattern = r'CREATE TABLE ([a-z]+) \((.+)\);'
		tableMatch = re.findall(tablePattern, request)
		for table in tableMatch:
			tableName = table[0]
			tableRequest = table[1]
			# self.dataSchema[tableName] = {}
			data[tableName] = {}
			# self.dataSchema[tableName]['columns'] = {}
			data[tableName]['columns'] = {}
			data[tableName]['numberToCreate'] = 10
			columnMatch = tableRequest.split(",")
			# self.dataSchema[tableName]['columns'] = self.extractColumns(columnMatch)
			data[tableName]['columns'] = self.extractColumns(columnMatch)
			# print(num, name)
		return data

	def extractColumns(self, columnTable):
		columnPattern = r'(\S+) (\S+) ?\(?(\d+)?\)? (.*)'
		columnData = {}
		for column in columnTable:
			match = re.findall(columnPattern, column)
			if match:
				columName = match[0][0]
				columnData[columName] = {} if (not columnData.has_key(columName)) else columnData[columName]
				if (columName.lower().strip().find('primary') != -1):
					patternPrimaryKey = r'primary key ?\((.+)\)'
					matchPrimaryColumn = re.findall(patternPrimaryKey, column.lower())
					primaryKeys = matchPrimaryColumn[0].split(",")
					for key in primaryKeys:
						if (not columnData.has_key(key)):
							columnData[key] = {}
						columnData[key]['primary'] = True
				else:
					columnType = match[0][1]
					columnData[columName]['name'] = columName
					columnData[columName]['type'] = columnType if columnType else None
					columnData[columName]['nullable'] = (column.lower().find('not null') != -1)
					try:
						columnData[columName]['size'] = int(match[0][2])
					except Exception as e:
						columnData[columName]['size'] = None
					
		return columnData

	def generateDatas(self, dataSchema):
		# print(dataSchema)
		data = {}
		for tableName in dataSchema:
			# pass
			data[tableName] = []
			numberOfRow = dataSchema[tableName]['numberToCreate']
			for i in range(numberOfRow):
				data[tableName].append(self.generateNewRow(dataSchema[tableName]['columns'], numberOfRow))
				# print(i)
			# print(dataSchema[tableName])
			# print('-----------------------')
		# print(dataSchema)

	def generateJson(self, outputFile, data):
		try:
			with open(outputFile, 'w') as file:
				file.write(json.dumps(data, indent=2))
		except Exception as e:
			print('Erreur lors de la creation du fichier')
			print(e)
			exit(1)

	def generateNewRow(self, columns, numberOfRow):
		newRow = {}
		for column in columns:
			# print column
			if (column.strip().lower().find('primary') == -1):
				newRow[column] = self.generateDataColumn(columns[column], numberOfRow)
		return newRow

	def generateDataColumn(self, column, numberOfRow):
		generatedData = None
		# print(column)
		if (column.has_key('type')):
			if column['type'].strip().lower() == 'varchar':
				generatedData = fake.sentence()
			elif column['type'].strip().lower() == 'int':
				generatedData = random.randint(1, numberOfRow)
			elif column['type'].strip().lower() == 'name':
				generatedData = fake.name()
			elif column['type'].strip().lower() == 'adress':
				generatedData = fake.adress()
			elif column['type'].strip().lower() == 'first_name':
				generatedData = fake.first_name()
			elif column['type'].strip().lower() == 'last_name':
				generatedData = fake.last_name()
			elif column['type'].strip().lower() == 'credit_card_number':
				generatedData = fake.credit_card_number()
			elif column['type'].strip().lower() == 'military_ship':
				generatedData = fake.military_ship()
			elif column['type'].strip().lower() == 'color':
				generatedData = fake.hex_color()
			elif column['type'].strip().lower() == 'catch_phrase_verb':
				generatedData = fake.catch_phrase_verb()
			elif column['type'].strip().lower() == 'company':
				generatedData = fake.company()
		return generatedData

if __name__ == '__main__':
	if (args.jsonFile):
		outputFile = args.outputFile if args.outputFile else './data-schema.json'
		launcher = DataGenerator(jsonFile = args.jsonFile, outputFile = outputFile)
		launcher.launch()
	elif (args.inputFile):
		outputFile = args.outputFile if args.outputFile else './data-schema.json'
		launcher = DataGenerator(inputFile = args.inputFile, outputFile = outputFile)
		launcher.launch()
	else:
		parser.print_help()
		# verifier qu'il existe
