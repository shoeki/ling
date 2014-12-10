#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as db
import argparse
import json
import re
import nltk
import stemmer
from progress.bar import Bar

# definição da linha de comando
cmd = argparse.ArgumentParser(description='Popula o banco de dados a partir de um arquivo JSON.')
cmd.add_argument('data')
cmd.add_argument('corpus')
args = cmd.parse_args()
##############################

with open(args.data, 'r') as source:
    data = json.load(source)

with open('subs.json', 'r') as lista_grafia:
    grafia_subs = json.load(lista_grafia)

con = db.connect('corpus.db')
st = stemmer.RSLPStemmer()


with con:
    
    cur = con.cursor()

    def getstem(token):
        '''
        Finds the appropriate stem for a token, correcting typographical errors.
        '''

        stem = st.stem(token)

        if stem in grafia_subs:
            return grafia_subs[stem]
        else:
            return stem


    bar = Bar('Textos', max = len(data))

    for text in filter(lambda t: t['corpo'], data):
        
        # Prepare data
        if text['titulo']: tit = text['titulo'][0]
        # text should be stripped of excessive newline characters
        corpo = re.sub('\n\n+', '\n', ''.join(text['corpo']))
        h = str(text['hash'])

        # Insert data in the appropriate fields
        try:
            cur.execute('INSERT INTO Texto (textoid,autor,titulo,corpo,data,corpus) VALUES (?, ?, ?, ?, ?, ?)', (h, '', tit, corpo, text['data'][0], args.corpus))
        except db.IntegrityError:
            ''' Como o campo hash está marcado para ser único em init.py,
            caso se tente inserir um texto duplicado no banco de dados,
            uma exceção IntegrityError é imediatamente gerada. '''
            pass

        ### Tokenization and stemming ###
        pattern = r'\w+(-\w+)*'
       
        # Get tokens and stems
        tokens = [(tk, getstem(tk)) for tk in 
            map(lambda w: w.lower(), nltk.regexp_tokenize(corpo, pattern))]
    
        stems = list(set([(tk[1], ) for tk in tokens if tk[1]]))
        
        pos = 0
        cur.executemany('INSERT OR IGNORE INTO Palavra(palavra) VALUES(?)', stems)
        for tk in tokens:
            cur.execute('INSERT INTO Token VALUES (?, ?, ?, ?, ?)',
                    (tk[0].lower(), pos, tk[1], h, args.corpus))
            pos = pos + 1

        bar.next()
    bar.finish()
