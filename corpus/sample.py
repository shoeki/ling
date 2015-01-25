#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import argparse
import tools
import sqlite3 as db


# Retira os argumentos da linha de comando
comando = argparse.ArgumentParser(description='Amostragem por afixo')
comando.add_argument('corpus')
comando.add_argument('afixo')
args = comando.parse_args()

afixo = args.afixo
corpus = args.corpus

# A cada afixo, corresponde uma expressão regular (listada no arquivo tools.py).
# Essa expressão vai ser usada para buscar ocorrências do afixo no arquivo de
# tokens.
regex = re.compile(tools.afixo[afixo], re.UNICODE)

vocab = {}    # vocabulário a ser incrementado aos poucos.
curva_do_vocab = []    # lista de triplas: (types, tokens, hapax)
N = 0    # número de tokens com o afixo estudado.

# Para cada afixo, também há palavras que apenas parecem instanciá-lo, pois
# apresentam a mesma sequência fonológica desse afixo.
exceptions = tools.getExceptions(args.afixo.decode('utf-8'))

con = db.connect('data/corpus.db')

with con:
    # Este bloco de código constrói a curva de vocabulário, a partir do arqui-
    # vo de tokens. A cada linha desse arquivo, a curva é atualizada, com a
    # informação de quantos tokens já foram processados, quantos tipos e
    # quantos hapax legomena.

    cur = con.cursor()

    cur.execute('SELECT token, stem FROM Token WHERE corpus = ?', (corpus,))

    for tk in cur.fetchall():
        token = tk[0]
        stem = tk[1]

        if type(stem) == unicode and regex.search(stem):

            # Faz a correção ortográfica nos casos em que o afixo não foi escrito
            # na forma que foi buscada.
            #if stem[:-len(args.afixo)] != args.afixo:
            #    print stem
            #    stem = stem[:-len(args.afixo)] + args.afixo
            #    print '-->', stem

            if stem not in exceptions:
            
                # A cada vez que um token é encontrado, ele é acrescentado ao
                # vocabulário, como uma instância de um tipo, que já pode ter
                # aparecido antes ou não.
                vocab.setdefault(stem, []).append(token)

                # Atualiza, de fato, a curva de vocabulário com mais um passo.
                N = N + 1
                hapax = len([tipo for tipo in vocab.values() if len(tipo) == 1])
                types = len(vocab)
                curva_do_vocab.append((types, N, hapax))

# Este bloco salva a curva em um arquivo vgc.
with open('vgc/' + afixo + '_' + corpus + '.vgc', 'w') as output:
    output.write('N' + '\t' + 'V' + '\t' + 'V1' + '\n')
    for step in curva_do_vocab:
        output.write(str(step[1]) + '\t' + str(step[0]) +
            '\t' + str(step[2]) + '\n')

# Este bloco salva os tokens organizados por stem (para fins de conferência).
for stem in vocab:
    vocab[stem] = list(set(vocab[stem]))
with open('vgc/' + afixo + '_' + corpus + '.json', 'w') as output:
    json.dump(vocab, output, indent=4)