import random
import Key
from faker import Faker
import tools
fake = Faker()

class DataGenerator:
    def __init__(self):
        self.schema_init = {}
        self.schema_to_work = {}
        self.order_of_table = {}
        self.timeout = 50
        self.default_number_of_data_to_create = 10

        self.data = {}
        self.table_name_generated_data = []
        self.unique_datas = {}
        self.primary_column = {}
        self.ref_data = {}

    
    def launcher(self, schema):
        self.schema_init = schema
        self.complete_schema(schema)
        self.data = self.generate_datas(self.schema_to_work)

    def complete_schema(self, schema):
        """
            ajoute un numero d'order et le nombre d entite a creer dans le schema
            
            :param schema: le schema d une base de donnee genere par le script auparavant
            :type schema: todo
            
            :return: un schema avec un complement d information (ordre de generation, bombre de donnee par default a generer)
            :rtype: le meme que le schema
        """
        self.schema_init = schema
        data_schema_ordered = self.order_table(schema)
        data_schema_ordered_with_number = self.add_default_number_to_table_list(data_schema_ordered)
        self.schema_to_work = data_schema_ordered_with_number
        return data_schema_ordered_with_number

    # ce truc de merde marche pas, peut etre un else que j'ai pas mis que le est mal gerer
    def order_table(self, data_schema_with_foreign_key):
        """
            ordonne les tables
              si il n'y a aucune dependance ajoute directement
              si il y a des dependance et qu elles sont deja remplis alors on ajoute
              sinon on boucle

            :param data_schema_with_foreign_key: un schema de base de donnee
            :type data_schema_with_foreign_key: todo

            :return: le meme schema avec un element permettant d ordonnee la creation de la donnee
            :rtype: todo
        """
        columns_key = Key.columns
        type_key = Key.type
        foreign_key_key = Key.foreignkey
        table_name_key = Key.table_name
        order_key = Key.order
        timeout = self.timeout
        number_of_table = len(data_schema_with_foreign_key)
        table_already_done = []
        number_of_tableDone = len(table_already_done)
        try_time = 0
        while len(table_already_done) != number_of_table and try_time <= timeout:
            try_time += 1
            save = True
            for table_name in data_schema_with_foreign_key:
                if table_name not in table_already_done:
                    foreign_key_counter = 0
                    for column_name in data_schema_with_foreign_key[table_name][columns_key]:
                        if data_schema_with_foreign_key[table_name][columns_key][column_name][type_key] == foreign_key_key:
                            foreign_key_counter += 1
                            if table_name_key not in data_schema_with_foreign_key[table_name][columns_key][column_name][foreign_key_key].keys():
                                save = False
                            else:
                                if data_schema_with_foreign_key[table_name][columns_key][column_name][foreign_key_key][table_name_key] not in table_already_done:
                                    save = False 
                    if(foreign_key_counter == 0):
                        save = True
                    if(save == True):
                        data_schema_with_foreign_key[table_name][order_key] = len(table_already_done)
                        table_already_done.append(table_name)
                        try_time = 0
            number_of_tableDone = len(table_already_done)
        if (try_time == timeout):
            print('[Erreur][order] erreur lors de l ordonnancement des tables, l une d elle a une foreign key qui n existe pas')
        return data_schema_with_foreign_key

    def from_schema_to_order(self, schema):
        """
            recupere les ordres de chaque table et fait un objet avec pour indice l'ordre {1: recette-type, 2:recette}
            
            :param schema: un schema de base de donnee
            :type schema: todo

            :return: un tableau permettant de savoir l ordre de creation
            :rtype: {1: recette-type, 2:recette, n: nemetable} 
        """
        order_of_table = {}
        for table_name in schema:
            if (Key.order in schema[table_name]):
                order_of_table[schema[table_name][Key.order]] = table_name
            else:
                if (Key.nonorder not in order_of_table):
                    order_of_table[Key.nonorder] = []
                order_of_table[Key.nonorder].append(table_name)
        self.order_of_table = order_of_table
        return order_of_table

    def add_default_number_to_table_list(self, table_list):
        """
            ajoute un nombre d entite a creer par default a toute les tables dans un schema de base

            :param table_list: objet listant des tables
            :type table_list: todo

            :return: le meme objet mais avec un nouvel attribut par table pour savoir le nombre d entite a cree
        """
        table_with_number = {}
        for table_name in table_list:
            table_with_number[table_name] = self.add_default_number_to_table(table_list[table_name])
        return table_with_number

    def add_default_number_to_table(self, table):
        """ 
            ajoute un nombre d entite a creer dans un schema de table

            :param table: un schema d une table
            :type table: object

            :return: le meme schema avec un attribut en plus pour savoir le nombre d'entree a creer
            :rtype: object
        """
        table[Key.default_number_of_data_to_create] = self.default_number_of_data_to_create
        return table

    def generate_datas(self, data_schema):
        """
            a partir d un schema d une base on genere de la donnee

            :param data_schema: schema de base de donnee
            :type data_schema: todo

            :return: donnee genere par table
            :rtype: liste d'objet par table {table1 : [entre1, entre2]}
        """
        print('### Generation de la data ###')
        self.schema_to_work = data_schema if not data_schema == self.schema_to_work else self.schema_to_work
        data = {}
        for table_name in data_schema:
            data[table_name] = self.generate_table_data(table_name)
        self.data = data
        return data

    def generate_ordered_datas(self, data_schema, order_of_table):
        """
            a partir d un schema d une base on genere de la donnee dans l ordre recuperer par la fonction order_table

            :param data_schema: schema de base de donnee
            :type data_schema: todo
            :param order_of_table: ordonnancement des table
            :type data_schema: object

            :return: donnee genere par table
            :rtype: liste d'objet par table {table1 : [entre1, entre2]}
        """
        print('### Generation de la data ###')
        self.schema_to_work = data_schema if not data_schema == self.schema_to_work else self.schema_to_work
        data = {}
        for i in range(len(order_of_table)):
            table_name = order_of_table[i]
        #for table_name in data_schema:
            if(table_name not in self.data):
                data[order_of_table[i]] = self.generate_table_data(table_name)
                self.data[table_name] = data[table_name]
        return data

    def generate_table_data(self, table_name):
        """
            a partir du schema d une table on genere toute les donnees

            :param table_name: nom d une table
            :type table_name: string

            :return: liste des donnees genere pour une table
            :rtype: array 
        """
        data_schema = self.schema_to_work
        primarykey_key = Key.primarykey
        columns_key = Key.columns
        final_timeout = self.timeout
        if (not table_name in self.table_name_generated_data):
            table_data = []
            number_of_row_to_create = data_schema[table_name][Key.default_number_of_data_to_create]
            for i in range(number_of_row_to_create):
                table_data.append(self.generate_new_row(data_schema[table_name][columns_key], number_of_row_to_create, i, table_name))
                new_entree_primary = self.primary_column_keeper(table_name, table_data[i])
                if (primarykey_key not in self.unique_datas[table_name].keys()):
                    self.unique_datas[table_name][primarykey_key] = []
                timeout = 0
                while (new_entree_primary in self.unique_datas[table_name][primarykey_key] and timeout < self.timeout):
                    timeout += 1
                    del table_data[i]
                    table_data.append(self.generate_new_row(data_schema[table_name][columns_key], number_of_row_to_create, i, table_name))
                    new_entree_primary = self.primary_column_keeper(table_name, table_data[i])
                self.unique_datas[table_name][primarykey_key].append(new_entree_primary)
                if (timeout == final_timeout):
                    print "[error] [primary generation] Tentative de generation dans la table %s a echoue a cause de la PRIMARY KEY constraint" % table_name
            self.table_name_generated_data.append(table_name)
            return table_data
        else:
            return []

    def primary_column_keeper(self, table_name, new_data):
        """
            genere a partir d'un nouvel objet
            un objet avec uniquement les columns ayant pour caracteristique 
            d etre une primary key

            :param table_name: nom de la table a gerer
            :type table_name: string
            :param new_data: la nouvelle donnee generee
            :type new_data: todo

            :return: un object uniquement compose de primary key
        """
        return_primary = None
        if (table_name in self.primary_column.keys()):
            if (len(self.primary_column[table_name]) > 0):
                return_primary = {}
                for primary_column_iterator in self.primary_column[table_name]:
                    return_primary[primary_column_iterator] = new_data[primary_column_iterator]
        return return_primary

    def generate_new_row(self, columns, number_of_row, id, table_name):
        """
            genere une nouvelle entree

            :param columns: liste des colonnes d une table
            :type columns: objet d'objet de type column
            :param number_of_row: nombre d entree theoriquement generer pour cette table 
            :type number_of_row: int
            :param id: id de la derniere entree generer 
            :type id: int 
            :param table_name: nom de la table qui est actuellement gerer 
            :type table_name: string 

            :return: une entree

        """
        print('### Generation d une entree pour la table %s ###'% table_name)
        unique_key = Key.unique
        new_row = {}
        for column_name in columns:
            if (table_name not in self.unique_datas.keys()):
                self.unique_datas[table_name] = {}
            if (column_name not in self.unique_datas[table_name].keys()):
                self.unique_datas[table_name][column_name] = {}
                self.unique_datas[table_name][column_name][unique_key] = []

            new_data = self.generate_data_column(columns[column_name], number_of_row, id = id)
            if (columns[column_name][unique_key]):
                timeout = 0
                while ((new_data in self.unique_datas[table_name][column_name][unique_key]) and (timeout < self.timeout)) :
                    new_data = self.generate_data_column(columns[column_name], number_of_row, id = id)
                    timeout += 1
                if timeout == self.timeout:
                    # todo : comprendre pourquoi ca marche pas 
                    # print("[error] [unique generation] Tentative de generation de donnees unique dans la table %s pour la colonne %s echoue" %table_name , column_name)
                    print("[error] [unique generation] Tentative de generation de donnees unique dans la table pour la colonne echoue")

            self.unique_datas[table_name][column_name][unique_key].append(new_data)
            new_row[column_name] = new_data
        return new_row

    def generate_data_column(self, column, number_of_row, id):
        """
            Genere une donnee en fonction du type de la colonne

            :param column: le schema de la colonne a traite
            :param number_of_row: nombre d entree theoriquement generer pour cette table 
            :type number_of_row: int
            :param id: id de la derniere entree generer 
            :type id: int 

            :return: une donnee generer aleatoirement
            :rtype: str|int
        """
        foreign_data = self.data
        generated_data = None
        if (column['name'] == 'id'):
            generated_data = id+1
        else:
            if (Key.type in column.keys()):
                if column[Key.type] == Key.foreignkey:
                    if Key.foreignkey in column.keys():
                        foreign_column = column[Key.foreignkey][Key.column_name]
                        foreign_table = column[Key.foreignkey][Key.table_name]
                        if(foreign_table not in self.data):
                            self.data[foreign_table] = self.generate_table_data(foreign_table)
                        one_random_element_in_foreign_data = tools.take_one_element_in_array(self.data[foreign_table])
                        generated_data = one_random_element_in_foreign_data[foreign_column]
                    else:
                        print('[Error] column de type foreign key mais pas de table de destination')
                        exit(1)
                    #todo
                else:
                    generated_datas = tools.generate_random_data(
                        column[Key.type], 
                        number_of_row, 
                        column[Key.reference_file] if (Key.reference_file in column.keys()) else '', 
                        self.ref_data[column[Key.ref]] if (Key.ref in column.keys() and column[Key.ref] in self.ref_data) else ''
                    )
                    generated_data = generated_datas[Key.data]

                    if (Key.ref_list_data in generated_datas.keys() and Key.ref in column.keys()):
                        self.ref_data[column[Key.ref]] = generated_datas[Key.ref_list_data]
        return generated_data
