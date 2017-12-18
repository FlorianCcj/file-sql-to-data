#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import json
import argparse
import random
from lxml import etree
from faker import Faker
fake = Faker()

import sys
sys.path.append('./modules/')
import FileReader
import FileCreator
from SchemaExtractorFromSqlFile import * 
from FromSchemaToData import * 
import tools

parser = argparse.ArgumentParser()
parser.add_argument('-sf','--sql_file', help = 'sql file schema to generate data')
parser.add_argument('-of','--output_file', help = 'json file which resume the schema')
parser.add_argument('-schf','--schema_file', help = 'json file which resume the schema to generate data')
parser.add_argument('-y','--yes', help = 'permit to ignore the json verification and use default value', action='store_true')
args = parser.parse_args()

class app:
	def __init__(self):
		self.request = ''
		self.input_file = '../sql-file/cuisine.sql'
		self.schema_extractor = SchemaExtractor()
		self.data_generator = DataGenerator()

	def from_sql_file_to_schema(self, sql_file, output_file):
		self.request = FileReader.read_file_sql(self.input_file)
		self.schema_extractor.auto_extract_with_sql_parse(self.request)
		self.data_generator.complete_schema(self.schema_extractor.columns_data_by_table)
		FileCreator.generate_json_file(self.data_generator.schema_to_work, output_file)

	def from_schema_to_data(self, schema_file, output_file):
		schema = FileReader.read_json_file(schema_file)
		order_of_table = self.data_generator.from_schema_to_order(schema)
		self.data_generator.generate_ordered_datas(schema, order_of_table)
		# self.datagenerator.generatedatas(schema)
		formated_data = tools.from_data_to_ordered_object_to_print(self.data_generator.data, order_of_table)
		FileCreator.generate_txt_file_from_object(formated_data, output_file)

print(args)
if __name__ == '__main__':
	launcher = app()
	if (args.schema_file):
		output_file = args.output_file if args.output_file else './data.sql'
		launcher.from_schema_to_data(args.schema_file, output_file)
	elif (args.sql_file):
		if args.yes:
			output_file = './data-schema.json'
			launcher.from_sql_file_to_schema(args.sql_file, output_file)
			data_file = args.output_file if args.output_file else './data.sql'
			launcher.from_schema_to_data(output_file, data_file)
		else:
			output_file = (args.output_file if args.output_file else './data-schema.json')
			launcher.from_sql_file_to_schema(args.sql_file, output_file)
	else:
		parser.print_help()
	