#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import json

db = sqlite3.connect('data/corpus.db')

with db:
    cur = db.cursor()

    with open('subs.json', 'r') as grafia:
        grafia_subs = json.load(grafia)

    # atualizar grafia
    words = cur.execute('SELECT stem FROM Token').fetchall()
    words = map(lambda w: w[0], words)
    words = filter(lambda w: w in grafia_subs and grafia_subs[w], words)
    words = map(lambda w: (grafia_subs[w], w), words)
    print words

    if words:
        cur.executemany('UPDATE Token SET stem = ? WHERE stem = ?', words)
        cur.executemany('DELETE FROM Palavra WHERE palavra = ?',
                map(lambda w: w[1], words))
