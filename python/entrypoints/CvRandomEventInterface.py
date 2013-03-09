# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvRandomEventInterface.py
#
# These functions are App Entry Points from C++
# WARNING: These function names should not be changed
# WARNING: These functions can not be placed into a class
#
# No other modules should import this
#
import CvUtil
from CvPythonExtensions import *
import CustomFunctions
import PyHelpers

# lfgr start
import BugUtil

LOG_DEBUG = True
# lfgr end

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

def canTriggerAeronsChosen(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	if pUnit.getLevel() < 5:
		return False
	return True

def canTriggerAmuriteTrialUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isHiddenNationality() :
		return False
	return True

def applyAmuriteTrial1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_AMURITES'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pCity = pPlayer2.getCapitalCity()
		pUnit.setXY(pCity.getX(), pCity.getY(), false, true, true)

def doArmageddonApocalypse(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	iPercent = gc.getDefineINT('APOCALYPSE_KILL_CHANCE')
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')) == False:
		for pyCity in PyPlayer(iPlayer).getCityList():
			pCity = pyCity.GetCy()
			iPop = pCity.getPopulation()
			iPop = int(iPop / 2)
			if iPop == 0:
				iPop = 1
			pCity.setPopulation(iPop)
	pyPlayer = PyPlayer(iPlayer)
	apUnitList = pyPlayer.getUnitList()
	for pUnit in apUnitList:
		if (CyGame().getSorenRandNum(100, "Apocalypse") <= iPercent):
			if pUnit.isAlive():
				pUnit.kill(False, PlayerTypes.NO_PLAYER)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_APOCALYPSE_KILLED", ()),'',1,'Art/Interface/Buttons/Apocalypse.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
	if pPlayer.isHuman():
		t = "TROPHY_FEAT_APOCALYPSE"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def doArmageddonArs(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_ARS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonBlight(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	pPlayer = gc.getPlayer(iPlayer)
	py = PyPlayer(iPlayer)
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		for pyCity in py.getCityList():
			pCity = pyCity.GetCy()
			i = CyGame().getSorenRandNum(15, "Blight")
#			i = 10
			i += pCity.getPopulation()
			i -= pCity.totalGoodBuildingHealth()
			if i > 0:
				pCity.changeEspionageHealthCounter(i)
	for pUnit in py.getUnitList():
		if pUnit.isAlive():
			pUnit.doDamageNoCaster(25, 100, gc.getInfoTypeForString('DAMAGE_DEATH'), false)

def doArmageddonBuboes(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_BUBOES')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonHellfire(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	if iPlayer == 0:
		iChampion = gc.getInfoTypeForString('UNIT_CHAMPION')
		iDemon = gc.getInfoTypeForString('PROMOTION_DEMON')
		iHellfire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')
		iHellfireChance = gc.getDefineINT('HELLFIRE_CHANCE')
		pPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if (pPlayer2.isAlive()):
				if pPlayer2.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
					pPlayer = pPlayer2
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if not pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					if not pPlot.isCity():
						if pPlot.isFlatlands():
							if pPlot.getBonusType(-1) == -1:
								if CyGame().getSorenRandNum(10000, "Hellfire") <= iHellfireChance:
									iImprovement = pPlot.getImprovementType()
									bValid = True
									if iImprovement != -1 :
										if gc.getImprovementInfo(iImprovement).isPermanent():
											bValid = False
									if bValid :
										pPlot.setImprovementType(iHellfire)
										newUnit = pPlayer.initUnit(iChampion, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.setHasPromotion(iDemon, True)

def doArmageddonPestilence(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		for pyCity in PyPlayer(iPlayer).getCityList() :
			pCity = pyCity.GetCy()
			i = CyGame().getSorenRandNum(9, "Pestilence")
			i += (pCity.getPopulation() / 4)
			i -= pCity.totalGoodBuildingHealth()
			pCity.changeEspionageHealthCounter(i)
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		if pUnit.isAlive():
			pUnit.doDamageNoCaster(25, 100, gc.getInfoTypeForString('DAMAGE_DEATH'), false)

def doArmageddonStephanos(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_STEPHANOS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonWrath(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	iEnraged = gc.getInfoTypeForString('PROMOTION_ENRAGED')
	iUnit = gc.getInfoTypeForString('UNIT_WRATH')
	iLand = gc.getInfoTypeForString('DOMAIN_LAND')
	iWrathConvertChance = gc.getDefineINT('WRATH_CONVERT_CHANCE')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)
	pPlayer = gc.getPlayer(iPlayer)
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		if pUnit.getDomainType() == iLand:
			if pUnit.isAlive():
				if CyGame().getSorenRandNum(100, "Wrath") < iWrathConvertChance:
					if isWorldUnitClass(pUnit.getUnitClassType()) == False:
						pUnit.setHasPromotion(iEnraged, True)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WRATH_ENRAGED", ()),'',1,'Art/Interface/Buttons/Promotions/Enraged.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)

def doArmageddonYersinia(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_YERSINIA')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doAzer(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AZER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doBanditNietz3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HORSEMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName("Nietz the Bandit Lord")
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)

def helpBanditNietz3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_BANDIT_NIETZ_3_HELP", ())
	return szHelp

def doCalabimSanctuary1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-4)

def canTriggerCityFeud(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return False
	return True

def doCityFeudArson(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCapitalCity()
	cf.doCityFire(pCity)

def doCityFeudStart1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCapitalCity = pPlayer.getCapitalCity()
	pCapitalCity.changeHappinessTimer(5)

def doCityFeudStart3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCapitalCity = pPlayer.getCapitalCity()
	pCapitalCity.changeOccupationTimer(5)

def helpCityFeudStart1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCapitalCity()
	szHelp = localText.getText("TXT_KEY_EVENT_CITY_FEUD_START_1_HELP", (pCity.getName(), ))
	return szHelp

def helpCityFeudStart3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCapitalCity()
	szHelp = localText.getText("TXT_KEY_EVENT_CITY_FEUD_START_3_HELP", (pCity.getName(), ))
	return szHelp

def canTriggerCitySplit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return False
	if pPlayer.getOpenPlayer() == -1:
		return False
	if CyGame().getWBMapScript():
		return False
	if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_BARBARIAN')):
		return False
	iKoun = gc.getInfoTypeForString('LEADER_KOUN')
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iPlayer)
		if pLoopPlayer.getLeaderType() == iKoun:
			return False
	return True

def doCitySplit1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pSplitPlayer = cf.formEmpire(pPlayer.getCivilizationType(), gc.getInfoTypeForString('LEADER_KOUN'), TeamTypes.NO_TEAM, pCity, pPlayer.getAlignment(), pPlayer)
	pSplitPlayer.setParent(kTriggeredData.ePlayer)

def doSoverignCity1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	cf.formEmpire(pPlayer.getCivilizationType(), gc.getInfoTypeForString('LEADER_KOUN'), pPlayer.getTeam(), pCity, pPlayer.getAlignment(), pPlayer)

def doDissent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if gc.getGame().getSorenRandNum(100, "Dissent 1") < 50:
		pCity.changeOccupationTimer(2)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_1", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

def helpDissent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DISSENT_1_HELP", ())
	return szHelp

def doDissent2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if gc.getGame().getSorenRandNum(100, "Dissent 2") < 50:
		pCity.changeOccupationTimer(4)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_2_BAD", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	else:
		pCity.changeHappinessTimer(5)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_2_GOOD", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

def helpDissent2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DISSENT_2_HELP", ())
	return szHelp

def canApplyDissent4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) != gc.getInfoTypeForString('CIVIC_SOCIAL_ORDER'):
		return False
	return True

def applyExploreLairDepths1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iRnd = CyGame().getSorenRandNum(100, "Explore Lair")
	if iRnd < 50:
		cf.exploreLairBigBad(pUnit)
	if iRnd >= 50:
		cf.exploreLairBigGood(pUnit)

def applyExploreLairDwarfVsLizardmen1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	bBronze = False
	bPoison = False
	if bPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
		bBronze = True
	if bPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
		bPoison = True
	pPlot = pUnit.plot()
	pNewPlot = cf.findClearPlot(-1, pPlot)
	if pNewPlot != -1:
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit3 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bPoison:
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
			newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
			newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
		newUnit4 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		newUnit5 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		if bBronze:
			newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
			newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)

def applyExploreLairDwarfVsLizardmen2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	bBronze = False
	bPoison = False
	if bPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
		bBronze = True
	if bPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
		bPoison = True
	pPlot = pUnit.plot()
	pNewPlot = cf.findClearPlot(-1, pPlot)
	if pNewPlot != -1:
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bPoison:
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
			newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED_BLADE'), True)
		newUnit3 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		newUnit4 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		newUnit5 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
		if bBronze:
			newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
			newUnit4.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)
			newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), True)

def applyExploreLairPortal1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iBestValue = 0
	pBestPlot = -1
	for i in range (CyMap().numPlots()):
		iValue = 0
		pPlot = CyMap().plotByIndex(i)
		if not pPlot.isWater():
			if not pPlot.isPeak():
				if pPlot.getNumUnits() == 0:
					iValue = CyGame().getSorenRandNum(1000, "Portal")
					if not pPlot.isOwned():
						iValue += 1000
					if iValue > iBestValue:
						iBestValue = iValue
						pBestPlot = pPlot
	if pBestPlot != -1:
		pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), false, true, true)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_PORTAL",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pBestPlot.getX(),pBestPlot.getY(),True,True)

def doFlareEntropyNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL1'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_DEFILE",point.x,point.y,point.z)
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				pPlot.changePlotCounter(100)
	CyGame().changeGlobalCounter(2)

def doFlareFireNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_ARTILLERY_SHELL_EXPLODE'),point)
	CyAudioGame().Play3DSound("AS3D_UN_GRENADE_EXPLODE",point.x,point.y,point.z)
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iForest = gc.getInfoTypeForString('FEATURE_FOREST')
	iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iJungle):
					pPlot.setFeatureType(iFlames, 0)
					if pPlot.isOwned():
						CyInterface().addMessage(pPlot.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FLAMES", ()),'',1,'Art/Interface/Buttons/Fire.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

def doFlareLifeNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL1'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_SANCTIFY",point.x,point.y,point.z)
	for iX in range(kTriggeredData.iPlotX-2, kTriggeredData.iPlotX+3, 1):
		for iY in range(kTriggeredData.iPlotY-2, kTriggeredData.iPlotY+3, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				pPlot.changePlotCounter(-100)
	CyGame().changeGlobalCounter(-2)

def doFlareNatureNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_BLOOM'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_BLOOM",point.x,point.y,point.z)
	iForestNew = gc.getInfoTypeForString('FEATURE_FOREST_NEW')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				if (pPlot.getImprovementType() == -1 and pPlot.getFeatureType() == -1 and pPlot.isWater() == False):
					if not pPlot.isPeak():
						pPlot.setFeatureType(iForestNew, 0)

def doFlareWaterNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPRING'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				if pPlot.getTerrainType() == iDesert:
					pPlot.setTerrainType(iPlains,True,True)
				if pPlot.getFeatureType() == iFlames:
					pPlot.setFeatureType(-1, -1)
				if pPlot.getImprovementType() == iSmoke:
					pPlot.setImprovementType(-1)

def canTriggerPlotEmpty(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	# lfgr bugfix
	if pPlot.isCity() :
		return False
	# lfgr end
	return True

def canTriggerFoodSicknessUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if not pUnit.isAlive():
		return False
	return True

def doFoodSickness(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iDmg = pUnit.getDamage() + 20
	if iDmg > 99:
		iDmg = 99
	pUnit.setDamage(iDmg, PlayerTypes.NO_PLAYER)
	pUnit.changeImmobileTimer(2)

def doFrostling(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_FROSTLING'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doGodslayer(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	cf.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_GODSLAYER'))

def doGovernorAssassination(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	bMatch = False
	iCivic = pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT'))
	if iCivic != gc.getInfoTypeForString('CIVIC_DESPOTISM'):
		if iCivic == gc.getInfoTypeForString('CIVIC_GOD_KING'):
			bMatch = True
		if iCivic == gc.getInfoTypeForString('CIVIC_ARISTOCRACY'):
			if iEvent == gc.getInfoTypeForString('EVENT_GOVERNOR_ASSASSINATION_1'):
				bMatch = True
		if iCivic == gc.getInfoTypeForString('CIVIC_CITY_STATES') or iCivic == gc.getInfoTypeForString('CIVIC_REPUBLIC'):
			if iEvent == gc.getInfoTypeForString('EVENT_GOVERNOR_ASSASSINATION_3'):
				bMatch = True
		if iCivic == gc.getInfoTypeForString('CIVIC_THEOCRACY'):
			if iEvent == gc.getInfoTypeForString('EVENT_GOVERNOR_ASSASSINATION_4'):
				bMatch = True
		if bMatch == True:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PEOPLE_APPROVE", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			pCity.changeHappinessTimer(3)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_WRONG", ()),'',1,'Art/Interface/Buttons/General/unhealthy_person.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
			pCity.changeHurryAngerTimer(3)

def doGuildOfTheNineMerc41(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MERCENARY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WOODSMAN1'), True)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEXTEROUS'), True)
	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RANGER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SINISTER'), True)

def canTriggerGuildOfTheNineMerc5(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCoastal(10) == False:
		return False
	return True

def doGuildOfTheNineMerc51(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MERCENARY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AMPHIBIOUS'), True)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_BOARDING_PARTY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIVATEER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)

def doGuildOfTheNineMerc61(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MERCENARY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MUTATED'), True)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_TASKMASTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setUnitArtStyleType(gc.getInfoTypeForString('UNIT_ARTSTYLE_BALSERAPHS'))

def doGuildOfTheNineMerc71(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MERCENARY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEFENSIVE'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DWARF'), True)
	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DWARVEN_CANNON'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doGuildOfTheNineMerc81(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MERCENARY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_OGRE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LIZARDMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doGreatBeastGurid(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_GURID')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doGreatBeastLeviathan(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_LEVIATHAN')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		pBestPlot = -1
		iBestPlot = -1
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					iPlot = CyGame().getSorenRandNum(500, "Leviathan")
					iPlot = iPlot + (pPlot.area().getNumTiles() * 10)
			if iPlot > iBestPlot:
				iBestPlot = iPlot
				pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doGreatBeastMargalard(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_MARGALARD')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def applyHyboremsWhisper1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = cf.getAshenVeilCity(1)
	pPlayer.acquireCity(pCity,false,false)

def helpHyboremsWhisper1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pCity = cf.getAshenVeilCity(1)
	szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	return szHelp

def applyHyboremsWhisper2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = cf.getAshenVeilCity(2)
	pPlayer.acquireCity(pCity,false,false)

def helpHyboremsWhisper2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pCity = cf.getAshenVeilCity(2)
	szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	return szHelp

def applyHyboremsWhisper3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = cf.getAshenVeilCity(3)
	pPlayer.acquireCity(pCity,false,false)

def helpHyboremsWhisper3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pCity = cf.getAshenVeilCity(3)
	szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	return szHelp

def applyIronOrb3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	szBuffer = localText.getText("TXT_KEY_EVENT_IRON_ORB_3_RESULT", ())
	pPlayer.chooseTech(1, szBuffer, True)

def doJudgementRight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_RIGHT", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	pCity.changeHappinessTimer(10)

def doJudgementWrong(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_WRONG", ()),'',1,'Art/Interface/Buttons/General/unhealthy_person.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	pCity.changeCrime(3)

def doLetumFrigus3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE'),True)

def helpLetumFrigus3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_LETUM_FRIGUS_3_HELP", ())
	return szHelp

def canTriggerLunaticCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	iReligion = pPlayer.getStateReligion()
	iTemple = -1
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')
	if iReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')
	if iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')
	if iReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
		iTemple = gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')
	if iTemple == -1:
		return False
	if pCity.getNumRealBuilding(iTemple) == 0:
		return False
	return True

def doMachineParts1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CLOCKWORK_GOLEM'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

def doMachineParts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CLOCKWORK_GOLEM'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)

def applyMalakimPilgrimage1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_MALAKIM'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pCity = pPlayer2.getCapitalCity()
		pUnit.setXY(pCity.getX(), pCity.getY(), false, true, true)

def doMarketTheft2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iRnd = gc.getGame().getSorenRandNum(21, "Market Theft 2") - 10
	pCity.changeCrime(iRnd)

def helpMarketTheft2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	szHelp = localText.getText("TXT_KEY_EVENT_MARKET_THEFT_2_HELP", ())
	return szHelp

def canTriggerMerchantKeep(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_MERCHANT')) == 0:
		return False
	return True

def doMistforms(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iMistform = gc.getInfoTypeForString('UNIT_MISTFORM')
	newUnit1 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doMushrooms(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setBonusType(gc.getInfoTypeForString('BONUS_MUSHROOMS'))

def canTriggerMutateUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	iMutated = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_MUTATED')
	if pUnit.isHasPromotion(iMutated):
		return False
	return True

def canApplyNoOrder(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
		return False
	return True

def doOrderVsVeil1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 1") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	(loopCity, iter) = pPlayer.firstCity(false)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, false)

def doOrderVsVeil2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 2") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	(loopCity, iter) = pPlayer.firstCity(false)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, false)

def doOrderVsVeil3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 25:
			pCity.setHasReligion(iVeil, False, False, False)
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 25:
			pCity.setHasReligion(iOrder, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 50:
		pCity.changePopulation(-1)

def canApplyOrderVsVeil4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DUNGEON')) == 0:
		return False
	return True

def helpOrderVsVeil1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_1_HELP", ())
	return szHelp

def helpOrderVsVeil2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_2_HELP", ())
	return szHelp

def helpOrderVsVeil3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_3_HELP", ())
	return szHelp

def doOrderVsVeilTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), 0)
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 1") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = player.nextCity(iter, false)

def doOrderVsVeilTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'), 0)
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
		pCity.changePopulation(-1)

def doOrderVsVeilTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	(loopCity, iter) = pPlayer.firstCity(false)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, false)

def helpOrderVsVeilTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_1_HELP", ())
	return szHelp

def helpOrderVsVeilTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_2_HELP", ())
	return szHelp

def helpOrderVsVeilTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_3_HELP", ())
	return szHelp

# lfgr added
def canTriggerOvercouncil(argsList):
	return semiRandomTurnTrigger( 10, 0.25 )
# lfgr end

def canTriggerParith(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if not pPlayer.isHuman():
		return False
	if CyGame().getTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH") != 1:
		return False
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
		return False
	return True

def applyParithYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = player.getUnit(kTriggeredData.iUnitId)
	CyGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", pUnit.getUnitType())

def canTriggerPenguins(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isAdjacentToWater() == False:
		return False
	if pPlot.isPeak():
		return False
	return True

def doPenguins(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setBonusType(gc.getInfoTypeForString('BONUS_PENGUINS'))

def canTriggerPickAlignment(argsList):
	kTriggeredData = argsList[0]
	if CyGame().getWBMapScript():
		return False
	return True

def doPickAlignment1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_GOOD'))

def doPickAlignment2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_NEUTRAL'))

def doPickAlignment3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))

def doPigGiant3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = cf.findClearPlot(-1, pCity.plot())
	if pPlot != -1:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)

def applyPronCapria(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_CAPRIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_CAPRIA_POPUP",()), iPlayer)

def canTriggerPronCapria(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_CAPRIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronEthne(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ETHNE'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ETHNE_POPUP",()), iPlayer)

def canTriggerPronEthne(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ETHNE'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronArendel(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ARENDEL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ARENDEL_POPUP",()), iPlayer)

def canTriggerPronArendel(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ARENDEL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronThessa(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_THESSA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_THESSA_POPUP",()), iPlayer)

def canTriggerPronThessa(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_THESSA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronHannah(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_HANNAH'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_HANNAH_POPUP",()), iPlayer)

def canTriggerPronHannah(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_HANNAH'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronRhoanna(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_RHOANNA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_RHOANNA_POPUP",()), iPlayer)

def canTriggerPronRhoanna(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_RHOANNA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronValledia(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_VALLEDIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_VALLEDIA_POPUP",()), iPlayer)

def canTriggerPronValledia(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_VALLEDIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronMahala(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_MAHALA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_MAHALA_POPUP",()), iPlayer)

def canTriggerPronMahala(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_MAHALA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronKeelyn(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_KEELYN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_KEELYN_POPUP",()), iPlayer)

def canTriggerPronKeelyn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_KEELYN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronSheelba(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_SHEELBA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_SHEELBA_POPUP",()), iPlayer)

def canTriggerPronSheelba(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_SHEELBA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronFaeryl(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_FAERYL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_FAERYL_POPUP",()), iPlayer)

def canTriggerPronFaeryl(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_FAERYL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronAlexis(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ALEXIS'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		cf.addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ALEXIS_POPUP",()), iPlayer)

def canTriggerPronAlexis(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iLeader = cf.getLeader(gc.getInfoTypeForString('LEADER_ALEXIS'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if eTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == gc.getInfoTypeForString('ATTITUDE_FRIENDLY'):
				return True
	return False

def canTriggerUniqueFeatureAifonIsle(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureBradelinesWell(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureBrokenSepulcher(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureGuardian(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_GUARDIAN')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureLetumFrigus(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureLetumFrigusIllians(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeaturePyreOfTheSeraphic(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
		return False
	iImp = gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerSageKeep(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_SCIENTIST')) == 0:
		return False
	return True

def doSailorsDirge(argsList):
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_SAILORS_DIRGE')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		pBestPlot = -1
		iBestPlot = -1
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					iPlot = CyGame().getSorenRandNum(500, "Sailors Dirge")
					iPlot = iPlot + (pPlot.area().getNumTiles() * 10)
					if pPlot.isOwned():
						iPlot = iPlot / 2
					if iPlot > iBestPlot:
						iBestPlot = iPlot
						pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			iSkeleton = gc.getInfoTypeForString('UNIT_SKELETON')
			bPlayer.initUnit(iSkeleton, newUnit.getX(), newUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			bPlayer.initUnit(iSkeleton, newUnit.getX(), newUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			bPlayer.initUnit(iSkeleton, newUnit.getX(), newUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doSailorsDirgeDefeated(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	cf.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_TREASURE'))

def applyShrineCamulos2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Shrine Camulos") < 10:
		pPlot = cf.findClearPlot(-1, pCity.plot())
		if pPlot != -1:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SHRINE_CAMULOS",()),'',1,'Art/Interface/Buttons/Units/Pit Beast.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
			newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PIT_BEAST'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.attack(pCity.plot(), False)

def doSignAeron(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeGlobalCounter(3)

def doSignBhall(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == -1:
				if pPlot.getImprovementType() == -1:
					if pPlot.isWater() == False:
						if CyGame().getSorenRandNum(100, "SignBhall") < 10:
							iTerrain = pPlot.getTerrainType()
							if iTerrain == iSnow:
								pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iTundra:
								pPlot.setTempTerrainType(iGrass, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iGrass:
								pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iPlains:
								pPlot.setTempTerrainType(iDesert, CyGame().getSorenRandNum(10, "Bob") + 10)

def doSignCamulos(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				loopPlayer.AI_changeAttitudeExtra(iPlayer, -1)
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, -1)

def doSignDagda(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				loopPlayer.AI_changeAttitudeExtra(iPlayer, 1)
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 1)

def doSignEsus(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeCrime(5)

def doSignLugus(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeCrime(-5)

def doSignMulcarn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == -1:
				if pPlot.getImprovementType() == -1:
					if pPlot.isWater() == False:
						if CyGame().getSorenRandNum(100, "SignMulcarn") < 10:
							iTerrain = pPlot.getTerrainType()
							if iTerrain == iTundra:
								pPlot.setTempTerrainType(iSnow, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iGrass:
								pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iPlains:
								pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iDesert:
								pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(10, "Bob") + 10)

def doSignSirona(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeGlobalCounter(-3)

def doSignSucellus(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iDiseased = gc.getInfoTypeForString('PROMOTION_DISEASED')
	apUnitList = PyPlayer(iPlayer).getUnitList()
	for pUnit in apUnitList:
		if pUnit.isHasPromotion(iDiseased):
			pUnit.setHasPromotion(iDiseased, False)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_DISEASED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Spells/Curedisease.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
		if pUnit.getDamage() > 0:
			pUnit.setDamage(pUnit.getDamage() / 2, PlayerTypes.NO_PLAYER)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_HEALED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Spells/Heal.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def doSignTali(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iSpring = gc.getInfoTypeForString('EFFECT_SPRING')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == iFlames:
				point = pPlot.getPoint()
				CyEngine().triggerEffect(iSpring,point)
				CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
				pPlot.setFeatureType(-1, 0)
			if pPlot.getImprovementType() == iSmoke:
				point = pPlot.getPoint()
				CyEngine().triggerEffect(iSpring,point)
				CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
				pPlot.setImprovementType(-1)

def canTriggerSmugglers(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_SMUGGLERS_PORT')) > 0:
		return False
	if pCity.isCoastal(10) == False:
		return False
	return True

def doSpiderMine3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GIANT_SPIDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)

def applyTreasure1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	cf.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_TREASURE'))

def canTriggerSwitchCivs(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if pPlayer.isHuman() == False:
		return False
	if CyGame().getRankPlayer(0) != kTriggeredData.ePlayer:
		return False
	if CyGame().getGameTurn() < 20:
		return False
	if gc.getTeam(otherPlayer.getTeam()).isAVassal():
		return False
	if CyGame().getWBMapScript():
		return False
	return True

def doSwitchCivs2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iNewPlayer = kTriggeredData.eOtherPlayer
	iOldPlayer = kTriggeredData.ePlayer
	CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, -1)

def canTriggerTraitor(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if (pCity.happyLevel() - pCity.unhappyLevel(0)) < 0:
		return False
	return True
	
# lfgr added
def canTriggerUndercouncil(argsList):
	return semiRandomTurnTrigger( 9, 0.15 )
# lfgr end

def doVeilVsOrderTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER'), 0)
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Veil vs Order Temple 1") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	(loopCity, iter) = pPlayer.firstCity(false)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, false)

def doVeilVsOrderTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER'), 0)
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
		pCity.changePopulation(-1)

def doVeilVsOrderTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = gc.getInfoTypeForString('RELIGION_THE_ORDER')
	iVeil = gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')
	(loopCity, iter) = pPlayer.firstCity(false)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, false)

def helpVeilVsOrderTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_1_HELP", ())
	return szHelp

def helpVeilVsOrderTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_2_HELP", ())
	return szHelp

def helpVeilVsOrderTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_3_HELP", ())
	return szHelp

def doSlaveEscape(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.kill(False, -1)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_ESCAPE", ()),'',1,'Art/Interface/Buttons/Units/Slave.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def canTriggerSlaveRevoltUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	pPlot = pUnit.plot()
	if pPlot.getNumUnits() != 1:
		return False
	return True

def doSlaveRevolt(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iRace = pUnit.getRace()
	plot = pUnit.plot()
	pUnit.kill(False, -1)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	pNewUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WARRIOR'), plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
	if iRace != -1:
		pNewUnit.setHasPromotion(iRace, True)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_REVOLT", ()),'',1,'Art/Interface/Buttons/Units/Slave.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def canApplyTraitAggressive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_AGGRESSIVE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitAggressive(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_AGGRESSIVE'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitAggressive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE'),True)

#Extra leaders (Traits): Start (Terkhen)
def canApplyTraitAgrarian(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_AGRARIAN'):
		return False
	return True

def helpTraitAgrarian(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_AGRARIAN'), CivilizationTypes.NO_CIVILIZATION, false )

def doTraitAgrarian(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_AGRARIAN'),True)
#Extra leaders (Traits): End

def canApplyTraitArcane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_ARCANE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitArcane(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_ARCANE'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitArcane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_ARCANE'),True)

def canApplyTraitCharismatic(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_CHARISMATIC'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitCharismatic(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_CHARISMATIC'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitCharismatic(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_CHARISMATIC'),True)

def canApplyTraitCreative(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_CREATIVE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitCreative(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_CREATIVE'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitCreative(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_CREATIVE'),True)

def canApplyTraitExpansive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_EXPANSIVE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitExpansive(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_EXPANSIVE'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitExpansive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_EXPANSIVE'),True)

def canApplyTraitFinancial(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_FINANCIAL'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitFinancial(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_FINANCIAL'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitFinancial(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_FINANCIAL'),True)

#Extra leaders (Traits): Start (Terkhen)
def canApplyTraitImperialistic(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_IMPERIALISTIC'):
		return False
	return True

def helpTraitImperialistic(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_IMPERIALISTIC'), CivilizationTypes.NO_CIVILIZATION, false )

def doTraitImperialistic(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_IMPERIALISTIC'),True)
#Extra leaders (Traits): End

def canApplyTraitIndustrious(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitIndustrious(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitIndustrious(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'),True)

def doTraitInsane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCivilization = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iTraitCount = 0
	for i in range(gc.getNumTraitInfos()):
		if (pPlayer.hasTrait(i) and i != gc.getInfoTypeForString('TRAIT_INSANE')):
			if (i != pCivilization.getCivTrait()):
				pPlayer.setHasTrait(i, False)
				iTraitCount = iTraitCount + 1
				
	Traits = [ 'TRAIT_AGRARIAN','TRAIT_AGGRESSIVE','TRAIT_ARCANE','TRAIT_CHARISMATIC','TRAIT_CREATIVE','TRAIT_EXPANSIVE','TRAIT_FINANCIAL','TRAIT_IMPERIALISTIC','TRAIT_INDUSTRIOUS','TRAIT_ORGANIZED','TRAIT_PHILOSOPHICAL','TRAIT_RAIDERS','TRAIT_SAGE','TRAIT_SAVAGE','TRAIT_SLAVER','TRAIT_SPIRITUAL' ]

	if (iTraitCount > 0):
		iRnd1 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 1")
		pPlayer.setHasTrait(gc.getInfoTypeForString(Traits[iRnd1]),True)
	if (iTraitCount > 1):
		iRnd2 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 2")
		while iRnd2 == iRnd1:
			iRnd2 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 2 - retry")
		pPlayer.setHasTrait(gc.getInfoTypeForString(Traits[iRnd2]),True)
	if (iTraitCount > 2):
		iRnd3 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 3")
		while iRnd3 == iRnd1 or iRnd3 == iRnd2:
			iRnd3 = CyGame().getSorenRandNum(len(Traits), "Insane Trait 3 - retry")
		pPlayer.setHasTrait(gc.getInfoTypeForString(Traits[iRnd3]),True)

# code from MagisterMod
	iRnd = (CyGame().getSorenRandNum(6, "Insane Attitude Change") - 3)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, iRnd)



def canApplyTraitOrganized(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_ORGANIZED'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitOrganized(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_ORGANIZED'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitOrganized(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_ORGANIZED'),True)

def canApplyTraitPhilosophical(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitPhilosophical(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitPhilosophical(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'),True)

def canApplyTraitRaiders(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_RAIDERS'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitRaiders(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_RAIDERS'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitRaiders(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_RAIDERS'),True)

#Extra leaders (Traits): Start (Terkhen)
def canApplyTraitSage(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_SAGE'):
		return False
	return True

def helpTraitSage(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_SAGE'), CivilizationTypes.NO_CIVILIZATION, false )

def doTraitSage(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_SAGE'),True)
#Extra leaders (Traits): End

#Extra leaders (Traits): Start (Terkhen)
def canApplyTraitSlaver(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_SLAVER'):
		return False
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
		return False
	return True

def helpTraitSlaver(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_SLAVER'), CivilizationTypes.NO_CIVILIZATION, false )

def doTraitSlaver(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait,False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_SLAVER'),True)
#Extra leaders (Traits): End

def canApplyTraitSpiritual(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_SPIRITUAL'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitSpiritual(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_SPIRITUAL'), CivilizationTypes.NO_CIVILIZATION, false )
# lfgr end

def doTraitSpiritual(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			if (gc.getTraitInfo(iTrait).isSelectable()):
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					pPlayer.setHasTrait(iTrait, False)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_SPIRITUAL'),True)

def doVolcanoCreation(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
	pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_VOLCANO'), 0)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_ARTILLERY_SHELL_EXPLODE'),point)
	CyAudioGame().Play3DSound("AS3D_UN_GRENADE_EXPLODE",point.x,point.y,point.z)
# FlavourMod: Idea nicked from Rystic's TweakMod by Jean Elcard 11/08/2009
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	sFlammables = ['FOREST', 'FOREST_NEW', 'FOREST_ANCIENT', 'JUNGLE', 'SCRUB']
	iFlammables = [gc.getInfoTypeForString('FEATURE_' + sFeature) for sFeature in sFlammables]
	for iDirection in range(DirectionTypes.NUM_DIRECTION_TYPES):
		pAdjacentPlot = plotDirection(pPlot.getX(), pPlot.getY(), DirectionTypes(iDirection))
		if pAdjacentPlot.getFeatureType() in iFlammables:
			iRandom = CyGame().getSorenRandNum(100, "FlavourMod: doVolcanoCreation")
			if iRandom < 30:
				pAdjacentPlot.setFeatureType(iFlames, -1)
			elif iRandom < 60:
				pAdjacentPlot.setImprovementType(iSmoke)
# FlavourMod: End Pilferage

def canTriggerWarGamesUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isAlive() == False:
		return False
	if pUnit.isOnlyDefensive():
		return False
	return True

def applyWBFallOfCuantineRosier1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_FALL_OF_CUANTINE_ROSIER_ALLY", 0)

def applyWBFallOfCuantineRosier2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_FALL_OF_CUANTINE_ROSIER_ALLY", 1)

def applyWBFallOfCuantineFleeCalabim(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_CIV_DECIUS", gc.getInfoTypeForString('CIVILIZATION_CALABIM'))

def applyWBFallOfCuantineFleeMalakim(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_CIV_DECIUS", gc.getInfoTypeForString('CIVILIZATION_MALAKIM'))

def applyWBGiftOfKylorinMeshabberRight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = CyMap().plot(19,16)
	pPlot.setPythonActive(False)
	pPlot = CyMap().plot(20,16)
	pUnit = pPlot.getUnit(0)
	pUnit.kill(True, 0)
	cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_MESHABBER_RIGHT",()),'art/interface/popups/Tya.dds')

def applyWBGiftOfKylorinMeshabberWrong(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot1 = CyMap().plot(19,16)
	pPlot1.setPythonActive(False)
	pPlot2 = CyMap().plot(20,16)
	pUnit = pPlot2.getUnit(0)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), False)
	pUnit.attack(pPlot1, False)
	cf.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_MESHABBER_WRONG",()),'art/interface/popups/Tya.dds')

def applyWBGiftOfKylorinSecretDoorYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = CyMap().plot(23,6)
	pPlot.setPythonActive(False)
	pPlot = CyMap().plot(23,5)
	pPlot.setFeatureType(-1, -1)

def applyWBLordOfTheBalorsTemptJudeccaYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	enemyTeam = otherPlayer.getTeam()
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(enemyTeam, False)
	eTeam.setPermanentWarPeace(6, False)
	eTeam.makePeace(6)
	eTeam.declareWar(enemyTeam, true, WarPlanTypes.WARPLAN_TOTAL)
	eTeam.setPermanentWarPeace(enemyTeam, True)
	eTeam.setPermanentWarPeace(6, True)

def applyWBLordOfTheBalorsTemptSallosYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(7, False)
	eTeam.makePeace(7)
	eTeam.setPermanentWarPeace(7, True)

def applyWBLordOfTheBalorsTemptOuzzaYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(8, False)
	eTeam.makePeace(8)
	eTeam.setPermanentWarPeace(8, True)
	for pyCity in PyPlayer(iPlayer).getCityList():
		pCity = pyCity.GetCy()
		if pCity.getPopulation() > 1:
			pCity.changePopulation(-1)

def applyWBLordOfTheBalorsTemptMeresinYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(9, False)
	eTeam.makePeace(9)
	eTeam.setPermanentWarPeace(9, True)

def applyWBLordOfTheBalorsTemptStatiusYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(10, False)
	eTeam.makePeace(10)
	eTeam.setPermanentWarPeace(10, True)
	pPlayer = gc.getPlayer(10)
	pPlayer.acquireCity(pCity,false,false)

def applyWBLordOfTheBalorsTemptLetheYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.setPermanentWarPeace(11, False)
	eTeam.makePeace(11)
	eTeam.setPermanentWarPeace(11, True)
	pUnit.kill(True, 0)

def applyWBSplinteredCourtDefeatedAmelanchier3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iDovielloTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_AMELANCHIER", gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				iDovielloTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iDovielloTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		eTeam = gc.getTeam(iDovielloTeam)
		if eTeam.isAtWar(iSvartalfarTeam):
			eTeam.makePeace(iSvartalfarTeam)
		if not eTeam.isAtWar(iLjosalfarTeam):
			eTeam.declareWar(iLjosalfarTeam, false, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedThessa3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iCalabimTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_THESSA", gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				iCalabimTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iCalabimTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		eTeam = gc.getTeam(iCalabimTeam)
		if eTeam.isAtWar(iSvartalfarTeam):
			eTeam.makePeace(iSvartalfarTeam)
		if not eTeam.isAtWar(iLjosalfarTeam):
			eTeam.declareWar(iLjosalfarTeam, false, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedRivanna3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iCalabimTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_RIVANNA", gc.getInfoTypeForString('CIVILIZATION_CALABIM'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				iCalabimTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iCalabimTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		eTeam = gc.getTeam(iCalabimTeam)
		if eTeam.isAtWar(iLjosalfarTeam):
			eTeam.makePeace(iLjosalfarTeam)
		if not eTeam.isAtWar(iSvartalfarTeam):
			eTeam.declareWar(iSvartalfarTeam, false, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedVolanna3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iDovielloTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_VOLANNA", gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				iDovielloTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iDovielloTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		eTeam = gc.getTeam(iDovielloTeam)
		if eTeam.isAtWar(iLjosalfarTeam):
			eTeam.makePeace(iLjosalfarTeam)
		if not eTeam.isAtWar(iSvartalfarTeam):
			eTeam.declareWar(iSvartalfarTeam, false, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtParithYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	CyGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", 1)

def canDoWBTheBlackTowerPickCivBannor(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_RADIANT_GUARD_CAPRIA_ALLY"):
		return True
	return False

def applyWBTheBlackTowerPickCivBannor(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_BANNOR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheBlackTowerPickCivHippus(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_HIPPUS'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheBlackTowerPickCivLanun(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_LANUN'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivLjosalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_SPLINTERED_COURT_LJOSALFAR"):
		return True
	return False

def applyWBTheBlackTowerPickCivLjosalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivLuchuirp(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_MOMUS_BEERI_ALLY"):
		return True
	return False

def applyWBTheBlackTowerPickCivLuchuirp(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivSvartalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR"):
		return True
	return False

def applyWBTheBlackTowerPickCivSvartalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheMomusBeerisOfferYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	gc.getGame().changeTrophyValue("TROPHY_WB_THE_MOMUS_BEERI_ALLY", 1)
	eTeam = gc.getTeam(0) #Falamar
	eTeam7 = gc.getTeam(7) #Beeri
	eTeam.setPermanentWarPeace(1, False)
	eTeam.setPermanentWarPeace(7, False)
	eTeam.declareWar(1, true, WarPlanTypes.WARPLAN_TOTAL)
	eTeam7.declareWar(1, true, WarPlanTypes.WARPLAN_TOTAL)
	eTeam.makePeace(7)
	eTeam.setPermanentWarPeace(1, True)
	eTeam.setPermanentWarPeace(7, True)

def applyWBTheRadiantGuardChooseSidesBasium(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY", 0)
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_BASIUM_ALLY", 1)

def applyWBTheRadiantGuardChooseSidesHyborem(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer

	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY", 1)
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_BASIUM_ALLY", 0)
	pPlayer = gc.getPlayer(1) #Basium
	pCity = pPlayer.getCapitalCity()
	apUnitList = PyPlayer(0).getUnitList()
	for pLoopUnit in apUnitList:
		if gc.getUnitInfo(pLoopUnit.getUnitType()).getReligionType() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
			szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ABANDON", (pLoopUnit.getName(), ))
			CyInterface().addMessage(0,True,25,szBuffer,'',1,gc.getUnitInfo(pLoopUnit.getUnitType()).getButton(),ColorTypes(7),pLoopUnit.getX(),pLoopUnit.getY(),True,True)
			newUnit = pPlayer.initUnit(pLoopUnit.getUnitType(), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pLoopUnit)
	eTeam = gc.getTeam(0) #Falamar
	eTeam.setPermanentWarPeace(1, False)
	eTeam.setPermanentWarPeace(2, False)
	eTeam.declareWar(1, true, WarPlanTypes.WARPLAN_TOTAL)
	eTeam.makePeace(2)
	eTeam.setPermanentWarPeace(1, True)
	eTeam.setPermanentWarPeace(2, True)

def doWerewolf1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = cf.findClearPlot(-1, pCity.plot())
	if pPlot != -1:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WEREWOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WEREWOLF_RELEASED", ()),'',1,'Art/Interface/Buttons/Units/Werewolf.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)

def doWerewolf3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WEREWOLF_KILLED", ()),'',1,'Art/Interface/Buttons/Units/Werewolf.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

######## BLESSED SEA ###########

def getHelpBlessedSea1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	map = gc.getMap()
	iOurMinLandmass = (3 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()) / 2
	
	szHelp = localText.getText("TXT_KEY_EVENT_BLESSED_SEA_HELP", (iOurMinLandmass, ))	

	return szHelp

def canTriggerBlessedSea(argsList):
	kTriggeredData = argsList[0]
	map = gc.getMap()
		
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	iMapMinLandmass = 2 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	iOurMaxLandmass = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers() / 2
	
	if (map.getNumLandAreas() < iMapMinLandmass):
		return false

	iOurLandmasses = 0
	for i in range(map.getIndexAfterLastArea()):
		area = map.getArea(i)
		if not area.isNone() and not area.isWater() and area.getCitiesPerPlayer(kTriggeredData.ePlayer) > 0:
			iOurLandmasses += 1
			
	if (iOurLandmasses > iOurMaxLandmass):
		return false

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.getUnitClassCount(CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_GALLEY')) == 0:
		if player.getUnitClassCount(CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CARAVEL')) == 0:
			if player.getUnitClassCount(CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_GALLEON')) == 0:
				return false
			
	return true

def canTriggerBlessedSea2(argsList):

	kTriggeredData = argsList[0]
	map = gc.getMap()
	iOurMinLandmass = (3 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()) / 2
	
	iOurLandmasses = 0
	for i in range(map.getIndexAfterLastArea()):
		area = map.getArea(i)
		if not area.isNone() and not area.isWater() and area.getCitiesPerPlayer(kTriggeredData.ePlayer) > 0:
			iOurLandmasses += 1
			
	if (iOurLandmasses < iOurMinLandmass):
		return false
	
	return true

def applyBlessedSea2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iBuilding = -1
	
	if (-1 != kTriggeredData.eReligion):
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo,gc.getNumSpecialBuildingInfos(),'SPECIALBUILDING_TEMPLE')):
				if (gc.getBuildingInfo(i).getReligionType() == kTriggeredData.eReligion):
					iBuilding = i
					break
		
		
	if (iBuilding == -1):
		return
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = player.firstCity(false)

	while(loopCity):

		if (loopCity.getPopulation() >= 5):
			if (loopCity.canConstruct(iBuilding, false, false, true)):
				loopCity.setNumRealBuilding(iBuilding, 1)
				
		(loopCity, iter) = player.nextCity(iter, false)
		

def canApplyBlessedSea2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iBuilding = -1
	
	if (-1 != kTriggeredData.eReligion):
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo,gc.getNumSpecialBuildingInfos(),'SPECIALBUILDING_TEMPLE')):
				if (gc.getBuildingInfo(i).getReligionType() == kTriggeredData.eReligion):
					iBuilding = i
					break
		
		
	if (iBuilding == -1):
		return false
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = player.firstCity(false)
	bFound = false

	while(loopCity):

		if (loopCity.getPopulation() >= 5):
			if (loopCity.canConstruct(iBuilding, false, false, true)):
				bFound = true
				break
				
		(loopCity, iter) = player.nextCity(iter, false)

	return bFound


######## HOLY MOUNTAIN ###########

def getHelpHolyMountain1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	map = gc.getMap()
	iMinPoints = 2 * gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	
	iBuilding = -1
	iReligion = gc.getPlayer(kTriggeredData.ePlayer).getStateReligion()
	
	if (-1 != iReligion):
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo, gc.getNumSpecialBuildingInfos(), 'SPECIALBUILDING_CATHEDRAL')):
				if (gc.getBuildingInfo(i).getReligionType() == iReligion):
					iBuilding = i
					break


		szHelp = localText.getText("TXT_KEY_EVENT_HOLY_MOUNTAIN_HELP", ( gc.getBuildingInfo(iBuilding).getTextKey(), gc.getBuildingInfo(iBuilding).getTextKey(), iMinPoints))

	return szHelp

def canTriggerHolyMountain(argsList):
	kTriggeredData = argsList[0]
	map = gc.getMap()
	
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if (plot.getOwner() == -1):
		return true
	
	return false

def expireHolyMountain1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if (plot == None):
		return true
	
	if (plot.getOwner() != kTriggeredData.ePlayer and plot.getOwner() != -1):
		return true
		
	return false

def canTriggerHolyMountainDone(argsList):

	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	
	if (kOrigTriggeredData == None):
		return false
		
	plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)
	if (plot == None):
		return false
	
	if (plot.getOwner() != kTriggeredData.ePlayer):
		return false
	
	return true

def canTriggerHolyMountainRevealed(argsList):

	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	
	if (kOrigTriggeredData == None):
		return false

	iNumPoints = 0		
	
	for i in range(gc.getNumBuildingInfos()):
		if (gc.getBuildingInfo(i).getReligionType() == kOrigTriggeredData.eReligion):
			if (gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo,gc.getNumSpecialBuildingInfos(),'SPECIALBUILDING_CATHEDRAL')):
				iNumPoints += 4 * player.countNumBuildings(i)
			elif (gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo,gc.getNumSpecialBuildingInfos(),'SPECIALBUILDING_TEMPLE')):
				iNumPoints += player.countNumBuildings(i)
			elif (gc.getBuildingInfo(i).getSpecialBuildingType() == CvUtil.findInfoTypeNum(gc.getSpecialBuildingInfo,gc.getNumSpecialBuildingInfos(),'SPECIALBUILDING_MONASTERY')):
				iNumPoints += player.countNumBuildings(i)
				
	if (iNumPoints < 2 * gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()):
		return false

	plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)
	if (plot == None):
		return false
		
	plot.setRevealed(player.getTeam(), true, true, -1)

	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
	kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
	
	return true

def doHolyMountainRevealed(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	if (kTriggeredData.ePlayer == gc.getGame().getActivePlayer()):
		CyCamera().JustLookAtPlot( CyMap().plot( kTriggeredData.iPlotX, kTriggeredData.iPlotY ) )

	return 1

######## MARATHON ###########

def canTriggerMarathon(argsList):	
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	team = gc.getTeam(player.getTeam())
	
	if (team.AI_getAtWarCounter(otherPlayer.getTeam()) == 1):
		(loopUnit, iter) = otherPlayer.firstUnit(false)
		while( loopUnit ):
			plot = loopUnit.plot()
			if (not plot.isNone()):
				if (plot.getOwner() == kTriggeredData.ePlayer):
					return true
			(loopUnit, iter) = otherPlayer.nextUnit(iter, false)

	return false

######## WEDDING FEUD ###########

def doWeddingFeud2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = player.firstCity(false)

	while(loopCity):
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(30)
		(loopCity, iter) = player.nextCity(iter, false)
		
	return 1

def getHelpWeddingFeud2(argsList):
	iEvent = argsList[0]
	event = gc.getEventInfo(iEvent)
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_2_HELP", (gc.getDefineINT("TEMP_HAPPY"), 30, religion.getChar()))

	return szHelp

def canDoWeddingFeud3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if player.getGold() - 10 * player.getNumCities() < 0:
		return false
				
	return true

def doWeddingFeud3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive() and loopPlayer.getStateReligion() == player.getStateReligion():
			loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
			player.AI_changeAttitudeExtra(iLoopPlayer, 1)

	if gc.getTeam(destPlayer.getTeam()).canDeclareWar(player.getTeam()):			
		if destPlayer.isHuman():
			# this works only because it's a single-player only event
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_OTHER_3", (gc.getReligionInfo(kTriggeredData.eReligion).getAdjectiveKey(), player.getCivilizationShortDescriptionKey())))
			popupInfo.setData1(kTriggeredData.eOtherPlayer)
			popupInfo.setData2(kTriggeredData.ePlayer)
			popupInfo.setPythonModule("CvRandomEventInterface")
			popupInfo.setOnClickedPythonCallback("weddingFeud3Callback")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
			popupInfo.addPopup(kTriggeredData.eOtherPlayer)
		else:
			gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)
			
	return 1


def weddingFeud3Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]
	
	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		player = gc.getPlayer(iData2)
		gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), false, WarPlanTypes.WARPLAN_LIMITED)
	
	return 0

def getHelpWeddingFeud3(argsList):
	iEvent = argsList[0]
	event = gc.getEventInfo(iEvent)
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_3_HELP", (1, religion.getChar()))

	return szHelp

######## SPICY ###########

def canTriggerSpicy(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iSpice = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_SPICES')
	iHappyBonuses = 0
	bSpices = false
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 4:
					return false
			if i == iSpice:
				return false

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iSpice, false):
		return false
	
	return true

def doSpicy2(argsList):
#	need this because plantations are notmally not allowed unless there are already spices
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	if not plot.isNone():
		plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_PLANTATION'))
	
	return 1

def getHelpSpicy2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iPlantation = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_PLANTATION')
	szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iPlantation).getTextKey(), ))

	return szHelp

######## BABY BOOM ###########

def canTriggerBabyBoom(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())

	if team.getAtWarCount(true) > 0:
		return false

	for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
		if iLoopTeam != player.getTeam():
			if team.AI_getAtPeaceCounter(iLoopTeam) == 1:
				return true

	return false

######## BARD TALE ###########

def applyBardTale3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	player.changeGold(-10 * player.getNumCities())
	
def canApplyBardTale3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if player.getGold() - 10 * player.getNumCities() < 0:
		return false
		
	return true
	

def getHelpBardTale3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	szHelp = localText.getText("TXT_KEY_EVENT_GOLD_LOST", (10 * player.getNumCities(), ))	

	return szHelp

######## LOOTERS ###########

def getHelpLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	szHelp = localText.getText("TXT_KEY_EVENT_LOOTERS_3_HELP", (1, 2, city.getNameKey()))

	return szHelp

def canApplyLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	iNumBuildings = 0	
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0  and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			iNumBuildings += 1
		
	return (iNumBuildings > 0)
	

def applyLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)
	
	iNumBuildings = gc.getGame().getSorenRandNum(2, "Looters event number of buildings destroyed")
	iNumBuildingsDestroyed = 0

	listBuildings = []	
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0  and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)

	for i in range(iNumBuildings+1):
		if len(listBuildings) > 0:
			iBuilding = listBuildings[gc.getGame().getSorenRandNum(len(listBuildings), "Looters event building destroyed")]
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.eOtherPlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), true, true)
			city.setNumRealBuilding(iBuilding, 0)
			iNumBuildingsDestroyed += 1
			listBuildings.remove(iBuilding)
				
	if iNumBuildingsDestroyed > 0:
		szBuffer = localText.getText("TXT_KEY_EVENT_NUM_BUILDINGS_DESTROYED", (iNumBuildingsDestroyed, gc.getPlayer(kTriggeredData.eOtherPlayer).getCivilizationAdjectiveKey(), city.getNameKey()))
		CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_WHITE"), -1, -1, true, true)

######## BROTHERS IN NEED ###########

def canTriggerBrothersInNeed(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	
	if not player.canTradeNetworkWith(kTriggeredData.eOtherPlayer):
		return false
	
	listResources = []
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IRON'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IVORY'))

#FfH: Modified by Kael 10/01/2007
#	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OIL'))
#	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_URANIUM'))
#FfH: End Modify
	
	bFound = false
	for iResource in listResources: 
		if (player.getNumTradeableBonuses(iResource) > 1 and otherPlayer.getNumAvailableBonuses(iResource) <= 0):
			bFound = true
			break
		
	if not bFound:
		return false
		
	for iTeam in range(gc.getMAX_CIV_TEAMS()):
		if iTeam != player.getTeam() and iTeam != otherPlayer.getTeam() and gc.getTeam(iTeam).isAlive():
			if gc.getTeam(iTeam).isAtWar(otherPlayer.getTeam()) and not gc.getTeam(iTeam).isAtWar(player.getTeam()):
				return true
			
	return false
	
def canDoBrothersInNeed1(argsList):
	kTriggeredData = argsList[1]
	newArgs = (kTriggeredData, )
	
	return canTriggerBrothersInNeed(newArgs)
	
######## HURRICANE ###########

def canTriggerHurricaneCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return false
		
	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return false
		
	if city.plot().getLatitude() <= 0:
		return false
		
	if city.getPopulation() < 2:
		return false
		
	return true

def canApplyHurricane1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	
	listBuildings = []	
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)
			
	return (len(listBuildings) > 0)

def canApplyHurricane2(argsList):			
	return (not canApplyHurricane1(argsList))

		
def applyHurricane1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	
	listCheapBuildings = []	
	listExpensiveBuildings = []	
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listCheapBuildings.append(iBuilding)
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listExpensiveBuildings.append(iBuilding)

	if len(listCheapBuildings) > 0:
		iBuilding = listCheapBuildings[gc.getGame().getSorenRandNum(len(listCheapBuildings), "Hurricane event cheap building destroyed")]
		szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), true, true)
		city.setNumRealBuilding(iBuilding, 0)

	if len(listExpensiveBuildings) > 0:
		iBuilding = listExpensiveBuildings[gc.getGame().getSorenRandNum(len(listExpensiveBuildings), "Hurricane event expensive building destroyed")]
		szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), true, true)
		city.setNumRealBuilding(iBuilding, 0)

		
######## CYCLONE ###########

def canTriggerCycloneCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return false
		
	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return false
		
	if city.plot().getLatitude() >= 0:
		return false
		
	return true

######## TSUNAMI ###########

def canTriggerTsunamiCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return false
		
	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return false
				
	return true

def canApplyTsunami1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	
	return (city.getPopulation() < 6)

def canApplyTsunami2(argsList):			
	return (not canApplyTsunami1(argsList))

		
def applyTsunami1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	
	city.kill()
	
def applyTsunami2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	
	listBuildings = []	
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0  and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)

	for i in range(5):
		if len(listBuildings) > 0:
			iBuilding = listBuildings[gc.getGame().getSorenRandNum(len(listBuildings), "Tsunami event building destroyed")]
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), true, true)
			city.setNumRealBuilding(iBuilding, 0)
			listBuildings.remove(iBuilding)
					

def getHelpTsunami2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	szHelp = localText.getText("TXT_KEY_EVENT_TSUNAMI_2_HELP", (5, city.getNameKey()))

	return szHelp

		
######## MONSOON ###########

def canTriggerMonsoonCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return false
		
	if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return false
		
	iJungleType = CvUtil.findInfoTypeNum(gc.getFeatureInfo, gc.getNumFeatureInfos(),'FEATURE_JUNGLE')
		
	for iDX in range(-3, 4):
		for iDY in range(-3, 4):
			pLoopPlot = plotXY(city.getX(), city.getY(), iDX, iDY)
			if not pLoopPlot.isNone() and pLoopPlot.getFeatureType() == iJungleType:
				return true
				
	return false

######## VOLCANO ###########

def getHelpVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_VOLCANO_1_HELP", ())

	return szHelp

def canApplyVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iNumImprovements = 0
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
						iNumImprovements += 1

	return (iNumImprovements > 0)

def applyVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	listPlots = []
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
						listPlots.append(loopPlot)
					
	listRuins = []
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_COTTAGE'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_HAMLET'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_VILLAGE'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_TOWN'))
	
	iRuins = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CITY_RUINS')

	for i in range(3):
		if len(listPlots) > 0:
			plot = listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Volcano event improvement destroyed")]
			iImprovement = plot.getImprovementType()
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getImprovementInfo(iImprovement).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getImprovementInfo(iImprovement).getButton(), gc.getInfoTypeForString("COLOR_RED"), plot.getX(), plot.getY(), true, true)
			if iImprovement in listRuins:
				plot.setImprovementType(iRuins)
			else:
				plot.setImprovementType(-1)
			listPlots.remove(plot)
			
			if i == 1 and gc.getGame().getSorenRandNum(100, "Volcano event num improvements destroyed") < 50:
				break

######## DUSTBOWL ###########

def canTriggerDustbowlCont(argsList):
	kTriggeredData = argsList[0]

	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	
	if (kOrigTriggeredData == None):
		return false

	iFarmType = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_FARM')
	iPlainsType = CvUtil.findInfoTypeNum(gc.getTerrainInfo,gc.getNumTerrainInfos(),'TERRAIN_PLAINS')
	
	map = gc.getMap()
	iBestValue = map.getGridWidth() + map.getGridHeight()
	bestPlot = None
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == kTriggeredData.ePlayer and plot.getImprovementType() == iFarmType and plot.getTerrainType() == iPlainsType):
			iValue = plotDistance(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY, plot.getX(), plot.getY())
			if iValue < iBestValue:
				iBestValue = iValue
				bestPlot = plot
				
	if bestPlot != None:
		kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
		kActualTriggeredDataObject.iPlotX = bestPlot.getX()
		kActualTriggeredDataObject.iPlotY = bestPlot.getY()
	else:
		player.resetEventOccured(trigger.getPrereqEvent(0))
		return false
		
	return true

def getHelpDustBowl2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_DUSTBOWL_2_HELP", ())

	return szHelp

######## SALTPETER ###########

def getSaltpeterNumExtraPlots():
	map = gc.getMap()	
	if map.getWorldSize() <= 1:
		return 1
	elif map.getWorldSize() <= 3:
		return 2
	elif map.getWorldSize() <= 4:
		return 3
	else:
		return 4

def getHelpSaltpeter(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_SALTPETER_HELP", (getSaltpeterNumExtraPlots(), ))

	return szHelp

def canApplySaltpeter(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	map = gc.getMap()
	
	player = gc.getPlayer(kTriggeredData.ePlayer)

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if (plot == None):
		return false
		
	iForest = CvUtil.findInfoTypeNum(gc.getFeatureInfo,gc.getNumFeatureInfos(),'FEATURE_FOREST')
	
	iNumPlots = 0
	for i in range(map.numPlots()):
		loopPlot = map.plotByIndex(i)
		if (loopPlot.getOwner() == kTriggeredData.ePlayer and loopPlot.getFeatureType() == iForest and loopPlot.isHills()):
			iDistance = plotDistance(kTriggeredData.iPlotX, kTriggeredData.iPlotY, loopPlot.getX(), loopPlot.getY())
			if iDistance > 0:
				iNumPlots += 1
	
	return (iNumPlots >= getSaltpeterNumExtraPlots())

def applySaltpeter(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	map = gc.getMap()
	
	player = gc.getPlayer(kTriggeredData.ePlayer)

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if (plot == None):
		return
		
	iForest = CvUtil.findInfoTypeNum(gc.getFeatureInfo,gc.getNumFeatureInfos(),'FEATURE_FOREST')
	
	listPlots = []
	for i in range(map.numPlots()):
		loopPlot = map.plotByIndex(i)
		if (loopPlot.getOwner() == kTriggeredData.ePlayer and loopPlot.getFeatureType() == iForest and loopPlot.isHills()):
			iDistance = plotDistance(kTriggeredData.iPlotX, kTriggeredData.iPlotY, loopPlot.getX(), loopPlot.getY())
			if iDistance > 0:
				listPlots.append((iDistance, loopPlot))

	listPlots.sort()
	
	iCount = getSaltpeterNumExtraPlots()
	for loopPlot in listPlots:
		if iCount == 0:
			break
		iCount -= 1
		gc.getGame().setPlotExtraYield(loopPlot[1].getX(), loopPlot[1].getY(), YieldTypes.YIELD_COMMERCE, 1)
		CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), localText.getText("TXT_KEY_EVENT_SALTPETER_DISCOVERED", ()), "", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_WHITE"), loopPlot[1].getX(), loopPlot[1].getY(), true, true)

######## GREAT DEPRESSION ###########

def applyGreatDepression(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	corporation = gc.getCorporationInfo(kTriggeredData.eCorporation)
	
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			loopPlayer.changeGold(-loopPlayer.getGold()/4)	
			
			if iPlayer != kTriggeredData.ePlayer:
				szText = localText.getText("TXT_KEY_EVENTTRIGGER_GREAT_DEPRESSION", (player.getCivilizationAdjectiveKey(), u"", u"", u"", u"", corporation.getTextKey()))
				szText += u"\n\n" + localText.getText("TXT_KEY_EVENT_GREAT_DEPRESSION_HELP", (25, ))
				popupInfo = CyPopupInfo()
				popupInfo.setText(szText)
				popupInfo.addPopup(iPlayer)
			
	
def getHelpGreatDepression(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_GREAT_DEPRESSION_HELP", (25, ))	

	return szHelp
	
######## CHAMPION ###########

def canTriggerChampion(argsList):	
	kTriggeredData = argsList[0]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())

	if team.getAtWarCount(true) > 0:
		return false
				
	return true
	
def canTriggerChampionUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	unit = player.getUnit(iUnit)
	
	if unit.isNone():
		return false
		
	if unit.getDamage() > 0:
		return false
		
	if unit.getExperience() < 3:
		return false

#FfH: Modified by Kael 09/26/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify

	if unit.isHasPromotion(iLeadership):
		return false

	return true
	
def applyChampion(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

#FfH: Modified by Kael 10/01/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify
	
	unit.setHasPromotion(iLeadership, true)
	
def getHelpChampion(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	
#FfH: Modified by Kael 09/26/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify

	szHelp = localText.getText("TXT_KEY_EVENT_CHAMPION_HELP", (unit.getNameKey(), gc.getPromotionInfo(iLeadership).getTextKey()))	

	return szHelp
	
######## ELECTRIC COMPANY ###########

def canTriggerElectricCompany(argsList):	
	kTriggeredData = argsList[0]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	player = gc.getPlayer(kTriggeredData.ePlayer)

	(loopCity, iter) = player.firstCity(false)

	while(loopCity):

		if (loopCity.angryPopulation(0) > 0):
			return false
				
		(loopCity, iter) = player.nextCity(iter, false)
						
	return true
	
######## GOLD RUSH ###########

def canTriggerGoldRush(argsList):	
	kTriggeredData = argsList[0]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iIndustrial = CvUtil.findInfoTypeNum(gc.getEraInfo,gc.getNumEraInfos(),'ERA_INDUSTRIAL')
	
	if player.getCurrentEra() != iIndustrial:
		return false
	
						
	return true
	
######## INFLUENZA ###########

def canTriggerInfluenza(argsList):	
	kTriggeredData = argsList[0]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())
	
	iIndustrial = CvUtil.findInfoTypeNum(gc.getEraInfo,gc.getNumEraInfos(),'ERA_INDUSTRIAL')
	
	if player.getCurrentEra() <= iIndustrial:
		return false
	
	iMedicine = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_MEDICINE')
	
	if team.isHasTech(iMedicine):
		return false
						
	return true
	
def applyInfluenza2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eventCity = player.getCity(kTriggeredData.iCityId)

	iNumCities = 2 + gc.getGame().getSorenRandNum(3, "Influenza event number of cities")

	listCities = []	
	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if loopCity.getPopulation() > 2:
			iDistance = plotDistance(eventCity.getX(), eventCity.getY(), loopCity.getX(), loopCity.getY())
			if iDistance > 0:
				listCities.append((iDistance, loopCity))
		(loopCity, iter) = player.nextCity(iter, false)
		
	listCities.sort()
	
	if iNumCities > len(listCities): 
		iNumCities = len(listCities)
				
	for i in range(iNumCities):
		(iDist, loopCity) = listCities[i]
		loopCity.changePopulation(-2)
		szBuffer = localText.getText("TXT_KEY_EVENT_INFLUENZA_HIT_CITY", (loopCity.getNameKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGE", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_RED"), loopCity.getX(), loopCity.getY(), true, true)
				

def getHelpInfluenza2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_INFLUENZA_HELP_2", (2, ))	

	return szHelp

######## SOLO FLIGHT ###########


def canTriggerSoloFlight(argsList):	
	kTriggeredData = argsList[0]

	map = gc.getMap()	
	if map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_DUEL'):
		iMinLandmass  = 3
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_TINY'):
		iMinLandmass  = 4
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_SMALL'):
		iMinLandmass  = 6
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_STANDARD'):
		iMinLandmass  = 8
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_LARGE'):
		iMinLandmass  = 10
	else:
		iMinLandmass  = 12
	
	if (map.getNumLandAreas() < iMinLandmass):
		return false
		
	if gc.getGame().isGameMultiPlayer():
		return false
	
	return true

def getHelpSoloFlight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1, ))	

	return szHelp

def applySoloFlight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
						

######## ANTELOPE ###########

def canTriggerAntelope(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_DEER')
	iHappyBonuses = 0
	bDeer = false
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return false
			if i == iDeer:
				return false	

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iDeer, false):
		return false
				
	return true

def doAntelope2(argsList):
#	Need this because camps are not normally allowed unless there is already deer.
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	if not plot.isNone():
		plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP'))
	
	return 1

def getHelpAntelope2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iCamp = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP')
	szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iCamp).getTextKey(), ))

	return szHelp

######## WHALEOFATHING ###########

def canTriggerWhaleOfAThing(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iWhale = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_WHALE')
	iHappyBonuses = 0
	bWhale = false
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return false
			if i == iWhale:
				return false

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iWhale, false):
		return false
		
	return true


######## HIYOSILVER ###########

def canTriggerHiyoSilver(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iSilver = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_SILVER')
	iHappyBonuses = 0
	bSilver = false
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return false
			if i == iSilver:
				return false

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iSilver, false):
		return false
				
	return true

######## WININGMONKS ###########

def canTriggerWiningMonks(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if player.getNumAvailableBonuses(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_WINE')) > 0:
		return false
				
	return true


def doWiningMonks2(argsList):
#	Need this because wineries are not normally allowed unless there is already wine.
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	if not plot.isNone():
		plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_WINERY'))
	
	return 1

def getHelpWiningMonks2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iImp = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_WINERY')
	szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iImp).getTextKey(), ))

	return szHelp


######## INDEPENDENTFILMS ###########

def canTriggerIndependentFilms(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	for i in range(gc.getNumBuildingInfos()):
		if gc.getBuildingInfo(i).getFreeBonus() == CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_MOVIES'):
			if player.countNumBuildings(i) > 0:
				return false
				
	return true

def doIndependentFilms(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_MOVIES')

	city.changeFreeBonus(iBonus, 1)
	
	return 1

def getHelpIndependentFilms(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_MOVIES')
	
	szHelp = localText.getText("TXT_KEY_EVENT_INDEPENDENTFILMS_HELP_1", ( 1, gc.getBonusInfo(iBonus).getChar(), city.getNameKey()))

	return szHelp

######## ANCIENT OLYMPICS ###########

def canTriggerAncientOlympics(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	stateReligion = player.getStateReligion()
	
	if stateReligion == CvUtil.findInfoTypeNum(gc.getReligionInfo,gc.getNumReligionInfos(),'RELIGION_JUDAISM'):
		return false

	if stateReligion == CvUtil.findInfoTypeNum(gc.getReligionInfo,gc.getNumReligionInfos(),'RELIGION_CHRISTIANITY'):
		return false

	if stateReligion == CvUtil.findInfoTypeNum(gc.getReligionInfo,gc.getNumReligionInfos(),'RELIGION_ISLAM'):
		return false

	return true

def doAncientOlympics2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	map = gc.getMap()

	for j in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(j)
		if j != kTriggeredData.ePlayer and loopPlayer.isAlive() and not loopPlayer.isMinorCiv():

			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if not plot.isWater() and plot.getOwner() == kTriggeredData.ePlayer and plot.isAdjacentPlayer(j, true):
					loopPlayer.AI_changeMemoryCount(kTriggeredData.ePlayer, MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 1)
					break
		
	return 1

def getHelpAncientOlympics2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	szHelp = localText.getText("TXT_KEY_EVENT_ANCIENTOLYMPICS_HELP_2", ( 1, ))

	return szHelp


######## MODERN OLYMPICS ###########

def canTriggerModernOlympics(argsList):

	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	
	if (kOrigTriggeredData == None):
		return false

	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
	kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
	kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
	
	return true

def getHelpModernOlympics(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1, ))	

	return szHelp

def applyModernOlympics(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
						

######## INTERSTATE ###########

def canTriggerInterstate(argsList):

	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if not player.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_EMANCIPATION')):
		return false
	
	return true

def getHelpInterstate(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_UNIT_MOVEMENT", (1, gc.getRouteInfo(CvUtil.findInfoTypeNum(gc.getRouteInfo,gc.getNumRouteInfos(),'ROUTE_ROAD')).getTextKey()))	

	return szHelp

def applyInterstate(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())
	
	iRoad = CvUtil.findInfoTypeNum(gc.getRouteInfo,gc.getNumRouteInfos(),'ROUTE_ROAD')
						
	team.changeRouteChange(iRoad, -5)
	
######## EARTH DAY ###########

def getHelpEarthDay2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_EARTHDAY_HELP_2", ())	

	return szHelp

def canApplyEarthDay2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iCivic = CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_ENVIRONMENTALISM')
	
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer and not loopPlayer.isHuman():
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				tradeData = TradeData()
				tradeData.ItemType = TradeableItems.TRADE_CIVIC
				tradeData.iData = iCivic
				if loopPlayer.canTradeItem(kTriggeredData.ePlayer, tradeData, False):
					if (loopPlayer.getTradeDenial(kTriggeredData.ePlayer, tradeData) == DenialTypes.NO_DENIAL):
						return true
	return false
	
		
def applyEarthDay2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iCivic = CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_ENVIRONMENTALISM')
	iCivicOption = CvUtil.findInfoTypeNum(gc.getCivicOptionInfo,gc.getNumCivicOptionInfos(),'CIVICOPTION_ECONOMY')
	
	listPlayers = []
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer and not loopPlayer.isHuman():
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				tradeData = TradeData()
				tradeData.ItemType = TradeableItems.TRADE_CIVIC
				tradeData.iData = iCivic
				if loopPlayer.canTradeItem(kTriggeredData.ePlayer, tradeData, False):
					if (loopPlayer.getTradeDenial(kTriggeredData.ePlayer, tradeData) == DenialTypes.NO_DENIAL):
						listPlayers.append((-loopPlayer.AI_civicValue(iCivic), iPlayer))
						
	listPlayers.sort()	
	
	if len(listPlayers) > 3:
		listPlayers = listPlayers[:2]
	
	for (iValue, iPlayer) in listPlayers:
		gc.getPlayer(iPlayer).setCivics(iCivicOption, iCivic)
		
######## FREEDOM CONCERT ###########

def getHelpFreedomConcert2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_FREEDOMCONCERT_HELP_2", ())	

	return szHelp

def canApplyFreedomConcert2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eventCity = player.getCity(kTriggeredData.iCityId)
	
	for iReligion in range(gc.getNumReligionInfos()):
		if eventCity.isHasReligion(iReligion):		
			(loopCity, iter) = player.firstCity(false)
			while(loopCity):
				if not loopCity.isHasReligion(iReligion):
					for jReligion in range(gc.getNumReligionInfos()):
						if loopCity.isHasReligion(jReligion):
							return true
				(loopCity, iter) = player.nextCity(iter, false)

	return false
		
def applyFreedomConcert2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eventCity = player.getCity(kTriggeredData.iCityId)
	
	for iReligion in range(gc.getNumReligionInfos()):
		if eventCity.isHasReligion(iReligion):
		
			bestCity = None
			iBestDistance = 0
			(loopCity, iter) = player.firstCity(false)
			while(loopCity):
				if not loopCity.isHasReligion(iReligion):
					bValid = false
					for jReligion in range(gc.getNumReligionInfos()):
						if loopCity.isHasReligion(jReligion):
							bValid = true
							break
					
					if bValid:				
						iDistance = plotDistance(eventCity.getX(), eventCity.getY(), loopCity.getX(), loopCity.getY())
						
						if iDistance < iBestDistance or bestCity == None:
							bestCity = loopCity
							iBestDistance = iDistance
						
				(loopCity, iter) = player.nextCity(iter, false)
				

			if bestCity != None:									
				bestCity.setHasReligion(iReligion, true, true, true)

######## HEROIC_GESTURE ###########

def canTriggerHeroicGesture(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not gc.getTeam(destPlayer.getTeam()).canChangeWarPeace(player.getTeam()):
		return false
		
	if gc.getTeam(destPlayer.getTeam()).AI_getWarSuccess(player.getTeam()) <= 0:
		return false

	if gc.getTeam(player.getTeam()).AI_getWarSuccess(destPlayer.getTeam()) <= 0:
		return false
	
	return true

def doHeroicGesture2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if destPlayer.isHuman():
		# this works only because it's a single-player only event
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_HEROIC_GESTURE_OTHER_3", (player.getCivilizationAdjectiveKey(), )))
		popupInfo.setData1(kTriggeredData.eOtherPlayer)
		popupInfo.setData2(kTriggeredData.ePlayer)
		popupInfo.setPythonModule("CvRandomEventInterface")
		popupInfo.setOnClickedPythonCallback("heroicGesture2Callback")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
		popupInfo.addPopup(kTriggeredData.eOtherPlayer)
	else:
		destPlayer.forcePeace(kTriggeredData.ePlayer)
		destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
		player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

	return

def heroicGesture2Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]
	
	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		player = gc.getPlayer(iData2)
		destPlayer.forcePeace(iData2)
		destPlayer.AI_changeAttitudeExtra(iData2, 1)
		player.AI_changeAttitudeExtra(iData1, 1)		

	return 0
	
def getHelpHeroicGesture2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	# Get help text
	szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()));

	return szHelp

######## GREAT_MEDIATOR ###########

def canTriggerGreatMediator(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not gc.getTeam(player.getTeam()).canChangeWarPeace(destPlayer.getTeam()):
		return false
		
	if gc.getTeam(player.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10:
		return false

	return true

def doGreatMediator2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if destPlayer.isHuman():
		# this works only because it's a single-player only event
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_GREAT_MEDIATOR_OTHER_3", (player.getCivilizationAdjectiveKey(), )))
		popupInfo.setData1(kTriggeredData.eOtherPlayer)
		popupInfo.setData2(kTriggeredData.ePlayer)
		popupInfo.setPythonModule("CvRandomEventInterface")
		popupInfo.setOnClickedPythonCallback("greatMediator2Callback")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
		popupInfo.addPopup(kTriggeredData.eOtherPlayer)
	else:
		gc.getTeam(player.getTeam()).makePeace(destPlayer.getTeam())
		destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
		player.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

	return

def greatMediator2Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]
	
	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		player = gc.getPlayer(iData2)
		gc.getTeam(destPlayer.getTeam()).makePeace(player.getTeam())
		destPlayer.AI_changeAttitudeExtra(iData2, 1)
		player.AI_changeAttitudeExtra(iData1, 1)		

	return 0
	
def getHelpGreatMediator2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	# Get help text
	szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()));

	return szHelp

######## ANCIENT_TEXTS ###########

def doAncientTexts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)

	return

def getHelpAncientTexts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1, ))	

	return szHelp


######## IMPACT_CRATER ###########

def canTriggerImpactCrater(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iUranium = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_URANIUM')
	if player.getNumAvailableBonuses(iUranium) > 0:
		return false
	
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iUranium, false):
		return false
	
	return true

def doImpactCrater2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	if not plot.isNone():
		plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_MINE'))
	
	return 1

def getHelpImpactCrater2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iMine = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_MINE')
	szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iMine).getTextKey(), ))

	return szHelp

######## SECURITY_TAX ###########

def canTriggerSecurityTax(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iWalls = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_WALLS')
	if player.getNumCities() > player.getBuildingClassCount(iWalls):
		return false
	
	return true


######## LITERACY ###########

def canTriggerLiteracy(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
	if player.getNumCities() > player.getBuildingClassCount(iLibrary):
		return false
	
	return true

######## TEA ###########

def canTriggerTea(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if player.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_MERCANTILISM')):
		return false

	bCanTrade = false		
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:	
			if player.canHaveTradeRoutesWith(iPlayer):
				bCanTrade = true	
				break
			
	if not bCanTrade:
		return false
	
	return true

######## HORSE WHISPERING ###########

def canTriggerHorseWhispering(argsList):
	kTriggeredData = argsList[0]

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false
	
	return true

def getHelpHorseWhispering1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	map = gc.getMap()
	
	iNumStables = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_HELP", (iNumStables, ))

	return szHelp

def canTriggerHorseWhisperingDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	iStable = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_STABLE')
	if gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() > player.getBuildingClassCount(iStable):
		return false
	
	return true

def getHelpHorseWhisperingDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	map = gc.getMap()
	
	iNumUnits = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_DONE_HELP_1", (iNumUnits, ))

	return szHelp

def applyHorseWhisperingDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	map = gc.getMap()
	plot = map.plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iNumUnits = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_HORSE_ARCHER')
	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)
	
	if iUnitType != -1:
		for i in range(iNumUnits):
			player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

######## HARBORMASTER ###########

def getHelpHarbormaster1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iHarborsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	iCaravelsRequired = iHarborsRequired / 2 + 1

	szHelp = localText.getText("TXT_KEY_EVENT_HARBORMASTER_HELP", (iHarborsRequired, iCaravelsRequired))

	return szHelp


def canTriggerHarbormaster(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	map = gc.getMap()

	iNumWater = 0
	
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		
		if plot.isWater():
			iNumWater += 1
			
		if 100 * iNumWater >= 40 * map.numPlots():
			return true
		
	return false

def canTriggerHarbormasterDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iHarbor = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_HARBOR')
	iHarborsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iHarborsRequired > player.getBuildingClassCount(iHarbor):
		return false

	iCaravel = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CARAVEL')
	iCaravelsRequired = iHarborsRequired / 2 + 1
	if iCaravelsRequired > player.getUnitClassCount(iCaravel):
		return false
	
	return true
	
######## CLASSIC LITERATURE ###########

def canTriggerClassicLiterature(argsList):
	kTriggeredData = argsList[0]
	
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	return true

def getHelpClassicLiterature1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iLibrariesRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()

	szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_HELP_1", (iLibrariesRequired, ))

	return szHelp


def canTriggerClassicLiteratureDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
	iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iBuildingsRequired > player.getBuildingClassCount(iLibrary):
		return false
	
	return true

def getHelpClassicLiteratureDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_DONE_HELP_2", ( ))

	return szHelp

def canApplyClassicLiteratureDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), 'ERA_ANCIENT')

	for iTech in range(gc.getNumTechInfos()):
		if gc.getTechInfo(iTech).getEra() == iEraAncient and player.canResearch(iTech, false):
			return true
			
	return false
		
def applyClassicLiteratureDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), 'ERA_ANCIENT')

	listTechs = []
	for iTech in range(gc.getNumTechInfos()):
		if gc.getTechInfo(iTech).getEra() == iEraAncient and player.canResearch(iTech, false):
			listTechs.append(iTech)
			
	if len(listTechs) > 0:
		iTech = listTechs[gc.getGame().getSorenRandNum(len(listTechs), "Classic Literature Event Tech selection")]
		gc.getTeam(player.getTeam()).setHasTech(iTech, true, kTriggeredData.ePlayer, true, true)
		
def getHelpClassicLiteratureDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	iSpecialist = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), 'SPECIALIST_SCIENTIST', )
	iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

	szCityName = u""
	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatLibrary)):
			szCityName = loopCity.getNameKey()
			break
				
		(loopCity, iter) = player.nextCity(iter, false)
	
	szHelp = localText.getText("TXT_KEY_EVENT_FREE_SPECIALIST", (1, gc.getSpecialistInfo(iSpecialist).getTextKey(), szCityName))

	return szHelp

def canApplyClassicLiteratureDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatLibrary)):
			return true
				
		(loopCity, iter) = player.nextCity(iter, false)
			
	return false
		
def applyClassicLiteratureDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	iSpecialist = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), 'SPECIALIST_SCIENTIST', )
	iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatLibrary)):
			loopCity.changeFreeSpecialistCount(iSpecialist, 1)
			return
				
		(loopCity, iter) = player.nextCity(iter, false)

######## MASTER BLACKSMITH ###########

def canTriggerMasterBlacksmith(argsList):
	kTriggeredData = argsList[0]
	
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	return true

def getHelpMasterBlacksmith1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	
	szHelp = localText.getText("TXT_KEY_EVENT_MASTER_BLACKSMITH_HELP_1", (iRequired, player.getCity(kTriggeredData.iCityId).getNameKey()))

	return szHelp

def expireMasterBlacksmith1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)	
	if city == None or city.getOwner() != kTriggeredData.ePlayer:
		return true
				
	return false

def canTriggerMasterBlacksmithDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iForge = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_FORGE')
	iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iBuildingsRequired > player.getBuildingClassCount(iForge):
		return false

	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))

	city = player.getCity(kOrigTriggeredData.iCityId)	
	if city == None or city.getOwner() != kTriggeredData.ePlayer:
		return false

	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
		
	return true

def canApplyMasterBlacksmithDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
	city = player.getCity(kTriggeredData.iCityId)
	
	if city == None:
		return false
	
	map = gc.getMap()
	iBestValue = map.getGridWidth() + map.getGridHeight()
	bestPlot = None
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == kTriggeredData.ePlayer and plot.canHaveBonus(iBonus, false)):
			iValue = plotDistance(city.getX(), city.getY(), plot.getX(), plot.getY())
			if iValue < iBestValue:
				iBestValue = iValue
				bestPlot = plot
				
	if bestPlot == None:
		return false

	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iPlotX = bestPlot.getX()
	kActualTriggeredDataObject.iPlotY = bestPlot.getY()
		
	return true

def applyMasterBlacksmithDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	city = player.getCity(kTriggeredData.iCityId)
	
	iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
	plot.setBonusType(iBonus)

	szBuffer = localText.getText("TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", (gc.getBonusInfo(iBonus).getTextKey(), city.getNameKey()))
	CyInterface().addMessage(kTriggeredData.ePlayer, false, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), gc.getInfoTypeForString("COLOR_WHITE"), plot.getX(), plot.getY(), true, true)

def canApplyMasterBlacksmithDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if player.getStateReligion() == -1:		
		return false
		
	return true

######## THE BEST DEFENSE ###########

def canTriggerBestDefense(argsList):
	kTriggeredData = argsList[0]
	
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	return true

def getHelpBestDefense1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	
	szHelp = localText.getText("TXT_KEY_EVENT_BEST_DEFENSE_HELP_1", (iRequired, ))

	return szHelp

def canTriggerBestDefenseDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iCastle = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_CASTLE')
	iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iBuildingsRequired > player.getBuildingClassCount(iCastle):
		return false
		
	return true

def getHelpBestDefenseDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_BEST_DEFENSE_DONE_HELP_2", (3, ))	

	return szHelp

def applyBestDefenseDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 3)
						

def canApplyBestDefenseDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iGreatWall = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_WALL')

	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatWall)):
			return true
				
		(loopCity, iter) = player.nextCity(iter, false)
			
	return false

######## NATIONAL SPORTS LEAGUE ###########

def canTriggerSportsLeague(argsList):
	kTriggeredData = argsList[0]
	
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	return true
def getHelpSportsLeague1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_STATUE_OF_ZEUS')
	
	szHelp = localText.getText("TXT_KEY_EVENT_SPORTS_LEAGUE_HELP_1", (iRequired, gc.getBuildingInfo(iBuilding).getTextKey()))

	return szHelp

def canTriggerSportsLeagueDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iCastle = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_COLOSSEUM')
	iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iBuildingsRequired > player.getBuildingClassCount(iCastle):
		return false
		
	return true

def canApplySportsLeagueDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iZeus = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_STATUE_OF_ZEUS')

	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if (loopCity.isHasBuilding(iZeus)):
			return true
				
		(loopCity, iter) = player.nextCity(iter, false)
			
	return false

######## CRUSADE ###########

def canTriggerCrusade(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	if holyCity.getOwner() != kTriggeredData.eOtherPlayer:
		return false
		
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iOtherPlayerCityId = holyCity.getID()	
			
	return true

def getHelpCrusade1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	
	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_HELP_1", (holyCity.getNameKey(), ))

	return szHelp

def expireCrusade1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	if holyCity.getOwner() == kTriggeredData.ePlayer:
		return false

	if player.getStateReligion() != kTriggeredData.eReligion:
		return true

	if holyCity.getOwner() != kTriggeredData.eOtherPlayer:
		return true

	if not gc.getTeam(player.getTeam()).isAtWar(otherPlayer.getTeam()):
		return true	
					
	return false

def canTriggerCrusadeDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)

	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	holyCity = gc.getGame().getHolyCity(kOrigTriggeredData.eReligion)

	if holyCity.getOwner() != kTriggeredData.ePlayer:
		return false
					
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iCityId = holyCity.getID()
	kActualTriggeredDataObject.eOtherPlayer = kOrigTriggeredData.eOtherPlayer
	kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion
	
	for iBuilding in range(gc.getNumBuildingInfos()):
		if gc.getBuildingInfo(iBuilding).getHolyCity() == kOrigTriggeredData.eReligion:
			kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
			break	
			
	return true

def getHelpCrusadeDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	szUnit = gc.getUnitInfo(holyCity.getConscriptUnit()).getTextKey()
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1
	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_DONE_HELP_1", (iNumUnits, szUnit, holyCity.getNameKey()))	

	return szHelp

def canApplyCrusadeDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	if -1 == holyCity.getConscriptUnit():
		return false
	
	return true

def applyCrusadeDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)						
	iUnitType = holyCity.getConscriptUnit()
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1
	
	if iUnitType != -1:
		for i in range(iNumUnits):
			player.initUnit(iUnitType, holyCity.getX(), holyCity.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)

def getHelpCrusadeDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	
	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_DONE_HELP_2", (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), holyCity.getNameKey()))	

	return szHelp

def canApplyCrusadeDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	
	if -1 == kTriggeredData.eBuilding or holyCity.isHasBuilding(kTriggeredData.eBuilding):
		return false			
	
	return true

def applyCrusadeDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	holyCity.setNumRealBuilding(kTriggeredData.eBuilding, 1)
						
	if (not gc.getGame().isNetworkMultiPlayer() and kTriggeredData.ePlayer == gc.getGame().getActivePlayer()):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
		popupInfo.setData1(kTriggeredData.eBuilding)
		popupInfo.setData2(holyCity.getID())
		popupInfo.setData3(0)
		popupInfo.setText(u"showWonderMovie")
		popupInfo.addPopup(kTriggeredData.ePlayer)

def getHelpCrusadeDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	
	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_DONE_HELP_3", (gc.getReligionInfo(kTriggeredData.eReligion).getTextKey(), iNumCities))	

	return szHelp

def canApplyCrusadeDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()

	if gc.getGame().getNumCities() == gc.getGame().countReligionLevels(kTriggeredData.eReligion):
		return false
		
	return true

def applyCrusadeDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	listCities = []	
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():			
			(loopCity, iter) = loopPlayer.firstCity(false)

			while(loopCity):
				if (not loopCity.isHasReligion(kTriggeredData.eReligion)):
					iDistance = plotDistance(holyCity.getX(), holyCity.getY(), loopCity.getX(), loopCity.getY())
					listCities.append((iDistance, loopCity))
						
				(loopCity, iter) = loopPlayer.nextCity(iter, false)
	
	listCities.sort()
	
	iNumCities = min(gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers(), len(listCities))
	
	for i in range(iNumCities):
		iDistance, loopCity = listCities[i]
		loopCity.setHasReligion(kTriggeredData.eReligion, true, true, true)	

######## ESTEEMEED_PLAYWRIGHT ###########

def canTriggerEsteemedPlaywright(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	# If source civ is operating this Civic, disallow the event to trigger.
	if player.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_SLAVERY')):
		return false

	return true


######## SECRET_KNOWLEDGE ###########
	
def getHelpSecretKnowledge2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	szHelp = localText.getText("TXT_KEY_EVENT_YIELD_CHANGE_BUILDING", (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+4[ICON_CULTURE]"))	

	return szHelp

def applySecretKnowledge2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	city = player.getCity(kTriggeredData.iCityId)
	city.setBuildingCommerceChange(gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(), CommerceTypes.COMMERCE_CULTURE, 4)

######## HIGH_WARLORD ###########

def canTriggerHighWarlord(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	# If source civ is operating this Civic, disallow the event to trigger.
	if player.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_EMANCIPATION')):
		return false

	return true


######## EXPERIENCED_CAPTAIN ###########

def canTriggerExperiencedCaptain(argsList):
	kTriggeredData = argsList[0]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	
	if unit.isNone():
		return false
		
	if unit.getExperience() < 7:
		return false

	return true

######## PARTISANS ###########

def getNumPartisanUnits(plot, iPlayer):
	for i in range(gc.getNumCultureLevelInfos()):
		iI = gc.getNumCultureLevelInfos() - i - 1
		if plot.getCulture(iPlayer) >= gc.getCultureLevelInfo(iI).getSpeedThreshold(gc.getGame().getGameSpeedType()):
			return iI
	return 0

def getHelpPartisans1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	capital = player.getCapitalCity()
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	if None != capital and not capital.isNone():
		iNumUnits = getNumPartisanUnits(plot, kTriggeredData.ePlayer)
		szUnit = gc.getUnitInfo(capital.getConscriptUnit()).getTextKey()
		
		szHelp = localText.getText("TXT_KEY_EVENT_PARTISANS_HELP_1", (iNumUnits, szUnit))	

	return szHelp

def canApplyPartisans1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	if getNumPartisanUnits(plot, kTriggeredData.ePlayer) <= 0:
		return false

	for i in range(3):
		for j in range(3):
			loopPlot = gc.getMap().plot(kTriggeredData.iPlotX + i - 1, kTriggeredData.iPlotY + j - 1)
			if None != loopPlot and not loopPlot.isNone():
				if not (loopPlot.isVisibleEnemyUnit(kTriggeredData.ePlayer) or loopPlot.isWater() or loopPlot.isImpassable() or loopPlot.isCity()):
					return true
	return false
	

def applyPartisans1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)	
	capital = player.getCapitalCity()
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	if None != capital and not capital.isNone():
		iNumUnits = getNumPartisanUnits(plot, kTriggeredData.ePlayer)

		listPlots = []
		for i in range(3):
			for j in range(3):
				loopPlot = gc.getMap().plot(kTriggeredData.iPlotX + i - 1, kTriggeredData.iPlotY + j - 1)
				if None != loopPlot and not loopPlot.isNone() and (i != 1 or j != 1):
					if not (loopPlot.isVisibleEnemyUnit(kTriggeredData.ePlayer) or loopPlot.isWater() or loopPlot.isImpassable()):
						listPlots.append(loopPlot)
		
		if len(listPlots) > 0:
			for i in range(iNumUnits):
				iPlot = gc.getGame().getSorenRandNum(len(listPlots), "Partisan event placement")
				player.initUnit(capital.getConscriptUnit(), listPlots[iPlot].getX(), listPlots[iPlot].getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

def getHelpPartisans2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	capital = player.getCapitalCity()
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	if None != capital and not capital.isNone():
		iNumUnits = max(1, getNumPartisanUnits(plot, kTriggeredData.ePlayer) / 2)
		szUnit = gc.getUnitInfo(capital.getConscriptUnit()).getTextKey()
		
		szHelp = localText.getText("TXT_KEY_EVENT_PARTISANS_HELP_2", (iNumUnits, szUnit, capital.getNameKey()))	

	return szHelp

def canApplyPartisans2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	return (max(1, getNumPartisanUnits(plot, kTriggeredData.ePlayer) / 2) > 0)
	
def applyPartisans2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)	
	capital = player.getCapitalCity()
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	if None != capital and not capital.isNone():
		iNumUnits = max(1, getNumPartisanUnits(plot, kTriggeredData.ePlayer) / 2)
		for i in range(iNumUnits):
			player.initUnit(capital.getConscriptUnit(), capital.getX(), capital.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

######## GREED ###########

def canTriggerGreed(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	
	if not gc.getTeam(player.getTeam()).canChangeWarPeace(otherPlayer.getTeam()):
		return false

	listBonuses = []

#FfH: Modified by Kael 10/01/2007
#	iOil = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OIL')
#	if 0 == player.getNumAvailableBonuses(iOil):
#		listBonuses.append(iOil)
#FfH: End Modify

	iIron = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IRON')
	if 0 == player.getNumAvailableBonuses(iIron):
		listBonuses.append(iIron)
	iHorse = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE')
	if 0 == player.getNumAvailableBonuses(iHorse):
		listBonuses.append(iHorse)
	iCopper = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
	if 0 == player.getNumAvailableBonuses(iCopper):
		listBonuses.append(iCopper)

	map = gc.getMap()
	bFound = false
	listPlots = []
	for iBonus in listBonuses:
		for i in range(map.numPlots()):
			loopPlot = map.plotByIndex(i)
			if loopPlot.getOwner() == kTriggeredData.eOtherPlayer and loopPlot.getBonusType(player.getTeam()) == iBonus and loopPlot.isRevealed(player.getTeam(), false) and not loopPlot.isWater():
				listPlots.append(loopPlot)
				bFound = true
		if bFound:
			break
			
	if not bFound:
		return false

	plot = listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Greed event plot selection")]
	
	if -1 == getGreedUnit(player, plot):
		return false
	
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iPlotX = plot.getX()
	kActualTriggeredDataObject.iPlotY = plot.getY()
				
	return true

def getHelpGreed1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	iBonus = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY).getBonusType(player.getTeam())
	
	iTurns = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent()
			
	szHelp = localText.getText("TXT_KEY_EVENT_GREED_HELP_1", (otherPlayer.getCivilizationShortDescriptionKey(), gc.getBonusInfo(iBonus).getTextKey(), iTurns))

	return szHelp

def expireGreed1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	if plot.getOwner() == kTriggeredData.ePlayer or plot.getOwner() == -1:
		return false
	
	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent():
		return true
	
	if plot.getOwner() != kTriggeredData.eOtherPlayer:
		return true
				
	return false

def canTriggerGreedDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)

	if plot.getOwner() != kOrigTriggeredData.ePlayer:
		return false
		
	if -1 == getGreedUnit(player, plot):
		return false

	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
	kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
	kActualTriggeredDataObject.eOtherPlayer = kOrigTriggeredData.eOtherPlayer
	
	return true

def getGreedUnit(player, plot):
	iBonus = plot.getBonusType(player.getTeam())
	iBestValue = 0
	iBestUnit = -1
	for iUnitClass in range(gc.getNumUnitClassInfos()):
		iUnit = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClass)
		if -1 != iUnit and player.canTrain(iUnit, false, false) and (gc.getUnitInfo(iUnit).getDomainType() == DomainTypes.DOMAIN_LAND):
			iValue = 0
			if gc.getUnitInfo(iUnit).getPrereqAndBonus() == iBonus:
				iValue = player.AI_unitValue(iUnit, UnitAITypes.UNITAI_ATTACK, plot.area(), false)
			else:
				for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
					if (gc.getUnitInfo(iUnit).getPrereqOrBonuses(j) == iBonus):
						iValue = player.AI_unitValue(iUnit, UnitAITypes.UNITAI_ATTACK, plot.area(), false)
						break
			if iValue > iBestValue:
				iBestValue = iValue
				iBestUnit = iUnit
				
	return iBestUnit
	

def getHelpGreedDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1
	iUnitType = getGreedUnit(player, plot)
	
	if iUnitType != -1:	
		szHelp = localText.getText("TXT_KEY_EVENT_GREED_DONE_HELP_1", (iNumUnits, gc.getUnitInfo(iUnitType).getTextKey()))	

	return szHelp

def applyGreedDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
		
	iUnitType = getGreedUnit(player, plot)
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1
	
	if iUnitType != -1:
		for i in range(iNumUnits):
			player.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)


######## WAR CHARIOTS ###########

def canTriggerWarChariots(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.eReligion = ReligionTypes(player.getStateReligion())
	
	return true

def getHelpWarChariots1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	szHelp = localText.getText("TXT_KEY_EVENT_WAR_CHARIOTS_HELP_1", (iNumUnits, ))

	return szHelp

def canTriggerWarChariotsDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CHARIOT')
	if player.getUnitClassCount(iUnitClassType) < iNumUnits:
		return false
	
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion
		
	return true

######## ELITE SWORDSMEN ###########

def getHelpEliteSwords1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	szHelp = localText.getText("TXT_KEY_EVENT_ELITE_SWORDS_HELP_1", (iNumUnits, ))

	return szHelp

def canTriggerEliteSwordsDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SWORDSMAN')
	if player.getUnitClassCount(iUnitClassType) < iNumUnits:
		return false
			
	return true


def canApplyEliteSwordsDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iCivic = CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_HEREDITARY_RULE')
	
	if not player.isCivic(iCivic):
		return false
	
	return true	

######## WARSHIPS ###########

def canTriggerWarships(argsList):
	kTriggeredData = argsList[0]
	
	map = gc.getMap()
	iNumWater = 0
	
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		
		if plot.isWater():
			iNumWater += 1
			
		if 100 * iNumWater >= 55 * map.numPlots():
			return true
			
	return false

def getHelpWarships1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	
	iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIGHTHOUSE')
	szHelp = localText.getText("TXT_KEY_EVENT_WARSHIPS_HELP_1", (iNumUnits, gc.getBuildingInfo(iBuilding).getTextKey()))

	return szHelp

def canTriggerWarshipsDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_TRIREME')

	if player.getUnitClassCount(iUnitClassType) < iNumUnits:
		return false
			
	return true


def canApplyWarshipsDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIGHTHOUSE')
	if player.getBuildingClassCount(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == 0:
		return false

	return true	

######## GUNS NOT BUTTER ###########

def getHelpGunsButter1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_TAJ_MAHAL')
	
	szHelp = localText.getText("TXT_KEY_EVENT_GUNS_BUTTER_HELP_1", (iNumUnits, gc.getBuildingInfo(iBuilding).getTextKey()))

	return szHelp

def canTriggerGunsButterDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_MUSKETMAN')

	if player.getUnitClassCount(iUnitClassType) < iNumUnits:
		return false
			
	return true


def canApplyGunsButterDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iCivic = CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_VASSALAGE')
	
	if not player.isCivic(iCivic):
		return false
	
	return true	

def canApplyGunsButterDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_TAJ_MAHAL')
	if player.getBuildingClassCount(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == 0:
		return false

	return true	

######## NOBLE KNIGHTS ###########

def canTriggerNobleKnights(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.eReligion = ReligionTypes(player.getStateReligion())
	
	return true

def getHelpNobleKnights1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
		
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_ORACLE')
	
	szHelp = localText.getText("TXT_KEY_EVENT_NOBLE_KNIGHTS_HELP_1", (iNumUnits, gc.getBuildingInfo(iBuilding).getTextKey()))

	return szHelp

def canTriggerNobleKnightsDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_KNIGHT')

	if player.getUnitClassCount(iUnitClassType) < iNumUnits:
		return false
			
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion

	iBuilding = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_ORACLE')
	
	(loopCity, iter) = player.firstCity(false)
	while(loopCity):
		if (loopCity.isHasBuilding(iBuilding)):
			kActualTriggeredDataObject.iPlotX = loopCity.getX()
			kActualTriggeredDataObject.iPlotY = loopCity.getY()
			kActualTriggeredDataObject.iCityId = loopCity.getID()
			break
				
		(loopCity, iter) = player.nextCity(iter, false)

	return true

def canApplyNobleKnightsDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
		
	iCivic = CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_ORGANIZED_RELIGION')
	
	if not player.isCivic(iCivic):
		return false
	
	return true	

######## OVERWHELM DOCTRINE ###########

def canTriggerOverwhelm(argsList):
	kTriggeredData = argsList[0]
	
	map = gc.getMap()
	iNumWater = 0
	
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if plot.isWater():
			iNumWater += 1
		if 100 * iNumWater >= 55 * map.numPlots():
			return true			
	return false

def getHelpOverwhelm1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iDestroyer = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_DESTROYER')
	iNumDestroyers = 4
	iBattleship = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_BATTLESHIP')
	iNumBattleships = 2
	iCarrier = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_CARRIER')
	iNumCarriers = 3
	iFighter = CvUtil.findInfoTypeNum(gc.getSpecialUnitInfo, gc.getNumSpecialUnitInfos(), 'SPECIALUNIT_FIGHTER')
	iNumFighters = 9
	iProject = CvUtil.findInfoTypeNum(gc.getProjectInfo, gc.getNumProjectInfos(), 'PROJECT_MANHATTAN_PROJECT')
			
	szHelp = localText.getText("TXT_KEY_EVENT_OVERWHELM_HELP_1", (iNumDestroyers, gc.getUnitInfo(iDestroyer).getTextKey(), iNumBattleships, gc.getUnitInfo(iBattleship).getTextKey(), iNumCarriers, gc.getUnitInfo(iCarrier).getTextKey(), iNumFighters, gc.getSpecialUnitInfo(iFighter).getTextKey(), gc.getProjectInfo(iProject).getTextKey()))

	return szHelp

def canTriggerOverwhelmDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iDestroyer = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_DESTROYER')
	iNumDestroyers = 4
	if player.getUnitClassCount(iDestroyer) < iNumDestroyers:
		return false
			
	iBattleship = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_BATTLESHIP')
	iNumBattleships = 2
	if player.getUnitClassCount(iBattleship) < iNumBattleships:
		return false

	iCarrier = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CARRIER')
	iNumCarriers = 3
	if player.getUnitClassCount(iCarrier) < iNumCarriers:
		return false

	iFighter = CvUtil.findInfoTypeNum(gc.getSpecialUnitInfo, gc.getNumSpecialUnitInfos(), 'SPECIALUNIT_FIGHTER')
	iNumFighters = 9
	iNumPlayerFighters = 0
	(loopUnit, iter) = player.firstUnit(false)
	while (loopUnit):
		if loopUnit.getSpecialUnitType() == iFighter:
			iNumPlayerFighters += 1
		(loopUnit, iter) = player.nextUnit(iter, false)

	if iNumPlayerFighters < iNumFighters:
		return false
			
	return true

def getHelpOverwhelmDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_OVERWHELM_DONE_HELP_3", ())
	
	return szHelp

def canApplyOverwhelmDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iProject = CvUtil.findInfoTypeNum(gc.getProjectInfo, gc.getNumProjectInfos(), 'PROJECT_MANHATTAN_PROJECT')
	if gc.getTeam(player.getTeam()).getProjectCount(iProject) == 0:
		return false
	
	return true

def applyOverwhelmDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	gc.getGame().changeNoNukesCount(1)
		
######## CORPORATE EXPANSION ###########

def canTriggerCorporateExpansion(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	city = gc.getGame().getHeadquarters(kTriggeredData.eCorporation)
	if None == city or city.isNone():
		return false

	# Hack to remember the number of cities you already have with the Corporation
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iOtherPlayerCityId = gc.getGame().countCorporationLevels(kTriggeredData.eCorporation)	
	kActualTriggeredDataObject.iCityId = city.getID()
	kActualTriggeredDataObject.iPlotX = city.getX()
	kActualTriggeredDataObject.iPlotY = city.getY()

	bFound = false
	for iBuilding in range(gc.getNumBuildingInfos()):
		if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == kTriggeredData.eCorporation:
			kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
			bFound = true
			break
			
	if not bFound:
		return false
	
	return true

def expireCorporateExpansion1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	city = player.getCity(kTriggeredData.iCityId)
	if None == city or city.isNone():
		return true

	return false

def getHelpCorporateExpansion1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1
	
	szHelp = localText.getText("TXT_KEY_EVENT_CORPORATE_EXPANSION_HELP_1", (gc.getCorporationInfo(kTriggeredData.eCorporation).getTextKey(), iNumCities))

	return szHelp

def canTriggerCorporateExpansionDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	
	iNumCitiesRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() + 1 + kOrigTriggeredData.iOtherPlayerCityId
	
	if iNumCitiesRequired > gc.getGame().countCorporationLevels(kOrigTriggeredData.eCorporation):
		return false

				
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.eCorporation = kOrigTriggeredData.eCorporation
	kActualTriggeredDataObject.eBuilding = kOrigTriggeredData.eBuilding
	kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
	kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
	kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
			
	return true

def getHelpCorporateExpansionDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_YIELD_CHANGE_BUILDING", (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+10[ICON_GOLD]"))

	return szHelp

def applyCorporateExpansionDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	city = player.getCity(kTriggeredData.iCityId)
	if None != city and not city.isNone():
		city.setBuildingCommerceChange(gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(), CommerceTypes.COMMERCE_GOLD, 10)
		
######## HOSTILE TAKEOVER ###########

def canTriggerHostileTakeover(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return false

	city = gc.getGame().getHeadquarters(kTriggeredData.eCorporation)
	if None == city or city.isNone():
		return false

	# Hack to remember the number of cities you already have with the Corporation
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iCityId = city.getID()
	kActualTriggeredDataObject.iPlotX = city.getX()
	kActualTriggeredDataObject.iPlotY = city.getY()

	bFound = false
	for iBuilding in range(gc.getNumBuildingInfos()):
		if gc.getBuildingInfo(iBuilding).getFoundsCorporation() == kTriggeredData.eCorporation:
			kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
			bFound = true
			break
			
	if not bFound:
		return false

	listResources = getHostileTakeoverListResources(gc.getCorporationInfo(kTriggeredData.eCorporation), player)
	if len(listResources) == 0:
		return false
		
	return true

def expireHostileTakeover1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	city = player.getCity(kTriggeredData.iCityId)
	if None == city or city.isNone():
		return true

	return false

def getHostileTakeoverListResources(corporation, player):
	map = gc.getMap()
	listHave = []
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if plot.getOwner() == player.getID():
			iBonus = plot.getBonusType(player.getTeam())
			if iBonus != -1:
				if not iBonus in listHave:
					listHave.append(iBonus)
	listNeed = []
	for i in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
		iBonus = corporation.getPrereqBonus(i)
		if iBonus != -1:
			if not iBonus in listHave:
				listNeed.append(iBonus)
	return listNeed
	
def getHelpHostileTakeover1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	listResources = getHostileTakeoverListResources(gc.getCorporationInfo(kTriggeredData.eCorporation), player)
	szList = u""
	bFirst = true
	for iBonus in listResources:
		if not bFirst:
			szList += u", "
		else:
			bFirst = false
		szList += u"[COLOR_HIGHLIGHT_TEXT]" + gc.getBonusInfo(iBonus).getDescription() + u"[COLOR_REVERT]"
		
	szHelp = localText.getText("TXT_KEY_EVENT_HOSTILE_TAKEOVER_HELP_1", (len(listResources), szList))

	return szHelp

def canTriggerHostileTakeoverDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	
	listResources = getHostileTakeoverListResources(gc.getCorporationInfo(kOrigTriggeredData.eCorporation), player)
	
	if len(listResources) > 0:
		return false
				
	kActualTriggeredDataObject = player.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.eCorporation = kOrigTriggeredData.eCorporation
	kActualTriggeredDataObject.eBuilding = kOrigTriggeredData.eBuilding
	kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId
	kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
	kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
			
	return true

def getHelpHostileTakeoverDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_YIELD_CHANGE_BUILDING", (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+20[ICON_GOLD]"))

	return szHelp

def applyHostileTakeoverDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	city = player.getCity(kTriggeredData.iCityId)
	if None != city and not city.isNone():
		city.setBuildingCommerceChange(gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(), CommerceTypes.COMMERCE_GOLD, 20)
		
		
######## Great Beast ########

def doGreatBeast3(argsList):
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = player.firstCity(false)

	while(loopCity):
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(40)
		(loopCity, iter) = player.nextCity(iter, false)

def getHelpGreatBeast3(argsList):
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_GREAT_BEAST_3_HELP", (gc.getDefineINT("TEMP_HAPPY"), 40, religion.getChar()))

	return szHelp

####### Comet Fragment ########

def canDoCometFragment(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	if (player.getSpaceProductionModifier()) > 10:
		return false
	
	return true

####### Immigrants ########

def canTriggerImmigrantCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if city.isNone():
		return false

	if ((city.happyLevel() - city.unhappyLevel(0) < 1) or (city.goodHealth() - city.badHealth(true) < 1)):
		return false

	if (city.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE) < 5500):
		return false

####### Controversial Philosopher ######

def canTriggerControversialPhilosopherCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return false
	if (not city.isCapital()):
		return false
	if (city.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH) < 3500):
		return false

	return true


				# More Events Mod starts #
# Modified by lfgr

######## Utility Functions (lfgr)

def semiRandomTurnTrigger( iTurns, fChance ) :
	game = CyGame()
	print "iTurns: %d" % iTurns
	iTurns *= gc.getGameSpeedInfo( game.getGameSpeedType() ).getGrowthPercent() / 100
	print "iTurns after gamespeed: %d" % iTurns
	iTurns = round( iTurns )
	print "iTurns after rounding: %d" % iTurns
	if( game.getGameTurn() % iTurns == 0 ) :
		print "Trigger!"
		return game.getSorenRandNum ( 1000, "Random Event Trigger" ) <= fChance * 1000
	else :
		return False

def cityHasBuilding( argsList, sBuildingType ) :
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	return pCity.getNumRealBuilding( gc.getInfoTypeForString( sBuildingType ) ) != 0

def cityReqBuildingHelp( argsList, sBuildingType ) :
	if( not cityHasBuilding( argsList, sBuildingType ) ) :
		szBuilding = gc.getBuildingInfo( gc.getInfoTypeForString( sBuildingType ) ).getDescription()
		return localText.getText( 'TXT_KEY_CIVIC_REQUIRES', ( szBuilding, ) );
	else :
		return ""

def playerHasTrait( argsList, sTraitType ) :
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.hasTrait( gc.getInfoTypeForString('TRAIT_BARBARIAN') )

def playerReqTraitHelp( argsList, sTraitType ) :
	if( not playerHasTrait( argsList, sTraitType ) ) :
		szTrait = gc.getTraitInfo( gc.getInfoTypeForString( sTraitType ) ).getDescription()
		return localText.getText( 'TXT_KEY_CIVIC_REQUIRES', ( szTrait, ) );
	else :
		return ""

def getBestUnitFromUpgrades( eUnitClass, pPlayer, pCity = None ) :
	if( eUnitClass == UnitClassTypes.NO_UNITCLASS ) :
		BugUtil.error( "RandomEvents: initBestUnitFromUpgrades() eUnitClass param is NO_UNITCLASS" )
	
	eUnit = gc.getCivilizationInfo( pPlayer.getCivilizationType() ).getCivilizationUnits( eUnitClass )
	if( eUnit == UnitTypes.NO_UNIT ) :
		if( LOG_DEBUG ) : CvUtil.pyPrint( "RandomEvents - getBestUnitFromUpgrades from unit class %s failed: no available units." % ( gc.getUnitClassInfo( eUnitClass ).getDescription() ) )
		return UnitTypes.NO_UNIT
	
	return recGetBestTrainableUnitFromUpgrade( eUnit, pPlayer, pCity )

def recGetBestTrainableUnitFromUpgrade( eUnit, pPlayer, pCity ) :
	eBestUnit = eUnit
	# loop upgrades
	for eUpgradeUnitClass in range( gc.getNumUnitClassInfos() ) :
		pUpgradeUnitClass = gc.getUnitClassInfo( eUpgradeUnitClass )
		if( pUpgradeUnitClass.getMaxGlobalInstances() > -1 ) :
			continue
		if( pUpgradeUnitClass.getMaxPlayerInstances() > -1 ) :
			continue
		if( pUpgradeUnitClass.getMaxTeamInstances() > -1 ) :
			continue
		if( gc.getUnitInfo( eUnit ).getUpgradeUnitClass( eUpgradeUnitClass ) ) :
			if( LOG_DEBUG ) : CvUtil.pyPrint( "RandomEvents - found upgrade class: %s" % ( pUpgradeUnitClass.getDescription() ) )
			eUpgradeUnit = gc.getCivilizationInfo( pPlayer.getCivilizationType() ).getCivilizationUnits( eUpgradeUnitClass )
			
			if( eUpgradeUnit != UnitTypes.NO_UNIT ) :
				if( LOG_DEBUG ) : CvUtil.pyPrint( "RandomEvents - found upgrade unit: %s" % ( gc.getUnitInfo( eUpgradeUnit ).getDescription() ) )
				
				if( LOG_DEBUG ) : CvUtil.pyPrint( "RandomEvents - Searching for further upgrades..." )
				# replacing eUpgradeUnit with trainable upgrades
				eUpgradeUnit = recGetBestTrainableUnitFromUpgrade( eUpgradeUnit, pPlayer, pCity )
				if( LOG_DEBUG ) : CvUtil.pyPrint( "RandomEvents - new upgrade unit: %s" % ( gc.getUnitInfo( eUpgradeUnit ).getDescription() ) )
				
				if( canTrain( eUpgradeUnit, pPlayer, pCity ) ) :
					pUpgradeUnit = gc.getUnitInfo( eUpgradeUnit )
					# ">=": Favor upgrades
					if( pUpgradeUnit.getPowerValue() >= gc.getUnitInfo( eBestUnit ).getPowerValue() ) :
						if( LOG_DEBUG ) : CvUtil.pyPrint( "RandomEvents - Upgrade %s is better than current best %s" % ( pUpgradeUnit.getDescription(), gc.getUnitInfo( eBestUnit ).getDescription() ) )
						eBestUnit = eUpgradeUnit
	if( LOG_DEBUG ) : CvUtil.pyPrint( "RandomEvents - Returning unit %s" % ( gc.getUnitInfo( eBestUnit ).getDescription() ) )
	return eBestUnit

def canTrain( eUnit, pPlayer, pCity ) :
	if( pCity != None ) :
		return pCity.canTrain( eUnit, False, False )
	else :
		return pPlayer.canTrain( eUnit, False, False )

def canDoBestUnitFromUpgrades( eUnitClass, pPlayer, pCity = None ) :
	return getBestUnitFromUpgrades( eUnitClass, pPlayer, pCity ) != UnitTypes.NO_UNIT

def getBestUnitFromUpgradesHelp( sUnitClass, pPlayer, pCity = None, lsPromotions = [] ) :
	eUnit = getBestUnitFromUpgrades( gc.getInfoTypeForString( sUnitClass ), pPlayer, pCity )
	
	lePromotions = []
	for sPromotion in lsPromotions :
		ePromotion = gc.getInfoTypeForString( sPromotion )
		if( ePromotion >= 0 ) :
			lePromotions.append( ePromotion )
		else :
			BugUtil.error( "RandomEvents: getBestUnitFromUpgradesHelp() lsPromotions param contains invalid promotion type string: %s" % sPromotion )
			return ""
	
	if( eUnit == UnitTypes.NO_UNIT ) :
		return localText.getText( 'TXT_KEY_EVENT_NO_BONUS_UNIT_AVAILABLE', () )
	else :
		szUnit = gc.getUnitInfo( eUnit ).getDescription()
		szResult =  localText.getText( 'TXT_KEY_EVENT_BONUS_UNIT', ( 1, szUnit, ) )
		for ePromotion in lePromotions :
			szPromotion = gc.getPromotionInfo( ePromotion ).getDescription()
			szResult += localText.getText( 'TXT_KEY_NEWLINE', () )
			szResult += localText.getText( 'TXT_KEY_EVENT_UNIT_PROMOTION', ( szUnit, szPromotion, ) )
		return szResult

def initBestUnitFromUpgrades( eUnitClass, pPlayer, pCity = None, iPlotX = -1, iPlotY = -1, lsPromotions = [] ) :
	
	if( iPlotX < 0 or iPlotY < 0 ) :
		if( pCity != None ) :
	 		iPlotX = pCity.getX()
	 		iPlotY = pCity.getY()
		else :
			BugUtil.error( "RandomEvents: initBestUnitFromUpgrades() missing plot or city param" )
			return None
	
	eUnit = getBestUnitFromUpgrades( eUnitClass, pPlayer, pCity )
	
	lePromotions = []
	for sPromotion in lsPromotions :
		ePromotion = gc.getInfoTypeForString( sPromotion )
		if( ePromotion >= 0 ) :
			lePromotions.append( ePromotion )
		else :
			BugUtil.error( "RandomEvents: initBestUnitFromUpgrades() lsPromotions param contains invalid promotion type string: %s" % sPromotion )
			return None
	
	pUnit = pPlayer.initUnit(eUnit, iPlotX, iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	for ePromotion in lePromotions :
		 pUnit.setHasPromotion( ePromotion, True )
	
	return pUnit

	
## Utility test funcs
def testBUFU( iPlayer, sUnitClass ) :
	eUnit = getBestUnitFromUpgrades( gc.getInfoTypeForString( sUnitClass ), gc.getPlayer( iPlayer ) )
	if( eUnit == UnitTypes.NO_UNIT ) :
		return "NO_UNIT"
	else :
		return gc.getUnitInfo( eUnit ).getDescription()


######## GELA (lfgr: fixed)
def ApplyGela1(argsList):
	gc.getGame().changeScenarioCounter(1)

def ApplyGela2(argsList):
	gc.getGame().changeScenarioCounter(2)
	
def ApplyGela3(argsList):
	gc.getGame().changeScenarioCounter(3)
			
def ApplyGela4(argsList):
	gc.getGame().changeScenarioCounter(4)
		
def ApplyGela5(argsList):
	gc.getGame().changeScenarioCounter(5)
		
def ApplyGela6(argsList):
	gc.getGame().changeScenarioCounter(6)
		
def ApplyGela7(argsList):
	gc.getGame().changeScenarioCounter(7)
		
def CanDoGela4(argsList):
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'))
	if 	iPlayer2 != -1:
		return True
	return False				

def CanDoGela2(argsList):
	iImp = gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def CanDoGela3(argsList):
	iImp = gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True
	
def CanDoGela5(argsList):
	iImp = gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def CanDoGela6(argsList):
	iImp = gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True
	
def CanDoGela7(argsList):
	iImp = gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		if( CyMap().getArea(i).getNumImprovements(iImp) > 0 ) :
			return True
	return False

######## STRANGE_ADEPT (lfgr: tweaked, moved to XML)

######## HELL_REFUGEES (lfgr: tweaked, moved to XML)

def CanDoHellRefugees(argsList):
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if (pPlayer2.isAlive()):
			if pPlayer2.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				return true
	return false

def doHellRefugees5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	
	eTeam = gc.getTeam(pPlayer.getTeam())
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if (pPlayer2.isAlive() and pPlayer2 != pPlayer  and iPlayer2 != gc.getBARBARIAN_PLAYER()):
			iReligion = pPlayer2.getStateReligion()
			if iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				i2Team = gc.getPlayer(iPlayer2).getTeam()
				if eTeam.isAtWar(i2Team):
					eTeam.makePeace(i2Team)	

######## SCHOLARS (lfgr: tweaked)

def CanDoScholars2(argsList):
	return cityHasBuilding( argsList, 'BUILDING_LIBRARY' )

def helpScholars2(argsList):
	return cityReqBuildingHelp( argsList, 'BUILDING_LIBRARY' )
			
def CanDoScholars4(argsList):
	return playerHasTrait( argsList, 'TRAIT_BARBARIAN' )

def helpScholars4( argsList ):
	return playerReqTraitHelp( argsList, 'TRAIT_BARBARIAN' )

######## TRAPPED_FROSTLINGS (lfgr: tweaked)

def CanTriggerTrappedFrostlings (argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	for iiX in range(iX-3, iX+3, 1):
				for iiY in range(iY-3, iY+3, 1):
					pPlot2 = CyMap().plot(iiX,iiY)
					iTerrain = pPlot2.getTerrainType()
					if iTerrain == iTundra:
						return true
					if iTerrain == iSnow:
						return true
	return false
	
def DoTrappedFrostlings2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit = gc.getInfoTypeForString('UNIT_FROSTLING')
	pBestPlot = -1
	iBestPlot = -1
	iX = pCity.getX()
	iY = pCity.getY()
	for iiX in range(iX-3, iX+3, 1):
				for iiY in range(iY-3, iY+3, 1):
					pPlot2 = CyMap().plot(iiX,iiY)
					if not pPlot2.isWater() and not pPlot2.isImpassable():
						if pPlot2.getNumUnits() == 0:
							if not pPlot2.isCity():
								iPlot = CyGame().getSorenRandNum(500, "Frostlings")
								if iPlot > iBestPlot:
									iBestPlot = iPlot
									pBestPlot = pPlot2
	if iBestPlot != -1:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

def CanDoTrappedFrostlings3(argsList):
	return cityHasBuilding( argsList, 'BUILDING_FREAK_SHOW' )
	
def helpTrappedFrostlings3(argsList):
	return cityReqBuildingHelp( argsList, 'BUILDING_FREAK_SHOW' )

######## PACIFIST_DEMONSTRATION (lfgr: tweaked)

def canTriggerPacifistDemonstration(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if not gc.getTeam(pPlayer.getTeam()).canChangeWarPeace(destPlayer.getTeam()):
		return False
	if gc.getTeam(pPlayer.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10:
		return False
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		return False
	return True	
	
def DoPacifistDemonstration2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.changeWarWeariness(destPlayer.getTeam(),35)

def DoPacifistDemonstration3(argsList):
	# TODO: Revolt turns and experience should scale with number of units
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	for i in range(pCity.plot().getNumUnits()):
		pUnit = pCity.plot().getUnit(i)
		pUnit.changeExperience(3, -1, False, False, False)

def CanDoPacifistDemonstration4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	return playerHasTrait( argsList, 'TRAIT_BARBARIAN' ) and canDoBestUnitFromUpgrades( gc.getInfoTypeForString( "UNITCLASS_WARRIOR" ), pPlayer, pCity )

def helpPacifistDemonstration4( argsList ):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	szResult = playerReqTraitHelp( argsList, 'TRAIT_BARBARIAN' )
	szResult += localText.getText( 'TXT_KEY_NEWLINE', () )
	szResult += getBestUnitFromUpgradesHelp( 'UNITCLASS_WARRIOR', pPlayer, pCity, ['PROMOTION_WEAK'] )
	return szResult

def DoPacifistDemonstration4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	# newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	initBestUnitFromUpgrades( gc.getInfoTypeForString( "UNITCLASS_WARRIOR" ), pPlayer, pCity, -1, -1, ['PROMOTION_WEAK'] )
	
def DoPacifistDemonstration5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	eTeam = gc.getTeam(pPlayer.getTeam())
	eTeam.changeWarWeariness(pPlayer.getTeam(),-10)
	for pUnit in PyPlayer( kTriggeredData.ePlayer ).getUnitList() :
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRISM')):
			pUnit.changeExperience(3, -1, False, False, False)

######## DEMON_SIGN (lfgr: tweaked, TOTEST)

def CanTriggerDemonSign (argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_MERCURIANS")):
		return False
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_INFERNALS")):
		return False
	return True

def CanDoDemonSign5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	return canDoBestUnitFromUpgrades( gc.getInfoTypeForString( "UNITCLASS_WARRIOR" ), pPlayer, pCity )

def helpDemonSign5( argsList ):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	return getBestUnitFromUpgradesHelp( 'UNITCLASS_WARRIOR', pPlayer, pCity, ['PROMOTION_PROPHECY_MARK'] )
	
def	doDemonSign5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	initBestUnitFromUpgrades( gc.getInfoTypeForString( "UNITCLASS_WARRIOR" ), pPlayer, pCity, -1, -1, ['PROMOTION_PROPHECY_MARK'] )
	
######## (lfgr: not fixed)

def CanDoAshCough2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SHEAIM")):
		return true
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_KURIOTATES")):
		return true
	return false

def CanDoAshCough4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD')) == 0:
		return False
	return True

def doAshCough4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Cough")< 50 :
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1'), True)
	else: 
		pCity.changeHurryAngerTimer(10)

def CanDoDeadAngel2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
		return False
	return true
	
def doDeadAngel4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.changePlotCounter(100)
	
def doDeadAngel5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUE_CARRIER'), True)
	
def doDevastatingPlague1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	iPop = pCity.getPopulation()
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	pCity.setPopulation(iPop)
	for i in range((pCity.plot()).getNumUnits()):
		pUnit = (pCity.plot()).getUnit(i)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED'), True)
	
def doDevastatingPlague4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	iPop = pCity.getPopulation()
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	pCity.setPopulation(iPop)
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	for i in range(0,iPop,1): 
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
def doMassiveSuicide5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
def CanDoNecroCannibalism2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
		return False
	return true
	
def doNecroCannibalism2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	iPop = pCity.getPopulation()
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	pCity.setPopulation(iPop)
	for i in range(0,iPop,1): 
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WARRIOR'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNIBALIZE'), True)
	
def	doNecroCannibalism4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def canTriggerHellPortalCity(argsList):
	# TODO: This should cause an error...
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS')) == 0:
			return True
		return False
	return False

def doHellPortal(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'), 1)

def doGhostShip (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	irand = CyGame().getSorenRandNum(120, "GhostShip")
	iX = pCity.getX()
	iY = pCity.getY()
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	if irand<20 :
		for iiX in range(iX-2, iX+2, 1):
			for iiY in range(iY-2, iY+2, 1):
				pPlot2 = CyMap().plot(iiX,iiY)
				if pPlot2.isWater():
					if pPlot2.getNumUnits() == 0:
						newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), iiX, iiY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_1",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	if irand>=20:
		if irand<40:
			pCity.changeEspionageHealthCounter(5)
			CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_2",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if irand>=40:
			if irand<60:
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_3",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)

			if irand>=60:
				if irand<80:
					pPlayer.changeGold(50)
					CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_4",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if irand>=80:
					if irand<100:
						pCity.changeHurryAngerTimer(5)
						CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_5",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)

					if irand>=100:					
						iPlayer = kTriggeredData.ePlayer
						cf.placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_TREASURE'))
						CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_6",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

						
def doOrphanedGoblin1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC_SLAYING'), True)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
	
def doOrphanedGoblin2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)

def doOrphanedGoblin3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iBestValue = 0
	pBestPlot = -1
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iX = pUnit.getX()
	iY = pUnit.getY()
	for iiX in range(iX-2, iX+2, 1):
		for iiY in range(iY-2, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			iValue = 0
			if not pPlot.isWater():
				if not pPlot.isPeak():
					if pPlot.getNumUnits() == 0:
						iValue = CyGame().getSorenRandNum(1000, "Goblin1")
						if iValue > iBestValue:
							iBestValue = iValue
							pBestPlot = pPlot
	if (pBestPlot!=-1):						
		if CyGame().getSorenRandNum(1000, "Goblin1")<500:
			newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN'), pBestPlot.getX(),pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)
		
		if CyGame().getSorenRandNum(1000, "Goblin1")>500:
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN'), pBestPlot.getX(),pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

def doOrphanedGoblin4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.changeExperience(1* -1, -1, False, False, False)
	pCity = pPlayer.getCapitalCity()
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
# lfgr: fixed
def doThatKindOfDay1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	pCity.setPopulation(1)
	
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if pUnit2.getOwner()== gc.getBARBARIAN_PLAYER():
					if not isWorldUnitClass(pUnit2.getUnitClassType()):
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)
		
# lfgr: fixed							
def doThatKindOfDay2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	pCity.setProduction(0)

	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if pUnit2.getOwner()== gc.getBARBARIAN_PLAYER() :
					if not isWorldUnitClass(pUnit2.getUnitClassType()):				
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)
									


def canDoThatKindOfDay3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.isHuman() == False:
		return False
	if CyGame().getRankPlayer(CyGame().countCivPlayersAlive()-1) == kTriggeredData.ePlayer:
		return False

	if CyGame().getWBMapScript():
		return False
	return True
	
def doThatKindOfDay3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iNewPlayer = CyGame().getRankPlayer(CyGame().countCivPlayersAlive()-1)
	iOldPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer2 = gc.getPlayer(CyGame().getRankPlayer(CyGame().countCivPlayersAlive()-1 ))
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, -1)
	
# lfgr: fixed
def doThatKindOfDay4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if pUnit2.getOwner()== gc.getBARBARIAN_PLAYER() :
					if not isWorldUnitClass(pUnit2.getUnitClassType()):				
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)
									
	
# lfgr: fixed
def doThatKindOfDay5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	pCity.changePopulation(1)
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if pUnit2.getOwner()== gc.getBARBARIAN_PLAYER() :
					if not isWorldUnitClass(pUnit2.getUnitClassType()):				
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)

# lfgr: fixed
def CanTriggerThatKindOfDay(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	
#	if (pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')):
	if ( gc.getTeam( pPlayer.getTeam() ).isAtWar( gc.getBARBARIAN_TEAM() ) ):
		if (gc.getGame().getGameTurnYear())<100:
			if pPlayer.getNumCities()==1 :
				pCity = pPlayer.getCapitalCity()
				iX = pCity.getX()
				iY = pCity.getY()			

				pPlot=CyMap().plot(iX,iY)
				if pPlot.getNumUnits() == 0:
					for iiX in range(iX-2, iX+3, 1):
						for iiY in range(iY-2, iY+3, 1):
							pPlot2 = CyMap().plot(iiX,iiY)
							for i in range(pPlot2.getNumUnits()):
								pUnit2 = pPlot2.getUnit(i)
								if pUnit2.getOwner()== gc.getBARBARIAN_PLAYER():
									if not isWorldUnitClass(pUnit2.getUnitClassType()):					
										return true

	return false

	

def canDoThatKindOfDay4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE')) == True:
		return True
	return False

def canDoThatKindOfDay5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_KURIOTATES")):
		return True
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ELOHIM")):
		return True
	return False

def CanDoPrincessRule4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALACE_MERCURIANS')) == 0:
		return False
	else: 
		if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALACE_INFERNAL')) == 0:
			return False
	return True

def CanDoCorruptJudge4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_MEMBERSHIP')) != gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'):
		return False
	return True

def CanDoWaywardElves2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_LJOSALFAR")):
		return True
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SVARTALFAR")):
		return True
	return False
	
def CanDoWaywardElves4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) != gc.getInfoTypeForString('CIVIC_SLAVERY'):
		return False
	return True
	
def doWayWardElves4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE'), pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE'), pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)

def doWayWardElves5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEXTEROUS'), True)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)

def doBoardGame4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ORDER'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INQUISITOR'), True)

def doWayWardElves1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_HAMLET'))

def doTraveller1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL') :
			implist = implist + [pPlot]
	pPlot= implist[CyGame().getSorenRandNum(len(implist), "Pick Plot")-1]
	pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)

def doTraveller2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA') :
			implist = implist + [pPlot]
	pPlot= implist[CyGame().getSorenRandNum(len(implist), "Pick Plot")-1]
	pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
	
def doTraveller3 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS') :
			implist = implist + [pPlot]
	pPlot= implist[CyGame().getSorenRandNum(len(implist), "Pick Plot")-1]
	pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
	
	
def doTraveller4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS') :
			implist = implist + [pPlot]
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER') :
			implist = implist + [pPlot]
	pPlot= implist[CyGame().getSorenRandNum(len(implist), "Pick Plot")-1]
	pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
	
def doTraveller5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	maxpop=-1
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			
			for pyCity in PyPlayer(iPlayer).getCityList() :
				pCity = pyCity.GetCy()
				if pCity.getPopulation() > maxpop:
					maxpop = pCity.getPopulation()
					pPlot= pCity.plot()
	pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
	
def CanDoTraveller1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL') :
			return true
	return false
	
def CanDoTraveller2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA') :
			return true
	return false
	
def CanDoTraveller3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS') :
			return true
	return false
	
def CanDoTraveller4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS') :
			return true
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER') :
			return true
	return false
	
def CanTriggerUnfortunateAssassinCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return true
	return false

def doUnfortunateAssassin3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pdestPlayer = pPlayer
	minattitude=0
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer != pPlayer :
				test= CyGame().getSorenRandNum(100, "Pick CIV")
				if test > minattitude :
					pdestPlayer=pLoopPlayer
					minattitude = test
	if CyGame().getSorenRandNum(100, "Pick Plot")<50 :
		pdestPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer,-1)
	else:
		pdestPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer,1)

def doUnfortunateAssassin5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def CanDoOvercrowdedDungeon5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
		return False
	return true

def doOvercrowdedDungeon5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Riot")<25 :
		pCity.changeOccupationTimer(5)

def spawnAncientWarrior( argsList ) :
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	
	CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_ANCIENT_BURIAL_X_WARRIOR_RISES",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),kTriggeredData.iPlotX,kTriggeredData.iPlotY,True,True)
	
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	newUnit = pBarbPlayer.initUnit(gc.getInfoTypeForString('UNIT_SKELETON'), kTriggeredData.iPlotX, kTriggeredData.iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName("Ancient Warrior")		
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
		
def doAncientBurial2 (argsList):
	if CyGame().getSorenRandNum(100, "Skeleton")<20 :
		spawnAncientWarrior( argsList )
		
def doAncientBurial3 (argsList):
	if CyGame().getSorenRandNum(100, "Skeleton")<90 :
		spawnAncientWarrior( argsList )
		
def doAncientBurial4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if CyGame().getSorenRandNum(100, "Skeleton")<40 :
		spawnAncientWarrior( argsList )
	else:
		CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_ANCIENT_BURIAL_4_JEWELRY",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),kTriggeredData.iPlotX,kTriggeredData.iPlotY,True,True)
		pPlayer.changeGold(90)

def doMadGolemicist2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHEUT_STONE'), True)
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	pPlot = pUnit.plot()
	pNewPlot = cf.findClearPlot(-1, pPlot)
	if pNewPlot != -1:
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOOD_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOOD_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
def doMadGolemicist3 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pPlot = pUnit.plot()
	if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_BARNAXUS'):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_BARNAXUS",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		pUnit.kill(True, PlayerTypes.NO_PLAYER)
	if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_GOLEM",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_STRENGTH'), True)
	else:
		if CyGame().getSorenRandNum(100, "Golem")<50 :
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_HUMAN_1",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FLESH_GOLEM'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_HUMAN_2",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER1'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER2'), True)		
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER3'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER4'), True)		
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER5'), True)	
			
def doMonkPilgrimage2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRST_PILGRIMAGE'), True)
	
def CanDoMonkPilgrimage2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isHuman():
		return true
	return false
	
def doElderDeath3 (argsList): 
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SKELETON'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def canTriggerSkilledJeweler(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_JEWELER')) > 0:
		return False
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
		return False
	return True	
				
######## MORE EVENTS MOD EXPANDED STARTS ########

def canTriggerInfernalFilter(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		return False
	return True

				# More Events Mod Ends #		

def canTriggerAshenVeilFilter(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		return False
	return True

def CanDoOil3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_KHAZAD")):
		return True
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_LUCHUIRP")):
		return True
	return False
	
def helpPoisonedWater3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_POISONED_WATER_HELP_3", ())
	return szHelp

def helpPoisonedWater4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_POISONED_WATER_HELP_4", ())
	return szHelp


def canTriggerDemonicTower(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		return False	
	return True


def doDemonicTower1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_BALOR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
      	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
      	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED'), True)


def helpDemonicTower1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEMONIC_TOWER_HELP_1", ())
	return szHelp


def canTriggerRalphAndSam(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		return False	
	return True

def doRalphAndSam1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOLF_PACK'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
      	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)

def helpRalphAndSam1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_RALPH_AND_SAM_HELP_1", ())
	return szHelp
	
	
def doCentaurTribe1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_CENTAUR_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
      	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)


def helpCentaurTribe1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_CENTAUR_TRIBE_HELP_1", ())
	return szHelp


def doSeaSerpent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_SEA_SERPENT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
      	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)


def helpSeaSerpent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_SEASERPENT_HELP_1", ())
	return szHelp

def doMonkeySee1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def helpMonkeySee1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_MONKEY_SEE_HELP_1", ())
	return szHelp

def canTriggerLanunPirates(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	map = gc.getMap()

#   If Barbarians are disabled in this game, this event will not occur.
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		return False

#   If Lanun already exist in this game, this event will not occur.
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)	
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
			return false
	return true


#   At least one civ on the board must know Optics
	bFoundValid = false
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_OPTICS')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = true
				break

	if not bFoundValid:
		return False


#	Find an eligible plot
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true)):
			return True

	return False

def getHelpLanunPirates1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_LANUN_PIRATES_HELP_1", ())	

	return szHelp

def applyLanunPirates1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	listPlots = []
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, true)):
			listPlots.append(i)

	if 0 == len(listPlots):
		return

	plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Lanun Pirates event location")])

	if map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_DUEL'):
		iNumUnit1  = 2
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_TINY'):
		iNumUnit1  = 2
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_SMALL'):
		iNumUnit1  = 3
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_STANDARD'):
		iNumUnit1  = 4
	elif map.getWorldSize() == CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), 'WORLDSIZE_LARGE'):
		iNumUnit1  = 5
	else: 
		iNumUnit1  = 6

	iUnitType1 = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_PRIVATEER')


	barbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	for i in range(iNumUnit1):
		barbPlayer.initUnit(iUnitType1, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_SEA, DirectionTypes.DIRECTION_SOUTH)

	(loopUnit, iter) = barbPlayer.firstUnit(false)
	while (loopUnit):
		if loopUnit.getUnitType() == iUnitType1:
			loopUnit.setName("Lanun Raider")
		(loopUnit, iter) = barbPlayer.nextUnit(iter, false)


def canTriggerKuriotatesWorkboat(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
		return False
	return True
	
	
def canTriggerCityKuriotatesWorkboat(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if not pCity.isSettlement():
		return False
	return True
	
def doHauntedCastle4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_SPECTRE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setName("Vengeful Dead")
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)			

def helpHauntedCastle4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_HAUNTED_CASTLE_HELP_4", ())
	return szHelp
	
######## MORE EVENTS MOD EXPANDED ENDS ########