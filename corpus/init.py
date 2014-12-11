#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Inicialização do banco de dados 
'''

import sqlite3 as db

con = db.connect('data/corpus.db')

with con:

    cur = con.cursor()

    ''' A unidade básica do banco de dados é o token (entendido como cada
    ocorrência de uma palavra). Cada token faz referência à palavra que ele
    instancia e ao texto em que aparece.
    '''

    cur.executescript('''
        CREATE TABLE Corpus(
            nome    TEXT PRIMARY KEY
            );
        CREATE TABLE Texto(
            textoid TEXT PRIMARY KEY,
            hash    TEXT UNIQUE, 
            autor   TEXT,
            titulo  TEXT,
            corpo   TEXT,
            data    TEXT,
            corpus  TEXT REFERENCES Corpus(nome)
            );
        CREATE TABLE Palavra(
            palavraid INTEGER PRIMARY KEY,
            palavra TEXT UNIQUE
            );
        CREATE TABLE Token(
            token   TEXT,
            pos     INTEGER,
            stem    INTEGER REFERENCES Palavra(palavraid),
            texto   INTEGER REFERENCES Texto(textoid),
            corpus  TEXT REFERENCES Corpus(nome)
            );
        ''')
