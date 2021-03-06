# -*- coding: utf-8 -*-
#!/usr/bin/python

import re
import json
import argparse
import random
from lxml import etree
from faker import Faker
fake = Faker()

# fake.seed(12) # avec une meme seed on a les meme valeur random
# fake.name()
# fake.adress()
# fake.first_name()
# fake.last_name()
# fake.text()
# fake.sentence()
# fake.credit_card_number()
# fake.military_ship()
# fake.hex_color()
# fake.catch_phrase_verb()
# fake.company()

parser = argparse.ArgumentParser()
parser.add_argument('-if','--inputFile', help = 'SQL file schema to generate data')
parser.add_argument('-of','--outputFile', help = 'json file which resume the schema')
parser.add_argument('-jf','--jsonFile', help = 'json file which resume the schema to generate data')
parser.add_argument('-y','--yes', help = 'permit to ignore the json verification and use default value')
args = parser.parse_args()

class DataGenerator:
  def __init__(self, inputFile = None, jsonFile = None, type = 'csv'):
    self.inputFile = inputFile
    self.jsonFile = jsonFile
    
    self.createRequest = {}
    self.request = ''
    
    self.dataSchema = {}
    self.data = {}
    self.tableNameGeneratedData = []

    self.unique = {}
    self.uniqueDatas = {}
    self.primaryColumn = {}
    self.foreignKeys = {}
    self.foreignKeysData = {}
    
    self.refData = {}

    self.timeout = 50
    self.defaultNumberToCreate = 10

  def launch(self):
    print('### Lancement de la generation de donnees ###')
    if (self.jsonFile):
      self.dataSchema = self.readJsonFile(self.jsonFile)
      self.primaryColumn = self.extractPrimaryColumn(self.dataSchema);
      self.data = self.generateDatas(self.dataSchema)
      self.data = self.generateForeignKey(self.dataSchema, self.data)
      return self.data
    elif (self.inputFile):
      # recuperation de la donnee
      self.request = self.readFileSql(self.inputFile)
      # extraction de chaque requete
      # extraction des columns
      self.dataSchema = self.extractCreateRequests(self.request)
      # recuperation des primary
      # creation des donnees
      self.foreignKeys = self.extractForeignKey(self.request);
      self.dataSchema = self.mergeSchemaAndForeignKeys(self.dataSchema, self.foreignKeys)
      if (not self.dataSchema):
        print ('fichier impossible a parser, verifier qu\'il sagit bien d\'un fichier sql en entree')
      return self.dataSchema

  def readFileSql(self, inputFile):
    print('### Lecture du fichier SQL ###')
    totalRequest = ''
    try:
      with open(inputFile, 'r') as file:
        for line in file:
          totalRequest += line 
    except FileNotFoundError as e:
      print('Le fichier {} n\'existe pas !'.format(e.filename))
      exit(1)
    except PermissionError as e:
      print('Droit de lecture absent sur le fichier {} !'.format(e.filename))
      exit(2)
    except Exception as e:
      print('Une erreur a empeche l\'ouverture du fichier : {}'.format(e.strerror))
      exit(3)
    return totalRequest

  def readJsonFile(self, jsonFile):
    print('### Lecture du fichier JSON ###')
    try:
      with open(jsonFile, 'r') as file:
        dataSchema = json.load(file)
    except Exception as e:
      print('Erreur lors de la lecture du fichier')
      print(e)
      exit(1)
    return dataSchema

  def extractCreateRequests(self, request):
    print('### Recuperation des differente CREATE TABLE ###')
    data = {}
    tablePattern = r'CREATE TABLE ([^ ]+) \((.+)\).*;'
    tableMatch = re.findall(tablePattern, request)
    for table in tableMatch:

      tableName = table[0].strip()
      tableRequest = table[1]
      data[tableName] = {}
      data[tableName]['columns'] = {}
      data[tableName]['numberToCreate'] = self.defaultNumberToCreate
      columnPattern = r'(?!\([^ )]+),(?! ?[^ (]+\))'
      columnMatch = re.split(columnPattern, tableRequest) 
      data[tableName]['columns'] = self.extractColumnsFromCreateRequest(columnMatch, tableName)
    return data

  def extractColumnsFromCreateRequest(self, columnRequestTable, tableName):
    print('### Recuperation des columns au sein de la CREATE TABLE %s ###'% tableName)
    columnPattern = r'([^ ]+) ([^ (]+)(?: ?\(([^)]+)\))? ?(.+)?'
    columnData = {}
    for columnRequest in columnRequestTable:
      match = re.findall(columnPattern, columnRequest)
      if match:
        columName = match[0][0].strip()
        columnData[columName] = {} if (not columnData.has_key(columName)) else columnData[columName]
        if (columnRequest.lower().strip().find('primary') != -1): # est-ce qu il faudrait pas le mettre sur column au lieu de columnName
          del columnData[columName]
          patternPrimaryKey = r'PRIMARY KEY ?\((.+)\)'
          matchPrimaryColumn = re.findall(patternPrimaryKey, columnRequest)
          if(len(matchPrimaryColumn) > 0):
            primaryKeys = matchPrimaryColumn[0].split(",")
            for key in primaryKeys:
              cleanKey = key.strip()
              if (not columnData.has_key(cleanKey)):
                columnData[cleanKey] = {}
              columnData[cleanKey]['primary'] = True
        elif (columName.lower().strip().find('index') != -1):
          del columnData[columName]
          pass
          # todo
        elif (columnRequest.lower().strip().find('unique') != -1):
          uniquePattern = r'\((.*)\)'
          matchUnique = re.findall(uniquePattern, columnRequest)
          uniqueColumnName = matchUnique[0].strip()
          if (not self.unique.has_key(tableName)):
            self.unique[tableName] = {}
          if (not self.unique[tableName].has_key(uniqueColumnName)):
            self.unique[tableName][uniqueColumnName] = {}
          self.unique[tableName][uniqueColumnName]['unique'] = True
          del columnData[columName]
          pass
        else:
          columnType = match[0][1]
          columnData[columName]['name'] = columName
          columnData[columName]['type'] = columnType if columnType else None
          columnData[columName]['nullable'] = (columnRequest.lower().find('not null') != -1)
          if (not columnData[columName].has_key('unique')):
            columnData[columName]['unique'] = False
          if (not columnData[columName].has_key('primary')):
            columnData[columName]['primary'] = False
          try:
            columnData[columName]['size'] = int(match[0][2])
          except Exception as e:
            columnData[columName]['size'] = None  
    columnData = self.isThisTableSColumnsUnique(tableName, columnData, self.unique)
    return columnData

  def extractForeignKey(self, request):
    print('### Recuperation des differente ALTER TABLE ###')
    data = {}
    # besoin de recuperer table et column de destination table et column source
    foreignKeyPattern = r'ALTER TABLE ([^ ]+) ADD CONSTRAINT FK\_[^ ]+ FOREIGN KEY \(([^ ]+)\) REFERENCES ([^ ]+) \(([^ ]+)\)'
    foreignKeysMatch = re.findall(foreignKeyPattern, request)
    # print (foreignKeysMatch)
    for foreignKey in foreignKeysMatch:
      # print(foreignKey)
      # print('----------------------------------------------')
      destTableName = foreignKey[0].strip()
      destColumName = foreignKey[1].strip()
      srcTableName = foreignKey[2].strip()
      srcColumName = foreignKey[3].strip()
      data[destTableName] = {'columns': {}} if (not data.has_key(destTableName)) else data[destTableName]
      data[destTableName]['columns'][destColumName] = {'type': 'foreign key', 'foreignKey': {'table': srcTableName, 'column': srcColumName}}
    return data

  def mergeSchemaAndForeignKeys(self, dataSchema, foreignKeys):
    data = dataSchema;
    for tableName in dataSchema:
      if foreignKeys.has_key(tableName):
        for columnName in dataSchema[tableName]['columns']:
          if foreignKeys[tableName]['columns'].has_key(columnName):
            for dataSColumn in foreignKeys[tableName]['columns'][columnName]:
              data[tableName]['columns'][columnName][dataSColumn] = foreignKeys[tableName]['columns'][columnName][dataSColumn]
    return dataSchema

  def isThisTableSColumnsUnique(self, tableName, tableColumns, uniqueTable):
    print('### Recuperation des colonnes Uniques ###')
    for column in tableColumns:
      if (uniqueTable.has_key(tableName)):
        if uniqueTable[tableName].has_key(column):
          tableColumns[column.strip()]['unique'] = True
        else:
          tableColumns[column.strip()]['unique'] = False
      else:
        tableColumns[column.strip()]['unique'] = False
    return tableColumns
      # check il il est dans le tablea self.unique

  def extractPrimaryColumn(self, dataSchema):
    print('### Recuperation des primary key ###')
    primaryColumn = {}
    for tableName in dataSchema:
      tableName = tableName.strip()
      primaryColumn[tableName] = [] 
      for columName in dataSchema[tableName]['columns']:
        if dataSchema[tableName]['columns'][columName.strip()].has_key('primary') and dataSchema[tableName]['columns'][columName.strip()]['primary']:
          primaryColumn[tableName].append(columName)
      
    return primaryColumn

  def generateDatas(self, dataSchema):
    print('### Generation de la data ###')
    data = {}
    for tableName in dataSchema:
      data[tableName] = self.generateTableData(tableName, dataSchema)
    return data

  def generateForeignKey(self, dataSchema, data):
    print('### Liaison de la data ###')
    newData = data
    for tableName in dataSchema:
      for columnName in dataSchema[tableName]['columns']:
        if (dataSchema[tableName]['columns'][columnName]['type'] == 'foreign key' and dataSchema[tableName]['columns'][columnName].has_key('foreignKey')):
          srcTableName = dataSchema[tableName]['columns'][columnName]['foreignKey']['table']
          srcColumnName = dataSchema[tableName]['columns'][columnName]['foreignKey']['column']
          if (not self.foreignKeysData.has_key(srcTableName)):
            self.foreignKeysData[srcTableName] = {}
          if (not self.foreignKeysData[srcTableName].has_key(srcColumnName)):
            self.foreignKeysData[srcTableName][srcColumnName] = []
          if (self.foreignKeysData[srcTableName][srcColumnName] == []):
            self.foreignKeysData[srcTableName][srcColumnName] = self.generateForeignKeyData(srcTableName, srcColumnName)
          for numerousOfData in range(0, len(data[tableName])-1):
            timeout = 0
            transformData = newData[tableName][numerousOfData]
            transformData[columnName] = self.generateForeignKeyColumn(self.foreignKeysData[srcTableName][srcColumnName])
            if (self.primaryColumn.has_key(tableName) and columnName in self.primaryColumn[tableName]):
              newEntreePrimary = self.primaryColumnKeeper(tableName, transformData) 
            # todo : a factoriser dans une fonction
              while (newEntreePrimary in self.uniqueDatas[tableName]['primaryKey'] and timeout < self.timeout):
                timeout += 1
                transformData[columnName] = self.generateForeignKeyColumn(self.foreignKeysData[srcTableName][srcColumnName])
                newEntreePrimary = self.primaryColumnKeeper(tableName, transformData)
              self.uniqueDatas[tableName]['primaryKey'].append(newEntreePrimary)
            newData[tableName][numerousOfData] = transformData
            if (timeout == 50):
              print "[error] [primary generation FK] Tentative de generation dans la table %s a echoue a cause de la PRIMARY KEY constraint" % tableName
    return newData

  def generateForeignKeyColumn(self, dataToRand):
    randomNum = random.randint(0, len(dataToRand)-1)
    return dataToRand[randomNum]

  def generateForeignKeyData(self, tableName, columnName):
    dataForForeignKeys = [];
    if (self.data.has_key(tableName)):
      for data in self.data[tableName]:
        if (data.has_key(columnName)):
          dataForForeignKeys.append(data[columnName])
        else:
          print('[ERREUR][FK] la foreign key %s(%s) n existe pas'%tableName, columnName)
    else:
      print('[ERREUR] [FK] la table %s(%s) pour recuperer la foreign key n existe pas'%tableName, columnName)   
    return dataForForeignKeys

  def generateTableData(self, tableName, dataSchema):
    if (not tableName in self.tableNameGeneratedData):
      tableData = []
      numberOfRow = dataSchema[tableName]['numberToCreate']
      for i in range(numberOfRow):
        tableData.append(self.generateNewRow(dataSchema[tableName]['columns'], numberOfRow, i, tableName))
        newEntreePrimary = self.primaryColumnKeeper(tableName, tableData[i])
        if (not self.uniqueDatas[tableName].has_key('primaryKey')):
          self.uniqueDatas[tableName]['primaryKey'] = []
        timeout = 0
        while (newEntreePrimary in self.uniqueDatas[tableName]['primaryKey'] and timeout < self.timeout):
          timeout += 1
          del tableData[i]
          tableData.append(self.generateNewRow(dataSchema[tableName]['columns'], numberOfRow, i, tableName))
          newEntreePrimary = self.primaryColumnKeeper(tableName, tableData[i])
        self.uniqueDatas[tableName]['primaryKey'].append(newEntreePrimary)
        if (timeout == 50):
          print "[error] [primary generation] Tentative de generation dans la table %s a echoue a cause de la PRIMARY KEY constraint" % tableName
      self.tableNameGeneratedData.append(tableName)
      return tableData
    else:
      return self.data[tableName]

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
    newRow = {}
    for columnName in columns:
      if (not self.uniqueDatas.has_key(tableName)):
        self.uniqueDatas[tableName] = {}
      if (not self.uniqueDatas[tableName].has_key(columnName)):
        self.uniqueDatas[tableName][columnName] = {}
        self.uniqueDatas[tableName][columnName]['unique'] = []

      newData = self.generateDataColumn(columns[columnName], numberOfRow, id = id)
      if (columns[columnName]['unique']):
        timeout = 0
        while ((newData in self.uniqueDatas[tableName][columnName]['unique']) and (timeout < self.timeout)) :
          newData = self.generateDataColumn(columns[columnName], numberOfRow, id = id)
          timeout += 1
        if timeout == self.timeout:
          # todo : comprendre pourquoi ca marche pas 
          # print("[error] [unique generation] Tentative de generation de donnees unique dans la table %s pour la colonne %s echoue" %tableName , columnName)
          print("[error] [unique generation] Tentative de generation de donnees unique dans la table pour la colonne echoue")

      self.uniqueDatas[tableName][columnName]['unique'].append(newData)
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
    if (column.has_key('refFile')):
      print(column['refFile'])
      if (not self.refData.has_key(column['refFile'])):
        self.refData[column['refFile']] = self.readJsonFile(column['refFile'])
      if (self.refData[column['refFile']]):
        refRecupData = random.choice(self.refData[column['refFile']])
      else:
        refRecupData = None
    return refRecupData
      # si les donnees interne n'ont pas la cle column.refFile
      #   ouvrir
      #   recuperer les donnees
      #   les mettre dans les donnees interne
      # si les donnees internes on la cle et qu il n est pas vide
      #   recurer une donnee aleatoire dans les data
      # sinon retourner 'null'
      
class FileCreator:
  def __init__(self, outputFile = None, extension = None, data = {}, dataType = None):
    self.extensionFile = extension
    self.data = data
    self.outputFile = {}
    if (not outputFile):
      if (not dataType):
        self.outputFile['name'] = 'default-output-file'
        self.outputFile['ext'] = 'txt'
        self.outputFile['total'] = self.outputFile['name']+'.'+self.outputFile['ext']
      else:
        self.outputFile['name'] = 'default-output-file'
        self.outputFile['ext'] = dataType
        self.outputFile['total'] = self.outputFile['name']+'.'+self.outputFile['ext']
    else:
        self.outputFile['total'] = outputFile
    self.launch()

  def launch(self):
    self.chooseFormat(self.extensionFile)

  def chooseFormat(self, extension = None):
    if (extension == 'csv'):
      pass
    elif (extension == 'json'):
      self.generateJsonFile(self.data, self.outputFile['total'])
    else:
      # WIP
      self.generateJsonFile(self.data, self.outputFile['total']+'.json')
      self.generateXmlFile(self.data, self.outputFile['total']+'.xml')
      self.generateSqlFile(self.data, self.outputFile['total']+'.sql')

  def generateJsonFile(self, data, outputFile):
    try:
      with open(outputFile, 'w') as file:
        file.write(json.dumps(data, indent=2))
    except Exception as e:
      print('Erreur lors de la creation du fichier')
      print(e)
      exit(1)

  def generateXmlFile(self, data, outputFile):
    root = etree.Element('data')
    try:
      for tableName in data:
        table = etree.SubElement(root, tableName)
        for elementOfTable in data[tableName]:
          elementOfXml = etree.SubElement(table, 'element')
          if(elementOfTable.has_key('id')):
            elementOfXml.set('id', str(elementOfTable['id']))
          columnOfXml = None
          for columnOfTable in elementOfTable:
            columnOfXml = etree.SubElement(elementOfXml, columnOfTable).text = str(elementOfTable[columnOfTable])
    except:
      print('Erreur de formmat pour la creation de format Xml')
      exit(1)
    try:
      with open(outputFile, 'w') as fic:
        fic.write(etree.tostring(root, pretty_print=True).decode('utf-8'))
    except IOError:
      print('Problème rencontre lors de l\'ecriture...')
      exit(1)

  def generateSqlFile(self, data, outputFile):
    fichier = open(outputFile, "w")
    eolSymbole = '\n'
    
    try:
      for tableName in data:
        beginInsertValueLign = 'INSERT INTO ' + str(tableName) + ' (' 
        for columnName in data[tableName][0]:
          beginInsertValueLign = beginInsertValueLign + columnName + ', '
        beginInsertValueLign = beginInsertValueLign[:len(beginInsertValueLign)-2] + ') VALUES '
        fichier.write(beginInsertValueLign) 
        fichier.write(eolSymbole)

        endInsertValueLignInitial = '('
        for element in data[tableName]:
          endInsertValueLign = endInsertValueLignInitial
          for column in element:
            endInsertValueLign = endInsertValueLign + str(element[column]) + ', '
          endInsertValueLign = endInsertValueLign[:len(endInsertValueLign)-2] + ')'
          
          fichier.write(endInsertValueLign) 
          fichier.write(eolSymbole)
        fichier.write(';')
        fichier.write(eolSymbole)
        fichier.write(eolSymbole)
    except:
      print('Erreur de formmat pour la creation de format Sql')
      exit(1)


    fichier.close()

if __name__ == '__main__':
  if (args.jsonFile):
    outputFile = args.outputFile if args.outputFile else './data.json'
    launcher = DataGenerator(jsonFile = args.jsonFile)
    data = launcher.launch()
    maker = FileCreator(data = data, outputFile = outputFile)
  elif (args.inputFile):
    outputFile = args.outputFile if args.outputFile else './data-schema.json'
    launcher = DataGenerator(inputFile = args.inputFile)
    dataSchema = launcher.launch()
    maker = FileCreator(data = dataSchema, outputFile = outputFile)
  else:
    parser.print_help()



def reflexion():
  '''
    referentiel:
      type: 
        ref
      data: fichier

    generation csv
    generation sql
  '''
  pass
