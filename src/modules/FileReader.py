import json

def readFileSql(inputFile):
  """
    concatene un fichier en une seul string

    :param inputFile: le fichier a lire
    :type inputFile: string

    :return: une string avec toutes les lignes misent bout a bout
    :rtype: string
  """
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

def readJsonFile(jsonFile):
  """
    recupere un json d un fichier pour le retourner en objet

    :param inputFile: le fichier a lire
    :type inputFile: string

    :return: l objet sortit du fichier
    :rtype: object
  """
  print('### Lecture du fichier JSON ###')
  try:
    with open(jsonFile, 'r') as file:
      dataSchema = json.load(file)
  except Exception as e:
    print('Erreur lors de la lecture du fichier')
    print(e)
    exit(1)
  return dataSchema