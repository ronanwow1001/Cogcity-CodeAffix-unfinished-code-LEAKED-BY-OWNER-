from panda3d.core import TransparencyAttrib
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

class GameTest(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self. FlairDirector = Actor('phase_3.5/models/char/suitC-mod.bam',
                               {'neutral': 'phase_3.5/models/char/suitC-neutral.bam',
                                'victory': 'phase_4/models/char/suitC-victory.bam',
                                'walk': 'phase_3.5/models/char/suitC-walk.bam'})

        self.FlairDirector.reparentTo(render)
        self.FlairDirector.loop('neutral')
        self.TorsoTex = loader.loadTexture('phase_3.5/maps/t_blazer.jpg')
        self.FlairDirector.find('**/torso').setTexture(self.TorsoTex, 1)
        self.ArmTex = loader.loadTexture('phase_3.5/maps/t_sleeve.jpg')
        self.FlairDirector.find('**/arms').setTexture(self.ArmTex, 1)
        self.LegTex = loader.loadTexture('phase_3.5/maps/t_leg.jpg')
        self.FlairDirector.find('**/legs').setTexture(self.LegTex, 1)
        self.Head = loader.loadModel('phase_3.5/models/char/FlairDirector.egg')
        self.headTexture = loader.loadTexture("phase_3.5/maps/flair-director.jpg")
        self.Head.reparentTo(self.FlairDirector.find('**/joint_head'))
        self.FlairDirector.findAllMatches('**/joint_head').setTexture(self.headTexture, 1)
        self.icon = loader.loadModel('phase_3/models/gui/SourcebotIcon.bam')
        self.icon.reparentTo(render)
        self.iconTexture = loader.loadTexture('phase_3/maps/SourcebotIcon.png')
        self.icon.setTexture(self.iconTexture, 1)
        self.icon.setHpr(180, 0, 0)
        self.icon.setPos(0.1, 0, -0.30)
        self.icon.setScale(1.00)
        self.icon.reparentTo(self.FlairDirector.find('**/joint_attachMeter'))
        self.FlairDirector.setScale(1.70)

def Flair(data):
    print (data)


game = GameTest()
run()

