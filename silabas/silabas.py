#!/usr/bin/env python3

import re

class Sigma:
    
    # definição do alfabeto da língua.
    # TODO: Ler esse alfabeto a partir de um arquivo, a fim de tornar o script
    # mais flexível.
    v = r'[aeiouãõáéóíú]'
    c = r'[bcçdfgjklLmnñpqrstvxwyz]'
    n = r'[mn]'

    L = r'(?P<sil>'
    R = r')'
    Z = r'(' + c[:-1] + r']|$)'

    # Estes são os moldes silábicos da língua. É preciso traduzi-los em expressões
    # regulares; assim, cada caractere é um marcador que será substituído pelas
    # definições feitas acima. L e R representam, respectivamente '(' e ')', e Z 
    # representa uma consoante (ou fim de palavra) que não pode mais ser incluída
    # no molde e, portanto, indica que a sílaba acabou.
    moldes = ['LccvvcRZ', 'LccvvRZ', 'LcvvcRZ', 'LcvvRZ', 'LvvRZ', 
            'LccvncRZ', 'LccvcRZ', 'LccvRZ', 'LcvncRZ', 'LcvcRZ',
            'LcvR', 'LvncRZ', 'LvcRZ', 'LvRZ']

    model = []


    def __init__(self):

        # tradução dos moldes em expressões regulares.
        for m in self.moldes:
            regex = ''.join(map(lambda x: getattr(self, x), [x for x in m]))
            self.model.append(re.compile(regex))

    
    def syll(self, s):
        '''
        Input: string, contendo a palavra a ser silabificada.
        Output: list, contendo as sílabas encontradas na palavra.

        O script processa cada palavra sequencialmente, da esquerda para direita,
        testando todas as expressões regulares em cada posição, a fim de encontrar
        a mais inclusiva delas, que não desrespeite as restrições da língua.
        '''
        
        silabas = []
        i = 0

        while i < len(s):
            sigma = ''
            for molde in self.model:
                m = molde.match(s[i:])
                if m:
                    if len(m.group('sil')) > len(sigma):
                        sigma = m.group('sil')
            if sigma:
                silabas.append(sigma)
                i += len(sigma)
            else:
                i += 1

        return silabas


if __name__ == '__main__':
    s = Sigma()
    teste = ['casa', 'monstro', 'transporte', 'caixa', 'distração', 'recado',
            'oLos', 'felicidade', 'expresões', 'encantada', 'encanamento']
    for w in teste:
        print('.'.join(s.syll(w)))
