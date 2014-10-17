#!/usr/bin/env python3

import re

class Sigma:
    
    v = r'[aeiouãõáéóíú]'
    c = r'[bcçdfgjklLmnñpqrstvxwyz]'
    n = r'[mn]'
    L = r'(?P<sil>'
    R = r')'
    Z = r'(?P<resto>' + c[:-1] + r']|$)'
    moldes = ['LccvvcRZ', 'LccvvRZ', 'LcvvcRZ', 'LcvvRZ', 'LvvRZ', 
            'LccvncRZ', 'LccvcRZ', 'LccvRZ', 'LcvncRZ', 'LcvcRZ',
            'LcvR', 'LvncRZ', 'LvcRZ', 'LvRZ']
    model = []


    def __init__(self):

        for m in self.moldes:
            regex = ''.join(map(lambda x: getattr(self, x), [x for x in m]))
            self.model.append(re.compile(regex))

    
    def syll(self, s):    
        subs = []
        i = 0
        while i < len(s):
            silaba = ''
            for molde in self.model:
                m = molde.match(s[i:])
                if m:
                    if len(m.group('sil')) > len(silaba):
                        silaba = m.group('sil')
            if silaba:
                subs.append(silaba)
                i += len(silaba)
            else:
                i += 1
        return subs

if __name__ == '__main__':
    s = Sigma()
    teste = ['casa', 'monstro', 'transporte', 'caixa', 'distração', 'recado',
            'oLos', 'felicidade', 'expresões']
    for w in teste:
        print('.'.join(s.syll(w)))
