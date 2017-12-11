import random
import Key
from faker import Faker
fake = Faker()
import FileReader

def update_object(object_init, object_update_container):
  new_object = object_init
  if isinstance(new_object, type({})) and isinstance(object_update_container, type({})):
    for element in object_update_container:
      if element not in new_object:
        new_object[element] = object_update_container[element]
      else:
        new_object[element] = update_object(new_object[element], object_update_container[element])
  else:
    # todo : faire le cas des tableau
    new_object = object_update_container
  return new_object

def fromStringArrayToObject(objectToGenerate):
  pass

def fromDataToObjectToPrint(data):
  objectToPrint = {}
  lignToPrint = 0
  for tableName in data:
    beginInsertValueLign = 'INSERT INTO `' + str(tableName) + '` (' 
    for columnName in data[tableName][0]:
      beginInsertValueLign = beginInsertValueLign + '`' + str(columnName) + '`, '
    beginInsertValueLign = beginInsertValueLign[:len(beginInsertValueLign)-2] + ') VALUES '
    objectToPrint[lignToPrint] = beginInsertValueLign 
    lignToPrint += 1

    endInsertValueLignInitial = '('
    for element in data[tableName]:
      endInsertValueLign = endInsertValueLignInitial
      for column in element:
        endInsertValueLign = endInsertValueLign + str(element[column]) + ', '
      endInsertValueLign = endInsertValueLign[:len(endInsertValueLign)-2] + '),'
      objectToPrint[lignToPrint] = endInsertValueLign
      lignToPrint += 1
    objectToPrint[lignToPrint-1] = objectToPrint[lignToPrint-1][:len(endInsertValueLign)-1]
    objectToPrint[lignToPrint] = ';'
    lignToPrint += 1  
  return objectToPrint

def generateRandomData(type, maxNumber = 10, id = 0, file = '', refData = []):
    # print('### Generation d une column d une entree ###')
    generatedData = None
    generatedDatas = {}
    if (type):
      if type.strip().lower() == 'varchar':
        generatedData = fake.sentence()
      elif type.strip().lower().find('varchar') != -1:
        generatedData = fake.sentence()
      elif type.strip().lower() == 'LONGTEXT'.lower():
        generatedData = fake.paragraph()
      elif type.strip().lower() == 'tinyint':
        generatedData = fake.boolean()
      elif type.strip().lower() == 'boolean':
        generatedData = fake.boolean()
      elif type.strip().lower().find('tinyint') != -1:
        generatedData = fake.boolean()
      elif type.strip().lower() == 'int':
        generatedData = random.randint(1, maxNumber)
      elif type.strip().lower().find('int') != -1:
        generatedData = random.randint(1, maxNumber)
      elif type.strip().lower() == 'name':
        generatedData = fake.name()
      elif type.strip().lower() == 'adress':
        generatedData = fake.adress()
      elif type.strip().lower() == 'first_name':
        generatedData = fake.first_name()
      elif type.strip().lower() == 'last_name':
        generatedData = fake.last_name()
      elif type.strip().lower() == 'credit_card_number':
        generatedData = fake.credit_card_number()
      elif type.strip().lower() == 'military_ship':
        generatedData = fake.military_ship()
      elif type.strip().lower() == 'color':
        generatedData = fake.hex_color()
      elif type.strip().lower() == 'catch_phrase_verb':
        generatedData = fake.catch_phrase_verb()
      elif type.strip().lower() == 'company':
        generatedData = fake.company()
      elif type.strip().lower() == 'ref':
        generatedDatas = self.takeRefData(file, refData)
      elif type.strip().lower() == 'id':
        generatedData = id+1
      else:
        generatedData = None
    if (Key.refListData not in generatedDatas.keys()):
      generatedDatas = {Key.data: generatedData, Key.refListData: None}
    return generatedDatas

def takeRefData(self, file, refData):
    refRecupData = None
    if(not len(refData) > 0):
      refData = FileReader.readJsonFile(file)    
    if(len(refData) > 0):
      refRecupData = random.choice(refData)
    return {Key.data: refRecupData, Key.refListData: refData} 