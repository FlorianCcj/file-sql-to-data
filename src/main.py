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
		
		self.createRequest = {}
		self.request = ''
		
		self.dataSchema = {}
		self.data = {}
		self.tableNameGeneratedData = []

		self.unique = {}
		self.uniqueDatas = {}
		self.primaryColumn = {}
		
		self.timeout = 50

	def launch(self):
		print('### Lancement de la generation de données ###')
		if (self.jsonFile):
			self.dataSchema = self.readJsonFile(self.jsonFile)
			self.primaryColumn = self.extractPrimaryColumn(self.dataSchema);
			self.data = self.generateDatas(self.dataSchema)
			# self.generateJsonFile('data.json', self.data)
			return self.data
		elif (self.inputFile):
			self.request = self.readFileSql(self.inputFile)
			self.dataSchema = self.extractCreateRequests(self.request)
			return self.dataSchema
			if (not self.dataSchema):
				print ('fichier impossible a parser, verifier qu\'il sagit bien d\'un fichier sql en entree')

	def readFileSql(self, inputFile):
		print('### Lecture du fichier SQL ###')
		totalRequest = ''
		try:
			with open(inputFile, 'r') as file:
				for line in file:
					totalRequest += line 
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
		print('### Lecture du fichier JSON ###')
		try:
			with open(jsonFile, 'r') as file:
				dataSchema = json.load(file)
		except Exception as e:
			print('Erreur lors de la lecture du fichier')
			print(e)
			exit(1)
		return dataSchema

	def extractCreateRequests(self, request):
		print('### Recuperation des differente CREATE TABLE ###')
		data = {}
		tablePattern = r'CREATE TABLE ([^ ]+) \((.+)\).*;'
		tableMatch = re.findall(tablePattern, request)
		for table in tableMatch:

			tableName = table[0].strip()
			tableRequest = table[1]
			data[tableName] = {}
			data[tableName]['columns'] = {}
			data[tableName]['numberToCreate'] = 10
			columnPattern = r'(?!\([^ )]+),(?! ?[^ (]+\))'
			columnMatch = re.split(columnPattern, tableRequest) 
			data[tableName]['columns'] = self.extractColumnsFromCreateRequest(columnMatch, tableName)
		return data

	def extractColumnsFromCreateRequest(self, columnRequestTable, tableName):
		print('### Recuperation des columns au sein de la CREATE TABLE %s ###'% tableName)
		columnPattern = r'([^ ]+) ([^ (]+)(?: ?\(([^)]+)\))? ?(.+)?'
		columnData = {}
		for columnRequest in columnRequestTable:
			match = re.findall(columnPattern, columnRequest)
			if match:
				columName = match[0][0].strip()
				columnData[columName] = {} if (not columnData.has_key(columName)) else columnData[columName]
				if (columnRequest.lower().strip().find('primary') != -1): # est-ce qu il faudrait pas le mettre sur column au lieu de columnName
					del columnData[columName]
					patternPrimaryKey = r'PRIMARY KEY ?\((.+)\)'
					matchPrimaryColumn = re.findall(patternPrimaryKey, columnRequest)
					if(len(matchPrimaryColumn) > 0):
						primaryKeys = matchPrimaryColumn[0].split(",")
						for key in primaryKeys:
							cleanKey = key.strip()
							if (not columnData.has_key(cleanKey)):
								columnData[cleanKey] = {}
							columnData[cleanKey]['primary'] = True
				elif (columName.lower().strip().find('index') != -1):
					del columnData[columName]
					pass
					# todo
				elif (columnRequest.lower().strip().find('unique') != -1):
					uniquePattern = r'\((.*)\)'
					matchUnique = re.findall(uniquePattern, columnRequest)
					uniqueColumnName = matchUnique[0].strip()
					if (not self.unique.has_key(tableName)):
						self.unique[tableName] = {}
					if (not self.unique[tableName].has_key(uniqueColumnName)):
						self.unique[tableName][uniqueColumnName] = {}
					self.unique[tableName][uniqueColumnName]['unique'] = True
					del columnData[columName]
					pass
				else:
					columnType = match[0][1]
					columnData[columName]['name'] = columName
					columnData[columName]['type'] = columnType if columnType else None
					columnData[columName]['nullable'] = (columnRequest.lower().find('not null') != -1)
					if (not columnData[columName].has_key('unique')):
						columnData[columName]['unique'] = False
					if (not columnData[columName].has_key('primary')):
						columnData[columName]['primary'] = False
					try:
						columnData[columName]['size'] = int(match[0][2])
					except Exception as e:
						columnData[columName]['size'] = None	
		columnData = self.isThisTableSColumnsUnique(tableName, columnData, self.unique)
		return columnData

	def isThisTableSColumnsUnique(self, tableName, tableColumns, uniqueTable):
		print('### Recuperation des colonnes Uniques ###')
		for column in tableColumns:
			if (uniqueTable.has_key(tableName)):
				if uniqueTable[tableName].has_key(column):
					tableColumns[column.strip()]['unique'] = True
				else:
					tableColumns[column.strip()]['unique'] = False
			else:
				tableColumns[column.strip()]['unique'] = False
		return tableColumns
			# check il il est dans le tablea self.unique

	def extractPrimaryColumn(self, dataSchema):
		print('### Recuperation des primary key ###')
		primaryColumn = {}
		for tableName in dataSchema:
			tableName = tableName.strip()
			primaryColumn[tableName] = []
			for columName in dataSchema[tableName]['columns']:
				if dataSchema[tableName]['columns'][columName.strip()]['primary']:
					primaryColumn[tableName].append(columName)
		print primaryColumn
		return primaryColumn

	def generateDatas(self, dataSchema):
		print('### Generation de la data ###')
		data = {}
		for tableName in dataSchema:
			data[tableName] = self.generateTableData(tableName, dataSchema)
		return data

	def generateTableData(self, tableName, dataSchema):
		if (not tableName in self.tableNameGeneratedData):
			tableData = []
			numberOfRow = dataSchema[tableName]['numberToCreate']
			for i in range(numberOfRow):
				tableData.append(self.generateNewRow(dataSchema[tableName]['columns'], numberOfRow, i, tableName))
				newEntreePrimary = self.primaryColumnKeeper(tableName, tableData[i])
				if (not self.uniqueDatas[tableName].has_key('primaryKey')):
					self.uniqueDatas[tableName]['primaryKey'] = []
				timeout = 0
				while (newEntreePrimary in self.uniqueDatas[tableName]['primaryKey'] and timeout < self.timeout):
					timeout += 1
					del tableData[i]
					tableData.append(self.generateNewRow(dataSchema[tableName]['columns'], numberOfRow, i, tableName))
					newEntreePrimary = self.primaryColumnKeeper(tableName, tableData[i])
				self.uniqueDatas[tableName]['primaryKey'].append(newEntreePrimary)
				if (timeout == 50):
					print "Tentative de generation dans la table `%s` a echoué a cause de la PRIMARY KEY constraint" % tableName
			self.tableNameGeneratedData.append(tableName)
			return tableData
		else:
			return self.data[tableName]

	def primaryColumnKeeper(self, tableName, newData):
		returnPrimary = None
		if (self.primaryColumn.has_key(tableName)):
			if (len(self.primaryColumn[tableName]) > 0):
				returnPrimary = {}
				for primaryColumnIterator in self.primaryColumn[tableName]:
					returnPrimary[primaryColumnIterator] = newData[primaryColumnIterator]
		return returnPrimary

	def generateNewRow(self, columns, numberOfRow, id, tableName):
		print('### Generation d une entree pour la table %s ###'% tableName)
		newRow = {}
		for columnName in columns:
			if (not self.uniqueDatas.has_key(tableName)):
				self.uniqueDatas[tableName] = {}
			if (not self.uniqueDatas[tableName].has_key(columnName)):
				self.uniqueDatas[tableName][columnName] = {}
				self.uniqueDatas[tableName][columnName]['unique'] = []

			newData = self.generateDataColumn(columns[columnName], numberOfRow, id = id)
			if (columns[columnName]['unique']):
				timeout = 0
				while ((newData in self.uniqueDatas[tableName][columnName]['unique']) and (timeout < self.timeout)) :
					newData = self.generateDataColumn(columns[columnName], numberOfRow, id = id)
					timeout += 1
				if timeout == self.timeout:
					print "Tentative de generation de données unique dans la table `%s` pour la colonne `%s` echoué" % tableName, columnName
			#	print newData

			self.uniqueDatas[tableName][columnName]['unique'].append(newData)
			newRow[columnName] = newData
		return newRow

	def generateDataColumn(self, column, numberOfRow, id):
		print('### Generation d une column d une entree ###')
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