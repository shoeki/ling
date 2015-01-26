#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import freqlist
import random


if __name__ == '__main__':
    
    cmd = argparse.ArgumentParser(description='Por exemplo: ./vgc.py all'
                                        ' mento data/out_mento.vgc')
    cmd.add_argument('corpus', help='Nome do corpus dentro do banco de dados.'
                                    ' "all" seleciona todo o banco.')
    cmd.add_argument('afixo', help='Referência do afixo desejado, que precisa estar'
                                    ' definida em tools.py')
    cmd.add_argument('output', help='Arquivo de output que receberá a curva de'
                                    ' vocabulário.')
    args = cmd.parse_args()
    
    freqs = freqlist.getList(args.afixo, args.corpus)
    print('Types:', len(freqs))
    
    token_count = 0
    type_count = 0
    hapax_count = 0
    random.seed()
    d = {}
    output_list = []
    
    while freqs:
        
        index = random.randint(0, len(freqs) - 1)
        token_count += 1
        current_word = freqs[index][0]
        current_freq = freqs[index][1]
        
        if current_word in d:
            d[current_word] = d[current_word] + 1
            if d[current_word] == 2:
                hapax_count = hapax_count - 1
        else:
            d[current_word] = 1
            hapax_count += 1
            type_count += 1
            
        if current_freq == d[current_word]:
            del freqs[index]
            
        output_list.append((token_count, type_count, hapax_count))
            
        
    with open(args.output, 'w') as output:
        for step in output_list:  
            output.write(str(step[0]) + ',' + str(step[1])
                     + ',' + str(step[2]) + '\n')