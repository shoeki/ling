#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Stemmer apenas para a flexão.
'''

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *
import codecs
import string
import json
from nltk.data import load
from nltk.stem.api import StemmerI
import argparse

with open('subs.json','r') as lista_grafia:
    grafia_subs = json.load(lista_grafia)

class RSLPStemmer(StemmerI):
    """
    Adaptação da classe original distribuída com o NLTK.
    """

    def __init__ (self):
        self._model = []

        self._model.append(self.read_rule("step0.pt"))
        self._model.append(self.read_rule("step1.pt"))
        self._model.append(self.read_rule("step5.pt"))

    def read_rule (self, filename):
        rules = load('nltk:stemmers/rslp/' + filename, format='raw').decode("utf8")
        lines = rules.split("\n")

        lines = [line for line in lines if line != ""]     # remove blank lines
        lines = [line for line in lines if line[0] != "#"]  # remove comments

        # NOTE: a simple but ugly hack to make this parser happy with double '\t's
        lines = [line.replace("\t\t", "\t") for line in lines]

        # parse rules
        rules = []
        for line in lines:
            rule = []
            tokens = line.split("\t")

            # text to be searched for at the end of the string
            rule.append(tokens[0][1:-1]) # remove quotes

            # minimum stem size to perform the replacement
            rule.append(int(tokens[1]))

            # text to be replaced into
            rule.append(tokens[2][1:-1]) # remove quotes

            # exceptions to this rule
            rule.append([token[1:-1] for token in tokens[3].split(",")])

            # append to the results
            rules.append(rule)

        return rules

    def stem(self, word):
        word = word.lower()

        # the word ends in 's'? apply rule for plural reduction
        if word[-1] == "s":
            word = self.apply_rule(word, 0)

        # the word ends in 'a'? apply rule for feminine reduction
        if word[-1] == "a":
            word = self.apply_rule(word, 1)

        # noun reduction
        prev_word = word
        if word == prev_word:
            # verb reduction
            prev_word = word
            word = self.apply_rule(word, 2)

        return word

    def apply_rule(self, word, rule_index):
        rules = self._model[rule_index]
        for rule in rules:
            suffix_length = len(rule[0])
            if word[-suffix_length:] == rule[0]:       # if suffix matches
                if len(word) >= suffix_length + rule[1]:  # if we have minimum size
                    if word not in rule[3]:                # if not an exception
                        word = word[:-suffix_length] + rule[2]
                        break

        return word

def getstem(token):
    '''
    Encontra a stem apropriada para token, corrigindo erros de grafia.
    '''

    st = stemmer.RSLPStemmer()
    stem = st.stem(token)

    if stem in grafia_subs:
        return grafia_subs[stem]
    else:
        return stem

if __name__ == "main":

    comando = argparse.ArgumentParser(description='Stemmer para retirar as flexões')
    comando.add_argument('input')
    comando.add_argument('output')
    comando.add_argument('exceptions')
    args = comando.parse_args()

    stemmer = RSLPStemmer()

    words_by_stem = {}

    # carrega a lista de substituições de ortografia
    with codecs.open(args.exceptions, 'r', encoding='utf-8') as grafia_ex:
        grafia_subs = json.load(grafia_ex)

    with codecs.open(args.input, 'r', encoding='utf-8') as source:
        for word in source:
            word = word.split('\t')[0]
            word = string.rstrip(word)
            stem = stemmer.stem(word)
            if stem in grafia_subs:
                stem = grafia_subs[stem]
            words_by_stem.setdefault(stem, []).append(word)

    with codecs.open(args.output, 'w', encoding='utf-8') as output:
        json.dump(words_by_stem, output, indent = 4)
