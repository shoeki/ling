#!/usr/bin/env python3

import unittest
from trans import g2pbr

class PhonTest(unittest.TestCase):
    
    def setUp(self):
        self.test_words = {
            'financiamento': 'finãsiamẽto',
        }
        self.phon = g2pbr.Phon(rules='trans/rules.pt')
    
    def test_words(self):
        for w in self.test_words:
            self.assertEqual(self.phon.run([w])[0], self.test_words[w])
            
if __name__ == '__main__':
    unittest.main()