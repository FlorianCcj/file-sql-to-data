import random
import Key
from faker import Faker
import tools
fake = Faker()

class DataGenerator:
  def __init__(self):
    self.schemaInit = {}
    self.schema_to_work = {}
    self.orderOfTable = {}
    self.timeout = 50
    self.defaultNumberOfDataToCreate = 10

    self.data = {}
    self.tableNameGeneratedData = []
    self.uniqueDatas = {}
    self.primaryColumn = {}
    self.refData = {}

    
  def launcher(self, schema, schemaExtractor):
    self.schemaInit = schema
    self.schemaExtractor = schemaExtractor
    self.completeSchema(schema)
    self.data = self.generateDatas(self.schema_to_work)

  def completeSchema(self, schema, schemaExtractor = {}):
    self.schemaInit = schema
    self.schemaExtractor = schemaExtractor if schemaExtractor != {} else self.schemaExtractor
    dataScemaOrdered = self.orderTable(schema)
    dataScemaOrderedWithNumber = self.addDefaultNumberToTableList(dataScemaOrdered)
    self.schema_to_work = dataScemaOrderedWithNumber
    return dataScemaOrderedWithNumber

  def orderTable(self, dataSchemaWithForeignKey):
    columnsKey = Key.columns
    typeKey = Key.type
    foreignKeyKey = Key.foreignKey
    tableNameKey = Key.tableName
    orderKey = Key.order
    timeout = self.timeout
    numberOfTable = len(dataSchemaWithForeignKey)
    tableAlreadyDone = []
    numberOfTableDone = len(tableAlreadyDone)
    tryTime = 0
    while len(tableAlreadyDone) != numberOfTable and tryTime <= timeout:
      tryTime += 1
      save = True
      for tableName in dataSchemaWithForeignKey:
        if tableName not in tableAlreadyDone:
          foreignKeyCounter = 0
          for columnName in dataSchemaWithForeignKey[tableName][columnsKey]:
            if dataSchemaWithForeignKey[tableName][columnsKey][columnName][typeKey] == foreignKeyKey:
              foreignKeyCounter += 1
              if tableNameKey not in dataSchemaWithForeignKey[tableName][columnsKey][columnName][foreignKeyKey].keys():
                save = False
              else:
                if dataSchemaWithForeignKey[tableName][columnsKey][columnName][foreignKeyKey][tableNameKey] not in tableAlreadyDone:
                  save = False 

          if(foreignKeyCounter == 0):
            save = True
          if(save == True):
            dataSchemaWithForeignKey[tableName][orderKey] = len(tableAlreadyDone)
            tableAlreadyDone.append(tableName)
            tryTime = 0
      numberOfTableDone = len(tableAlreadyDone)
    if (tryTime == timeout):
      print('[Erreur][order] erreur lors de l ordonnancement des tables, l une d elle a une foreign key qui n existe pas')
    return dataSchemaWithForeignKey

  def fromSchemaToOrder(self, schema):
    orderOfTable = {}
    for tableName in schema:
      if (Key.order in schema[tableName]):
        orderOfTable[schema[tableName][Key.order]] = tableName
      else:
        if (Key.nonorder not in orderOfTable):
          orderOfTable[Key.nonorder] = []
        orderOfTable[Key.nonorder].append(tableName)
    self.orderOfTable = orderOfTable
    return orderOfTable

  def addDefaultNumberToTableList(self, tableList):
    tableWithNumber = {}
    for tableName in tableList:
      tableWithNumber[tableName] = self.addDefaultNumberToTable(tableList[tableName])
    return tableWithNumber

  def addDefaultNumberToTable(self, table):
    table[Key.defaultNumberOfDataToCreate] = self.defaultNumberOfDataToCreate
    return table

  def generateDatas(self, dataSchema, schemaExtractor = {}):
    print('### Generation de la data ###')
    self.schemaExtractor = schemaExtractor if schemaExtractor != {} else self.schemaExtractor
    data = {}
    for tableName in dataSchema:
      data[tableName] = self.generateTableData(tableName, dataSchema)
    self.data = data
    return data

  def generateTableData(self, tableName, dataSchema):
    primaryKeyKey = Key.primaryKey
    columnsKey = Key.columns
    finalTimeout = self.timeout
    if (not tableName in self.tableNameGeneratedData):
      tableData = []
      numberOfRowToCreate = dataSchema[tableName][Key.defaultNumberOfDataToCreate]
      for i in range(numberOfRowToCreate):
        tableData.append(self.generateNewRow(dataSchema[tableName][columnsKey], numberOfRowToCreate, i, tableName))
        newEntreePrimary = self.primaryColumnKeeper(tableName, tableData[i])
        if (primaryKeyKey not in self.uniqueDatas[tableName].keys()):
          self.uniqueDatas[tableName][primaryKeyKey] = []
        timeout = 0
        while (newEntreePrimary in self.uniqueDatas[tableName][primaryKeyKey] and timeout < self.timeout):
          timeout += 1
          del tableData[i]
          tableData.append(self.generateNewRow(dataSchema[tableName][columnsKey], numberOfRowToCreate, i, tableName))
          newEntreePrimary = self.primaryColumnKeeper(tableName, tableData[i])
        self.uniqueDatas[tableName][primaryKeyKey].append(newEntreePrimary)
        if (timeout == finalTimeout):
          print "[error] [primary generation] Tentative de generation dans la table %s a echoue a cause de la PRIMARY KEY constraint" % tableName
      self.tableNameGeneratedData.append(tableName)
      return tableData
    else:
      return {}
    # return self.data[tableName]

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
    uniqueKey = Key.unique
    newRow = {}
    for columnName in columns:
      if (tableName not in self.uniqueDatas.keys()):
        self.uniqueDatas[tableName] = {}
      if (columnName not in self.uniqueDatas[tableName].keys()):
        self.uniqueDatas[tableName][columnName] = {}
        self.uniqueDatas[tableName][columnName][uniqueKey] = []

      newData = self.generateDataColumn(columns[columnName], numberOfRow, id = id)
      if (columns[columnName][uniqueKey]):
        timeout = 0
        while ((newData in self.uniqueDatas[tableName][columnName][uniqueKey]) and (timeout < self.timeout)) :
          newData = self.generateDataColumn(columns[columnName], numberOfRow, id = id)
          timeout += 1
        if timeout == self.timeout:
          # todo : comprendre pourquoi ca marche pas 
          # print("[error] [unique generation] Tentative de generation de donnees unique dans la table %s pour la colonne %s echoue" %tableName , columnName)
          print("[error] [unique generation] Tentative de generation de donnees unique dans la table pour la colonne echoue")

      self.uniqueDatas[tableName][columnName][uniqueKey].append(newData)
      newRow[columnName] = newData
    return newRow

  def generateDataColumn(self, column, numberOfRow, id):
    # print('### Generation d une column d une entree ###')
    generatedData = None
    if (column['name'] == 'id'):
      generatedData = id+1
    else:
      if (column.has_key(Key.type)):
        generatedDatas = tools.generateRandomData(
          column[Key.type], 
          numberOfRow, 
          column[Key.referenceFile] if (Key.referenceFile in column.keys()) else '', 
          self.refData[column[Key.ref]] if (Key.ref in column.keys() and column[Key.ref] in self.refData) else ''
        )
        generatedData = generatedDatas[Key.data]

        if (Key.refListData in generatedDatas.keys() and Key.ref in column.keys()):
          self.refData[column[Key.ref]] = generatedDatas[Key.refListData]
    return generatedData
