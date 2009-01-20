#!/usr/bin/env python
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

import os
from TG.gccxml.codeAnalyzer import CodeAnalyzer
from TG.gccxml.xforms.ctypes import AtomFilterVisitor, CCodeGenContext
from TG.gccxml.xforms.ctypes import utils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

analyzer = CodeAnalyzer(
        inc=['./inc'], 
        src=['src/genOpenGL.c'], 
        baseline=['src/baseline.c'])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FilterVisitor(AtomFilterVisitor):
    def onFunction(self, item):
        if item.extern and item.name.startswith('gl'):
            if item.arguments:
                if not max(arg.name for arg in item.arguments):
                    self.patchFunctionArgNames(item)

            self.select(item)

    def patchFunctionArgNames(self, funcItem):
        # we are missing the argument names for the functions in glext.
        # For some reason, the authors of glext.h decided to only put
        # the argument names on the typedefs.  Unfortunately, C can't
        # keep the argument names for each function typdef because they
        # only keep unique typedefs -- meaning that the names have to
        # be thrown away.  So in TG.gccxml, we parse the
        # post-preprocessed sources to grab the function pointer
        # typdefs in order to grab the argument names out of them.
        # Using these patches, we can now use the glext's convention
        # for naming function pointers to patch the argument names back
        # into the functions.

        fnName = funcItem.name

        for fnName in (fnName, fnName+'ARB', fnName+'EXT'):
            modName = 'PFN%sPROC' % (fnName.upper(),)
            if self._applyFunctionNamePatch(funcItem, modName):
                return True
            
            modName = '%sProcPtr' % (fnName,)
            if self._applyFunctionNamePatch(funcItem, modName):
                return True

        return False

    def _applyFunctionNamePatch(self, funcItem, patchName):
        patches = self.ftPatches.get(patchName, [])
        for patch in patches:
            for arg, name in zip(funcItem.arguments, patch.argNames):
                if not arg.name:
                    arg.name = name
            return True
        else:
            return False

    def onPPInclude(self, item):
        print '"%s" includes "%s"' % (item.file.name, item.filename)

    def onPPDefine(self, item):
        if item.ident in self.filterConditionals:
            return

        if item.ident.startswith('GL'):
            # Grab all GL defines
            self.select(item)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    filterConditionals = set([
        'GL_GLEXT_PROTOTYPES',
        'GLAPI',
        'GL_TYPEDEFS_2_0',
        'GL_GLEXT_LEGACY',
        'GL_GLEXT_FUNCTION_POINTERS',
        ])
    def onPPConditional(self, item):
        if not item.isOpening():
            return 
        if item.body in self.filterConditionals:
            return
        if item.body.startswith('GL_VERSION'):
            return

        if item.body.startswith('GL'):
            # Grab all opening GL blocks to capture OpenGL Extension defines.
            # Closing and continuation blocks will be linked with the opening blocks.
            self.select(item.inOrder())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    root = analyzer.loadModel()

    ftPatches = {}
    for fa in root.files.itervalues():
        patchMap = fa.getPatchFor('FunctionType')
        for key, lst in patchMap.iteritems():
            ftPatches.setdefault(key, []).extend(lst)

    context = CCodeGenContext(root)
    context.atomFilter = FilterVisitor()
    context.atomFilter.ftPatches = ftPatches

    ciFilesByName = dict((os.path.basename(f.name), f) for f in context if f)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # setup imports

    for ciFile in ciFilesByName.itervalues():
        ciFile.importAll('_ctypes_opengl')

    gl = ciFilesByName['gl.h']

    glext = ciFilesByName['glext.h']
    glext.importAll(gl)

    glu = ciFilesByName['glu.h']
    glu.importAll(gl)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # write output files

    context.outputPath = '../../proj/openGL/raw/'
    print
    print "Writing out ctypes code:"
    print "========================"
    for ciFile in ciFilesByName.values():
        print 'Writing:', ciFile.filename
        ciFile.writeToFile()
        print 'Done Writing:', ciFile.filename
        print
    print

    utils.includeSupportIn(context.getOutputFilename('_ctypes_support.py'), copySource=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    main()

