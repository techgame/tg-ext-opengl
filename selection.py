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

import functools
import itertools

from .raw import gl, glu

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Selector(object):
    def start(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def finish(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def load(self, item):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def push(self, item):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def pop(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NameSelector(Selector):
    """Uses the builtin name-based geometry selection model provided by OpenGL"""

    def __init__(self, bufferSize=1024):
        Selector.__init__(self)
        self.setBufferSize(bufferSize)
        self._namedItems = {}

    _buffer = (gl.GLuint*0)()
    def getBufferSize(self):
        return len(self._buffer)
    def setBufferSize(self, size):
        self._buffer = (gl.GLuint*size)()
    bufferSize = property(getBufferSize, setBufferSize)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def start(self):
        self._namedItems.clear()
        gl.glSelectBuffer(self.bufferSize, self._buffer)
        gl.glRenderMode(gl.GL_SELECT)
        gl.glInitNames()

    def finish(self, incZDepth=False):
        hitRecords = gl.glRenderMode(gl.GL_RENDER)
        selection = self._processHits(hitRecords, self.getNamedItem, incZDepth)
        self._namedItems.clear()
        return selection

    def _processHits(self, hitRecords, getNamedItem, incZDepth=False):
        offset = 0
        buffer = self._buffer
        result = []
        for hit in xrange(hitRecords):
            nameRecords, minZ, maxZ = buffer[offset:offset+3]
            names = list(buffer[offset+3:offset+3+nameRecords])
            offset += 3+nameRecords

            namedHit = [getNamedItem(n) for n in names]
            if incZDepth:
                namedHit = ((minZ, maxZ), namedHit)
            result.append(namedHit)
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getNamedItem(self, n):
        return self._namedItems[n]
    def addItems(self, items):
        n = id(items[0])
        self._namedItems[n] = items
        return n

    def load(self, *items):
        n = self.addItems(items)
        gl.glLoadName(n)
    def push(self, *items):
        n = self.addItems(items)
        gl.glPushName(n)
    def pop(self):
        gl.glPopName()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    c_viewport = (gl.GLint*4)
    def pickMatrix(self, pos, size, vpbox):
        gl.glTranslatef(
                (vpbox[2] - 2*(pos[0] - vpbox[0]))/size[0], 
                (vpbox[3] - 2*(pos[1] - vpbox[1]))/size[1], 
                0)
        gl.glScalef(
                vpbox[2]/size[0],
                vpbox[3]/size[1],
                1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StencilSelector(Selector):
    def __init__(self):
        Selector.__init__(self)
        self._namedItems = {}
        self._nameStack = []

    @classmethod
    def checkViable(klass):
        isViable = self._isViable
        if isViable is not None:
            return isViable

        v = gl.GLint(0)
        gl.glGetIntegerv(gl.GL_STENCIL_BITS, gl.byref(v))
        v = v.value
        isViable = (v < 8)
        if not isViable:
            print 'WARNING: need at least 8 stencil bits, only found', v
            
        return isViable

    def start(self):
        self._namedItems.clear()
        self._nameStack[:] = []
        self.nextId = itertools.count(0x1).next

        self._setCurrentName = functools.partial(gl.glStencilFunc, gl.GL_ALWAYS, mask=-1)

        gl.glClearStencil(0)
        gl.glClear(gl.GL_STENCIL_BUFFER_BIT)

        gl.glStencilOp(gl.GL_KEEP, gl.GL_KEEP, gl.GL_REPLACE)
        self._setCurrentName(0)
        gl.glEnable(gl.GL_STENCIL_TEST)

    def finish(self):
        sel = []
        gl.glDisable(gl.GL_STENCIL_TEST)

        (x,y),(w,h) = self.pickRect
        if x>0 and y>0:
            vbuf = (gl.GLuint * max(1, w*h))(0)
            gl.glReadPixels(int(x),int(y),int(w),int(h),
                gl.GL_STENCIL_INDEX, gl.GL_UNSIGNED_INT, vbuf)

            sel = self._processHits(vbuf, self.getNamedItem)

        self._namedItems.clear()
        self._nameStack[:] = []
        return sel

    def _processHits(self, vbuf, getNamedItem):
        r = []
        for hit in vbuf:
            if hit>0:
                r.append([getNamedItem(hit)])
        return r

    def pickMatrix(self, pos, size, vpbox):
        self.pickRect = pos,size

    def getNamedItem(self, n):
        return self._namedItems[n]
    def addItems(self, items):
        n = self.nextId()
        self._namedItems[n] = items
        return n

    def load(self, *items):
        n = self.addItems(items)
        self._setCurrentName(n)

    def push(self, *items):
        n = self.addItems(items)
        self._nameStack.append(n)
        self._setCurrentName(n)

    def pop(self):
        n = self._nameStack.pop()
        self._setCurrentName(n)

