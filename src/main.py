# -*- coding: utf-8 -*-
import re

class DataGenerator:
	def __init__(self, inputFile, outputFile):
		self.inputFile = inputFile
		self.outputFile = outputFile
		self.request = ''
		self.createRequest = {}
		self.dataSchema = {}

	def launch(self):
		self.readFile()
		self.extractCreateRequests(self.request)

	def readFile(self):
		try:
			with open(self.inputFile, 'r') as file:
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
		# pattern = r'(CREATE TABLE (nom de la table) (un truc qui prend tout ce qu\'il y a avant le ";"); truc de merde ne comprenant pas de CREATE TABLE )+ '
		pattern = r'CREATE TABLE ([a-z]+) \((.+)\);'
		match = re.findall(pattern, request)
		for num, name in enumerate(match):
			self.saveSchema(name[0], name[1])
			print(num, name)
		# print (match)

	def saveSchema(self, tableName, createRequest):
		self.dataSchema.tableName = {}
		self.dataSchema.tableName.name = tableName
		self.dataSchema.tableName.request = createRequest
		# separer les colonnes puis itérer

		print('fuck')

	def saveColumn(self, columnRequest)
		print('fuck')

if __name__ == '__main__':
	launcher = DataGenerator('../sql-file/film.sql', './data-schema.json')
	launcher.launch();

# launcher = DataGenerator('../sql-file/film.sql', './data-schema.json')