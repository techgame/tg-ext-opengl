#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <style>
        frame {frame-main:1; locking:1; size:'800,600'}
        frame>layout {layout-cfg:'1,EXPAND'}
        frame>layout>panel {layout-cfg:'1,EXPAND'}
    </style>

    <frame title='GLCanvas in a Skin' show='1'>
        <menubar>
            <menu text='View'>
                <item text='Full Screen\tCtrl-F' help='Shows My Frame on the entire screen'>
                    display = None
                    def getDisplay():
                        global display
                        if display is None:
                            display = wx.Display(wx.Display.GetFromPoint(ctx.frame.GetPosition()))
                        return display
                    def delDisplay():
                        global display
                        display = None

                    oldMode = None
                    def changeMode(*args):
                        global oldMode
                        if oldMode is None:
                            oldMode = getDisplay().GetCurrentMode()
                        return getDisplay().ChangeMode(wx.VideoMode(*args))

                    def restoreMode():
                        global oldMode
                        if oldMode is not None:
                            getDisplay().ChangeMode(oldMode)
                            oldMode = None
                        delDisplay()

                    <event>

                        if ctx.frame.IsFullScreen():
                            print 'reset mode:', restoreMode()
                            ctx.frame.ShowFullScreen(False)
                        else:
                            print 'change mode:', changeMode(1280,854,32)
                            ctx.frame.ShowFullScreen(True)
                    </event>
                    <event type='EVT_UPDATE_UI'>
                        if ctx.frame.IsFullScreen():
                            obj.SetText('Restore from Full Screen\tCtrl-F')
                        else:
                            obj.SetText('Full Screen\tCtrl-F')
                    </event>
                </item>
            </menu>
        </menubar>
        <layout>
            <panel>
                <layout>
                    <opengl-canvas>
                        import sys
                        import time
                        frame = ctx.frame
                        title = frame.GetTitle()
                        obj.winframeLog = []
                        obj.glframeLog = []
                        obj.lastUpdate = time.clock()

                        def updateFPS(obj, winstart, glstart, glend, winend):
                            winframeLog = obj.winframeLog
                            glframeLog = obj.glframeLog
                            winframeLog.append(winend-winstart)
                            glframeLog.append(glend-glstart)

                            if winend - obj.lastUpdate >= 1:
                                obj.lastUpdate = winend
                                count = len(winframeLog)

                                winfps = count / max(1.0, sum(winframeLog, 0.0))
                                winframeLog[:] = winframeLog[-10:]

                                glfps = count / max(1.0, sum(glframeLog, 0.0))
                                glframeLog[:] = glframeLog[-10:]

                                fpsStr = '%.6s : %.6s FPS (effective : true), %6s frames' % (glfps, winfps, count)
                                frame.SetTitle('%s - %s' % (title, fpsStr))
                                print '\\r', fpsStr.ljust(75),
                                sys.stdout.flush()

                        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                        from TG.openGL.raw import gl, glu

                        obj.SetCurrent()
                        gl.glClearColor(0.0, 0.0, 0.0, 0.0)

                        def wireCube(k):
                            gl.glBegin(gl.GL_LINE_LOOP)
                            gl.glVertex2f(k, k)
                            gl.glVertex2f(-k, k)
                            gl.glVertex2f(-k, -k)
                            gl.glVertex2f(k, -k)
                            gl.glVertex2f(k, k)
                            gl.glEnd()

                        def render():
                            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
                            gl.glPushMatrix()
                            gl.glRotatef((time.clock()*181) % 360.0, 0, 0, 1)
                            gl.glColor3f(1.0, 0.0, 1.0)
                            for i in xrange(1,100):
                                wireCube(i)
                            gl.glPopMatrix()
                            gl.glFlush()

                        def resize((w,h)):
                            if not w or not h: return
                            gl.glViewport(0, 0, w, h)
                            gl.glMatrixMode(gl.GL_PROJECTION)
                            gl.glLoadIdentity()
                            gl.glFrustum(-w/200., w/200., -h/200., h/200., 1., 100.0)
                            gl.glMatrixMode(gl.GL_MODELVIEW)
                            gl.glLoadIdentity()
                            glu.gluLookAt (0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

                        <event type="EVT_ERASE_BACKGROUND"/>
                        <event>
                            winstart = time.clock()

                            dc = wx.PaintDC(obj)
                            obj.SetCurrent()

                            glstart = time.clock()
                            render()
                            glend = time.clock()
                            
                            obj.SwapBuffers()
                            winend = time.clock()

                            # uncomment the following to enter an update loop
                            ## wx.CallAfter(obj.Refresh)

                            updateFPS(obj, winstart, glstart, glend, winend)
                        </event>
                        <event type="EVT_SIZE">
                            obj.Refresh()
                            obj.SetCurrent()
                            resize(obj.GetSize())
                        </event>                        

                        <timer seconds='1/60.'>
                            <event>elem.xmlParent().obj.Refresh()</event>
                        </timer>

                        resize(obj.GetSize())
                    </opengl-canvas>
                </layout>
            </panel>
        </layout>
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    wxSkinModel.fromSkin(xmlSkin).skinModel()


