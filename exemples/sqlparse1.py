#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Andi Albrecht, albrecht.andi@gmail.com
#
# This example is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause
#
# Example for retrieving column definitions from a CREATE statement
# using low-level functions.

import sqlparse
import sys
sys.path.append('../src/modules/')
import FileReader

def extract_definitions(token_list):
    # assumes that token_list is a parenthesis
    definitions = []
    tmp = []
    # grab the first token, ignoring whitespace. idx=1 to skip open (
    tidx, token = token_list.token_next(1)
    while token and not token.match(sqlparse.tokens.Punctuation, ')'):
        tmp.append(token)
        # grab the next token, this times including whitespace
        tidx, token = token_list.token_next(tidx, skip_ws=False)
        # split on ",", except when on end of statement
        if token and token.match(sqlparse.tokens.Punctuation, ','):
            definitions.append(tmp)
            tmp = []
            tidx, token = token_list.token_next(tidx)
    if tmp and isinstance(tmp[0], sqlparse.sql.Identifier):
        definitions.append(tmp)
    return definitions


if __name__ == '__main__':
    SQL1 = """CREATE TABLE foo (
             id integer primary key,
             title varchar(200) not null,
             description text);"""

    SQL = FileReader.readFileSql('../sql-file/cuisine.sql')

    parsed = sqlparse.parse(SQL)[0]

    # extract the parenthesis which holds column definitions
    _, par = parsed.token_next_by(i=sqlparse.sql.Parenthesis)
    #print(parsed)
    #print(par)
    columns = extract_definitions(par)

    for column in columns:
        #print('NAME: {name} DEFINITION: {definition}'.format(
        #name=column[0], definition=''.join(str(t) for t in column[1:])))
        # print(column)
        for test in column:
            print('-----------------')
            #print(test)
    #print(columns)

stmt = sqlparse.parse(SQL)[0]
print(dir(stmt))
print(stmt.get_type()) # type de la table
# CREATE
print(stmt.get_alias()) # alias de la table
# foo
print(stmt._get_first_name()) # nom de la table
# foo
print(stmt.get_real_name()) # nom de la table
# foo
print(stmt.tokens) # 
# print(stmt.tokens) # token
print('------------------') # 
print(stmt.token_next_by(i=sqlparse.sql.Parenthesis)) # 
_, par = stmt.token_next_by(i=sqlparse.sql.Parenthesis)
#print(par)
# print(dir(par))
# print(par.get_real_name())

#columns = extract_definitions(par)
#for elem in par:
#    print(elem)

# 'get_sublists', 
# 'get_token_at_offset', 'get_type', 'group_tokens', 'has_alias', 'has_ancestor', 'insert_after', 'insert_before', 'is_child_of', 'is_group', 
# 'is_keyword', 'is_whitespace', 'match', 'normalized', 'parent', 'token_first', 'token_index', 'token_matching', 'token_next', 'token_next_by', 'token_not_matching', 'token_prev', 
#'tokens', 'ttype', 'value', 'within']



#print(stmt.get_sublists())
#stmt.get_columns()
# [<Column 'id'>, <Column 'title'>, <Column 'description']
#col = stmt.get_column('title')
#print(col.name)
#print(col.notnull )
