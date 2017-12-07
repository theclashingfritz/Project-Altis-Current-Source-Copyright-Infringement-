from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.movement.PyVec3 import PyVec3
from toontown.toonbase import ToonPythonUtil as PythonUtil
import __builtin__

class Mover:
    notify = DirectNotifyGlobal.directNotify.newCategory('Mover')
    SerialNum = 0
    Profile = 0
    Pstats = 1
    PSCPy = 'App:Show code:moveObjects:MoverPy'

    def __init__(self, objNodePath, fwdSpeed = 1, rotSpeed = 1):
        self.serialNum = Mover.SerialNum
        Mover.SerialNum += 1
        self.VecType = Vec3
        self.impulses = {}
        if Mover.Pstats:
            self.pscPy = PStatCollector(Mover.PSCPy)

    def destroy(self):
        for name, impulse in self.impulses.items():
            Mover.notify.debug('removing impulse: %s' % name)
            self.removeImpulse(name)

    def addImpulse(self, name, impulse):
        self.impulses[name] = impulse
        impulse._setMover(self)

    def removeImpulse(self, name):
        self.impulses[name]._clearMover(self)
        del self.impulses[name]

    def getCollisionEventName(self):
        return 'moverCollision-%s' % self.serialNum

    def move(self, dt = -1, profile = 0):
        if Mover.Profile and not profile:

            def func(doMove = self.move):
                for i in xrange(10000):
                    doMove(dt, profile=1)

            __builtin__.func = func
            PythonUtil.startProfile(cmd='func()', filename='profile', sorts=['cumulative'], callInfo=0)
            del __builtin__.func
            return

        if Mover.Pstats:
            self.pscPy.start()
        for impulse in self.impulses.values():
            impulse._process(self.getDt())
        if Mover.Pstats:
            self.pscPy.stop()
