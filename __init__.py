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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def printGLInfo(out=None, incExtensions=False):
    from .raw import gl

    print >>out, 'GL Version: ', gl.glGetString(gl.GL_VERSION)
    print >>out, '    Vendor: ', gl.glGetString(gl.GL_VENDOR)
    print >>out, '  Renderer: ', gl.glGetString(gl.GL_RENDERER)
    if incExtensions:
        ext = gl.glGetString(gl.GL_EXTENSIONS).split()
        print >>out, 'GL Extensions:', len(ext),
        for i, e in enumerate(ext):
            if i % 2 == 0:
                print >> out
                print >> out, "   ",
            print >>out, "%-40s" % (e,),
        print

