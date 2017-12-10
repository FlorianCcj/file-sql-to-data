
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