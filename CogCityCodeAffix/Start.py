import makeAcog
import printcode
from direct.showbase.ShowBase import ShowBase
import sys
from pandac.PandaModules import *


class commands(ShowBase):

    def __init__(self):

        wp = WindowProperties()

        self.accept("escape-up", sys.exit)
        self.accept("f11", self.fullscreen)


    def fullscreen(self):
           max_resolution = max(((mode.width, mode.height) for mode in
           base.pipe.getDisplayInformation().getDisplayModes()))
           wp = WindowProperties.getDefault()
           wp.setSize(max_resolution)
           base.win.requestProperties(wp)
           self.accept("f11", self.exitFullscreen)

    def exitFullscreen(self):
           wp = WindowProperties.getDefault()
           wp.setSize(1280, 720)
           base.win.requestProperties(wp)
           self.accept("f11", self.fullscreen)

start = commands()
base.run()