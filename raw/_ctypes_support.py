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

import os, sys
import new
import ctypes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Const
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

abiLoaderMap = {
    'c': ctypes.cdll,
    'cdecl': ctypes.cdll,

    'posix': ctypes.cdll,
    'nt': getattr(ctypes, 'windll', None),
    'ce': getattr(ctypes, 'windll', None),

    'win': getattr(ctypes, 'windll', None),
    'ole': getattr(ctypes, 'oledll', None),

    'py': ctypes.pydll,
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def loadFirstLibrary(*libraryname, **kw):
    abi = kw.get('abi', os.name)

    abiLoadLibrary = abiLoaderMap[abi].LoadLibrary
    for name in libraryname: 
        path = find_library(name)
        if path:
            library = abiLoadLibrary(path)
            return library

def attachToLibFn(fn, restype, argtypes, errcheck, lib):
    fn.api = getattr(lib, fn.__name__, None)
    if fn.api is not None:
        fn.api.restype = restype
        fn.api.argtypes = argtypes
        if errcheck is not None:
            fn.api.errcheck = errcheck

        doc = getattr(fn, '__doc__', None)
        if doc:
            fn.api.__doc__ = doc
        return replaceFunctionApi(fn, fn.api)
    else:
        return fn

def replaceFunctionApi(fn, api):
    assert fn.func_defaults == (None,), (fn, fn.func_defaults)
    assert fn.func_code.co_varnames[-1] == '_api_', (fn, fn.func_code.co_varnames)
    result = new.function(fn.func_code, fn.func_globals, fn.func_name, (api,), fn.func_closure)
    result.func_dict = fn.func_dict
    return result

def scrubNamespace(namespace, hostNamespace):
    names = set(namespace.iterkeys()) & set(hostNamespace.iterkeys())
    for n in names:
        if namespace[n] is hostNamespace[n]:
            del namespace[n]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Customized find library for applications
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if os.name == "nt":
    def find_library(name, executable_path=os.path.dirname(sys.executable)):
        # See MSDN for the REAL search order.
        paths = [os.path.join(executable_path, 'bin'), executable_path] 
        paths += os.environ['PATH'].split(os.pathsep)

        for directory in paths:
            fname = os.path.join(directory, name)
            if os.path.exists(fname):
                return fname
            if fname.lower().endswith(".dll"):
                continue
            fname = fname + ".dll"
            if os.path.exists(fname):
                return fname
        return None

if os.name == "posix" and sys.platform == "darwin":
    from ctypes.macholib.dyld import dyld_find as _dyld_find
    pathSearches = [
        '%(path)slib%(name)s.dylib',
        '%(path)s%(name)s.dylib',
        '%(path)s%(name)s.framework/%(name)s']

    def find_library(name, executable_path=os.path.dirname(sys.executable)):
        paths = ['', '@executable_path/../Frameworks/', executable_path]
        

        libNameData = {'path': '', 'name': name}
        for directory in paths:
            libNameData['path'] = directory
            for pthFmt in pathSearches:
                libName = pthFmt % libNameData
                try:
                    return _dyld_find(libName, executable_path)
                except ValueError:
                    continue
        return None

