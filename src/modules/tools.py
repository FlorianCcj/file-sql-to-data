
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