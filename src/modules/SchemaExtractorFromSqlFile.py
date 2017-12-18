import re
import tools
import sqlparse
import Key

class SchemaExtractor:
  def __init__(self):
    self.request = ""
    self.create_requests = {}
    self.columns_requests = {}
    self.columns_data_by_table = {}
    self.unique_columns = {}
    self.primarykey_columns = {}
    self.foreignkeys_columns = {}
    self.data_schema = {}

  def auto_extract(self, sql_request):
    self.request = sql_request
    self.create_requests = self.extract_create_requests(self.request)
    for table_name in self.create_requests:
      self.columns_requests[table_name] = self.parse_columns_from_create_request(self.create_requests[table_name], table_name)
      self.columns_data_by_table[table_name] = {Key.columns: {}}
      for column_number in range(len(self.columns_requests[table_name])):
        extract_data = self.parse_column_data_from_column_request(self.columns_requests[table_name][column_number], table_name)
        if (Key.index in extract_data.keys()):
          pass 
        elif (Key.primarykey in extract_data.keys()):
          for column_indice in extract_data[Key.primarykey][Key.column_name]:
            column_name = column_indice  
            if column_name not in self.columns_data_by_table[table_name][Key.columns].keys():
              self.columns_data_by_table[table_name][Key.columns][column_name] = {}
            self.columns_data_by_table[table_name][Key.columns][column_name][Key.primarykey] = True

            if(table_name not in self.primarykey_columns.keys()):
              self.primarykey_columns[table_name] = {}
            self.primarykey_columns[table_name][column_name] = {Key.primarykey: True}
        elif (Key.unique in extract_data.keys()):
          column_name = extract_data[Key.unique][Key.column_name]
          if column_name not in self.columns_data_by_table[table_name][Key.columns].keys():
            self.columns_data_by_table[table_name][Key.columns][column_name] = {}
          self.columns_data_by_table[table_name][Key.columns][column_name][Key.unique] = True
          
          if(table_name not in self.unique_columns.keys()):
            self.unique_columns[table_name] = {}
          if(column_name not in self.unique_columns[table_name].keys()):
            self.unique_columns[table_name][column_name] = True
        else:
          column_name = extract_data[Key.columns][Key.name]
          if column_name not in self.columns_data_by_table[table_name][Key.columns].keys():
            self.columns_data_by_table[table_name][Key.columns][column_name] = extract_data[Key.columns]
          else:
            self.columns_data_by_table[table_name][Key.columns][column_name].update(extract_data[Key.columns])
          if Key.unique not in self.columns_data_by_table[table_name][Key.columns][column_name]:
             self.columns_data_by_table[table_name][Key.columns][column_name][Key.unique] = False
          if Key.primarykey not in self.columns_data_by_table[table_name][Key.columns][column_name]:
             self.columns_data_by_table[table_name][Key.columns][column_name][Key.primarykey] = False 
    self.parse_altertable_requests(self.request)
    self.columns_data_by_table = tools.update_object(self.columns_data_by_table, self.foreignkeys_columns)

    return self.columns_data_by_table

  def auto_extract_with_sql_parse(self, sql_request):
    self.request = sql_request
    self.create_requests = self.extract_create_requests_with_sql_parse(self.request)
    for table_name in self.create_requests:
      self.columns_requests[table_name] = self.parse_columns_from_create_request(self.create_requests[table_name], table_name)
      self.columns_data_by_table[table_name] = {Key.columns: {}}
      for column_number in range(len(self.columns_requests[table_name])):
        extract_data = self.parse_column_data_from_column_request(self.columns_requests[table_name][column_number], table_name)
        if (Key.index in extract_data.keys()):
          pass 
        elif (Key.primarykey in extract_data.keys()):
          for column_indice in extract_data[Key.primarykey][Key.column_name]:
            column_name = column_indice  
            if column_name not in self.columns_data_by_table[table_name][Key.columns].keys():
              self.columns_data_by_table[table_name][Key.columns][column_name] = {}
            self.columns_data_by_table[table_name][Key.columns][column_name][Key.primarykey] = True

            if(table_name not in self.primarykey_columns.keys()):
              self.primarykey_columns[table_name] = {}
            self.primarykey_columns[table_name][column_name] = {Key.primarykey: True}
        elif (Key.unique in extract_data.keys()):
          column_name = extract_data[Key.unique][Key.column_name]
          if column_name not in self.columns_data_by_table[table_name][Key.columns].keys():
            self.columns_data_by_table[table_name][Key.columns][column_name] = {}
          self.columns_data_by_table[table_name][Key.columns][column_name][Key.unique] = True
          
          if(table_name not in self.unique_columns.keys()):
            self.unique_columns[table_name] = {}
          if(column_name not in self.unique_columns[table_name].keys()):
            self.unique_columns[table_name][column_name] = True
        else:
          column_name = extract_data[Key.columns][Key.name]
          if column_name not in self.columns_data_by_table[table_name][Key.columns].keys():
            self.columns_data_by_table[table_name][Key.columns][column_name] = extract_data[Key.columns]
          else:
            self.columns_data_by_table[table_name][Key.columns][column_name].update(extract_data[Key.columns])
          if Key.unique not in self.columns_data_by_table[table_name][Key.columns][column_name]:
             self.columns_data_by_table[table_name][Key.columns][column_name][Key.unique] = False
          if Key.primarykey not in self.columns_data_by_table[table_name][Key.columns][column_name]:
             self.columns_data_by_table[table_name][Key.columns][column_name][Key.primarykey] = False 
    self.parse_altertable_requests(self.request)
    self.columns_data_by_table = tools.update_object(self.columns_data_by_table, self.foreignkeys_columns)

    return self.columns_data_by_table

  def extract_create_requests(self, request):
    print('### Recuperation des differente CREATE TABLE ###')
    data = {}
    table_pattern = r'CREATE TABLE ([^ ]+) \((.+)\).*;'
    table_match = re.findall(table_pattern, request)
    for table in table_match:
      table_name = table[0].strip()
      table_request = table[1]
      data[table_name] = table_request
    self.create_requests = data
    return data

  def extract_create_requests_with_sql_parse(self, request):
    data = {}
    stmt = sqlparse.parse(request)
    for i in range(len(stmt)):
      if(stmt[i].get_type() == 'CREATE'):
        table_name = stmt[i].get_real_name()
        table_request = stmt[i].__str__()
        _, par = stmt[i].token_next_by(i=sqlparse.sql.Parenthesis)
        data[table_name] = par.value[1:-1]
    self.create_requests = data
    return data

  def parse_columns_from_create_request(self, table_request, table_name):
    column_pattern = r'(?!\([^ )]+),(?! ?[^ (]+\))'
    column_match = re.split(column_pattern, table_request)
    self.columns_requests[table_name] = column_match
    return column_match
    
  def parse_column_data_from_column_request(self, column_request, table_name):
    column_data = {}
    column_pattern = r'([^ ]+) ([^ (]+)(?: ?\(([^)]+)\))? ?(.+)?'
    match = re.findall(column_pattern, column_request)
    if match:
      column_directive = match[0][0].strip()
      if (column_request.lower().strip().find(Key.primarykey_search) != -1):
        pattern_primarykey = r'PRIMARY KEY ?\((.+)\)'
        match_primary_column = re.findall(pattern_primarykey, column_request)
        if(len(match_primary_column) > 0):
          primarykeys = match_primary_column[0].split(",")
          clean_keys = map(lambda x: x.strip(), primarykeys)
        column_data = {Key.primarykey: {Key.table_name: table_name, Key.column_name: clean_keys}}
      elif (column_directive.lower().strip().find(Key.index_search) != -1):
        column_data = {Key.index: {}}
      elif (column_request.lower().strip().find(Key.unique_search) != -1):
        unique_pattern = r'\((.*)\)'
        match_unique = re.findall(unique_pattern, column_request)
        unique_column_name = match_unique[0].strip()
        column_data = {Key.unique: {Key.table_name: table_name, Key.column_name: unique_column_name}}
      else:
        column_type = match[0][1]
        column_data[Key.name] = column_directive
        column_data[Key.type] = column_type if column_type else None
        column_data[Key.nullable] = (column_request.lower().find(Key.not_nullable) != -1)
        try:
          column_data[Key.size] = int(match[0][2])
        except Exception as e:
          column_data[Key.size] = None
        column_data = {Key.columns: column_data}
    # je sais pas comment transferer dans les data local
    return column_data

  def parse_altertable_requests(self, sql_request):
    data = {}
    foreignkey_pattern = r'ALTER TABLE ([^ ]+) ADD CONSTRAINT FK\_[^ ]+ FOREIGN KEY \(([^ ]+)\) REFERENCES ([^ ]+) \(([^ ]+)\)'
    foreignkeys_match = re.findall(foreignkey_pattern, sql_request)
    for foreignkey in foreignkeys_match:
      dest_table_name = foreignkey[0].strip()
      dest_column_name = foreignkey[1].strip()
      src_table_name = foreignkey[2].strip()
      src_column_name = foreignkey[3].strip()
      data[dest_table_name] = {Key.columns: {}} if (dest_table_name not in data.keys()) else data[dest_table_name]
      data[dest_table_name][Key.columns][dest_column_name] = {Key.type: Key.foreignkey, Key.foreignkey: {Key.table_name: src_table_name, Key.column_name: src_column_name}}
    self.foreignkeys_columns = data 
    return data


