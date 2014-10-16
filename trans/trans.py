#!/usr/bin/env python3

import re
import sys

class Phon:
    '''
    Aplicação de regras fonológicas para o português.

    A ideia é ler um arquivo com regras que podem ser aplicadas a strings.
    A motivação inicial para este script foi criar um sistema de transcrição
    fonética/fonológica a partir de palavras escritas. Como isso pode ser feito
    de diversas formas, dependendo da variedade do português, as regras são
    dadas por um arquivo de texto carregado pelo script.
    '''

    vowels = 'aeiou'
    nasal_v = 'ãêîõû'
    nasals = 'mn'
    consonants = 'bcdfghjklmnpqrstvxywz'

    def __init__(self, rules='rules.pt'):

        self.model = self.read(rules)


    def read(self, source):
        '''
        Cada linha do arquivo de regras tem o formato:
        input   output  exceções

        exceções é uma lista de palavras separadas por vírgulas.

        Linhas de comentário começam com '#'.
        '''

        rules = []

        with open(source, 'r') as s:
            for line in s:
                if line[0] != '#':
                    rule = list(map(lambda s: s.strip(), (line.split('\t'))))
                    try:
                        rule[2] = rule[2].split(',')
                    except IndexError:
                        rule.append('')
                    rules.extend(self.expand(rule))

        return rules


    def expand(self, rule):
        '''
        Esta é a parte mais tricky.
        
        As regras podem ser escritas com variáveis; por exemplo, VC denota
        qualquer vogal seguida de uma consoante. Esta função expande essa
        regra abreviada e tem como valor de retorno uma lista de regras
        que abrange todas as possibilidades de instanciação das variáveis.

        A instanciação de uma variável deve ser a mesma no input/contexto
        da regra e no output. Assim, se VN -> V pode ser instanciada por an -> a,
        mas não por an -> e.
        '''

        i = 0
        cxs = [[list(rule[0]), rule[1]]]

        while i < len(rule[0]):
            
            if rule[0][i] == 'V':
                l = []
                for cx in cxs:
                    for v in self.vowels + self.nasal_v:
                        cx[0][i] = v
                        out = cx[1].replace('V', v, 1)
                        # é preciso dar conta das nasalizações
                        if rule[1][i] == 'Ṽ':
                            out = cx[1].replace('Ṽ',
                                    self.nasal_v[self.vowels.find(v)])
                        l.append([cx[0][:], out])

            if rule[0][i] == 'Ṽ':
                l = []
                for cx in cxs:
                    for v in self.nasal_v:
                        cx[0][i] = v
                        out = cx[1].replace('Ṽ', v)
                        l.append([cx[0][:], out])

            if rule[0][i] == 'C':
                l = []
                for cx in cxs:
                    for c in self.consonants:
                        cx[0][i] = c
                        out = cx[1].replace('C',c)
                        l.append([cx[0][:], out])

            if rule[0][i] == 'N':
                l = []
                for cx in cxs:
                    for n in self.nasals:
                        cx[0][i] = n
                        out = cx[1].replace('N', n)
                        l.append([cx[0][:], out])
            
            try:
                cxs = l[:]
            except UnboundLocalError:
                pass
            i += 1

        return list(map(lambda l: (''.join(l[0]).replace('0', ''), 
            l[1], rule[2]), cxs))


    def apply_rule(self, word, rule):

        return re.sub(rule[0], rule[1], word).replace('0', '')


    def run(self, words):
        
        for rule in self.model:
            words = list(map(lambda w: self.apply_rule(w, rule), words))

        return words


if __name__ == '__main__':
    
    args = sys.argv[1:]
    ph = Phon()

    try:
        with open(args[0], 'r') as words:
            for line in words:
                print('\t'.join(ph.run(line.split())))
    except FileNotFoundError:
        print('Indique o nome do arquivo')
