#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

import sys
sys.path.append('./modules/')
import FileReader
import FileCreator
from SchemaExtractorFromSqlFile import * 
from FromSchemaToData import * 
import tools

parser = argparse.ArgumentParser()
parser.add_argument('-sql','--sql_file', help = 'sql file schema to generate data')
parser.add_argument('-out','--output_file', help = 'json file which resume the schema')
parser.add_argument('-sch','--schema', help = 'json file which resume the schema to generate data')
parser.add_argument('-psch','--prepared_schema', help = 'json file with some prepared parametters')
parser.add_argument('-y','--yes', help = 'permit to ignore the json verification and use default value', action='store_true')
args = parser.parse_args()

class app:
	def __init__(self):
			self.request = ''
			self.input_file = '../sql-file/cuisine.sql'
			self.schema_extractor = SchemaExtractor()
			self.data_generator = DataGenerator()

	def from_sql_file_to_schema(self, sql_file, output_file, prepared_file = None):
			self.request = FileReader.read_file_sql(self.input_file)
			self.schema_extractor.auto_extract_with_sql_parse(self.request)
			self.data_generator.complete_schema(self.schema_extractor.columns_data_by_table)
			schema = self.from_schema_to_meta_schema(prepared_file = prepared_file, schema = self.data_generator.schema_to_work)
			FileCreator.generate_json_file(self.data_generator.schema_to_work, output_file)

	def from_schema_to_data(self, schema_file, output_file, prepared_file = None):
			schema = self.from_schema_to_meta_schema(schema_file, prepared_file)
			order_of_table = self.data_generator.from_schema_to_order(schema)
			self.data_generator.generate_ordered_datas(schema, order_of_table)
			# self.datagenerator.generatedatas(schema)
			formated_data = tools.from_data_to_ordered_object_to_print(self.data_generator.data, order_of_table)
			FileCreator.generate_txt_file_from_object(formated_data, output_file)

	def from_schema_to_meta_schema(self, schema_file = None, prepared_file = None, schema = None, prepared_schema = None):
		if(schema_file == None and schema == None):
				print('[error][from_schema_to_meta_schema] Il faut au moins une source de schema')
				exit(1)
		elif(prepared_file == None and prepared_schema == None):
				schema_from_file = schema if not schema == None else FileReader.read_json_file(schema_file)
				return schema_from_file
		else:
				schema_from_file = schema if not schema == None else FileReader.read_json_file(schema_file)
				if(prepared_file == None):
						schema = schema_from_file
				else:
						schema_from_prepared_file = prepared_schema if not prepared_schema == None else FileReader.read_json_file(prepared_file)
						schema = tools.update_object(schema_from_file, schema_from_prepared_file)
				return schema

if __name__ == '__main__':
	launcher = app()
	prepared_file = args.prepared_schema
	if (args.schema):
		output_file = args.output_file if args.output_file else './data.sql'
		launcher.from_schema_to_data(args.schema, output_file, prepared_file)
	elif (args.sql_file):
		if args.yes:
			output_file = './data-schema.json'
			launcher.from_sql_file_to_schema(args.sql_file, output_file, prepared_file)
			data_file = args.output_file if args.output_file else './data.sql'
			launcher.from_schema_to_data(output_file, data_file, prepared_file)
		else:
			output_file = (args.output_file if args.output_file else './data-schema.json')
			launcher.from_sql_file_to_schema(args.sql_file, output_file, prepared_file)
	else:
		parser.print_help()
	