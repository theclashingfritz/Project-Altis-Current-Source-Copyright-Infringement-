from toontown.coghq.SpecImports import *
from toontown.toonbase import ToontownGlobals
import random
CogParent = 10000
GuardCogParent = 10021
BattleCellId = 0
GuardBattleCellId = 1
BattleCells = {BattleCellId: {'parentEntId': CogParent,
                'pos': Point3(0, 0, 0)},
 GuardBattleCellId: {'parentEntId': GuardCogParent,
                     'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': 1,
  'level': ToontownGlobals.BoardOfficeBossLevel,
  'battleCell': BattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0,
  'revives': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.BoardOfficeSkelecogLevel,
  'battleCell': BattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.BoardOfficeCogLevel,
  'battleCell': BattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': ToontownGlobals.BoardOfficeCogLevel,
  'battleCell': BattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([5, 6, 7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1}]
ReserveCogData = []
