from toontown.toon.DistributedNPCToonAI import *

class DistributedNPCLoopyGAI(DistributedNPCToonAI):

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonAI.__init__(self, air, npcId, questCallback)
