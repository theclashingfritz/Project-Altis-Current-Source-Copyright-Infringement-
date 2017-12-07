from direct.gui.DirectGui import *
from panda3d.core import *
from panda3d.direct import *
from toontown.toonbase.ToontownBattleGlobals import *
from toontown.toon import InventoryBase
from toontown.toonbase import TTLocalizer
from toontown.battle import BattleGlobals
from toontown.quest import BlinkingArrows
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from toontown.toontowngui import TTDialog

class InventoryNewNEW(InventoryBase.InventoryBase, DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryNew')
    PressableTextColor = Vec4(1, 1, 1, 1)
    PressableGeomColor = Vec4(1, 1, 1, 1)
    PressableImageColor = Vec4(0, 0.6, 1, 1)
    PropBonusPressableImageColor = Vec4(1.0, 0.6, 0.0, 1)
    NoncreditPressableImageColor = Vec4(0.3, 0.6, 0.6, 1)
    PropBonusNoncreditPressableImageColor = Vec4(0.6, 0.6, 0.3, 1)
    DeletePressableImageColor = Vec4(0.7, 0.1, 0.1, 1)
    UnpressableTextColor = Vec4(1, 1, 1, 0.3)
    UnpressableGeomColor = Vec4(1, 1, 1, 0.3)
    UnpressableImageColor = Vec4(0.3, 0.3, 0.3, 0.8)
    BookUnpressableTextColor = Vec4(1, 1, 1, 1)
    BookUnpressableGeomColor = Vec4(1, 1, 1, 1)
    BookUnpressableImage0Color = Vec4(0, 0.6, 1, 1)
    BookUnpressableImage2Color = Vec4(0.1, 0.7, 1, 1)
    ShadowColor = Vec4(0, 0, 0, 0)
    ShadowBuffedColor = Vec4(1, 1, 1, 1)
    UnpressableShadowBuffedColor = Vec4(1, 1, 1, 0.3)
    TrackYOffset = 0.0
    TrackYSpacing = -0.12
    ButtonXOffset = -0.31
    ButtonXSpacing = 0.18

    def __init__(self, toon, invStr = None, ShowSuperGags = 1):
        InventoryBase.InventoryBase.__init__(self, toon, invStr)
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(InventoryNewNEW)
        self.battleCreditLevel = None
        self.detailCredit = None
        self.__battleCreditMultiplier = 1
        self.__invasionCreditMultiplier = 1
        self.__respectInvasions = 1
        self._interactivePropTrackBonus = -1
        self.tutorialFlag = 0
        self.gagTutMode = 0
        self.showSuperGags = ShowSuperGags
        self.clickSuperGags = 1
        self.activeTab = 4
        self.propAndOrganicBonusStack = config.GetBool('prop-and-organic-bonus-stack', 0)
        self.propBonusIval = Parallel()
        self.activateMode = 'book'
        self.load()
        self.hide()

    def setBattleCreditMultiplier(self, mult):
        self.__battleCreditMultiplier = mult

    def getBattleCreditMultiplier(self):
        return self.__battleCreditMultiplier

    def setInteractivePropTrackBonus(self, trackBonus):
        self._interactivePropTrackBonus = trackBonus

    def getInteractivePropTrackBonus(self):
        return self._interactivePropTrackBonus

    def setInvasionCreditMultiplier(self, mult):
        self.__invasionCreditMultiplier = mult

    def getInvasionCreditMultiplier(self):
        return self.__invasionCreditMultiplier

    def setRespectInvasions(self, flag):
        self.__respectInvasions = flag

    def getRespectInvasions(self):
        return self.__respectInvasions

    def show(self):
        if self.tutorialFlag:
            self.tutArrows.arrowsOn(-0.4, -0.62, 90, -0.4, -0.62, 90, onTime=1.0, offTime=0.2)
            if self.numItem(THROW_TRACK, 0) == 0:
                self.tutArrows.arrow1.reparentTo(hidden)
            else:
                self.tutArrows.arrow1.reparentTo(self.battleFrame, 1)
            if self.numItem(SQUIRT_TRACK, 0) == 0:
                self.tutArrows.arrow2.reparentTo(hidden)
            else:
                self.tutArrows.arrow2.reparentTo(self.battleFrame, 1)
            self.tutText.show()
            self.tutText.reparentTo(self.battleFrame, 1)
        
        DirectFrame.show(self)

    def uberGagToggle(self, showSuperGags = 1):
        self.showSuperGags = showSuperGags
        for itemList in self.invModels:
            for itemIndex in xrange(MAX_LEVEL_INDEX + 1):
                if itemIndex <= LAST_REGULAR_GAG_LEVEL + 1 or self.showSuperGags:
                    itemList[itemIndex].show()
                else:
                    itemList[itemIndex].hide()

        for buttonList in self.buttons:
            for buttonIndex in xrange(MAX_LEVEL_INDEX + 1):
                if buttonIndex <= LAST_REGULAR_GAG_LEVEL or self.showSuperGags:
                    buttonList[buttonIndex].show()
                else:
                    buttonList[buttonIndex].hide()

    def enableUberGags(self, enableSG = -1):
        if enableSG != -1:
            self.clickSuperGags = enableSG
        
        for buttonList in self.buttons:
            for buttonIndex in xrange(LAST_REGULAR_GAG_LEVEL + 1, MAX_LEVEL_INDEX + 1):
                if self.clickSuperGags:
                    pass
                else:
                    self.makeUnpressable(buttonList[buttonIndex], self.buttons.index(buttonList), buttonIndex)

    def hide(self):
        if self.tutorialFlag:
            self.tutArrows.arrowsOff()
            self.tutText.hide()
        
        DirectFrame.hide(self)

    def updateTotalPropsText(self):
        textTotal = TTLocalizer.InventoryTotalGags % (self.totalProps, self.toon.getMaxCarry())
        if localAvatar.getPinkSlips() > 1:
            textTotal = textTotal + '\n\n' + TTLocalizer.InventroyPinkSlips % localAvatar.getPinkSlips()
        elif localAvatar.getPinkSlips() == 1:
            textTotal = textTotal + '\n\n' + TTLocalizer.InventroyPinkSlip
        self.totalLabel['text'] = textTotal

    def unload(self):
        self.notify.debug('Unloading Inventory for %d' % self.toon.doId)
        self.stopAndClearPropBonusIval()
        self.propBonusIval.finish()
        self.propBonusIval = None
        del self.invModels
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.upButton
        del self.downButton
        del self.rolloverButton
        del self.flatButton
        del self.invFrame
        del self.levelsButton
        del self.battleFrame
        del self.purchaseFrame
        del self.storePurchaseFrame
        self.deleteAllButton.destroy()
        del self.deleteAllButton
        self.deleteEnterButton.destroy()
        del self.deleteEnterButton
        self.deleteExitButton.destroy()
        del self.deleteExitButton
        del self.detailFrame
        del self.detailNameLabel
        del self.detailAmountLabel
        del self.detailDataLabel
        del self.totalLabel
        del self.activeTab
        self.cleanupDialog()

        for row in self.trackRows:
            row.destroy()

        del self.trackRows
        del self.trackNameLabels
        del self.trackBars
        for buttonList in self.buttons:
            for buttonIndex in xrange(MAX_LEVEL_INDEX + 1):
                buttonList[buttonIndex].destroy()

        del self.buttons
        InventoryBase.InventoryBase.unload(self)
        DirectFrame.destroy(self)

    def cleanupDialog(self):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None

    def load(self):
        self.notify.debug('Loading Inventory for %d' % self.toon.doId)
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        self.invModels = []
        offset = 0.0
        for track in xrange(len(AvPropsNew)):
            itemList = []
            for item in xrange(len(AvPropsNew[track])):
                itemList.append(invModel.find('**/' + AvPropsNew[track][item]))

            self.invModels.append(itemList)

        invModel.removeNode()
        del invModel
        self.buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        self.battleGui = loader.loadModel('phase_3.5/models/gui/battle_gui_new')
        self.healRow =  self.battleGui.find('**/healBar')
        self.trapRow =  self.battleGui.find('**/trapBar')
        self.lureRow =  self.battleGui.find('**/lureBar')
        self.soundRow =  self.battleGui.find('**/soundBar')
        self.throwRow =  self.battleGui.find('**/throwBar')
        self.squirtRow =  self.battleGui.find('**/squirtBar')
        self.zapRow =  self.battleGui.find('**/zapBar')
        self.dropRow =  self.battleGui.find('**/dropBar')
        bars = [self.healRow, self.trapRow, self.lureRow, self.soundRow, self.throwRow, self.squirtRow, self.zapRow, self.dropRow]
        self.battleCircle =  self.battleGui.find('**/battleCircle')
        self.tab = self.battleGui.find('**/whiteTab')
        self.rowModel = self.buttonModels.find('**/InventoryRow')
        self.rowModel = self.buttonModels.find('**/InventoryRow')
        self.upButton = self.buttonModels.find('**/InventoryButtonUp')
        self.downButton = self.buttonModels.find('**/InventoryButtonDown')
        self.rolloverButton = self.buttonModels.find('**/InventoryButtonRollover')
        self.flatButton = self.buttonModels.find('**/InventoryButtonFlat')
        self.invFrame = DirectFrame(relief=None, parent=self)
        self.levelsButton = None
        self.battleFrame = None
        self.purchaseFrame = None
        self.storePurchaseFrame = None
        trashcanGui = loader.loadModel('phase_3/models/gui/trashcan_gui')
        self.deleteEnterButton = DirectButton(parent=self.invFrame, image=(trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_RLVR')), text=('', TTLocalizer.InventoryDelete, TTLocalizer.InventoryDelete), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.1, text_pos=(0, -0.1), text_font=getInterfaceFont(), textMayChange=0, relief=None, pos=(-1.3, 0, -0.35), scale=0.70)
        self.deleteAllButton = DirectButton(parent=self.invFrame, image=(trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_RLVR')), text=('', TTLocalizer.InventoryDeleteAll, TTLocalizer.InventoryDeleteAll), text_fg=(1, 0, 0, 1), text_shadow=(1, 1, 1, 1), text_scale=0.1, text_pos=(0, -0.1), text_font=getInterfaceFont(), textMayChange=0, relief=None, pos=(0.55, 0, -1), scale=0.75, command=self.__zeroInvConfirm)
        self.deleteExitButton = DirectButton(parent=self.invFrame, image=(trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_RLVR')), text=('', TTLocalizer.InventoryDone, TTLocalizer.InventoryDone), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.1, text_pos=(0, -0.1), text_font=getInterfaceFont(), textMayChange=0, relief=None, pos=(-1, 0, -0.35), scale=1.0)
        trashcanGui.removeNode()
        self.deleteHelpText = DirectLabel(parent=self.invFrame, relief=None, pos=(0.272, 0.3, -0.907), text=TTLocalizer.InventoryDeleteHelp, text_fg=(0, 0, 0, 1), text_scale=0.08, textMayChange=0)
        self.deleteHelpText.hide()
        self.trackRows = []
        self.trackTabs = []
        self.trackNameLabels = []
        self.trackBars = []
        self.buttons = []
        for track in xrange(len(Tracks)):
            trackTab = DirectButton(parent=self.invFrame, text=TextEncoder.upper(Tracks[track]), relief=None, scale=(0.5, 0.5, 0.5), pos=(-0.7 + offset, 0, -0.54), geom=self.tab, geom_color=(TrackColors[track][0] * 0.6,
         TrackColors[track][1] * 0.6,
         TrackColors[track][2] * 0.6,
         1), text_font=ToontownGlobals.getInterfaceFont(), text_scale=TTLocalizer.INtrackNameLabels, text_pos=(0,0,0), text_align=TextNode.ACenter, command=self.doTab, extraArgs=[track], pressEffect=1)
            offset += 0.2
            trackFrame = DirectFrame(parent=self.invFrame, image=bars[track], scale=(1.0, 1.0, 1.0), pos=(0, 0, -0.7), state=DGG.NORMAL, relief=None)
            trackFrame.bind(DGG.WITHIN, self.enterTrackFrame, extraArgs=[track])
            trackFrame.bind(DGG.WITHOUT, self.exitTrackFrame, extraArgs=[track])
            self.trackRows.append(trackFrame)
            self.trackTabs.append(trackTab)
            adjustLeft = -0.065
            self.trackNameLabels.append(DirectLabel(text=TextEncoder.upper(Tracks[track]), parent=self.trackRows[track], pos=(-0.72 + adjustLeft, -0.1, 0.01), scale=TTLocalizer.INtrackNameLabels, relief=None, text_fg=(0.2, 0.2, 0.2, 1), text_font=getInterfaceFont(), text_align=TextNode.ALeft, textMayChange=0))
            self.trackBars.append(DirectWaitBar(parent=self.trackRows[track], pos=(-0.58 + adjustLeft, -0.1, -0.025), relief=DGG.SUNKEN, frameSize=(-0.6,
             0.6,
             -0.1,
             0.1), borderWidth=(0.02, 0.02), scale=0.25, frameColor=(TrackColors[track][0] * 0.6,
             TrackColors[track][1] * 0.6,
             TrackColors[track][2] * 0.6,
             1), barColor=(TrackColors[track][0] * 0.9,
             TrackColors[track][1] * 0.9,
             TrackColors[track][2] * 0.9,
             1), text='0 / 0', text_scale=0.16, text_fg=(0, 0, 0, 0.8), text_align=TextNode.ACenter, text_pos=(0, -0.05)))
            self.buttons.append([])
            for item in xrange(len(Levels[track])):
                button = DirectButton(parent=self.trackRows[track], image=(self.upButton,
                 self.downButton,
                 self.rolloverButton,
                 self.flatButton), geom=self.invModels[track][item], text='50', text_scale=0.04, text_align=TextNode.ARight, geom_scale=0.7, geom_pos=(-0.01, -0.1, 0), text_fg=Vec4(1, 1, 1, 1), text_pos=(0.07, -0.04), textMayChange=1, relief=None, image_color=(0, 0.6, 1, 1), pos=(self.ButtonXOffset + item * self.ButtonXSpacing + adjustLeft, -0.1, 0), command=self.__handleSelection, extraArgs=[track, item])
                button.bind(DGG.ENTER, self.showDetail, extraArgs=[track, item])
                button.bind(DGG.EXIT, self.hideDetail)
                self.buttons[track].append(button)
        
        for x in xrange(len(self.trackRows)):
            self.hideTrack(x)
            self.trackRows[x].setBin('gui-popup', 50)
			
        self.detailFrame = DirectFrame(parent=self.invFrame, relief=None, pos=(1.05, 0, -0.08))
        self.circleFrame = DirectFrame(parent=self.detailFrame, relief=None, image=self.battleCircle, image_scale=0.25, pos=(0, 0, -0.25))
        self.detailNameLabel = DirectLabel(parent=self.circleFrame, text='', text_scale=TTLocalizer.INdetailNameLabel, text_fg=(0.05, 0.14, 0.4, 1), scale=0.045, pos=(0, 0, 0.1), text_font=getInterfaceFont(), text_align=TextNode.ACenter, relief=None, image=self.invModels[0][0])
        self.detailAmountLabel = DirectLabel(parent=self.circleFrame, text='', text_fg=(0.05, 0.14, 0.4, 1), scale=0.04, pos=(0, 0, -0.07), text_font=getInterfaceFont(), text_align=TextNode.ACenter, relief=None)
        self.detailDataLabel = DirectLabel(parent=self.circleFrame, text='', text_fg=(0.05, 0.14, 0.4, 1), scale=0.03, pos=(0, 0, -0.1), text_font=getInterfaceFont(), text_align=TextNode.ACenter, relief=None)
        self.detailCreditLabel = DirectLabel(parent=self.circleFrame, text=TTLocalizer.InventorySkillCreditNone, text_fg=(0.05, -0.14, -0.2, 1), scale=0.04, pos=(0, 0, 0.05), text_font=getInterfaceFont(), text_align=TextNode.ACenter, relief=None)
        self.detailCreditLabel.hide()
        self.totalLabel = DirectLabel(text='', parent=self.circleFrame, pos=(0, 0, 0.02), scale=0.05, text_fg=(0.05, 0.14, 0.4, 1), text_font=getInterfaceFont(), relief=None)
        self.dialog = None
        self.updateTotalPropsText()
        self.detailFrame.setBin('gui-popup', 50)
        
        for x in xrange(len(self.trackTabs)):
            self.trackTabs[x].hide()
        
        for x in xrange(len(self.trackTabs)):
            if self.toon.hasTrackAccess(x):
                self.trackTabs[x].show()
       
        self.doTab(self.activeTab)

        for x in xrange(8):
            self.accept('alt-%d' % (x+1), self.doTab, extraArgs=[
                x])
				
        self.accept('wheel_up', self.incrementTab, extraArgs=[1])
        self.accept('wheel_down', self.incrementTab, extraArgs=[-1])
		
    def incrementTab(self, index):
        trackAccess = base.localAvatar.getTrackAccess()
        list = []
        for x in xrange(len(trackAccess)):
            if trackAccess[x]:
                list.append(x)
        try:
            try:
                currIndex = list.index(self.activeTab)
            except:
                return
            newIndex = currIndex + index
            if newIndex >= 8:
                newIndex = list[0]
            self.activeTab = list[newIndex]
            self.doTab(self.activeTab)
        except:
            pass
		
    def doTab(self, index):
        trackAccess = base.localAvatar.getTrackAccess()
        if not trackAccess[index]:
           return
        
        self.activeTab = index
        for track in xrange(len(self.trackRows)):
            self.hideTrack(track)
            self.trackTabs[track]['geom_color']= Vec4(TrackColors[track][0] * 0.6, TrackColors[track][1] * 0.6, TrackColors[track][2] * 0.6, 1)
        
        self.trackTabs[index]['geom_color']= Vec4(TrackColors[index][0], TrackColors[index][1], TrackColors[index][2], 1)
        self.showTrack(index)
        for track in range(0, len(Tracks)):
            for level in xrange(len(Levels[track])):
                button = self.buttons[track][level]
                if self.itemIsUsable(track, level):
                    button.show()
                else:
                    button.hide()
        
        for x in xrange(7):
            self.accept('control-%d' % (x+1), self.__handleSelection, extraArgs=[
                self.activeTab, x, True])

    def __handleSelection(self, track, level, viaKeyboard = False):
        if self.activateMode == 'purchaseDelete' or self.activateMode == 'bookDelete' or self.activateMode == 'storePurchaseDelete':
            if self.numItem(track, level):
                self.useItem(track, level)
                self.updateGUI(track, level)
                messenger.send('inventory-deletion', [track, level])
                self.showDetail(track, level)
        elif self.activateMode == 'purchase' or self.activateMode == 'storePurchase':
            messenger.send('inventory-selection', [track, level, viaKeyboard])
            self.showDetail(track, level)
        elif self.gagTutMode:
            pass
        else:
            messenger.send('inventory-selection', [track, level])

    def __handleRun(self):
        messenger.send('inventory-run')

    def __handleFire(self):
        messenger.send('inventory-fire')

    def __handleSOS(self):
        messenger.send('inventory-sos')

    def __handlePass(self):
        messenger.send('inventory-pass')

    def __handleLevels(self):
        if settings.get('show-cog-levels', True):
            settings['show-cog-levels'] = False
            self.levelsButton['text'] = TTLocalizer.InventoryLevelsShow
        else:
            settings['show-cog-levels'] = True
            self.levelsButton['text'] = TTLocalizer.InventoryLevelsHide
        
        messenger.send('inventory-levels')

    def __handleBackToPlayground(self):
        messenger.send('inventory-back-to-playground')

    def __zeroInvConfirm(self):
        self.cleanupDialog()
        self.dialog = TTDialog.TTDialog(style=TTDialog.YesNo, text=TTLocalizer.InventoryDeleteConfirm, command=self.__zeroInvAndUpdate)
        self.dialog.show()
    
    def __zeroInvAndUpdate(self, value):
        self.cleanupDialog()
        
        if value:
            self.zeroInv()
            self.updateGUI()

    def showDetail(self, track, level, event = None):
        self.totalLabel.hide()
        self.detailNameLabel.show()
        self.detailNameLabel.configure(text=AvPropStrings[track][level], image_image=self.invModels[track][level])
        self.detailNameLabel.configure(image_scale=20, image_pos=(-0.2, 0, -2.2))
        self.detailAmountLabel.show()
        self.detailAmountLabel.configure(text=TTLocalizer.InventoryDetailAmount % {'numItems': self.numItem(track, level),
         'maxItems': self.getMax(track, level)})
        self.detailDataLabel.show()
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        if track == LURE_TRACK:
            damage = BattleGlobals.NumRoundsLured[level]
        else:
            damage = getAvPropDamage(track, level, self.toon.experience.getExp(track))
        damageBonusStr = ''
        damageBonus = 0
        if self.propAndOrganicBonusStack:
            if propBonus:
                damageBonus += getDamageBonus(damage, track)
                if track == SOUND_TRACK:
                    damageBonusStr = TTLocalizer.SoundExtraText
                elif track == HEAL_TRACK:
                    bonus = int(damage * 0.2)
                    damageBonusStr = TTLocalizer.InventoryDamageBonus % TTLocalizer.HealExtraText % {'heal': bonus}
                elif track == LURE_TRACK:
                    damageBonus = 1
            if organicBonus:
                damageBonus += getDamageBonus(damage, track)
                if track == SOUND_TRACK:
                    damageBonusStr = TTLocalizer.SoundExtraText
                elif track == HEAL_TRACK:
                    bonus = int(damage * 0.2)
                    damageBonusStr = TTLocalizer.InventoryDamageBonusString % TTLocalizer.HealExtraText % {'heal': bonus}
                elif track == LURE_TRACK:
                    damageBonus = 1
            if damageBonus:
                damageBonusStr = TTLocalizer.InventoryDamageBonus % damageBonus
        else:
            if propBonus or organicBonus:
                damageBonus += getDamageBonus(damage, track)
                if track == SOUND_TRACK:
                    damageBonusStr = TTLocalizer.SoundExtraText
                elif track == HEAL_TRACK:
                    bonus = int(damage * 0.2)
                    damageBonusStr = TTLocalizer.InventoryDamageBonusString % TTLocalizer.HealExtraText % {'heal': bonus}
                elif track == LURE_TRACK:
                    damageBonus = 1
            if damageBonus:
                damageBonusStr = TTLocalizer.InventoryDamageBonus % damageBonus
        accString = AvTrackAccStrings[track]
        if track == DROP_TRACK and organicBonus:
            accString += '(+10%)'
        if track == SQUIRT_TRACK or (track == TRAP_TRACK and organicBonus) or track == ZAP_TRACK:
            self.detailDataLabel.configure(text=TTLocalizer.InventoryDetailDataExtra % {'accuracy': accString,
             'damageString': self.getToonupDmgStr(track, level),
             'damage': damage,
             'bonus': damageBonusStr,
             'singleOrGroup': self.getSingleGroupStr(track, level),
             'extra': self.getExtraText(track, level, organicBonus)})
        else:
            self.detailDataLabel.configure(text=TTLocalizer.InventoryDetailData % {'accuracy': accString,
             'damageString': self.getToonupDmgStr(track, level),
             'damage': damage,
             'bonus': damageBonusStr,
             'singleOrGroup': self.getSingleGroupStr(track, level)})
        if self.itemIsCredit(track, level):
            mult = self.__battleCreditMultiplier
            if self.__respectInvasions:
                mult *= self.__invasionCreditMultiplier
            self.setDetailCredit(track, (level + 1) * mult)
        else:
            self.setDetailCredit(track, None)
        self.detailCreditLabel.show()

    def setDetailCredit(self, track, credit):
        if credit != None:
            if self.toon.earnedExperience:
                maxCredit = ExperienceCap - self.toon.earnedExperience[track]
                credit = min(credit, maxCredit)
            credit = int(credit * 10 + 0.5)
            if credit % 10 == 0:
                credit /= 10
            else:
                credit /= 10.0
        
        if self.detailCredit == credit:
            return
        
        if credit != None:
            self.detailCreditLabel['text'] = TTLocalizer.InventorySkillCredit % credit
            if self.detailCredit == None:
                self.detailCreditLabel['text_fg'] = (0.05, 0.14, 0.4, 1)
        else:
            self.detailCreditLabel['text'] = TTLocalizer.InventorySkillCreditNone
            self.detailCreditLabel['text_fg'] = (0.5, 0.0, 0.0, 1.0)
        
        self.detailCredit = credit

    def hideDetail(self, event = None):
        self.totalLabel.show()
        self.detailNameLabel.hide()
        self.detailAmountLabel.hide()
        self.detailDataLabel.hide()
        self.detailCreditLabel.hide()

    def noDetail(self):
        self.totalLabel.hide()
        self.detailNameLabel.hide()
        self.detailAmountLabel.hide()
        self.detailDataLabel.hide()
        self.detailCreditLabel.hide()

    def setActivateMode(self, mode, heal = 1, trap = 1, lure = 1, bldg = 0, creditLevel = None, tutorialFlag = 0, gagTutMode = 0):
        self.notify.debug('setActivateMode() mode:%s heal:%s trap:%s lure:%s bldg:%s' % (mode,
            heal,
            trap,
            lure,
            bldg))
        
        self.previousActivateMode = self.activateMode
        self.activateMode = mode
        self.deactivateButtons()
        self.heal = heal
        self.trap = trap
        self.lure = lure
        self.bldg = bldg
        self.battleCreditLevel = creditLevel
        self.tutorialFlag = tutorialFlag
        self.gagTutMode = gagTutMode
        self.__activateButtons()
        self.enableUberGags()

    def setActivateModeBroke(self):
        if self.activateMode == 'storePurchase':
            self.setActivateMode('storePurchaseBroke')
        elif self.activateMode == 'purchase':
            self.setActivateMode('purchaseBroke', gagTutMode=self.gagTutMode)
        else:
            self.notify.error('Unexpected mode in setActivateModeBroke(): %s' % self.activateMode)
        
        self.enableUberGags()

    def deactivateButtons(self):
        self.cleanupDialog()
        if self.previousActivateMode == 'book':
            self.bookDeactivateButtons()
        elif self.previousActivateMode == 'bookDelete':
            self.bookDeleteDeactivateButtons()
        elif self.previousActivateMode == 'purchaseDelete':
            self.purchaseDeleteDeactivateButtons()
        elif self.previousActivateMode == 'purchase':
            self.purchaseDeactivateButtons()
        elif self.previousActivateMode == 'purchaseBroke':
            self.purchaseBrokeDeactivateButtons()
        elif self.previousActivateMode == 'gagTutDisabled':
            self.gagTutDisabledDeactivateButtons()
        elif self.previousActivateMode == 'battle':
            self.battleDeactivateButtons()
        elif self.previousActivateMode == 'storePurchaseDelete':
            self.storePurchaseDeleteDeactivateButtons()
        elif self.previousActivateMode == 'storePurchase':
            self.storePurchaseDeactivateButtons()
        elif self.previousActivateMode == 'storePurchaseBroke':
            self.storePurchaseBrokeDeactivateButtons()
        elif self.previousActivateMode == 'plantTree':
            self.plantTreeDeactivateButtons()
        else:
            self.notify.error('No such mode as %s' % self.previousActivateMode)

    def __activateButtons(self):
        self.cleanupDialog()
        if hasattr(self, 'activateMode'):
            if self.activateMode == 'book':
                self.bookActivateButtons()
            elif self.activateMode == 'bookDelete':
                self.bookDeleteActivateButtons()
            elif self.activateMode == 'purchaseDelete':
                self.purchaseDeleteActivateButtons()
            elif self.activateMode == 'purchase':
                self.purchaseActivateButtons()
            elif self.activateMode == 'purchaseBroke':
                self.purchaseBrokeActivateButtons()
            elif self.activateMode == 'gagTutDisabled':
                self.gagTutDisabledActivateButtons()
            elif self.activateMode == 'battle':
                self.battleActivateButtons()
            elif self.activateMode == 'storePurchaseDelete':
                self.storePurchaseDeleteActivateButtons()
            elif self.activateMode == 'storePurchase':
                self.storePurchaseActivateButtons()
            elif self.activateMode == 'storePurchaseBroke':
                self.storePurchaseBrokeActivateButtons()
            elif self.activateMode == 'plantTree':
                self.plantTreeActivateButtons()
            else:
                self.notify.error('No such mode as %s' % self.activateMode)
            
            self.doTab(self.activeTab)

    def bookActivateButtons(self):
        self.setPos(0, 0, 0.52)
        self.setScale(1.0)
        self.detailFrame.setPos(0.1, 0, -0.855)
        self.detailFrame.setScale(0.75)
        self.deleteEnterButton.hide()
        self.deleteAllButton.hide()
        self.deleteExitButton.hide()
        self.invFrame.reparentTo(self)
        self.invFrame.setPos(0, 0, 0)
        self.invFrame.setScale(1)
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        self.makeBookUnpressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def bookDeactivateButtons(self):
        self.deleteEnterButton['command'] = None

    def bookDeleteActivateButtons(self):
        messenger.send('enterBookDelete')
        self.setPos(-0.2, 0, 0.4)
        self.setScale(0.8)
        self.deleteEnterButton.hide()
        self.deleteEnterButton.setPos(1.00, 0, -0.639)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.show()
        self.deleteExitButton.setPos(1.00, 0, -0.639)
        self.deleteExitButton.setScale(0.75)
        self.deleteHelpText.show()
        self.invFrame.reparentTo(self)
        self.invFrame.setPos(0, 0, 0)
        self.invFrame.setScale(1)
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0:
                            self.makeUnpressable(button, track, level)
                        else:
                            self.makeDeletePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def bookDeleteDeactivateButtons(self):
        messenger.send('exitBookDelete')
        self.deleteHelpText.hide()
        self.deleteDeactivateButtons()

    def purchaseDeleteActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.purchaseFrame == None:
            self.loadPurchaseFrame()
        self.purchaseFrame.show()
        self.invFrame.reparentTo(self.purchaseFrame)
        self.invFrame.setPos(0, 0, 0.52)
        self.invFrame.setScale(0.81)
        self.detailFrame.setPos(-1.17, 0, -1)
        self.detailFrame.setScale(1.25)
        self.deleteEnterButton.hide()
        self.deleteEnterButton.setPos(-0.55, 0, -1)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.show()
        self.deleteExitButton.setPos(-0.55, 0, -1)
        self.deleteExitButton.setScale(0.75)
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0 or level >= UBER_GAG_LEVEL_INDEX:
                            self.makeUnpressable(button, track, level)
                        else:
                            self.makeDeletePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def purchaseDeleteDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.purchaseFrame.hide()
        self.deleteDeactivateButtons()
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0 or level >= UBER_GAG_LEVEL_INDEX:
                            self.makeUnpressable(button, track, level)
                        else:
                            self.makeDeletePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def storePurchaseDeleteActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if not self.storePurchaseFrame:
            self.loadStorePurchaseFrame()
        
        self.storePurchaseFrame.show()
        self.invFrame.reparentTo(self.storePurchaseFrame)
        self.invFrame.setPos(0, 0, 0.505)
        self.invFrame.setScale(0.81)
        self.detailFrame.setPos(-1.175, 0, -1)
        self.detailFrame.setScale(1.25)
        self.deleteEnterButton.hide()
        self.deleteEnterButton.setPos(-0.55, 0, -1)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.show()
        self.deleteExitButton.setPos(-0.55, 0, -1)
        self.deleteExitButton.setScale(0.75)
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0 or level >= UBER_GAG_LEVEL_INDEX:
                            self.makeUnpressable(button, track, level)
                        else:
                            self.makeDeletePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def storePurchaseDeleteDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.storePurchaseFrame.hide()
        self.deleteDeactivateButtons()

    def storePurchaseBrokeActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if not self.storePurchaseFrame:
            self.loadStorePurchaseFrame()
        
        self.storePurchaseFrame.show()
        self.invFrame.reparentTo(self.storePurchaseFrame)
        self.invFrame.setPos(0, 0, 0.505)
        self.invFrame.setScale(0.81)
        self.detailFrame.setPos(-1.175, 0, -1)
        self.detailFrame.setScale(1.25)
        self.deleteAllButton.show()
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.55, 0, -1)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.55, 0, -1)
        self.deleteExitButton.setScale(0.75)
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        self.makeUnpressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def storePurchaseBrokeDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.storePurchaseFrame.hide()

    def deleteActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0, 0, 0)
        self.setScale(1)
        self.deleteEnterButton.hide()
        self.deleteExitButton.show()
        self.deleteExitButton['command'] = self.setActivateMode
        self.deleteExitButton['extraArgs'] = [self.previousActivateMode]
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if self.numItem(track, level) <= 0:
                            self.makeUnpressable(button, track, level)
                        else:
                            self.makePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def deleteDeactivateButtons(self):
        self.deleteExitButton['command'] = None

    def purchaseActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if not self.purchaseFrame:
            self.loadPurchaseFrame()
        
        self.purchaseFrame.show()
        self.invFrame.reparentTo(self.purchaseFrame)
        self.invFrame.setPos(0, 0, 0.52)
        self.invFrame.setScale(0.81)
        self.detailFrame.setPos(-1.17, 0, -1)
        self.detailFrame.setScale(1.25)
        totalProps = self.totalProps
        maxProps = self.toon.getMaxCarry()
        self.deleteAllButton.show()
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.55, 0, -1)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.55, 0, -1)
        self.deleteExitButton.setScale(0.75)
        if self.gagTutMode:
            self.deleteAllButton.hide()
            self.deleteEnterButton.hide()
        
        self.deleteEnterButton['command'] = self.setActivateMode
        self.deleteEnterButton['extraArgs'] = ['purchaseDelete']
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        unpaid = not base.cr.isPaid()
                        if self.numItem(track, level) >= self.getMax(track, level) or totalProps == maxProps or unpaid and gagIsPaidOnly(track, level) or level > LAST_REGULAR_GAG_LEVEL:
                            if gagIsPaidOnly(track, level):
                                self.makeDisabledPressable(button, track, level)
                            elif unpaid and gagIsVelvetRoped(track, level):
                                self.makeDisabledPressable(button, track, level)
                            else:
                                self.makeUnpressable(button, track, level)
                        elif unpaid and gagIsVelvetRoped(track, level):
                            self.makeDisabledPressable(button, track, level)
                        else:
                            self.makePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def purchaseDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.purchaseFrame.hide()

    def storePurchaseActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if not self.storePurchaseFrame:
            self.loadStorePurchaseFrame()
        
        self.storePurchaseFrame.show()
        self.invFrame.reparentTo(self.storePurchaseFrame)
        self.invFrame.setPos(0, 0, 0.505)
        self.invFrame.setScale(0.81)
        self.detailFrame.setPos(-1.175, 0, -1)
        self.detailFrame.setScale(1.25)
        totalProps = self.totalProps
        maxProps = self.toon.getMaxCarry()
        self.deleteAllButton.show()
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.55, 0, -1)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.55, 0, -1)
        self.deleteExitButton.setScale(0.75)
        self.deleteEnterButton['command'] = self.setActivateMode
        self.deleteEnterButton['extraArgs'] = ['storePurchaseDelete']
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        unpaid = not base.cr.isPaid()
                        if self.numItem(track, level) >= self.getMax(track, level) or totalProps == maxProps or unpaid and gagIsPaidOnly(track, level) or level > LAST_REGULAR_GAG_LEVEL:
                            if gagIsPaidOnly(track, level):
                                self.makeDisabledPressable(button, track, level)
                            elif unpaid and gagIsVelvetRoped(track, level):
                                self.makeDisabledPressable(button, track, level)
                            else:
                                self.makeUnpressable(button, track, level)
                        elif unpaid and gagIsVelvetRoped(track, level):
                            self.makeDisabledPressable(button, track, level)
                        else:
                            self.makePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def storePurchaseDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.storePurchaseFrame.hide()

    def purchaseBrokeActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if not self.purchaseFrame:
            self.loadPurchaseFrame()
        
        self.purchaseFrame.show()
        self.invFrame.reparentTo(self.purchaseFrame)
        self.invFrame.setPos(0, 0, 0.52)
        self.invFrame.setScale(0.81)
        self.detailFrame.setPos(-1.17, 0, -1)
        self.detailFrame.setScale(1.25)
        self.deleteAllButton.show()
        self.deleteEnterButton.show()
        self.deleteEnterButton.setPos(-0.55, 0, -1)
        self.deleteEnterButton.setScale(0.75)
        self.deleteExitButton.hide()
        self.deleteExitButton.setPos(-0.55, 0, -1)
        self.deleteExitButton.setScale(0.75)
        if self.gagTutMode:
            self.deleteEnterButton.hide()
        
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        button.show()
                        if not self.gagTutMode:
                            self.makeUnpressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def purchaseBrokeDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.purchaseFrame.hide()

    def gagTutDisabledActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0.2, 0, -0.04)
        self.setScale(1)
        if self.purchaseFrame == None:
            self.loadPurchaseFrame()
        self.purchaseFrame.show()
        self.invFrame.reparentTo(self.purchaseFrame)
        self.invFrame.setPos(0, 0, 0.52)
        self.invFrame.setScale(0.81)
        self.detailFrame.setPos(-1.17, 0, -1)
        self.detailFrame.setScale(1.25)
        self.deleteExitButton.hide()
        self.deleteEnterButton.hide()
        self.deleteAllButton.hide()

    def gagTutDisabledDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.purchaseFrame.hide()

    def battleActivateButtons(self):
        self.stopAndClearPropBonusIval()
        self.reparentTo(aspect2d)
        self.setPos(0, 0, 0.1)
        self.setScale(1)
        if not self.battleFrame:
            self.loadBattleFrame()
        
        self.battleFrame.show()
        self.battleFrame.setScale(0.9)
        self.invFrame.reparentTo(self.battleFrame)
        self.invFrame.setPos(0, 0, -0.25)
        self.invFrame.setScale(1)
        self.detailFrame.setPos(1.125, 0, -0.15)
        self.detailFrame.setScale(1)
        self.deleteAllButton.hide()
        self.deleteEnterButton.hide()
        self.deleteExitButton.hide()
        if self.bldg == 1:
            self.runButton.hide()
            self.sosButton.show()
            self.passButton.show()
            self.levelsButton.show()
        elif self.tutorialFlag == 1:
            self.runButton.hide()
            self.sosButton.hide()
            self.passButton.hide()
            self.fireButton.hide()
            self.levelsButton.hide()
        else:
            self.runButton.show()
            self.sosButton.show()
            self.passButton.show()
            self.fireButton.show()
            self.levelsButton.show()

            if localAvatar.getPinkSlips():
                self.fireButton['state'] = DGG.NORMAL
                self.fireButton['image_color'] = Vec4(0, 0.6, 1, 1)
            else:
                self.fireButton['state'] = DGG.DISABLED
                self.fireButton['image_color'] = Vec4(0.4, 0.4, 0.4, 1)
        
        if settings.get('show-cog-levels', True):
            self.levelsButton['text'] = TTLocalizer.InventoryLevelsHide
        else:
            self.levelsButton['text'] = TTLocalizer.InventoryLevelsShow
        
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level):
                        unpaid = not base.cr.isPaid()
                        button.show()
                        if self.numItem(track, level) <= 0 or track == HEAL_TRACK and not self.heal or track == TRAP_TRACK and not self.trap or track == LURE_TRACK and not self.lure:
                            self.makeUnpressable(button, track, level)
                        elif unpaid and gagIsVelvetRoped(track, level):
                            self.makeDisabledPressable(button, track, level)
                        elif self.itemIsCredit(track, level):
                            self.makePressable(button, track, level)
                        else:
                            self.makeNoncreditPressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

        self.propBonusIval.loop()

    def battleDeactivateButtons(self):
        self.invFrame.reparentTo(self)
        self.levelsButton.hide()
        self.battleFrame.hide()
        self.stopAndClearPropBonusIval()

    def plantTreeActivateButtons(self):
        self.reparentTo(aspect2d)
        self.setPos(0, 0, 0.1)
        self.setScale(1)
        if not self.battleFrame:
            self.loadBattleFrame()
        
        self.battleFrame.show()
        self.battleFrame.setScale(0.9)
        self.invFrame.reparentTo(self.battleFrame)
        self.invFrame.setPos(-0.25, 0, 0.35)
        self.invFrame.setScale(1)
        self.detailFrame.setPos(1.125, 0, -0.08)
        self.detailFrame.setScale(1)
        self.deleteAllButton.hide()
        self.deleteEnterButton.hide()
        self.deleteExitButton.hide()
        self.runButton.hide()
        self.sosButton.hide()
        self.levelsButton.hide()
        self.passButton['text'] = TTLocalizer.lCancel
        self.passButton.show()
        for track in xrange(len(Tracks)):
            if self.toon.hasTrackAccess(track):
                self.showTrack(track)
                for level in xrange(len(Levels[track])):
                    button = self.buttons[track][level]
                    if self.itemIsUsable(track, level) and (level == 0 or self.toon.doIHaveRequiredTrees(track, level)):
                        button.show()
                        self.makeUnpressable(button, track, level)
                        if self.numItem(track, level):
                            if not self.toon.isTreePlanted(track, level):
                                self.makePressable(button, track, level)
                    else:
                        button.hide()

            else:
                self.hideTrack(track)

    def plantTreeDeactivateButtons(self):
        self.passButton['text'] = TTLocalizer.InventoryPass
        self.invFrame.reparentTo(self)
        self.levelsButton.hide()
        self.battleFrame.hide()

    def itemIsUsable(self, track, level):
        if self.gagTutMode:
            trackAccess = self.toon.getTrackAccess()
            return trackAccess[track] >= level + 1
        
        curSkill = self.toon.experience.getExp(track)
        if curSkill < Levels[track][level]:
            return 0
        
        return 1

    def itemIsCredit(self, track, level):
        if self.toon.earnedExperience:
            if self.toon.earnedExperience[track] >= ExperienceCap:
                return 0
        if self.battleCreditLevel == None:
            return 1
        
        return level < self.battleCreditLevel

    def getMax(self, track, level):
        if self.gagTutMode and (track not in (4, 5) or level):
            return 1
        
        return InventoryBase.InventoryBase.getMax(self, track, level)

    def getCurAndNextExpValues(self, track):
        curSkill = self.toon.experience.getExp(track)
        retVal = MaxSkill
        for amount in Levels[track]:
            if curSkill < amount:
                retVal = amount
                return (curSkill, retVal)

        return (curSkill, retVal)

    def makePressable(self, button, track, level):
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        bonus = organicBonus or propBonus
        if bonus:
            shadowColor = self.ShadowBuffedColor
        else:
            shadowColor = self.ShadowColor
        button.configure(image0_image=self.upButton, image2_image=self.rolloverButton, text_shadow=shadowColor, geom_color=self.PressableGeomColor, 
            commandButtons=(DGG.LMB,))
        
        if self._interactivePropTrackBonus == track:
            button.configure(image_color=self.PropBonusPressableImageColor)
            self.addToPropBonusIval(button)
        else:
            button.configure(image_color=self.PressableImageColor)

    def makeDisabledPressable(self, button, track, level):
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        bonus = organicBonus or propBonus
        if bonus:
            shadowColor = self.UnpressableShadowBuffedColor
        else:
            shadowColor = self.ShadowColor
        
        button.configure(text_shadow=shadowColor, geom_color=self.UnpressableGeomColor, image_image=self.flatButton, commandButtons=(DGG.LMB,))
        button.configure(image_color=self.UnpressableImageColor)

    def makeNoncreditPressable(self, button, track, level):
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        bonus = organicBonus or propBonus
        if bonus:
            shadowColor = self.ShadowBuffedColor
        else:
            shadowColor = self.ShadowColor
        button.configure(image0_image=self.upButton, image2_image=self.rolloverButton, text_shadow=shadowColor, geom_color=self.PressableGeomColor, 
            commandButtons=(DGG.LMB,))
        
        if self._interactivePropTrackBonus == track:
            button.configure(image_color=self.PropBonusNoncreditPressableImageColor)
            self.addToPropBonusIval(button)
        else:
            button.configure(image_color=self.NoncreditPressableImageColor)

    def makeDeletePressable(self, button, track, level):
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        bonus = organicBonus or propBonus
        if bonus:
            shadowColor = self.ShadowBuffedColor
        else:
            shadowColor = self.ShadowColor
        
        button.configure(image0_image=self.upButton, image2_image=self.rolloverButton, text_shadow=shadowColor, geom_color=self.PressableGeomColor, 
            commandButtons=(DGG.LMB,))
        
        button.configure(image_color=self.DeletePressableImageColor)

    def makeUnpressable(self, button, track, level):
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        bonus = organicBonus or propBonus
        if bonus:
            shadowColor = self.UnpressableShadowBuffedColor
        else:
            shadowColor = self.ShadowColor
        
        button.configure(text_shadow=shadowColor, geom_color=self.UnpressableGeomColor, image_image=self.flatButton, commandButtons=())
        button.configure(image_color=self.UnpressableImageColor)

    def makeBookUnpressable(self, button, track, level):
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        bonus = organicBonus or propBonus
        if bonus:
            shadowColor = self.ShadowBuffedColor
        else:
            shadowColor = self.ShadowColor
        
        button.configure(text_shadow=shadowColor, geom_color=self.BookUnpressableGeomColor, image_image=self.flatButton, commandButtons=())
        button.configure(image0_color=self.BookUnpressableImage0Color, image2_color=self.BookUnpressableImage2Color)

    def hideTrack(self, trackIndex):
        self.trackNameLabels[trackIndex].hide()
        self.trackBars[trackIndex].hide()
        self.trackRows[trackIndex].hide()
        for levelIndex in xrange(0, len(Levels[trackIndex])):
            self.buttons[trackIndex][levelIndex].hide()

    def showTrack(self, trackIndex):
        self.trackNameLabels[trackIndex].show()
        self.trackBars[trackIndex].show()
        self.trackRows[trackIndex].show()
        for levelIndex in xrange(0, len(Levels[trackIndex])):
            self.buttons[trackIndex][levelIndex].show()

        (curExp, nextExp) = self.getCurAndNextExpValues(trackIndex)
        if curExp >= regMaxSkill:
            self.trackBars[trackIndex]['range'] = UberSkill
            self.trackBars[trackIndex]['text'] = TTLocalizer.InventoryUberTrackExp % {'nextExp': MaxSkill - curExp}
        else:
            self.trackBars[trackIndex]['range'] = nextExp
            self.trackBars[trackIndex]['text'] = TTLocalizer.InventoryTrackExp % {'curExp': curExp,
                'nextExp': nextExp}

    def updateInvString(self, invString):
        InventoryBase.InventoryBase.updateInvString(self, invString)
        self.updateGUI()
		
    def getInvString(self):
        InventoryBase.InventoryBase.getInvString(self)

    def updateButton(self, track, level):
        button = self.buttons[track][level]
        button['text'] = str(self.numItem(track, level))
        organicBonus = self.toon.checkGagBonus(track, level)
        propBonus = self.checkPropBonus(track)
        bonus = organicBonus or propBonus
        if bonus:
            textScale = 0.05
        else:
            textScale = 0.04
        
        button.configure(text_scale=textScale)

    def buttonBoing(self, track, level):
        button = self.buttons[track][level]
        oldScale = button.getScale()
        s = Sequence(button.scaleInterval(0.1, oldScale * 1.333, blendType='easeOut'), button.scaleInterval(0.1, oldScale, blendType='easeIn'), 
            name='inventoryButtonBoing-' + str(self.this))
        
        s.start()

    def updateGUI(self, track = None, level = None):
        self.updateTotalPropsText()
        if track == None and level == None:
            for track in xrange(len(Tracks)):
                curExp, nextExp = self.getCurAndNextExpValues(track)
                if curExp >= UnpaidMaxSkills[track] and self.toon.getGameAccess() != OTPGlobals.AccessFull:
                    self.trackBars[track]['range'] = nextExp
                    self.trackBars[track]['text'] = TTLocalizer.InventoryGuestExp
                elif curExp >= regMaxSkill:
                    self.trackBars[track]['text'] = TTLocalizer.InventoryUberTrackExp % {'nextExp': MaxSkill - curExp}
                    self.trackBars[track]['value'] = curExp - regMaxSkill
                else:
                    self.trackBars[track]['text'] = TTLocalizer.InventoryTrackExp % {'curExp': curExp,
                     'nextExp': nextExp}
                    self.trackBars[track]['value'] = curExp
                
                for level in xrange(0, len(Levels[track])):
                    self.updateButton(track, level)
                
                for x in xrange(len(Tracks)):
                    if self.toon.hasTrackAccess(x):
                        self.trackTabs[x].show()
                    else:
                        self.trackTabs[x].hide()

        elif track != None and level != None:
            self.updateButton(track, level)
        else:
            self.notify.error('Invalid use of updateGUI')
        
        self.doTab(self.activeTab)
        self.__activateButtons()

    def getSingleGroupStr(self, track, level):
        if track == HEAL_TRACK:
            if isGroup(track, level):
                return TTLocalizer.InventoryAffectsAllToons
            else:
                return TTLocalizer.InventoryAffectsOneToon
        elif isGroup(track, level):
            return TTLocalizer.InventoryAffectsAllCogs
        else:
            return TTLocalizer.InventoryAffectsOneCog
			
    def getExtraText(self, track, level, organicBonus = False):
        if track == SQUIRT_TRACK:
           if organicBonus:
               bonusRounds = 1
           else:
               bonusRounds = 0
           if bonusRounds:
               text = TTLocalizer.InventorySquirtRoundsString % str(BattleGlobals.NumRoundsWet[level]) + ' (+1)'
           else:
               text = TTLocalizer.InventorySquirtRoundsString % str(BattleGlobals.NumRoundsWet[level])
           return text
        elif track == TRAP_TRACK:
            return TTLocalizer.TrapExtraText
        elif track == ZAP_TRACK:
            bonus = 0
            if organicBonus:
                bonus = int(InstaKillChance[level] * 0.5)
            if bonus:
                text = TTLocalizer.ZapExtraText % str(InstaKillChance[level]) + ' (+%d)' % bonus
            else:
                text = TTLocalizer.ZapExtraText % str(InstaKillChance[level])
            return text

    def getToonupDmgStr(self, track, level):
        if track == HEAL_TRACK:
            return TTLocalizer.InventoryHealString
        elif track == LURE_TRACK:
            return TTLocalizer.InventoryLureString
        else:
            return TTLocalizer.InventoryDamageString

    def deleteItem(self, track, level):
        if self.numItem(track, level):
            self.useItem(track, level)
            self.updateGUI(track, level)

    def loadBattleFrame(self):
        battleModels = loader.loadModel('phase_3.5/models/gui/battle_gui_new')
        self.levelsButton = DirectButton(self, relief=None, pos=(0.675, 0, -0.5), text='', text_scale=TTLocalizer.INlevelsButton, text_fg=Vec4(1, 1, 1, 1), textMayChange=1, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=(2.5, 1.05, 1), image_color=(1, 0.6, 0, 1), command=self.__handleLevels)
        self.battleFrame = DirectFrame(relief=None, parent=self)
        self.runButton = DirectButton(parent=self.battleFrame, relief=None, pos=(1.4, 0, -0.5), text=TTLocalizer.InventoryRun, text_scale=TTLocalizer.INrunButton, text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), textMayChange=0, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=(2, 1.05, 1), image_color=(0, 0.6, 1, 1), command=self.__handleRun)
        self.sosButton = DirectButton(parent=self.battleFrame, relief=None, pos=(1.45, 0, -0.7), text=TTLocalizer.InventorySOS, text_scale=0.05, text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), textMayChange=0, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=(2, 1.05, 1), image_color=(0, 0.6, 1, 1), command=self.__handleSOS)
        self.passButton = DirectButton(parent=self.battleFrame, relief=None, pos=(1.45, 0, -0.6), text=TTLocalizer.InventoryPass, text_scale=TTLocalizer.INpassButton, text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), textMayChange=1, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=(2, 1.05, 1), image_color=(0, 0.6, 1, 1), command=self.__handlePass)
        self.fireButton = DirectButton(parent=self.battleFrame, relief=None, pos=(1.4, 0, -0.8), text=TTLocalizer.InventoryFire, text_scale=TTLocalizer.INfireButton, text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), textMayChange=0, image=(self.upButton, self.downButton, self.rolloverButton), image_scale=(2, 1.05, 1), image_color=(0, 0.6, 1, 1), command=self.__handleFire)
        self.tutText = DirectFrame(parent=self.battleFrame, relief=None, pos=(-1, 0, -0.1133), scale=0.143, image=DGG.getDefaultDialogGeom(), image_scale=5.125, image_pos=(0, 0, -0.65), image_color=ToontownGlobals.GlobalDialogColor, text_scale=TTLocalizer.INclickToAttack, text=TTLocalizer.InventoryClickToAttack, textMayChange=0)
        self.tutText.hide()
        self.tutArrows = BlinkingArrows.BlinkingArrows(parent=self.battleFrame)
        battleModels.removeNode()
        self.levelsButton.hide()
        self.battleFrame.hide()

    def loadPurchaseFrame(self):
        self.purchaseFrame = DirectFrame(relief=None, parent=self)
        self.purchaseFrame.setX(-.06)
        self.purchaseFrame.hide()

    def loadStorePurchaseFrame(self):
        self.storePurchaseFrame = DirectFrame(relief=None, parent=self)
        self.storePurchaseFrame.hide()

    def buttonLookup(self, track, level):
        return self.invModels[track][level]

    def enterTrackFrame(self, track, guiItem):
        messenger.send('enterTrackFrame', [track])

    def exitTrackFrame(self, track, guiItem):
        messenger.send('exitTrackFrame', [track])

    def checkPropBonus(self, track):
        return True if track == self._interactivePropTrackBonus else False

    def stopAndClearPropBonusIval(self):
        if self.propBonusIval and self.propBonusIval.isPlaying():
            self.propBonusIval.finish()
        self.propBonusIval = Parallel(name='dummyPropBonusIval')

    def addToPropBonusIval(self, button):
        flashObject = button
        try:
            flashObject = button.component('image0')
        except:
            pass

        goDark = LerpColorScaleInterval(flashObject, 0.5, Point4(0.1, 0.1, 0.1, 1.0), Point4(1, 1, 1, 1), blendType='easeIn')
        goBright = LerpColorScaleInterval(flashObject, 0.5, Point4(1, 1, 1, 1), Point4(0.1, 0.1, 0.1, 1.0), blendType='easeOut')
        newSeq = Sequence(goDark, goBright, Wait(0.2))
        self.propBonusIval.append(newSeq)
