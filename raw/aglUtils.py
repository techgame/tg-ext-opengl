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

import ctypes, ctypes.util
from ctypes import cast, byref, c_void_p, c_int, POINTER

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ AGL Stuff
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AGL_SWAP_RECT = 200
AGL_BUFFER_RECT = 202
AGL_SWAP_LIMIT = 203
AGL_COLORMAP_TRACKING = 210
AGL_COLORMAP_ENTRY = 212
AGL_RASTERIZATION = 220
AGL_SWAP_INTERVAL = 222
AGL_STATE_VALIDATION = 230
AGL_BUFFER_NAME = 231
AGL_ORDER_CONTEXT_TO_FRONT = 232
AGL_CONTEXT_SURFACE_ID = 233
AGL_CONTEXT_DISPLAY_ID = 234
AGL_SURFACE_ORDER = 235
AGL_SURFACE_OPACITY = 236
AGL_CLIP_REGION = 254
AGL_FS_CAPTURE_SINGLE = 255
AGL_SURFACE_BACKING_SIZE = 304
AGL_ENABLE_SURFACE_BACKING_SIZE = 305
AGL_SURFACE_VOLATILE = 306

AGL_NONE = 0
AGL_ALL_RENDERERS = 1
AGL_BUFFER_SIZE = 2
AGL_LEVEL = 3
AGL_RGBA = 4
AGL_DOUBLEBUFFER = 5
AGL_STEREO = 6
AGL_AUX_BUFFERS = 7
AGL_RED_SIZE = 8
AGL_GREEN_SIZE = 9
AGL_BLUE_SIZE = 10
AGL_ALPHA_SIZE = 11
AGL_DEPTH_SIZE = 12
AGL_STENCIL_SIZE = 13
AGL_ACCUM_RED_SIZE = 14
AGL_ACCUM_GREEN_SIZE = 15
AGL_ACCUM_BLUE_SIZE = 16
AGL_ACCUM_ALPHA_SIZE = 17
AGL_PIXEL_SIZE = 50
AGL_MINIMUM_POLICY = 51
AGL_MAXIMUM_POLICY = 52
AGL_OFFSCREEN = 53
AGL_FULLSCREEN = 54
AGL_SAMPLE_BUFFERS_ARB = 55
AGL_SAMPLES_ARB = 56
AGL_AUX_DEPTH_STENCIL = 57
AGL_COLOR_FLOAT = 58
AGL_MULTISAMPLE = 59
AGL_SUPERSAMPLE = 60
AGL_SAMPLE_ALPHA = 61

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

libAGLPath = ctypes.util.find_library("AGL")
if libAGLPath:
    libAGL = ctypes.cdll.LoadLibrary(libAGLPath)
else: libAGL = None

libOpenGLPath = ctypes.util.find_library("OpenGL")
if libOpenGLPath:
    libOpenGL = ctypes.cdll.LoadLibrary(libOpenGLPath)
else: libOpenGL = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AGLError(Exception):
    pass

def aglCheckError():
    err = libAGL.aglGetError()
    if err:
        errStr = cast(libAGL.aglErrorString(err), ctypes.c_char_p)
        raise AGLError('%s(%d[0x%x])' %(errStr.value, err, err))
    return True
    

def setAGLSwapInterval(interval=1):
    """Sets the AGL_SWAP_INTERVAL for the current context"""
    aglCtx = libAGL.aglGetCurrentContext()
    libAGL.aglSetInteger(aglCtx, AGL_SWAP_INTERVAL, byref(c_int(interval)))
    aglCheckError()
    return True

def getCGLContextAndFormat():
    """Using the current OpenGL context (via aglGetCurrentContext), return a
    compatible CarbonGL context and pixel format suitable for working with
    quicktime"""

    # getting cglContext and cglPixel format to initialize the movie from
    cglCtx = libOpenGL.CGLGetCurrentContext()
    if not cglCtx:
        cglCtx = c_void_p()
        aglCtx = libAGL.aglGetCurrentContext()
        r = libAGL.aglGetCGLContext(aglCtx, byref(cglCtx))

    aglAttribs = [
        AGL_RGBA, 
        #AGL_DOUBLEBUFFER, 
        AGL_MINIMUM_POLICY, 
        #AGL_DEPTH_SIZE, 1,
        AGL_RED_SIZE, 1, 
        AGL_GREEN_SIZE, 1, 
        AGL_BLUE_SIZE, 1, 
        AGL_ALPHA_SIZE, 1, 
        AGL_NONE]

    aglAttribs = (c_int*len(aglAttribs))(*aglAttribs)
    aglPix = libAGL.aglChoosePixelFormat(None, 0, aglAttribs)
    aglCheckError()

    cglPix = c_void_p()
    libAGL.aglGetCGLPixelFormat(aglPix, byref(cglPix))
    aglCheckError()

    return cglCtx, cglPix

