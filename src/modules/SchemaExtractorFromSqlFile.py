# extract createRequest
# extract table name
# extract column
# extract unique
# extract primary

import re
# todo  a supprimer apres
import FileCreator 
import tools

class SchemaExtractor:
  def __init__(self):
    self.request = ""
    self.createRequests = {}
    self.columnsRequests = {}
    self.columnsDataByTable = {}
    self.uniqueColumns = {}
    self.primaryKeyColumns = {}
    self.foreignKeysColumns = {}
    self.dataSchema = {}

    self.indexSearchKey = "index"
    self.primaryKeySearchKey = "primary"
    self.uniqueSearchKey = "unique"

    self.indexKey = "index"
    self.primaryKeyKey = "primary key"
    self.foreignKeyKey = "foreignKey"
    self.uniqueKey = "unique"
    
    self.tableNameKey = "tableName"
    self.columnNameKey = "columnName"

    self.nameKey = "name"
    self.typeKey = "type"
    self.nullableKey = "nullable"
    self.notNullableKey = "not null"
    self.sizeKey = "size"
    
    self.tableKey = "table"
    self.columnKey = "column"
    self.columnsKey = "columns"

  def autoExtract(self, sqlRequest):
    self.request = sqlRequest
    self.createRequests = self.extractCreateRequests(self.request)
    for tableName in self.createRequests:
      self.columnsRequests[tableName] = self.parseColumnsFromCreateRequest(self.createRequests[tableName], tableName)
      self.columnsDataByTable[tableName] = {self.columnKey: {}}
      for columnNumber in range(len(self.columnsRequests[tableName])):
        extractData = self.parseColumnDataFromColumnRequest(self.columnsRequests[tableName][columnNumber], tableName)
        if (self.indexKey in extractData.keys()):
          pass 
        elif (self.primaryKeyKey in extractData.keys()):
          for columnIndice in extractData[self.primaryKeyKey][self.columnNameKey]:
            columnName = columnIndice  
            if columnName not in self.columnsDataByTable[tableName][self.columnKey].keys():
              self.columnsDataByTable[tableName][self.columnKey][columnName] = {}
            self.columnsDataByTable[tableName][self.columnKey][columnName][self.primaryKeyKey] = True

            if(tableName not in self.primaryKeyColumns.keys()):
              self.primaryKeyColumns[tableName] = {}
            self.primaryKeyColumns[tableName][columnName] = {self.primaryKeyKey: True}
        elif (self.uniqueKey in extractData.keys()):
          columnName = extractData[self.uniqueKey][self.columnNameKey]
          if columnName not in self.columnsDataByTable[tableName][self.columnKey].keys():
            self.columnsDataByTable[tableName][self.columnKey][columnName] = {}
          self.columnsDataByTable[tableName][self.columnKey][columnName][self.uniqueKey] = True
          
          if(tableName not in self.uniqueColumns.keys()):
            self.uniqueColumns[tableName] = {}
          if(columnName not in self.uniqueColumns[tableName].keys()):
            self.uniqueColumns[tableName][columnName] = True
        else:
          columnName = extractData[self.columnKey][self.nameKey]
          if columnName not in self.columnsDataByTable[tableName][self.columnKey].keys():
            self.columnsDataByTable[tableName][self.columnKey][columnName] = extractData[self.columnKey]
          else:
            self.columnsDataByTable[tableName][self.columnKey][columnName].update(extractData[self.columnKey])
          if self.uniqueKey not in self.columnsDataByTable[tableName][self.columnKey][columnName]:
             self.columnsDataByTable[tableName][self.columnKey][columnName][self.uniqueKey] = False
          if self.primaryKeyKey not in self.columnsDataByTable[tableName][self.columnKey][columnName]:
             self.columnsDataByTable[tableName][self.columnKey][columnName][self.primaryKeyKey] = False 
    self.parseAltertableRequests(self.request)
    self.columnsDataByTable = tools.update_object(self.columnsDataByTable, self.foreignKeysColumns)

    return self.columnsDataByTable

  def extractCreateRequests(self, request):
    print('### Recuperation des differente CREATE TABLE ###')
    data = {}
    tablePattern = r'CREATE TABLE ([^ ]+) \((.+)\).*;'
    tableMatch = re.findall(tablePattern, request)
    for table in tableMatch:
      tableName = table[0].strip()
      tableRequest = table[1]
      data[tableName] = tableRequest
    self.createRequests = data
    return data

  def parseColumnsFromCreateRequest(self, tableRequest, tableName):
    columnPattern = r'(?!\([^ )]+),(?! ?[^ (]+\))'
    columnMatch = re.split(columnPattern, tableRequest)
    self.columnsRequests[tableName] = columnMatch
    return columnMatch
    
  def parseColumnDataFromColumnRequest(self, columnRequest, tableName):
    columnData = {}
    columnPattern = r'([^ ]+) ([^ (]+)(?: ?\(([^)]+)\))? ?(.+)?'
    match = re.findall(columnPattern, columnRequest)
    if match:
      columDirective = match[0][0].strip()
      if (columnRequest.lower().strip().find(self.primaryKeySearchKey) != -1):
        patternPrimaryKey = r'PRIMARY KEY ?\((.+)\)'
        matchPrimaryColumn = re.findall(patternPrimaryKey, columnRequest)
        if(len(matchPrimaryColumn) > 0):
          primaryKeys = matchPrimaryColumn[0].split(",")
          cleanKeys = map(lambda x: x.strip(), primaryKeys)
        columnData = {self.primaryKeyKey: {self.tableNameKey: tableName, self.columnNameKey: cleanKeys}}
      elif (columDirective.lower().strip().find(self.indexSearchKey) != -1):
        columnData = {self.indexKey: {}}
      elif (columnRequest.lower().strip().find(self.uniqueSearchKey) != -1):
        uniquePattern = r'\((.*)\)'
        matchUnique = re.findall(uniquePattern, columnRequest)
        uniqueColumnName = matchUnique[0].strip()
        columnData = {self.uniqueKey: {self.tableNameKey: tableName, self.columnNameKey: uniqueColumnName}}
      else:
        columnType = match[0][1]
        columnData[self.nameKey] = columDirective
        columnData[self.typeKey] = columnType if columnType else None
        columnData[self.nullableKey] = (columnRequest.lower().find(self.notNullableKey) != -1)
        try:
          columnData[self.sizeKey] = int(match[0][2])
        except Exception as e:
          columnData[self.sizeKey] = None
        columnData = {self.columnKey: columnData}
    # je sais pas comment transferer dans les data local
    return columnData

  def parseAltertableRequests(self, sqlRequest):
    data = {}
    foreignKeyPattern = r'ALTER TABLE ([^ ]+) ADD CONSTRAINT FK\_[^ ]+ FOREIGN KEY \(([^ ]+)\) REFERENCES ([^ ]+) \(([^ ]+)\)'
    foreignKeysMatch = re.findall(foreignKeyPattern, sqlRequest)
    for foreignKey in foreignKeysMatch:
      destTableName = foreignKey[0].strip()
      destColumName = foreignKey[1].strip()
      srcTableName = foreignKey[2].strip()
      srcColumName = foreignKey[3].strip()
      data[destTableName] = {self.columnKey: {}} if (destTableName not in data.keys()) else data[destTableName]
      data[destTableName][self.columnKey][destColumName] = {self.typeKey: self.foreignKeyKey, self.foreignKeyKey: {self.tableNameKey: srcTableName, self.columnNameKey: srcColumName}}
    self.foreignKeysColumns = data 
    return data


