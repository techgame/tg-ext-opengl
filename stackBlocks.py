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

from contextlib import contextmanager

from TG.openGL.raw import gl
from TG.openGL.raw.errors import GLError

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getInfo():
   return {
        'vendor': gl.glGetString(gl.GL_VENDOR),
        'renderer': gl.glGetString(gl.GL_RENDERER),
        'version': gl.glGetString(gl.GL_VERSION),
        'extensions': gl.glGetString(gl.GL_EXTENSIONS),
        }

def _glPurgeStackOf(popStack, count):
    for idx in xrange(count):
        popStack()

@contextmanager
def glName(name):
    gl.glPushName(name)
    try:
        yield
    finally:
        gl.glPopName()

def glGetValueFor(glid):
    v = gl.GLint(0)
    gl.glGetIntegerv(glid, gl.byref(v))
    return v.value

def glPurgeNames():
    count = glGetValueFor(gl.GL_NAME_STACK_DEPTH)
    _glPurgeStackOf(gl.glPopName, count)

@contextmanager
def glClientAttribs(mask):
    gl.glPushClientAttrib(mask)
    try:
        yield
    finally:
        gl.glPopClientAttrib()

def glPurgeClientAttribs():
    count = glGetValueFor(gl.GL_CLIENT_ATTRIB_STACK_DEPTH)
    _glPurgeStackOf(gl.glPopClientAttrib, count)

@contextmanager
def glAttribs(mask):
    gl.glPushAttrib(mask)
    try:
        yield
    finally:
        gl.glPopAttrib()

def glPurgeAttribs():
    count = glGetValueFor(gl.GL_ATTRIB_STACK_DEPTH)
    _glPurgeStackOf(gl.glPopAttrib, count)

@contextmanager
def glImmediate(mode=None):
    gl.glBegin(mode)
    try:
        yield
    finally:
        gl.glEnd()
glBlock = glImmediate

@contextmanager
def glMatrix(mode=None):
    if mode is not None:
        gl.glMatrixMode(mode)
        gl.glPushMatrix()
        try:
            yield
        finally:
            gl.glMatrixMode(mode)
            gl.glPopMatrix()
            gl.glMatrixMode(gl.GL_MODEL_VIEW)

    else:
        gl.glPushMatrix()
        try:
            yield
        finally:
            gl.glPopMatrix()

_matrixStackDepth = {
        gl.GL_MODELVIEW: gl.GL_MODELVIEW_STACK_DEPTH,
        gl.GL_PROJECTION: gl.GL_PROJECTION_STACK_DEPTH,
        gl.GL_TEXTURE: gl.GL_TEXTURE_STACK_DEPTH,
        }
def glPurgeMatrix(mode=None, matrixStackDepth=_matrixStackDepth):
    stackDepthToken = matrixStackDepth[mode or glGetValueFor(gl.GL_MATRIX_MODE)]
    count = glGetValueFor(stackDepthToken)

    if mode is None:
        _glPurgeStackOf(gl.glPopMatrix, count)
        gl.glLoadIdentity()
    else:
        gl.glMatrixMode(mode)
        _glPurgeStackOf(gl.glPopMatrix, count)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)

def glPurgeAllStacks():
    glPurgeMatrix(gl.GL_MODELVIEW)
    glPurgeMatrix(gl.GL_PROJECTION)
    glPurgeMatrix(gl.GL_TEXTURE)
    glPurgeAttribs()
    glPurgeClientAttribs()
    glPurgeNames()

