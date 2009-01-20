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
from TG.openGL.data import Color, bezier

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestLinearBezier(unittest.TestCase):
    u = [0, .125, .25, .5, .75, .875, 1]
    cpts = Color(['#000', '#70f', '#f48', '#fff'], '4B')

    def doCVTestFor(self, rawQuestion, rawAnswer):
        q = rawQuestion.astype('B').tolist()
        self.assertEqual(q, rawAnswer)

    def doAt(self, (i, j), result):
        bm = bezier.b1; u = self.u; cpts = self.cpts
        self.doCVTestFor(bm.atU(u).atP([cpts[i], cpts[j]]), result)
        self.doCVTestFor(bm.atU(u) * [cpts[i], cpts[j]], result)
        self.doCVTestFor(bm.atP([cpts[i], cpts[j]]).atU(u), result)
        self.doCVTestFor(bm.at([cpts[i], cpts[j]], u), result)
    
    def testCpts0vs1(self):
        self.doAt((0, 1), [
                [0, 0, 0, 255], 
                [14, 0, 31, 255], 
                [29, 0, 63, 255], 
                [59, 0, 127, 255], 
                [89, 0, 191, 255], 
                [104, 0, 223, 255], 
                [119, 0, 255, 255]])
    def testCpts0vs2(self):
        self.doAt((0, 2), [
                [  0,   0,   0, 255],
                [ 31,   8,  17, 255],
                [ 63,  17,  34, 255],
                [127,  34,  68, 255],
                [191,  51, 102, 255],
                [223,  59, 119, 255],
                [255,  68, 136, 255]])
    def testCpts0vs3(self):
        self.doAt((0, 3), [
                [  0,   0,   0, 255],
                [ 31,  31,  31, 255],
                [ 63,  63,  63, 255],
                [127, 127, 127, 255],
                [191, 191, 191, 255],
                [223, 223, 223, 255],
                [255, 255, 255, 255]])

    def testCpts1vs2(self):
        self.doAt((1, 2), [
                [119, 0, 255, 255], 
                [136, 8, 240, 255], 
                [153, 17, 225, 255], 
                [187, 34, 195, 255], 
                [221, 51, 165, 255], 
                [238, 59, 150, 255], 
                [255, 68, 136, 255]])
    def testCpts1vs3(self):
        self.doAt((1, 3), [
                [119, 0, 255, 255], 
                [136, 31, 255, 255], 
                [153, 63, 255, 255], 
                [187, 127, 255, 255], 
                [221, 191, 255, 255], 
                [238, 223, 255, 255], 
                [255, 255, 255, 255]])
    def testCpts2vs3(self):
        self.doAt((2, 3), [
                [255, 68, 136, 255], 
                [255, 91, 150, 255], 
                [255, 114, 165, 255], 
                [255, 161, 195, 255], 
                [255, 208, 225, 255], 
                [255, 231, 240, 255], 
                [255, 255, 255, 255]])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestQuadraticBezier(unittest.TestCase):
    u = [0, .125, .25, .5, .75, .875, 1]
    cpts = Color(['#000', '#70f', '#f48', '#fff'], '4B')

    def doCVTestFor(self, rawQuestion, rawAnswer):
        q = rawQuestion.astype('B').tolist()
        self.assertEqual(q, rawAnswer)

    def doAt(self, (i, j, k), result):
        bm = bezier.b2; u = self.u; cpts = self.cpts
        self.doCVTestFor(bm.atU(u).atP([cpts[i], cpts[j], cpts[k]]), result)
        self.doCVTestFor(bm.atU(u) * [cpts[i], cpts[j], cpts[k]], result)
        self.doCVTestFor(bm.atP([cpts[i], cpts[j], cpts[k]]).atU(u), result)
        self.doCVTestFor(bm.at([cpts[i], cpts[j], cpts[k]], u), result)
    
    def testCpts0vs1vs2(self):
        self.doAt((0, 1, 2), [
                [0, 0, 0, 255], 
                [30, 1, 57, 255], 
                [60, 4, 104, 255], 
                [123, 17, 161, 255], 
                [188, 38, 172, 255], 
                [221, 52, 159, 255], 
                [255, 68, 136, 255]])
    def testCpts0vs1vs3(self):
        self.doAt((0, 1, 3), [
                [0, 0, 0, 255], 
                [30, 3, 59, 255], 
                [60, 15, 111, 255], 
                [123, 63, 191, 255], 
                [188, 143, 239, 255], 
                [221, 195, 251, 255], 
                [255, 255, 255, 255]])
    def testCpts0vs2vs3(self):
        self.doAt((0, 2, 3), [
                [0, 0, 0, 255], 
                [59, 18, 33, 255], 
                [111, 41, 66, 255], 
                [191, 97, 131, 255], 
                [239, 168, 194, 255], 
                [251, 210, 224, 255], 
                [255, 255, 255, 255]])
    def testCpts1vs2vs3(self):
        self.doAt((1, 2, 3), [
                [119, 0, 255, 255], 
                [150, 18, 228, 255], 
                [178, 41, 210, 255], 
                [221, 97, 195, 255], 
                [246, 168, 210, 255], 
                [252, 210, 228, 255], 
                [255, 255, 255, 255]])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestCubicBezier(unittest.TestCase):
    u = [0, .125, .25, .5, .75, .875, 1]
    cpts = Color(['#000', '#70f', '#f48', '#fff'], '4B')

    def doCVTestFor(self, rawQuestion, rawAnswer):
        q = rawQuestion.astype('B').tolist()
        self.assertEqual(q, rawAnswer)

    def test(self):
        bm = bezier.b3; u = self.u; cpts = self.cpts
        result = [
            [0, 0, 0, 255], 
            [45, 3, 79, 255], 
            [90, 13, 130, 255], 
            [172, 57, 178, 255], 
            [231, 136, 200, 255], 
            [248, 190, 220, 255], 
            [255, 255, 255, 255]]

        self.doCVTestFor(bm.atU(u).atP(cpts), result)
        self.doCVTestFor(bm.atU(u) * cpts, result)
        self.doCVTestFor(bm.atP(cpts).atU(u), result)
        self.doCVTestFor(bm.at(cpts, u), result)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

