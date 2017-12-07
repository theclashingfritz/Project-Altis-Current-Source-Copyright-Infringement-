from toontown.suit import DistributedFactorySuit
from toontown.suit.Suit import *
from direct.directnotify import DirectNotifyGlobal
from direct.actor import Actor
from otp.avatar import Avatar
from toontown.suit import SuitDNA
from toontown.toonbase import ToontownGlobals
from panda3d.core import *
from panda3d.direct import *
from toontown.battle import SuitBattleGlobals
from direct.task import Task
from toontown.battle import BattleProps
from toontown.toonbase import TTLocalizer
import string

class DistributedStageSuit(DistributedFactorySuit.DistributedFactorySuit):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedStageSuit')

    def setCogSpec(self, spec):
        self.spec = spec
        self.setPos(spec['pos'])
        self.setH(spec['h'])
        self.originalPos = spec['pos']
        self.escapePos = spec['pos']
        self.pathEntId = spec['path']
        self.behavior = spec['behavior']
        self.skeleton = spec['skeleton']
        self.boss = spec['boss']
        self.revives = spec.get('revives')
        if self.reserve:
            self.reparentTo(hidden)
        else:
            self.doReparent()
        if self.boss:
            self.renameBoss()

    def renameBoss(self):
        if self.getSkeleRevives() > 0:
            nameInfo = TTLocalizer.SuitBaseNameWithLevel % {'name': TTLocalizer.Clerk,
             'dept': self.getStyleDept(),
             'level': '%s%s%s' % (self.getActualLevel(), TTLocalizer.SkeleRevivePostFix, ' Elite')}
            self.setName(TTLocalizer.Clerk)
            self.setDisplayName(nameInfo)
        else:
            nameInfo = TTLocalizer.SuitBaseNameWithLevel % {'name': TTLocalizer.Clerk,
             'dept': self.getStyleDept(),
             'level': str(self.getActualLevel()) + ' Elite'}
            self.setName(TTLocalizer.Clerk)
            self.setDisplayName(nameInfo)
