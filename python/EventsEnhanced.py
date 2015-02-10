# Events Enhanced EventManager
# by lfgr
# includes:
# 	World Unit Popup (WU POPUP) by ostar
# 	Great Person Mod (GREAT PERSON MOD START) by xienwold, ostar

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup as PyPopup
import CustomFunctions
import sys
import BugCore

# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
game = gc.getGame()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

options = BugCore.game.EventsEnhanced

def onUnitBuilt(argsList):
	'Unit Completed'
	city = argsList[0]
	unit = argsList[1]
	pPlayer = gc.getPlayer( city.getOwner() )
	
#WU POPUP
	# LFGR_TODO: use unitCreated to extend on Gealan, Mary Morbus, but exclude first-turn units (probably annoying) and armaggeddon units (already have an event popup)
	
	# Disable if AIAutoplay is activated. For some reason it's 1 sometimes when not activated.
	if( game.getAIAutoPlay( game.getActivePlayer() ) <= 1 ) :
		if isWorldUnitClass(unit.getUnitClassType()) == True:
			if( ( options.isWUPopupHuman() and pPlayer.isHuman() ) or ( options.isWUPopupAI() and not pPlayer.isHuman() ) ) :
				if pPlayer.isBarbarian() == False:
					activePlayer = gc.getPlayer(game.getActivePlayer())

					sPlayerName = pPlayer.getName()
					sUnitName = PyInfo.UnitInfo(unit.getUnitType()).getDescription()

					if gc.getTeam(unit.getTeam()).isHasMet(activePlayer.getTeam()):
						sPopupText = CyTranslator().getText('TXT_KEY_MISC_SOMEONE_CREATED_UNIT',(sPlayerName, sUnitName))
					else:
						sPopupText = CyTranslator().getText('TXT_KEY_MISC_UNKNOWN_CREATED_UNIT',(sUnitName, ))
					cf.addPopup(sPopupText, str(gc.getUnitInfo(unit.getUnitType()).getImage()))
#WU POPUP END

def onUnitCreated(argsList):
	'Unit Completed'
	pUnit = argsList[0]
	pPlayer = gc.getPlayer(pUnit.getOwner())
	
#GREAT PERSON MOD START
	# Disable if AIAutoplay is activated. For some reason it's 1 sometimes when not activated.
	if( game.getAIAutoPlay( game.getActivePlayer() ) <= 1 ) :
		if( ( options.isGPPopupHuman() and pPlayer.isHuman() ) or ( options.isGPPopupAI() and not pPlayer.isHuman() ) ) :
			sUnitName = pUnit.getNameNoDesc()
			# TODO: does not trigger when nameless gp is born due to lack of new names
			if( sUnitName != "" ) :
				Message = "TXT_KEY_QUOTE_%s" %(sUnitName,)
				cf.addPopup(CyTranslator().getText(str(Message),()), 'Art/GreatPeople/Simple/'+str(gc.getUnitInfo(pUnit.getUnitType()).getType())+'/'+str(sUnitName)+'.dds')
			return
#GREAT PERSON MOD END
