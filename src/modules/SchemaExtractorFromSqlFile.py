import re
import tools
import sqlparse
import Key

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

  def autoExtract(self, sqlRequest):
    self.request = sqlRequest
    self.createRequests = self.extractCreateRequests(self.request)
    for tableName in self.createRequests:
      self.columnsRequests[tableName] = self.parseColumnsFromCreateRequest(self.createRequests[tableName], tableName)
      self.columnsDataByTable[tableName] = {self.columnsKey: {}}
      for columnNumber in range(len(self.columnsRequests[tableName])):
        extractData = self.parseColumnDataFromColumnRequest(self.columnsRequests[tableName][columnNumber], tableName)
        if (self.indexKey in extractData.keys()):
          pass 
        elif (self.primaryKeyKey in extractData.keys()):
          for columnIndice in extractData[self.primaryKeyKey][self.columnNameKey]:
            columnName = columnIndice  
            if columnName not in self.columnsDataByTable[tableName][self.columnsKey].keys():
              self.columnsDataByTable[tableName][self.columnsKey][columnName] = {}
            self.columnsDataByTable[tableName][self.columnsKey][columnName][self.primaryKeyKey] = True

            if(tableName not in self.primaryKeyColumns.keys()):
              self.primaryKeyColumns[tableName] = {}
            self.primaryKeyColumns[tableName][columnName] = {self.primaryKeyKey: True}
        elif (self.uniqueKey in extractData.keys()):
          columnName = extractData[self.uniqueKey][self.columnNameKey]
          if columnName not in self.columnsDataByTable[tableName][self.columnsKey].keys():
            self.columnsDataByTable[tableName][self.columnsKey][columnName] = {}
          self.columnsDataByTable[tableName][self.columnsKey][columnName][self.uniqueKey] = True
          
          if(tableName not in self.uniqueColumns.keys()):
            self.uniqueColumns[tableName] = {}
          if(columnName not in self.uniqueColumns[tableName].keys()):
            self.uniqueColumns[tableName][columnName] = True
        else:
          columnName = extractData[self.columnsKey][self.nameKey]
          if columnName not in self.columnsDataByTable[tableName][self.columnsKey].keys():
            self.columnsDataByTable[tableName][self.columnsKey][columnName] = extractData[self.columnsKey]
          else:
            self.columnsDataByTable[tableName][self.columnsKey][columnName].update(extractData[self.columnsKey])
          if self.uniqueKey not in self.columnsDataByTable[tableName][self.columnsKey][columnName]:
             self.columnsDataByTable[tableName][self.columnsKey][columnName][self.uniqueKey] = False
          if self.primaryKeyKey not in self.columnsDataByTable[tableName][self.columnsKey][columnName]:
             self.columnsDataByTable[tableName][self.columnsKey][columnName][self.primaryKeyKey] = False 
    self.parseAltertableRequests(self.request)
    self.columnsDataByTable = tools.update_object(self.columnsDataByTable, self.foreignKeysColumns)

    return self.columnsDataByTable

  def autoExtractWithSqlParse(self, sqlRequest):
    self.request = sqlRequest
    self.createRequests = self.extractCreateRequestsWithSqlParse(self.request)
    for tableName in self.createRequests:
      self.columnsRequests[tableName] = self.parseColumnsFromCreateRequest(self.createRequests[tableName], tableName)
      self.columnsDataByTable[tableName] = {Key.columns: {}}
      for columnNumber in range(len(self.columnsRequests[tableName])):
        extractData = self.parseColumnDataFromColumnRequest(self.columnsRequests[tableName][columnNumber], tableName)
        if (Key.index in extractData.keys()):
          pass 
        elif (Key.primaryKey in extractData.keys()):
          for columnIndice in extractData[Key.primaryKey][Key.columnName]:
            columnName = columnIndice  
            if columnName not in self.columnsDataByTable[tableName][Key.columns].keys():
              self.columnsDataByTable[tableName][Key.columns][columnName] = {}
            self.columnsDataByTable[tableName][Key.columns][columnName][Key.primaryKey] = True

            if(tableName not in self.primaryKeyColumns.keys()):
              self.primaryKeyColumns[tableName] = {}
            self.primaryKeyColumns[tableName][columnName] = {Key.primaryKey: True}
        elif (Key.unique in extractData.keys()):
          columnName = extractData[Key.unique][Key.columnName]
          if columnName not in self.columnsDataByTable[tableName][Key.columns].keys():
            self.columnsDataByTable[tableName][Key.columns][columnName] = {}
          self.columnsDataByTable[tableName][Key.columns][columnName][Key.unique] = True
          
          if(tableName not in self.uniqueColumns.keys()):
            self.uniqueColumns[tableName] = {}
          if(columnName not in self.uniqueColumns[tableName].keys()):
            self.uniqueColumns[tableName][columnName] = True
        else:
          columnName = extractData[Key.columns][Key.name]
          if columnName not in self.columnsDataByTable[tableName][Key.columns].keys():
            self.columnsDataByTable[tableName][Key.columns][columnName] = extractData[Key.columns]
          else:
            self.columnsDataByTable[tableName][Key.columns][columnName].update(extractData[Key.columns])
          if Key.unique not in self.columnsDataByTable[tableName][Key.columns][columnName]:
             self.columnsDataByTable[tableName][Key.columns][columnName][Key.unique] = False
          if Key.primaryKey not in self.columnsDataByTable[tableName][Key.columns][columnName]:
             self.columnsDataByTable[tableName][Key.columns][columnName][Key.primaryKey] = False 
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

  def extractCreateRequestsWithSqlParse(self, request):
    data = {}
    stmt = sqlparse.parse(request)
    for i in range(len(stmt)):
      if(stmt[i].get_type() == 'CREATE'):
        tableName = stmt[i].get_real_name()
        tableRequest = stmt[i].__str__()
        _, par = stmt[i].token_next_by(i=sqlparse.sql.Parenthesis)
        data[tableName] = par.value[1:-1]
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
      if (columnRequest.lower().strip().find(Key.primaryKeySearch) != -1):
        patternPrimaryKey = r'PRIMARY KEY ?\((.+)\)'
        matchPrimaryColumn = re.findall(patternPrimaryKey, columnRequest)
        if(len(matchPrimaryColumn) > 0):
          primaryKeys = matchPrimaryColumn[0].split(",")
          cleanKeys = map(lambda x: x.strip(), primaryKeys)
        columnData = {Key.primaryKey: {Key.tableName: tableName, Key.columnName: cleanKeys}}
      elif (columDirective.lower().strip().find(Key.indexSearch) != -1):
        columnData = {Key.index: {}}
      elif (columnRequest.lower().strip().find(Key.uniqueSearch) != -1):
        uniquePattern = r'\((.*)\)'
        matchUnique = re.findall(uniquePattern, columnRequest)
        uniqueColumnName = matchUnique[0].strip()
        columnData = {Key.unique: {Key.tableName: tableName, Key.columnName: uniqueColumnName}}
      else:
        columnType = match[0][1]
        columnData[Key.name] = columDirective
        columnData[Key.type] = columnType if columnType else None
        columnData[Key.nullable] = (columnRequest.lower().find(Key.notNullable) != -1)
        try:
          columnData[Key.size] = int(match[0][2])
        except Exception as e:
          columnData[Key.size] = None
        columnData = {Key.columns: columnData}
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
      data[destTableName] = {Key.columns: {}} if (destTableName not in data.keys()) else data[destTableName]
      data[destTableName][Key.columns][destColumName] = {Key.type: Key.foreignKey, Key.foreignKey: {Key.tableName: srcTableName, Key.columnName: srcColumName}}
    self.foreignKeysColumns = data 
    return data


