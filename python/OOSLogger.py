import os
from CvPythonExtensions import *
import CvUtil
import BugPath

gc = CyGlobalContext()

szFilename = "OOSLog.txt"
iMaxFilenameTries = 100

bWroteLog = False

SEPERATOR = "-----------------------------------------------------------------\n"


# Simply checks every game turn for OOS. If it finds it, writes the
# info contained in the sync checksum to a log file, then sets the bWroteLog
# variable so that it only happens once.
def doGameUpdate():
	global bWroteLog
	bOOS = CyInterface().isOOSVisible()

	if (bOOS and not bWroteLog):
		writeLog()
		# Automatic OOS detection START
		gc.getGame().setOOSVisible()
		# Automatic OOS detection END
		bWroteLog = True
	# Make sure that OOS will be generated when the game is not restarted after an OOS.
	if (not bOOS):
		bWroteLog = False

def writeLog():
	playername = CvUtil.convertToStr(gc.getPlayer(gc.getGame().getActivePlayer()).getName())
	szNewFilename = BugPath.getRootDir() + "\\Logs\\" + "OOSLog - %s - " % (playername) + "Turn %s" % (gc.getGame().getGameTurn()) + ".txt"
	pFile = open(szNewFilename, "w")

	# Backup current language
	iLanguage = CyGame().getCurrentLanguage()
	# Force english language for logs
	CyGame().setCurrentLanguage(0)

	#
	# Global data
	#
	pFile.write(SEPERATOR)
	pFile.write(SEPERATOR)

	
	pFile.write(CvUtil.convertToStr(CyTranslator().getText("TXT_KEY_VERSION", ())))
	pFile.write("\n\n")

	pFile.write("  GLOBALS  \n")

	pFile.write(SEPERATOR)
	pFile.write(SEPERATOR)
	pFile.write("\n\n")

	pFile.write("Next Map Rand Value: %d\n" % CyGame().getMapRand().get(10000, "OOS Log"))
	pFile.write("Next Soren Rand Value: %d\n" % CyGame().getSorenRand().get(10000, "OOS Log"))

	pFile.write("Global counter: %d\n" % CyGame().getGlobalCounter() )
	pFile.write("Total cities: %d\n" % CyGame().getNumCities() )
	pFile.write("Total civilization cities: %d\n" % CyGame().getNumCivCities() )
	pFile.write("Total population: %d\n" % CyGame().getTotalPopulation() )
	pFile.write("Total deals: %d\n" % CyGame().getNumDeals() )

	pFile.write("Total owned plots: %d\n" % CyMap().getOwnedPlots() )
	pFile.write("Total number of areas: %d\n" % CyMap().getNumAreas() )

	pFile.write("\n\n")

	#
	# Player data
	#
	iPlayer = 0
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isEverAlive()):
			pFile.write(SEPERATOR)
			pFile.write(SEPERATOR)

			pFile.write("  PLAYER %d: %s  \n" % (iPlayer, CvUtil.convertToStr(pPlayer.getName())))
			pFile.write("  Civilizations: %s  \n" % (CvUtil.convertToStr(pPlayer.getCivilizationDescriptionKey())))

			pFile.write(SEPERATOR)
			pFile.write(SEPERATOR)
			pFile.write("\n\n")

			pFile.write("Basic data:\n")
			pFile.write("-----------\n")
			pFile.write("Player %d Score: %d\n" % (iPlayer, gc.getGame().getPlayerScore(iPlayer) ))

			pFile.write("Player %d Population: %d\n" % (iPlayer, pPlayer.getTotalPopulation() ) )
			pFile.write("Player %d Total Land: %d\n" % (iPlayer, pPlayer.getTotalLand() ) )
			pFile.write("Player %d Gold: %d\n" % (iPlayer, pPlayer.getGold() ) )
			pFile.write("Player %d Assets: %d\n" % (iPlayer, pPlayer.getAssets() ) )
			pFile.write("Player %d Power: %d\n" % (iPlayer, pPlayer.getPower() ) )
			pFile.write("Player %d Num Cities: %d\n" % (iPlayer, pPlayer.getNumCities() ) )
			pFile.write("Player %d Num Units: %d\n" % (iPlayer, pPlayer.getNumUnits() ) )
			pFile.write("Player %d Num Selection Groups: %d\n" % (iPlayer, pPlayer.getNumSelectionGroups() ) )
			pFile.write("Player %d Difficulty: %d\n" % (iPlayer, pPlayer.getHandicapType() ))
			pFile.write("Player %d Religion: %s\n" % (iPlayer, CvUtil.convertToStr(pPlayer.getStateReligionKey()) ))
			pFile.write("Player %d Total culture: %d\n" % (iPlayer, pPlayer.countTotalCulture() ))

			pFile.write("\n\n")

			pFile.write("Yields:\n")
			pFile.write("-------\n")
			for iYield in range( int(YieldTypes.NUM_YIELD_TYPES) ):
				pFile.write("Player %d %s Total Yield: %d\n" % (iPlayer, gc.getYieldInfo(iYield).getDescription(), pPlayer.calculateTotalYield(iYield) ))

			pFile.write("\n\n")

			pFile.write("Commerce:\n")
			pFile.write("---------\n")
			for iCommerce in range( int(CommerceTypes.NUM_COMMERCE_TYPES) ):
				pFile.write("Player %d %s Total Commerce: %d\n" % (iPlayer, gc.getCommerceInfo(iCommerce).getDescription(), pPlayer.getCommerceRate(CommerceTypes(iCommerce)) ))

			pFile.write("\n\n")

			pFile.write("Bonus Info:\n")
			pFile.write("-----------\n")
			for iBonus in range(gc.getNumBonusInfos()):
				pFile.write("Player %d, %s, Number Available: %d\n" % (iPlayer, gc.getBonusInfo(iBonus).getDescription(), pPlayer.getNumAvailableBonuses(iBonus) ))
				pFile.write("Player %d, %s, Import: %d\n" % (iPlayer, gc.getBonusInfo(iBonus).getDescription(), pPlayer.getBonusImport(iBonus) ))
				pFile.write("Player %d, %s, Export: %d\n" % (iPlayer, gc.getBonusInfo(iBonus).getDescription(), pPlayer.getBonusExport(iBonus) ))
				pFile.write("\n")

			pFile.write("\n\n")

			pFile.write("Improvement Info:\n")
			pFile.write("-----------------\n")
			for iImprovement in range(gc.getNumImprovementInfos()):
				pFile.write("Player %d, %s, Improvement count: %d\n" % (iPlayer, CvUtil.convertToStr(gc.getImprovementInfo(iImprovement).getDescription()), pPlayer.getImprovementCount(iImprovement) ))

			pFile.write("\n\n")

			pFile.write("Building Class Info:\n")
			pFile.write("--------------------\n")
			for iBuildingClass in range(gc.getNumBuildingClassInfos()):
				pFile.write("Player %d, %s, Building class count plus building: %d\n" % (iPlayer, CvUtil.convertToStr(gc.getBuildingClassInfo(iBuildingClass).getDescription()), pPlayer.getBuildingClassCountPlusMaking(iBuildingClass) ))

			pFile.write("\n\n")

			pFile.write("Unit Class Info:\n")
			pFile.write("--------------------\n")
			for iUnitClass in range(gc.getNumUnitClassInfos()):
				pFile.write("Player %d, %s, Unit class count plus training: %d\n" % (iPlayer, CvUtil.convertToStr(gc.getUnitClassInfo(iUnitClass).getDescription()), pPlayer.getUnitClassCountPlusMaking(iUnitClass) ))

			pFile.write("\n\n")

			pFile.write("UnitAI Types Info:\n")
			pFile.write("------------------\n")
			for iUnitAIType in range(int(UnitAITypes.NUM_UNITAI_TYPES)):
				pFile.write("Player %d, %s, Unit AI Type count: %d\n" % (iPlayer, gc.getUnitAIInfo(iUnitAIType).getDescription(), pPlayer.AI_totalUnitAIs(UnitAITypes(iUnitAIType)) ))
			

			pFile.write("\n\n")

			pFile.write("City Info:\n")
			pFile.write("----------\n")
			iNumCities = pPlayer.getNumCities()

			if (iNumCities == 0):
				pFile.write("No Cities")
			else:
				pLoopCityTuple = pPlayer.firstCity(False)
				while (pLoopCityTuple[0] != None):
					pCity = pLoopCityTuple[0]
					#pFile.write("Player %d, City ID: %d, %s, Plot Radius: %d\n" % (iPlayer, pCity.getID(), CvUtil.convertToStr(pCity.getName()), pCity.getPlotRadius() ))

					pFile.write("X: %d, Y: %d\n" % (pCity.getX(), pCity.getY()) )
					pFile.write("Founded: %d\n" % pCity.getGameTurnFounded() )
					pFile.write("Population: %d\n" % pCity.getPopulation() )
					pFile.write("Buildings: %d\n" % pCity.getNumBuildings() )
					pFile.write("Improved Plots: %d\n" % pCity.countNumImprovedPlots() )
					pFile.write("Producing: %s\n" % pCity.getProductionName() )
					pFile.write("Turns remaining for production: %d\n" % pCity.getProductionTurnsLeft() )
					pFile.write("%d happiness, %d unhappiness, %d health, %d unhealth\n" % (pCity.happyLevel(), pCity.unhappyLevel(0), pCity.goodHealth(), pCity.badHealth(False)) )
					pFile.write("%d Tiles Worked, %d Specialists, %d Great People\n" % (pCity.getWorkingPopulation(), pCity.getSpecialistPopulation(), pCity.getNumGreatPeople()) )
					pFile.write("City radius: %d\n" % pCity.getPlotRadius() )
					if (pCity.isSettlement()):
						pFile.write("City is a settlement")


					pLoopCityTuple = pPlayer.nextCity(pLoopCityTuple[1], False)
					pFile.write("\n")


			pFile.write("\n\n")

			pFile.write("Unit Info:\n")
			pFile.write("----------\n")
			iNumUnits = pPlayer.getNumUnits()

			if (iNumUnits == 0):
				pFile.write("No Units")
			else:
				pLoopUnitTuple = pPlayer.firstUnit(False)
				while (pLoopUnitTuple[0] != None):
					pUnit = pLoopUnitTuple[0]
					pFile.write("Player %d, Unit ID: %d, %s\n" % (iPlayer, pUnit.getID(), CvUtil.convertToStr(pUnit.getName()) ))
					pFile.write("X: %d, Y: %d\n" % (pUnit.getX(), pUnit.getY()) )
					pFile.write("Damage: %d\n" % pUnit.getDamage() )
					#pFile.write("Experience: %d\n" % pUnit.getExperienceTimes100() )
					pFile.write("Experience: %d\n" % pUnit.getExperience() )
					pFile.write("Level: %d\n" % pUnit.getLevel() )
					pFile.write("Promotions:\n")
					for j in range(gc.getNumPromotionInfos()):
						if (pUnit.isHasPromotion(j)):
							pFile.write("%s\n" % (CvUtil.convertToStr(gc.getPromotionInfo(j).getDescription()) ))

					pLoopUnitTuple = pPlayer.nextUnit(pLoopUnitTuple[1], False)
					pFile.write("\n")
				

			# Space at end of player's info
			pFile.write("\n\n")
		
	# Restore current language
	CyGame().setCurrentLanguage(iLanguage)

	# Close file

	pFile.close()
