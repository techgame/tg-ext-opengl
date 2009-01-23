noErrorCheck = set([
    'glBegin',
    'glVertex', 'glColor', 'glIndex', 
    'glNormal', 'glEdgeFlag', 
    'glTexCoord', 'glMultiTexCoord', 'glMaterial', 
    'glEvalCoord', 'glEvalPoint', 
    'glArrayElement', 
    'glCallList', 'glCallLists', 

    'glInitNames', 'glPushName', 'glPopName', 'glLoadName',

    'glMatrixMode',
    'glLoadIdentity', 
    'glLoadMatrixf', 'glLoadMatrixd', 
    'glTranslatef', 'glTranslated',
    'glRotatef', 'glRotated',
    'glScalef', 'glScaled',

    'glEnable', 'glDisable',
    'glEnableClientState', 'glDisableClientState',
    ])

mustErrorCheck = set([
    'glIsEnabled',
    'glRenderMode',
    'glDrawArrays', 'glDrawBuffer', 'glDrawElements', 'glDrawRangeElements'

    'glReadPixels', 'glCopyPixels', 'glDrawPixels',
    'glPixelMapfv', 'glPixelMapuiv', 'glPixelMapusv', 
    'glPixelStoref', 'glPixelStorei', 
    'glPixelTransferf', 'glPixelTransferi', 
    'glPixelZoom', 

    'glTexParameteri', 'glTexParameteriv', 'glTexParameterf', 'glTexParameterfv',

    'glGetTexImage', 'glGetCompressedTexImage',
    'glTexImage', 'glTexSubImage', 
    'glCopyTexImage', 'glCopyTexSubImage',
    'glCompressedTexImage', 'glCompressedTexSubImage',

    'glBindTexture', 'glBindBuffer', 'glBindAttribLocation',
    ])

