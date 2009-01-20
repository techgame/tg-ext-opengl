##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest

from numpy import allclose
from TG.openGL.data import VertexArray, Vertex

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestVertexArrays(unittest.TestCase):
    def doCVTestFor(self, rawQuestion, rawAnswer):
        question = VertexArray(rawQuestion)
        answer = rawAnswer
        self.assertEqual(question.tolist(), [answer])

        question = Vertex(rawQuestion)
        answer = rawAnswer
        self.assertEqual(question.tolist(), answer)

    def testVertexZeros(self):
        self.doCVTestFor([0, 0], [0, 0])
        self.doCVTestFor([0, 0, 0], [0, 0, 0])
        self.doCVTestFor([0, 0, 0, 0], [0, 0, 0, 0])

    def testVertexDefault(self):
        v = Vertex()
        vf = Vertex(dtype='f')
        v3f = Vertex(dtype='3f')
        self.assertEqual(v.tolist(), [0., 0., 0.])
        self.assertEqual(vf.tolist(), [0., 0., 0.])
        self.assertEqual(v3f.tolist(), [0., 0., 0.])

    def testVertexFromVertex(self):
        v = Vertex([2., 3., 4.])
        vf = Vertex([2., 3., 4.], '3f')

        self.assertEqual(v.tolist(), [2., 3., 4.])
        self.assertEqual(vf.tolist(), [2., 3., 4.])

        self.assertEqual(Vertex(v).tolist(), [2., 3., 4.])
        self.assertEqual(Vertex(vf).tolist(), [2., 3., 4.])

        self.assertEqual(Vertex(v, '3f').tolist(), [2., 3., 4.])
        self.assertEqual(Vertex(vf, '3f').tolist(), [2., 3., 4.])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

