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

from functools import partial
from numpy import array
from ..raw import gl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_dtype_gltype_map = {
    'B': (gl.GL_UNSIGNED_BYTE,'ub'),
    'b': (gl.GL_BYTE,'b'),
    'H': (gl.GL_UNSIGNED_SHORT,'us'),
    'h': (gl.GL_SHORT,'s'),
    'I': (gl.GL_UNSIGNED_INT,'ui'),
    'L': (gl.GL_UNSIGNED_INT,'ui'),
    'i': (gl.GL_INT,'i'),
    'l': (gl.GL_INT,'i'),
    'f': (gl.GL_FLOAT,'f'),
    'd': (gl.GL_DOUBLE,'d'),
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

arrayFormatInfo = {
    None: (None, '', True, '', 0),
    'vertex': (gl.GL_VERTEX_ARRAY, 'glVertex', True, 'hlifd', [2,3,4]),
    'texture_coord': (gl.GL_TEXTURE_COORD_ARRAY, 'glTexCoord', True, 'hlifd', [1,2,3,4]),
    'multi_texture_coord': (gl.GL_TEXTURE_COORD_ARRAY, 'glTexCoord', 'glMultiTexCoord', 'hlifd', [1,2,3,4]),
    'normal': (gl.GL_NORMAL_ARRAY, 'glNormal', True, 'bhlifd', [3]),
    'color': (gl.GL_COLOR_ARRAY, 'glColor', True, 'BHLIbhlifd', [1,3,4]),
    'secondary_color': (gl.GL_SECONDARY_COLOR_ARRAY, 'glSecondaryColor', True, 'BHLIbhlifd', [1,3]), 
    'color_index': (gl.GL_INDEX_ARRAY, 'glIndex', True, 'Bhlifd', 1),
    'fog_coord': (gl.GL_FOG_COORD_ARRAY, 'glFogCoord', True, 'fd', 1),
    'edge_flag': (gl.GL_EDGE_FLAG_ARRAY, 'glEdgeFlag', True, 'B', 1),
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_arrayViewRegistry = {}
def _registerArrayView(klass):
    klass._configClass()
    _arrayViewRegistry[klass.kind] = klass

def arrayView(kind):
    avFactory = _arrayViewRegistry[kind]
    return avFactory()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ArrayView(object):
    arrayFormatInfo = arrayFormatInfo

    kind = None
    glid_kind = None
    glid_buffer = gl.GL_ARRAY_BUFFER

    glfn_single = None
    glfn_group = None

    def config(klassOrSelf, kind=None):
        if kind is None:
            kind = klassOrSelf.kind
        klassOrSelf.kind = kind
        afinfo = klassOrSelf.arrayFormatInfo[kind]
        klassOrSelf.glid_kind = afinfo[0]

        if isinstance(afinfo[4], (int, long)):
            # dimension is not used in format
            fmt = '%(fmt)s'
        else: fmt = '%(dim)d%(fmt)sv'

        klassOrSelf.glfn_single = afinfo[1] + fmt
        klassOrSelf.glfn_group = afinfo[1] + 'Pointer'
        return klassOrSelf
    _configClass = classmethod(config)

    def bind(self, arr, gl=gl):
        arr = array(arr, copy=False, subok=1)
        glid_type, glc_fmt = _dtype_gltype_map[arr.dtype.char]
        glc_dim = arr.shape[-1]

        if len(arr.strides) >= 2:
            glgroup_raw = getattr(gl, self.glfn_group)
            self._glsend = partial(glgroup_raw, glc_dim, glid_type, arr.strides[-2], arr.ctypes)
            self._glenable = partial(gl.glEnableClientState, self.glid_kind)
            self._gldisable = partial(gl.glDisableClientState, self.glid_kind)
        else: 
            glsingle_raw = getattr(gl, self.glfn_single % dict(dim=glc_dim, fmt=glc_fmt))
            self._glsend = partial(glsingle_raw, arr.ctypes)
            self._glenable = lambda: None
            self._gldisable = lambda: None

    def enable(self): 
        self._glenable()
    def disable(self): 
        self._gldisable()
    def send(self):
        self._glsend()

_registerArrayView(ArrayView)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VertexArrayView(ArrayView): 
    kind = 'vertex'
_registerArrayView(VertexArrayView)

class TexCoordArrayView(ArrayView): 
    kind = 'texture_coord'
_registerArrayView(TexCoordArrayView)

class MultiTexCoordArrayView(ArrayView): 
    kind = 'multi_texture_coord'
_registerArrayView(MultiTexCoordArrayView)

class NormalArrayView(ArrayView): 
    kind = 'normal'
_registerArrayView(NormalArrayView)

class ColorArrayView(ArrayView): 
    kind = 'color'
_registerArrayView(ColorArrayView)

class SecondaryColorArrayView(ArrayView): 
    kind = 'secondary_color'
_registerArrayView(SecondaryColorArrayView)

class ColorIndexArrayView(ArrayView): 
    kind = 'color_index'
_registerArrayView(ColorIndexArrayView)

class FogCoordArrayView(ArrayView): 
    kind = 'fog_coord'
_registerArrayView(FogCoordArrayView)

class EdgeFlagArrayView(ArrayView): 
    kind = 'edge_flag'
_registerArrayView(EdgeFlagArrayView)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Add in draw array views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from . import drawArrayViews

