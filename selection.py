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
        selection = self._processHits(hitRecords, self._namedItems, incZDepth)
        self._namedItems.clear()
        return selection

    def _processHits(self, hitRecords, namedItems, incZDepth=False):
        offset = 0
        buffer = self._buffer
        result = []
        for hit in xrange(hitRecords):
            nameRecords, minZ, maxZ = buffer[offset:offset+3]
            names = list(buffer[offset+3:offset+3+nameRecords])
            offset += 3+nameRecords

            namedHit = [namedItems[n] for n in names]
            if incZDepth:
                namedHit = ((minZ, maxZ), namedHit)
            result.append(namedHit)
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def load(self, *items):
        n = id(items[0])
        self._namedItems[n] = items
        gl.glLoadName(n)
    def push(self, *items):
        n = id(items[0])
        self._namedItems[n] = items
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

class ColorSelector(Selector):
    """Runs a selection pass using the color buffer to allow for fragments to
    affect what gets picked.  This enables textures (and alpha) to affect the
    shape of objects."""

