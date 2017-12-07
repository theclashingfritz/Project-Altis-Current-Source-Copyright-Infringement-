from pandac.PandaModules import Vec4
from toontown.safezone.OZSafeZoneLoader import OZSafeZoneLoader
from toontown.town.OZTownLoader import OZTownLoader
from toontown.toonbase import ToontownGlobals
from toontown.hood.ToonHood import ToonHood

class OZHood(ToonHood):
    notify = directNotify.newCategory('OZHood')

    ID = ToontownGlobals.OutdoorZone
    TOWNLOADER_CLASS = OZTownLoader
    SAFEZONELOADER_CLASS = OZSafeZoneLoader
    STORAGE_DNA = 'phase_6/dna/storage_OZ.pdna'
    SKY_FILE = 'phase_3.5/models/props/TT_sky'
    SPOOKY_SKY_FILE = 'phase_3.5/models/props/BR_sky'
    TITLE_COLOR = (1.0, 0.5, 0.4, 1.0)

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.underwaterColor = Vec4(0.23921568627450980392156862745098, 0.84705882352941176470588235294118, 1, 1)

    def load(self):
        ToonHood.load(self)

        self.fog = Fog('OZFog')

    def enter(self, requestStatus):
        ToonHood.enter(self, requestStatus)

        base.camLens.setNearFar(ToontownGlobals.SpeedwayCameraNear, ToontownGlobals.SpeedwayCameraFar)

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)

        ToonHood.exit(self)