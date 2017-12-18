import json

def read_file_sql(input_file):
    """
        concatene un fichier en une seul string

        :param inputFile: le fichier a lire
        :type inputFile: string

        :return: une string avec toutes les lignes misent bout a bout
        :rtype: string
    """
    print('### Lecture du fichier SQL ###')
    total_request = ''
    try:
        with open(input_file, 'r') as file:
            for line in file:
                total_request += line 
    except FileNotFoundError as e:
        print('Le fichier {} n\'existe pas !'.format(e.filename))
        exit(1)
    except PermissionError as e:
        print('Droit de lecture absent sur le fichier {} !'.format(e.filename))
        exit(2)
    except Exception as e:
        print('Une erreur a empeche l\'ouverture du fichier : {}'.format(e.strerror))
        exit(3)
    return total_request

def read_json_file(json_file):
    """
        recupere un json d un fichier pour le retourner en objet

        :param inputFile: le fichier a lire
        :type inputFile: string

        :return: l objet sortit du fichier
        :rtype: object
    """
    print('### Lecture du fichier JSON ###')
    try:
        with open(json_file, 'r') as file:
            data_schema = json.load(file)
    except Exception as e:
        print('Erreur lors de la lecture du fichier')
        print(e)
        exit(1)
    return data_schema