from pandac.PandaModules import *
from direct.task import Task
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from pandac.PandaModules import *
from direct.task import Task
import math
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from pandac.PandaModules import Point3
from pandac.PandaModules import *
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from direct.interval.LerpInterval import LerpPosInterval


from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
import sys
import time
from threading import Timer
from panda3d.core import GraphicsWindow

if __debug__:
    loadPrcFile("config/config.prc")


class GameTest(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        base.disableMouse()

        self.makeAcog = loader.loadModel("phase_5/models/cogdominium/tt_m_ara_cbr_barrelRoom.bam")
        self.makeAcog.reparentTo(render)
        self.stomper1 = (self.makeAcog.find('**/stomper_GRP_01'))
        self.stomper2 = (self.makeAcog.find('**/stomper_GRP_02'))
        self.stomper3 = (self.makeAcog.find('**/stomper_GRP_03'))
        self.stomper4 = (self.makeAcog.find('**/stomper_GRP_04'))
        self.stomper5 = (self.makeAcog.find('**/stomper_GRP_05'))
        self.stomper6 = (self.makeAcog.find('**/stomper_GRP_06'))
        self.stomper7 = (self.makeAcog.find('**/stomper_GRP_07'))
        self.stomper8 = (self.makeAcog.find('**/stomper_GRP_08'))
        self.stomper9 = (self.makeAcog.find('**/stomper_GRP_09'))
        self.stomper10 = (self.makeAcog.find('**/stomper_GRP_10'))
        self.stomper11 = (self.makeAcog.find('**/stomper_GRP_11'))
        self.stomper12 = (self.makeAcog.find('**/stomper_GRP_12'))
        self.stomper3.setPos(0, 0, 18.00)
        self.stomper5.setPos(0, 0, 10.00)
        self.stomper4.setPos(0, 0, 22.00)
        self.stomper2.setPos(0, 0, 7.00)
        self.stomper7.setPos(0, 0, 0)
        self.stomper8.setPos(0, 0, 5.00)
        self.stomper9.setPos(0, 0, 13.00)
        self.stomper10.setPos(0, 0, 10.00)
        self.stomper11.setPos(0, 0, 22.00)
        self.stomper12.setPos(0, 0, 7.00)
        self.lStomper = loader.loadModel('phase_9/models/cogHQ/square_stomper.bam')
        self.lStomper.setHpr(-90, 0, 180)
        self.lStomper.reparentTo(render)
        self.lStomper.setScale(3)
        self.lStomper.setPos(-12.5, 0, 3)
        self.rStomper = loader.loadModel('phase_9/models/cogHQ/square_stomper.bam')
        self.rStomper.setHpr(90, 0, 0)
        self.rStomper.reparentTo(render)
        self.rStomper.setScale(3)
        self.rStomper.setPos(12.5, 0, 3)
        self.lStomper.find('**/shaft').setScale(1, 3, 1)
        self.rStomper.find('**/shaft').setScale(1, 3, 1)
        self.lStomper.hide()
        self.rStomper.hide()



        self.music = loader.loadMusic("phase_3/audio/bgm/cc_make-a-cog-theme.wav")
        self.music.play()
        self.music.setLoop(True)

        font = self.loader.loadFont("phase_3/models/fonts/vtRemingtonPortable.ttf")

        self.elevator = loader.loadModel("phase_5/models/cogdominium/cogdominiumElevator.bam")
        self.elevator.reparentTo(self.render)
        self.elevator.setY(25.37)
        self.elevator.find('**/floor_light_buttons').removeNode()
        self.rightDoor = (self.elevator.find('**/right_door'))
        self.leftDoor = (self.elevator.find('**/left_door'))
        self.leftDoor.setX(3.50)
        self.rightDoor.setX(-3.50)

        self.skelCog = Actor("phase_5/models/char/cogC_robot-zero.bam",
                             {'neutral': 'phase_3.5/models/char/suitC-neutral.bam',
                              'victory': 'phase_4/models/char/suitC-victory.bam',
                              'walk': 'phase_3.5/models/char/suitC-walk.bam'})
        self.skelCog.reparentTo(self.render)
        self.skelCog.setPos(-16, 0, -4.76)
        self.skelCog.loop('neutral')
        self.skelCog.setH(180)

        self.explosion = self.loader.loadModel("phase_3.5/models/props/explosion.bam")
        self.explosion.reparentTo(self.render)
        self.explosion.setPos(0, -2, 3)
        self.explosion.hide()

        self.flyThru = self.loader.loadModel("phase_5/models/cogdominium/tt_m_gui_csa_flyThru.bam")
        self.flyThru.reparentTo(self.render)
        self.flyThru.setScale(15.42)
        self.flyThru.setPos(-2.90, -8.61, 7.60)
        self.flyThru.find('**/blankScreen_locator').removeNode()
        self.flyThru.find('**/buttonUp_locator').removeNode()
        self.flyThru.find('**/buttonDown_locator').removeNode()
        self.flyThru.find('**/buttonHover_locator').removeNode()
        self.flyThru.hide()

        self.Lawbot = Actor('phase_3.5/models/char/suitC-mod.bam', {'neutral': 'phase_3.5/models/char/suitC-neutral.bam',
                                                                    'victory': 'phase_4/models/char/suitC-victory.bam',
                                                                    'walk': 'phase_3.5/models/char/suitC-walk.bam'})
        self.Lawbot.reparentTo(render)
        self.Lawbot.loop('neutral')
        self.TorsoTex = loader.loadTexture('phase_3.5/maps/l_blazer.jpg')
        self.Lawbot.find('**/torso').setTexture(self.TorsoTex, 1)
        self.ArmTex = loader.loadTexture('phase_3.5/maps/l_sleeve.jpg')
        self.Lawbot.find('**/arms').setTexture(self.ArmTex, 1)
        self.LegTex = loader.loadTexture('phase_3.5/maps/l_leg.jpg')
        self.Lawbot.find('**/legs').setTexture(self.LegTex, 1)
        self.Head = loader.loadModel('phase_3.5/models/char/suitC-heads.bam').find('**/flunky')
        self.headTexture = loader.loadTexture("phase_3.5/maps/bottom-feeder.jpg")
        self.Head.reparentTo(self.Lawbot.find('**/joint_head'))
        self.Lawbot.findAllMatches('**/joint_head').setTexture(self.headTexture, 1)
        self.icon = loader.loadModel('phase_3/models/gui/cog_icons.bam')
        self.icon.reparentTo(render)
        self.icon.reparentTo(self.Lawbot.find('**/joint_attachMeter'))
        self.icon.find('**/MoneyIcon').removeNode()
        self.icon.find('**/cog').removeNode()
        self.icon.find('**/SalesIcon').removeNode()
        self.icon.find('**/CorpIcon').removeNode()
        self.icon.setH(180)
        self.icon.setScale(0.70)
        self.Lawbot.setH(180.00)
        self.Lawbot.setTransparency(TransparencyAttrib.MAlpha)
        self.Lawbot.setColor(0.0, 0.0, 1.0, 0.7)
        self.Lawbot.find('**/hands').setColor(0.0, 0.0, 0.0, 0.0)
        self.Lawbot.hide()
        Name = TextNode("nametag")
        Name.setText("Bottem Feeder\nLawbot\nLevel 1")
        Name.setFont(font)
        self.nameTag = render.attachNewNode(Name)
        self.nameTag.setBillboardAxis()
        self.nameTag.reparentTo(self.Lawbot.find('**/joint_nameTag'))
        self.nameTag.setZ(7.51)
        Name.setAlign(TextNode.ACenter)
        Name.setCardColor(0.8, 0.8, 0.8, 0.5)
        Name.setCardAsMargin(0.1, 0, 0, -0.2)
        Name.setCardDecal(True)
        Name.setTextColor(0, 0, 0, 1.0)
        self.nameTag.setScale(0.33)


        self.Cashbot = Actor('phase_3.5/models/char/suitC-mod.bam', {'neutral': 'phase_3.5/models/char/suitC-neutral.bam',
                                                                    'victory': 'phase_4/models/char/suitC-victory.bam',
                                                                    'walk': 'phase_3.5/models/char/suitC-walk.bam'})
        self.Cashbot.reparentTo(render)
        self.Cashbot.loop('neutral')
        self.TorsoTex = loader.loadTexture('phase_3.5/maps/m_blazer.jpg')
        self.Cashbot.find('**/torso').setTexture(self.TorsoTex, 1)
        self.ArmTex = loader.loadTexture('phase_3.5/maps/m_sleeve.jpg')
        self.Cashbot.find('**/arms').setTexture(self.ArmTex, 1)
        self.LegTex = loader.loadTexture('phase_3.5/maps/m_leg.jpg')
        self.Cashbot.find('**/legs').setTexture(self.LegTex, 1)
        self.Head = loader.loadModel('phase_3.5/models/char/suitC-heads.bam').find('**/coldcaller')
        self.Head.reparentTo(self.Cashbot.find('**/joint_head'))
        self.icon = loader.loadModel('phase_3/models/gui/cog_icons.bam')
        self.icon.reparentTo(render)
        self.icon.reparentTo(self.Cashbot.find('**/joint_attachMeter'))
        self.icon.find('**/SalesIcon').removeNode()
        self.icon.find('**/cog').removeNode()
        self.icon.find('**/LegalIcon').removeNode()
        self.icon.find('**/CorpIcon').removeNode()
        self.icon.setH(180)
        self.icon.setScale(0.70)
        self.Cashbot.setH(180.00)
        self.Cashbot.setTransparency(TransparencyAttrib.MAlpha)
        self.Cashbot.setColor(0.0, 1.0, 0.0, 0.5)
        self.Cashbot.find('**/hands').setColor(0.0, 0.0, 0.0, 0.0)
        self.Cashbot.hide()
        Name = TextNode("nametag")
        Name.setText("Short Change\nCashbot\nLevel 1")
        Name.setFont(font)
        self.nameTag = render.attachNewNode(Name)
        self.nameTag.setBillboardAxis()
        self.nameTag.reparentTo(self.Cashbot.find('**/joint_nameTag'))
        self.nameTag.setZ(7.51)
        Name.setAlign(TextNode.ACenter)
        Name.setCardColor(0.8, 0.8, 0.8, 0.5)
        Name.setCardAsMargin(0.1, 0, 0, -0.2)
        Name.setCardDecal(True)
        Name.setTextColor(0, 0, 0, 1.0)
        self.nameTag.setScale(0.33)
        self.Cashbot.hide()

        self.Sellbot = Actor('phase_3.5/models/char/suitC-mod.bam', {'neutral': 'phase_3.5/models/char/suitC-neutral.bam',
                                                                    'victory': 'phase_4/models/char/suitC-victory.bam',
                                                                    'walk': 'phase_3.5/models/char/suitC-walk.bam'})
        self.Sellbot.reparentTo(render)
        self.Sellbot.loop('neutral')
        self.TorsoTex = loader.loadTexture('phase_3.5/maps/s_blazer.jpg')
        self.Sellbot.find('**/torso').setTexture(self.TorsoTex, 1)
        self.ArmTex = loader.loadTexture('phase_3.5/maps/s_sleeve.jpg')
        self.Sellbot.find('**/arms').setTexture(self.ArmTex, 1)
        self.LegTex = loader.loadTexture('phase_3.5/maps/s_leg.jpg')
        self.Sellbot.find('**/legs').setTexture(self.LegTex, 1)
        self.Head = loader.loadModel('phase_3.5/models/char/suitC-heads.bam').find('**/coldcaller')
        self.Head.reparentTo(self.Sellbot.find('**/joint_head'))
        self.Head.reparentTo(self.Sellbot.find('**/joint_head'))
        self.icon = loader.loadModel('phase_3/models/gui/cog_icons.bam')
        self.icon.reparentTo(render)
        self.icon.reparentTo(self.Sellbot.find('**/joint_attachMeter'))
        self.icon.find('**/MoneyIcon').removeNode()
        self.icon.find('**/cog').removeNode()
        self.icon.find('**/LegalIcon').removeNode()
        self.icon.find('**/CorpIcon').removeNode()
        self.Head.setColor(0, 0, 1, 0.4)
        self.icon.setH(180)
        self.icon.setScale(0.70)
        self.Sellbot.setH(180.00)
        self.Sellbot.setTransparency(TransparencyAttrib.MAlpha)
        self.Sellbot.setColor(0.352, 0.227, 0.419, 0.7)
        self.Sellbot.find('**/hands').setColor(0.0, 0.0, 0.0, 0.0)
        Name = TextNode("nametag")
        Name.setText("Cold Caller\nSellbot\nLevel 1")
        Name.setFont(font)
        self.nameTag = render.attachNewNode(Name)
        self.nameTag.setBillboardAxis()
        self.nameTag.reparentTo(self.Sellbot.find('**/joint_nameTag'))
        self.nameTag.setZ(7.51)
        Name.setAlign(TextNode.ACenter)
        Name.setCardColor(0.8, 0.8, 0.8, 0.5)
        Name.setCardAsMargin(0.1, 0, 0, -0.2)
        Name.setCardDecal(True)
        Name.setTextColor(0, 0, 0, 1.0)
        self.nameTag.setScale(0.33)
        self.Sellbot.hide()
        self.Sellbot.setBlend(frameBlend=True)

        self.Bossbot = Actor('phase_3.5/models/char/suitC-mod.bam',
                             {'neutral': 'phase_3.5/models/char/suitC-neutral.bam',
                              'victory': 'phase_4/models/char/suitC-victory.bam',
                              'walk': 'phase_3.5/models/char/suitC-walk.bam'})
        self.Bossbot.reparentTo(render)
        self.Bossbot.loop('neutral')
        self.TorsoTex = loader.loadTexture('phase_3.5/maps/c_blazer.jpg')
        self.Bossbot.find('**/torso').setTexture(self.TorsoTex, 1)
        self.ArmTex = loader.loadTexture('phase_3.5/maps/c_sleeve.jpg')
        self.Bossbot.find('**/arms').setTexture(self.ArmTex, 1)
        self.LegTex = loader.loadTexture('phase_3.5/maps/c_leg.jpg')
        self.Bossbot.find('**/legs').setTexture(self.LegTex, 1)
        self.Head = loader.loadModel('phase_3.5/models/char/suitC-heads.bam')
        self.Head.find('**/coldcaller').hide()
        self.Head.find('**/gladhander').hide()
        self.Head.find('**/micromanager').hide()
        self.Head.find('**/moneybags').hide()
        self.Head.find('**/tightwad').hide()
        self.Head.reparentTo(self.Bossbot.find('**/joint_head'))
        self.icon = loader.loadModel('phase_3/models/gui/cog_icons.bam')
        self.icon.reparentTo(render)
        self.icon.reparentTo(self.Bossbot.find('**/joint_attachMeter'))
        self.icon.find('**/MoneyIcon').removeNode()
        self.icon.find('**/cog').removeNode()
        self.icon.find('**/LegalIcon').removeNode()
        self.icon.find('**/SalesIcon').removeNode()
        self.icon.setH(180)
        self.icon.setScale(0.70)
        self.Bossbot.setH(180.00)
        self.Bossbot.setTransparency(TransparencyAttrib.MAlpha)
        self.Bossbot.setColor(0.466, 0.0, 1.0, 0.7)
        self.Bossbot.find('**/hands').setColor(0.0, 0.0, 0.0, 0.0)
        Name = TextNode("nametag")
        Name.setText("Flunky\nBossbot\nLevel 1")
        Name.setFont(font)
        self.nameTag = render.attachNewNode(Name)
        self.nameTag.setBillboardAxis()
        self.nameTag.reparentTo(self.Bossbot.find('**/joint_nameTag'))
        self.nameTag.setZ(7.51)
        Name.setAlign(TextNode.ACenter)
        Name.setCardColor(0.8, 0.8, 0.8, 0.5)
        Name.setCardAsMargin(0.1, 0, 0, -0.2)
        Name.setCardDecal(True)
        Name.setTextColor(0, 0, 0, 1.0)
        self.nameTag.setScale(0.33)
        self.Bossbot.hide()


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
        self.Sourcebot.setTransparency(TransparencyAttrib.MAlpha)
        self.Sourcebot.setColor(0.9, 0.6, 0.8, 0.7)
        self.Sourcebot.find('**/hands').setColor(0.0, 0.0, 0.0, 0.0)
        Name = TextNode("nametag")
        Name.setText("Payroll Converter\nSourcebot\nLevel 1")
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
        self.Sourcebot.setH(180)
        self.Sourcebot.hide()


        #------sfx------#

        self.cameraMoveSfx = self.loader.loadSfx("phase_9/audio/sfx/CHQ_FACT_elevator_up_down_loop.ogg")
        self.cameraMoveSfx.setVolume(5.0)

        self.click = self.loader.loadSfx("phase_3/audio/sfx/cc_click.ogg")
        self.hover = self.loader.loadSfx("phase_3/audio/sfx/cc_hover-over-button.ogg")

        self.poof = self.loader.loadSfx("phase_4/audio/sfx/firework_distance_02.ogg")
        self.largeSmash = self.loader.loadSfx("phase_9/audio/sfx/CHQ_FACT_stomper_large.ogg")
        self.largeSmashExec = SoundInterval(self.largeSmash, duration=5.5)

        self.conveyorBeltSfx = self.loader.loadSfx("phase_12/audio/sfx/CHQ_FACT_conveyor_belt.ogg")

        self.cogDialSHORT = self.loader.loadSfx("phase_3.5/audio/dial/COG_VO_grunt.ogg")
        self.cogDialMED = self.loader.loadSfx("phase_3.5/audio/dial/COG_VO_statement.ogg")
        self.cogDialLONG = self.loader.loadSfx("phase_3.5/audio/dial/COG_VO_murmur.ogg")
        self.cogDialQUESTION = self.loader.loadSfx("phase_3.5/audio/dial/COG_VO_question.ogg")

        #-----Sequences------#

        Walk1 = self.stomper1.posInterval(9.50, Point3(0, 0, 18.00))
        Walk2 = self.stomper1.posInterval(9.50, Point3(0, 0, 0))
        self.stomperPound1 = Sequence(Walk1, Walk2)
        self.stomperPound1.loop()

        Walk1 = self.stomper6.posInterval(9.50, Point3(0, 0, 18.00))
        Walk2 = self.stomper6.posInterval(9.50, Point3(0, 0, 0))
        self.stomperPound2 = Sequence(Walk1, Walk2)
        self.stomperPound2.loop()



        Walk1 = self.stomper3.posInterval(9.50, Point3(0, 0, 0))
        Walk2 = self.stomper3.posInterval(9.50, Point3(0, 0, 18.00))
        self.stomperPound3 = Sequence(Walk1, Walk2)
        self.stomperPound3.loop()

        Walk1 = self.stomper5.posInterval(5.50, Point3(0, 0, 0))
        Walk2 = self.stomper5.posInterval(5.50, Point3(0, 0, 10.00))
        self.stomperPound4 = Sequence(Walk1, Walk2)
        self.stomperPound4.loop()

        Walk1 = self.stomper4.posInterval(5.50, Point3(0, 0, 0))
        Walk2 = self.stomper4.posInterval(5.50, Point3(0, 0, 22.00))
        self.stomperPound5 = Sequence(Walk1, Walk2)
        self.stomperPound5.loop()

        Walk1 = self.stomper2.posInterval(3.50, Point3(0, 0, 0))
        Walk2 = self.stomper2.posInterval(3.50, Point3(0, 0, 7.00))
        self.stomperPound6 = Sequence(Walk1, Walk2)
        self.stomperPound6.loop()

        Walk1 = self.stomper7.posInterval(9.50, Point3(0, 0, 18.00))
        Walk2 = self.stomper7.posInterval(9.50, Point3(0, 0, 0))
        self.stomperPound7 = Sequence(Walk1, Walk2)
        self.stomperPound7.loop()

        Walk1 = self.stomper8.posInterval(5.50, Point3(0, 0, 5.00))
        Walk2 = self.stomper8.posInterval(9.50, Point3(0, 0, 0))
        self.stomperPound8 = Sequence(Walk1, Walk2)
        self.stomperPound8.loop()

        Walk1 = self.stomper9.posInterval(6.50, Point3(0, 0, 0))
        Walk2 = self.stomper9.posInterval(6.50, Point3(0, 0, 13.00))
        self.stomperPound9 = Sequence(Walk1, Walk2)
        self.stomperPound9.loop()

        Walk1 = self.stomper10.posInterval(5.50, Point3(0, 0, 0))
        Walk2 = self.stomper10.posInterval(5.50, Point3(0, 0, 10.00))
        self.stomperPound10 = Sequence(Walk1, Walk2)
        self.stomperPound10.loop()

        Walk1 = self.stomper11.posInterval(5.50, Point3(0, 0, 0))
        Walk2 = self.stomper11.posInterval(5.50, Point3(0, 0, 22.00))
        self.stomperPound11 = Sequence(Walk1, Walk2)
        self.stomperPound11.loop()

        Walk1 = self.stomper12.posInterval(3.50, Point3(0, 0, 0))
        Walk2 = self.stomper12.posInterval(3.50, Point3(0, 0, 7.00))
        self.stomperPound12 = Sequence(Walk1, Walk2)
        self.stomperPound12.loop()

        Walk1 = self.camera.posInterval(1.50, Point3(0, -77.48, 3.42))
        Spin1 = self.camera.hprInterval(1.00, Vec3(0, 0, 0))
        Walk2 = self.camera.posInterval(2.50, Point3(0, -77.48, 3.42))
        Walk3 = self.camera.posInterval(3.00, Point3(0, -22.48, 3.42))
        self.cameraStart = Sequence(Walk1, Spin1, Walk2, Walk3)

        Walk1 = self.camera.posInterval(3.00, Point3(0, -22.48, 3.42))
        Spin1 = self.camera.hprInterval(0.00, Vec3(0, 0, 0))
        self.cameraStartAgain = Sequence(Walk1, Spin1)

        skelMove1 = self.skelCog.posInterval(0.50, Point3(-16, -0, 0))
        skelMove2 = self.skelCog.posInterval(2.00, Point3(0, -0, 0))
        self.skelMove = Sequence(skelMove1,
                                 skelMove2)

        Walk1 = self.camera.posInterval(15.50, Point3(6.31, -45.31, 9.27))
        Spin1 = self.camera.hprInterval(0.00, Vec3(337.52, 0, 0))
        Walk2 = self.camera.posInterval(0.00, Point3(6.08, -100.53, 9.27))
        Walk3 = self.camera.posInterval(12.00, Point3(14.07, -77.33, 9.27))
        Walk4 = self.camera.posInterval(0.00, Point3(18.93, -82.36, 25.51))
        Spin2 = self.camera.hprInterval(0.00, Vec3(30.26, 347.91, 0))
        Walk5 = self.camera.posInterval(15.00, Point3(0.44, -51.38, 21.411))
        Spin3 = self.camera.hprInterval(0.00, Vec3(337.52, 0, 0))
        self.cameraIntro = Sequence(Walk1, Spin1, Walk2, Walk3,
                                    Walk4, Spin2,
                                    Walk5, Spin3
             )
        self.cameraIntro.loop()

        rotate1 = self.camera.hprInterval(3.00, Vec3(-25, 0, 0))
        self.cameraRotate = Sequence(rotate1)

        fly = self.flyThru.hprInterval(1.00, Vec3(180, 0, 0))
        self.flyThruDONE = Sequence(
            fly
        )

        move1 = self.Sellbot.hprInterval(1.50, Vec3(196.26, 0, 0))
        move2 = self.Sellbot.posInterval(2.00, Point3(12.43, -5.09, 0))
        move3 = self.Sellbot.hprInterval(2.00, Vec3(140.91, 0, 0))
        self.SellbotMove = Sequence(
            move1, move2,
            move3
        )

        move1 = self.Lawbot.hprInterval(1.50, Vec3(196.26, 0, 0))
        move2 = self.Lawbot.posInterval(2.00, Point3(12.43, -5.09, 0))
        move3 = self.Lawbot.hprInterval(2.00, Vec3(140.91, 0, 0))
        self.LawbotMove = Sequence(move1, move2, move3)

        move1 = self.Cashbot.hprInterval(1.50, Vec3(196.26, 0, 0))
        move2 = self.Cashbot.posInterval(2.00, Point3(12.43, -5.09, 0))
        move3 = self.Cashbot.hprInterval(2.00, Vec3(140.91, 0, 0))
        self.CashbotMove = Sequence(move1, move2, move3)

        move1 = self.Bossbot.hprInterval(1.50, Vec3(196.26, 0, 0))
        move2 = self.Bossbot.posInterval(2.00, Point3(12.43, -5.09, 0))
        move3 = self.Bossbot.hprInterval(2.00, Vec3(140.91, 0, 0))
        self.BossbotMove = Sequence(move1, move2, move3)

        move1 = self.Sourcebot.hprInterval(1.50, Vec3(196.26, 0, 0))
        move2 = self.Sourcebot.posInterval(2.00, Point3(12.43, -5.09, 0))
        move3 = self.Sourcebot.hprInterval(2.00, Vec3(140.91, 0, 0))
        self.SourcebotMove = Sequence(move1, move2, move3)

        rotate1 = self.camera.hprInterval(1.00, Vec3(-21, 0, 0))
        move1 = self.camera.posInterval(1.00, Vec3(-2.24, -22.97, 5.02))
        self.toPro = Sequence(rotate1, move1)

        move1 = self.leftDoor.posInterval(1.50, Point3(0, 0, 0))
        self.elevatorOpenLeft = Sequence(
            move1
        )
        move1 = self.rightDoor.posInterval(1.50, Point3(0, 0, 0))
        self.elevatorOpenRight = Sequence(
            move1
        )

        lSmashB = self.lStomper.posInterval(0.125, Point3(0.01, 0, 3))
        lSmashE = self.lStomper.posInterval(1, Point3(-15, 0, 3))
        rSmashB = self.rStomper.posInterval(0.125, Point3(-0.01, 0, 3))
        rSmashE = self.rStomper.posInterval(1, Point3(15, 0, 3))
        lemmeSmashL = Sequence(lSmashB, Wait(1.25), lSmashE)
        lemmeSmashR = Sequence(rSmashB, Wait(1.25), rSmashE)
        self.lemmeSmash = \
            Parallel(
            lemmeSmashL, self.largeSmashExec,
            lemmeSmashR,
            name="Lemme Smash"
        )

        #----camera---#

        self.camera.setPos(6.31, -82.36, 9.27)
        self.camera.setHpr(35.71, 0, 0)

        #-----buttons-------#

        ButtonImage = self.loader.loadModel("phase_3/models/gui/cc_icon_gui_check_x.bam")
        self.finish = DirectButton(frameSize=None,
                          image=(ButtonImage.find('**/check_up'),
                                 ButtonImage.find(
                                     '**/check_down'),
                                 ButtonImage.find(
                                     '**/check_up')),
                          relief=None, clickSound=self.click, command=self.moveCameraToNameTag,
                          geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.5, 0, -0.8),
                          borderWidth=(0.13, 0.01), scale=.3)
        self.finish.hide()

        ButtonImage = self.loader.loadModel("phase_3/models/gui/cc_icon_gui_check_x.bam")
        self.finish2 = DirectButton(frameSize=None,
                                   image=(ButtonImage.find('**/check_up'),
                                          ButtonImage.find(
                                              '**/check_down'),
                                          ButtonImage.find(
                                              '**/check_up')),
                                   relief=None, clickSound=self.click, command=self.intoPro,
                                   geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.5, 0, -0.8),
                                   borderWidth=(0.13, 0.01), scale=.3)
        self.finish2.hide()

        ButtonImage = self.loader.loadModel("phase_3/models/gui/cc_icon_gui_check_x.bam")
        self.exit = DirectButton(frameSize=None,
                                   image=(ButtonImage.find('**/close_up'),
                                          ButtonImage.find(
                                              '**/close_down'),
                                          ButtonImage.find(
                                              '**/close_up')),
                                   relief=None, command=self.goBack, clickSound=self.click,
                                   geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(-1.5, 0, -0.8),
                                   borderWidth=(0.13, 0.01), scale=.3)
        self.exit.hide()

        self.folder = OnscreenImage(image='phase_3.5/maps/cc_metal-plate.png',
                                    pos=(1.50, 0, 0.4), scale=(0.6))
        self.folder.setTransparency(TransparencyAttrib.MAlpha)
        self.folder.hide()

        ButtonImage = loader.loadModel("phase_3/models/gui/cc_icon_gui_buttons_departments.bam")
        self.systems = DirectButton(frameSize=None,
                          image=(ButtonImage.find('**/button_up'),
                                 ButtonImage.find(
                                     '**/button_down'),
                                 ButtonImage.find(
                                     '**/button_hover')),
                          relief=None, command=self.systemGUIpopup, clickSound=self.click, rolloverSound=self.hover,
                          geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.3, 0, 0.8),
                          borderWidth=(0.13, 0.01), scale=0.5)
        self.systems.hide()

        ButtonImage = loader.loadModel("phase_3/models/gui/cc_icon_gui_buttons_arrow_skip.bam")
        self.SellbotButton = DirectButton(frameSize=None,
                                    image=(ButtonImage.find('**/click_up'),
                                           ButtonImage.find(
                                               '**/click_down'),
                                           ButtonImage.find(
                                               '**/click_hover')),
                                    relief=None, command=self.spawnSellbot, clickSound=self.click, rolloverSound=self.hover,
                                    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.5, 0, 0.6),
                                    borderWidth=(0.13, 0.01), scale=0.4)
        self.SellbotButton.hide()

        ButtonImage = loader.loadModel("phase_3/models/gui/cc_icon_gui_buttons_arrow_skip.bam")
        self.LawbotButton = DirectButton(frameSize=None,
                                    image=(ButtonImage.find('**/click_up'),
                                           ButtonImage.find(
                                               '**/click_down'),
                                           ButtonImage.find(
                                               '**/click_hover')),
                                    relief=None, command=self.spawnLawbot, clickSound=self.click, rolloverSound=self.hover,
                                    geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.5, 0, 0.5),
                                    borderWidth=(0.13, 0.01), scale=0.4)
        self.LawbotButton.hide()

        ButtonImage = loader.loadModel("phase_3/models/gui/cc_icon_gui_buttons_arrow_skip.bam")
        self.CashbotButton = DirectButton(frameSize=None,
                                         image=(ButtonImage.find('**/click_up'),
                                                ButtonImage.find(
                                                    '**/click_down'),
                                                ButtonImage.find(
                                                    '**/click_hover')),
                                         relief=None, command=self.spawnCashbot, clickSound=self.click, rolloverSound=self.hover,
                                         geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.5, 0, 0.4),
                                         borderWidth=(0.13, 0.01), scale=0.4)
        self.CashbotButton.hide()

        ButtonImage = loader.loadModel("phase_3/models/gui/cc_icon_gui_buttons_arrow_skip.bam")
        self.BossbotButton = DirectButton(frameSize=None,
                                          image=(ButtonImage.find('**/click_up'),
                                                 ButtonImage.find(
                                                     '**/click_down'),
                                                 ButtonImage.find(
                                                     '**/click_hover')),
                                          relief=None, command=self.spawnBossbot, clickSound=self.click, rolloverSound=self.hover,
                                          geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.5, 0, 0.3),
                                          borderWidth=(0.13, 0.01), scale=0.4)
        self.BossbotButton.hide()

        ButtonImage = loader.loadModel("phase_3/models/gui/cc_icon_gui_buttons_arrow_skip.bam")
        self.SourcebotButton = DirectButton(frameSize=None,
                                          image=(ButtonImage.find('**/click_up'),
                                                 ButtonImage.find(
                                                     '**/click_down'),
                                                 ButtonImage.find(
                                                     '**/click_hover')),
                                          relief=None, command=self.spawnSourcebot, clickSound=self.click, rolloverSound=self.hover,
                                          geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(1.5, 0, 0.2),
                                          borderWidth=(0.13, 0.01), scale=0.4)
        self.SourcebotButton.hide()

        ButtonImage = loader.loadModel("phase_5/models/cogdominium/tt_m_gui_csa_flyThru.bam")
        self.flyThruButton = DirectButton(frameSize=None,
                                            image=(ButtonImage.find('**/buttonUp'),
                                                   ButtonImage.find(
                                                       '**/buttonDown'),
                                                   ButtonImage.find(
                                                       '**/buttonHover')),
                                            relief=None, command=self.setText,
                                            geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(-0.2, 0, 0.75), clickSound=self.click, rolloverSound=self.hover,
                                            borderWidth=(0.13, 0.01), scale=4)
        self.flyThruButton.hide()

        #-----texts-------#
        self.logoLeft = OnscreenImage(image='phase_3/maps/cogcitycodeaffix-logo-hor-left[OLD].png', pos=(-0.46, 0, 0.2), scale=(0.7))
        self.logoLeft.setTransparency(TransparencyAttrib.MAlpha)

        self.logoRight = OnscreenImage(image='phase_3/maps/cogcitycodeaffix-logo-hor-right[OLD].png', pos=(0.56, 0, 0.18), scale=(0.7))
        self.logoRight.setTransparency(TransparencyAttrib.MAlpha)

        self.nameType = OnscreenImage(image='phase_3.5/maps/cc_type-a-name.png', pos=(-0.49, 0, 0.1), scale=0.8)
        self.nameType.setTransparency(TransparencyAttrib.MAlpha)
        self.nameType.hide()

        b = DirectEntry(text="", scale=.08, pos=(-0.9, 0, 0.08),
                        numLines=2, focus=3)
        b.hide()

        text = TextNode("play")
        text.setText("Press ENTER to play")
        text.setFont(font)

        self.textNodePath = aspect2d.attachNewNode(text)
        self.textNodePath.setScale(0.09)
        self.textNodePath.setPos(-0.5, 0, -0.7)

        self.text2 = TextNode("play")
        self.text2.setText("Hello, I am The Big Cheese, one of your superiors...")
        self.text2.setFont(font)
        self.text2.setWordwrap(25)
        self.textNodePath2 = aspect2d.attachNewNode(self.text2)
        self.textNodePath2.setScale(0.05)
        self.textNodePath2.setPos(-1.2, 0, 0.6)
        self.textNodePath2.setColor(0, 0, 0)
        self.textNodePath2.hide()

        #-----collisions-----#

        self.collblock = self.loader.loadModel("phase_4/models/modules/collisionBlock.bam")

        self.collblock = self.collblock.attachNewNode(CollisionNode('block_collision'))
        self.collblock.node().addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collblock.node().setIntoCollideMask(BitMask32.allOff())

        #-------times-----#

        self.t = Sequence(Func(self.finish.hide), Wait(9), Func(self.flyThru.show), Func(self.flyThruButton.show), Func(self.textNodePath2.show),
                          Func(self.cogDialMED.play))
        self.t2 = Sequence(Func(self.explosion.show), Wait(0.30), Func(self.explosion.hide))
        self.t3 = Sequence(Func(self.cameraMoveSfx.play), Wait(2.60), Func(self.cameraMoveSfx.stop),
                           Wait(2.50), Func(self.cameraMoveSfx.play), Wait(2.78), Func(self.cameraMoveSfx.stop), Wait(0.20))
        self.t4 = Sequence(Func(self.flyThruButton.hide), Wait(2.00), Func(self.flyThruButton.show))
        self.t5 = Sequence(Func(self.conveyorBeltSfx.play), Wait(2.50), Func(self.conveyorBeltSfx.stop))
        self.t6 = Sequence(Func(self.flyThruDONE.start), Wait(2.50), Func(self.flyThru.hide))
        self.t7 = Sequence(Func(self.moveINT), Func(self.cameraMoveSfx.play), Wait(5.50), Func(self.moveINTSTOP),
                                                                             Func(self.cameraMoveSfx.stop), Func(b.show), Func(self.finish2.show))
        self.t8 = Sequence(Func(self.cameraMoveSfx.play), Wait(2.00), Func(self.cameraMoveSfx.stop),
                           Wait(0.70), Func(self.elevatorOpenLeft.start), Func(self.elevatorOpenRight.start))


        #----------key/click-events-------#

        self.acceptOnce("enter-up", self.play)
        self.accept("alt-o", self.oobe)

        #------func-------#

    def setText(self):
           self.text2.setText("As the co-leader of COGS, Inc., i would like to introduce you to...")
           self.cogDialLONG.play()
           self.flyThruButton["command"] = self.setText2

    def setText2(self):
           self.text2.setText("Cogcity: CodeAffix!")
           self.cogDialSHORT.play()
           self.cogDialLONG.stop()
           self.flyThruButton["command"] = self.setText3

    def setText3(self):
        self.text2.setText("Before we get started, you need to create a cog first!")
        self.cogDialMED.play()
        self.cogDialSHORT.stop()
        self.flyThruButton["command"] = self.setText4

    def setText4(self):
        self.text2.setText("Here, i will send out a skelecog so that you can start making your new cog!")
        self.cogDialLONG.play()
        self.cogDialMED.stop()
        self.t4.start()
        self.skelMove.start()
        self.t5.start()
        self.flyThruButton["command"] = self.setText5

    def setText5(self):
        self.text2.setText("Here at Cogcity, we make sure that each of our cogs are fully functional.")
        self.cogDialMED.play()
        self.cogDialLONG.stop()
        self.flyThruButton["command"] = self.setText6

    def setText6(self):
        self.text2.setText("We call these special robots: Cogs, because of the file type named: .cog")
        self.cogDialLONG.play()
        self.flyThruButton["command"] = self.setText7

    def setText7(self):
        self.text2.setText(".cog is the file type for cogs which is in the departments folder.")
        self.cogDialMED.play()
        self.cogDialLONG.stop()
        self.flyThruButton["command"] = self.setText8

    def setText8(self):
        self.text2.setText("Just start by selecting your own .cog type in the departments folder.")
        self.cogDialLONG.play()
        self.cogDialMED.stop()
        self.flyThruButton["command"] = self.setText9

    def setText9(self):
        self.text2.setText("After that, type or choose your own cog name!")
        self.cogDialSHORT.play()
        self.cogDialLONG.stop()
        self.flyThruButton["command"] = self.setText10

    def setText10(self):
        self.text2.setText("Simple, right? I will be down in a second for the rest of the steps.")
        self.cogDialQUESTION.play()
        self.cogDialSHORT.stop()
        self.flyThruButton["command"] = self.setText11

    def setText11(self):
        self.text2.setText("Also, you might wanna hurry up... Our boss dose not like waiting.")
        self.cogDialMED.play()
        self.cogDialQUESTION.stop()
        self.flyThruButton["command"] = self.setTextFINAL

    def setTextFINAL(self):
        self.GUIpopup()
        self.textNodePath2.hide()
        self.flyThruButton.hide()
        self.t6.start()

    def play(self):
        if self.logoRight:
           self.logoRight.hide()
           self.logoLeft.hide()
           self.t3.start()
           self.t.start()
           self.textNodePath.hide()
           self.cameraIntro.pause()
           self.cameraStart.start()

    def playAgain(self):
        if self.logoRight:
           self.logoRight.hide()
           self.logoLeft.hide()
           self.textNodePath.hide()
           self.systems.show()
           self.finish.show()
           self.exit.show()
           self.cameraIntro.pause()
           self.cameraStartAgain.start()

    def GUIpopup(self):
        self.exit.show()
        self.systems.show()

    def goBack(self):
           self.acceptOnce("enter", self.playAgain)
           self.logoLeft.show()
           self.logoRight.show()
           self.SellbotButton.hide()
           self.LawbotButton.hide()
           self.CashbotButton.hide()
           self.BossbotButton.hide()
           self.SourcebotButton.hide()
           self.exit.hide()
           self.systems.hide()
           self.finish.hide()
           self.textNodePath.show()
           self.cameraIntro.finish()
           self.cameraIntro.start()
           self.cameraIntro.loop()


    def systemGUIpopup(self):
            if self.systems:
                self.SellbotButton.show()
                self.LawbotButton.show()
                self.CashbotButton.show()
                self.BossbotButton.show()
                self.SourcebotButton.show()
            else:
                self.SellbotButton.hide()
                self.LawbotButton.hide()
                self.CashbotButton.hide()
                self.BossbotButton.hide()
                self.SourcebotButton.hide()

    def spawnSellbot(self):
        if self.Sellbot:
            self.poof.play()
            self.Sellbot.show()
            self.t2.start()
            self.Cashbot.hide()
            self.Lawbot.hide()
            self.Bossbot.hide()
            self.Sourcebot.hide()
            self.finish.show()
        else:
            self.Sellbot.hide()

    def spawnLawbot(self):
        if self.Lawbot:
            self.poof.play()
            self.Sellbot.hide()
            self.t2.start()
            self.Cashbot.hide()
            self.Lawbot.show()
            self.Bossbot.hide()
            self.Sourcebot.hide()
            self.finish.show()
        else:
            self.Lawbot.hide()

    def spawnCashbot(self):
        if self.Cashbot:
            self.poof.play()
            self.Sellbot.hide()
            self.t2.start()
            self.Cashbot.show()
            self.Lawbot.hide()
            self.Bossbot.hide()
            self.Sourcebot.hide()
            self.finish.show()
        else:
            self.Cashbot.hide()

    def spawnBossbot(self):
        if self.Bossbot:
            self.poof.play()
            self.t2.start()
            self.Sellbot.hide()
            self.Cashbot.hide()
            self.Lawbot.hide()
            self.Bossbot.show()
            self.Sourcebot.hide()
            self.finish.show()
        else:
            self.Bossbot.hide()

    def spawnSourcebot(self):
        if self.Sourcebot:
            self.t2.start()
            self.poof.play()
            self.Sellbot.hide()
            self.Cashbot.hide()
            self.Lawbot.hide()
            self.Bossbot.hide()
            self.Sourcebot.show()
            self.finish.show()
        else:
            self.Sourcebot.hide()

    def switchToSolidBody(self, task):
        self.skelCog.hide()
        if self.Sellbot:
            self.Sellbot.setTransparency(TransparencyAttrib.MNone)
            self.Sellbot.clearColor()
            self.Sellbot.find('**/hands').setColor(0.55, 0.65, 1.0, 1.0)
        if self.Lawbot:
            self.Lawbot.setTransparency(TransparencyAttrib.MNone)
            self.Lawbot.clearColor()
            self.Lawbot.find('**/hands').setColor(0.75, 0.75, 0.95, 1.0)
        if self.Cashbot:
            self.Cashbot.setTransparency(TransparencyAttrib.MNone)
            self.Cashbot.clearColor()
            self.Cashbot.find('**/hands').setColor(1.0, 0.5, 0.6, 1.0)
        if self.Bossbot:
            self.Bossbot.setTransparency(TransparencyAttrib.MNone)
            self.Bossbot.clearColor()
            self.Bossbot.find('**/hands').setColor(0.95, 0.75, 0.75, 1.0)
        if self.Sourcebot:
            self.Sourcebot.setTransparency(TransparencyAttrib.MNone)
            self.Sourcebot.clearColor()
            self.Sourcebot.find('**/hands').setColor(0.53, 0.59, 0.66, 1.0)
        return Task.done

    def walkToNameTag(self, task):
        self.cameraMoveSfx.play()
        self.cameraRotate.start()
        self.SellbotMove.start()
        self.LawbotMove.start()
        self.CashbotMove.start()
        self.BossbotMove.start()
        self.SourcebotMove.start()
        self.lStomper.hide()
        self.rStomper.hide()
        self.t7.start()
        self.Cashbot.loop('walk')
        self.Sellbot.loop('walk')
        self.Lawbot.loop('walk')
        self.Bossbot.loop('walk')
        self.Sourcebot.loop('walk')
        return Task.done

    def moveCameraToNameTag(self):
        if self.camera:
            self.SellbotButton.hide()
            self.LawbotButton.hide()
            self.CashbotButton.hide()
            self.BossbotButton.hide()
            self.SourcebotButton.hide()
            self.finish.hide()
            self.exit.hide()
            self.systems.hide()
            self.lStomper.show()
            self.rStomper.show()
            self.lemmeSmash.start()
            self.smashDelay = Parallel(self.largeSmashExec)
            self.smashDelay.start()
            taskMgr.doMethodLater(.75, self.switchToSolidBody, 'Make Cogs With Hologram Bodies Have Solid Ones')
            taskMgr.doMethodLater(3.5, self.walkToNameTag, 'Make Cogs Walk To Type-A-Name')

    def moveINT(self):
        if self.moveCameraToNameTag:
            self.Sellbot.play('walk')
            self.Lawbot.play('walk')
            self.Cashbot.play('walk')
            self.Bossbot.play('walk')
            self.Sourcebot.play('walk')
            self.Sellbot.loop('walk')
            self.Lawbot.loop('walk')
            self.Cashbot.loop('walk')
            self.Bossbot.loop('walk')
            self.Sourcebot.loop('walk')

    def moveINTSTOP(self):
        if self.moveCameraToNameTag:
            self.Sellbot.stop('walk')
            self.Lawbot.stop('walk')
            self.Cashbot.stop('walk')
            self.Bossbot.stop('walk')
            self.Sourcebot.stop('walk')
            self.Sellbot.play('neutral')
            self.Lawbot.play('neutral')
            self.Cashbot.play('neutral')
            self.Bossbot.play('neutral')
            self.Sourcebot.play('neutral')
            self.Sellbot.loop('neutral')
            self.Lawbot.loop('neutral')
            self.Cashbot.loop('neutral')
            self.Bossbot.loop('neutral')
            self.Sourcebot.loop('neutral')

    def intoPro(self):
        if self.makeAcog:
            self.toPro.start()
            self.t8.start()

def makeAcog(data):
    print(data)
game = GameTest()