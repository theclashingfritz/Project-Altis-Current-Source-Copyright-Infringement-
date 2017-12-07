from toontown.toonbase.ToonPythonUtil import invertDict
from toontown.toonbase import ToontownGlobals
from toontown.coghq import NullCogs
from toontown.coghq import CashbotMintBoilerRoom_Battle00_Cogs
from toontown.coghq import CashbotMintBoomerangRoom_Battle00_Cogs
from toontown.coghq import CashbotMintBoilerRoom_Battle01_Cogs
from toontown.coghq import CashbotMintControlRoom_Battle00_Cogs
from toontown.coghq import CashbotMintDuctRoom_Battle00_Cogs
from toontown.coghq import CashbotMintDuctRoom_Battle01_Cogs
from toontown.coghq import CashbotMintGearRoom_Battle00_Cogs
from toontown.coghq import CashbotMintGearRoom_Battle01_Cogs
from toontown.coghq import CashbotMintLavaRoomFoyer_Battle00_Cogs
from toontown.coghq import CashbotMintLavaRoomFoyer_Battle01_Cogs
from toontown.coghq import CashbotMintLobby_Battle00_Cogs
from toontown.coghq import CashbotMintLobby_Battle01_Cogs
from toontown.coghq import CashbotMintOilRoom_Battle00_Cogs
from toontown.coghq import CashbotMintPaintMixerReward_Battle00_Cogs
from toontown.coghq import CashbotMintPipeRoom_Battle00_Cogs
from toontown.coghq import CashbotMintPipeRoom_Battle01_Cogs
from toontown.coghq import CashbotMintPaintMixer_Battle00
from toontown.coghq import CashbotMintPaintMixer_Battle00_Cogs
from toontown.coghq import CashbotMintStomperAlley_Action01

# Explicit imports for the below room modules:
from toontown.coghq import CashbotMintEntrance_Action00
from toontown.coghq import CashbotMintBoilerRoom_Action00
from toontown.coghq import CashbotMintBoilerRoom_Battle00
from toontown.coghq import CashbotMintBoomerangRoom_Battle00
from toontown.coghq import CashbotMintDuctRoom_Action00
from toontown.coghq import CashbotMintDuctRoom_Battle00
from toontown.coghq import CashbotMintGearRoom_Action00
from toontown.coghq import CashbotMintGearRoom_Battle00
from toontown.coghq import CashbotMintLavaRoomFoyer_Action00
from toontown.coghq import CashbotMintLavaRoomFoyer_Action01
from toontown.coghq import CashbotMintLavaRoomFoyer_Battle00
from toontown.coghq import CashbotMintLavaRoom_Action00
from toontown.coghq import CashbotMintLobby_Action00
from toontown.coghq import CashbotMintLobby_Battle00
from toontown.coghq import CashbotMintPaintMixer_Action00
from toontown.coghq import CashbotMintPipeRoom_Action00
from toontown.coghq import CashbotMintPipeRoom_Battle00
from toontown.coghq import CashbotMintStomperAlley_Action00
from toontown.coghq import CashbotMintBoilerRoom_Battle01
from toontown.coghq import CashbotMintControlRoom_Battle00
from toontown.coghq import CashbotMintDuctRoom_Battle01
from toontown.coghq import CashbotMintGearRoom_Battle01
from toontown.coghq import CashbotMintLavaRoomFoyer_Battle01
from toontown.coghq import CashbotMintOilRoom_Battle00
from toontown.coghq import CashbotMintLobby_Battle01
from toontown.coghq import CashbotMintPaintMixerReward_Battle00
from toontown.coghq import CashbotMintPipeRoom_Battle01

def getMintRoomSpecModule(roomId):
    return CashbotMintSpecModules[roomId]


def getCogSpecModule(roomId):
    roomName = CashbotMintRoomId2RoomName[roomId]
    return CogSpecModules.get(roomName, NullCogs)


def getNumBattles(roomId):
    return roomId2numBattles[roomId]


CashbotMintRoomId2RoomName = {0: 'CashbotMintEntrance_Action00',
 1: 'CashbotMintBoilerRoom_Action00',
 2: 'CashbotMintBoilerRoom_Battle00',
 3: 'CashbotMintDuctRoom_Action00',
 4: 'CashbotMintDuctRoom_Battle00',
 5: 'CashbotMintGearRoom_Action00',
 6: 'CashbotMintGearRoom_Battle00',
 7: 'CashbotMintLavaRoomFoyer_Action00',
 8: 'CashbotMintLavaRoomFoyer_Action01',
 9: 'CashbotMintLavaRoomFoyer_Battle00',
 10: 'CashbotMintLavaRoom_Action00',
 11: 'CashbotMintLobby_Action00',
 12: 'CashbotMintLobby_Battle00',
 13: 'CashbotMintPaintMixer_Action00',
 14: 'CashbotMintPaintMixer_Battle00',
 15: 'CashbotMintPipeRoom_Action00',
 16: 'CashbotMintPipeRoom_Battle00',
 17: 'CashbotMintStomperAlley_Action00',
 18: 'CashbotMintStomperAlley_Action01',
 19: 'CashbotMintBoomerangRoom_Battle00',
 20: 'CashbotMintBoilerRoom_Battle01',
 21: 'CashbotMintControlRoom_Battle00',
 22: 'CashbotMintDuctRoom_Battle01',
 23: 'CashbotMintGearRoom_Battle01',
 24: 'CashbotMintLavaRoomFoyer_Battle01',
 25: 'CashbotMintOilRoom_Battle00',
 26: 'CashbotMintLobby_Battle01',
 27: 'CashbotMintPaintMixerReward_Battle00',
 28: 'CashbotMintPipeRoom_Battle01'}
CashbotMintRoomName2RoomId = invertDict(CashbotMintRoomId2RoomName)
CashbotMintEntranceIDs = (0,)
CashbotMintMiddleRoomIDs = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
CashbotMintFinalRoomIDs = (20, 21, 22, 23, 24, 25, 26, 27, 28)
CashbotMintConnectorRooms = ('phase_10/models/cashbotHQ/connector_7cubeL2', 'phase_10/models/cashbotHQ/connector_7cubeR2')
CashbotMintSpecModules = {}
for roomName, roomId in CashbotMintRoomName2RoomId.items():
    CashbotMintSpecModules[roomId] = locals()[roomName]

CogSpecModules = {'CashbotMintBoilerRoom_Battle00': CashbotMintBoilerRoom_Battle00_Cogs,
 'CashbotMintBoilerRoom_Battle01': CashbotMintBoilerRoom_Battle01_Cogs,
 'CashbotMintBoomerangRoom_Battle00': CashbotMintBoomerangRoom_Battle00_Cogs,
 'CashbotMintControlRoom_Battle00': CashbotMintControlRoom_Battle00_Cogs,
 'CashbotMintDuctRoom_Battle00': CashbotMintDuctRoom_Battle00_Cogs,
 'CashbotMintDuctRoom_Battle01': CashbotMintDuctRoom_Battle01_Cogs,
 'CashbotMintGearRoom_Battle00': CashbotMintGearRoom_Battle00_Cogs,
 'CashbotMintGearRoom_Battle01': CashbotMintGearRoom_Battle01_Cogs,
 'CashbotMintLavaRoomFoyer_Battle00': CashbotMintLavaRoomFoyer_Battle00_Cogs,
 'CashbotMintLavaRoomFoyer_Battle01': CashbotMintLavaRoomFoyer_Battle01_Cogs,
 'CashbotMintLobby_Battle00': CashbotMintLobby_Battle00_Cogs,
 'CashbotMintLobby_Battle01': CashbotMintLobby_Battle01_Cogs,
 'CashbotMintOilRoom_Battle00': CashbotMintOilRoom_Battle00_Cogs,
 'CashbotMintPaintMixer_Battle00': CashbotMintPaintMixer_Battle00_Cogs,
 'CashbotMintPaintMixerReward_Battle00': CashbotMintPaintMixerReward_Battle00_Cogs,
 'CashbotMintPipeRoom_Battle00': CashbotMintPipeRoom_Battle00_Cogs,
 'CashbotMintPipeRoom_Battle01': CashbotMintPipeRoom_Battle01_Cogs}
roomId2numBattles = {}
for roomName, roomId in CashbotMintRoomName2RoomId.items():
    if roomName not in CogSpecModules:
        roomId2numBattles[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        roomId2numBattles[roomId] = len(cogSpecModule.BattleCells)

name2id = CashbotMintRoomName2RoomId
roomId2numBattles[name2id['CashbotMintBoilerRoom_Battle00']] = 3
roomId2numBattles[name2id['CashbotMintPipeRoom_Battle00']] = 2
del name2id
middleRoomId2numBattles = {}
for roomId in CashbotMintMiddleRoomIDs:
    middleRoomId2numBattles[roomId] = roomId2numBattles[roomId]
