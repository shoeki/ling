#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse
import tools
import sqlite3 as db

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

regex = re.compile(tools.afixo[afixo], re.UNICODE)

exceptions = tools.getExceptions(args.afixo)

con = db.connect('data/corpus.db')

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
        cur.execute('SELECT stem, count(*) AS tk FROM Token WHERE corpus = ? AND match(stem) = 1 GROUP BY stem ORDER BY tk DESC', (corpus,))
    freqs = cur.fetchall()

    with open(args.output, 'w') as tfl:
        tfl.write('f' + '\n')
        for step in freqs:
            tfl.write(str(step[1]) + '\n')

    with open(args.output + '.list', 'w') as tfl:
        for step in freqs:
            tfl.write(step[0] + '\t' + str(step[1]) + '\n')
