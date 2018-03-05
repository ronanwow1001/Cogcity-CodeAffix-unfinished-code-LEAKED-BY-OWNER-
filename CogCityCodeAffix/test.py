from direct.actor.Actor import Actor
from pandac.PandaModules import *
from direct.task import Task
import math
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Point3
from pandac.PandaModules import *
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import Vec3, Vec4, BitMask32
from direct.showbase.Transitions import *
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.filter.CommonFilters import *
from panda3d.ai import *
import sys

class Game(DirectObject):
    # constructor

    def __init__(self):
        ShowBase.__init__(self)

        # base.disableMouse()

        self.GameControl()
        self.Stage1()

    def KontrolGame(self):
        self.accept("w", self.Walk)
        self.accept("w-up", self.Stop)
        self.accept("a", self.Turn, [-1])
        self.accept("d", self.Turn, [1])
        self.accept("space", self.Jump)

    def LoadModel(self):
        # load game model
        self.Hero = Actor.Actor("models/Hero.egg", {"Walk": "models/Hero-walk.egg"})
        self.Hero.reparentTo(render)
        self.Hero.setScale(0.1, 0.1, 0.1)
        self.Hero.setPos(-6, 0, 0.4)
        self.Hero.pose("Jalan", 15)
        self.Hero.setHpr(-90, 0, 0)

        self.dummy = render.attachNewNode('dummy')
        self.dummy.setPos(0, 0, 0)

    def Stage1(self):
        # load stage 1
        self.LoadModel()
        self.Terrain1 = loader.loadModel("models/Stage1.egg")
        self.Terrain1.reparentTo(render)
        self.InitCollision()

    def InitCollision(self):
        #
        ray = CollisionRay(0, 0, 5, 0, 0, -1)
        self.HeroC = self.Hero.attachNewNode(CollisionNode('cnode'))
        self.HeroC.node().addSolid(ray)
        self.HeroC.show()
        self.HeroC.node().setIntoCollideMask(BitMask32.allOff())
        self.HeroC.node().setFromCollideMask(BitMask32.bit(2))

        plane1 = CollisionPolygon(Point3(-10, -10, 0.1), Point3(-2, -10, 0.1), Point3(-2, 10, 0.1),
                                  Point3(-10, 10, 0.1))
        plane2 = CollisionPolygon(Point3(-2, -10, 0.1), Point3(1, -10, -0.9), Point3(1, 10, -0.9), Point3(-2, 10, 0.1))
        plane3 = CollisionPolygon(Point3(1, -10, -0.9), Point3(5, -10, -0.9), Point3(5, 10, -0.9), Point3(1, 10, -0.9))

        self.LevelCP = self.dummy.attachNewNode(CollisionNode('cnodeLevel'))
        self.LevelCP.node().addSolid(plane1)
        self.LevelCP.node().addSolid(plane2)
        self.LevelCP.node().addSolid(plane3)

        self.LevelCP.show()
        self.LevelCP.node().setIntoCollideMask(BitMask32.bit(2))

        self.Handlernya = CollisionHandlerQueue()
        # self.HandlerCS = CollisionHandlerEvent()
        # self.HandlerCS.addInPattern('into-g')
        traverser.addCollider(self.HeroC, self.Handlernya)
        # traverser.addCollider(self.HeroCS,self.HandlerCS)
        traverser.traverse(render)

    def DetectCollision(self):
        #
        self.Handlernya.sortEntries()
        entry = self.Handlernya.getEntry(0)
        self.point = entry.getSurfacePoint(render)
        normal = entry.getSurfaceNormal(render)
        # print(entry)
        # print(self.point)

    def Walk(self):
        self.Hero.play("Walk")
        self.Hero.loop("Walk", fromFrame=1, toFrame=60)
        self.Hero.setPlayRate(1.8, 'Walk')
        taskMgr.add(self.Move, "MoveTask")

    def Move(self, task):
        self.DetectCollision()
        Jarak = 0.01
        sudut = self.Hero.getH() * math.pi / 180.0
        dx = Jarak * math.sin(sudut)
        dy = Jarak * -math.cos(sudut)
        self.Hero.setPos(Point3(self.Hero.getX() - dx, self.Hero.getY() - dy, self.point.getZ()))
        return Task.cont

    def Turn(self, arah):
        HeroTurn = self.Hero.hprInterval(.2, Vec3(self.Hero.getH() - (10 * arah), 0, 0))
        HeroTurn.start()

    def Stop(self):
        taskMgr.remove("MoveTask")
        self.Hero.stop()
        self.Hero.pose("Walk", 15)

    def Jump(self):
        self.Hero.play("Walk", fromFrame=61, toFrame=90)
        self.Hero.loop("Walk", fromFrame=61, toFrame=90)
        while self.Hero.getZ() < 2:
            self.Hero.setPos(Point3(self.Hero.getX(), self.Hero.getY(), self.Hero.getZ() + 0.1))


game = Game()
run()