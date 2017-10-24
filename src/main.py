# -*- coding: utf-8 -*-
#!/usr/bin/python
# actuellement lance via `python ./main.py -if '../sql-file/film.sql'`
import re
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-if','--inputFile', help='SQL file schema to generate data')
parser.add_argument('-of','--outputFile', help='json file which resume the schema')
args = parser.parse_args()

class DataGenerator:
	def __init__(self, inputFile, outputFile):
		self.inputFile = inputFile
		self.outputFile = outputFile
		self.request = ''
		self.createRequest = {}
		self.dataSchema = {}
		self.data = {}

	def launch(self):
		self.readFileSql(self.inputFile)
		self.extractCreateRequests(self.request)
		self.generateJson(self.outputFile, self.dataSchema)
		# print(self.dataSchema)

	def readFileSql(self, inputFile):
		try:
			with open(inputFile, 'r') as file:
				for line in file:
					self.request += line 
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

	def extractCreateRequests(self, request):
		tablePattern = r'CREATE TABLE ([a-z]+) \((.+)\);'
		tableMatch = re.findall(tablePattern, request)
		for table in tableMatch:
			tableName = table[0]
			tableRequest = table[1]
			self.dataSchema[tableName] = {}
			self.dataSchema[tableName]['column'] = {}
			columnMatch = tableRequest.split(",")
			self.dataSchema[tableName]['column'] = self.extractColumns(columnMatch)
			# print(num, name)

	def extractColumns(self, columnTable):
		# WIP
		columnPattern = r'(\S+) (\S+) ?\(?(\d+)?\)? (.*)'
		columnData = {}
		for column in columnTable:
			match = re.findall(columnPattern, column)
			if match:
				columName = match[0][0]
				columnData[columName] = {}
				if (columName.lower().strip().find('primary') != -1):
					patternPrimaryKey = r'primary key ?\((.+)\)'
					matchPrimaryColumn = re.findall(patternPrimaryKey, column.lower())
					primaryKeys = matchPrimaryColumn[0].split(",")
					print(columnData)
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

	def generateJson(self, outputFile, data):
		try:
			with open(outputFile, 'w') as file:
				file.write(json.dumps(data, indent=2))
		except Exception as e:
			print('Erreur lors de la creation du fichier')
			print(e)
			exit(1)

if __name__ == '__main__':
	if (not args.inputFile):
		parser.print_help()
	else:
		# verifier qu'il existe
		outputFile = args.outputFile if args.outputFile else './data-schema.json'
		launcher = DataGenerator(args.inputFile, outputFile)
		launcher.launch()
