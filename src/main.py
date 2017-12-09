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
		self.launcher()

	def launcher(self):
		self.request = FileReader.readFileSql(self.inputFile)
		self.schemaExtractor.autoExtract(self.request)
		FileCreator.generateJsonFile(self.schemaExtractor.columnsDataByTable, './data-schema.json')
		# ordonnancer
		dataScemaOrdered = self.testOrderData(self.schemaExtractor.columnsDataByTable)
		FileCreator.generateJsonFile(dataScemaOrdered, './data-schema-ordered.json')
		# ajouter le nombre de data a creer
		# ajouter les referentiels dans la DB
		# creer les fichier

	def testOrderData(self, dataSchemaWithForeignKey):
		columnKey = self.schemaExtractor.columnKey
		typeKey = self.schemaExtractor.typeKey
		foreignKeyKey = self.schemaExtractor.foreignKeyKey
		tableNameKey = self.schemaExtractor.tableNameKey
		orderKey = 'order'
		timeout = 50
		numberOfTable = len(dataSchemaWithForeignKey)
		tableAlreadyDone = []
		numberOfTableDone = len(tableAlreadyDone)
		tryTime = 0
		while len(tableAlreadyDone) != numberOfTable and tryTime <= timeout:
			print('------------------')
			print(len(tableAlreadyDone))
			print(numberOfTable)
			print(tryTime)
			print(timeout)
			tryTime += 1 # init
			# tryTime += 0 # add
			save = True
			for tableName in dataSchemaWithForeignKey:
				if tableName not in tableAlreadyDone:
					foreignKeyCounter = 0
					tableForeignKey = [] # add
					for columnName in dataSchemaWithForeignKey[tableName][columnKey]:
						if dataSchemaWithForeignKey[tableName][columnKey][columnName][typeKey] == foreignKeyKey:
							foreignKeyCounter += 1
							# if dataSchemaWithForeignKey[tableName][columnKey][columnName][foreignKeyKey]: # add
							# 	if 'tableName' in dataSchemaWithForeignKey[tableName][columnKey][columnName][foreignKeyKey]: # add
							# 		tableForeignKey.append(dataSchemaWithForeignKey[tableName][columnKey][columnName][foreignKeyKey]['tableName']) # add
							if tableNameKey not in dataSchemaWithForeignKey[tableName][columnKey][columnName][foreignKeyKey].keys():
								save = False
							else:
								if dataSchemaWithForeignKey[tableName][columnKey][columnName][foreignKeyKey][tableNameKey] not in tableAlreadyDone:
									save = False 

					if(foreignKeyCounter == 0):
						save = True
					if(save == True): # init
					# if(True == True):
						dataSchemaWithForeignKey[tableName][orderKey] = len(tableAlreadyDone) # init 
						# dataSchemaWithForeignKey[tableName][orderKey] = tableForeignKey 
						# dataSchemaWithForeignKey[tableName][orderKey] = foreignKeyCounter 
						tableAlreadyDone.append(tableName)
						tryTime = 0
			numberOfTableDone = len(tableAlreadyDone)
			print('+++++++++++++++')
			print(len(tableAlreadyDone))
			print(numberOfTable)
			print(tryTime)
			print(timeout)
		if (tryTime == timeout):
			print('[Erreur][order] erreur lors de l ordonnancement des tables, l une d elle a une foreign key qui n existe pas')
		return dataSchemaWithForeignKey



Test()












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
		self.foreignKeys = {}
		self.foreignKeysData = {}
		
		self.refData = {}

		self.timeout = 50
		self.defaultNumberToCreate = 10

	def launch(self):
		print('### Lancement de la generation de donnees ###')
		if (self.jsonFile):
			self.dataSchema = self.readJsonFile(self.jsonFile)
			self.primaryColumn = self.extractPrimaryColumn(self.dataSchema);
			self.data = self.generateDatas(self.dataSchema)
			self.data = self.generateForeignKey(self.dataSchema, self.data)
			return self.data
		elif (self.inputFile):
			# recuperation de la donnee
			self.request = self.readFileSql(self.inputFile)
			# extraction de chaque requete
			# extraction des columns
			self.dataSchema = self.extractCreateRequests(self.request)
			# recuperation des primary
			# creation des donnees
			self.foreignKeys = self.extractForeignKey(self.request);
			self.dataSchema = self.mergeSchemaAndForeignKeys(self.dataSchema, self.foreignKeys)
			if (not self.dataSchema):
				print ('fichier impossible a parser, verifier qu\'il sagit bien d\'un fichier sql en entree')
			return self.dataSchema

	def generateDatas(self, dataSchema):
		print('### Generation de la data ###')
		data = {}
		for tableName in dataSchema:
			data[tableName] = self.generateTableData(tableName, dataSchema)
		return data

	def generateForeignKey(self, dataSchema, data):
		print('### Liaison de la data ###')
		newData = data
		for tableName in dataSchema:
			for columnName in dataSchema[tableName]['columns']:
				if (dataSchema[tableName]['columns'][columnName]['type'] == 'foreign key' and dataSchema[tableName]['columns'][columnName].has_key('foreignKey')):
					srcTableName = dataSchema[tableName]['columns'][columnName]['foreignKey']['table']
					srcColumnName = dataSchema[tableName]['columns'][columnName]['foreignKey']['column']
					if (not self.foreignKeysData.has_key(srcTableName)):
						self.foreignKeysData[srcTableName] = {}
					if (not self.foreignKeysData[srcTableName].has_key(srcColumnName)):
						self.foreignKeysData[srcTableName][srcColumnName] = []
					if (self.foreignKeysData[srcTableName][srcColumnName] == []):
						self.foreignKeysData[srcTableName][srcColumnName] = self.generateForeignKeyData(srcTableName, srcColumnName)
					for numerousOfData in range(0, len(data[tableName])-1):
						timeout = 0
						transformData = newData[tableName][numerousOfData]
						transformData[columnName] = self.generateForeignKeyColumn(self.foreignKeysData[srcTableName][srcColumnName])
						if (self.primaryColumn.has_key(tableName) and columnName in self.primaryColumn[tableName]):
							newEntreePrimary = self.primaryColumnKeeper(tableName, transformData)	
						# todo : a factoriser dans une fonction
							while (newEntreePrimary in self.uniqueDatas[tableName]['primaryKey'] and timeout < self.timeout):
								timeout += 1
								transformData[columnName] = self.generateForeignKeyColumn(self.foreignKeysData[srcTableName][srcColumnName])
								newEntreePrimary = self.primaryColumnKeeper(tableName, transformData)
							self.uniqueDatas[tableName]['primaryKey'].append(newEntreePrimary)
						newData[tableName][numerousOfData] = transformData
						if (timeout == 50):
							print "[error] [primary generation FK] Tentative de generation dans la table %s a echoue a cause de la PRIMARY KEY constraint" % tableName
		return newData

	def generateForeignKeyColumn(self, dataToRand):
		randomNum = random.randint(0, len(dataToRand)-1)
		return dataToRand[randomNum]

	def generateForeignKeyData(self, tableName, columnName):
		dataForForeignKeys = [];
		if (self.data.has_key(tableName)):
			for data in self.data[tableName]:
				if (data.has_key(columnName)):
					dataForForeignKeys.append(data[columnName])
				else:
					print('[ERREUR][FK] la foreign key %s(%s) n existe pas'%tableName, columnName)
		else:
			print('[ERREUR] [FK] la table %s(%s) pour recuperer la foreign key n existe pas'%tableName, columnName)		
		return dataForForeignKeys

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
					print "[error] [primary generation] Tentative de generation dans la table %s a echoue a cause de la PRIMARY KEY constraint" % tableName
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
					# todo : comprendre pourquoi ca marche pas 
					# print("[error] [unique generation] Tentative de generation de donnees unique dans la table %s pour la colonne %s echoue" %tableName , columnName)
					print("[error] [unique generation] Tentative de generation de donnees unique dans la table pour la colonne echoue")

			self.uniqueDatas[tableName][columnName]['unique'].append(newData)
			newRow[columnName] = newData
		return newRow

	def generateDataColumn(self, column, numberOfRow, id):
		# print('### Generation d une column d une entree ###')
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
				elif column['type'].strip().lower() == 'boolean':
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
				elif column['type'].strip().lower() == 'ref':
					generatedData = self.takeRefData(column)
				else:
					generatedData = None
		return generatedData

	def takeRefData(self, column):
		refRecupData = None
		if (column.has_key('refFile')):
			print(column['refFile'])
			if (not self.refData.has_key(column['refFile'])):
				self.refData[column['refFile']] = self.readJsonFile(column['refFile'])
			if (self.refData[column['refFile']]):
				refRecupData = random.choice(self.refData[column['refFile']])
			else:
				refRecupData = None
		return refRecupData
			# si les donnees interne n'ont pas la cle column.refFile
			# 	ouvrir
			# 	recuperer les donnees
			# 	les mettre dans les donnees interne
			# si les donnees internes on la cle et qu il n est pas vide
			# 	recurer une donnee aleatoire dans les data
			# sinon retourner 'null'
class FileCreator:
	def __init__(self, outputFile = None, extension = None, data = {}, dataType = None):
		self.extensionFile = extension
		self.data = data
		self.outputFile = {}
		if (not outputFile):
			if (not dataType):
				self.outputFile['name'] = 'default-output-file'
				self.outputFile['ext'] = 'txt'
				self.outputFile['total'] = self.outputFile['name']+'.'+self.outputFile['ext']
			else:
				self.outputFile['name'] = 'default-output-file'
				self.outputFile['ext'] = dataType
				self.outputFile['total'] = self.outputFile['name']+'.'+self.outputFile['ext']
		else:
				self.outputFile['total'] = outputFile
		self.launch()

	def launch(self):
		self.chooseFormat(self.extensionFile)

	def chooseFormat(self, extension = None):
		if (extension == 'csv'):
			pass
		elif (extension == 'json'):
			self.generateJsonFile(self.data, self.outputFile['total'])
		else:
			# WIP
			self.generateJsonFile(self.data, self.outputFile['total']+'.json')
			self.generateXmlFile(self.data, self.outputFile['total']+'.xml')
			self.generateSqlFile(self.data, self.outputFile['total']+'.sql')

	def generateJsonFile(self, data, outputFile):
		try:
			with open(outputFile, 'w') as file:
				file.write(json.dumps(data, indent=2))
		except Exception as e:
			print('Erreur lors de la creation du fichier')
			print(e)
			exit(1)

	def generateXmlFile(self, data, outputFile):
		root = etree.Element('data')
		try:
			for tableName in data:
				table = etree.SubElement(root, tableName)
				for elementOfTable in data[tableName]:
					elementOfXml = etree.SubElement(table, 'element')
					if(elementOfTable.has_key('id')):
						elementOfXml.set('id', str(elementOfTable['id']))
					columnOfXml = None
					for columnOfTable in elementOfTable:
						columnOfXml = etree.SubElement(elementOfXml, columnOfTable).text = str(elementOfTable[columnOfTable])
		except:
			print('Erreur de formmat pour la creation de format Xml')
			exit(1)
		try:
			with open(outputFile, 'w') as fic:
				fic.write(etree.tostring(root, pretty_print=True).decode('utf-8'))
		except IOError:
			print('Problème rencontre lors de l\'ecriture...')
			exit(1)

	def generateSqlFile(self, data, outputFile):
		fichier = open(outputFile, "w")
		eolSymbole = '\n'
		
		try:
			for tableName in data:
				beginInsertValueLign = 'INSERT INTO ' + str(tableName) + ' (' 
				for columnName in data[tableName][0]:
					beginInsertValueLign = beginInsertValueLign + columnName + ', '
				beginInsertValueLign = beginInsertValueLign[:len(beginInsertValueLign)-2] + ') VALUES '
				fichier.write(beginInsertValueLign)	
				fichier.write(eolSymbole)

				endInsertValueLignInitial = '('
				for element in data[tableName]:
					endInsertValueLign = endInsertValueLignInitial
					for column in element:
						endInsertValueLign = endInsertValueLign + str(element[column]) + ', '
					endInsertValueLign = endInsertValueLign[:len(endInsertValueLign)-2] + ')'
					
					fichier.write(endInsertValueLign)	
					fichier.write(eolSymbole)
				fichier.write(';')
				fichier.write(eolSymbole)
				fichier.write(eolSymbole)
		except:
			print('Erreur de formmat pour la creation de format Sql')
			exit(1)


		fichier.close()

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
