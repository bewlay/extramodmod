# Events Enhanced EventManager
# by lfgr
# includes:
# 	World Unit Popup (WU POPUP) by ostar
# 	Great Person Mod (GREAT PERSON MOD START) by xienwold, ostar

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import CustomFunctions
import BugCore
import BugData


# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
game = gc.getGame()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

options = BugCore.game.EventsEnhanced


# Constants
EE_MOD_ID = "EventsEnhanced"

ORPHANED_GOBLIN_ACTIVE_PERCENT = 25 # Percent of games the Orphaned Goblin event is active
ORPHANED_GOBLIN_TRIGGER_PERMILLE = 20 # Permille of goblin combats triggering the orphaned goblin event (if active)


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


def _canTriggerOrphanedGoblin() :
	table = BugData.getTable( EE_MOD_ID )
	if "orphaned_goblin_can_trigger" not in table :
		# Only exists in 20% of games
		table["orphaned_goblin_can_trigger"] = CyGame().getSorenRandNum( 100, "OG active" ) < ORPHANED_GOBLIN_ACTIVE_PERCENT

	return table["orphaned_goblin_can_trigger"] and "orphaned_goblin_triggered" not in table

def _setOrphanedGoblinTriggered() :
	table = BugData.getTable( EE_MOD_ID )
	table["orphaned_goblin_triggered"] = True


def onCombatResult( argsList ) :
	'Combat Result'
	pWinner, pLoser = argsList

# more events mod -- modified by lfgr 06/2021
	if _canTriggerOrphanedGoblin() :
		if pLoser.getUnitType() in ( gc.getInfoTypeForString('UNIT_GOBLIN'), gc.getInfoTypeForString('UNIT_GOBLIN_SCORPION_CLAN') ) :
			if gc.getPlayer( pLoser.getOwner() ).isBarbarian() :
				if not pWinner.isAnimal() and pWinner.getRace() == UnitTypes.NO_UNIT :
					if CyGame().getSorenRandNum( 100, "OG triggers" ) < ORPHANED_GOBLIN_TRIGGER_PERMILLE :
						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_ORPHANED_GOBLIN')
						gc.getPlayer( pWinner.getOwner() ).initTriggeredData(iEvent, True, -1,
								pWinner.getX(), pWinner.getY(), pWinner.getOwner(), -1, -1, -1, pWinner.getID(), -1)
						_setOrphanedGoblinTriggered()