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
	"""
		Unit must have the Marksman promotion
		Unit must be not summoned
	"""
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iMark = gc.getInfoTypeForString('PROMOTION_MARKSMAN')
	if not pUnit.isHasPromotion(iMark):
		return False
	if pUnit.getDuration() > 0:
		return False
	if pUnit.getSummoner() != -1:
		return False
	return True

def canTriggerAmuriteTrialUnit(argsList):
	"""
		Unit must not be hidden nationality
	"""
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isHiddenNationality() :
		return False
	return True

def applyAmuriteTrial1(argsList):
	"""
		Moves the unit to the amurite capital
	"""
	# LFGR_TODO: open borders?
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iPlayer2 = cf.getCivilization(gc.getInfoTypeForString('CIVILIZATION_AMURITES'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pCity = pPlayer2.getCapitalCity()
		pUnit.setXY(pCity.getX(), pCity.getY(), False, True, True)

def doArmageddonApocalypse(argsList):
	"""
		Kills half of all non-fallow cities' population
		Kills about 60% of living units. (defined by APOCALYPSE_KILL_CHANCE)
	"""
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
	"""
		Spawns Ars Moriendi
	"""
	kTriggeredData = argsList[0]
	iUnit = gc.getInfoTypeForString('UNIT_ARS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		cf.addUnit(iUnit)

def doArmageddonBlight(argsList):
	# TODO: non-fallow?
	"""
		Adds an random amount of unhealthiness to all non-infernal cities, increasing with unhealthiness present in city
		Does about 25% death damage to all living units, to a limit of 50%
	"""
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	pPlayer = gc.getPlayer(iPlayer)
	py = PyPlayer(iPlayer)
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		for pyCity in py.getCityList():
			pCity = pyCity.GetCy()
			i = CyGame().getSorenRandNum(15, "Blight")
			i += pCity.getPopulation()
			i += pCity.getFeatureBadHealth()
			i -= pCity.getFeatureGoodHealth()
			i -= pCity.totalGoodBuildingHealth()
			if i > 0:
				pCity.changeEspionageHealthCounter(i)
	for pUnit in py.getUnitList():
		if pUnit.isAlive():
			pUnit.doDamageNoCaster(25, 100, gc.getInfoTypeForString('DAMAGE_DEATH'), False)

def doArmageddonBuboes(argsList):
	"""
		Spawns Buobes
	"""
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
			pUnit.doDamageNoCaster(25, 100, gc.getInfoTypeForString('DAMAGE_DEATH'), False)

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
	if not pPlot.isNone():
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_AZER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

######## BANDIT_NIETZ (lfgr: moved to XML)

def doBanditNietz3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HORSEMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName("Nietz the Bandit Lord")
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BOUNTY_HUNTER'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)

######## CALABIM_SANCTUARY (lfgr: fixed, moved to XML)

######## CITY_FEUD_ARSON (lfgr: moved to XML)

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

######## CITY_SPLIT

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

######## SOVERIGN_CITY

def doSoverignCity1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	cf.formEmpire(pPlayer.getCivilizationType(), gc.getInfoTypeForString('LEADER_KOUN'), pPlayer.getTeam(), pCity, pPlayer.getAlignment(), pPlayer)

######## DISSENT (lfgr: moved to XML)

def doDissent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if gc.getGame().getSorenRandNum(100, "Dissent 1") < 50:
		pCity.changeOccupationTimer(2)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_1", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

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

def canApplyDissent4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) != gc.getInfoTypeForString('CIVIC_SOCIAL_ORDER'):
		return False
	return True

######## (lfgr: not reviewed)

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
		pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True)
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
			if not pPlot.isNone():
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
			if not pPlot.isNone():
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
			if not pPlot.isNone():
				pPlot.changePlotCounter(-100)
	CyGame().changeGlobalCounter(-2)

def doFlareNatureNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_BLOOM'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_BLOOM",point.x,point.y,point.z)
	iForestNew = gc.getInfoTypeForString('FEATURE_FOREST_NEW')
	iLjos = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
	iSvart = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if not pPlot.isNone():
				if pPlot.canHaveFeature(iForestNew): #This checks for valid terrain and whether there is already a feature on the tile
					if pPlot.getImprovementType() == -1:
						pPlot.setFeatureType(iForestNew, 0)
					elif pPlot.isOwned():
						iCiv = gc.getPlayer(pPlot.getOwner()).getCivilizationType()
						if iCiv == iLjos or iCiv == iSvart:
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
			if not pPlot.isNone():
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
	if not pPlot.isNone():
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
	pPlayer.acquireCity(pCity,False,False)

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
	pPlayer.acquireCity(pCity,False,False)

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
	pPlayer.acquireCity(pCity,False,False)

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

######## LETUM_FRIGUS (lfgr: moved to XML)

def doLetumFrigus3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE'),True)

######## (lfgr: not reviewed)

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
		pUnit.setXY(pCity.getX(), pCity.getY(), False, True, True)

######## MARKET_THEFT (lfgr: moved to XML)

def doMarketTheft2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iRnd = gc.getGame().getSorenRandNum(21, "Market Theft 2") - 10
	pCity.changeCrime(iRnd)

######## (lfgr: not reviewed)

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
	pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_MUSHROOMS'))

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

######## ORDER_VS_VEIL (lfgr: moved to XML)

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
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

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
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

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

######## ORDER_VS_VEIL_TEMPLE (lfgr: moved to XML)

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
	(loopCity, iter) = player.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = player.nextCity(iter, False)

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
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

# lfgr added
def canTriggerOvercouncil(argsList):
	return semiRandomTurnTrigger( 10, 0.25 )
# lfgr end

######## (lfgr: not reviewed)

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
	pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_PENGUINS'))

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

def doSignArawn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iUndead = gc.getInfoTypeForString('PROMOTION_UNDEAD')
	apUnitList = PyPlayer(iPlayer).getUnitList()
	for pUnit in apUnitList:
		if pUnit.isHasPromotion(iUndead):
			pUnit.changeImmobileTimer(1)
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

######## VEIL_VS_ORDER_TEMPLE (lfgr: moved to XML)

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
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

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
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

######## (lfgr: not reviewed)

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

# lfgr
# REPLACE
# \Qdef canApplyTrait\E([^(]*)\Q(argsList):\E\r\n\t\QiEvent = argsList[0]\E\r\n\t\QkTriggeredData = argsList[1]\E\r\n\t\QpPlayer = gc.getPlayer(kTriggeredData.ePlayer)\E\r\n\t\Qif gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('\E([^']*)\Q'):\E\r\n\t\t\Qreturn False\E\r\n\t\Qreturn True\E
# WITH
# def canApplyTrait\1\(argsList\):\r\n\tiEvent = argsList[0]\r\n\tkTriggeredData = argsList[1]\r\n\tpPlayer = gc.getPlayer\(kTriggeredData.ePlayer\)\r\n\tif gc.getLeaderHeadInfo\(pPlayer.getLeaderType\(\)\).getPermanentTrait\(\) == gc.getInfoTypeForString\('\2'\):\r\n\t\treturn False\r\n\treturn True\r\n\r\n# lfgr: adaptive event help\r\ndef helpTrait\1\(argsList\) :\r\n\treturn CyGameTextMgr\(\).parseTraits\( gc.getInfoTypeForString\('\2'\), CivilizationTypes.NO_CIVILIZATION, False \)\r\n# lfgr end
# lfgr end

def canApplyTraitAggressive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_AGGRESSIVE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitAggressive(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_AGGRESSIVE'), CivilizationTypes.NO_CIVILIZATION, False )
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

def canApplyTraitArcane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_ARCANE'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitArcane(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_ARCANE'), CivilizationTypes.NO_CIVILIZATION, False )
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
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_CHARISMATIC'), CivilizationTypes.NO_CIVILIZATION, False )
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
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_CREATIVE'), CivilizationTypes.NO_CIVILIZATION, False )
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
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_EXPANSIVE'), CivilizationTypes.NO_CIVILIZATION, False )
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
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_FINANCIAL'), CivilizationTypes.NO_CIVILIZATION, False )
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

def canApplyTraitIndustrious(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitIndustrious(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_INDUSTRIOUS'), CivilizationTypes.NO_CIVILIZATION, False )
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
				iTraitCount += 1

	Traits = [ 'TRAIT_AGGRESSIVE','TRAIT_ARCANE','TRAIT_CHARISMATIC','TRAIT_CREATIVE','TRAIT_EXPANSIVE','TRAIT_FINANCIAL','TRAIT_INDUSTRIOUS','TRAIT_ORGANIZED','TRAIT_PHILOSOPHICAL','TRAIT_RAIDERS','TRAIT_SPIRITUAL' ]

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
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_ORGANIZED'), CivilizationTypes.NO_CIVILIZATION, False )
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
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL'), CivilizationTypes.NO_CIVILIZATION, False )
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
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_RAIDERS'), CivilizationTypes.NO_CIVILIZATION, False )
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

def canApplyTraitSpiritual(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == gc.getInfoTypeForString('TRAIT_SPIRITUAL'):
		return False
	return True

# lfgr: adaptive event help
def helpTraitSpiritual(argsList) :
	return CyGameTextMgr().parseTraits( gc.getInfoTypeForString('TRAIT_SPIRITUAL'), CivilizationTypes.NO_CIVILIZATION, False )
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
	if not pUnit.isAlive():
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
	eTeam.declareWar(enemyTeam, True, WarPlanTypes.WARPLAN_TOTAL)
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
	pPlayer.acquireCity(pCity,False,False)

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
			eTeam.declareWar(iLjosalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

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
			eTeam.declareWar(iLjosalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

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
			eTeam.declareWar(iSvartalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

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
			eTeam.declareWar(iSvartalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

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
	eTeam.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
	eTeam7.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
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
	eTeam.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
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

###############################
######## BTS EVENTS ###########
###############################

######## MARATHON ###########

def canTriggerMarathon(argsList):	
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	team = gc.getTeam(player.getTeam())
	
	if (team.AI_getAtWarCounter(otherPlayer.getTeam()) == 1):
		(loopUnit, iter) = otherPlayer.firstUnit(False)
		while( loopUnit ):
			plot = loopUnit.plot()
			if (not plot.isNone()):
				if (plot.getOwner() == kTriggeredData.ePlayer):
					return True
			(loopUnit, iter) = otherPlayer.nextUnit(iter, False)

	return False

######## WEDDING FEUD ###########

def doWeddingFeud2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = player.firstCity(False)

	while(loopCity):
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(30)
		(loopCity, iter) = player.nextCity(iter, False)
		
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
		return False

	return True

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
			gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)

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
		gc.getTeam(destPlayer.getTeam()).declareWar(player.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)

	return 0

def getHelpWeddingFeud3(argsList):
	iEvent = argsList[0]
	event = gc.getEventInfo(iEvent)
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_3_HELP", (1, religion.getChar()))

	return szHelp

######## BABY BOOM ###########

def canTriggerBabyBoom(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())

	if team.getAtWarCount(True) > 0:
		return False

	for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
		if iLoopTeam != player.getTeam():
			if team.AI_getAtPeaceCounter(iLoopTeam) == 1:
				return True

	return False

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
			CyInterface().addMessage(kTriggeredData.eOtherPlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), True, True)
			city.setNumRealBuilding(iBuilding, 0)
			iNumBuildingsDestroyed += 1
			listBuildings.remove(iBuilding)
				
	if iNumBuildingsDestroyed > 0:
		szBuffer = localText.getText("TXT_KEY_EVENT_NUM_BUILDINGS_DESTROYED", (iNumBuildingsDestroyed, gc.getPlayer(kTriggeredData.eOtherPlayer).getCivilizationAdjectiveKey(), city.getNameKey()))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_WHITE"), -1, -1, True, True)

######## BROTHERS IN NEED ###########

def canTriggerBrothersInNeed(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	
	if not player.canTradeNetworkWith(kTriggeredData.eOtherPlayer):
		return False
	
	listResources = []
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IRON'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IVORY'))

#FfH: Modified by Kael 10/01/2007
#	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_OIL'))
#	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_URANIUM'))
#FfH: End Modify
	
	bFound = False
	for iResource in listResources: 
		if (player.getNumTradeableBonuses(iResource) > 1 and otherPlayer.getNumAvailableBonuses(iResource) <= 0):
			bFound = True
			break
		
	if not bFound:
		return False
		
	for iTeam in range(gc.getMAX_CIV_TEAMS()):
		if iTeam != player.getTeam() and iTeam != otherPlayer.getTeam() and gc.getTeam(iTeam).isAlive():
			if gc.getTeam(iTeam).isAtWar(otherPlayer.getTeam()) and not gc.getTeam(iTeam).isAtWar(player.getTeam()):
				return True
			
	return False
	
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
		return False
		
	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False
		
	if city.plot().getLatitude() <= 0:
		return False
		
	if city.getPopulation() < 2:
		return False
		
	return True

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
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), True, True)
		city.setNumRealBuilding(iBuilding, 0)

	if len(listExpensiveBuildings) > 0:
		iBuilding = listExpensiveBuildings[gc.getGame().getSorenRandNum(len(listExpensiveBuildings), "Hurricane event expensive building destroyed")]
		szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), gc.getInfoTypeForString("COLOR_RED"), city.getX(), city.getY(), True, True)
		city.setNumRealBuilding(iBuilding, 0)

		
######## CYCLONE ###########

def canTriggerCycloneCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return False
		
	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False
		
	if city.plot().getLatitude() >= 0:
		return False
		
	return True

######## MONSOON ###########

def canTriggerMonsoonCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return False
		
	if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False
		
	iJungleType = CvUtil.findInfoTypeNum(gc.getFeatureInfo, gc.getNumFeatureInfos(),'FEATURE_JUNGLE')
		
	for iDX in range(-3, 4):
		for iDY in range(-3, 4):
			pLoopPlot = plotXY(city.getX(), city.getY(), iDX, iDY)
			if not pLoopPlot.isNone() and pLoopPlot.getFeatureType() == iJungleType:
				return True
				
	return False

######## VOLCANO ########### lfgr: moved to XML

# LFGR_TODO: canApply should be in Trigger

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
			CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getImprovementInfo(iImprovement).getButton(), gc.getInfoTypeForString("COLOR_RED"), plot.getX(), plot.getY(), True, True)
			if iImprovement in listRuins:
				plot.setImprovementType(iRuins)
			else:
				plot.setImprovementType(-1)
			listPlots.remove(plot)
			
			if i == 1 and gc.getGame().getSorenRandNum(100, "Volcano event num improvements destroyed") < 50:
				break

######## DUSTBOWL ########### (lfgr: moved to XML)

def canTriggerDustbowlCont(argsList):
	kTriggeredData = argsList[0]

	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	kOrigTriggeredData = player.getEventOccured(trigger.getPrereqEvent(0))
	
	if (kOrigTriggeredData == None):
		return False

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
		return False
		
	return True

######## CHAMPION ########### (lfgr: tweaked, moved to XML)

def canTriggerChampion(argsList):	
	kTriggeredData = argsList[0]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())

	if team.getAtWarCount(True) > 0:
		return False
				
	return True
	
def canTriggerChampionUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	unit = player.getUnit(iUnit)
	
	if unit.isNone():
		return False
		
	if unit.getDamage() > 0:
		return False

#FfH: Modified by Kael 09/26/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify

	if unit.isHasPromotion(iLeadership):
		return False

	return True
	
def applyChampion(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

#FfH: Modified by Kael 10/01/2007
#	iLeadership = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_LEADERSHIP')
	iLeadership = gc.getInfoTypeForString('PROMOTION_HERO')
#FfH: End Modify
	
	unit.setHasPromotion(iLeadership, True)
	
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

######## ANTELOPE ###########

def canTriggerAntelope(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_DEER')
	iHappyBonuses = 0
	bDeer = False
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return False
			if i == iDeer:
				return False	

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iDeer, False):
		return False
				
	return True

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
	bWhale = False
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = player.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return False
			if i == iWhale:
				return False

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iWhale, False):
		return False
		
	return True

######## ANCIENT OLYMPICS ###########

def doAncientOlympics2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	map = gc.getMap()

	for j in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(j)
		if j != kTriggeredData.ePlayer and loopPlayer.isAlive() and not loopPlayer.isMinorCiv():

			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if not plot.isWater() and plot.getOwner() == kTriggeredData.ePlayer and plot.isAdjacentPlayer(j, True):
					loopPlayer.AI_changeMemoryCount(kTriggeredData.ePlayer, MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 1)
					break
		
	return 1

def getHelpModernOlympics(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	
	szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1, ))	

	return szHelp

######## HEROIC_GESTURE ###########

def canTriggerHeroicGesture(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not gc.getTeam(destPlayer.getTeam()).canChangeWarPeace(player.getTeam()):
		return False
		
	if gc.getTeam(destPlayer.getTeam()).AI_getWarSuccess(player.getTeam()) <= 0:
		return False

	if gc.getTeam(player.getTeam()).AI_getWarSuccess(destPlayer.getTeam()) <= 0:
		return False
	
	return True

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
		return False
		
	if gc.getTeam(player.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10:
		return False

	return True

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
	"""
		+1 Attitude from all known players
	"""
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

######## LITERACY ###########

def canTriggerLiteracy(argsList):

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
	if player.getNumCities() > player.getBuildingClassCount(iLibrary):
		return False
	
	return True

######## ESTEEMEED_PLAYWRIGHT ###########

def canTriggerEsteemedPlaywright(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	
	# If source civ is operating this Civic, disallow the event to trigger.
	if player.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_SLAVERY')):
		return False

	return True

######## EXPERIENCED_CAPTAIN ########### (lfgr: tweaked, moved to XML)

######## HOSTILE TAKEOVER ###########

######## Great Beast ########

def doGreatBeast3(argsList):
	kTriggeredData = argsList[1]
	
	player = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = player.firstCity(False)

	while(loopCity):
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(40)
		(loopCity, iter) = player.nextCity(iter, False)

def getHelpGreatBeast3(argsList):
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_GREAT_BEAST_3_HELP", (gc.getDefineINT("TEMP_HAPPY"), 40, religion.getChar()))

	return szHelp

####### Controversial Philosopher ######

def canTriggerControversialPhilosopherCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]
	
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	
	if city.isNone():
		return False
	if (not city.isCapital()):
		return False
	if (city.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH) < 3500):
		return False

	return True


				# More Events Mod starts #
# Modified by lfgr

######## General Functions (lfgr)

# original: CanTriggerUnfortunateAssassinCity
def canTriggerCityCapital(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return True
	return False

######## Utility Functions (lfgr)

def semiRandomTurnTrigger( iTurns, fChance ) :
	game = CyGame()
	print "iTurns: %d" % iTurns
	iTurns *= gc.getGameSpeedInfo( game.getGameSpeedType() ).getGrowthPercent() / 100.0
	print "iTurns after gamespeed: %d" % iTurns
	iTurns = round( iTurns )
	print "iTurns after rounding: %d" % iTurns
	if( iTurns == 0 or game.getGameTurn() % iTurns == 0 ) :
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
	return pPlayer.hasTrait( gc.getInfoTypeForString( sTraitType ) )

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
				return True
	return False

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
						return True
					if iTerrain == iSnow:
						return True
	return False
	
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
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_INFERNAL")):
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
	
######## (lfgr: not reviewed)

def CanDoAshCough2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SHEAIM")):
		return True
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_KURIOTATES")):
		return True
	return False

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
	return True
	
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
	return True
	
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

# lfgr: tweaked 08/2014
def doOrphanedGoblin3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iBestValue = 0
	pBestPlot = -1
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	for pPlot in cf.getNearPlots( pUnit.plot(), 2 ) :
		iValue = 0
		if not pPlot.isWater():
			if not pPlot.isPeak():
				if pPlot.getNumUnits() == 0:
					iValue = CyGame().getSorenRandNum(1000, "Goblin1")
					if iValue > iBestValue:
						iBestValue = iValue
						pBestPlot = pPlot
	if (pBestPlot!=-1) :
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN'), pBestPlot.getX(),pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
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

# lfgr: added 08/2014
def canDoOrphanedGoblin4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	
	pCity = pPlayer.getCapitalCity()
	return pCity != None and not pCity.isNone()
	
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
										return True

	return False

	

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

# lfgr: removed CanDoPrincessRule4 (03/2015)

# lfgr: added 03/2015
def doPrincessRule4( argsList ) :
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_PRINCESS_RULE_4_MESSAGE",()),'',1,'Art/Interface/Buttons/General/unhealthy_person.dds',ColorTypes(7),kTriggeredData.iPlotX,kTriggeredData.iPlotY,True,True)

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
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL') :
			return True
	return False
	
def CanDoTraveller2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA') :
			return True
	return False
	
def CanDoTraveller3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS') :
			return True
	return False
	
def CanDoTraveller4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS') :
			return True
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER') :
			return True
	return False

######## UNFORTUNATE_ASSASSIN (lfgr: moved to general functions, changed, moved to XML)

######## (lfgr: not reviewed)

def CanDoOvercrowdedDungeon5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
		return False
	return True

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
		return True
	return False
	
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
	
######## POISONED_WATER (lfgr: moved to XML)

######## DEMONIC_TOWER (lfgr: moved to XML)

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

######## RALPH_AND_SAM (lfgr: moved to XML)

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
	
######## CENTAUR_TRIBE (lfgr: moved to XML)
	
def doCentaurTribe1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_CENTAUR_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
      	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)

######## SEASERPENT (lfgr: moved to XML)

def doSeaSerpent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_SEA_SERPENT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
      	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)

######## MONKEY_SEE (lfgr: moved to XML)

def doMonkeySee1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
######## MONKEY_SEE (lfgr: moved to XML)

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
			return False
	return True


#   At least one civ on the board must know Optics
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_OPTICS')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):			
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False


#	Find an eligible plot
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			return True

	return False

def applyLanunPirates1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	listPlots = []
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and plot.isWater() and not plot.isImpassable() and not plot.getNumUnits() > 0 and not plot.isLake() and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
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

	(loopUnit, iter) = barbPlayer.firstUnit(False)
	while (loopUnit):
		if loopUnit.getUnitType() == iUnitType1:
			loopUnit.setName("Lanun Raider")
		(loopUnit, iter) = barbPlayer.nextUnit(iter, False)
	
######## KURIOTATES_FISH/KURIOTATES_CLAM/KURIOTATES_CRAB

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
	
######## HAUNTED_CASTLE (lfgr: moved to XML)
	
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
	
######## MORE EVENTS MOD EXPANDED ENDS ########