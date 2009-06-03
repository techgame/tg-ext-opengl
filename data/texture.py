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

import sys
import weakref
from bisect import bisect_left

from numpy import array, asarray, zeros
from ctypes import cast, byref, c_void_p

from TG.geomath.data.box import Box

from ..raw import gl, glext
from ..raw import errors as glErrors

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class glTexParamProperty(object):
    _as_parameter_ = None
    raiseErrors = True
    def __init__(self, propertyEnum, raiseErrors=True):
        self._as_parameter_ = gl.GLenum(propertyEnum)
        if raiseErrors != self.raiseErrors:
            self.raiseErrors = raiseErrors

    def __get__(self, obj, klass=None):
        if obj is None: 
            return self

        cValue = self.GLParamType()
        try:
            self.glGetTexParameter(obj.target, self, cValue)
            return cValue.value
        except glErrors.GLError:
            if self.raiseErrors: raise
    get = __get__

    def __set__(self, obj, value):
        if not isinstance(value, (list, tuple)):
            value = (value,)
        cValue = self.GLParamType(*value)
        try:
            self.glSetTexParameter(obj.target, self, cValue)
        except glErrors.GLError:
            if self.raiseErrors: raise
    set = __set__

class glTexParamProperty_i(glTexParamProperty):
    GLParamType = (gl.GLint*1)
    glGetTexParameter = property(lambda self: gl.glGetTexParameteriv)
    glSetTexParameter = property(lambda self: gl.glTexParameteriv)

class glTexParamProperty_f(glTexParamProperty):
    GLParamType = (gl.GLfloat*1)
    glGetTexParameter = property(lambda self: gl.glGetTexParameteriv)
    glSetTexParameter = property(lambda self: gl.glTexParameteriv)

class glTexParamProperty_4f(glTexParamProperty):
    GLParamType = (gl.GLfloat*4)
    glGetTexParameter = property(lambda self: gl.glGetTexParameterfv)
    glSetTexParameter = property(lambda self: gl.glTexParameterfv)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PixelStore(object):
    alignment = 4
    swapBytes = False
    lsbFirst = False

    rowLength = imgHeight = 0 # 0 means use for row length to image height
    skipPixels = skipRows = skipImages = 0

    fmtPNames = {
        'alignment': (gl.GL_UNPACK_ALIGNMENT, gl.GL_PACK_ALIGNMENT),
        'swapBytes': (gl.GL_UNPACK_SWAP_BYTES, gl.GL_PACK_SWAP_BYTES),
        'lsbFirst': (gl.GL_UNPACK_LSB_FIRST, gl.GL_PACK_LSB_FIRST),

        'rowLength': (gl.GL_UNPACK_ROW_LENGTH, gl.GL_PACK_ROW_LENGTH),
        'imgHeight': (gl.GL_UNPACK_IMAGE_HEIGHT, gl.GL_PACK_IMAGE_HEIGHT),
                                        
        'skipPixels': (gl.GL_UNPACK_SKIP_ROWS, gl.GL_PACK_SKIP_ROWS),
        'skipRows': (gl.GL_UNPACK_SKIP_PIXELS, gl.GL_PACK_SKIP_PIXELS),
        'skipImages': (gl.GL_UNPACK_SKIP_IMAGES, gl.GL_PACK_SKIP_IMAGES),
    }
    formatAttrs = None # a list of (pname, newValue, origValue)
    pack = False

    def __init__(self, **kwattrs):
        self.create(**kwattrs)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __setattr__(self, name, value):
        if name in self.fmtPNames:
            self[name] = value
        return object.__setattr__(self, name, value)

    def __getitem__(self, name):
        pname = self.fmtPNames[name][self.pack]
        return self.formatAttrs[pname]
    def __setitem__(self, name, value):
        pname = self.fmtPNames[name][self.pack]
        restoreValue = getattr(self.__class__, name)
        self.formatAttrs[pname] = (value, restoreValue)
        object.__setattr__(self, name, value)
    def __delitem__(self, name):
        pname = self.fmtPNames[name][self.pack]
        del self.formatAttrs[pname]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def create(self, pack=False, **kwattrs):
        self.formatAttrs = {}
        self.pack = pack
        self.set(kwattrs)

    def set(self, val=None, **kwattr):
        for n,v in (val or kwattr).iteritems():
            setattr(self, n, v)

    def select(self):
        for pname, value in self.formatAttrs.iteritems():
            gl.glPixelStorei(pname, value[0])
        return self

    def deselect(self):
        for pname, value in self.formatAttrs.iteritems():
            gl.glPixelStorei(pname, value[1])
        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Texture Image
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextureImageBasic(object):
    srcFormatMap = {
        'rgb': gl.GL_RGB, 'RGB': gl.GL_RGB,
        'rgba': gl.GL_RGBA, 'RGBA': gl.GL_RGBA,

        'bgr': gl.GL_BGR, 'BGR': gl.GL_BGR,
        'bgra': gl.GL_BGRA, 'BGRA': gl.GL_BGRA,

        'ci': gl.GL_COLOR_INDEX, 'color_index': gl.GL_COLOR_INDEX,
        'si': gl.GL_STENCIL_INDEX, 'stencil_index': gl.GL_STENCIL_INDEX,
        'dc': gl.GL_DEPTH_COMPONENT, 'depth': gl.GL_DEPTH_COMPONENT, 'depth_component': gl.GL_DEPTH_COMPONENT,

        'r': gl.GL_RED, 'R': gl.GL_RED, 'red': gl.GL_RED,
        'g': gl.GL_GREEN, 'G': gl.GL_GREEN, 'green': gl.GL_GREEN,
        'b': gl.GL_BLUE, 'B': gl.GL_BLUE, 'blue': gl.GL_BLUE,
        'a': gl.GL_ALPHA, 'A': gl.GL_ALPHA, 'alpha': gl.GL_ALPHA,

        'l': gl.GL_LUMINANCE, 'L': gl.GL_LUMINANCE, 'luminance': gl.GL_LUMINANCE,
        'la': gl.GL_LUMINANCE_ALPHA, 'LA': gl.GL_LUMINANCE_ALPHA, 'luminance_alpha': gl.GL_LUMINANCE_ALPHA,
    }

    dataTypeMap = {
        'bitmap': gl.GL_BITMAP,

        'ub': gl.GL_UNSIGNED_BYTE, 'ubyte': gl.GL_UNSIGNED_BYTE, 'B': gl.GL_UNSIGNED_BYTE,
        'b': gl.GL_BYTE, 'byte': gl.GL_BYTE,

        'us': gl.GL_UNSIGNED_SHORT, 'ushort': gl.GL_UNSIGNED_SHORT, 'S': gl.GL_UNSIGNED_SHORT,
        's': gl.GL_SHORT, 'short': gl.GL_SHORT,

        'ui': gl.GL_UNSIGNED_INT, 'uint': gl.GL_UNSIGNED_INT, 'I': gl.GL_UNSIGNED_INT,
        'ul': gl.GL_UNSIGNED_INT, 'ulong': gl.GL_UNSIGNED_INT, 'L': gl.GL_UNSIGNED_INT,
        'i': gl.GL_INT, 'int': gl.GL_INT, 'l': gl.GL_INT, 'long': gl.GL_INT,

        'f': gl.GL_FLOAT, 'f32': gl.GL_FLOAT, 'float': gl.GL_FLOAT, 'float32': gl.GL_FLOAT,

        'ub332': gl.GL_UNSIGNED_BYTE_3_3_2, 'ub233r': gl.GL_UNSIGNED_BYTE_2_3_3_REV,
        'us565': gl.GL_UNSIGNED_SHORT_5_6_5, 'us565r': gl.GL_UNSIGNED_SHORT_5_6_5_REV,
        'us4444': gl.GL_UNSIGNED_SHORT_4_4_4_4, 'us4444r': gl.GL_UNSIGNED_SHORT_4_4_4_4_REV,
        'us5551': gl.GL_UNSIGNED_SHORT_5_5_5_1, 'us1555r': gl.GL_UNSIGNED_SHORT_1_5_5_5_REV,
        'ui8888': gl.GL_UNSIGNED_INT_8_8_8_8, 'ui8888r': gl.GL_UNSIGNED_INT_8_8_8_8_REV, 
        'uiAAA2': gl.GL_UNSIGNED_INT_10_10_10_2, 'ui2AAAr': gl.GL_UNSIGNED_INT_2_10_10_10_REV, }
    border = False

    _dataTypeSizeMap = {
        1: (1, False), 
        2: (2, False), 
        3: (3, False), 
        4: (4, False), 

        gl.GL_UNSIGNED_BYTE: (1, False),
        gl.GL_BYTE: (1, False),
        gl.GL_BITMAP: (1, False),
        gl.GL_UNSIGNED_SHORT: (2, False),
        gl.GL_SHORT: (2, False),
        gl.GL_UNSIGNED_INT: (4, False),
        gl.GL_INT: (4, False),
        gl.GL_FLOAT: (4, False),

        gl.GL_UNSIGNED_BYTE_3_3_2: (1, True),
        gl.GL_UNSIGNED_BYTE_2_3_3_REV: (1, True),
        gl.GL_UNSIGNED_SHORT_5_6_5: (2, True),
        gl.GL_UNSIGNED_SHORT_5_6_5_REV: (2, True),
        gl.GL_UNSIGNED_SHORT_4_4_4_4: (2, True),
        gl.GL_UNSIGNED_SHORT_4_4_4_4_REV: (2, True),
        gl.GL_UNSIGNED_SHORT_5_5_5_1: (2, True),
        gl.GL_UNSIGNED_SHORT_1_5_5_5_REV: (2, True),
        gl.GL_UNSIGNED_INT_8_8_8_8: (4, True),
        gl.GL_UNSIGNED_INT_8_8_8_8_REV: (4, True),
        gl.GL_UNSIGNED_INT_10_10_10_2: (4, True),
        gl.GL_UNSIGNED_INT_2_10_10_10_REV: (4, True),
        }
    _dataComponentsMap = {
        gl.GL_RGB: 3, gl.GL_RGBA: 4,
        gl.GL_BGR: 3, gl.GL_BGRA: 4,
        gl.GL_COLOR_INDEX: 1, gl.GL_STENCIL_INDEX: 1, gl.GL_DEPTH_COMPONENT: 1,
        gl.GL_RED: 1, gl.GL_GREEN: 1, gl.GL_BLUE: 1, gl.GL_ALPHA: 1, 
        gl.GL_LUMINANCE: 1, gl.GL_LUMINANCE_ALPHA: 2, 
    }

    def __init__(self, *args, **kwattrs):
        super(TextureImageBasic, self).__init__()

        self.create(*args, **kwattrs)

    def create(self, *args, **kwattrs):
        self.set(kwattrs)

    def set(self, val=None, **kwattr):
        for n,v in (val or kwattr).iteritems():
            setattr(self, n, v)

    def getDataTypeSize(self):
        byteSize, compIncluded = self._dataTypeSizeMap[self.dataType]
        if not compIncluded:
            byteSize *= self._dataComponentsMap[self.format]
        return byteSize

    def getSizeInBytes(self):
        byteSize = self.getDataTypeSize()

        if self._pixelStore:
            alignment = self._pixelStore.alignment
            byteSize += (alignment - byteSize) % alignment

        border = self.border and 2 or 0

        for e in self.size:
            if e > 1:
                byteSize *= e + border
        return byteSize

    _dataType = None
    def getDataType(self):
        return self._dataType
    def setDataType(self, dataType):
        self._dataType = dataType
    # dataType should be: gl.GL_UNSIGNED_BYTE, gl.GL_BYTE, gl.GL_BITMAP, gl.GL_UNSIGNED_SHORT, gl.GL_SHORT, gl.GL_UNSIGNED_INT, gl.GL_INT, gl.GL_FLOAT, ...
    dataType = property(getDataType, setDataType)

    _format = None
    def getFormat(self):
        return self._format
    def setFormat(self, format):
        if isinstance(format, basestring):
            format = self.srcFormatMap[format]
        self._format = format
    # format should be: gl.GL_COLOR_INDEX,  gl.GL_RED, gl.GL_GREEN, gl.GL_BLUE, gl.GL_ALPHA,  gl.GL_RGB,  gl.GL_BGR  gl.GL_RGBA, gl.GL_BGRA, gl.GL_LUMINANCE, gl.GL_LUMINANCE_ALPHA
    format = property(getFormat, setFormat)

    _pointer = None
    def getPointer(self):
        return self._pointer
    ptr = property(getPointer)

    def clear(self):
        self.newPixelStore()
        self.texClear()

    _rawData = None
    def texData(self, rawData, pointer, pixelStoreSettings):
        if pixelStoreSettings:
            self.updatePixelStore(pixelStoreSettings)
        self._rawData = rawData
        if not pointer:
            self._pointer = c_void_p(None)
        elif isinstance(pointer, (int, long)):
            self._pointer = c_void_p(pointer)
        else:
            self._pointer = cast(pointer, c_void_p)

    def texClear(self, pixelStoreSettings=None):
        self.texData(None, None, pixelStoreSettings)
    texNull = texClear
    def texString(self, strdata, pixelStoreSettings=None):
        self.texData(strdata, strdata, pixelStoreSettings)
    strdata = property(fset=texString)
    def texCData(self, cdata, pixelStoreSettings=None):
        self.texData(cdata, cdata, pixelStoreSettings)
    cdata = property(fset=texCData)
    def texArray(self, array, pixelStoreSettings=None):
        self.texString(array.tostring(), pixelStoreSettings)
    array = property(fset=texArray)

    def texBlank(self):
        # setup the alignment properly
        blankData = self._blank

        nbytes = self.getSizeInBytes()
        if len(blankData) < nbytes:
            blankData = (gl.GLubyte*nbytes*4)()
            self.__class__._blank = blankData

        ps = self.newPixelStore(alignment=1)
        self.texCData(blankData)
    _blank = ()

    def setImageOn(self, texture, level=0, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def setSubImageOn(self, texture, level=0, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def setCompressedImageOn(self, texture, level=0, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def setCompressedSubImageOn(self, texture, level=0, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _pixelStore = None
    def getPixelStore(self):
        if self._pixelStore is None:
            self.newPixelStore()
        return self._pixelStore
    def setPixelStore(self, pixelStore):
        if isinstance(pixelStore, dict):
            self.updatePixelStore(pixelStore)
        self._pixelStore = pixelStore
    def delPixelStore(self):
        if self._pixelStore is not None:
            del self._pixelStore
    pixelStore = property(getPixelStore, setPixelStore, delPixelStore)

    def newPixelStore(self, *args, **kw):
        pixelStore = PixelStore(*args, **kw)
        self.setPixelStore(pixelStore)
        return pixelStore
    def updatePixelStore(self, settings):
        ps = self.getPixelStore()
        ps.set(settings)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def select(self):
        pixelStore = self._pixelStore
        if pixelStore is not None:
            pixelStore.select()
        return self

    def deselect(self):
        pixelStore = self._pixelStore
        if pixelStore is not None:
            pixelStore.deselect()
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    box = Box.property(dtype='i', publish='box')

    def getSize(self):
        return self.box.size
    def setSize(self, size):
        self.box.size = size
    size = property(getSize, setSize)

    def getPos(self):
        return self.box.p0
    def setPos(self, pos):
        self.box.p0 = pos
    pos = property(getPos, setPos)

    def getPosSize(self):
        return (self.pos, self.size)
    def setPosSize(self, pos, size=None):
        if size is None:
            pos, size = pos
        self.pos = pos
        self.size = size
    posSize = property(getPosSize, setPosSize)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextureImage1D(TextureImageBasic):
    box = Box.property([0], [0], dtype='i', publish='box')

    def setImageOn(self, texture, level=0, **kw):
        texture.setImage1d(self, level, **kw)
        return texture
    def setSubImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setSubImage1d(self, level)
        return texture
    def setCompressedImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setCompressedImage1d(self, level)
        return texture
    def setCompressedSubImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setCompressedSubImage1d(self, level)
        return texture

class TextureImage2D(TextureImageBasic):
    box = Box.property([0, 0], [0, 0], dtype='i', publish='box')

    def setImageOn(self, texture, level=0, **kw):
        texture.setImage2d(self, level, **kw)
        return texture
    def setSubImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setSubImage2d(self, level)
        return texture
    def setCompressedImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setCompressedImage2d(self, level)
        return texture
    def setCompressedSubImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setCompressedSubImage2d(self, level)
        return texture

class TextureImage3D(TextureImageBasic):
    box = Box.property([0, 0, 0], [0, 0, 0], dtype='i', publish='box')

    def setImageOn(self, texture, level=0, **kw):
        texture.setImage3d(self, level, **kw)
        return texture
    def setSubImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setSubImage3d(self, level)
        return texture
    def setCompressedImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setCompressedImage3d(self, level)
        return texture
    def setCompressedSubImageOn(self, texture, level=0, **kw):
        if kw: self.set(kw)
        texture.setCompressedSubImage3d(self, level)
        return texture

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Texture object itself
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Texture(object):
    texParams = []
    texPostParams = []

    targetMap = {
        '1d': gl.GL_TEXTURE_1D, 'proxy-1d': gl.GL_PROXY_TEXTURE_1D, 
        '2d': gl.GL_TEXTURE_2D, 'proxy-2d': gl.GL_PROXY_TEXTURE_2D, 
        '3d': gl.GL_TEXTURE_3D, 'proxy-3d': gl.GL_PROXY_TEXTURE_3D,

        'rect': glext.GL_TEXTURE_RECTANGLE_ARB, 'proxy-rect': glext.GL_PROXY_TEXTURE_RECTANGLE_ARB,

        'cube': gl.GL_TEXTURE_CUBE_MAP, 'proxy-cube': gl.GL_PROXY_TEXTURE_CUBE_MAP,
        'cube+x': gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X, 'cube-x': gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
        'cube+y': gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Y, 'cube-y': gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
        'cube+z': gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Z, 'cube-z': gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
    }

    formatMap = {
        1: 1, 2: 2, 3: 3, 4: 4, '1': 1, '2': 2, '3': 3, '4': 4,

        'rgb': gl.GL_RGB, 'RGB': gl.GL_RGB,
        'r3b3g2': gl.GL_R3_G3_B2, 'R3B3G2': gl.GL_R3_G3_B2,
        'rbg4': gl.GL_RGB4, 'RBG4': gl.GL_RGB4,
        'rbg5': gl.GL_RGB4, 'RBG5': gl.GL_RGB4,
        'rbg8': gl.GL_RGB8, 'RBG8': gl.GL_RGB8,
        'rbg12': gl.GL_RGB12, 'RBG12': gl.GL_RGB12,
        'rbg16': gl.GL_RGB16, 'RBG16': gl.GL_RGB16,

        'rgba': gl.GL_RGBA, 'RGBA': gl.GL_RGBA,
        'rbga2': gl.GL_RGBA2, 'RBGA2': gl.GL_RGBA2,
        'rbga4': gl.GL_RGBA4, 'RBGA4': gl.GL_RGBA4,
        'rbga8': gl.GL_RGBA8, 'RBGA8': gl.GL_RGBA8,
        'rbga12': gl.GL_RGBA12, 'RBGA12': gl.GL_RGBA12,
        'rbga16': gl.GL_RGBA16, 'RBGA16': gl.GL_RGBA16,

        'rbg5a1': gl.GL_RGB5_A1, 'RBG5A1': gl.GL_RGB5_A1,
        'rbg10a2': gl.GL_RGB10_A2, 'RBG10A2': gl.GL_RGB10_A2,

        'a': gl.GL_ALPHA, 'A': gl.GL_ALPHA,'alpha': gl.GL_ALPHA,
        'a4': gl.GL_ALPHA4, 'A4': gl.GL_ALPHA4,
        'a8': gl.GL_ALPHA8, 'A8': gl.GL_ALPHA8,
        'a12': gl.GL_ALPHA12, 'A12': gl.GL_ALPHA12,
        'a16': gl.GL_ALPHA16, 'A16': gl.GL_ALPHA16,

        'l': gl.GL_LUMINANCE, 'L': gl.GL_LUMINANCE, 'luminance': gl.GL_LUMINANCE,
        'l4': gl.GL_LUMINANCE4, 'L4': gl.GL_LUMINANCE4, 
        'l8': gl.GL_LUMINANCE8, 'L8': gl.GL_LUMINANCE8, 
        'l12': gl.GL_LUMINANCE12, 'L12': gl.GL_LUMINANCE12, 
        'l16': gl.GL_LUMINANCE16, 'L16': gl.GL_LUMINANCE16, 

        'la': gl.GL_LUMINANCE_ALPHA, 'LA': gl.GL_LUMINANCE_ALPHA, 'luminance_alpha': gl.GL_LUMINANCE_ALPHA,
        'l6a2': gl.GL_LUMINANCE6_ALPHA2, 'L6A2': gl.GL_LUMINANCE6_ALPHA2, 
        'l12a4': gl.GL_LUMINANCE12_ALPHA4, 'L12A4': gl.GL_LUMINANCE12_ALPHA4, 
        'la4': gl.GL_LUMINANCE4_ALPHA4, 'LA4': gl.GL_LUMINANCE4_ALPHA4, 'l4a4': gl.GL_LUMINANCE4_ALPHA4, 'L4A4': gl.GL_LUMINANCE4_ALPHA4, 
        'la8': gl.GL_LUMINANCE8_ALPHA8, 'LA8': gl.GL_LUMINANCE8_ALPHA8, 'l8a8': gl.GL_LUMINANCE8_ALPHA8, 'L8A8': gl.GL_LUMINANCE8_ALPHA8, 
        'la12': gl.GL_LUMINANCE12_ALPHA12, 'LA12': gl.GL_LUMINANCE12_ALPHA12, 'l12a12': gl.GL_LUMINANCE12_ALPHA12, 'L12A12': gl.GL_LUMINANCE12_ALPHA12, 
        'la16': gl.GL_LUMINANCE16_ALPHA16, 'LA16': gl.GL_LUMINANCE16_ALPHA16, 'l16a16': gl.GL_LUMINANCE16_ALPHA16, 'L16A16': gl.GL_LUMINANCE16_ALPHA16, 

        'i': gl.GL_INTENSITY, 'I': gl.GL_INTENSITY, 'intensity': gl.GL_INTENSITY,
        'i4': gl.GL_INTENSITY4, 'I4': gl.GL_INTENSITY4, 'intensity4': gl.GL_INTENSITY4,
        'i8': gl.GL_INTENSITY8, 'I8': gl.GL_INTENSITY8, 'intensity8': gl.GL_INTENSITY8,
        'i12': gl.GL_INTENSITY12, 'I12': gl.GL_INTENSITY12, 'intensity12': gl.GL_INTENSITY12,
        'i16': gl.GL_INTENSITY16, 'I16': gl.GL_INTENSITY16, 'intensity16': gl.GL_INTENSITY16,

        'c-rgb': gl.GL_COMPRESSED_RGB, 'C-RGB': gl.GL_COMPRESSED_RGB, 'compressed_rgb': gl.GL_COMPRESSED_RGB,
        'c-rgba': gl.GL_COMPRESSED_RGBA, 'C-RGBA': gl.GL_COMPRESSED_RGBA, 'compressed_rgba': gl.GL_COMPRESSED_RGBA,
        'c-a': gl.GL_COMPRESSED_ALPHA, 'C-A': gl.GL_COMPRESSED_ALPHA, 'compressed_alpha': gl.GL_COMPRESSED_ALPHA,
        'c-l': gl.GL_COMPRESSED_LUMINANCE, 'C-L': gl.GL_COMPRESSED_LUMINANCE, 'compressed_luminance': gl.GL_COMPRESSED_LUMINANCE,
        'c-la': gl.GL_COMPRESSED_LUMINANCE_ALPHA, 'C-LA': gl.GL_COMPRESSED_LUMINANCE_ALPHA, 'compressed_luminance_alpha': gl.GL_COMPRESSED_LUMINANCE_ALPHA,
        'c-i': gl.GL_COMPRESSED_INTENSITY, 'C-I': gl.GL_COMPRESSED_INTENSITY, 'compressed_intensity': gl.GL_COMPRESSED_INTENSITY, } 

    def set(self, val=None, **kwattr):
        if val:
            if isinstance(val, dict):
                val = val.iteritems()
            else: val = iter(val)
        else: val = kwattr.iteritems()

        for n,v in val:
            try:
                setattr(self, n, v)
            except glErrors.GLError, glerr:
                if glerr.error == 0x500:
                    print >> sys.stdout, '%s: %s for name: %r value: %r' % (glerr.__class__.__name__, glerr, n, v)

    def release(self):
        if self.texture_id is None:
            return

        self._delTextureInfo()

    texture_id = None
    def _getTextureInfo(self):
        target = self.target
        texture_id = self.texture_id
        if texture_id is None:
            if not target:
                target = self.setTarget()

            texture_id = gl.GLenum(0)
            gl.glGenTextures(1, byref(texture_id))

            def delGLTexture(wr, texture_id=texture_id.value):
                texture_id = gl.GLenum(texture_id)
                gl.glDeleteTextures(1, byref(texture_id))
            texture_id.wr = weakref.ref(texture_id, delGLTexture)

            self.texture_id = texture_id
            self.set(self.texParams)
            self.set(self.texPostParams)

        return target, texture_id

    def _delTextureInfo(self):
        self.texture_id = None

    def bind(self):
        target, texture_id = self._getTextureInfo()
        gl.glBindTexture(target, texture_id)
    def unbind(self):
        target = self.target
        if target:
            gl.glBindTexture(target, 0)

    def enable(self):
        gl.glEnable(self.target)
    def disable(self):
        gl.glDisable(self.target)

    def select(self):
        self.bind()
        self.enable()
        return self

    def deselect(self):
        self.disable()
        self.unbind()
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _target = 0 # gl.GL_TEXTURE_1D, gl.GL_TEXTURE_2D, etc.
    def getTarget(self):
        return self._target
    def setTarget(self, targets=None):
        if targets is None:
            targets = [v for n, v in self.texParams if n == 'target']
        elif isinstance(targets, (long, int, str)):
            targets = [targets]

        target = self.validTargets(targets).next()
        self._target = target
        self.bind()
        return target
    target = property(getTarget, setTarget)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _format = None # gl.GL_RGBA, gl.GL_INTENSITY, etc.
    def getFormat(self):
        return self._format
    def setFormat(self, format):
        if isinstance(format, basestring):
            format = self.formatMap[format]
        self._format = format
    format = property(getFormat, setFormat)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    genMipmaps = glTexParamProperty_i(gl.GL_GENERATE_MIPMAP, False)

    wrapS = glTexParamProperty_i(gl.GL_TEXTURE_WRAP_S)
    wrapT = glTexParamProperty_i(gl.GL_TEXTURE_WRAP_T)
    wrapR = glTexParamProperty_i(gl.GL_TEXTURE_WRAP_R)
    _wrapGroup = (wrapS, wrapT, wrapR)

    def setWrap(self, wrap):
        if not isinstance(wrap, tuple):
            wrap = wrap, wrap, wrap
        for slot, value in zip(self._wrapGroup, wrap[:self.ndim]):
            slot.set(self, value)
    wrap = property(fset=setWrap)

    magFilter = glTexParamProperty_i(gl.GL_TEXTURE_MAG_FILTER, False)
    minFilter = glTexParamProperty_i(gl.GL_TEXTURE_MIN_FILTER, False)
    
    def setFilter(self, filter):
        if isinstance(filter, tuple):
            self.magFilter = filter[0]
            self.minFilter = filter[1]
        else:
            self.magFilter = filter
            self.minFilter = filter
    filter = property(fset=setFilter)

    baseLevel = glTexParamProperty_i(gl.GL_TEXTURE_BASE_LEVEL)
    maxLevel = glTexParamProperty_i(gl.GL_TEXTURE_MAX_LEVEL)

    depthMode = glTexParamProperty_i(gl.GL_DEPTH_TEXTURE_MODE)

    compareMode = glTexParamProperty_i(gl.GL_TEXTURE_COMPARE_MODE)
    compareFunc = glTexParamProperty_i(gl.GL_TEXTURE_COMPARE_FUNC)

    borderColor = glTexParamProperty_4f(gl.GL_TEXTURE_BORDER_COLOR)

    priority = glTexParamProperty_f(gl.GL_TEXTURE_PRIORITY)

    minLOD = glTexParamProperty_f(gl.GL_TEXTURE_MIN_LOD)
    maxLOD = glTexParamProperty_f(gl.GL_TEXTURE_MIN_LOD)
    biasLOD = glTexParamProperty_f(gl.GL_TEXTURE_LOD_BIAS)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Size & Dimensios
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    box = None
    texSize = zeros(1, 'L')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Texture Data
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    TextureImage1DFactory = TextureImage1D
    @classmethod
    def data1d(klass, *args, **kw):
        return klass.TextureImage1DFactory(*args, **kw)

    TextureImage2DFactory = TextureImage2D
    @classmethod
    def data2d(klass, *args, **kw):
        return klass.TextureImage2DFactory(*args, **kw)

    TextureImage3DFactory = TextureImage3D
    @classmethod
    def data3d(klass, *args, **kw):
        return klass.TextureImage3DFactory(*args, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def blankImage(self, data, level=0, **kw):
        data.texBlank()
        data.setImageOn(self, level, **kw)
        data.texClear()
        return data

    def blankImage1d(self, *args, **kw):
        return self.blankImage(self.data1d(*args, **kw))
    def blankImage2d(self, *args, **kw):
        return self.blankImage(self.data2d(*args, **kw))
    def blankImage3d(self, *args, **kw):
        return self.blankImage(self.data3d(*args, **kw))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Tex Image Setting
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setImage(self, data, level=0, **kw):
        data.setImageOn(self, level, **kw)
        return data
    def setImage1d(self, data, level=0):
        self.bind(); data.select()
        try:
            texSize = data.size
            gl.glTexImage1D(self.target, level, self.format, 
                    texSize[0], data.border, 
                    data.format, data.dataType, data.ptr)
            self.texSize = texSize.copy()
        finally:
            data.deselect()
        return data
    def setImage2d(self, data, level=0):
        self.bind(); data.select()
        try:
            texSize = data.size
            gl.glTexImage2D(self.target, level, self.format, 
                    texSize[0], texSize[1], data.border, 
                    data.format, data.dataType, data.ptr)

            self.texSize = texSize.copy()
        finally:
            data.deselect()
        return data
    def setImage3d(self, data, level=0):
        self.bind(); data.select()
        try:
            texSize = data.size
            gl.glTexImage3D(self.target, level, self.format, 
                    texSize[0], texSize[1], texSize[2], data.border, 
                    data.format, data.dataType, data.ptr)
            self.texSize = texSize.copy()
        finally:
            data.deselect()
        return data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setSubImage(self, data, level=0, **kw):
        data.setSubImageOn(self, level, **kw)
        return self
    def setSubImage1d(self, data, level=0):
        self.bind(); data.select()
        try:
            texPos = data.pos; texSize = data.size
            gl.glTexSubImage1D(self.target, level,
                    texPos[0], 
                    texSize[0], 
                    data.format, data.dataType, data.ptr)
        finally:
            data.deselect()
        return data
    def setSubImage2d(self, data, level=0):
        self.bind(); data.select()
        try:
            texPos = data.pos; texSize = data.size
            gl.glTexSubImage2D(self.target, level, 
                    texPos[0], texPos[1], 
                    texSize[0], texSize[1], 
                    data.format, data.dataType, data.ptr)
        finally:
            data.deselect()
        return data
    def setSubImage3d(self, data, level=0):
        self.bind(); data.select()
        try:
            texPos = data.pos; texSize = data.size
            gl.glTexSubImage3D(self.target, level,
                    texPos[0], texPos[1], texPos[2], 
                    texSize[0], texSize[1], texSize[2], 
                    data.format, data.dataType, data.ptr)
        finally:
            data.deselect()
        return data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setCompressedImage(self, data, level=0, **kw):
        data.setCompressedImageOn(self, level, **kw)
        return data
    def setCompressedImage1d(self, data, level=0):
        self.bind(); data.select()
        try:
            texSize = data.size
            gl.glCompressedTexImage1D(self.target, level, self.format, 
                    texSize[0], data.border, 
                    data.format, data.dataType, data.ptr)
            self.texSize = texSize.copy()
        finally:
            data.deselect()
        return data
    def setCompressedImage2d(self, data, level=0):
        self.bind(); data.select()
        try:
            texSize = data.size
            gl.glCompressedTexImage2D(self.target, level, self.format, 
                    texSize[0], texSize[1], data.border, 
                    data.format, data.dataType, data.ptr)
            self.texSize = texSize.copy()
        finally:
            data.deselect()
        return data
    def setCompressedImage3d(self, data, level=0):
        self.bind(); data.select()
        try:
            texSize = data.size
            gl.glCompressedTexImage3D(self.target, level, self.format, 
                    texSize[0], texSize[1], texSize[2], data.border, 
                    data.format, data.dataType, data.ptr)
            self.texSize = texSize.copy()
        finally:
            data.deselect()
        return data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setCompressedSubImage(self, data, level=0):
        data.setCompressedSubImageOn(self, level, **kw)
        return data
    def setCompressedSubImage1d(self, data, level=0):
        self.bind(); data.select()
        try:
            texPos = data.pos; texSize = data.size
            gl.glCompressedTexSubImage1D(self.target, level,
                    texPos[0],
                    texSize[0], 
                    data.format, data.dataType, data.ptr)
        finally:
            data.deselect()
        return data
    def setCompressedSubImage2d(self, data, level=0):
        self.bind(); data.select()
        try:
            texPos = data.pos; texSize = data.size
            gl.glCompressedTexSubImage2D(self.target, level,
                    texPos[0], texPos[1], 
                    texSize[0], texSize[1], 
                    data.format, data.dataType, data.ptr)
        finally:
            data.deselect()
        return data
    def setCompressedSubImage3d(self, data, level=0):
        self.bind(); data.select()
        try:
            texPos = data.pos; texSize = data.size
            gl.glCompressedTexSubImage3D(self.target, level, 
                    texPos[0], texPos[1], texPos[2], 
                    texSize[0], texSize[1], texSize[2], 
                    data.format, data.dataType, data.ptr)
        finally:
            data.deselect()
        return data

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _maxTextureSizeByTarget = {}

    _textureTargetToMaxPName = {
        gl.GL_TEXTURE_1D: gl.GL_MAX_TEXTURE_SIZE, gl.GL_PROXY_TEXTURE_1D: gl.GL_MAX_TEXTURE_SIZE,
        gl.GL_TEXTURE_2D: gl.GL_MAX_TEXTURE_SIZE, gl.GL_PROXY_TEXTURE_2D: gl.GL_MAX_TEXTURE_SIZE,
        gl.GL_TEXTURE_3D: gl.GL_MAX_3D_TEXTURE_SIZE, gl.GL_PROXY_TEXTURE_3D: gl.GL_MAX_3D_TEXTURE_SIZE,
        gl.GL_TEXTURE_CUBE_MAP: gl.GL_MAX_CUBE_MAP_TEXTURE_SIZE, gl.GL_PROXY_TEXTURE_CUBE_MAP: gl.GL_MAX_CUBE_MAP_TEXTURE_SIZE,
        glext.GL_TEXTURE_RECTANGLE_ARB: glext.GL_MAX_RECTANGLE_TEXTURE_SIZE_ARB, glext.GL_PROXY_TEXTURE_RECTANGLE_ARB: glext.GL_MAX_RECTANGLE_TEXTURE_SIZE_ARB,
        }

    def getMaxTextureSize(self):
        return self.getMaxTextureSizeFor(self.target)

    @classmethod
    def getMaxTextureSizeFor(klass, target):
        r = klass._maxTextureSizeByTarget.get(target, None)
        if r is None:
            pname = klass._textureTargetToMaxPName[target]
            i = gl.GLint(0)
            gl.glGetIntegerv(pname, byref(i))
            r = i.value
            if r == 0 and target == gl.GL_TEXTURE_2D:
                r = 512
            klass._maxTextureSizeByTarget[target] = r
        return r

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _rstNormalizeTargets = {
        gl.GL_TEXTURE_1D: True,
        gl.GL_TEXTURE_2D: True,
        gl.GL_TEXTURE_3D: True,
        gl.GL_TEXTURE_CUBE_MAP: True,

        glext.GL_TEXTURE_RECTANGLE_ARB: False,
        }

    def texCoordsFor(self, texCoords):
        return self.texCoordsForData(texCoords, self.texSize, self.target)

    def isNormalizedTarget(self):
        return self._rstNormalizeTargets.get(self.target, True)

    @classmethod
    def texCoordsForData(klass, texCoords, texSize, target):
        if klass._rstNormalizeTargets.get(target, True):
            return texCoords/texSize
        else: return texCoords

    def getVertexMesh(self, box=None, key='quads'):
        if box is None: 
            box = self.box
        return box.geoXfrm(key)
    vertexMesh = property(getVertexMesh)

    def getTexCoordMesh(self, box=None, key='quads-flip'):
        if box is None: 
            box = self.box
        return self.texCoordsFor(box.geoXfrm(key))
    texCoordMesh = property(getTexCoordMesh)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Various nits about sizes being powers of 2
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _targetNDims = {
        gl.GL_TEXTURE_1D: 1,
        gl.GL_TEXTURE_2D: 2,
        gl.GL_TEXTURE_3D: 3,
        gl.GL_TEXTURE_CUBE_MAP: 2,

        glext.GL_TEXTURE_RECTANGLE_ARB: 2,
        }

    def getNDim(self):
        return self.targetNDim(self.target)
    ndim = property(getNDim)

    @staticmethod
    def targetNDim(target, targetNDims=_targetNDims):
        return targetNDims[target]
    del _targetNDims

    _targetPowersOfTwo = {
        gl.GL_TEXTURE_1D: True,
        gl.GL_TEXTURE_2D: True,
        gl.GL_TEXTURE_3D: True,
        gl.GL_TEXTURE_CUBE_MAP: True,

        glext.GL_TEXTURE_RECTANGLE_ARB: False,
        }

    _powersOfTwo = [0] + [1<<s for s in xrange(31)]
    @staticmethod
    def idxNextPowerOf2(v, powersOfTwo=_powersOfTwo):
        return bisect_left(powersOfTwo, v)
    @staticmethod
    def nextPowerOf2(v, powersOfTwo=_powersOfTwo):
        return powersOfTwo[bisect_left(powersOfTwo, v)]
    del _powersOfTwo

    def asValidSize(self, size):
        return self.asValidSizeForTarget(size, self.target)
    @classmethod
    def asValidSizeForTarget(klass, size, target):
        if klass._targetPowersOfTwo.get(target, False):
            size = [klass.nextPowerOf2(s) for s in size]
        return asarray(size)

    @classmethod
    def validTargets(klass, targetList=None):
        supported = klass._targetMap_supported
        if supported is None:
            supported = {}
            klass._targetMap_supported = supported

            for alias, target in klass.targetMap.items():
                gl.glIsEnabled(gl.GL_TEXTURE_1D)
                try: 
                    gl.glIsEnabled(target)
                except glErrors.GLError, e: 
                    continue

                supported[alias] = target
                supported[target] = target

        if targetList is None:
            return supported

        return (supported[e] 
                    for v in targetList 
                        for e in (v if isinstance(v, (tuple, list)) else [v]) 
                            if e in supported)
    _targetMap_supported = None

