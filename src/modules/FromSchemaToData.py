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

    
  def launcher(self, schema):
    self.schemaInit = schema
    self.completeSchema(schema)
    self.data = self.generateDatas(self.schema_to_work)

  def completeSchema(self, schema):
    """
      ajoute un numero d'order et le nombre d entite a creer dans le schema
      
      :param schema: le schema d une base de donnee genere par le script auparavant
      :type schema: todo
      
      :return: un schema avec un complement d information (ordre de generation, bombre de donnee par default a generer)
      :rtype: le meme que le schema
    """
    self.schemaInit = schema
    dataScemaOrdered = self.orderTable(schema)
    dataScemaOrderedWithNumber = self.addDefaultNumberToTableList(dataScemaOrdered)
    self.schema_to_work = dataScemaOrderedWithNumber
    return dataScemaOrderedWithNumber

  def orderTable(self, dataSchemaWithForeignKey):
    """
      ordonne les tables
        si il n'y a aucune dependance ajoute directement
        si il y a des dependance et qu elles sont deja remplis alors on ajoute
        sinon on boucle

        :param dataSchemaWithForeignKey: un schema de base de donnee
        :type dataSchemaWithForeignKey: todo

        :return: le meme schema avec un element permettant d ordonnee la creation de la donnee
        :rtype: todo
    """
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
    """
      recupere les ordres de chaque table et fait un objet avec pour indice l'ordre {1: recette-type, 2:recette}
      
      :param schema: un schema de base de donnee
      :type schema: todo

      :return: un tableau permettant de savoir l ordre de creation
      :rtype: {1: recette-type, 2:recette, n: nemetable} 
    """
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
    """
      ajoute un nombre d entite a creer par default a toute les tables dans un schema de base

      :param tableList: objet listant des tables
      :type tableList: todo

      :return: le meme objet mais avec un nouvel attribut par table pour savoir le nombre d entite a cree
    """
    tableWithNumber = {}
    for tableName in tableList:
      tableWithNumber[tableName] = self.addDefaultNumberToTable(tableList[tableName])
    return tableWithNumber

  def addDefaultNumberToTable(self, table):
    """ 
      ajoute un nombre d entite a creer dans un schema de table

      :param table: un schema d une table
      :type table: object

      :return: le meme schema avec un attribut en plus pour savoir le nombre d'entree a creer
      :rtype: object
    """
    table[Key.defaultNumberOfDataToCreate] = self.defaultNumberOfDataToCreate
    return table

  def generateDatas(self, dataSchema):
    """
      a partir d un schema d une base on genere de la donnee

      :param dataSchema: schema de base de donnee
      :type dataSchema: todo

      :return: donnee genere par table
      :rtype: liste d'objet par table {table1 : [entre1, entre2]}
    """
    print('### Generation de la data ###')
    self.schema_to_work = dataSchema if not dataSchema == self.schema_to_work else self.schema_to_work
    data = {}
    for tableName in dataSchema:
      data[tableName] = self.generateTableData(tableName)
    self.data = data
    return data

  def generateOrderedDatas(self, dataSchema, orderOfTable):
    """
      a partir d un schema d une base on genere de la donnee dans l ordre recuperer par la fonction orderTable

      :param dataSchema: schema de base de donnee
      :type dataSchema: todo
      :param orderOfTable: ordonnancement des table
      :type dataSchema: object

      :return: donnee genere par table
      :rtype: liste d'objet par table {table1 : [entre1, entre2]}
    """
    print('### Generation de la data ###')
    self.schema_to_work = dataSchema if not dataSchema == self.schema_to_work else self.schema_to_work
    data = {}
    for i in range(len(orderOfTable)):
      tableName = orderOfTable[i]
    #for tableName in dataSchema:
      if(tableName not in self.data):
        data[orderOfTable[i]] = self.generateTableData(tableName)
        self.data[tableName] = data[tableName]
    return data

  def generateTableData(self, tableName):
    """
      a partir du schema d une table on genere toute les donnees

      :param tableName: nom d une table
      :type tableName: string

      :return: liste des donnees genere pour une table
      :rtype: array 
    """
    dataSchema = self.schema_to_work
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
      return []

  def primaryColumnKeeper(self, tableName, newData):
    """
      genere a partir d'un nouvel objet
      un objet avec uniquement les columns ayant pour caracteristique 
      d etre une primary key

      :param tableName: nom de la table a gerer
      :type tableName: string
      :param newData: la nouvelle donnee generee
      :type newData: todo

      :return: un object uniquement compose de primary key

    """
    returnPrimary = None
    if (self.primaryColumn.has_key(tableName)):
      if (len(self.primaryColumn[tableName]) > 0):
        returnPrimary = {}
        for primaryColumnIterator in self.primaryColumn[tableName]:
          returnPrimary[primaryColumnIterator] = newData[primaryColumnIterator]
    return returnPrimary

  def generateNewRow(self, columns, numberOfRow, id, tableName):
    """
      genere une nouvelle entree

      :param columns: liste des colonnes d une table
      :type columns: objet d'objet de type column
      :param numberOfRow: nombre d entree theoriquement generer pour cette table 
      :type numberOfRow: int
      :param id: id de la derniere entree generer 
      :type id: int 
      :param tableName: nom de la table qui est actuellement gerer 
      :type tableName: string 

      :return: une entree

    """
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
    """
      Genere une donnee en fonction du type de la colonne

      :param column: le schema de la colonne a traite
      :param numberOfRow: nombre d entree theoriquement generer pour cette table 
      :type numberOfRow: int
      :param id: id de la derniere entree generer 
      :type id: int 

      :return: une donnee generer aleatoirement
      :rtype: str|int
    """
    foreignData = self.data
    generatedData = None
    if (column['name'] == 'id'):
      generatedData = id+1
    else:
      if (column.has_key(Key.type)):
        if column[Key.type] == Key.foreignKey:
          if Key.foreignKey in column.keys():
            foreignColumn = column[Key.foreignKey][Key.columnName]
            foreignTable = column[Key.foreignKey][Key.tableName]
            if(foreignTable not in self.data):
              self.data[foreignTable] = self.generateTableData(foreignTable)
            oneRandomElementInForeignData = tools.takeOneElementInArray(self.data[foreignTable])
            generatedData = oneRandomElementInForeignData[foreignColumn]
          else:
            print('[Error] column de type foreign key mais pas de table de destination')
            exit(1)
          #todo
        else:
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
