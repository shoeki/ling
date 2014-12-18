# -*- coding: utf-8 -*-

'''
'''

import re
from datetime import datetime as dt
import json
import sqlite3

db = sqlite3.connect('data/corpus.db')
db.text_factory = lambda x: x.decode('utf-8')   # compatibilidade com Python < 3

exceptions = 'exceptions.json'

afixo = {
        'mento': 'mento$|mnto$|mentu$',
        'ção': 'ção$|çao$',
        'ura': '(t|d)ura$'
    }

def getExceptions(afixo):
    '''
    Dado um afixo, retorna a lista de exceções correspondente, carregada a
    partir de um arquivo JSON.
    '''

    # carrega uma lista com as exceções do afixo estudado.
    try:
        with open(exceptions, 'r') as exs:
            return json.load(exs, object_hook=lambda dic: dic[afixo])
    except TypeError:
        return {}


def getContexts(query, n=20):
    '''
    Busca contextos de ocorrência da <query> no corpus, retornando, no máximo,
    <n> contextos.
    '''

    with db:
        cur = db.cursor()
        tokens = cur.execute('SELECT corpo FROM Texto WHERE textoid IN'
                             '(SELECT texto FROM Token WHERE token = ? LIMIT ?)',
                             (query, n)).fetchall()
    
    # fetchall() retorna uma lista de tuples. Precisamos transformá-la
    # em uma lista de strings.
    
    return map(lambda t: t[0], tokens)

#def countCorpus(nome):
#    '''
#    Dado o nome de um corpus, retorna o número de artigos e o número de tokens
#    coletados.
#    '''
#
#    corpus = getCorpus(nome)
#    tokens = getTokens(nome)
#
#    return (len(corpus), len(tokens))
#
#
#def normalizaData(formato, s):
#    '''
#    Dada uma string s, identifica uma data caracterizada pela regex e retorna
#    a data normalizada: %Y%m%d.
#    '''
#
#    regex = {
#            '%d/%m/%Y': '\d{2}/\d{2}/\d{4}'
#        }
#
#    r = re.compile(regex[formato])
#    data = dt.strptime(re.search(r, s).group(0), formato).strftime('%Y%m%d')
#    return data
#
#
#def sortCorpus(corpus, formato='%d/%m/%Y'):
#    '''
#    Retorna uma cópia do corpus com os artigos ordenados por data.
#    '''
#
#    for item in corpus:
#        item['data'] = normalizaData(formato, item['data'][0])
#    datas = sorted(list(set([item['data'] for item in corpus])))
#
#    output = []
#
#    for d in datas:
#        output.extend([item for item in corpus if d in item['data']])
#
#    return output
#
#
#def updateCorpus(nome, source):
#    '''
#    Centraliza todas as operações de escrita nos corpora, por segurança.
#    '''
#
#    with open(corpus[nome], 'w') as output:
#        json.dump(source, output, indent=4)
#
#
#def getCorpus(nome):
#    '''
#    Dado o nome de um corpus, retorna o json correspondente.
#    '''
#
#    with open(corpus[nome], 'r') as source:
#        return json.load(source)
#
#
#def getTokens(nome):
#    '''
#    Dado o nome de um corpus, retorna a lista de tokens que foram extraídos
#    dele.
#    '''
#
#    with open(tokens[nome], 'r') as source:
#        return map(lambda l: l.split('\t'), [lin for lin in source])
#
#
#def getPattern(afixo, corpus, N=0):
#    '''
#    Dado o nome de um afixo, procura no corpus por todas as palavras que o
#    instanciam.
#    '''
#
#    c = getTokens(corpus)
#
#    stemspath = cpath[corpus] + afixo + '_' + corpus + '.json'
#    with open(stemspath, 'r') as s:
#        stems = json.load(s)
#
#    if N > 0:
#        return map(lambda t: t[1], [t for t in c if t[1] in stems.keys()][:N])
#    else:
#        return map(lambda t: t[1], [t for t in c if t[1] in stems.keys()])
#
#
#def getFreqs(afixo, corpus, N=0):
#    '''
#    Dado o nome de um afixo, gera um dicionário com a distribuição de
#    frequência que caracteriza
#    '''
#
#    c = getPattern(afixo, corpus, N)
#
#    gfreq = {}
#
#    for w in c:
#        try:
#            gfreq[w] = gfreq[w] + 1
#        except KeyError:
#            gfreq[w] = 1
#
#    return gfreq
#
#
#def getCurve(afixo, corpus):
#    '''
#    Dado um afixo e o nome de um corpus, retorna a representação numérica
#    da curva de crescimento de vocabulário correspondente.
#    '''
#
#    curva = cpath[corpus] + afixo + '_' + corpus + '.csv'
#
#    with open(curva, 'r') as source:
#        return map(lambda l: l.split(','), [lin for lin in source])
#
#
#def updateTokens(nome, forms):
#    '''
#    Centraliza todas as operações de escrita nas listas de tokens,
#    por segurança.
#    '''
#
#    with open(tokens[nome], 'w') as output:
#        for linha in forms:
#            output.write('\t'.join(linha))
#
#
#def subsTokens(nome):
#    '''
#    Dado o nome de um corpus, atualiza a lista de tokens que foram extraídos
#    dele, utilizando a última versão da lista de substituição
#    '''
#
#    with open(subs, 'r') as subst:
#        lsubs = json.load(subst)
#    tokens = getTokens(nome)
#
#    def sub(token):
#        if token[1] in lsubs:
#            return [token[0], lsubs[token[1]], token[2]]
#        else:
#            return token
#
#    updateTokens(nome, map(sub, tokens))
#
#
#def getHapaxes(afixo, corpus, samplesize=0):
#    '''
#    Dado um afixo e o nome de um corpus, retorna todos os hapaxes para o
#    tamanho de amostra
#    '''
#
#    pass
