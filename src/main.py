# -*- coding: utf-8 -*-
#!/usr/bin/python

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
parser.add_argument('-y','--yes', help = 'permit to ignore the json verification and use default value')
args = parser.parse_args()

class DataGenerator:
	def __init__(self, inputFile = None, jsonFile = None, type = 'csv'):
		self.inputFile = inputFile
		self.jsonFile = jsonFile
		self.request = ''
		self.createRequest = {}
		self.dataSchema = {}
		self.data = {}

	def launch(self):
		if (self.jsonFile):
			self.dataSchema = self.readJsonFile(self.jsonFile)
			self.data = self.generateDatas(self.dataSchema)
			# self.generateJsonFile('data.json', self.data)
			return self.data
		elif (self.inputFile):
			self.request = self.readFileSql(self.inputFile)
			self.dataSchema = self.extractCreateRequests(self.request)
			return self.dataSchema
			if (not self.dataSchema):
				print ('fichier impossible a parser, verifier qu\'il sagit bien d\'un fichier sql en entree')
			# else:
				# self.generateJsonFile(self.outputFile, self.dataSchema)

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
		tablePattern = r'CREATE TABLE ([a-z]+) \((.+)\).*;'
		tableMatch = re.findall(tablePattern, request)
		for table in tableMatch:
			tableName = table[0]
			tableRequest = table[1]
			data[tableName] = {}
			data[tableName]['columns'] = {}
			data[tableName]['numberToCreate'] = 10
			columnMatch = tableRequest.split(",")
			data[tableName]['columns'] = self.extractColumnsFromCreateRequest(columnMatch)
		return data

	def extractColumnsFromCreateRequest(self, columnTable):
		columnPattern = r'(\S+) ([^ (]+)(?: ?\(([^)]+)\))? ?(.+)?'
		columnData = {}
		for column in columnTable:
			match = re.findall(columnPattern, column)
			if match:
				columName = match[0][0]
				columnData[columName] = {} if (not columnData.has_key(columName)) else columnData[columName]
				if (columName.lower().strip().find('primary') != -1):
					del columnData[columName]
					patternPrimaryKey = r'PRIMARY KEY ?\((.+)\)'
					matchPrimaryColumn = re.findall(patternPrimaryKey, column)
					if(len(matchPrimaryColumn) > 0):
						primaryKeys = matchPrimaryColumn[0].split(",")
						for key in primaryKeys:
							# print(key)
							if (not columnData.has_key(key)):
								columnData[key] = {}
							columnData[key]['primary'] = True
				elif (columName.lower().strip().find('index') != -1):
					del columnData[columName]
					pass
					# todo
				elif (columName.lower().strip().find('unique') != -1):
					# todo
					del columnData[columName]
					pass
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
		data = {}
		for tableName in dataSchema:
			data[tableName] = []
			numberOfRow = dataSchema[tableName]['numberToCreate']
			for i in range(numberOfRow):
				data[tableName].append(self.generateNewRow(dataSchema[tableName]['columns'], numberOfRow, id = i))
		return data

	def generateNewRow(self, columns, numberOfRow, id):
		newRow = {}
		for column in columns:
			newRow[column] = self.generateDataColumn(columns[column], numberOfRow, id = id )
		return newRow

	def generateDataColumn(self, column, numberOfRow, id):
		generatedData = None
		if (column['name'] == 'id'):
			generatedData = id+1
		else:
			if (column.has_key('type')):
				if column['type'].strip().lower() == 'varchar':
					generatedData = fake.sentence()
				elif column['type'].strip().lower().find('varchar') != -1:
					generatedData = fake.sentence()
				elif column['type'].strip().lower() == 'LONGTEXT'.lower():
					generatedData = fake.paragraph()
				elif column['type'].strip().lower() == 'tinyint':
					generatedData = fake.boolean()
				elif column['type'].strip().lower().find('tinyint') != -1:
					generatedData = fake.boolean()
				elif column['type'].strip().lower() == 'int':
					generatedData = random.randint(1, numberOfRow)
				elif column['type'].strip().lower().find('int') != -1:
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
				else:
					generatedData = None
		return generatedData

class FileCreator:
	def __init__(self, outputFile = None, extension = 'json', data = {}, dataType = None):
		self.extensionFile = extension
		self.data = data
		if (not outputFile):
			if (not dataType):
				self.outputFile = 'default-output-file.txt'
			else:
				self.outputFile = 'default-output-file.' + dataType
		else:
			self.outputFile = outputFile
		self.launch()

	def launch(self):
		self.chooseFormat(self.extensionFile)

	def chooseFormat(self, extension = None):
		if (extension == 'csv'):
			pass
		else:
			self.generateJsonFile(self.data, self.outputFile)

	def generateJsonFile(self, data, outputFile):
		try:
			with open(outputFile, 'w') as file:
				file.write(json.dumps(data, indent=2))
		except Exception as e:
			print('Erreur lors de la creation du fichier')
			print(e)
			exit(1)

if __name__ == '__main__':
	if (args.jsonFile):
		outputFile = args.outputFile if args.outputFile else './data.json'
		launcher = DataGenerator(jsonFile = args.jsonFile)
		data = launcher.launch()
		maker = FileCreator(data = data, outputFile = outputFile)
	elif (args.inputFile):
		outputFile = args.outputFile if args.outputFile else './data-schema.json'
		launcher = DataGenerator(inputFile = args.inputFile)
		dataSchema = launcher.launch()
		maker = FileCreator(data = dataSchema, outputFile = outputFile)
	else:
		parser.print_help()



def reflexion():
	'''
		referenciel, foreign key, unique

		unique:
			del si un unique ou si la primary key ne correspond pas

			recup unique et primary key
			si unique recup un tableau [colonneQuiDoitEtreUnique, row]

		referentiel:
			type: 
				ref
			data: fichier

		foreign key 1toN:
			type: foreign key, 1toN
			foreign-key: [table, colonne]

		foreign key NtoN:
			type: foreign key NtoN:
			foreign key: et la .... c'est le drame
	'''
	pass