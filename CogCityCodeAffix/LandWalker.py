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

if __debug__:
    loadPrcFile("config/config.prc")

class landWalker(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        base.disableMouse()

        font = self.loader.loadFont("phase_3/models/fonts/vtRemingtonPortable.ttf")

        self.land = self.loader.loadModel("phase_11/models/lawbotHQ/LawbotPlaza.bam")
        self.land.reparentTo(self.render)

        self.Sourcebot = Actor('phase_3.5/models/char/suitC-mod.bam',
                               {'neutral': 'phase_3.5/models/char/suitC-neutral.bam',
                                'victory': 'phase_4/models/char/suitC-victory.bam',
                                'walk': 'phase_3.5/models/char/suitC-walk.bam'})

        self.Sourcebot.reparentTo(render)
        self.Sourcebot.loop('neutral')
        self.TorsoTex = loader.loadTexture('phase_3.5/maps/t_blazer.jpg')
        self.Sourcebot.find('**/torso').setTexture(self.TorsoTex, 1)
        self.ArmTex = loader.loadTexture('phase_3.5/maps/t_sleeve.jpg')
        self.Sourcebot.find('**/arms').setTexture(self.ArmTex, 1)
        self.LegTex = loader.loadTexture('phase_3.5/maps/t_leg.jpg')
        self.Sourcebot.find('**/legs').setTexture(self.LegTex, 1)
        self.Head = loader.loadModel('phase_3.5/models/char/suitC-heads.bam').find('**/tightwad')
        self.headTexture = loader.loadTexture("phase_3.5/maps/payroll-converter.jpg")
        self.Head.reparentTo(self.Sourcebot.find('**/joint_head'))
        self.Sourcebot.findAllMatches('**/joint_head').setTexture(self.headTexture, 1)
        self.icon = loader.loadModel('phase_3/models/gui/SourcebotIcon.bam')
        self.icon.reparentTo(render)
        self.iconTexture = loader.loadTexture('phase_3/maps/SourcebotIcon.png')
        self.icon.setTexture(self.iconTexture, 1)
        self.icon.setHpr(180, 0, 0)
        self.icon.setPos(0.1, 0, -0.30)
        self.icon.setScale(1.00)
        self.icon.reparentTo(self.Sourcebot.find('**/joint_attachMeter'))
        Name = TextNode("nametag")
        Name.setText("Prof. Bill\nPayroll Converter\nSourcebot\nLevel 1")
        Name.setFont(font)
        self.nameTag = render.attachNewNode(Name)
        self.nameTag.setBillboardAxis()
        self.nameTag.reparentTo(self.Sourcebot.find('**/joint_nameTag'))
        self.nameTag.setZ(7.51)
        Name.setAlign(TextNode.ACenter)
        Name.setCardColor(0.8, 0.8, 0.8, 0.5)
        Name.setCardAsMargin(0.1, 0, 0, -0.2)
        Name.setCardDecal(True)
        Name.setTextColor(0, 0, 0, 1.0)
        self.nameTag.setScale(0.33)


#____________________________LANDWALKER___________________#

        self.collisions()

    def collisions(self):
        self.keyMap = {"left": 0, "right": 0, "forward": 0, "backward": 0, "up": 0, "side-left": 0, "side-right": 0}
        self.isMoving_forward = False
        self.isMoving_side = False
        base.cTrav = CollisionTraverser()

        self.colEV = CollisionHandlerEvent()
        self.groundHandler = CollisionHandlerFloor()
        self.wallHandler = CollisionHandlerPusher()

        self.FLOOR_MASK = BitMask32.bit(1)

        self.WALL_MASK = BitMask32.bit(2)

        self.TRIGGER_MASK = BitMask32.bit(3)

        self.HITBOX_MASK = BitMask32.bit(4)

        self.Sourcebot.setCollideMask(BitMask32.allOff())
        self.LEGSNP = NodePath('toonlegsnp')
        self.LEGSNP.reparentTo(self.Sourcebot)
        self.LEGSNP.setZ(5)
        self.avatarCollider = self.Sourcebot.attachNewNode(CollisionNode('LEGSCNODE'))
        self.avatarCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self.avatarCollider.node().setFromCollideMask(self.WALL_MASK)
        self.avatarCollider.node().setIntoCollideMask(BitMask32.allOff())
        self.avatarCollider.setSz(5)
        self.avatarCollider2 = self.Sourcebot.attachNewNode(CollisionNode('LEGSCHIT'))
        self.avatarCollider2.node().addSolid(CollisionSphere(0, 0, 0, 1))
        self.avatarCollider2.node().setFromCollideMask(BitMask32.allOff())
        self.avatarCollider2.node().setIntoCollideMask(self.HITBOX_MASK)
        self.avatarCollider2.setSz(6)
        self.avatarSensor = self.Sourcebot.attachNewNode(CollisionNode('avatarSensor'))
        self.avatarSensor.node().addSolid(CollisionSphere(0, 0, 0, 1.2))
        self.avatarSensor.node().setFromCollideMask(self.WALL_MASK | self.TRIGGER_MASK)
        self.avatarSensor.node().setIntoCollideMask(BitMask32.allOff())
        self.raygeometry = CollisionRay(0, 0, 2, 0, 0, -1)
        self.avatarRay = self.LEGSNP.attachNewNode(CollisionNode('avatarRay'))
        self.avatarRay.node().addSolid(self.raygeometry)
        self.avatarRay.node().setFromCollideMask(self.FLOOR_MASK)
        self.avatarRay.node().setIntoCollideMask(BitMask32.allOff())

        self.groundHandler.addCollider(self.avatarRay, self.Sourcebot)

        self.wallHandler.addCollider(self.avatarCollider, self.Sourcebot)

        self.wallHandler.addCollider(self.avatarCollider2, self.Sourcebot)

        base.cTrav.addCollider(self.avatarRay, self.groundHandler)
        base.cTrav.addCollider(self.avatarCollider, self.wallHandler)
        base.cTrav.addCollider(self.avatarCollider2, self.wallHandler)
        base.cTrav.addCollider(self.avatarSensor, self.colEV)
        #---------------------------------------------------------------#

        #-----------------WALK-CODE-----------------#

        base.accept("arrow_left", self.setKey, ["left", 1])
        base.accept("arrow_right", self.setKey, ["right", 1])
        base.accept("arrow_up", self.setKey, ["forward", 1])
        base.accept("arrow_down", self.setKey, ["backward", 1])
        base.accept("arrow_left-up", self.setKey, ["left", 0])
        base.accept("arrow_right-up", self.setKey, ["right", 0])
        base.accept("arrow_up-up", self.setKey, ["forward", 0])
        base.accept("arrow_down-up", self.setKey, ["backward", 0])
        base.accept("arrow_down-arrow_up", self.setKey, ["backward", 1])
        base.accept("arrow_up-arrow_down", self.setKey, ["forward", 1])

        #-------------wasd--------------------#

        base.accept("a", self.setKey, ["side-left", 1])
        base.accept("d", self.setKey, ["side-right", 1])
        base.accept("w", self.setKey, ["forward", 1])
        base.accept("s", self.setKey, ["backward", 1])
        base.accept("a-up", self.setKey, ["side-left", 0])
        base.accept("d-up", self.setKey, ["side-right", 0])
        base.accept("w-up", self.setKey, ["forward", 0])
        base.accept("s-up", self.setKey, ["backward", 0])
        base.accept("s-w", self.setKey, ["backward", 1])
        base.accept("w-s", self.setKey, ["forward", 1])

        taskMgr.add(self.move, "movetask")

        self.cameraJoint()
        self.camera.setPos(0, -16.5, 3.89)

        self.accept("alt-o", self.oobe)

    def setKey(self, key, value):
        self.keyMap[key] = value

    def move(self, task):
        try:
            if (self.keyMap["left"] != 0):
                self.Sourcebot.setH(self.Sourcebot.getH() + 75 * globalClock.getDt())
            if (self.keyMap["right"] != 0):
                self.Sourcebot.setH(self.Sourcebot.getH() - 75 * globalClock.getDt())
            if (self.keyMap["side-right"] != 0):
                self.Sourcebot.setX(self.Sourcebot, 24 * globalClock.getDt())
            if (self.keyMap["side-left"] != 0):
                self.Sourcebot.setX(self.Sourcebot, -24 * globalClock.getDt())
            if (self.keyMap["forward"] != 0):
                self.Sourcebot.setY(self.Sourcebot, 24 * globalClock.getDt())
            if (self.keyMap["backward"] != 0):
                self.Sourcebot.setY(self.Sourcebot, -12.5 * globalClock.getDt())
        except:
            pass

        if (self.keyMap["forward"] != 0):
            if self.isMoving_forward is False:
                self.isMoving_side = False
                self.AVATAR_MOTION = 'MOVING'
                self.Sourcebot.stop("neutral")
                self.Sourcebot.play("walk")
                self.Sourcebot.setPlayRate(1, 'walk')
                self.Sourcebot.loop("walk")
                self.isMoving_forward = True
        elif (self.keyMap["left"] != 0) or (self.keyMap["right"] != 0) or (self.keyMap["backward"] != 0):
            if self.isMoving_side is False:
                self.isMoving_forward = False
                self.AVATAR_MOTION = 'MOVING'
                self.Sourcebot.play("walk")
                self.Sourcebot.setPlayRate(-1.0, 'walk')
                self.Sourcebot.stop("neutral")
                self.Sourcebot.loop("walk")
                self.isMoving_side = True
        else:
            if self.isMoving_forward or self.isMoving_side:
                self.AVATAR_MOTION = 'NORMAL'
                self.Sourcebot.stop("walk")
                self.Sourcebot.loop("neutral")
                self.Sourcebot.loop("neutral")
                self.Sourcebot.loop("neutral")
                self.isMoving_side = False
                self.isMoving_forward = False
        return task.cont


    def cameraJoint(self):
        self.camera.reparentTo(self.Sourcebot.find('**/joint_nameTag'))




def LandWalker(data):
    print(data)

game = landWalker()
game.run()