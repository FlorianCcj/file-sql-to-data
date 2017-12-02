import json

def generateJsonFile(data, outputFile):
  try:
    with open(outputFile, 'w') as file:
      file.write(json.dumps(data, indent=2))
  except Exception as e:
    print('Erreur lors de la creation du fichier')
    print(e)
    exit(1)