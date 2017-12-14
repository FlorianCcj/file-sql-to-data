import json

def generateJsonFile(data, outputFile):
  """
    dump un objet json dans un fichier

    :param data: l'objet a dumper
    :type data: object
    :param outputFile: chemin vers le fichier de destination
    :type outputFile: string
  """
  try:
    with open(outputFile, 'w') as file:
      file.write(json.dumps(data, indent=2))
  except Exception as e:
    print('Erreur lors de la creation du fichier')
    print(e)
    exit(1)

def generateXmlFile(data, outputFile):
  """
    genere un xml dans un fichier

    :param data: l'objet a dumper
    :type data: object
    :param outputFile: chemin vers le fichier de destination
    :type outputFile: string
  """
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
    print('Probleme rencontre lors de l\'ecriture...')
    exit(1)

def generateSqlFile(data, outputFile):
  """
    passe un fichier en requete sql et le print dans un fichier

    :param data: l'objet a dumper
    :type data: object
    :param outputFile: chemin vers le fichier de destination
    :type outputFile: string
  """
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

def generateTxtFileFromArray(data, outputFile):
  """
    dump un array json dans un fichier

    :param data: l'array a dumper
    :type data: array
    :param outputFile: chemin vers le fichier de destination
    :type outputFile: string
  """
  fichier = open(outputFile, "w")
  eolSymbole = '\n'
  
  try:
    for lign in data:
      fichier.write(lign) 
      fichier.write(eolSymbole)
  except:
    print('Erreur lors de l ecriture de tableau dans un fichier')
    exit(1)

  fichier.close()

def generateTxtFileFromObject(data, outputFile):
  """
    ecrit un objet ligne par ligne dans un fichier

    :param data: l'objet a dumper
    :type data: object
    :param outputFile: chemin vers le fichier de destination
    :type outputFile: string
  """
  fichier = open(outputFile, "w")
  eolSymbole = '\n'
  
  try:
    for i in range(len(data)):
      fichier.write(data[i]) 
      fichier.write(eolSymbole)
  except:
    print('Erreur lors de l ecriture de tableau dans un fichier')
    exit(1)

  fichier.close()
