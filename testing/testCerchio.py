#!/usr/bin/python
# coding: utf-8

import unittest
import math
from Cerchio import *

# classe test deriva da ()


class testCerchio(unittest.TestCase):

    # imposta un'istanza test chiamata c
    def setUp(self):
        self.c = Cerchio(10.0)

    # controlla il tipo
    def testObj(self):
        self.assertTrue(
            isinstance(self.c, Cerchio),
            "c non è un Cerchio"
        )

    # testa che i metodi siano richiamabili
    def testMeth(self):
        self.assertTrue(
            callable(self.c.raggio),
            "c non ha il metodo raggio"
        )
        self.assertTrue(
            callable(self.c.perimetro),
            "c non ha il metodo perimetro"
        )
        self.assertTrue(
            callable(self.c.area),
            "c non ha il metodo area"
        )

    # testa il metodo raggio che è sia un get che un set
    def testraggio(self):
        # 					robustezza: input non validi
        self.assertRaises(
            TypeError,
            self.c.raggio,
            ""
        )
        self.assertRaises(
            ValueError,
            self.c.raggio,
            -1.0
        )
        # 			coerenza funzionale: risultati attesi dei metodi get/set
        # 			setto il raggio prima della prova per avere la certezza del dato corretto
        self.c.raggio(2.0)
        self.assertEqual(
            self.c.raggio(),
            2.0,
            "il raggio di c non è recuperato correttamente"
        )

    # test del metodo perimetro
    def testperimetro(self):
        self.c.raggio(5.0)
        self.assertEqual(
            self.c.perimetro(),
            10.0 * math.pi,
            "Il perimetro di c non è calcolato correttamente"
        )
    # 						coerenza funzionale: risultati attesi dei metodi

        # test del metodo area
    def testarea(self):
        self.c.raggio(4.0)
        self.assertEqual(
            self.c.area(),
            math.pi * 4.0 * 4.0,
            "L'area di c non è calcolata correttamente"
        )

    # elimina l'istanza di test
    def tearDown(self):
        del self.c

# fa in modo che i test vengano eseguiti quando il file viene eseguito
# come script principale, mentre non vengono eseguiti se il file viene
# importato come modulo in un altro script.


if __name__ == '__main__':
    unittest.main()
