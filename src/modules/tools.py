import random
import Key
import FileReader
from faker import Faker
fake = Faker()

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


def from_strings_array_to_objects(object_to_generate, array_of_string, idMin = 0):
    # pas gerer pour l instant
    for name in array_of_string:
        new_object = {}
        for column_name in object_to_generate:
            new_object[column_name] = generate_random_data(object_to_generate[column_name[Key.type]])
            pass
        pass
    pass


def from_data_to_object_to_print(data):
    object_to_print = {}
    lign_to_print = 0
    for table_name in data:
        begin_insert_value_lign = 'INSERT INTO `' + str(table_name) + '` (' 
        for column_name in data[table_name][0]:
            begin_insert_value_lign = begin_insert_value_lign + '`' + str(column_name) + '`, '
        begin_insert_value_lign = begin_insert_value_lign[:len(begin_insert_value_lign)-2] + ') VALUES '
        object_to_print[lign_to_print] = begin_insert_value_lign 
        lign_to_print += 1

        end_insert_value_lign_initial = '('
        for element in data[table_name]:
            end_insert_value_lign = end_insert_value_lign_initial
            for column in element:
                end_insert_value_lign = end_insert_value_lign + str(element[column]) + ', '
            end_insert_value_lign = end_insert_value_lign[:len(end_insert_value_lign)-2] + '),'
            object_to_print[lign_to_print] = end_insert_value_lign
            lign_to_print += 1
        object_to_print[lign_to_print-1] = object_to_print[lign_to_print-1][:len(end_insert_value_lign)-1]
        object_to_print[lign_to_print] = ';'
        lign_to_print += 1  
    return object_to_print


def from_data_to_ordered_object_to_print(data, order_of_table):
    object_to_print = {}
    lign_to_print = 0

    for i in range(len(order_of_table)):
        table_name = order_of_table[i]
        begin_insert_value_lign = 'INSERT INTO `' + str(table_name) + '` (' 
        for column_name in data[table_name][0]:
            begin_insert_value_lign = begin_insert_value_lign + '`' + str(column_name) + '`, '
        begin_insert_value_lign = begin_insert_value_lign[:len(begin_insert_value_lign)-2] + ') VALUES '
        object_to_print[lign_to_print] = begin_insert_value_lign 
        lign_to_print += 1

        end_insert_value_lign_initial = '('
        for element in data[table_name]:
            end_insert_value_lign = end_insert_value_lign_initial
            for column in element:
                end_insert_value_lign = end_insert_value_lign + str(element[column]) + ', '
            end_insert_value_lign = end_insert_value_lign[:len(end_insert_value_lign)-2] + '),'
            object_to_print[lign_to_print] = end_insert_value_lign
            lign_to_print += 1
        object_to_print[lign_to_print-1] = object_to_print[lign_to_print-1][:len(end_insert_value_lign)-1]
        object_to_print[lign_to_print] = ';'
        lign_to_print += 1
    if(not len(data) == len(order_of_table)):
        print('//!\\\\ Attention il y a moins de table triees que de table de donnee')  
    return object_to_print


def generate_random_data(type, max_number = 10, id = 0, file = '', ref_data = []):
    # print('### Generation d une column d une entree ###')
    generated_data = None
    generated_datas = {}
    if (type):
        if type.strip().lower() == 'varchar':
            generated_data = fake.sentence()
        elif type.strip().lower().find('varchar') != -1:
            generated_data = fake.sentence()
        elif type.strip().lower() == 'LONGTEXT'.lower():
            generated_data = fake.paragraph()
        elif type.strip().lower() == 'tinyint':
            generated_data = fake.boolean()
        elif type.strip().lower() == 'boolean':
            generated_data = fake.boolean()
        elif type.strip().lower().find('tinyint') != -1:
            generated_data = fake.boolean()
        elif type.strip().lower() == 'int':
            generated_data = random.randint(1, max_number)
        elif type.strip().lower().find('int') != -1:
            generated_data = random.randint(1, max_number)
        elif type.strip().lower() == 'name':
            generated_data = fake.name()
        elif type.strip().lower() == 'adress':
            generated_data = fake.adress()
        elif type.strip().lower() == 'first_name':
            generated_data = fake.first_name()
        elif type.strip().lower() == 'last_name':
            generated_data = fake.last_name()
        elif type.strip().lower() == 'credit_card_number':
            generated_data = fake.credit_card_number()
        elif type.strip().lower() == 'military_ship':
            generated_data = fake.military_ship()
        elif type.strip().lower() == 'color':
            generated_data = fake.hex_color()
        elif type.strip().lower() == 'catch_phrase_verb':
            generated_data = fake.catch_phrase_verb()
        elif type.strip().lower() == 'company':
            generated_data = fake.company()
        elif type.strip().lower() == 'ref':
            generated_datas = self.take_ref_data(file, ref_data)
        elif type.strip().lower() == 'id':
            generated_data = id+1
        else:
            generated_data = None
    if (Key.ref_list_data not in generated_datas.keys()):
        generated_datas = {Key.data: generated_data, Key.ref_list_data: None}
    return generated_datas


def take_ref_data(file, ref_data):
    ref_recup_data = None
    if(not len(ref_data) > 0):
        ref_data = FileReader.read_json_file(file)    
    if(len(ref_data) > 0):
        ref_recup_data = random.choice(ref_data)
    return {Key.data: ref_recup_data, Key.ref_list_data: ref_data} 


def take_one_element_in_array(data_to_rand):
    return random.choice(data_to_rand)