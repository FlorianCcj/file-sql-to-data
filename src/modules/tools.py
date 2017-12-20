import random
import Key
import FileReader
from faker import Faker
fake = Faker()

def update_object(object_init, object_update_container):
    """
        take all data in the second parameter to add or replace it in the first parameter

        :param object_init: the object which is the base of the copy
        :type object_init: object
        :param object_update_containert: the object where we are getting all atribut to add them to the base object
        :type object_update_container: object

        :return: the fusion of both object
        :rtype: object
    """
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
    """
        take a list of string to generate object with it
    """
    # pas gerer pour l instant
    for name in array_of_string:
        new_object = {}
        for column_name in object_to_generate:
            new_object[column_name] = generate_random_data(object_to_generate[column_name[Key.type]])
            pass
        pass
    pass


def from_data_to_object_to_print(data):
    """
        generate an object with number as key, and a lign to write in the file as value

        :param data: database in one object
        :type data: object with key tablenam an value array of table value

        :return: object with all lign to write
        :rtype: object 
    """
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
    """
        generate an object with number as key, and a lign to write in the file as value

        :param data: database in one object
        :type data: object with key tablenam an value array of table value
        :param order_of_table: order of the table to know which table we have to write in first
        :type order_of_table: object

        :return: object with all lign to write
        :rtype: object 
    """
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
        print('[error][from data to lign]//!\\\\ Attention il y a moins de table triees que de table de donnee')  
    return object_to_print


def generate_random_data(type, max_number = 10, id = 0, file = '', ref_data = []):
    """
        generate random data depend on type

        :param type: type of data to generate
        :type type: string
        :param max_number: number max of the number to generate
        :type type: number
        :param id: id of the last data generated
        :type id: number
        :param file: if need to take a data in a list of value from a file
        :type file: string
        :param ref_data: if need to take a data in a list of value
        :type ref_data: array

        :return: generated data
        :rtype: string|boolean|number
    """
    generated_data = None
    generated_datas = {}
    if (type):
        ### Type classique ###
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
        ### Name ###
        elif type.strip().lower() == 'name':
            generated_data = fake.name()
        elif type.strip().lower() == 'name_male':
            generated_data = fake.name_male()
        elif type.strip().lower() == 'name_female':
            generated_data = fake.name_female()
        elif type.strip().lower() == 'first_name_female':
            generated_data = fake.first_name_female()
        elif type.strip().lower() == 'first_name':
            generated_data = fake.first_name()
        elif type.strip().lower() == 'last_name':
            generated_data = fake.last_name()
        ### Personnal Data ###
        elif type.strip().lower() == 'job':
            generated_data = fake.job()
        elif type.strip().lower() == 'credit_card_number':
            generated_data = fake.credit_card_number()
        elif type.strip().lower() == 'military_ship':
            generated_data = fake.military_ship()
        elif type.strip().lower() == 'catch_phrase_verb':
            generated_data = fake.catch_phrase_verb()
        elif type.strip().lower() == 'company':
            generated_data = fake.company()
        ### Place ###
        elif type.strip().lower() == 'state':
            generated_data = fake.state()
        elif type.strip().lower() == 'postalcode':
            generated_data = fake.postalcode()
        elif type.strip().lower() == 'zipcode':
            generated_data = fake.zipcode()
        elif type.strip().lower() == 'address':
            generated_data = fake.address()
        elif type.strip().lower() == 'street_address':
            generated_data = fake.street_address()
        elif type.strip().lower() == 'country':
            generated_data = fake.country()
        elif type.strip().lower() == 'city':
            generated_data = fake.city()
        ### color ###
        elif type.strip().lower() == 'color':
            generated_data = fake.hex_color()
        elif type.strip().lower() == 'color_name':
            generated_data = fake.color_name()
        ### Time ###
        elif type.strip().lower() == 'year':
            generated_data = fake.year()
        elif type.strip().lower() == 'month':
            generated_data = fake.month()
        elif type.strip().lower() == 'month_name':
            generated_data = fake.month_name()
        elif type.strip().lower() == 'day_of_week':
            generated_data = fake.day_of_week()
        elif type.strip().lower() == 'time':
            generated_data = fake.time(pattern="%H:%M:%S", end_datetime=None)
        elif type.strip().lower() == 'am_pm':
            generated_data = fake.am_pm()
        elif type.strip().lower() == 'day_of_month':
            generated_data = fake.day_of_month()
        elif type.strip().lower() == 'date':
            generated_data = fake.date(pattern="%Y-%m-%d", end_datetime=None)
        ### File ###
        elif type.strip().lower() == 'file_extension':
            generated_data = fake.file_extension(category=None)
        elif type.strip().lower() == 'file_name':
            generated_data = fake.file_name(category=None, extension=None)
        
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
    """
        take a random data in an array or a file

        :param file: file where to find a data
        :type file: string
        :param ref_data: array where to find a data
        :type ref_data: array

        :return: an object with random data choosen and list of data where to choose
        :rtype: object
    """
    ref_recup_data = None
    if(not len(ref_data) > 0):
        ref_data = FileReader.read_json_file(file)    
    if(len(ref_data) > 0):
        ref_recup_data = random.choice(ref_data)
    return {Key.data: ref_recup_data, Key.ref_list_data: ref_data} 


def take_one_element_in_array(data_to_rand):
    """
        take an element in an array

        :param data_to_rand: array where to take a random value
        :type data_to_rand: array

        :return: data from the array
        :rtype: depend on type of values in the array
    """
    return random.choice(data_to_rand)