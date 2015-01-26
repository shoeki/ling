#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
import tools
import sqlite3 as db


def getList(aff, corpus, db_file = 'data/corpus.db'):
    
    con = db.connect(db_file)
    
    exceptions = tools.getExceptions(aff)
    regex = re.compile(tools.afixo[aff], re.UNICODE)
    
    def match(word):
        if type(word) == str and regex.search(word) and word not in exceptions:
            return 1
        else:
            return 0
    
    with con:
    
        cur = con.cursor()
    
        con.create_function('match', 1, match)
    
        if corpus == 'all':
            cur.execute('SELECT stem, count(*) AS tk FROM Token WHERE match(stem) = 1 GROUP BY stem ORDER BY tk DESC')
        else:
            cur.execute('SELECT stem, count(*) AS tk FROM Token'
                        'WHERE corpus = ? AND match(stem, ?) = 1'
                        'GROUP BY stem ORDER BY tk DESC', (corpus,))
    return cur.fetchall()


if __name__ == '__main__':
    
    cmd = argparse.ArgumentParser(description='Por exemplo: ./freqlist.py all'
                                        ' mento data/out_mento.tfl')
    cmd.add_argument('corpus', help='Nome do corpus dentro do banco de dados.'
                                    ' "all" seleciona todo o banco.')
    cmd.add_argument('afixo', help='Referência do afixo desejado, que precisa estar'
                                    ' definida em tools.py')
    cmd.add_argument('output', help='Arquivo de output que receberá a lista de'
                                    ' frequências.')
    args = cmd.parse_args()
    
    afixo = args.afixo
    corpus = args.corpus
    
    freqs = getList(afixo, corpus)
   
    with open(args.output, 'w') as tfl:
        tfl.write('f' + '\n')
        for step in freqs:
            tfl.write(str(step[1]) + '\n')

    with open(args.output + '.list', 'w') as tfl:
        for step in freqs:
            tfl.write(step[0] + '\t' + str(step[1]) + '\n')