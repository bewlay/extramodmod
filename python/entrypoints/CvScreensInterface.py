## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
import CvMainInterface
import CvTechChooser
import CvForeignAdvisor
import CvExoticForeignAdvisor
import CvReligionScreen
import CvCorporationScreen
import CvCivicsScreen
import CvVictoryScreen
import CvEspionageAdvisor

import CvOptionsScreen
import CvReplayScreen
import CvHallOfFameScreen
import CvDanQuayle
import CvUnVictoryScreen

import CvDawnOfMan
import CvTechSplashScreen
import CvTopCivs
import CvInfoScreen

import CvIntroMovieScreen
import CvVictoryMovieScreen
import CvWonderMovieScreen
import CvEraMovieScreen
import CvSpaceShipScreen

#import CvPediaMain
#import CvPediaHistory
# BUG - Sevopedia - start
import SevoScreenEnums
# BUG - Sevopedia - end

import CvWorldBuilderScreen

import CvDebugTools
import CvDebugInfoScreen
#import CvDiplomacy

import CvUtil
import CvEventInterface
import CvPopupInterface
import CvScreenUtilsInterface
import ScreenInput as PyScreenInput
from CvScreenEnums import *
from CvPythonExtensions import *

#FfH: Added by Talchas 05/19/2007
import CvTrophyHall
#FfH: End Add
# BUG - Options - end
import BugCore
AdvisorOpt = BugCore.game.Advisors
CustDomAdvOpt = BugCore.game.CustDomAdv
TechWindowOpt = BugCore.game.TechWindow
# BUG - Options - end

g_bIsScreenActive = -1

## World Builder ##
import WBBuildingScreen
import WBTechScreen
import WBPromotionScreen
import WBCorporationScreen
import WBBonusScreen
import WBProjectScreen
import WBSpecialistScreen
import WBDiplomacyScreen
## Platy Screens ##

def toggleSetNoScreens():
	global g_bIsScreenActive
	print "SCREEN OFF"
	g_bIsScreenActive = -1

def toggleSetScreenOn(argsList):
	global g_bIsScreenActive
	print "%s SCREEN TURNED ON" %(argsList[0],)
	g_bIsScreenActive = argsList[0]

#diplomacyScreen = CvDiplomacy.CvDiplomacy()

mainInterface = CvMainInterface.CvMainInterface()
def showMainInterface():
	mainInterface.interfaceScreen()

def reinitMainInterface():
	mainInterface.initState()

def numPlotListButtons():
	return mainInterface.numPlotListButtons()

#FfH: Added by Talchas 05/19/2007
trophyHall = CvTrophyHall.CvTrophyHall()
def showTrophyHall():
	if (-1 != CyGame().getActivePlayer()):
		#infoScreen.showScreen(-1, 1, 1)
		trophyHall.interfaceScreen()
#FfH: End Add

techChooser = CvTechChooser.CvTechChooser()
def showTechChooser():
	if (-1 != CyGame().getActivePlayer()):
		techChooser.interfaceScreen()

hallOfFameScreen = CvHallOfFameScreen.CvHallOfFameScreen(HALL_OF_FAME)
def showHallOfFame(argsList):
	hallOfFameScreen.interfaceScreen(argsList[0])

civicScreen = CvCivicsScreen.CvCivicsScreen()
def showCivicsScreen():
	if (-1 != CyGame().getActivePlayer()):
		civicScreen.interfaceScreen()

religionScreen = CvReligionScreen.CvReligionScreen()
def showReligionScreen():
	if (-1 != CyGame().getActivePlayer()):
		religionScreen.interfaceScreen()

corporationScreen = CvCorporationScreen.CvCorporationScreen()
def showCorporationScreen():
	if (-1 != CyGame().getActivePlayer()):
		corporationScreen.interfaceScreen()

## FfH Card Game: begin
def updateCorporationElement(part, argsList = None):
	corporationScreen.updateElement(part, argsList)
## FfH Card Game: end

optionsScreen = CvOptionsScreen.CvOptionsScreen()
def showOptionsScreen():
	optionsScreen.interfaceScreen()

#foreignAdvisor = CvForeignAdvisor.CvForeignAdvisor()
foreignAdvisor = CvExoticForeignAdvisor.CvExoticForeignAdvisor()
def showForeignAdvisorScreen(argsList):
	if (-1 != CyGame().getActivePlayer()):
		foreignAdvisor.interfaceScreen(argsList[0])

# BUG - Finance Advisor - start
financeAdvisor = None
def createFinanceAdvisor():
	"""Creates the correct Finance Advisor based on an option."""
	global financeAdvisor
	if financeAdvisor is None:
		if (AdvisorOpt.isBugFinanceAdvisor()):
			import BugFinanceAdvisor
			financeAdvisor = BugFinanceAdvisor.BugFinanceAdvisor()
		else:
			import CvFinanceAdvisor
			financeAdvisor = CvFinanceAdvisor.CvFinanceAdvisor()
		HandleInputMap[FINANCE_ADVISOR] = financeAdvisor
# BUG - Finance Advisor - end

def showFinanceAdvisor():
	if (-1 != CyGame().getActivePlayer()):
		financeAdvisor.interfaceScreen()

# BUG - CustDomAdv - start
domesticAdvisor = None
def createDomesticAdvisor():
	"""Creates the correct Domestic Advisor based on an option."""
	global domesticAdvisor
	if domesticAdvisor is None:
		if (CustDomAdvOpt.isEnabled()):
			import CvCustomizableDomesticAdvisor
			domesticAdvisor = CvCustomizableDomesticAdvisor.CvCustomizableDomesticAdvisor()
		else:
			import CvDomesticAdvisor
			domesticAdvisor = CvDomesticAdvisor.CvDomesticAdvisor()
		HandleInputMap[DOMESTIC_ADVISOR] = domesticAdvisor
# BUG - CustDomAdv - end

def showDomesticAdvisor(argsList):
	if (-1 != CyGame().getActivePlayer()):
		domesticAdvisor.interfaceScreen()

# BUG - Military Advisor - start
militaryAdvisor = None
def createMilitaryAdvisor():
	"""Creates the correct Military Advisor based on an option."""
	global militaryAdvisor
	if militaryAdvisor is None:
		if (AdvisorOpt.isBUG_MA()):
			import CvBUGMilitaryAdvisor
			militaryAdvisor = CvBUGMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
		else:
			import CvMilitaryAdvisor
			militaryAdvisor = CvMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
		HandleInputMap[MILITARY_ADVISOR] = militaryAdvisor

def showMilitaryAdvisor():
	if (-1 != CyGame().getActivePlayer()):
		if (AdvisorOpt.isBUG_MA()):
			# TODO: move to CvBUGMilitaryAdvisor.interfaceScreen()
			militaryAdvisor.IconGridActive = False
		militaryAdvisor.interfaceScreen()
# BUG - Military Advisor - end

espionageAdvisor = CvEspionageAdvisor.CvEspionageAdvisor()
def showEspionageAdvisor():
#	if (-1 != CyGame().getActivePlayer()):
	espionageAdvisor.interfaceScreen()

dawnOfMan = CvDawnOfMan.CvDawnOfMan(DAWN_OF_MAN)
def showDawnOfMan(argsList):
	dawnOfMan.interfaceScreen()

introMovie = CvIntroMovieScreen.CvIntroMovieScreen()
def showIntroMovie(argsList):
	introMovie.interfaceScreen()

victoryMovie = CvVictoryMovieScreen.CvVictoryMovieScreen()
def showVictoryMovie(argsList):
	victoryMovie.interfaceScreen(argsList[0])

wonderMovie = CvWonderMovieScreen.CvWonderMovieScreen()
def showWonderMovie(argsList):
	wonderMovie.interfaceScreen(argsList[0], argsList[1], argsList[2])

eraMovie = CvEraMovieScreen.CvEraMovieScreen()
def showEraMovie(argsList):
	return
#	eraMovie.interfaceScreen(argsList[0])

spaceShip = CvSpaceShipScreen.CvSpaceShipScreen()
def showSpaceShip(argsList):
	if (-1 != CyGame().getActivePlayer()):
		spaceShip.interfaceScreen(argsList[0])

replayScreen = CvReplayScreen.CvReplayScreen(REPLAY_SCREEN)
def showReplay(argsList):
	if argsList[0] > -1:
		CyGame().saveReplay(argsList[0])
	replayScreen.showScreen(argsList[4])

danQuayleScreen = CvDanQuayle.CvDanQuayle()
def showDanQuayleScreen(argsList):
	danQuayleScreen.interfaceScreen()

unVictoryScreen = CvUnVictoryScreen.CvUnVictoryScreen()
def showUnVictoryScreen(argsList):
	unVictoryScreen.interfaceScreen()

topCivs = CvTopCivs.CvTopCivs()
def showTopCivs():
	topCivs.showScreen()

infoScreen = CvInfoScreen.CvInfoScreen(INFO_SCREEN)
def showInfoScreen(argsList):
	if (-1 != CyGame().getActivePlayer()):
		iTabID = argsList[0]
		iEndGame = argsList[1]
		infoScreen.showScreen(-1, iTabID, iEndGame)

debugInfoScreen = CvDebugInfoScreen.CvDebugInfoScreen()
def showDebugInfoScreen():
	debugInfoScreen.interfaceScreen()

# BUG - Tech Splash Screen - start
techSplashScreen = None
def createTechSplash():
	"""Creates the correct Tech Splash Screen based on an option."""
	global techSplashScreen
	if techSplashScreen is None:
		if (TechWindowOpt.isDetailedView()):
			import TechWindow
			techSplashScreen = TechWindow.CvTechSplashScreen(TECH_SPLASH)
		elif (TechWindowOpt.isWideView()):
			import TechWindowWide
			techSplashScreen = TechWindowWide.CvTechSplashScreen(TECH_SPLASH)
		else:
			import CvTechSplashScreen
			techSplashScreen = CvTechSplashScreen.CvTechSplashScreen(TECH_SPLASH)
	HandleInputMap[TECH_SPLASH] = techSplashScreen

def deleteTechSplash(option=None, value=None):
	global techSplashScreen
	techSplashScreen = None
	if TECH_SPLASH in HandleInputMap:
		del HandleInputMap[TECH_SPLASH]

def showTechSplash(argsList):
	if techSplashScreen is None:
		createTechSplash()
	techSplashScreen.interfaceScreen(argsList[0])
# BUG - Tech Splash Screen - end

victoryScreen = CvVictoryScreen.CvVictoryScreen(VICTORY_SCREEN)
def showVictoryScreen():
	if (-1 != CyGame().getActivePlayer()):
		victoryScreen.interfaceScreen()

# RevolutionDCM - RevolutionWatchAdvisor - start
revolutionWatchAdvisor = None
def createRevolutionWatchAdvisor():
	"""Creates the Revolution Watch Advisor."""
	global revolutionWatchAdvisor
	if revolutionWatchAdvisor is None:
		import RevolutionWatchAdvisor
		revolutionWatchAdvisor = RevolutionWatchAdvisor.RevolutionWatchAdvisor()
		HandleInputMap[REVOLUTION_WATCH_ADVISOR] = revolutionWatchAdvisor

def showRevolutionWatchAdvisor(argsList):
	if (-1 != CyGame().getActivePlayer()):
		revolutionWatchAdvisor.interfaceScreen()

def isRevolutionWatchAdvisor():
	return revolutionWatchAdvisor.isVisible()

def cityScreenRedraw():
	mainInterface.updateCityScreen()

# RevolutionDCM - RevolutionWatchAdvisor - end
# BUG - Sevopedia - start

pediaMainScreen = None
bUsingSevopedia = False
def createCivilopedia():
	"""Creates the correct Civilopedia based on an option."""
	global pediaMainScreen
	global bUsingSevopedia
	if pediaMainScreen is None:
		import SevoPediaUtil
		if (AdvisorOpt.Sevopedia()):
			import SevoPediaMain
			import SevoPediaHistory
			bUsingSevopedia = True
			pediaMainScreen = SevoPediaMain.SevoPediaMain()
		else:
			import CvPediaMain
			import CvPediaHistory
			bUsingSevopedia = False
			pediaMainScreen = CvPediaMain.CvPediaMain()
		HandleInputMap.update(
							{
								PEDIA_MAIN : pediaMainScreen,
								PEDIA_TECH : pediaMainScreen,
								PEDIA_UNIT : pediaMainScreen,
								PEDIA_BUILDING : pediaMainScreen,
								PEDIA_PROMOTION : pediaMainScreen,
								PEDIA_PROJECT : pediaMainScreen,
								PEDIA_UNIT_CHART : pediaMainScreen,
								PEDIA_BONUS : pediaMainScreen,
								PEDIA_IMPROVEMENT : pediaMainScreen,
								PEDIA_TERRAIN : pediaMainScreen,
								PEDIA_FEATURE : pediaMainScreen,
								PEDIA_CIVIC : pediaMainScreen,
								PEDIA_CIVILIZATION : pediaMainScreen,
								PEDIA_LEADER : pediaMainScreen,
								PEDIA_RELIGION : pediaMainScreen,
#								PEDIA_CORPORATION : pediaMainScreen,
								PEDIA_SPELL : pediaMainScreen,
								PEDIA_HISTORY : pediaMainScreen,

								SevoScreenEnums.PEDIA_MAIN		: pediaMainScreen,
								SevoScreenEnums.PEDIA_TECHS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_UNITS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_UNIT_UPGRADES	: pediaMainScreen,
								SevoScreenEnums.PEDIA_UNIT_CATEGORIES	: pediaMainScreen,
								SevoScreenEnums.PEDIA_PROMOTIONS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_PROMOTION_TREE	: pediaMainScreen,
								SevoScreenEnums.PEDIA_BUILDINGS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_NATIONAL_WONDERS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_GREAT_WONDERS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_PROJECTS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_SPECIALISTS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_TERRAINS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_FEATURES		: pediaMainScreen,
								SevoScreenEnums.PEDIA_BONUSES		: pediaMainScreen,
								SevoScreenEnums.PEDIA_IMPROVEMENTS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_CIVS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_LEADERS		: pediaMainScreen,
							# MINOR_LEADERS_PEDIA 08/2013 lfgr
								SevoScreenEnums.PEDIA_MINOR_LEADERS	: pediaMainScreen,
							# MINOR_LEADERS_PEDIA end
								SevoScreenEnums.PEDIA_TRAITS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_CIVICS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_RELIGIONS		: pediaMainScreen,
#								SevoScreenEnums.PEDIA_CORPORATIONS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_SPELLS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_CONCEPTS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_BTS_CONCEPTS	: pediaMainScreen,
								SevoScreenEnums.PEDIA_HINTS		: pediaMainScreen,
								SevoScreenEnums.PEDIA_SHORTCUTS		: pediaMainScreen,
							})
		global HandleNavigationMap
		HandleNavigationMap = {
							MAIN_INTERFACE : mainInterface,
							PEDIA_MAIN : pediaMainScreen,
							PEDIA_TECH : pediaMainScreen,
							PEDIA_UNIT : pediaMainScreen,
							PEDIA_BUILDING : pediaMainScreen,
							PEDIA_PROMOTION : pediaMainScreen,
							PEDIA_PROJECT : pediaMainScreen,
							PEDIA_UNIT_CHART : pediaMainScreen,
							PEDIA_BONUS : pediaMainScreen,
							PEDIA_IMPROVEMENT : pediaMainScreen,
							PEDIA_TERRAIN : pediaMainScreen,
							PEDIA_FEATURE : pediaMainScreen,
							PEDIA_CIVIC : pediaMainScreen,
							PEDIA_CIVILIZATION : pediaMainScreen,
							PEDIA_LEADER : pediaMainScreen,
							PEDIA_HISTORY : pediaMainScreen,
							PEDIA_RELIGION : pediaMainScreen,
#							PEDIA_CORPORATION : pediaMainScreen,
							PEDIA_SPELL : pediaMainScreen,

							SevoScreenEnums.PEDIA_MAIN		: pediaMainScreen,
							SevoScreenEnums.PEDIA_TECHS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_UNITS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_UNIT_UPGRADES	: pediaMainScreen,
							SevoScreenEnums.PEDIA_UNIT_CATEGORIES	: pediaMainScreen,
							SevoScreenEnums.PEDIA_PROMOTIONS	: pediaMainScreen,
							SevoScreenEnums.PEDIA_PROMOTION_TREE	: pediaMainScreen,
							SevoScreenEnums.PEDIA_BUILDINGS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_NATIONAL_WONDERS	: pediaMainScreen,
							SevoScreenEnums.PEDIA_GREAT_WONDERS	: pediaMainScreen,
							SevoScreenEnums.PEDIA_PROJECTS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_SPECIALISTS	: pediaMainScreen,
							SevoScreenEnums.PEDIA_TERRAINS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_FEATURES		: pediaMainScreen,
							SevoScreenEnums.PEDIA_BONUSES		: pediaMainScreen,
							SevoScreenEnums.PEDIA_IMPROVEMENTS	: pediaMainScreen,
							SevoScreenEnums.PEDIA_CIVS		 	: pediaMainScreen,
							SevoScreenEnums.PEDIA_LEADERS		: pediaMainScreen,
						# MINOR_LEADERS_PEDIA 08/2013 lfgr
							SevoScreenEnums.PEDIA_MINOR_LEADERS	: pediaMainScreen,
						# MINOR_LEADERS_PEDIA end
							SevoScreenEnums.PEDIA_TRAITS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_CIVICS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_RELIGIONS		: pediaMainScreen,
#							SevoScreenEnums.PEDIA_CORPORATIONS	: pediaMainScreen,
							SevoScreenEnums.PEDIA_SPELLS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_CONCEPTS		: pediaMainScreen,
							SevoScreenEnums.PEDIA_BTS_CONCEPTS	: pediaMainScreen,
							SevoScreenEnums.PEDIA_HINTS			: pediaMainScreen,
							SevoScreenEnums.PEDIA_SHORTCUTS		: pediaMainScreen,
						}

def linkToPedia(argsList):
	pediaMainScreen.link(argsList[0])

def pediaShow():
	createCivilopedia()
	return pediaMainScreen.pediaShow()

def pediaBack():
	return pediaMainScreen.back()

def pediaForward():
	return pediaMainScreen.forward()

def pediaMain(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_MAIN, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_MAIN, argsList[0], True)

def pediaJumpToTech(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_TECHS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_TECH, argsList[0], True)

def pediaJumpToUnit(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_UNITS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_UNIT, argsList[0], True)

def pediaJumpToUnitChart(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_UNIT_CATEGORIES, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_UNIT_CHART, argsList[0], True)

def pediaJumpToPromotion(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_PROMOTIONS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_PROMOTION, argsList[0], True)

def pediaJumpToBuilding(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_BUILDINGS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_BUILDING, argsList[0], True)

def pediaJumpToProject(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_PROJECTS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_PROJECT, argsList[0], True)

def pediaJumpToSpecialist(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_SPECIALISTS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_SPECIALIST, argsList[0], True)

def pediaJumpToSpell(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_SPELLS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_SPELL, argsList[0], True)

def pediaJumpToTrait(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_TRAITS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_TRAITS, argsList[0], True)

def pediaJumpToTerrain(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_TERRAINS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_TERRAIN, argsList[0], True)

def pediaJumpToFeature(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_FEATURES, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_FEATURE, argsList[0], True)

def pediaJumpToBonus(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_BONUSES, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_BONUS, argsList[0], True)

def pediaJumpToImprovement(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_IMPROVEMENTS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_IMPROVEMENT, argsList[0], True)

def pediaJumpToCiv(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CIVS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_CIVILIZATION, argsList[0], True)

def pediaJumpToLeader(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_LEADERS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_LEADER, argsList[0], True)

def pediaJumpToCivic(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CIVICS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_CIVIC, argsList[0], True)

def pediaJumpToReligion(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_RELIGIONS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_RELIGION, argsList[0], True)

def pediaJumpToCorporation(argsList):
	if (bUsingSevopedia):
		pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CORPORATIONS, argsList[0], True, False)
	else:
		pediaMainScreen.pediaJump(PEDIA_CORPORATION, argsList[0], True)

def pediaShowHistorical(argsList):
	if (bUsingSevopedia):
		if (argsList[0] == CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT_NEW):
			pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_BTS_CONCEPTS, argsList[1], True, False)
		else:
			pediaMainScreen.pediaJump(SevoScreenEnums.PEDIA_CONCEPTS, argsList[1], True, False)
	else:
		iEntryId = pediaMainScreen.pediaHistorical.getIdFromEntryInfo(argsList[0], argsList[1])
		pediaMainScreen.pediaJump(PEDIA_HISTORY, iEntryId, True)

# BUG - Sevopedia - end

#################################################
## Worldbuilder
#################################################
worldBuilderScreen = CvWorldBuilderScreen.CvWorldBuilderScreen()
def getWorldBuilderScreen():
	return worldBuilderScreen

def showWorldBuilderScreen():
	worldBuilderScreen.interfaceScreen()

def hideWorldBuilderScreen():
	worldBuilderScreen.killScreen()

def WorldBuilderToggleUnitEditCB():
	worldBuilderScreen.toggleUnitEditCB()

def WorldBuilderEraseCB():
	worldBuilderScreen.eraseCB()

def WorldBuilderLandmarkCB():
	worldBuilderScreen.landmarkModeCB()

def WorldBuilderExitCB():
	worldBuilderScreen.Exit()

def WorldBuilderToggleCityEditCB():
	worldBuilderScreen.toggleCityEditCB()

def WorldBuilderNormalPlayerTabModeCB():
	worldBuilderScreen.normalPlayerTabModeCB()

def WorldBuilderNormalMapTabModeCB():
	worldBuilderScreen.normalMapTabModeCB()

def WorldBuilderRevealTabModeCB():
	worldBuilderScreen.revealTabModeCB()

def WorldBuilderDiplomacyModeCB():
	worldBuilderScreen.diplomacyModeCB()

def WorldBuilderRevealAllCB():
	worldBuilderScreen.revealAll(True)

def WorldBuilderUnRevealAllCB():
	worldBuilderScreen.revealAll(False)

def WorldBuilderHandleUnitCB( argsList ):
	worldBuilderScreen.handleUnitCB(argsList)

def WorldBuilderHandleTerrainCB( argsList ):
	worldBuilderScreen.handleTerrainCB(argsList)

def WorldBuilderHandleFeatureCB(argsList):
	worldBuilderScreen.handleFeatureCB(argsList)

def WorldBuilderHandleBonusCB( argsList ):
	worldBuilderScreen.handleBonusCB(argsList)

def WorldBuilderHandleImprovementCB(argsList):
	worldBuilderScreen.handleImprovementCB(argsList)

def WorldBuilderHandleTerritoryCB(argsList):
	worldBuilderScreen.handleTerritoryCB(argsList)

def WorldBuilderHandlePlotTypeCB( argsList ):
	worldBuilderScreen.handlePlotTypeCB(argsList)

def WorldBuilderHandleUnitEditExperienceCB( argsList ):
	worldBuilderScreen.handleUnitEditExperienceCB(argsList)

def WorldBuilderHandleUnitEditLevelCB( argsList ):
	worldBuilderScreen.handleUnitEditLevelCB(argsList)

def WorldBuilderHandleUnitEditNameCB( argsList ):
	worldBuilderScreen.handleUnitEditNameCB(argsList)

def WorldBuilderHandleCityEditPopulationCB( argsList ):
	worldBuilderScreen.handleCityEditPopulationCB(argsList)

##MagisterModmod
def WorldBuilderHandleCityEditRevIndexCB( argsList ):
	worldBuilderScreen.handleCityEditRevIndexCB(argsList)


def WorldBuilderHandleCivTypeEditPullDownCB( argsList ):
	worldBuilderScreen.handleCivTypeEditPullDownCB(argsList)


##MagisterModmod

def WorldBuilderHandleCityEditCultureCB( argsList ):
	worldBuilderScreen.handleCityEditCultureCB(argsList)

def WorldBuilderHandleCityEditNameCB( argsList ):
	worldBuilderScreen.handleCityEditNameCB(argsList)

def WorldBuilderHandleLandmarkTextCB( argsList ):
	worldBuilderScreen.handleLandmarkTextCB(argsList)

def WorldBuilderHandleUnitEditPullDownCB( argsList ):
	worldBuilderScreen.handleUnitEditPullDownCB(argsList)

def WorldBuilderHandleUnitAITypeEditPullDownCB( argsList ):
	worldBuilderScreen.handleUnitAITypeEditPullDownCB(argsList)

def WorldBuilderHandlePlayerEditPullDownCB( argsList ):
	worldBuilderScreen.handlePlayerEditPullDownCB(argsList)

def WorldBuilderHandlePlayerUnitPullDownCB( argsList ):
	worldBuilderScreen.handlePlayerUnitPullDownCB(argsList)

def WorldBuilderHandleSelectTeamPullDownCB( argsList ):
	worldBuilderScreen.handleSelectTeamPullDownCB(argsList)

def WorldBuilderHandleBuildingCB( argsList ):
	worldBuilderScreen.handleBuildingCB(argsList)

def WorldBuilderHandleTechCB( argsList ):
	worldBuilderScreen.handleTechCB(argsList)

def WorldBuilderHandleRouteCB( argsList ):
	worldBuilderScreen.handleRouteCB(argsList)

def WorldBuilderHandleLandmarkCB( argsList ):
	worldBuilderScreen.handleLandmarkCB(argsList)

## Platy World Builder Start ##

def WorldBuilderHandleEditScriptCB( argsList ):
	worldBuilderScreen.handleEditScriptCB(argsList)

def WorldBuilderHandleEnterNewScreenCB( argsList ):
	worldBuilderScreen.handleEnterNewScreenCB(argsList)

def WorldBuilderHandleCurrentPlayerEditPullDownCB( argsList ):
	worldBuilderScreen.handleCurrentPlayerEditPullDownCB(argsList)

## Unit Data ##

def WorldBuilderHandleUnitEditStrengthCB( argsList ):
	worldBuilderScreen.handleUnitEditStrengthCB(argsList)
##MagisterModmod

def WorldBuilderHandleUnitEditIDSelectCB( argsList ):
	worldBuilderScreen.handleUnitEditIDSelectCB(argsList)


def WorldBuilderHandleUnitReligionEditPullDownCB( argsList ):
	worldBuilderScreen.handleUnitReligionEditPullDownCB(argsList)

def WorldBuilderHandleUnitEditStrengthDefenseCB( argsList ):
	worldBuilderScreen.handleUnitEditStrengthDefenseCB(argsList)

def WorldBuilderHandleUnitEditDurationCB( argsList ):
	worldBuilderScreen.handleUnitEditDurationCB(argsList)

def WorldBuilderHandleUnitEditSummonerCB( argsList ):
	worldBuilderScreen.handleUnitEditSummonerCB(argsList)

def WorldBuilderHandleUnitEditHasCastedCB( argsList ):
	worldBuilderScreen.handleUnitEditHasCastedCB(argsList)

def WorldBuilderHandleUnitEditIsImmortalCB( argsList ):
	worldBuilderScreen.handleUnitEditIsImmortalCB(argsList)


def WorldBuilderHandleUnitEditAvatarOfCivLeaderCB( argsList ):
	worldBuilderScreen.handleUnitEditAvatarOfCivLeaderCB(argsList)


def WorldBuilderHandleUnitEditScenarioCounterCB( argsList ):
	worldBuilderScreen.handleUnitEditScenarioCounterCB(argsList)

##MagisterModmod

def WorldBuilderHandleUnitEditDamageCB( argsList ):
	worldBuilderScreen.handleUnitEditDamageCB(argsList)

def WorldBuilderHandleUnitEditCargoCB( argsList ):
	worldBuilderScreen.handleUnitEditCargoCB(argsList)

def WorldBuilderHandleUnitEditMovesCB( argsList ):
	worldBuilderScreen.handleUnitEditMovesCB(argsList)

def WorldBuilderHandleUnitEditImmobileTimerCB( argsList ):
	worldBuilderScreen.handleUnitEditImmobileTimerCB(argsList)

def WorldBuilderHandleUnitEditPromotionReadyCB( argsList ):
	worldBuilderScreen.handleUnitEditPromotionReadyCB(argsList)

def WorldBuilderHandleUnitEditMadeAttackCB( argsList ):
	worldBuilderScreen.handleUnitEditMadeAttackCB(argsList)

def WorldBuilderHandleUnitEditMadeInterceptionCB( argsList ):
	worldBuilderScreen.handleUnitEditMadeInterceptionCB(argsList)

def WorldBuilderHandleMoveUnitCB( argsList ):
	worldBuilderScreen.handleMoveUnitCB(argsList)

def WorldBuilderHandleUnitEditDuplicateCB( argsList ):
	worldBuilderScreen.handleUnitEditDuplicateCB(argsList)

def WorldBuilderHandleKillCB( argsList ):
	worldBuilderScreen.handleKillCB(argsList)

def WorldBuilderHandleUnitEditDirectionCB( argsList ):
	worldBuilderScreen.handleUnitEditDirectionCB(argsList)

def WorldBuilderHandleUnitEditLeaderCB( argsList ):
	worldBuilderScreen.handleUnitEditLeaderCB(argsList)

def WorldBuilderHandleUnitEditUnitTypeCB( argsList ):
	worldBuilderScreen.handleUnitEditUnitTypeCB(argsList)

## Game Option ##

def WorldBuilderHandleEditGameOptionCB( argsList ):
	worldBuilderScreen.handleEditGameOptionCB(argsList)

def WorldBuilderHandleGameEditStartYearCB( argsList ):
	worldBuilderScreen.handleGameEditStartYearCB(argsList)

def WorldBuilderHandleGameEditNukesExplodedCB( argsList ):
	worldBuilderScreen.handleGameEditNukesExplodedCB(argsList)

def WorldBuilderHandleVisibleOptionsCB( argsList ):
	worldBuilderScreen.handleVisibleOptionsCB(argsList)


##MagisterModmod
def WorldBuilderHandleGameEditScenarioCounterCB( argsList ):
	worldBuilderScreen.handleGameEditScenarioCounterCB(argsList)


def WorldBuilderHandleGlobalCounterEditCB( argsList ):
	worldBuilderScreen.handleGlobalCounterEditCB(argsList)
##MagisterModmod

## City Data ##

def WorldBuilderHandleChooseCityCB( argsList ):
	worldBuilderScreen.handleChooseCityCB(argsList)

def WorldBuilderHandleCityEditCultureLevelCB( argsList ):
	worldBuilderScreen.handleCityEditCultureLevelCB(argsList)

def WorldBuilderHandleCityEditHappinessCB( argsList ):
	worldBuilderScreen.handleCityEditHappinessCB(argsList)

def WorldBuilderHandleCityEditHealthCB( argsList ):
	worldBuilderScreen.handleCityEditHealthCB(argsList)

def WorldBuilderHandleCityEditTimersCB( argsList ):
	worldBuilderScreen.handleCityEditTimersCB(argsList)

def WorldBuilderHandleCityEditCurrentTimerCB( argsList ):
	worldBuilderScreen.handleCityEditCurrentTimerCB(argsList)

def WorldBuilderHandleCityEditDefenseCB( argsList ):
	worldBuilderScreen.handleCityEditDefenseCB(argsList)

def WorldBuilderHandleCityEditTradeRouteCB( argsList ):
	worldBuilderScreen.handleCityEditTradeRouteCB(argsList)

def WorldBuilderHandleCityEditBuildingClassCB( argsList ):
	worldBuilderScreen.handleCityEditBuildingClassCB(argsList)

def WorldBuilderHandleCityEditModiferCB( argsList ):
	worldBuilderScreen.handleCityEditModiferCB(argsList)

def WorldBuilderHandleCityEditModifyBuildingClassCB( argsList ):
	worldBuilderScreen.handleCityEditModifyBuildingClassCB(argsList)

def WorldBuilderHandleCityEditChooseProductionCB( argsList ):
	worldBuilderScreen.handleCityEditChooseProductionCB(argsList)

def WorldBuilderHandleCityEditProductionProgressCB( argsList ):
	worldBuilderScreen.handleCityEditProductionProgressCB(argsList)

def WorldBuilderHandleCityEditFoodCB( argsList ):
	worldBuilderScreen.handleCityEditFoodCB(argsList)

## Player Data ##

def WorldBuilderHandlePlayerEditGoldCB( argsList ):
	worldBuilderScreen.handlePlayerEditGoldCB(argsList)

def WorldBuilderHandleCurrentEraEditPullDownCB( argsList ):
	worldBuilderScreen.handleCurrentEraEditPullDownCB(argsList)

def WorldBuilderHandleTeamEditCommerceFlexibleCB( argsList ):
	worldBuilderScreen.handleTeamEditCommerceFlexibleCB(argsList)

def WorldBuilderHandlePlayerEditCommercePercentCB( argsList ):
	worldBuilderScreen.handlePlayerEditCommercePercentCB(argsList)

def WorldBuilderHandlePlayerEditGoldenAgeCB( argsList ):
	worldBuilderScreen.handlePlayerEditGoldenAgeCB(argsList)

def WorldBuilderHandlePlayerEditGoldenAgeUnitsCB( argsList ):
	worldBuilderScreen.handlePlayerEditGoldenAgeUnitsCB(argsList)

def WorldBuilderHandlePlayerEditAnarchyCB( argsList ):
	worldBuilderScreen.handlePlayerEditAnarchyCB(argsList)

def WorldBuilderHandlePlayerEditCombatExperienceCB( argsList ):
	worldBuilderScreen.handlePlayerEditCombatExperienceCB(argsList)

def WorldBuilderHandlePlayerEditCivicCB( argsList ):
	worldBuilderScreen.handlePlayerEditCivicCB(argsList)

def WorldBuilderHandleStateReligionEditPullDownCB( argsList ):
	worldBuilderScreen.handleStateReligionEditPullDownCB(argsList)

##MagisterModmod
def WorldBuilderHandleAlignmentEditPullDownCB( argsList ):
	worldBuilderScreen.handleAlignmentEditPullDownCB(argsList)

def WorldBuilderHandleEditPlayerTraitCB( argsList ):
	worldBuilderScreen.handleEditPlayerTraitCB(argsList)

def WorldBuilderHandleEditFeatHasCastWorldSpellCB( argsList ):
	worldBuilderScreen.handleEditFeatHasCastWorldSpellCB(argsList)

def WorldBuilderHandleEditFeatTrustCB( argsList ):
	worldBuilderScreen.handleEditFeatTrustCB(argsList)

def WorldBuilderHandleEditFeatHealUnitPerTurnCB( argsList ):
	worldBuilderScreen.handleEditFeatHealUnitPerTurnCB(argsList)



##MagisterModmod

def WorldBuilderHandlePlayerEditStateReligionUnitProductionCB( argsList ):
	worldBuilderScreen.handlePlayerEditStateReligionUnitProductionCB(argsList)

def WorldBuilderHandlePlayerEditStateReligionBuildingProductionCB( argsList ):
	worldBuilderScreen.handlePlayerEditStateReligionBuildingProductionCB(argsList)

def WorldBuilderHandleCurrentTechEditPullDownCB( argsList ):
	worldBuilderScreen.handleCurrentTechEditPullDownCB(argsList)

def WorldBuilderHandleTeamEditResearchProgressCB( argsList ):
	worldBuilderScreen.handleTeamEditResearchProgressCB(argsList)

def WorldBuilderHandleTriggerEventCB( argsList ):
	worldBuilderScreen.handleTriggerEventCB(argsList)

## Team Data ##

def WorldBuilderHandleTeamEditPullDownCB( argsList ):
	worldBuilderScreen.handleTeamEditPullDownCB(argsList)

def WorldBuilderHandleAddTeamCB( argsList ):
	worldBuilderScreen.handleAddTeamCB(argsList)

def WorldBuilderHandleTeamEditNukeInterceptionCB( argsList ):
	worldBuilderScreen.handleTeamEditNukeInterceptionCB(argsList)

def WorldBuilderHandleDomainEditPullDownCB( argsList ):
	worldBuilderScreen.handleDomainEditPullDownCB(argsList)

def WorldBuilderHandleTeamEditDomainMovesCB( argsList ):
	worldBuilderScreen.handleTeamEditDomainMovesCB(argsList)

def WorldBuilderHandleRouteEditPullDownCB( argsList ):
	worldBuilderScreen.handleRouteEditPullDownCB(argsList)

def WorldBuilderHandleTeamEditRouteChangeCB( argsList ):
	worldBuilderScreen.handleTeamEditRouteChangeCB(argsList)

def WorldBuilderHandleImprovementEditPullDownCB( argsList ):
	worldBuilderScreen.handleImprovementEditPullDownCB(argsList)

def WorldBuilderHandleYieldEditPullDownCB( argsList ):
	worldBuilderScreen.handleYieldEditPullDownCB(argsList)

def WorldBuilderHandleTeamEditImprovementYieldCB( argsList ):
	worldBuilderScreen.handleTeamEditImprovementYieldCB(argsList)

def WorldBuilderHandleTeamEditMapCenteringCB( argsList ):
	worldBuilderScreen.handleTeamEditMapCenteringCB(argsList)

def WorldBuilderHandleTeamEditGoldTradingCB( argsList ):
	worldBuilderScreen.handleTeamEditGoldTradingCB(argsList)

def WorldBuilderHandleTeamEditTechTradingCB( argsList ):
	worldBuilderScreen.handleTeamEditTechTradingCB(argsList)

def WorldBuilderHandleTeamEditMapTradingCB( argsList ):
	worldBuilderScreen.handleTeamEditMapTradingCB(argsList)

def WorldBuilderHandleTeamEditOpenBordersTradingCB( argsList ):
	worldBuilderScreen.handleTeamEditOpenBordersTradingCB(argsList)

def WorldBuilderHandleTeamEditPermanentAllianceTradingCB( argsList ):
	worldBuilderScreen.handleTeamEditPermanentAllianceTradingCB(argsList)

def WorldBuilderHandleTeamEditDefensivePactTradingCB( argsList ):
	worldBuilderScreen.handleTeamEditDefensivePactTradingCB(argsList)

def WorldBuilderHandleTeamEditVassalTradingCB( argsList ):
	worldBuilderScreen.handleTeamEditVassalTradingCB(argsList)

def WorldBuilderHandleTeamEditWaterWorkCB( argsList ):
	worldBuilderScreen.handleTeamEditWaterWorkCB(argsList)

def WorldBuilderHandleTeamEditExtraWaterSeeFromCB( argsList ):
	worldBuilderScreen.handleTeamEditExtraWaterSeeFromCB(argsList)

def WorldBuilderHandleTeamEditBridgeBuildingCB( argsList ):
	worldBuilderScreen.handleTeamEditBridgeBuildingCB(argsList)

def WorldBuilderHandleTeamEditIrrigationCB( argsList ):
	worldBuilderScreen.handleTeamEditIrrigationCB(argsList)

def WorldBuilderHandleTeamEditIgnoreIrrigationCB( argsList ):
	worldBuilderScreen.handleTeamEditIgnoreIrrigationCB(argsList)

def WorldBuilderHandleTeamEditEnemyWarWearinessCB( argsList ):
	worldBuilderScreen.handleTeamEditEnemyWarWearinessCB(argsList)

def WorldBuilderHandleTeamEditKnownCivsCB( argsList ):
	worldBuilderScreen.handleTeamEditKnownCivsCB(argsList)

def WorldBuilderHandleTeamEditTechShareCB( argsList ):
	worldBuilderScreen.handleTeamEditTechShareCB(argsList)

def WorldBuilderHandleTeamEditForceTeamVoteCB( argsList ):
	worldBuilderScreen.handleTeamEditForceTeamVoteCB(argsList)

## Plot ##

def WorldBuilderHandlePlotEditCultureCB( argsList ):
	worldBuilderScreen.handlePlotEditCultureCB(argsList)

def WorldBuilderHandlePlotEditYieldCB( argsList ):
	worldBuilderScreen.handlePlotEditYieldCB(argsList)

def WorldBuilderHandlePlotEditPlotTypeCB( argsList ):
	worldBuilderScreen.handlePlotEditPlotTypeCB(argsList)

def WorldBuilderHandlePlotEditTerrainCB( argsList ):
	worldBuilderScreen.handlePlotEditTerrainCB(argsList)

def WorldBuilderHandlePlotAddCityCB( argsList ):
	worldBuilderScreen.handlePlotAddCityCB(argsList)

##MagisterModmod
def WorldBuilderHandlePlotMoveDisabledAICB( argsList ):
	worldBuilderScreen.handlePlotMoveDisabledAICB(argsList)

def WorldBuilderHandlePlotMoveDisabledHumanCB( argsList ):
	worldBuilderScreen.handlePlotMoveDisabledHumanCB(argsList)

def WorldBuilderHandlePlotBuildDisabledCB( argsList ):
	worldBuilderScreen.handlePlotBuildDisabledCB(argsList)

def WorldBuilderHandlePlotFoundDisabledCB( argsList ):
	worldBuilderScreen.handlePlotFoundDisabledCB(argsList)

def WorldBuilderHandlePlotPythonActiveCB( argsList ):
	worldBuilderScreen.handlePlotPythonActiveCB(argsList)

def WorldBuilderHandlePlotEditMinLevelCB( argsList ):
	worldBuilderScreen.handlePlotMinLevelCB(argsList)

def WorldBuilderHandlePlotEditPortalExitXCB( argsList ):
	worldBuilderScreen.handlePlotPortalExitXCB(argsList)

def WorldBuilderHandlePlotEditPortalExitYCB( argsList ):
	worldBuilderScreen.handlePlotPortalExitYCB(argsList)

def WorldBuilderHandlePlotCounterEditCB( argsList ):
	worldBuilderScreen.handlePlotCounterEditCB(argsList)
##MagisterModmod

def WorldBuilderHandlePlotEditFeatureCB( argsList ):
	worldBuilderScreen.handlePlotEditFeatureCB(argsList)

def WorldBuilderHandlePlotEditVarietyCB( argsList ):
	worldBuilderScreen.handlePlotEditVarietyCB(argsList)

def WorldBuilderHandlePlotEditBonusCB( argsList ):
	worldBuilderScreen.handlePlotEditBonusCB(argsList)

def WorldBuilderHandlePlotEditImprovementCB( argsList ):
	worldBuilderScreen.handlePlotEditImprovementCB(argsList)

def WorldBuilderHandlePlotEditUpgradeProgressCB( argsList ):
	worldBuilderScreen.handlePlotEditUpgradeProgressCB(argsList)

def WorldBuilderHandlePlotEditRouteCB( argsList ):
	worldBuilderScreen.handlePlotEditRouteCB(argsList)

def WorldBuilderHandlePlotEditRiverCB( argsList ):
	worldBuilderScreen.handlePlotEditRiverCB(argsList)

def WorldBuilderHandleEventOtherPlayerCB( argsList ):
	worldBuilderScreen.handleEventOtherPlayerCB(argsList)

def WorldBuilderHandleEventUnitCB( argsList ):
	worldBuilderScreen.handleEventUnitCB(argsList)

## Platy World Builder End ##

def WorldBuilderGetHighlightPlot(argsList):
	return worldBuilderScreen.getHighlightPlot(argsList)

def WorldBuilderOnAdvancedStartBrushSelected(argsList):
	iList,iIndex,iTab = argsList;
	print("WB Advanced Start brush selected, iList=%d, iIndex=%d, type=%d" %(iList,iIndex,iTab))
	if (iTab == worldBuilderScreen.m_iASTechTabID):
		showTechChooser()
	elif (iTab == worldBuilderScreen.m_iASCityTabID and iList == worldBuilderScreen.m_iASAutomateListID):
		CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_AUTOMATE, worldBuilderScreen.m_iCurrentPlayer, -1, -1, -1, true)

	if (worldBuilderScreen.setCurrentAdvancedStartIndex(iIndex)):
		if (worldBuilderScreen.setCurrentAdvancedStartList(iList)):
			return 1
	return 0

def WorldBuilderOnNormalPlayerBrushSelected(argsList):
	iList,iIndex,iTab = argsList;
	print("WB brush selected, iList=%d, iIndex=%d, type=%d" %(iList,iIndex,iTab))
	if (worldBuilderScreen.setCurrentNormalPlayerIndex(iIndex)):
		return 1
	return 0

def WorldBuilderOnNormalMapBrushSelected(argsList):
	iList,iIndex,iTab = argsList;
	print("WB brush selected, iList=%d, iIndex=%d, type=%d" %(iList,iIndex,iTab))
	if (worldBuilderScreen.setCurrentNormalMapIndex(iIndex)):
		if (worldBuilderScreen.setCurrentNormalMapList(iList)):
			return 1
	return 0

def WorldBuilderOnWBEditBrushSelected(argsList):
	iList,iIndex,iTab = argsList;
	if (worldBuilderScreen.setEditButtonClicked(iIndex)):
		return 1
	return 0

def WorldBuilderOnWBEditReligionSelected(argsList):
	iList,iIndex,iTab = argsList;
	if (worldBuilderScreen.setEditReligionSelected(iIndex)):
		return 1
	return 0

def WorldBuilderOnWBEditHolyCitySelected(argsList):
	iList,iIndex,iTab = argsList;
	if (worldBuilderScreen.setEditHolyCitySelected(iIndex)):
		return 1
	return 0

def WorldBuilderOnWBEditCorporationSelected(argsList):
	iList,iIndex,iTab = argsList;
	if (worldBuilderScreen.setEditCorporationSelected(iIndex)):
		return 1
	return 0

def WorldBuilderOnWBEditHeadquartersSelected(argsList):
	iList,iIndex,iTab = argsList;
	if (worldBuilderScreen.setEditHeadquartersSelected(iIndex)):
		return 1
	return 0

def WorldBuilderOnAllPlotsBrushSelected(argsList):
	if (worldBuilderScreen.handleAllPlotsCB(argsList)):
		return 1
	return 0

def WorldBuilderGetASUnitTabID():
	return worldBuilderScreen.getASUnitTabID()

def WorldBuilderGetASCityTabID():
	return worldBuilderScreen.getASCityTabID()

def WorldBuilderGetASCityListID():
	return worldBuilderScreen.getASCityListID()

def WorldBuilderGetASBuildingsListID():
	return worldBuilderScreen.getASBuildingsListID()

def WorldBuilderGetASAutomateListID():
	return worldBuilderScreen.getASAutomateListID()

def WorldBuilderGetASImprovementsTabID():
	return worldBuilderScreen.getASImprovementsTabID()

def WorldBuilderGetASRoutesListID():
	return worldBuilderScreen.getASRoutesListID()

def WorldBuilderGetASImprovementsListID():
	return worldBuilderScreen.getASImprovementsListID()

def WorldBuilderGetASVisibilityTabID():
	return worldBuilderScreen.getASVisibilityTabID()

def WorldBuilderGetASTechTabID():
	return worldBuilderScreen.getASTechTabID()

def WorldBuilderGetUnitTabID():
	return worldBuilderScreen.getUnitTabID()

def WorldBuilderGetBuildingTabID():
	return worldBuilderScreen.getBuildingTabID()

def WorldBuilderGetTechnologyTabID():
	return worldBuilderScreen.getTechnologyTabID()

def WorldBuilderGetImprovementTabID():
	return worldBuilderScreen.getImprovementTabID()

def WorldBuilderGetBonusTabID():
	return worldBuilderScreen.getBonusTabID()

def WorldBuilderGetImprovementListID():
	return worldBuilderScreen.getImprovementListID()

def WorldBuilderGetBonusListID():
	return worldBuilderScreen.getBonusListID()

def WorldBuilderGetTerrainTabID():
	return worldBuilderScreen.getTerrainTabID()

def WorldBuilderGetTerrainListID():
	return worldBuilderScreen.getTerrainListID()

def WorldBuilderGetFeatureListID():
	return worldBuilderScreen.getFeatureListID()

def WorldBuilderGetPlotTypeListID():
	return worldBuilderScreen.getPlotTypeListID()

def WorldBuilderGetRouteListID():
	return worldBuilderScreen.getRouteListID()

def WorldBuilderGetTerritoryTabID():
	return worldBuilderScreen.getTerritoryTabID()

def WorldBuilderGetTerritoryListID():
	return worldBuilderScreen.getTerritoryListID()

def WorldBuilderHasTech(argsList):
	iTech = argsList[0]
	return worldBuilderScreen.hasTech(iTech)

def WorldBuilderHasPromotion(argsList):
	iPromotion = argsList[0]
	return worldBuilderScreen.hasPromotion(iPromotion)

def WorldBuilderHasBuilding(argsList):
	iBuilding = argsList[0]
	return worldBuilderScreen.getNumBuilding(iBuilding)
#################################################
## Utility Functions (can be overridden by CvScreenUtilsInterface
#################################################

def movieDone(argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().movieDone(argsList)):
		return

	if (argsList[0] == INTRO_MOVIE_SCREEN):
		introMovie.hideScreen()

	if (argsList[0] == VICTORY_MOVIE_SCREEN):
		victoryMovie.hideScreen()

def leftMouseDown (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().leftMouseDown(argsList)):
		return

	if ( argsList[0] == WORLDBUILDER_SCREEN ):
		worldBuilderScreen.leftMouseDown(argsList[1:])
		return 1
	return 0

def rightMouseDown (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().rightMouseDown(argsList)):
		return

	if ( argsList[0] == WORLDBUILDER_SCREEN ):
		worldBuilderScreen.rightMouseDown(argsList)
		return 1
	return 0

def mouseOverPlot (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().mouseOverPlot(argsList)):
		return

	if (WORLDBUILDER_SCREEN == argsList[0]):
		worldBuilderScreen.mouseOverPlot(argsList)

def handleInput (argsList):
	' handle input is called when a screen is up '
	inputClass = PyScreenInput.ScreenInput(argsList)

	# allows overides for mods
	ret = CvScreenUtilsInterface.getScreenUtils().handleInput( (inputClass.getPythonFile(),inputClass) )

	# get the screen that is active from the HandleInputMap Dictionary
	screen = HandleInputMap.get( inputClass.getPythonFile() )

	# call handle input on that screen
	if ( screen and not ret):
		return screen.handleInput(inputClass)
	return 0

def update (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().update(argsList)):
		return

	if (HandleInputMap.has_key(argsList[0])):
		screen = HandleInputMap.get(argsList[0])
		screen.update(argsList[1])

def onClose (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().onClose(argsList)):
		return

	if (HandleCloseMap.has_key(argsList[0])):
		screen = HandleCloseMap.get(argsList[0])
		screen.onClose()

# Forced screen update
def forceScreenUpdate (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().forceScreenUpdate(argsList)):
		return

	# Tech chooser update (forced from net message)
	if ( argsList[0] == TECH_CHOOSER ):
		techChooser.updateTechRecords(false)
	# Main interface Screen
	elif ( argsList[0] == MAIN_INTERFACE ):
		mainInterface.updateScreen()
	# world builder Screen
	elif ( argsList[0] == WORLDBUILDER_SCREEN ):
		worldBuilderScreen.updateScreen()

# Forced redraw
def forceScreenRedraw (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().forceScreenRedraw(argsList)):
		return

	# Main Interface Screen
	if ( argsList[0] == MAIN_INTERFACE ):
		mainInterface.redraw()
	elif ( argsList[0] == WORLDBUILDER_SCREEN ):
		worldBuilderScreen.redraw()
	elif ( argsList[0] == TECH_CHOOSER ):
		techChooser.updateTechRecords(true)


def minimapClicked (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().minimapClicked(argsList)):
		return

	if (MILITARY_ADVISOR == argsList[0]):
		militaryAdvisor.minimapClicked()
	return

############################################################################
## Misc Functions
############################################################################

def handleBack(screens):
	for iScreen in screens:
		if (HandleNavigationMap.has_key(iScreen)):
			screen = HandleNavigationMap.get( iScreen )
			screen.back()
	print "Mouse BACK"
	return 0

def handleForward(screens):
	for iScreen in screens:
		if (HandleNavigationMap.has_key(iScreen)):
			screen = HandleNavigationMap.get( iScreen )
			screen.forward()
	print "Mouse FWD"
	return 0

def refreshMilitaryAdvisor (argsList):
	if (1 == argsList[0]):
		militaryAdvisor.refreshSelectedGroup(argsList[1])
	elif (2 == argsList[0]):
		militaryAdvisor.refreshSelectedLeader(argsList[1])
	elif (3 == argsList[0]):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS): ## Suppress display of Great General bar
			militaryAdvisor.drawCombatExperience()
	elif (argsList[0] <= 0):
		militaryAdvisor.refreshSelectedUnit(-argsList[0], argsList[1])

def updateMusicPath (argsList):
	szPathName = argsList[0]
	optionsScreen.updateMusicPath(szPathName)

def refreshOptionsScreen():
	optionsScreen.refreshScreen()

def cityWarningOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]
	city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
	if (not city.isNone()):
		if (iButtonId == 0):
			if (city.isProductionProcess()):
				CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, False, False)
			else:
				CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, True, False)
		elif (iButtonId == 2):
			CyInterface().selectCity(city, False)

def cityWarningOnFocusCallback(argsList):
	CyInterface().playGeneralSound("AS2D_ADVISOR_SUGGEST")
	CyInterface().lookAtCityOffset(argsList[0])
	return 0

def liberateOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]
	city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
	if (not city.isNone()):
		if (iButtonId == 0):
			CyMessageControl().sendDoTask(iData1, TaskTypes.TASK_LIBERATE, 0, -1, False, False, False, False)
		elif (iButtonId == 2):
			CyInterface().selectCity(city, False)

def colonyOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]
	city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
	if (not city.isNone()):
		if (iButtonId == 0):
			CyMessageControl().sendEmpireSplit(CyGlobalContext().getGame().getActivePlayer(), city.area().getID())
		elif (iButtonId == 2):
			CyInterface().selectCity(city, False)

def featAccomplishedOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]

	if (iButtonId == 1):
		if (iData1 == FeatTypes.FEAT_TRADE_ROUTE):
			showDomesticAdvisor(())
		elif ((iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER) and (iData1 <= FeatTypes.FEAT_UNIT_SPY)):
			showMilitaryAdvisor()
		elif ((iData1 >= FeatTypes.FEAT_COPPER_CONNECTED) and (iData1 <= FeatTypes.FEAT_FOOD_CONNECTED)):
			showForeignAdvisorScreen([0])
		elif ((iData1 == FeatTypes.FEAT_NATIONAL_WONDER)):
		  # 2 is for the wonder tab...
			showInfoScreen([2, 0])
#		elif ((iData1 >= FeatTypes.FEAT_POPULATION_HALF_MILLION) and (iData1 <= FeatTypes.FEAT_POPULATION_2_BILLION)):
#		  # 1 is for the demographics tab...
#			showInfoScreen([1, 0])
		elif iData1 == FeatTypes.FEAT_CORPORATION_ENABLED:
			showCorporationScreen()

def featAccomplishedOnFocusCallback(argsList):
	iData1 = argsList[0]
	iData2 = argsList[1]
	iData3 = argsList[2]
	iData4 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	CyInterface().playGeneralSound("AS2D_FEAT_ACCOMPLISHED")
	if ((iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER) and (iData1 <= FeatTypes.FEAT_FOOD_CONNECTED)):
		CyInterface().lookAtCityOffset(iData2)

	return 0

def reassignPlayer(argsList):
	iButtonId = argsList[0]
	iOldPlayer = argsList[1]
	iNewPlayer = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]

	if iButtonId == 0:
#		CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, -1)
## OOS fix by Snarko
		CyMessageControl().sendModNetMessage(CvUtil.ChangeCiv, iOldPlayer, iNewPlayer, 0, 0)

#######################################################################################
## Handle Close Map
#######################################################################################
HandleCloseMap = {  DAWN_OF_MAN : dawnOfMan,
					SPACE_SHIP_SCREEN : spaceShip,
					TECH_CHOOSER : techChooser,
				# add new screens here
				}

#######################################################################################
## Handle Input Map
#######################################################################################
HandleInputMap = {  MAIN_INTERFACE : mainInterface,
#					DOMESTIC_ADVISOR : domesticAdvisor,
					RELIGION_SCREEN : religionScreen,
					CORPORATION_SCREEN : corporationScreen,
					CIVICS_SCREEN : civicScreen,
					TECH_CHOOSER : techChooser,
					FOREIGN_ADVISOR : foreignAdvisor,
#					FINANCE_ADVISOR : financeAdvisor,
#					MILITARY_ADVISOR : militaryAdvisor,
					DAWN_OF_MAN : dawnOfMan,
					WONDER_MOVIE_SCREEN : wonderMovie,
					ERA_MOVIE_SCREEN : eraMovie,
					SPACE_SHIP_SCREEN : spaceShip,
					INTRO_MOVIE_SCREEN : introMovie,
					OPTIONS_SCREEN : optionsScreen,
					INFO_SCREEN : infoScreen,
					REPLAY_SCREEN : replayScreen,
					VICTORY_SCREEN : victoryScreen,
					TOP_CIVS : topCivs,
					HALL_OF_FAME : hallOfFameScreen,
					VICTORY_MOVIE_SCREEN : victoryMovie,
					ESPIONAGE_ADVISOR : espionageAdvisor,
					DAN_QUAYLE_SCREEN : danQuayleScreen,

#FfH: Added by Talchas 05/19/2007
					101:trophyHall,
#FfH: End Add

					PEDIA_MAIN : pediaMainScreen,
					PEDIA_TECH : pediaMainScreen,
					PEDIA_UNIT : pediaMainScreen,
					PEDIA_BUILDING : pediaMainScreen,
					PEDIA_PROMOTION : pediaMainScreen,
					PEDIA_PROJECT : pediaMainScreen,
					PEDIA_UNIT_CHART : pediaMainScreen,
					PEDIA_BONUS : pediaMainScreen,
					PEDIA_IMPROVEMENT : pediaMainScreen,
					PEDIA_TERRAIN : pediaMainScreen,
					PEDIA_FEATURE : pediaMainScreen,
					PEDIA_CIVIC : pediaMainScreen,
					PEDIA_CIVILIZATION : pediaMainScreen,
					PEDIA_LEADER : pediaMainScreen,
					PEDIA_RELIGION : pediaMainScreen,
#					PEDIA_CORPORATION : pediaMainScreen,
					PEDIA_HISTORY : pediaMainScreen,
					WORLDBUILDER_SCREEN : worldBuilderScreen,

					DEBUG_INFO_SCREEN : debugInfoScreen,

				# add new screens here
					PEDIA_SPELL : pediaMainScreen,
					#RevolutionDCM
					REVOLUTION_WATCH_ADVISOR : revolutionWatchAdvisor,

## World Builder ##
					WB_BUILDING : WBBuildingScreen.WBBuildingScreen(),
					WB_TECH : WBTechScreen.WBTechScreen(),
					WB_PROMOTION : WBPromotionScreen.WBPromotionScreen(),
					WB_CORPORATION : WBCorporationScreen.WBCorporationScreen(),
					WB_BONUS : WBBonusScreen.WBBonusScreen(),
					WB_PROJECT : WBProjectScreen.WBProjectScreen(),
					WB_SPECIALIST : WBSpecialistScreen.WBSpecialistScreen(),
					WB_DIPLOMACY : WBDiplomacyScreen.WBDiplomacyScreen(),
## World Builder ##
				}

#######################################################################################
## Handle Navigation Map
#######################################################################################
HandleNavigationMap = {
					MAIN_INTERFACE : mainInterface,
					PEDIA_MAIN : pediaMainScreen,
					PEDIA_TECH : pediaMainScreen,
					PEDIA_UNIT : pediaMainScreen,
					PEDIA_BUILDING : pediaMainScreen,
					PEDIA_PROMOTION : pediaMainScreen,
					PEDIA_PROJECT : pediaMainScreen,
					PEDIA_UNIT_CHART : pediaMainScreen,
					PEDIA_BONUS : pediaMainScreen,
					PEDIA_IMPROVEMENT : pediaMainScreen,
					PEDIA_TERRAIN : pediaMainScreen,
					PEDIA_FEATURE : pediaMainScreen,
					PEDIA_CIVIC : pediaMainScreen,
					PEDIA_CIVILIZATION : pediaMainScreen,
					PEDIA_LEADER : pediaMainScreen,
					PEDIA_HISTORY : pediaMainScreen,
					PEDIA_RELIGION : pediaMainScreen,
#					PEDIA_CORPORATION : pediaMainScreen,

				# add new screens here
					PEDIA_SPELL : pediaMainScreen
				}
# BUG - Options - start
def init():
	createDomesticAdvisor()
	createFinanceAdvisor()
	createMilitaryAdvisor()
	createCivilopedia()
	createTechSplash()
# BUG - Options - end

# RevolutionDCM
	createRevolutionWatchAdvisor()
