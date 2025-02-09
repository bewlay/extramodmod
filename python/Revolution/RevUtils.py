# Utility functions for Revolution Mod
#
# by jdog5000
# Version 1.5

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import pickle
# --------- Revolution mod -------------
import RevDefs
import RevData
import SdToolKitCustom
import RevInstances
# Other Util files
from RevCivicsUtils import *
#phungus Rev Trait Effects
#from RevTraitsUtils import *
#Rev Trait End
import BugCore

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
game = CyGame()
localText = CyTranslator()
RevOpt = BugCore.game.Revolution


LOG_DEBUG = True
revCultureModifier = 1.0
endWarsOnDeath = True
gameSpeedMod = None
RevOpt = None # LFGR_TODO?

# Promotions used
iCommando = None
iGuerilla3 = None
iWoodsman3 = None
iSentry = None
iDrill2 = None

revReadyFrac = .6
revInstigatorThreshold = 1000
alwaysViolentThreshold = 1700
badLocalThreshold = 8
deniedTurns = 5

########################## Initialization ###############################

def init( ) :
		global revReadyFrac, revInstigatorThreshold, alwaysViolentThreshold, badLocalThreshold, deniedTurns

		revReadyFrac = RevOpt.getJoinRevolutionFrac()
		revInstigatorThreshold = RevOpt.getInstigateRevolutionThreshold()
		alwaysViolentThreshold = RevOpt.getAlwaysViolentThreshold()
		badLocalThreshold = RevOpt.getBadLocalThreshold()

		deniedTurns = RevOpt.getDeniedTurns()

########################## Generic helper functions ###############################

def getGameSpeedMod( ) : # LFGR_TODO: Could this lead to problems when playing multiple games in a single session?
	# LFGR_TODO: Make this a GameSpeed property.
		# Ratio of game turns to those of Epic, limited adjustment for extremely short/long differences
		global gameSpeedMod
		if( gameSpeedMod == None ) :
			gameSpeedMod = (751.0)/(game.getEstimateEndTurn() + 1.0)
			if( gameSpeedMod == 751.0 ) : gameSpeedMod = 1.0
			elif( gameSpeedMod > 2 ) : gameSpeedMod = 2.0
			elif( gameSpeedMod < 0.5 ) : gameSpeedMod = 0.5

		return gameSpeedMod


def doRefortify( iPlayer ) :
	#pyPlayer = PyPlayer( iPlayer )
	pPlayer = gc.getPlayer(iPlayer)

	CvUtil.pyPrint( "Refortifying units for player %d"%(iPlayer))

	for groupID in range(0,pPlayer.getNumSelectionGroups()) :
		pGroup = pPlayer.getSelectionGroup(groupID)
		if( pGroup.getNumUnits() > 0 ) :

			headUnit = pGroup.getHeadUnit()
			#CvUtil.pyPrint( "%s fortTurns %d"%(headUnit.getName(),headUnit.getFortifyTurns()) )
			if( headUnit.getFortifyTurns() > 0 ) :
				if( headUnit.isHurt() ) :
					#CvUtil.pyPrint( "%s is hurt"%(headUnit.getName()) )
					#pGroup.setActivityType(ActivityTypes.ACTIVITY_HEAL)
					pass
				else :
					#CvUtil.pyPrint( "Starting mission ..." )
					#pGroup.pushMission( MissionTypes.MISSION_FORTIFY, 0, 0, 0, False, True, MissionAITypes.MISSIONAI_GUARD_CITY, pGroup.plot(), pGroup.getHeadUnit() )
					pGroup.setActivityType(ActivityTypes.ACTIVITY_SLEEP)
					headUnit.NotifyEntity( MissionTypes.MISSION_FORTIFY )
					pass


def plotGenerator( startPlot, maxRadius ) :
	# To be used as: for [radius,plot] in RevUtils.plotGenerator(plot,5) :
	# Returns plots starting at radius 1 and up to max Radius

	# Start with center plot
	yield [0,startPlot]

	radius = 1
	gameMap = gc.getMap()
	# Expand radius slowly, searching concentric squares
	while( radius <= maxRadius ) :
		# Top and bottom rows
		for ix in range(startPlot.getX()-radius,startPlot.getX()+radius+1) :
			for iy in [startPlot.getY() - radius, startPlot.getY() + radius] :

				if( ix < 0 ) :
					if( gameMap.isWrapX() ) :
						ix = CyMap().getGridWidth() + ix
					else :
						continue
				elif( ix >= CyMap().getGridWidth() ) :
					if( gameMap.isWrapX() ) :
						ix = ix - CyMap().getGridWidth()
					else :
						continue

				if( iy < 0 ) :
					if( gameMap.isWrapY() ) :
						iy = CyMap().getGridHeight() + iy
					else :
						continue
				elif( iy >= CyMap().getGridHeight() ) :
					if( gameMap.isWrapY() ) :
						iy = iy - CyMap().getGridHeight()
					else :
						continue

				yield [radius,gameMap.plot(ix,iy)]

		# Left and right columns (leave out corners)
		for ix in [startPlot.getX()-radius,startPlot.getX()+radius] :
			for iy in range(startPlot.getY() - radius + 1, startPlot.getY() + radius) :

				if( ix < 0 ) :
					if( gameMap.isWrapX() ) :
						ix = CyMap().getGridWidth() + ix
					else :
						continue
				elif( ix >= CyMap().getGridWidth() ) :
					if( gameMap.isWrapX() ) :
						ix = ix - CyMap().getGridWidth()
					else :
						continue

				if( iy < 0 ) :
					if( gameMap.isWrapY() ) :
						iy = CyMap().getGridHeight() + iy
					else :
						continue
				elif( iy >= CyMap().getGridHeight() ) :
					if( gameMap.isWrapY() ) :
						iy = iy - CyMap().getGridHeight()
					else :
						continue

				yield [radius,gameMap.plot(ix,iy)]

		radius += 1

def getNumDefendersNearPlot( iPlotX, iPlotY, iPlayer, iRange = 2, bIncludePlot = True, bIncludeCities = False ) :
	# bIncludePlot takes precedence over bIncludeCities
	iNumUnits = 0

	gameMap = gc.getMap()
	basePlot = gameMap.plot(iPlotX,iPlotY)

	for [radius,pPlot] in plotGenerator( basePlot, iRange ) :

		if( pPlot.getX() == iPlotX and pPlot.getY() == iPlotY ) :
			if( not bIncludePlot ) :
				continue
		elif( pPlot.isCity() and not bIncludeCities ) :
			continue

		iNumUnits += pPlot.getNumDefenders( iPlayer )

	return iNumUnits


def getClosestCityXY( iPlotX, iPlotY, iPlayer, maxRange = 10, bIncludeBase = True ) :

	gameMap = gc.getMap()
	basePlot = gameMap.plot(iPlotX,iPlotY)

	for [radius,pPlot] in plotGenerator( basePlot, maxRange ) :
		if( radius == 0 and not bIncludeBase ) :
			continue
		if( pPlot.isCity() ) :
			if( pPlot.getOwner() == iPlayer ) :
				if( LOG_DEBUG ) : CvUtil.pyPrint("Revolt -  Found city %s (owner %d) at radius %d"%(pPlot.getPlotCity().getName(),pPlot.getPlotCity().getOwner(),radius))
				return [pPlot.getX(),pPlot.getY()]

	return None

def getSpawnablePlots( iPlotX, iPlotY, pSpawnPlayer, bLand = True, bIncludePlot = True, bIncludeCities = False, bIncludeForts = False, bSameArea = True, iRange = 2, iSpawnPlotOwner = -1, bCheckForEnemy = True, bAtWarPlots = True, bOpenBordersPlots = True ) :

		spawnablePlots = list()

		gameMap = gc.getMap()
		basePlot = gameMap.plot(iPlotX,iPlotY)

		iFort = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),RevDefs.sXMLFort)

		try :
			iBaseArea = basePlot.area().getID()
		except AttributeError :
			if( bSameArea ) : print "WARNING: Passed an arealess plot!"
			iBaseArea = -1
			bSameArea = False
		iBasePlotOwner = basePlot.getOwner()
		iNumPlotsChecked = 0

		for [radius,pPlot] in plotGenerator( basePlot, iRange ) :

				if( not bIncludePlot and pPlot.getX() == iPlotX and pPlot.getY() == iPlotY ) :
					continue

				if( pPlot.isImpassable() ):
					continue

				iNumPlotsChecked += 1

				if( bLand and pPlot.isWater() ) :
					continue

				if( not bLand and not pPlot.isWater() ) :
					continue

				if( not bIncludeCities and pPlot.isCity() ) :
					continue

				if( bSameArea and not iBaseArea == pPlot.area().getID() ) :
					continue

				if( bCheckForEnemy ) :
					if( len( getEnemyUnits(pPlot.getX(),pPlot.getY(),pSpawnPlayer.getID()) ) > 0 ) :
						continue

				if( not bIncludeForts and pPlot.getImprovementType() == iFort ) :
					continue

				# When iSpawnPlotOwner >= 0, plot owner must be either iSpawnPlotOwner, iBasePlotOwner, or no one
				if( iSpawnPlotOwner < 0 or pPlot.getOwner() == iSpawnPlotOwner or pPlot.getOwner() == iBasePlotOwner or pPlot.getOwner() == PlayerTypes.NO_PLAYER ) :
					spawnablePlots.append( [pPlot.getX(),pPlot.getY()] )
				elif( bAtWarPlots and gc.getTeam(pSpawnPlayer.getTeam()).isAtWar( gc.getPlayer(pPlot.getOwner()).getTeam() ) ) :
					spawnablePlots.append( [pPlot.getX(),pPlot.getY()] )
				elif( bOpenBordersPlots and gc.getTeam(pSpawnPlayer.getTeam()).isOpenBorders( gc.getPlayer(pPlot.getOwner()).getTeam() ) ) :
					spawnablePlots.append( [pPlot.getX(),pPlot.getY()] )

		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Found %d plots out of %d checked"%(len(spawnablePlots),iNumPlotsChecked))

#		for plot in spawnablePlots :
#			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - SP: %d, %d"%(plot[0],plot[1]))

		return spawnablePlots

def getEnemyUnits( iPlotX, iPlotY, iEnemyOfPlayer, domain = -1, bOnlyMilitary = False ) :

		pEnemyOfTeam = gc.getTeam( gc.getPlayer(iEnemyOfPlayer).getTeam() )
		gameMap = gc.getMap()
		pPlot = gameMap.plot(iPlotX,iPlotY)

		enemyUnits = list()

		for i in range(0,pPlot.getNumUnits()) :
			pUnit = pPlot.getUnit(i)
			pUnitTeam = gc.getTeam( pUnit.getTeam() )
			if( pEnemyOfTeam.isAtWar(pUnit.getTeam()) ) :
				if( domain < 0 or pUnit.getDomainType() == domain ) :
					if( not bOnlyMilitary or pUnit.canFight() ) :
						enemyUnits.append( pUnit )
						#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Unit %s, id %d, player %d, at %d,%d"%(pUnit.getName(),pUnit.getID(),pUnit.getOwner(),pUnit.plot().getX(),pUnit.plot().getY()))

		return enemyUnits

def getPlayerUnits( iPlotX, iPlotY, iPlayer, domain = -1 ) :

		gameMap = gc.getMap()
		pPlot = gameMap.plot(iPlotX,iPlotY)

		playerUnits = list()

		for i in range(0,pPlot.getNumUnits()) :
			pUnit = pPlot.getUnit(i)
			if( pUnit.getOwner() == iPlayer ) :
				if( domain < 0 or pUnit.getDomainType() == domain ) :
					playerUnits.append( pUnit )
					#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Unit %s, id %d, player %d, at %d,%d"%(pUnit.getName(),pUnit.getID(),pUnit.getOwner(),pUnit.plot().getX(),pUnit.plot().getY()))

		return playerUnits


def moveEnemyUnits( iPlotX, iPlotY, iEnemyOfPlayer, iMoveToX, iMoveToY, iInjureMax = 0, bDestroyNonLand = True, bLeaveSiege = False ) :

		unitList = getEnemyUnits( iPlotX, iPlotY, iEnemyOfPlayer )

##		for pUnit in unitList :
##				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Moving %s (id: %d, player: %d)"%(pUnit.getName(),pUnit.getID(),pUnit.getOwner()))
##				unitPlot = pUnit.plot()
##				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - from %d, %d"%(unitPlot.getX(),unitPlot.getY()))

		if( iInjureMax > 0 ) :
			for pUnit in unitList :
				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %d starts at %d"%(pUnit.getID(),pUnit.getDamage()))
				if( pUnit.canFight() ) :
					iPreDamage = pUnit.getDamage()
					iInjure = iPreDamage/3 + iInjureMax/2 + game.getSorenRandNum(iInjureMax/2,'Rev: Wound retreating units')
					iInjure = min([iInjure,90])
					iInjure = max([iInjure,iPreDamage])
					pUnit.setDamage( iInjure, iEnemyOfPlayer )
					#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %d injured to %d"%(pUnit.getID(),pUnit.getDamage()))

		pPlot = gc.getMap().plot(iMoveToX,iMoveToY)

		toKillList = list()
		for pUnit in unitList :
			if( not pUnit.getDomainType() == DomainTypes.DOMAIN_LAND or not pUnit.canMoveInto(pPlot,False,False,True) ) :
				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Pulling out %s for subsequent kill"%(pUnit.getName()))
				if( bDestroyNonLand ) :
					toKillList.append(pUnit)
				else :
					if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Leaving %s (%s)"%(pUnit.getName(),gc.getPlayer(pUnit.getOwner()).getCivilizationDescription(0)))
			elif( bLeaveSiege and pUnit.bombardRate() > 0 ) :
				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Leaving siege %s (%s)"%(pUnit.getName(),gc.getPlayer(pUnit.getOwner()).getCivilizationDescription(0)))
				pass
			else :
				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Moving %s (id: %d, player: %d)"%(pUnit.getName(),pUnit.getID(),pUnit.getOwner()))
				#unitPlot = pUnit.plot()
				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - from %d, %d"%(unitPlot.getX(),unitPlot.getY()))
				pUnit.setXY( iMoveToX, iMoveToY, False, False, False )
				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - to %d, %d"%(pUnit.plot().getX(),pUnit.plot().getY()))

		#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Units moved")

		for pUnit in toKillList :
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Killing %s at %d, %d"%(pUnit.getName(),pUnit.getX(),pUnit.getY()))
			if( not pUnit.isNone() and not pUnit.plot().isNone() ) :
				pUnit.kill(False,iEnemyOfPlayer)


def moveEnemyUnits2( iPlotX, iPlotY, iEnemyOfPlayer, iMoveToX, iMoveToY, iInjureMax = 0, bMoveAir = True, bLeaveSiege = False ) :

		unitList = getEnemyUnits( iPlotX, iPlotY, iEnemyOfPlayer )

##		for pUnit in unitList :
##				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Moving %s (id: %d, player: %d)"%(pUnit.getName(),pUnit.getID(),pUnit.getOwner()))
##				unitPlot = pUnit.plot()
##				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - from %d, %d"%(unitPlot.getX(),unitPlot.getY()))

		if( iInjureMax > 0 ) :
			for pUnit in unitList :
				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %d starts at %d"%(pUnit.getID(),pUnit.getDamage()))
				if( pUnit.canFight() ) :
					iPreDamage = pUnit.getDamage()
					iInjure = iPreDamage/3 + iInjureMax/2 + game.getSorenRandNum(iInjureMax/2,'Rev: Wound retreating units')
					iInjure = min([iInjure,90])
					iInjure = max([iInjure,iPreDamage])
					pUnit.setDamage( iInjure, iEnemyOfPlayer )
					#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %d injured to %d"%(pUnit.getID(),pUnit.getDamage()))

		pPlot = gc.getMap().plot(iMoveToX,iMoveToY)

		for pUnit in unitList :
			if( pUnit.getDomainType() == DomainTypes.DOMAIN_LAND or (bMoveAir and pUnit.getDomainType() == DomainTypes.DOMAIN_AIR) ) :
				if( bLeaveSiege and pUnit.getDomainType() == DomainTypes.DOMAIN_LAND and pUnit.bombardRate() > 0 ) :
					if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Leaving siege %s (%s)"%(pUnit.getName(),gc.getPlayer(pUnit.getOwner()).getCivilizationDescription(0)))
				else :
					if( pUnit.getDomainType() == DomainTypes.DOMAIN_AIR ) :
						if( pPlot.isCity() or pUnit.canMoveInto(pPlot,False,False,True) ) :
							if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Moving %s (id: %d, player: %d)"%(pUnit.getName(),pUnit.getID(),pUnit.getOwner()))
							pUnit.setXY( iMoveToX, iMoveToY, False, False, False )
						else :
							if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Can't move air unit %s (%s)"%(pUnit.getName(),gc.getPlayer(pUnit.getOwner()).getCivilizationDescription(0)))
					else :
						if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Moving %s (id: %d, player: %d)"%(pUnit.getName(),pUnit.getID(),pUnit.getOwner()))
						pUnit.setXY( iMoveToX, iMoveToY, False, False, False )
			else :
				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Leaving %s (%s)"%(pUnit.getName(),gc.getPlayer(pUnit.getOwner()).getCivilizationDescription(0)))


def clearOutCity( pCity, pPlayer, pEnemyPlayer ) :

	ix = pCity.getX()
	iy = pCity.getY()

	moveXY = getClosestCityXY( ix, iy, pPlayer.getID(), 25, bIncludeBase = False )
	if( moveXY == None ) :
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - No nearby cities, just placing not too far away")
		retreatPlots = getSpawnablePlots( ix, iy, pPlayer, bLand = True, bIncludePlot = False, bIncludeCities = True, bSameArea = True, iRange = 3, iSpawnPlotOwner = pPlayer.getID(), bCheckForEnemy = True )
		if( len(retreatPlots) == 0 ) :
			retreatPlots = getSpawnablePlots( ix, iy, pPlayer, bLand = True, bIncludePlot = False, bIncludeCities = True, bSameArea = False, iRange = 5, iSpawnPlotOwner = -1, bCheckForEnemy = True )

		if( len(retreatPlots) > 0 ) :
			moveXY = retreatPlots[game.getSorenRandNum(len(retreatPlots),'Rev')]

	if( not moveXY == None ) :
		moveEnemyUnits2( ix, iy, pEnemyPlayer.getID(), moveXY[0], moveXY[1], bMoveAir = True )

		# Handle water units
		waterUnits = getEnemyUnits( ix, iy, pEnemyPlayer.getID(), domain = DomainTypes.DOMAIN_SEA )

		if( len(waterUnits) > 0 ) :
			retreatPlots = getSpawnablePlots( ix, iy, pPlayer, bLand = False, bIncludePlot = False, bIncludeCities = False, bSameArea = False, iRange = 1, iSpawnPlotOwner = pPlayer.getID(), bCheckForEnemy = True )
			if( len(retreatPlots) == 0 ) :
				retreatPlots = getSpawnablePlots( ix, iy, pPlayer, bLand = False, bIncludePlot = False, bIncludeCities = False, bSameArea = False, iRange = 5, iSpawnPlotOwner = -1, bCheckForEnemy = True )
			if( len(retreatPlots) > 0 ) :
				moveXY = retreatPlots[game.getSorenRandNum(len(retreatPlots),'Rev')]
				for unit in waterUnits :
					if( unit.canMoveInto(gc.getMap().plot(moveXY[0],moveXY[1]),False,False,True) ) :
						if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Moving water unit %s (id: %d, player: %d)"%(unit.getName(),unit.getID(),unit.getOwner()))
						unit.setXY( moveXY[0], moveXY[1], False, False, False )


########################## Revolution helper functions ###############################


def getHandoverUnitTypes( city, pPlayer, compPlayer = None, bSilent = False ) :

		warriorClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo,gc.getNumUnitClassInfos(),RevDefs.sXMLWarrior)
		iWarrior = gc.getCivilizationInfo( pPlayer.getCivilizationType() ).getCivilizationUnits(warriorClass)
		workerClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo,gc.getNumUnitClassInfos(),RevDefs.sXMLWorker)
		iWorker = gc.getCivilizationInfo( pPlayer.getCivilizationType() ).getCivilizationUnits(workerClass)
		iBestDefender = UnitTypes.NO_UNIT
		iCounter = UnitTypes.NO_UNIT
		iAttack = UnitTypes.NO_UNIT
		if( not compPlayer == None ) :
			compPy = PyPlayer( compPlayer.getID() )

		for unitClass in range(0,gc.getNumUnitClassInfos()) :
			cityUnitType = gc.getCivilizationInfo( city.getCivilizationType() ).getCivilizationUnits(unitClass)

			if( gc.getUnitClassInfo(unitClass).getMaxGlobalInstances() > 0 or gc.getUnitClassInfo(unitClass).getMaxPlayerInstances() > 0 or gc.getUnitClassInfo(unitClass).getMaxTeamInstances() > 0 ) :
				continue
			
			if( pPlayer.isBarbarian() ) :
				playerUnitType = cityUnitType
			else :
				playerUnitType = gc.getCivilizationInfo( pPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)

			if( playerUnitType < 0 and cityUnitType < 0 ) :
##				print "WARNING: Civ types %d and %d have no unit of class type %d"%(city.getCivilizationType(),pPlayer.getCivilizationType(),unitClass)
				if city.getCivilizationType() == pPlayer.getCivilizationType():
					print "WARNING: Civ type %s has no unit of class type %s"%(gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDescription(), gc.getUnitClassInfo(unitClass).getDescription())
				else:
					print "WARNING: Neither Civ type %s nor %s has any unit of class type %s"%(gc.getCivilizationInfo(city.getCivilizationType()).getDescription(), gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDescription(), gc.getUnitClassInfo(unitClass).getDescription())
				continue

			if( playerUnitType < 0 ) :
				playerUnitType = cityUnitType
			elif( cityUnitType < 0 ) :
				cityUnitType = playerUnitType

			if( gc.getUnitInfo(cityUnitType).getDomainType() == DomainTypes.DOMAIN_LAND and city.canTrain(cityUnitType,False,False) ):

				unitInfo = gc.getUnitInfo(playerUnitType)
				if( not unitInfo.getPrereqAndTech() == TechTypes.NO_TECH ) :
					unitTechInfo = gc.getTechInfo( unitInfo.getPrereqAndTech() )

					# Defender (Archer,Longbow)
					if( unitInfo.getDefaultUnitAIType() == UnitAITypes.UNITAI_CITY_DEFENSE ):
						if( (iBestDefender == UnitTypes.NO_UNIT) or unitInfo.getCombat() >= gc.getUnitInfo(iBestDefender).getCombat() ) :
							if( compPlayer == None ) :
								iBestDefender = playerUnitType
							else :
								compUnitType = gc.getCivilizationInfo( compPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)
								if( len(compPy.getUnitsOfType(compUnitType)) > 0 ) :
									if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Revolt -  Comp has %d %s (def)"%(len(compPy.getUnitsOfType(compUnitType)),PyInfo.UnitInfo(compUnitType).getDescription()))
									iBestDefender = playerUnitType
								elif( unitTechInfo.getEra() < compPlayer.getCurrentEra() ) :
									if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Revolt -  Outdated unit %s (def)"%(PyInfo.UnitInfo(compUnitType).getDescription()))
									iBestDefender = playerUnitType
								else :
									pass

							#if( LOG_DEBUG ) : CvUtil.pyPrint("Revolt - Best defender set to %s"%(PyInfo.UnitInfo(iBestDefender).getDescription()))
					# Counter (Axemen,Phalanx)
					if( unitInfo.getUnitAIType(UnitAITypes.UNITAI_COUNTER) ):
						if( (iCounter == UnitTypes.NO_UNIT) or unitInfo.getCombat() >= gc.getUnitInfo(iCounter).getCombat() ) :
							if( compPlayer == None ) :
								iCounter = playerUnitType
							else :
								compUnitType = gc.getCivilizationInfo( compPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)
								if( len(compPy.getUnitsOfType(compUnitType)) > 1 ) :
									if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Revolt -  Comp has %d %s (count)"%(len(compPy.getUnitsOfType(compUnitType)),PyInfo.UnitInfo(compUnitType).getDescription()))
									iCounter = playerUnitType
								else :
									pass
							#if( LOG_DEBUG ) : CvUtil.pyPrint("Rev  - Best counter unit set to %s"%(PyInfo.UnitInfo(iCounter).getDescription()))
					# Assault units
					if( unitInfo.getUnitAIType( UnitAITypes.UNITAI_ATTACK ) ):
						if( (iAttack == UnitTypes.NO_UNIT) or unitInfo.getCombat() > gc.getUnitInfo(iAttack).getCombat() ) :
							if( compPlayer == None ) :
								iAttack = playerUnitType
							else :
								compUnitID = gc.getCivilizationInfo( compPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)
								if( len(compPy.getUnitsOfType(compUnitID)) > 1 ) :
									if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Revolt -  Comp has %d %s (att)"%(len(compPy.getUnitsOfType(compUnitID)),PyInfo.UnitInfo(compUnitID).getDescription()))
									iAttack = playerUnitType
								else :
									pass
							#if( LOG_DEBUG ) : CvUtil.pyPrint("Rev  - Best attack set to %s"%(PyInfo.UnitInfo(iAttack).getDescription()))

		if( iBestDefender == UnitTypes.NO_UNIT ) :
			if( not iCounter == UnitTypes.NO_UNIT ) :
				iBestDefender = iCounter
			else :
				iBestDefender = iWarrior
		if( iCounter == UnitTypes.NO_UNIT ) : iCounter = iBestDefender
		if( iAttack == UnitTypes.NO_UNIT ) : iAttack = iCounter

		if( LOG_DEBUG and not bSilent ) :
				if iBestDefender != UnitTypes.NO_UNIT:
					CvUtil.pyPrint("Revolt - Best defender set to %s"%(PyInfo.UnitInfo(iBestDefender).getDescription()))
				if iCounter != UnitTypes.NO_UNIT:
					CvUtil.pyPrint("Revolt - Best counter unit set to %s"%(PyInfo.UnitInfo(iCounter).getDescription()))
				if iAttack != UnitTypes.NO_UNIT:
					CvUtil.pyPrint("Revolt - Best attack set to %s"%(PyInfo.UnitInfo(iAttack).getDescription()))

		return [iWorker,iBestDefender,iCounter,iAttack]

def getUprisingUnitTypes( pCity, pRevPlayer, isCheckEnemy, bSilent = False ) :
		# Returns list of units that can be given to violent rebel uprisings, odds of giving are set by the relative number of times a unit type appears in list

		spawnableUnits = list()
		trainableUnits = list()

		owner = gc.getPlayer( pCity.getOwner() )
		ownerPy = PyPlayer( pCity.getOwner() )
		iOwnerEra = owner.getCurrentRealEra()

		bIsBarb = pRevPlayer.isBarbarian()
		enemyPy = None
		if( isCheckEnemy and not bIsBarb ) :
			enemyPy = PyPlayer( pRevPlayer.getID() )

		for unitClass in range(0,gc.getNumUnitClassInfos()) :
#			ownerUnitType = gc.getCivilizationInfo( owner.getCivilizationType() ).getCivilizationUnits(unitClass)
			ownerUnitType = gc.getCivilizationInfo( pRevPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)
			
			if ownerUnitType == -1:
#				ownerUnitType = gc.getCivilizationInfo( pRevPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)
				ownerUnitType = gc.getCivilizationInfo( owner.getCivilizationType() ).getCivilizationUnits(unitClass)
				
			ownerUnits = ownerPy.getUnitsOfType( ownerUnitType )
			unitInfo = gc.getUnitInfo(ownerUnitType)
			
			if( gc.getUnitClassInfo(unitClass).getMaxGlobalInstances() > 0 or gc.getUnitClassInfo(unitClass).getMaxPlayerInstances() > 0 or gc.getUnitClassInfo(unitClass).getMaxTeamInstances() > 0 ) :
				continue

			if( unitInfo == None ) :
				continue

			if (unitInfo.getPrereqReligion() != ReligionTypes.NO_RELIGION):
				continue
				
			if( not unitInfo.getDomainType() == DomainTypes.DOMAIN_LAND ) :
				continue
			
#			if( gc.getUnitClassInfo(unitClass).getMaxGlobalInstances() > 0 or gc.getUnitClassInfo(unitClass).getMaxPlayerInstances() > 0 or gc.getUnitClassInfo(unitClass).getMaxTeamInstances() > 0 ) :
#				continue

			# First check what units there are nearby
			if( not unitInfo.getPrereqAndTech() == TechTypes.NO_TECH ) :
				unitTechInfo = gc.getTechInfo( unitInfo.getPrereqAndTech() )

				if( unitTechInfo.getEra() > iOwnerEra - 3 ) :
					#if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Rebel: %s requires knowledge of %s"%(unitInfo.getDescription(),unitTechInfo.getDescription()))
					if( len(ownerUnits) > 0 ) :
						if( ownerUnits[0].canAttack() ) :
							if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Rebel:  Owner has %d %s"%(len(ownerUnits),PyInfo.UnitInfo(ownerUnitType).getDescription()))

							if( unitInfo.getUnitAIType(UnitAITypes.UNITAI_ATTACK) or unitInfo.getUnitAIType(UnitAITypes.UNITAI_COUNTER) ):

								# Probability of spawning units based on those nearby
								for unit in ownerUnits :
									if( plotDistance( unit.getX(), unit.getY(), pCity.getX(), pCity.getY() ) < 7 ) :
										if( bIsBarb ) :
											spawnUnitID = ownerUnitType
										else :
											spawnUnitID = gc.getCivilizationInfo( pRevPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)
										spawnableUnits.append( spawnUnitID )
										
										if spawnUnitID != -1:
											if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Rebel:  Can spawn from owner %s"%(PyInfo.UnitInfo(spawnUnitID).getDescription()))
											
										if( unitInfo.getDefaultUnitAIType() == UnitAITypes.UNITAI_CITY_DEFENSE ) :
											if( unitTechInfo.getEra() == iOwnerEra ) :
												if( spawnableUnits.count( spawnUnitID ) > 1 ) :
													break
											else :
												if( spawnableUnits.count( spawnUnitID ) > 3 ) :
													break
										else :
											if( unitTechInfo.getEra() == iOwnerEra ) :
												if( spawnableUnits.count( spawnUnitID ) > 3 ) :
													break
											else :
												if( spawnableUnits.count( spawnUnitID ) > 5 ) :
													break

								if( unitTechInfo.getEra() < iOwnerEra and unitTechInfo.getEra() >= iOwnerEra - 2) :
									# Can spawn old units from further away
									for unit in ownerUnits :
										if( unit.area().getID() == pCity.area().getID() ):
											if( bIsBarb ) :
												spawnUnitID = ownerUnitType
											else :
												spawnUnitID = gc.getCivilizationInfo( pRevPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)

											if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Rebel:  Outdated unit in Area %s"%(PyInfo.UnitInfo(ownerUnitType).getDescription()))
											if( pCity.canTrain(ownerUnitType,False,False) ) :
												spawnableUnits.append( spawnUnitID )
												if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Rebel:  Can spawn outdated unit from Area buildable %s"%(PyInfo.UnitInfo(ownerUnitType).getDescription()))

											break

					if( not enemyPy == None ) :
						enemyUnitType = gc.getCivilizationInfo( pRevPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)
						enemyUnits = enemyPy.getUnitsOfType( enemyUnitType )
						if( len( enemyUnits ) > 0 ) :
							if( enemyUnits[0].canAttack() ) :
								if( unitInfo.getUnitAIType( UnitAITypes.UNITAI_ATTACK )  ):
									iCount = 0
									for unit in enemyUnits :
										if( plotDistance( unit.getX(), unit.getY(), pCity.getX(), pCity.getY() ) < 7 ) :
											spawnableUnits.append( enemyUnitType )
											if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Rebel:  Can spawn from enemy %s"%(PyInfo.UnitInfo(enemyUnitType).getDescription()))

											iCount += 1
											if( unitInfo.getDefaultUnitAIType() == UnitAITypes.UNITAI_CITY_DEFENSE and iCount > 1 ) :
												break
											elif( iCount > 3 ) :
												break

			if( pCity.canTrain(ownerUnitType,False,False) ):
				if( unitInfo.getUnitAIType( UnitAITypes.UNITAI_ATTACK ) ):
					if( bIsBarb ) :
						spawnUnitID = ownerUnitType
					else :
						spawnUnitID = gc.getCivilizationInfo( pRevPlayer.getCivilizationType() ).getCivilizationUnits(unitClass)

					trainableUnits.append( spawnUnitID )
					if( unitInfo.getCombat() > 4 ) :
						trainableUnits.append( spawnUnitID )
						if( unitInfo.getCombat() > 15 ) :
							trainableUnits.append( spawnUnitID )
					if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("Rebel:  Can build %s"%(PyInfo.UnitInfo(ownerUnitType).getDescription()))

		if( len(spawnableUnits) < 1 ) :
			spawnableUnits = trainableUnits

		return spawnableUnits

def giveRebelUnitFreePromotion( pUnit ) :
	# TODO: Add provisions for hilly/forested cities giving special promotions
	global iCommando, iGuerilla3, iWoodsman3, iSentry, iDrill2

	if( iGuerilla3 == None ) :
		try :
			iGuerilla3 = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),RevDefs.sXMLGuerrilla3)
		except :
			pass

	if( iWoodsman3 == None ) :
		try :
			iWoodsman3 = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),RevDefs.sXMLWoodsman3)
		except :
			pass

	if( iSentry == None ) :
		try :
			iSentry = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),RevDefs.sXMLSentry)
		except :
			pass

	if( iDrill2 == None ) :
		try :
			iDrill2 = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),RevDefs.sXMLDrill2)
		except :
			pass

	if( iCommando == None ) :
		try :
			iCommando = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),RevDefs.sXMLCommando)
		except :
			pass

	if( not iGuerilla3 == None and pUnit.isPromotionValid(iGuerilla3) and  25 > game.getSorenRandNum(100,'Revolt - Promotion odds') ) :
		pUnit.setHasPromotion( iGuerilla3, True )
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %s starting with Guerilla3 promotion"%(pUnit.getName()))
		return

	if( not iWoodsman3 == None and pUnit.isPromotionValid(iWoodsman3) and  30 > game.getSorenRandNum(100,'Revolt - Promotion odds') ) :
		pUnit.setHasPromotion( iWoodsman3, True )
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %s starting with Woodsman3 promotion"%(pUnit.getName()))
		return

	if( not iSentry == None and pUnit.isPromotionValid(iSentry) and  40 > game.getSorenRandNum(100,'Revolt - Promotion odds') ) :
		pUnit.setHasPromotion( iSentry, True )
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %s starting with Sentry promotion"%(pUnit.getName()))
		return

	if( not iCommando == None and pUnit.isPromotionValid(iCommando) and  40 > game.getSorenRandNum(100,'Revolt - Promotion odds') ) :
		pUnit.setHasPromotion( iCommando, True )
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %s starting with Commando promotion"%(pUnit.getName()))
		return

	if( not iDrill2 == None and pUnit.isPromotionValid(iDrill2) ) :
		pUnit.setHasPromotion( iDrill2, True )
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %s starting with Drill2 promotion"%(pUnit.getName()))
		return
	else :
		if( not iSentry == None and pUnit.isPromotionValid(iSentry) ) :
			pUnit.setHasPromotion( iSentry, True )
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %s starting with Sentry promotion"%(pUnit.getName()))
			return
		elif( not iCommando == None and pUnit.isPromotionValid(iCommando) ) :
			pUnit.setHasPromotion( iCommando, True )
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - %s starting with Commando promotion"%(pUnit.getName()))
			return

	if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - No promotion possible for %s"%(pUnit.getName()))


def computeWarOdds( attacker, victim, area, allowAttackerVassal = True, allowVictimVassal = True, allowBreakVassal = True ) :

		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Calculating war odds")

		attackerTeam = gc.getTeam( attacker.getTeam() )
		victimTeam = gc.getTeam( victim.getTeam() )

		if( attackerTeam.getID() == victimTeam.getID() ) :
			return [-50,attackerTeam,victimTeam]

		if( attackerTeam.isAtWar(victimTeam.getID()) ) :
			return [100,attackerTeam,victimTeam]

		warOdds = 0

		if( attackerTeam.isAVassal() ) :
			if( not allowAttackerVassal ) :
				return [-50,attackerTeam,victimTeam]
			if( attackerTeam.isVassal(victimTeam.getID()) ) :
				if( not allowBreakVassal ) :
					return [-50,attackerTeam,victimTeam]
				else :
					# Allow vassal to rebel!!!
					warOdds -= 25

			else :
				warOdds -= 10
				for teamID in range(0,gc.getMAX_CIV_TEAMS()) :
					if( attackerTeam.isVassal(teamID) ) :
						attackerTeam = gc.getTeam( teamID )
						attacker = gc.getPlayer( attackerTeam.getLeaderID() )
						break

		if( victimTeam.isAVassal() ) :
			if( not allowVictimVassal ) :
				return [-50,attackerTeam,victimTeam]
			if( victimTeam.isVassal(attackerTeam.getID()) ) :
				if( not allowBreakVassal ) :
					return [-50,attackerTeam,victimTeam]
				else :
					# Allow master to attack
					warOdds -= 10
			else :
				for teamID in range(0,gc.getMAX_CIV_TEAMS()) :
					if( victimTeam.isVassal(teamID) ) :
						victimTeam = gc.getTeam( teamID )
						victim = gc.getPlayer( victimTeam.getLeaderID() )
						break

		if( attacker.AI_getAttitude(victim.getID()) == AttitudeTypes.ATTITUDE_FURIOUS ) :
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Attacker furious with potential victim")
			warOdds += 50
		elif( attacker.AI_getAttitude(victim.getID()) == AttitudeTypes.ATTITUDE_ANNOYED ) :
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Attacker annoyed with potential victim")
			warOdds += 25
		elif( attacker.AI_getAttitude(victim.getID()) == AttitudeTypes.ATTITUDE_PLEASED ) :
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Attacker pleased with potential victim")
			warOdds -= 25
		elif ( attacker.AI_getAttitude(victim.getID()) == AttitudeTypes.ATTITUDE_FRIENDLY ) :
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Attacker friendly with potential victim")
			warOdds -= 50
		else :
			if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Attacker cautious with potential victim")

		if( area.getPower(victim.getID()) == 0 ) :
			if( victim.getPower() == 0 ) :
				powerFrac = 2
				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Victim is powerless, %f for attacker"%(powerFrac))
			else :
				powerFrac = attacker.getPower()/(1.0*victim.getPower()) + .2
				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Victim has no power presence in area, %f for attacker"%(powerFrac))
		else :
			powerFrac = area.getPower(attacker.getID())/(1.0*area.getPower(victim.getID()))
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Power fraction is %f for attacker"%(powerFrac))
		if( area.getCitiesPerPlayer(attacker.getID()) > 1 and powerFrac > 1.5 ) :
			warOdds += 50
		elif( powerFrac > 1.2 ) :
			warOdds += 35
		elif( powerFrac > 1.0 ) :
			warOdds += 10
		elif( powerFrac < .9 ) :
			warOdds -= 25
		elif( area.getCitiesPerPlayer(attacker.getID()) < 1 or powerFrac < .7 ) :
			warOdds -= 40

		if( area.getCitiesPerPlayer(attacker.getID()) > area.getCitiesPerPlayer(victim.getID()) ) :
			warOdds += 10

		iAgg = CvUtil.findInfoTypeNum(gc.getTraitInfo,gc.getNumTraitInfos(),RevDefs.sXMLAggressive)
		if( attacker.hasTrait(iAgg) ) :
			warOdds += 10

		if( attacker.isRebel() ) :
			warOdds += 10

		warOdds = min([warOdds,100])

		return [warOdds,attackerTeam,victimTeam]


def giveTechs( toPlayer, fromPlayer, expensiveVars = [1,3], doTakeAway = True ) :

		# Give all techs known by fromPlayer, except a few of the most expensive
		knownTechs = list()
		mostExpensive = list()
		minMostExpensive = 0
		numMostExpensive = expensiveVars[0] + game.getSorenRandNum(expensiveVars[1],'Rev: Pick num techs')

		fromPlayerTeam = gc.getTeam( fromPlayer.getTeam() )
		toPlayerTeam = gc.getTeam( toPlayer.getTeam() )

		for techID in range(0,gc.getNumTechInfos()) :
			if gc.getCivilizationInfo(toPlayer.getCivilizationType()).isCivilizationFreeTechs(techID):
				knownTechs.append( techID )
			elif toPlayer.canEverResearch( techID):
				if( fromPlayerTeam.isHasTech( techID ) ) :
					knownTechs.append( techID )
					if( gc.getTechInfo( techID ).getResearchCost() > minMostExpensive ) :
						if( len(mostExpensive) < numMostExpensive ) :
							mostExpensive.append( techID )
						else :
							for j in range(0,len(mostExpensive)) :
								if( gc.getTechInfo( mostExpensive[j] ).getResearchCost() == minMostExpensive ) :
									mostExpensive.remove( mostExpensive[j] )
									break
							mostExpensive.append( techID )
							minMostExpensive = gc.getTechInfo( mostExpensive[0] ).getResearchCost()
							for j in range(0,len(mostExpensive)) :
								if( gc.getTechInfo( mostExpensive[j] ).getResearchCost() < minMostExpensive ) :
									minMostExpensive = gc.getTechInfo( mostExpensive[j] ).getResearchCost()

			if( doTakeAway and toPlayerTeam.isHasTech(techID) and toPlayerTeam.getNumMembers() == 1 ) :
				# take away all techs
				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Taking away %s"%(PyInfo.TechnologyInfo(techID).getDescription()))
				toPlayerTeam.setHasTech(techID,False,toPlayer.getID(),False,False)

		if( doTakeAway ) :
			if( not toPlayer.getTechScore() == 0 ) :
				# Shouldn't have to do this, but tech scores never came out to zero for reincarnated civs ...
				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Resetting tech score ...")
				toPlayer.changeTechScore( -toPlayer.getTechScore() )

		for techID in knownTechs :
			if( not techID in mostExpensive ) :
				#if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - Giving rev %s"%(PyInfo.TechnologyInfo(techID).getDescription()))
				toPlayerTeam.setHasTech(techID,True,toPlayer.getID(),False,False)
			else :
				if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - NOT giving rev all of %s"%(PyInfo.TechnologyInfo(techID).getDescription()))
				techCost = toPlayerTeam.getResearchCost( techID )
				maxFreeResearch = techCost*0.75
				toPlayerTeam.setResearchProgress( techID, game.getSorenRandNum(int(maxFreeResearch),'RevUtils: free research'), toPlayer.getID() )


########################## City helper functions ###############################

def isCityHilly( pCity ) :
	hillScore = 0

	for [iRadius, plot] in plotGenerator(pCity.plot(), 3) :
		# TODO: Make this functional
		if( plot.isHill() ) :
			hillScore += 3.5 - iRadius

	if( hillScore > 10 ) :
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - City %s is hilly with score %d"%(pCity.getName(),hillScore))
		return True
	else :
		return False

def isCityForested( pCity ) :
	forestScore = 0

	for [iRadius, plot] in plotGenerator(pCity.plot(), 3) :
		# TODO: Make this functional
		if( plot.isForested() ) :
			forestScore += 3.5 - iRadius

	if( forestScore > 8 ) :
		if( LOG_DEBUG ) : CvUtil.pyPrint("  Revolt - City %s is forested with score %d"%(pCity.getName(),forestScore))
		return True
	else :
		return False


def giveCityCulture( pCity, iPlayer, newCityVal, newPlotVal, overwriteHigher = False, bSilent = False, iPlotBase = 100 ) :
		# Places this culture value in city and city plot
		# Places half this value in neighboring plots

		if( iPlayer < 0 or iPlayer > gc.getBARBARIAN_PLAYER() ) :
			return

		if( overwriteHigher or newCityVal > pCity.getCulture(iPlayer) ) :
			pCity.setCulture( iPlayer, newCityVal, True )
			if( LOG_DEBUG and not bSilent) : CvUtil.pyPrint("  Revolt - Culture set to %d"%(pCity.getCulture(iPlayer)))

		if( overwriteHigher or newPlotVal > pCity.plot().getCulture(iPlayer) ) :
			pCity.plot().setCulture( iPlayer, newPlotVal, True )

		gameMap = gc.getMap()

		if( iPlotBase > 0 ) :
			culRadius = 2
			if( pCity.getCultureLevel() > 2 ) :
				culRadius = 3

			for [radius,pPlot] in plotGenerator( pCity.plot(), culRadius ) :
				iTotalCulture = pPlot.countTotalCulture()
				if( radius > 0 and iTotalCulture > 0 ) :

					# Cultural presence drops off with radius
					factor = (iPlotBase+game.getSorenRandNum(iPlotBase/8,'Rev: Culture'))/radius
					newPlotCul = min([newPlotVal, (factor*pPlot.countTotalCulture())/100])
					if( overwriteHigher or newPlotCul > pPlot.getCulture(iPlayer) ) :
						pPlot.setCulture( iPlayer, newPlotCul, True )

def isCanBribeCity( pCity ) :

	iRevIdx = pCity.getRevolutionIndex()
	localRevIdx = pCity.getLocalRevIndex()

	if( iRevIdx > 1700 ) :
		return [False, 'Violent']

	if( iRevIdx < .75*600 ) :
		if( localRevIdx < 8 ) :
			return [False, 'No Need']

	return [True, None]

def computeBribeCosts( pCity, bSilent = True ) :

	iSmall = -1
	iMed = -1
	iLarge = -1

	turnBribeData = RevData.getCityVal( pCity, 'TurnBribeCosts' )
	if( not turnBribeData == None ) :
		if( game.getGameTurn() == turnBribeData[0] ) :
			iSmall = turnBribeData[1][0]
			iMed = turnBribeData[1][1]
			iLarge = turnBribeData[1][2]

			return [iSmall, iMed, iLarge]

	# Compute costs to bribe rebels at three levels
	# Start by computing a base cost based on players economy strength
	iTurn = game.getGameTurn()
	pPlayer = gc.getPlayer( pCity.getOwner() )
	iGold = pPlayer.getGold()
	iEra = pPlayer.getCurrentEra()

	if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("  Revolt - Computing bribe city costs for %s, %s   pop %d"%(pCity.getName(),pPlayer.getCivilizationDescription(0),pCity.getPopulation()))

	iBaseCost = 0
	if( iTurn < 10 ) :
		iBaseCost = 0
	else :
		iAvgEcon = (pPlayer.getEconomyHistory(iTurn-4) + pPlayer.getEconomyHistory(iTurn-3) + pPlayer.getEconomyHistory(iTurn-2) + pPlayer.getEconomyHistory(iTurn-1))/4.0
		iAvgEcon = max([iAvgEcon,0])

		iBaseCost = pow(iAvgEcon,0.65) + iGold/20 + 10
		if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("  Revolt - Avg Econ : %d, cur gold : %d, iBaseCost : %d = %d + %d + 10"%(iAvgEcon, iGold, iBaseCost,pow(iAvgEcon,0.65),iGold/20))

	iRevIdx = pCity.getRevolutionIndex()
	localRevIdx = pCity.getLocalRevIndex()

	iRevCost = (iRevIdx + 20*min([localRevIdx,20]) - 0.35*600)/(9 + 2*gc.getNumEraInfos() - 2*iEra)

	if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("  Revolt - Rev Cost: %d from index %d, %d local"%(iRevCost,iRevIdx,localRevIdx))

	iModifier = 1.0
	lastBribeTurn = RevData.getCityVal( pCity, 'BribeTurn' )
	if( not lastBribeTurn == None ) :
		iModifier += 10/(iTurn - lastBribeTurn + 1.0)
	if( pCity.getPopulation() < 7 ) :
		iModifier -= 1/(2.0 + pCity.getPopulation())
	if( not pPlayer.isHuman() ) :
		iModifier = (2*iModifier)/3.0

	iExtra = 0
	if( pCity.getNumRevolts(pCity.getOwner()) > 1 ) :
		iExtra = 10 + iEra

	iRand = 7*game.getGameTurn() + pCity.getID()

	iMed = iModifier*(iBaseCost + iRevCost + iExtra)
	iSmall = (2*iMed)/3 + iRand%10
#	iLarge = (5*iMed)/3 + iRand%(1+int(iMed/14))
	iLarge = (5*iMed)/3 + iRand%15
	iMed += iRand%15

	iSmall = int(max([iSmall,21]))
	iMed   = int(max([iMed,  40]))
	iLarge = int(max([iLarge,78]))

	if( LOG_DEBUG and not bSilent ) : CvUtil.pyPrint("  Revolt - Bribe costs: small %d, med %d, large %d"%(iSmall,iMed,iLarge))

	RevData.setCityVal( pCity, 'TurnBribeCosts', [game.getGameTurn(), [iSmall,iMed,iLarge]] )

	return [iSmall, iMed, iLarge]

def bribeCity( pCity, bribeSize ) :

	iRevIdx = pCity.getRevolutionIndex()

	if( bribeSize == 'Small' ) :
		# Small reduction in rev index, mostly just for buyoffturns
		newRevIdx = int( 0.9*iRevIdx - 10 )
		newRevIdx = max([newRevIdx,0])
		pCity.setRevolutionIndex( newRevIdx )
		pCity.changeRevolutionCounter( 5 )
		RevData.setCityVal( pCity, 'BribeTurn', game.getGameTurn() )
		RevData.setCityVal( pCity, 'TurnBribeCosts', None )
	elif( bribeSize == 'Med' ) :
		# Med reduction in rev index
		newRevIdx = int( 0.8*iRevIdx - 25 )
		newRevIdx = max([newRevIdx,0])
		pCity.setRevolutionIndex( newRevIdx )
		pCity.changeRevolutionCounter( 7 )
		RevData.setCityVal( pCity, 'BribeTurn', game.getGameTurn() )
		RevData.setCityVal( pCity, 'TurnBribeCosts', None )
	elif( bribeSize == 'Large' ) :
		# Large reduction in rev index, longer time till next revolt too
		newRevIdx = int( 0.7*iRevIdx - 50 )
		newRevIdx = max([newRevIdx,0])
		pCity.setRevolutionIndex( newRevIdx )
		pCity.changeRevolutionCounter( 10 )
		RevData.setCityVal( pCity, 'BribeTurn', game.getGameTurn() )
		RevData.setCityVal( pCity, 'TurnBribeCosts', None )
	else :
		print 'Error!  Unrecognized bribeSize string %s'%(bribeSize)

########################## RevIndex helper functions #####################

# LFGR_TODO: Maybe use pCity.getUnhappyLevelForRevIdx() here?
def getModNumUnhappy( pCity, wwMod = 2.0, silent = False ) :

	modifier = int( wwMod*pCity.getPopulation()*pCity.getWarWearinessPercentAnger()/1000 )

	modNumUnhappy = pCity.angryPopulation(0) - modifier - 1

	if( not silent and LOG_DEBUG and pCity.angryPopulation(0) > 0 and game.getGameTurn()%25 == 0 ) :
		CvUtil.pyPrint("  Revolt - %s has numUnhappy %d, mod %d, modNumUn %d"%(pCity.getName(),pCity.angryPopulation(0),modifier,modNumUnhappy))

	if( modNumUnhappy <= 0 ) :
		numHappy = max( 0, pCity.happyLevel() - pCity.unhappyLevel(0) )
		numHappy = min( numHappy, pCity.getPopulation() )
		return -numHappy
	else :
		return modNumUnhappy

def doRevRequestDeniedPenalty( pCity, capitalArea, revIdxInc = 100, bExtraHomeland = False, bExtraColony = False ) :

	localRevIdx = pCity.getLocalRevIndex()

	if( bExtraColony and not pCity.area().getID() == capitalArea ) :
		pCity.changeRevolutionIndex( int(max([1.5*revIdxInc + 12*min([localRevIdx,20]), .75*revIdxInc])) )
	elif( bExtraHomeland and pCity.area().getID() == capitalArea ) :
		pCity.changeRevolutionIndex( int(max([1.5*revIdxInc + 12*min([localRevIdx,20]), .75*revIdxInc])) )
	else :
		pCity.changeRevolutionIndex( int(max([revIdxInc + 12*min([localRevIdx,20]), .5*revIdxInc])) )

	if( pCity.getRevRequestAngerTimer() < 3*deniedTurns ) :
		pCity.changeRevRequestAngerTimer( min([2*deniedTurns, 3*deniedTurns - pCity.getRevRequestAngerTimer()]) )
	pCity.changeRevolutionCounter( deniedTurns )

def computeCivSizeRaw( iPlayer ) :
	# Ratio of amount of land player owns to what would be equal for this map for national effects, effective radius of civ's empire for comparing with city distance
	expCivPlots = CyMap().getLandPlots() / ( gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() * 1.0)

	civSizeValRaw = gc.getPlayer(iPlayer).getTotalLand() / (1.0*expCivPlots)
	iCivEffRadRaw = pow((.5*gc.getPlayer(iPlayer).getTotalLand() + .5*expCivPlots)/3.4, .5)

	return [civSizeValRaw,iCivEffRadRaw]

def computeCivSize( iPlayer ) :
	# Ratio of amount of land player owns to what would be equal for this map for national effects, effective radius of civ's empire for comparing with city distance
	expCivPlots = CyMap().getLandPlots() / ( gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() * 1.0)

	# TODO:  use CyGame::getCurrentEra to get average era instead of per player?  Would hurt most players
#	civSizeEraMod = max( [0, 0.85-0.20*gc.getPlayer(iPlayer).getCurrentEra()] )
#	civSizeEraMod = max( [0, 0.85-0.20*gc.getGame().getCurrentPeriod()] )
#	civSizeValue  = ( gc.getPlayer(iPlayer).getTotalLand() / (1.0*expCivPlots) ) + civSizeEraMod

	map = gc.getMap()
	civSizeValue = gc.getPlayer(iPlayer).getNumCities() / gc.getWorldInfo(map.getWorldSize()).getTargetNumCities()
	
	iCivEffRadius = pow((.5*gc.getPlayer(iPlayer).getTotalLand() + .5*expCivPlots)/3.4, .5)

	return [civSizeValue,iCivEffRadius]


########################## Player modification functions ###########################################

def changeCiv( playerIdx, newCivType = -1, newLeaderType = -1, teamIdx = -1 ) :
	# Changes specified players civ, leader
	# Does not change isHuman setting

	player = gc.getPlayer(playerIdx)
	oldCivType = player.getCivilizationType()
	oldLeaderType = player.getLeaderType()
	if( newCivType >= 0 and not newCivType == oldCivType ) :
		player.changeCiv( newCivType )
		if( not RevInstances.DynamicCivNamesInst == None ) :
			RevInstances.DynamicCivNamesInst.resetName( playerIdx )
			RevInstances.DynamicCivNamesInst.recalcNameWithMessage( playerIdx )
	if( newLeaderType >= 0 and not newLeaderType == oldLeaderType ) :
		player.setName("")
		player.changeLeader( newLeaderType )
		if( not RevInstances.DynamicCivNamesInst == None ) :
			RevInstances.DynamicCivNamesInst.resetName( playerIdx )
			RevInstances.DynamicCivNamesInst.onSetPlayerAlive( [playerIdx, True] )

	return True

def changePersonality( playerIdx, newPersonality = -1 ) :
	# Changes leader personality of this civ

	player = gc.getPlayer(playerIdx)

	if( newPersonality < 0 ) :
		iBestValue = 0
		newPersonality = -1

		for iI in range(0,gc.getNumLeaderHeadInfos()) :
			if (not iI == gc.getDefineINT("BARBARIAN_LEADER")) :
				iValue = (1 + game.getSorenRandNum(10000, "Choosing Personality"))

				for iJ in range(0,gc.getMAX_CIV_PLAYERS()) :
					if (gc.getPlayer(iJ).isEverAlive()) :
						if (gc.getPlayer(iJ).getPersonalityType() == iI) :
							iValue /= 2

				if (iValue > iBestValue) :
					iBestValue = iValue
					newPersonality = iI

	if (newPersonality >= 0 and newPersonality < gc.getNumLeaderHeadInfos()) :
		player.setPersonalityType(newPersonality)

def changeHuman( newHumanIdx, oldHumanIdx ) :
##********************************
##   LEMMY 101 FIX
##********************************
	game.changeHumanPlayer( oldHumanIdx, newHumanIdx )
##********************************
##   LEMMY 101 FIX
##********************************

	# try :
		# CyCamera().JustLookAt( gc.getPlayer(newHumanIdx).getCapitalCity().plot().getPoint() )
	# except :
		# try :
			# CyCamera().JustLookAt( gc.getPlayer(newHumanIdx).firstCity()[0].plot().getPoint() )
		# except :
			# try :
				# CyCamera().JustLookAt( gc.getPlayer(newHumanIdx).firstUnit()[0].plot().getPoint() )
			# except :
				# pass
	doRefortify( newHumanIdx )
	#CyMessageControl().sendPlayerOption(PlayerOptionTypes.PLAYEROPTION_WAIT_END_TURN, True )
	return True


########################## Debug functions ###########################################

def debugHandoverUnitTypes( cityStr, iTakeoverPlayer, bDoOwnerAsComp ) :

	takeoverPlayer = gc.getPlayer(iTakeoverPlayer)

	for idx in range(0,gc.getMAX_PLAYERS()) :

		pyOwner = PyPlayer( idx )
		cityList = pyOwner.getCityList()

		for city in cityList :
			pCity = city.GetCy()
			if( cityStr in pCity.getName() ) :
				CvUtil.pyPrint( "Found city %s owned by %s"%(cityStr,gc.getPlayer(idx).getCivilizationDescription(0)) )
				CvUtil.pyPrint( "Initiating mock takeover by %s"%(takeoverPlayer.getCivilizationDescription(0)) )

				compPlayer = takeoverPlayer
				if( bDoOwnerAsComp ) :
					compPlayer = gc.getPlayer(idx)

				unitList = getHandoverUnitTypes( pCity, takeoverPlayer, compPlayer, False )

				unitStr = "["
				for unitType in unitList :
					unitStr += "%s, "%(PyInfo.UnitInfo(unitType).getDescription())
				unitStr += "]"

				CvUtil.pyPrint( unitStr )

				return

	print "Did not find city %s"%(cityStr)

def debugUprisingUnitTypes( cityStr, iRevPlayer, bCheckEnemy ) :

	pRevPlayer = gc.getPlayer(iRevPlayer)

	for idx in range(0,gc.getMAX_PLAYERS()) :

		pyOwner = PyPlayer( idx )
		cityList = pyOwner.getCityList()

		for city in cityList :
			pCity = city.GetCy()
			if( cityStr in pCity.getName() ) :
				CvUtil.pyPrint( "Found city %s owned by %s"%(cityStr,gc.getPlayer(idx).getCivilizationDescription(0)) )
				CvUtil.pyPrint( "Initiating mock revolt by %s"%(pRevPlayer.getCivilizationDescription(0)) )


				unitList = getUprisingUnitTypes( pCity, pRevPlayer, bCheckEnemy, False )

				unitStr = "["
				for unitType in unitList :
					unitStr += "%s, "%(PyInfo.UnitInfo(unitType).getDescription())
				unitStr += "]"

				CvUtil.pyPrint( unitStr )

				return

	print "Did not find city %s"%(cityStr)
