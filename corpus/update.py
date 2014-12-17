#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Busca todas as palavras do corpus e as compara com a lista de substituições.
Caso haja alguma entrada nessa lista que não esteja corrigida no corpus,
o script faz a correção necessária.
'''

import sqlite3
import json

db = sqlite3.connect('data/corpus.db')

with db:
    cur = db.cursor()

    with open('subs.json', 'r') as grafia:
        grafia_subs = json.load(grafia)

    words = cur.execute('SELECT palavra FROM Palavra').fetchall()
    words = map(lambda w: w[0], words)
    words = filter(lambda w: w in grafia_subs and grafia_subs[w], words)
    words = map(lambda w: (grafia_subs[w], w), words)
    
    for w in words:
        print w[1] + ' -> ' + w[0]

    if words:
        cur.executemany('UPDATE OR IGNORE Palavra SET palavra = ?'
                        'WHERE palavra = ?', words)
        cur.executemany('UPDATE Token SET stem = ? WHERE stem = ?',
                        words)
