import json

def generate_json_file(data, output_file):
    """
        dump un objet json dans un fichier

        :param data: l'objet a dumper
        :type data: object
        :param outputfile: chemin vers le fichier de destination
        :type outputfile: string
    """
    try:
        with open(output_file, 'w') as file:
            file.write(json.dumps(data, indent=2))
    except Exception as e:
        print('Erreur lors de la creation du fichier')
        print(e)
        exit(1)


def generate_xml_file(data, output_file):
    """
        genere un xml dans un fichier

        :param data: l'objet a dumper
        :type data: object
        :param outputFile: chemin vers le fichier de destination
        :type outputFile: string
    """
    root = etree.Element('data')
    try:
        for table_name in data:
            table = etree.SubElement(root, table_name)
            for element_of_table in data[table_name]:
                element_of_xml = etree.SubElement(table, 'element')
                if('id' in element_of_table.keys()):
                    element_of_xml.set('id', str(element_of_table['id']))
                column_Of_Xml = None
                for column_of_table in element_of_table:
                    column_of_xml = etree.SubElement(element_of_xml, column_of_table).text = str(element_of_table[column_of_table])
    except:
        print('Erreur de formmat pour la creation de format Xml')
        exit(1)
    try:
        with open(outputFile, 'w') as fic:
            fic.write(etree.tostring(root, pretty_print=True).decode('utf-8'))
    except IOError:
        print('Probleme rencontre lors de l\'ecriture...')
        exit(1)


def generate_Sql_File(data, output_File):
    """
        passe un fichier en requete sql et le print dans un fichier

        :param data: l'objet a dumper
        :type data: object
        :param outputFile: chemin vers le fichier de destination
        :type outputFile: string
    """
    fichier = open(output_File, "w")
    eol_Symbole = '\n'
    
    try:
        for table_name in data:
            begin_insert_value_lign = 'INSERT INTO ' + str(table_Name) + ' (' 
            for column_name in data[table_name][0]:
                begin_insert_value_lign = begin_insert_value_lign + column_name + ', '
            begin_insert_value_lign = begin_insert_value_lign[:len(begin_insert_value_lign)-2] + ') VALUES '
            fichier.write(begin_insert_value_lign) 
            fichier.write(eol_symbole)

            end_insert_value_lign_initial = '('
            for element in data[table_name]:
                end_insert_value_lign = end_insert_value_lign_initial
                for column in element:
                    end_insert_value_lign = end_insert_value_lign + str(element[column]) + ', '
                end_insert_value_lign = end_insert_value_lign[:len(end_insert_value_lign)-2] + ')'
                
                fichier.write(end_insert_value_lign) 
                fichier.write(eol_symbole)
            fichier.write(';')
            fichier.write(eol_symbole)
            fichier.write(eol_symbole)
    except:
        print('Erreur de formmat pour la creation de format Sql')
        exit(1)

    fichier.close()


def generate_txt_file_from_array(data, output_file):
    """
        dump un array json dans un fichier

        :param data: l'array a dumper
        :type data: array
        :param outputfile: chemin vers le fichier de destination
        :type outputfile: string
    """
    fichier = open(output_file, "w")
    eol_symbole = '\n'
    
    try:
        for lign in data:
            fichier.write(lign) 
            fichier.write(eol_symbole)
    except:
        print('Erreur lors de l ecriture de tableau dans un fichier')
        exit(1)

    fichier.close()


def generate_txt_file_from_object(data, output_file):
    """
        ecrit un objet ligne par ligne dans un fichier

        :param data: l'objet a dumper
        :type data: object
        :param outputfile: chemin vers le fichier de destination
        :type outputfile: string
    """
    fichier = open(output_file, "w")
    eol_symbole = '\n'
    
    try:
        for i in range(len(data)):
            fichier.write(data[i]) 
            fichier.write(eol_symbole)
    except:
        print('Erreur lors de l ecriture de tableau dans un fichier')
        exit(1)

    fichier.close()
