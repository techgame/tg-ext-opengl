#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re

import ctypes
from ctypes import *
import _ctypes_support
from ._ctypes_errCheckMaps import noErrorCheck, mustErrorCheck

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ CTypes Overrides 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def POINTER(baseType):
    # overrides ctypes's POINTER method to just use the direct classes for
    # character strings, and c_void_p for all others, to maximize compatibility
    # with numpy
    if baseType == c_char:
        return c_char_p
    elif baseType == c_wchar:
        return c_wchar_p
    else:
        return c_void_p

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if hasattr(ctypes, 'windll'):
    openGL32 = _ctypes_support.loadFirstLibrary('OpenGL32')
    glu32 = _ctypes_support.loadFirstLibrary('glu32')

    wglGetProcAddress = openGL32.wglGetProcAddress

    def attachToLibFn(fn, restype, argtypes, fnErrCheck):
        fnaddr = wglGetProcAddress(fn.__name__)
        if fnaddr:
            result = WINFUNCTYPE(restype, *argtypes)(fnaddr)
            if fnErrCheck is not None:
                result.errcheck = fnErrCheck
            result.api = result
            result.__name__ = fn.__name__

        elif fn.__name__.startswith('glu'):
            result = _ctypes_support.attachToLibFn(fn, restype, argtypes, fnErrCheck, glu32)
            if result.api is None:
                result = _ctypes_support.attachToLibFn(fn, restype, argtypes, fnErrCheck, openGL32)

        else:
            result = _ctypes_support.attachToLibFn(fn, restype, argtypes, fnErrCheck, openGL32)
            if result.api is None:
                result = _ctypes_support.attachToLibFn(fn, restype, argtypes, fnErrCheck, glu32)
        return result
else:
    openGLLib = _ctypes_support.loadFirstLibrary('OpenGL')
    def attachToLibFn(fn, restype, argtypes, fnErrCheck):
        return _ctypes_support.attachToLibFn(fn, restype, argtypes, fnErrCheck, openGLLib)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

getNameToFirstDigit = re.compile(r'(gl[A-Za-z_]+)\d?').match

def fnBaseName(fn):
    return getNameToFirstDigit(fn.__name__).groups()[0]

def mustErrorCheckFn(fn):
    return name not in mustErrorCheck

glGetError = None

def glNullCheckError(result, func, args):
    err = None
    print '=== %s%r -%r-> %r ' % (func.__name__, args, err, result)
    return result
def glCheckError(result, func, args):
    err = glGetError()
    #print '+++ %s%r -%r-> %r ' % (func.__name__, args, err, result)
    if err != 0:
        from errors import GLError
        raise GLError(err, callInfo=(func, args, result))
    return result

def _bindError(errorFunc, g=globals()):
    g[errorFunc.__name__] = errorFunc

def _getErrorCheckForFn(fn):
    name = fnBaseName(fn)
    if name in noErrorCheck:
        return None
    elif name in mustErrorCheck:
        return glCheckError
    #else:
    #    return glNullCheckError

def cleanupNamespace(namespace):
    _ctypes_support.scrubNamespace(namespace, globals())

def bind(restype, argtypes, errcheck=None):
    def bindFuncTypes(fn):
        fnErrCheck = errcheck
        if fn.__name__ == 'glGetError':
            bindErrorFunc = True
        else:
            bindErrorFunc = False
            if not errcheck:
                fnErrCheck = _getErrorCheckForFn(fn)

        result = attachToLibFn(fn, restype, argtypes, fnErrCheck)

        if bindErrorFunc:
            _bindError(result)

        return result
    return bindFuncTypes

