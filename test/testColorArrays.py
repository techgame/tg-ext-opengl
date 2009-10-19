#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
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
from TG.ext.openGL.data import ColorArray, Color

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestColorArrays(unittest.TestCase):
    def doCVTestFor(self, rawQuestion, rawAnswer):
        question = Color(rawQuestion)
        answer = rawAnswer
        self.assertEqual(question.tolist(), answer)

        question = ColorArray(rawQuestion)
        answer = rawAnswer
        self.assertEqual(question.tolist(), [answer])

        question = Color(rawAnswer)
        answer = rawAnswer
        self.assertEqual(question.tolist(), answer)

    def testCAfromHex1x1(self):
        self.doCVTestFor("#3", [0x33, 0x33, 0x33, 0xff])
        self.doCVTestFor("#3:", [0x33, 0x33, 0x33, 0xff])

    def testCAfromHex1x2(self):
        self.doCVTestFor("#3a", [0x3a, 0x3a, 0x3a, 0xff])
        self.doCVTestFor("#3a:", [0x3a, 0x3a, 0x3a, 0xff])

    def testCAfromHex2by1(self):
        self.doCVTestFor("#3:a", [0x33, 0x33, 0x33, 0xaa])
        self.doCVTestFor("#3:a:", [0x33, 0x33, 0x33, 0xaa])

    def testCAfromHex2by2(self):
        self.doCVTestFor("#3a:f9", [0x3a, 0x3a, 0x3a, 0xf9])
        self.doCVTestFor("#3a:f9:", [0x3a, 0x3a, 0x3a, 0xf9])

    def testCAfromHex3by1(self):
        self.doCVTestFor("#3af", [0x33, 0xaa, 0xff, 0xff])
        self.doCVTestFor("#3:a:f", [0x33, 0xaa, 0xff, 0xff])
        self.doCVTestFor("#3:a:f:", [0x33, 0xaa, 0xff, 0xff])

    def testCAfromHex3by2(self):
        self.doCVTestFor("#3af9b7", [0x3a, 0xf9, 0xb7, 0xff])
        self.doCVTestFor("#3a:f9:b7", [0x3a, 0xf9, 0xb7, 0xff])
        self.doCVTestFor("#3a:f9:b7:", [0x3a, 0xf9, 0xb7, 0xff])

    def testCAfromHex4by1(self):
        self.doCVTestFor("#3af9", [0x33, 0xaa, 0xff, 0x99])
        self.doCVTestFor("#3:a:f:9", [0x33, 0xaa, 0xff, 0x99])
        self.doCVTestFor("#3:a:f:9:", [0x33, 0xaa, 0xff, 0x99])

    def testCAfromHex4by2(self):
        self.doCVTestFor("#8142feac", [0x81, 0x42, 0xfe, 0xac])
        self.doCVTestFor("#81:42:fe:ac", [0x81, 0x42, 0xfe, 0xac])
        self.doCVTestFor("#81:42:fe:ac:", [0x81, 0x42, 0xfe, 0xac])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if 1:
    class TestFloatColorArrays(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(rawQuestion, '4f')
            answer = ColorArray(rawAnswer, '4B')

            self.assertNotEqual(answer.tolist(), question.tolist())
            self.assertEqual(question.xformAs(answer.edtype).tolist(), answer.tolist())
            self.assert_(allclose(255*question, answer))
            self.assert_(allclose(question, answer*(1./255.)))
            self.assertEqual(answer.xformAs(question.edtype).tolist(), question.tolist())
            self.assertNotEqual(answer.tolist(), question.tolist())

    class TestColorArraysAssign(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(3)
            question[0] = rawQuestion

            # note that the arrays don't baby-sit your values for you...
            question[1] = rawAnswer
            question[1] /= 255.

            question[2].xformFrom(ColorArray(rawAnswer, '4B'))

            self.assert_(allclose(255*question[0], rawAnswer))
            self.assert_(allclose(255*question[1], rawAnswer))
            self.assert_(allclose(255*question[2], rawAnswer))

if 1:
    class TestColorArrayswithN6(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray([rawQuestion]*6)
            answer = [rawAnswer]*6
            self.assertEqual(question.tolist(), answer)

    class TestDualColorArrays(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(rawQuestion)
            answer = ColorArray(rawAnswer)
            self.assertEqual(question.tolist(), answer.tolist())

    class TestDualColorArrayswithN6(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray([rawQuestion]*6)
            answer = ColorArray([rawAnswer]*6)
            self.assertEqual(question.tolist(), answer.tolist())

if 1:
    class TestColorArrays4(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(rawQuestion, '4B')
            answer = rawAnswer
            self.assertEqual(question.tolist(), [answer])

    class TestDualColorArrays4(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(rawQuestion, '4B')
            answer = ColorArray(rawAnswer, '4B')
            self.assertEqual(question.tolist(), answer.tolist())

    class TestColorArrays4withN6(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray([rawQuestion]*6, '4B')
            answer = [rawAnswer]*6
            self.assertEqual(question.tolist(), answer)

    class TestDualColorArrays4withN6(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray([rawQuestion]*6, '4B')
            answer = ColorArray([rawAnswer]*6, '4B')
            self.assertEqual(question.tolist(), answer.tolist())

if 1:
    class TestColorArrays3(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(rawQuestion, '3B')
            answer = rawAnswer[:3]
            self.assertEqual(question.tolist(), [answer])

    class TestDualColorArrays3(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(rawQuestion, '3B')
            answer = ColorArray(rawAnswer[:3], '3B')
            self.assertEqual(question.tolist(), answer.tolist())

    class TestColorArrays3withN6(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray([rawQuestion]*6, '3B')
            answer = [rawAnswer[:3]]*6
            self.assertEqual(question.tolist(), answer)

    class TestDualColorArrays3withN6(TestColorArrays):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray([rawQuestion]*6, '3B')
            answer = ColorArray([rawAnswer[:3]]*6, '3B')
            self.assertEqual(question.tolist(), answer.tolist())

if 1:
    class TestColorArrayDefaults(unittest.TestCase):
        def doCVTestFor(self, rawQuestion, rawAnswer):
            question = ColorArray(rawQuestion)
            answer = rawAnswer
            self.assertEqual(question.tolist(), answer)

        def testCAn0(self):
            self.doCVTestFor(None, [[1., 1., 1., 1.]])
            self.doCVTestFor(0, [])
            self.doCVTestFor([], [])
            self.doCVTestFor(ColorArray(shape=(1, 0,-1)), [[]])
            self.doCVTestFor(ColorArray(shape=(1, 0, 1,-1)), [[]])
            self.doCVTestFor(ColorArray(shape=(1, 0, 3,-1)), [[]])
            self.doCVTestFor(ColorArray(shape=(3, 0, 1,-1)), [[], [], []])

        def testCAn1(self):
            self.doCVTestFor(1, [[1., 1., 1., 1.]])
        def testCAn5(self):
            self.doCVTestFor(5, 5*[[1., 1., 1., 1.]])

        def testCAdata(self):
            self.doCVTestFor([1., 2., 3., 4.], [[1., 2., 3., 4.]])
            self.doCVTestFor([[1., 2., 3., 4.]], [[1., 2., 3., 4.]])
            self.doCVTestFor(ColorArray([1., 2., 3., 4.]), [[1., 2., 3., 4.]])

        def testCAdataAndShape1(self):
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], shape=(1, 1,-1)), [[[1., 2., 3., 4.]]])
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], '4B', shape=(1, 1,-1)), [[[1, 2, 3, 4]]])
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], '4f', shape=(1, 1,-1)), [[[1, 2, 3, 4]]])
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], '4d', shape=(1, 1,-1)), [[[1., 2., 3., 4.]]])

        def testCAdataAndShape5(self):
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], shape=(5,-1)), 5*[[1., 2., 3., 4.]])
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], '4B', shape=(5,-1)), 5*[[1., 2., 3., 4.]])
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], '4f', shape=(5,-1)), 5*[[1., 2., 3., 4.]])
            self.doCVTestFor(ColorArray([1., 2., 3., 4.], '4d', shape=(5,-1)), 5*[[1., 2., 3., 4.]])

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def testCAshape1(self):
            self.doCVTestFor(ColorArray([0], shape=(1,-1)), [[0., 0., 0., 0.]])
            self.doCVTestFor(ColorArray([0L], shape=(1,-1)), [[0., 0., 0., 0.]])
            self.doCVTestFor(ColorArray([0.], shape=(1,-1)), [[0., 0., 0., 0.]])

        def testCAshape5(self):
            self.doCVTestFor(ColorArray([0], shape=(5,-1)), 5*[[0., 0., 0., 0.]])
            self.doCVTestFor(ColorArray([0L], shape=(5,-1)), 5*[[0., 0., 0., 0.]])
            self.doCVTestFor(ColorArray([0.], shape=(5,-1)), 5*[[0., 0., 0., 0.]])

        def testCAshape5(self):
            self.doCVTestFor(ColorArray([-2], shape=(5,-1)), 5*[[-2., -2., -2., -2.]])
            self.doCVTestFor(ColorArray([-4L], shape=(5,-1)), 5*[[-4., -4., -4., -4.]])
            self.doCVTestFor(ColorArray([-.25], shape=(5,-1)), 5*[[-.25,-.25,-.25,-.25]])

        def testCAshape5by2(self):
            self.doCVTestFor(ColorArray([-2], shape=(5, 2,-1)), 5*[2*[[-2., -2., -2., -2.]]])
            self.doCVTestFor(ColorArray([-4L], shape=(5, 2,-1)), 5*[2*[[-4., -4., -4., -4.]]])
            self.doCVTestFor(ColorArray([-.25], shape=(5, 2,-1)), 5*[2*[[-.25,-.25,-.25,-.25]]])

if 1:
    class TestColorBlend(unittest.TestCase):
        cpts = ColorArray(['#000', '#fff'], '4B')

        def doCVTestFor(self, rawQuestion, rawAnswer):
            self.assertEqual(rawQuestion.squeeze().tolist(), rawAnswer.squeeze().tolist())
        def testBlend0(self):
            self.doCVTestFor(self.cpts[0].blend(self.cpts[1], 0.), self.cpts[0])
        def testBlend1(self):
            self.doCVTestFor(self.cpts[0].blend(self.cpts[1], 1.), self.cpts[1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

