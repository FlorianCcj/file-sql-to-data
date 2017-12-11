import random
import Key
from faker import Faker
fake = Faker()

class DataGenerator:
  def __init__(self):
    self.schemaInit = {}
    self.schema_to_work = {}
    self.timeout = 50
    self.defaultNumberOfDataToCreate = 10

    self.data = {}
    self.tableNameGeneratedData = []
    self.uniqueDatas = {}
    self.primaryColumn = {}

    
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
      numberOfRow = dataSchema[tableName][Key.defaultNumberOfDataToCreate]
      for i in range(numberOfRow):
        tableData.append(self.generateNewRow(dataSchema[tableName][columnsKey], numberOfRow, i, tableName))
        newEntreePrimary = self.primaryColumnKeeper(tableName, tableData[i])
        if (primaryKeyKey not in self.uniqueDatas[tableName].keys()):
          self.uniqueDatas[tableName][primaryKeyKey] = []
        timeout = 0
        while (newEntreePrimary in self.uniqueDatas[tableName][primaryKeyKey] and timeout < self.timeout):
          timeout += 1
          del tableData[i]
          tableData.append(self.generateNewRow(dataSchema[tableName][columnsKey], numberOfRow, i, tableName))
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
    refKey = Key.referenceFile
    if (column.has_key(refKey)):
      print(column[refKey])
      if (not self.refData.has_key(column[refKey])):
        self.refData[column[refKey]] = self.readJsonFile(column[refKey])
      if (self.refData[column[refKey]]):
        refRecupData = random.choice(self.refData[column[refKey]])
      else:
        refRecupData = None
    return refRecupData
