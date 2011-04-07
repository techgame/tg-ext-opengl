##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from functools import partial
from numpy import asarray
from ..raw import gl
from .arrayViews import _dtype_gltype_map, _registerArrayView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

drawModes = {
    None: gl.GL_POINTS,
    'pts': gl.GL_POINTS,
    'points': gl.GL_POINTS,

    'lines': gl.GL_LINES,
    'lineLoop': gl.GL_LINE_LOOP,
    'lineStrip': gl.GL_LINE_STRIP,

    'tris': gl.GL_TRIANGLES,
    'triangles': gl.GL_TRIANGLES,
    'triStrip': gl.GL_TRIANGLE_STRIP,
    'triangleStrip': gl.GL_TRIANGLE_STRIP,
    'triFan': gl.GL_TRIANGLE_FAN,
    'triangleFan': gl.GL_TRIANGLE_FAN,

    'quads': gl.GL_QUADS,
    'quadStrip': gl.GL_QUAD_STRIP,
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DrawArrayView(object):
    drawModes = drawModes
    glid_buffer = gl.GL_ELEMENT_ARRAY_BUFFER
    kind = 'draw_array'
    
    def config(klassOrSelf, kind=None):
        pass
    _configClass = classmethod(config)

    def bind(self, mode, arr, gl=gl):
        if isinstance(arr, (int, long)):
            arr = asarray([0, arr], dtype='i')
        elif isinstance(arr, slice):
            arr = asarray([arr.start, arr.stop], dtype='i')
        else: arr = asarray(arr, dtype='i')
        glid_mode = self.drawModes.get(mode, mode)

        self._glsingle = partial(gl.glDrawArrays, glid_mode, arr[0], arr[1])
        if arr.ndim > 1:
            self._glgroup = partial(gl.glMultiDrawArrays, glid_mode, arr[0].ctypes, arr[1].ctypes, arr.shape[1])
        else: self._glgroup = self._glsingle
        return self

    def one(self):
        self._glsingle()
    def send(self):
        self._glgroup()

    def _glNoOP(self): pass
    _glsingle = _glNoOP
    _glgroup = _glNoOP

_registerArrayView(DrawArrayView)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DrawElementArrayView(DrawArrayView):
    kind = 'draw_elements'
    def bind(self, mode, arr, gl=gl):
        arr = asarray(arr)

        glid_type = _dtype_gltype_map[arr.dtype.char][0]
        glid_mode = self.drawModes.get(mode, mode)

        self._glsingle = partial(gl.glDrawElements, glid_mode, arr.size, glid_type, arr.ctypes)

        #XXX: Implement this when used
        #self._glgroup = partial(gl.glMultiDrawElements, glid_mode, arr[0].ctypes, glid_type, arr[1].ctypes)
        self._glgroup = self._glsingle
        return self

_registerArrayView(DrawElementArrayView)

