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

from TG.openGL import data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestRect(unittest.TestCase):
    Rect = data.Rect

    def doVTest(self, rawQuestion, rawAnswer):
        if rawQuestion.dtype.base.char not in ('f', 'd'):
            rawAnswer = [map(int, ra) for ra in rawAnswer]

        self.failUnless(allclose(rawQuestion.pos, rawAnswer[0]), (rawQuestion.pos.tolist(), rawAnswer[0]))
        self.failUnless(allclose(rawQuestion.size, rawAnswer[1]), (rawQuestion.size.tolist(), rawAnswer[1]))

    def testBasic(self):
        self.doVTest(self.Rect(), [[0, 0], [0, 0]])

        r = self.Rect()
        r.size = [3.125, 6.25]
        self.doVTest(r, [[0, 0], [3.125, 6.25]])

        r = self.Rect(dtype='b')
        r.size = [3.125, 6.25]
        self.doVTest(r, [[0, 0], [3, 6]])

    def testFromSize(self):
        self.doVTest(self.Rect.fromSize((3.125, 6.25)), [[0, 0], [3.125, 6.25]])
        self.doVTest(self.Rect.fromSize((3.125, 6.25), dtype='b'), [[0, 0], [3, 6]])
    
    def testFromSizeAspect(self):
        self.doVTest(self.Rect.fromSize((3.125, 6.25), 1.5), [[0, 0], [3.125, 3.125/1.5]])
        self.doVTest(self.Rect.fromSize((3.125, 6.25), 1.5, dtype='b'), [[0, 0], [3, int(3/1.5)]])
    
    def testFromPosSize(self):
        self.doVTest(self.Rect.fromPosSize((2.3, 4.8), (3.125, 6.25)), [[2.3, 4.8], [3.125, 6.25]])
        self.doVTest(self.Rect.fromPosSize((2.3, 4.8), (3.125, 6.25), dtype='b'), [[2, 4], [3, 6]])
    
    def testFromPosSizeAspect(self):
        self.doVTest(self.Rect.fromPosSize((2.3, 4.8), (3.125, 6.25), 1.5), [[2.3, 4.8], [3.125, 3.125/1.5]])
        self.doVTest(self.Rect.fromPosSize((2.3, 4.8), (3.125, 6.25), 1.5, dtype='b'), [[2, 4], [3, 2]])
    
    def testFromCorners(self):
        self.doVTest(self.Rect.fromCorners((2.5, 1.5), (5.75, 6.75)), [[2.5, 1.5], [3.25, 5.25]])
        self.doVTest(self.Rect.fromCorners((2.5, 1.5), (5.75, 6.75), dtype='b'), [[2, 1], [3, 5]])
    
class TestRectf(TestRect):
    Rect = data.Rectf

class TestRecti(TestRect):
    Rect = data.Recti

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

