# extract createRequest
# extract table name
# extract column
# extract unique
# extract primary

import re
# todo  a supprimer apres
import FileCreator 

class SchemaExtractor:
  def __init__(self):
    self.request = ""
    self.createRequests = {}
    self.columnsRequests = {}
    self.columnsDataByTable = {}
    self.uniqueColumn = {}
    self.dataSchema = {}

    self.columnKey = "column"

    self.indexSearchKey = "index"
    self.primaryKeySearchKey = "primary"
    self.uniqueSearchKey = "unique"

    self.indexKey = "index"
    self.primaryKeyKey = "primary key"
    self.uniqueKey = "unique"
    
    self.tableNameKey = "tableName"
    self.columnNameKey = "columnName"

    self.nameKey = "name"
    self.typeKey = "type"
    self.nullableKey = "nullable"
    self.notNullableKey = "not null"
    self.sizeKey = "size"

  def autoExtract(self, sqlRequest):
    self.request = sqlRequest
    self.createRequests = self.extractCreateRequests(self.request)
    for tableName in self.createRequests:
      self.columnsRequests[tableName] = self.parseColumnsFromCreateRequest(self.createRequests[tableName])
      self.columnsDataByTable[tableName] = {}
      for columnNumber in range(len(self.columnsRequests[tableName])):
        extractData = self.parseColumnDataFromColumnRequest(self.columnsRequests[tableName][columnNumber], tableName)
        if (self.indexKey in extractData.keys()):
          pass 
        elif (self.primaryKeyKey in extractData.keys()):
          pass 
        elif (self.uniqueKey in extractData.keys()):
          if extractData[self.uniqueKey][self.columnNameKey] not in self.columnsDataByTable[tableName].keys():
            self.columnsDataByTable[tableName][extractData[self.uniqueKey][self.columnNameKey]] = {}
          self.columnsDataByTable[tableName][extractData[self.uniqueKey][self.columnNameKey]][self.uniqueKey] = True
        else:
          if extractData[self.columnKey][self.nameKey] not in self.columnsDataByTable[tableName].keys():
            self.columnsDataByTable[tableName][extractData[self.columnKey][self.nameKey]] = extractData[self.columnKey]
          else:
            self.columnsDataByTable[tableName][extractData[self.columnKey][self.nameKey]].update(extractData[self.columnKey])
    generateJsonFile(self.columnsDataByTable, './wip.json')
    # WIP
    print(self.columnsDataByTable)        


  def extractCreateRequests(self, request):
    print('### Recuperation des differente CREATE TABLE ###')
    data = {}
    tablePattern = r'CREATE TABLE ([^ ]+) \((.+)\).*;'
    tableMatch = re.findall(tablePattern, request)
    for table in tableMatch:
      tableName = table[0].strip()
      tableRequest = table[1]
      data[tableName] = tableRequest
    return data

  def parseColumnsFromCreateRequest(self, tableRequest):
    columnPattern = r'(?!\([^ )]+),(?! ?[^ (]+\))'
    columnMatch = re.split(columnPattern, tableRequest) 
    return columnMatch
    
  def parseColumnDataFromColumnRequest(self, columnRequest, tableName):
    columnData = {}
    columnPattern = r'([^ ]+) ([^ (]+)(?: ?\(([^)]+)\))? ?(.+)?'
    match = re.findall(columnPattern, columnRequest)
    #print(match)
    if match:
      columDirective = match[0][0].strip()
      if (columnRequest.lower().strip().find(self.primaryKeySearchKey) != -1):
        # todo
        # patternPrimaryKey = r'PRIMARY KEY ?\((.+)\)'
        # matchPrimaryColumn = re.findall(patternPrimaryKey, columnRequest)
        # if(len(matchPrimaryColumn) > 0):
          # primaryKeys = matchPrimaryColumn[0].split(",")
          # for key in primaryKeys:
        columnData = {self.primaryKeyKey: {}}
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
    # WIP
    print (columnData)
    return columnData

  def extractAltertableRequest(self, request):
    pass


