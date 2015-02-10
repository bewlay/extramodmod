## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

#AdventurerCounter Start (Imported from Rise from Erebus, modified by Terkhen)
lAdventurerBuildings = []
lAdventurerBuildingsPoints = []
#AdventurerCounter End

class CustomFunctions:

	def addBonus( self, iBonus, iNum, sIcon ):
		listPlots = []
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			if ( pPlot.canHaveBonus( gc.getInfoTypeForString( iBonus ), True ) and pPlot.getBonusType( -1 ) == -1 and pPlot.isCity() == False ):
				listPlots.append( i )
		if len( listPlots ) > 0:
			for i in range ( iNum ):
				iRnd = CyGame().getSorenRandNum( len( listPlots ), "Add Bonus" )
				pPlot = CyMap().plotByIndex( listPlots[iRnd] )
				pPlot.setBonusType( gc.getInfoTypeForString( iBonus ) )
				if sIcon != -1:
					iActivePlayer = CyGame().getActivePlayer()
					CyInterface().addMessage( iActivePlayer, True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_RESOURCE_DISCOVERED", () ), 'AS2D_DISCOVERBONUS', 1, sIcon, ColorTypes( 8 ), pPlot.getX(), pPlot.getY(), True, True )

	def addPopup( self, szText, sDDS ):
		szTitle = CyGameTextMgr().getTimeStr( CyGame().getGameTurn(), False )
		popup = PyPopup.PyPopup( -1 )
		popup.addDDS( sDDS, 0, 0, 128, 384 )
		popup.addSeparator()
		popup.setHeaderString( szTitle )
		popup.setBodyString( szText )
		popup.launch( True, PopupStates.POPUPSTATE_IMMEDIATE )

	def addPlayerPopup( self, szText, iPlayer ):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType( ButtonPopupTypes.BUTTONPOPUP_PYTHON )
		popupInfo.setText( szText )
		popupInfo.addPythonButton( CyTranslator().getText( "TXT_KEY_POPUP_CLOSE", () ), "" )
		popupInfo.addPopup( iPlayer )

	def addUnit( self, iUnit ):
		pBestPlot = -1
		iBestPlot = -1
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			iPlot = -1
			if pPlot.isWater() == False:
				if pPlot.getNumUnits() == 0:
					if pPlot.isCity() == False:
						if pPlot.isImpassable() == False:
							iPlot = CyGame().getSorenRandNum( 500, "Add Unit" )
							iPlot = iPlot + ( pPlot.area().getNumTiles() * 10 )
							if pPlot.isBarbarian():
								iPlot = iPlot + 200
							if pPlot.isOwned():
								iPlot = iPlot / 2
							if iPlot > iBestPlot:
								iBestPlot = iPlot
								pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer( gc.getBARBARIAN_PLAYER() )
			newUnit = bPlayer.initUnit( iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH )

	def addUnitFixed( self, caster, iUnit ):
		pPlot = caster.plot()
		pNewPlot = self.findClearPlot( -1, pPlot )
		if pNewPlot != -1:
			pPlayer = gc.getPlayer( gc.getBARBARIAN_PLAYER() )
			newUnit = pPlayer.initUnit( iUnit, pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH )
			return newUnit
		return -1

	def doCrusade( self, iPlayer ):
		iCrusadeChance = gc.getDefineINT( 'CRUSADE_SPAWN_CHANCE' )
		iDemagog = gc.getInfoTypeForString( 'UNIT_DEMAGOG' )
		iTown = gc.getInfoTypeForString( 'IMPROVEMENT_TOWN' )
		iVillage = gc.getInfoTypeForString( 'IMPROVEMENT_VILLAGE' )
		pPlayer = gc.getPlayer( iPlayer )
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			if pPlot.getImprovementType() == iTown:
				if pPlot.getOwner() == iPlayer :
##--------		Unofficial Bug Fix: Added by Denev		--------##
# To prevent spawning demagog in the same tile with his enemy unit.
					if not pPlot.isVisibleEnemyUnit( iPlayer ):
##--------		Unofficial Bug Fix: End Add				--------##
						if CyGame().getSorenRandNum( 100, "Crusade" ) < iCrusadeChance:
							newUnit = pPlayer.initUnit( iDemagog, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH )
							pPlot.setImprovementType( iVillage )

	def doFear( self, pVictim, pPlot, pCaster, bResistable ):
		if pVictim.isImmuneToFear():
			return False
		if bResistable:
			if CyGame().getSorenRandNum( 100, "Crusade" ) < pVictim.getResistChance( pCaster, gc.getInfoTypeForString( 'SPELL_ROAR' ) ):
				return False
		iX = pVictim.getX()
		iY = pVictim.getY()
		pBestPlot = -1
		iBestPlot = 0
		for iiX in range( iX - 1, iX + 2, 1 ):
			for iiY in range( iY - 1, iY + 2, 1 ):
				pLoopPlot = CyMap().plot( iiX, iiY )
				if not pLoopPlot.isNone():
					if not pLoopPlot.isVisibleEnemyUnit( pVictim.getOwner() ):
						if pVictim.canMoveOrAttackInto( pLoopPlot, False ):
							if ( abs( pLoopPlot.getX() - pPlot.getX() ) > 1 ) or ( abs( pLoopPlot.getY() - pPlot.getY() ) > 1 ):
								iRnd = CyGame().getSorenRandNum( 500, "Fear" )
								if iRnd > iBestPlot:
									iBestPlot = iRnd
									pBestPlot = pLoopPlot
		if pBestPlot != -1:
			pVictim.setXY( pBestPlot.getX(), pBestPlot.getY(), False, True, True )
			return True
		return False

# WILDERNESS 08/2013 lfgr / WildernessExploration, PromotionExplResultBonus
	def exploreLair( self, pUnit, bEpic ) :
		pPlot = pUnit.plot()
		
		iDestroyLair = 0
		
		ePillageImprovement = gc.getImprovementInfo( pPlot.getImprovementType() ).getImprovementPillage()
		bNoDestroy = ( ePillageImprovement != -1 )
		
		eSpawn = self.pickSpawn( pUnit )
		tOutcome = self.pickNonSpawnOutcome( pUnit, bEpic, bNoDestroy )
		
		if( eSpawn == None and tOutcome == None ) :
			CvUtil.pyPrint( "ERROR: Neither spawn nor non-spawn outcome available, adding 'NOTHING'" )
			iDestroyLair = self.doNonSpawnOutcome( pUnit, ( 'Special', 100, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_NOTHING', 'NOTHING' ) )
		elif( eSpawn == None ) :
			CvUtil.pyPrint( "WARNING: No spawn outcome available" )
			iDestroyLair = self.doNonSpawnOutcome( pUnit, tOutcome )
		elif( tOutcome == None ) :
			CvUtil.pyPrint( "WARNING: No non-spawn outcome available" )
			iDestroyLair = self.doSpawn( pUnit, eSpawn )
		else :
			if( CyGame().getSorenRandNum( 100, "Explore Lair" ) < 50 ) :
				iDestroyLair = self.doSpawn( pUnit, eSpawn )
			else :
				iDestroyLair = self.doNonSpawnOutcome( pUnit, tOutcome )
		
		if iDestroyLair > CyGame().getSorenRandNum( 100, "Explore Lair" ):
			if( bNoDestroy ) :
				CyInterface().addMessage( pUnit.getOwner(), True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_LAIR_EXPLORED", () ), 'AS2D_POSITIVE_DINK', 1, 'Art/Interface/Buttons/Spells/Explore Lair.dds', ColorTypes( 8 ), pPlot.getX(), pPlot.getY(), True, True )
				pPlot.setImprovementType( -1 ) # to remove landmark
				pPlot.setImprovementType( ePillageImprovement )
			else :
				CyInterface().addMessage( pUnit.getOwner(), True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_LAIR_DESTROYED", () ), 'AS2D_POSITIVE_DINK', 1, 'Art/Interface/Buttons/Spells/Explore Lair.dds', ColorTypes( 8 ), pPlot.getX(), pPlot.getY(), True, True )
				pPlot.setImprovementType( -1 )
		pUnit.finishMoves()
		pUnit.changeExperience( 1, -1, False, False, False )
	
	def doSpawn( self, pUnit, eSpawn ) :
		pPlot = pUnit.plot()
		
		# Push units out or set spawn plot
		pSpawnPlot = pPlot
		
		# LFGR_TODO: try to push other units out of way to ensure abusing by surrounding the lair with units is not possible
		pPlot2 = self.findClearPlot( -1, pPlot )
		if pPlot2 != -1:
			if( gc.getSpawnInfo( eSpawn ).isExplorationNoPush() ) :
				pSpawnPlot = pPlot2
			else :
				for i in range( pPlot.getNumUnits(), -1, -1 ):
					pUnit = pPlot.getUnit( i )
					pUnit.setXY( pPlot2.getX(), pPlot2.getY(), True, True, True )
		else:
			raise Exception( "Couldn't find clear plot to move unit (we shouldn't have reached this point then)" )
		
		# Spawn
		pSpawnPlot.createSpawn( eSpawn, UnitAITypes.NO_UNITAI )
		
		sMessage = gc.getSpawnInfo( eSpawn ).getDescription()
		if( sMessage == "" ) :
			sMessage = CyTranslator().getText( "TXT_KEY_MESSAGE_EXPLORE_LAIR_BIGBAD", () )
		CyInterface().addMessage( pUnit.getOwner(), True, 25, sMessage, '', 1, 'Art/Interface/Buttons/Spells/Explore Lair.dds', ColorTypes( 7 ), pPlot.getX(), pPlot.getY(), True, True )
		
		return 0
	
	def doNonSpawnOutcome( self, pUnit, tOutcome ) :
		pPlot = pUnit.plot()
		iPlayer = pUnit.getOwner()
		pPlayer = gc.getPlayer( iPlayer )
		
		iDestroyLair = 0
		sMessage = None
		
		if( tOutcome[0] == 'Special' ) :
			iDestroyLair = tOutcome[1]
			bGood = tOutcome[2]
			sMessage = tOutcome[3]
			sType = tOutcome[4]
			
			if( sType == 'DEATH' ) :
				pUnit.kill( True, 0 )
			elif( sType == 'POISONED' ) :
				pUnit.setHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_POISONED' ), True )
				pUnit.doDamageNoCaster( 25, 90, gc.getInfoTypeForString( 'DAMAGE_POISON' ), False )
			elif( sType == 'NOTHING' ) :
				pass
			elif( sType == 'CAGE' ) :
				CyInterface().addMessage( pUnit.getOwner(), True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_LAIR_DESTROYED", () ), 'AS2D_POSITIVE_DINK', 1, 'Art/Interface/Buttons/Spells/Explore Lair.dds', ColorTypes( 8 ), pPlot.getX(), pPlot.getY(), True, True )
				pPlot.setImprovementType( gc.getInfoTypeForString( 'IMPROVEMENT_CAGE' ) )
				for i in range( pPlot.getNumUnits() ) :
					pUnit2 = pPlot.getUnit( i )
					if( pUnit2.getOwner() == pUnit.getOwner() ) :
						pUnit2.setHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_HELD' ), True )
			elif( sType == 'TREASURE' ) :
				self.placeTreasure( iPlayer, self.saveGetInfoType( gc.getNumUnitInfos(), 'EQUIPMENT_TREASURE' ) )
			elif( sType == 'IRON_WEAPONS' ) :
				pUnit.setHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_IRON_WEAPONS' ), True )
				pUnit.setHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_BRONZE_WEAPONS' ), False )
			elif( sType == 'MITHRIL_WEAPONS' ) :
				pUnit.setHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_MITHRIL_WEAPONS' ), True )
				pUnit.setHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_IRON_WEAPONS' ), False )
				pUnit.setHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_BRONZE_WEAPONS' ), False )
			elif( sType == 'GOLDEN_AGE' ) :
				pPlayer.changeGoldenAgeTurns( CyGame().goldenAgeLength() )
			else :
				raise Exception( "Unknown special outcome type: %s" % ( tOutcome[0] ) )
		
		elif( tOutcome[0] == 'Promotions' ) :
			iDestroyLair = tOutcome[1]
			bGood = tOutcome[2]
			sMessage = tOutcome[3]
			lsPromotions = tOutcome[4]
			
			for sPromotion in lsPromotions :
				ePromotion = self.saveGetInfoType( gc.getNumPromotionInfos(), sPromotion )
				pUnit.setHasPromotion( ePromotion, True )
		
		elif( tOutcome[0] == 'RemovePromotions' ) :
			iDestroyLair = tOutcome[1]
			bGood = tOutcome[2]
			sMessage = tOutcome[3]
			lsPromotions = tOutcome[4]
			
			for sPromotion in lsPromotions :
				ePromotion = self.saveGetInfoType( gc.getNumPromotionInfos(), sPromotion )
				pUnit.setHasPromotion( ePromotion, False )
		
		elif( tOutcome[0] == 'Event' ) :
			iDestroyLair = tOutcome[1]
			sEvent = tOutcome[2]
			
			iUnitID = self.getUnitPlayerID( pUnit )
			eEvent = self.saveGetInfoType( gc.getNumEventTriggerInfos(), sEvent )
			pPlayer.initTriggeredData( eEvent, True, -1, pUnit.getX(), pUnit.getY(), pUnit.getOwner(), -1, -1, -1, iUnitID, -1 )
		
		elif( tOutcome[0] == 'Goody' ) :
			iDestroyLair = tOutcome[1]
			sGoody = tOutcome[2]
			
			eGoody = self.saveGetInfoType( gc.getNumGoodyInfos(), sGoody )
			pPlayer.receiveGoody( pPlot, eGoody, pUnit )
		
		elif( tOutcome[0] == 'Bonus' ) :
			iDestroyLair = tOutcome[1]
			bGood = True
			sMessage = tOutcome[2]
			sBonus = tOutcome[3]
			
			eBonus = self.saveGetInfoType( gc.getNumBonusInfos(), sBonus )
			pPlot.setBonusType( eBonus )
		
		elif( tOutcome[0] == 'Damage' ) :
			iDestroyLair = tOutcome[1]
			bGood = False
			sMessage = tOutcome[2]
			iDamage = tOutcome[3]
			iDamageLimit = tOutcome[4]
			sDamageType = tOutcome[5]
			
			pUnit.doDamageNoCaster( iDamage, iDamageLimit, gc.getInfoTypeForString( sDamageType ), False )
		
		else :
			raise Exception( "Unknown outcome type: %s" % ( str( tOutcome[0] ) ) )
		
		if( sMessage != None ) :
			eColor = -1
			if( bGood ) :
				eColor = ColorTypes( 8 )
			else :
				eColor = ColorTypes( 7 )
			CyInterface().addMessage( pUnit.getOwner(), True, 25, CyTranslator().getText( sMessage, () ), '', 1, 'Art/Interface/Buttons/Spells/Explore Lair.dds', eColor, pPlot.getX(), pPlot.getY(), True, True )
		
		return iDestroyLair
	
	def pickSpawn( self, pUnit ) :
		pPlot = pUnit.plot()
		
		# LFGR_TODO: try to push other units out of way to ensure abusing by surrounding the lair with units is not possible
		if( self.findClearPlot( -1, pPlot ) == -1 ) :
			CvUtil.pyPrint( "pickSpawn: No clear plot around, returning None" )
			return None
		
		eBestSpawn = None
		iBestValue = 0
		for eSpawn in range( gc.getNumSpawnInfos() ) :
			pSpawn = gc.getSpawnInfo( eSpawn )
			if( pSpawn.isExplorationResult() ) :
				iValue = pPlot.getSpawnValue( eSpawn, True )
				if( iValue > 0 ) :
					iValue += CyGame().getSorenRandNum( 100, "Pick SpawnInfo" )
					if( eBestSpawn == None or iValue > iBestValue or ( iValue == iBestValue and CyGame().getSorenRandNum( 2, "Bob" ) == 1 ) ) :
						eBestSpawn = eSpawn
						iBestValue = iValue
		
		return eBestSpawn
		
	def pickNonSpawnOutcome( self, pUnit, bEpic, bNoDestroy ) :
		pPlot = pUnit.plot()
		pPlayer = gc.getPlayer( pUnit.getOwner() )
		
		# Get parameters
		iExploLevel = pUnit.getExplorationLevel()
		iChallenge = pPlot.getLairDanger()
		iChallenge += CyGame().getSorenRandNum( 50, "Explore Lair" ) - 25
		iChallengeHandling = iExploLevel - iChallenge
		iExploLevel += CyGame().getSorenRandNum( 50, "Explore Lair" ) - 25
		
		sDbgMessage = "Exploration parameters: iOriginalExploLevel=%d, iChallange=%d, iChallengeHandling=%d, iExploLevel=%d" % ( pUnit.getExplorationLevel(), iChallenge, iChallengeHandling, iExploLevel )
		CvUtil.pyPrint( sDbgMessage )
		
		dslOutcomes = {}
		
		bMelee = ( pUnit.getUnitCombatType() == self.saveGetInfoType( gc.getNumUnitCombatInfos(), 'UNITCOMBAT_MELEE' ) )
		bAdept = ( pUnit.getUnitCombatType() == self.saveGetInfoType( gc.getNumUnitCombatInfos(), 'UNITCOMBAT_ADEPT' ) )
		bRecon = ( pUnit.getUnitCombatType() == self.saveGetInfoType( gc.getNumUnitCombatInfos(), 'UNITCOMBAT_RECON' ) )
		bArcher = ( pUnit.getUnitCombatType() == self.saveGetInfoType( gc.getNumUnitCombatInfos(), 'UNITCOMBAT_ARCHER' ) )
		bDisciple = ( pUnit.getUnitCombatType() == self.saveGetInfoType( gc.getNumUnitCombatInfos(), 'UNITCOMBAT_DISCIPLE' ) )
		
		bHasBronzeWorking = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_BRONZE_WORKING' ) ) )
		bHasCodeOfLaws = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_CODE_OF_LAWS' ) ) )
		bHasFishing = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_FISHING' ) ) )
		bHasHunting = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_HUNTING' ) ) )
		bHasIronWorking = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_IRON_WORKING' ) ) )
		bHasKnowledgeOfTheEther = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_KNOWLEDGE_OF_THE_ETHER' ) ) )
		bHasMining = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_MINING' ) ) )
		bHasMysticism = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_MYSTICISM' ) ) )
		bHasPoisons = pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_POISONS' ) )
		bHasPriesthood = pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_PRIESTHOOD' ) )
		bHasSorcery = pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_SORCERY' ) )
		bHasTrade = ( pPlayer.isHasTech( self.saveGetInfoType( gc.getNumTechInfos(), 'TECH_TRADE' ) ) )
		
		bBannor = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_BANNOR" ) )
		bElohim = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_ELOHIM" ) )
		bKhazad = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_KHAZAD" ) )
		bLanun = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_LANUN" ) )
		bLjosalfar = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_LJOSALFAR" ) )
		bMalakim = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_MALAKIM" ) )
		bMercurians = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_MERCURIANS" ) )
		bSheaim = ( pPlayer.getCivilizationType() == self.saveGetInfoType( gc.getNumCivilizationInfos(), "CIVILIZATION_SHEAIM" ) )
		
		bGood = ( pPlayer.getAlignment() == gc.getInfoTypeForString( 'ALIGNMENT_GOOD' ) )
		
		# Categories and their weights
		dsiCategories = {
			'Bad' : 1,
			'Neutral' : 1,
			'Good' : 2,
			'Religion' : 1,
			'RemoveMalus' : 2,
			'Item' : 1,
			'Prisoner' : 1,
			'Bonus' : 2
		}
		
		for sCategory in dsiCategories :
			dslOutcomes[sCategory] = []
		
		# BAD
		if( iChallengeHandling < -25 ) :
			if( pUnit.isAlive() ) :
				dslOutcomes['Bad'].append( ( 'Promotions', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_DISEASED', ['PROMOTION_DISEASED'] ) )
			if( iExploLevel < 75 ) :
				if( pUnit.isAlive() ) :
					dslOutcomes['Bad'].append( ( 'Promotions', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_ENRAGED', ['PROMOTION_ENRAGED'] ) )
			if( pUnit.getLevel() == 1 and iChallenge >= 35 ) :
				dslOutcomes['Bad'].append( ( 'Special', 0, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_DEATH', 'DEATH' ) )
				dslOutcomes['Bad'].append( ( 'Promotions', 80, False, "Your Unit receives the Burning Blood Promotion", ['PROMOTION_BURNING_BLOOD'] ) ) # LFGR_TODO
			if( iExploLevel < 25 and iChallenge >= 35 ) :
				if( pUnit.isAlive() ) :
					dslOutcomes['Bad'].append( ( 'Promotions', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_CRAZED', ['PROMOTION_CRAZED'] ) )
					dslOutcomes['Bad'].append( ( 'Promotions', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_POSSESSED', ['PROMOTION_ENRAGED', 'PROMOTION_CRAZED', 'PROMOTION_DEMON'] ) )
			if( iExploLevel < 50 ) :
				if( pUnit.isAlive() ) :
					dslOutcomes['Bad'].append( ( 'Promotions', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_PLAGUED', ['PROMOTION_PLAGUED'] ) )
					dslOutcomes['Bad'].append( ( 'Promotions', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_WITHERED', ['PROMOTION_WITHERED'] ) )
		if( iChallengeHandling < 0 ) :
			if( pUnit.isAlive() ) :
				dslOutcomes['Bad'].append( ( 'Special', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_POISONED', 'POISONED' ) )
			if( not bNoDestroy ) :
				dslOutcomes['Bad'].append( ( 'Damage', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_COLLAPSE', 50, 90, 'DAMAGE_PHYSICAL' ) )
			if( iExploLevel < 75 ) :
				if( pUnit.isAlive() ) :
					dslOutcomes['Bad'].append( ( 'Promotions', 50, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_MUTATED', ['PROMOTION_MUTATED'] ) )
			# LFGR_TODO: Should add damage outcomes for non-alive units here.
		
		# GOOD
		if( iChallengeHandling >= 0 ) :
			if( iChallenge < 35 ) :
				dslOutcomes['Good'].append( ( 'Goody', 90, 'GOODY_EXPLORE_LAIR_HIGH_GOLD' ) )
				dslOutcomes['Good'].append( ( 'Special', 80, True, None, 'TREASURE' ) )
				if( pUnit.isAlive() ) :
					dslOutcomes['Good'].append( ( 'Promotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_SPIRIT_GUIDE', ['PROMOTION_SPIRIT_GUIDE'] ) )
					dslOutcomes['Good'].append( ( 'Goody', 80, 'GOODY_EXPLORE_LAIR_EXPERIENCE' ) )
				if( not pPlot.isWater() ) :
					dslOutcomes['Good'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_SUPPLIES' ) )
					dslOutcomes['Good'].append( ( 'Goody', 80, 'GOODY_EXPLORE_LAIR_ITEM_HEALING_SALVE' ) )
			if( iChallenge >= 35 and iChallenge < 60 ) :
				dslOutcomes['Good'].append( ( 'Promotions', 80, True, "Your Unit receives the Courage Promotion", ['PROMOTION_COURAGE'] ) ) # LFGR_TODO
				if( bMelee ) :
					dslOutcomes['Good'].append( ( 'Promotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_ENCHANTED_BLADE', ['PROMOTION_ENCHANTED_BLADE'] ) )
				if( bAdept ) :
					dslOutcomes['Good'].append( ( 'Promotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_SPELLSTAFF', ['PROMOTION_SPELLSTAFF'] ) )
				if( bRecon ) :
					dslOutcomes['Good'].append( ( 'Promotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_POISONED_BLADE', ['PROMOTION_POISONED_BLADE'] ) )
				if( bArcher ) :
					dslOutcomes['Good'].append( ( 'Promotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_FLAMING_ARROWS', ['PROMOTION_FLAMING_ARROWS'] ) )
				if( bDisciple ) :
					dslOutcomes['Good'].append( ( 'Promotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_SHIELD_OF_FAITH', ['PROMOTION_SHIELD_OF_FAITH'] ) )
				
				if( gc.getUnitInfo( pUnit.getUnitType() ).getWeaponTier() >= 1 ) :
					if( not pUnit.isHasPromotion( gc.getInfoTypeForString( 'PROMOTION_MITHRIL_WEAPONS' ) ) ) :
						if( gc.getUnitInfo( pUnit.getUnitType() ).getWeaponTier() >= 3 and bHasIronWorking ) :
							dslOutcomes['Good'].append( ( 'Special', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_MITHRIL_WEAPONS', 'MITHRIL_WEAPONS' ) )
						if( not pUnit.isHasPromotion( gc.getInfoTypeForString( 'PROMOTION_IRON_WEAPONS' ) ) ) :
							if( gc.getUnitInfo( pUnit.getUnitType() ).getWeaponTier() >= 2 and bHasBronzeWorking ) :
								dslOutcomes['Good'].append( ( 'Special', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_IRON_WEAPONS', 'IRON_WEAPONS' ) )
							if( not pUnit.isHasPromotion( gc.getInfoTypeForString( 'PROMOTION_BRONZE_WEAPONS' ) ) ):
								dslOutcomes['Good'].append( ( 'Promotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BRONZE_WEAPONS', ['PROMOTION_BRONZE_WEAPONS'] ) )
			if( iChallenge >= 60 ) :
				dslOutcomes['Good'].append( ( 'Promotions', 100, True, "Your Unit receives the Valor Promotion", ['PROMOTION_VALOR'] ) ) # LFGR_TODO
				dslOutcomes['Good'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_TREASURE_VAULT' ) )
				dslOutcomes['Good'].append( ( 'Goody', 100, 'GOODY_GRAVE_TECH' ) )
				dslOutcomes['Good'].append( ( 'Special', 100, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_GOLDEN_AGE', 'GOLDEN_AGE' ) )
				if( not pPlot.isWater() ) :
					if( bLjosalfar or bHasHunting ) :
						dslOutcomes['Religion'].append( ( 'Goody', 90, 'GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_LEAVES' ) )
					if( bLanun or bHasFishing ) :
						dslOutcomes['Religion'].append( ( 'Goody', 90, 'GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_OVERLORDS' ) )
					if( bKhazad or bHasMining ) :
						dslOutcomes['Religion'].append( ( 'Goody', 90, 'GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_RUNES' ) )
					if( bHasMysticism ) :
						if( bSheaim or bHasKnowledgeOfTheEther ) :
							dslOutcomes['Religion'].append( ( 'Goody', 90, 'GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ASHEN' ) )
						if( bMalakim or bHasTrade ) :
							dslOutcomes['Religion'].append( ( 'Goody', 90, 'GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_EMPYREAN' ) )
						# LFGR_TODO: Council of Esus: Svartalfar or Trade
						if( bBannor or bHasCodeOfLaws ) :
							dslOutcomes['Religion'].append( ( 'Goody', 90, 'GOODY_EXPLORE_LAIR_PRISONER_DISCIPLE_ORDER' ) )
				if( pUnit.isHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_CRAZED' ) ) ) : # Enraged isn't sufficient
					if( not pUnit.isHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), 'PROMOTION_DEMON' ) ) ) : # For the possessed outcome (we don't know the former race); LFGR_TODO: Save former race in SDTK or create new "Demonic Possession" promo
						dslOutcomes['RemoveMalus'].append( ( 'RemovePromotions', 80, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_REMOVE_CRAZED', ['PROMOTION_ENRAGED', 'PROMOTION_CRAZED'] ) )
			if( iChallenge >= 75 ) :
				if( not pPlot.isWater() ) :
					dslOutcomes['Item'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_ITEM_JADE_TORC' ) )
					dslOutcomes['Item'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_ITEM_ROD_OF_WINDS' ) )
					dslOutcomes['Item'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_ITEM_TIMOR_MASK' ) )
					
					if( bHasHunting and not bHasPoisons ) :
						dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_ASSASSIN' ) )
					if( bHasBronzeWorking and not bHasIronWorking ) :
						dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_CHAMPION' ) )
					if( bHasKnowledgeOfTheEther and not bHasSorcery ) :
						dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_MAGE' ) )
					if( bGood and bHasMysticism and ( not bElohim or not bHasPriesthood ) ) :
						dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_MONK' ) )
					if( bGood and bHasMysticism and not bMercurians ) :
						dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_ANGEL' ) )
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_ARTIST' ) )
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_GENERAL' ) )
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_ENGINEER' ) )
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_MERCHANT' ) )
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_PROPHET' ) )
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_SCIENTIST' ) )
					dslOutcomes['Bonus'].extend( 3 * [( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_MANA', 'BONUS_MANA' )] )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_COPPER', 'BONUS_COPPER' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_GEMS', 'BONUS_GEMS' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_GOLD', 'BONUS_GOLD' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_IRON', 'BONUS_IRON' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_MITHRIL', 'BONUS_MITHRIL' ) )
				if( pPlot.isWater() ) :
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_SEA_SERPENT' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_PEARL', 'BONUS_PEARL' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_CLAM', 'BONUS_CLAM' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_CRAB', 'BONUS_CRAB' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_FISH', 'BONUS_FISH' ) )
					dslOutcomes['Bonus'].append( ( 'Bonus', 100, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_BONUS_SHRIMP', 'BONUS_SHRIMP' ) )
			if( iChallenge >= 90 ) :
				if( not pPlot.isWater() ) :
					dslOutcomes['Prisoner'].append( ( 'Goody', 100, 'GOODY_EXPLORE_LAIR_PRISONER_ADVENTURER' ) )
		
		# NEUTRAL
		bEmpty = True
		for sCategory in dsiCategories :
			if( len( dslOutcomes[sCategory] ) != 0 ) :
				bEmpty = False
				break
		
		if( bEmpty or ( iChallengeHandling >= -25 and iChallengeHandling < 25 ) ) :
			#dslOutcomes['Neutral'].append( ( 'Special', 100, True, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_NOTHING', 'NOTHING' ) )
			if( pUnit.isAlive() ) :
				dslOutcomes['Neutral'].append( ( 'Promotions', 80, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_PROPHECY_MARK', ['PROMOTION_PROPHECY_MARK'] ) )
			if( not pPlot.isWater() ) :
				dslOutcomes['Neutral'].append( ( 'Event', 0, 'EVENTTRIGGER_EXPLORE_LAIR_PORTAL' ) )
				# LFGR_TODO: disabled until fixed
				# dslOutcomes['Neutral'].append( ( 'Event', 100, 'EVENTTRIGGER_EXPLORE_LAIR_DEPTHS' ) )
				dslOutcomes['Neutral'].append( ( 'Event', 80, 'EVENTTRIGGER_EXPLORE_LAIR_DWARF_VS_LIZARDMEN' ) )
				if( not bNoDestroy ) :
					dslOutcomes['Neutral'].append( ( 'Special', 0, False, 'TXT_KEY_MESSAGE_EXPLORE_LAIR_CAGE', 'CAGE' ) )
		
		# Filter outcomes
		dslFilteredOutcomes = {}
		for sCategory in dsiCategories :
			dslFilteredOutcomes[sCategory] = []
			for tOutcome in dslOutcomes[sCategory] :
				bValid = True
				if( tOutcome[0] == 'Promotions' ) :
					lPromotions = tOutcome[4]
					for sPromotion in lPromotions :
						if( pUnit.isHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), sPromotion ) ) ) :
							bValid = False
							break
						# LFGR_TODO: promotion immunity
				if( tOutcome[0] == 'RemovePromotions' ) :
					lPromotions = tOutcome[4]
					bValid = False
					for sPromotion in lPromotions :
						if( pUnit.isHasPromotion( self.saveGetInfoType( gc.getNumPromotionInfos(), sPromotion ) ) ) :
							bValid = True
							break
				elif( tOutcome[0] == 'Goody' ) :
					eGoody = self.saveGetInfoType( gc.getNumGoodyInfos(), tOutcome[2] )
					bValid = pPlayer.canReceiveGoody( pPlot, eGoody, pUnit )
				elif( tOutcome[0] == 'Bonus' ) :
					eBonus = self.saveGetInfoType( gc.getNumBonusInfos(), tOutcome[3] )
					bValid = ( pPlot.getBonusType( -1 ) == -1 ) and pPlot.canHaveBonus( eBonus, False ) and pPlayer.isHasTech( gc.getBonusInfo( eBonus ).getTechReveal() )
					# LFGR_TODO: bonus nearby (when a mechanic to spawn lairs is implemented)
				
				if( bValid ) :
					dslFilteredOutcomes[sCategory].append( tOutcome )
		
		# Choose category
		lsCategories = []
		for sCategory in dsiCategories :
			if( len( dslFilteredOutcomes[sCategory] ) != 0 ) :
				CvUtil.pyPrint( "  Valid category: %s" % sCategory )
				lsCategories.extend( [sCategory] * dsiCategories[sCategory] ) # add it times its weight
		
		if( len( lsCategories ) == 0 ) :
			CvUtil.pyPrint( "No Valid categories!" )
			return None
		
		sCategory = lsCategories[CyGame().getSorenRandNum( len( lsCategories ), "Pick outcome category" )]
		
		CvUtil.pyPrint( "Chosen category: %s" % sCategory )
		
		return dslFilteredOutcomes[sCategory][CyGame().getSorenRandNum( len( dslFilteredOutcomes[sCategory] ), "Pick outcome" )]
	
	def saveGetInfoType( self, iNum, sInfo ) :
		eID = gc.getInfoTypeForString( sInfo )
		if( eID < 0 or eID >= iNum ) :
			raise Exception( "InfoType unknown or wrong: %s" % ( sInfo ) )
		else :
			return eID

# lfgr: removed old exploreLair functions.

# WILDERNESS end

	def formEmpire( self, iCiv, iLeader, iTeam, pCity, iAlignment, pFromPlayer ):
		iPlayer = pFromPlayer.initNewEmpire( iLeader, iCiv )
		if iPlayer != PlayerTypes.NO_PLAYER:
			pPlot = pCity.plot()
			for i in range( pPlot.getNumUnits(), -1, -1 ):
				pUnit = pPlot.getUnit( i )
				pUnit.jumpToNearestValidPlot()
			pPlayer = gc.getPlayer( iPlayer )
			if iTeam != TeamTypes.NO_TEAM:
				if iTeam < pPlayer.getTeam():
					gc.getTeam( iTeam ).addTeam( pPlayer.getTeam() )
				else:
					gc.getTeam( pPlayer.getTeam() ).addTeam( iTeam )
			pPlayer.acquireCity( pCity, False, True )
			pCity = pPlot.getPlotCity()
			pPlayer.initUnit( gc.getInfoTypeForString( 'UNIT_ARCHER' ), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH )
			pPlayer.initUnit( gc.getInfoTypeForString( 'UNIT_ARCHER' ), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH )
			pPlayer.initUnit( gc.getInfoTypeForString( 'UNIT_ARCHER' ), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH )
			pPlayer.initUnit( gc.getInfoTypeForString( 'UNIT_ARCHER' ), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH )
			pPlayer.initUnit( gc.getInfoTypeForString( 'UNIT_WORKER' ), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH )
			if iAlignment != -1:
				pPlayer.setAlignment( iAlignment )
		return pPlayer

	def grace( self ):
		iGrace = 20 * ( int( CyGame().getGameSpeedType() ) + 1 )
		iDiff = gc.getNumHandicapInfos() + 1 - int( gc.getGame().getHandicapType() )
		iGrace = iGrace * iDiff
		iGrace = CyGame().getSorenRandNum( iGrace, "grace" ) + iGrace
		if iGrace > CyGame().getGameTurn():
			return True
		return False

	def doCityFire( self, pCity ):
		iCount = 0
		iDemon = gc.getInfoTypeForString( 'BUILDING_DEMONIC_CITIZENS' )
		for iBuilding in range( gc.getNumBuildingInfos() ):
			if iBuilding != iDemon:
				if pCity.getNumRealBuilding( iBuilding ) > 0:
					if gc.getBuildingInfo( iBuilding ).getConquestProbability() != 100:
##--------		Unofficial Bug Fix: Modified by Denev	--------##
#						if CyGame().getSorenRandNum(100, "City Fire") <= 10:
						if CyGame().getSorenRandNum( 100, "City Fire" ) < 10:
##--------		Unofficial Bug Fix: End Modify			--------##
							pCity.setNumRealBuilding( iBuilding, 0 )
							CyInterface().addMessage( pCity.getOwner(), True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_CITY_FIRE", ( gc.getBuildingInfo( iBuilding ).getDescription(), ) ), '', 1, gc.getBuildingInfo( iBuilding ).getButton(), ColorTypes( 8 ), pCity.getX(), pCity.getY(), True, True )
							iCount += 1
		if iCount == 0:
			CyInterface().addMessage( pCity.getOwner(), True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_CITY_FIRE_NO_DAMAGE", () ), 'AS2D_SPELL_FIRE_ELEMENTAL', 1, 'Art/Interface/Buttons/Fire.dds', ColorTypes( 8 ), pCity.getX(), pCity.getY(), True, True )

	def doHellTerrain( self ):
		iAshenVeil = gc.getInfoTypeForString( 'RELIGION_THE_ASHEN_VEIL' )
		iBurningSands = gc.getInfoTypeForString( 'TERRAIN_BURNING_SANDS' )
		iBanana = gc.getInfoTypeForString( 'BONUS_BANANA' )
		iCotton = gc.getInfoTypeForString( 'BONUS_COTTON' )
		iCorn = gc.getInfoTypeForString( 'BONUS_CORN' )
		iCow = gc.getInfoTypeForString( 'BONUS_COW' )
		iEvil = gc.getInfoTypeForString( 'ALIGNMENT_EVIL' )
		iFarm = gc.getInfoTypeForString( 'IMPROVEMENT_FARM' )
		iFlames = gc.getInfoTypeForString( 'FEATURE_FLAMES' )
		iFlamesSpreadChance = gc.getDefineINT( 'FLAMES_SPREAD_CHANCE' )
		iGulagarm = gc.getInfoTypeForString( 'BONUS_GULAGARM' )
		iHorse = gc.getInfoTypeForString( 'BONUS_HORSE' )
		iInfernal = gc.getInfoTypeForString( 'CIVILIZATION_INFERNAL' )
		iMarble = gc.getInfoTypeForString( 'BONUS_MARBLE' )
		iNeutral = gc.getInfoTypeForString( 'ALIGNMENT_NEUTRAL' )
		iNightmare = gc.getInfoTypeForString( 'BONUS_NIGHTMARE' )
		iPig = gc.getInfoTypeForString( 'BONUS_PIG' )
		iRazorweed = gc.getInfoTypeForString( 'BONUS_RAZORWEED' )
		iRice = gc.getInfoTypeForString( 'BONUS_RICE' )
		iSheep = gc.getInfoTypeForString( 'BONUS_SHEEP' )
		iSheutStone = gc.getInfoTypeForString( 'BONUS_SHEUT_STONE' )
		iSilk = gc.getInfoTypeForString( 'BONUS_SILK' )
		iSnakePillar = gc.getInfoTypeForString( 'IMPROVEMENT_SNAKE_PILLAR' )
		iSugar = gc.getInfoTypeForString( 'BONUS_SUGAR' )
		iToad = gc.getInfoTypeForString( 'BONUS_TOAD' )
		iWheat = gc.getInfoTypeForString( 'BONUS_WHEAT' )
		iForest = gc.getInfoTypeForString( 'FEATURE_FOREST' )
		iJungle = gc.getInfoTypeForString( 'FEATURE_JUNGLE' )
		iAForest = gc.getInfoTypeForString( 'FEATURE_FOREST_ANCIENT' )
		iNForest = gc.getInfoTypeForString( 'FEATURE_FOREST_NEW' )
		iBForest = gc.getInfoTypeForString( 'FEATURE_FOREST_BURNT' )
		iObsPlains = gc.getInfoTypeForString( 'FEATURE_OBSIDIAN_PLAINS' )
		iCount = CyGame().getGlobalCounter()
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			iFeature = pPlot.getFeatureType()
			iTerrain = pPlot.getTerrainType()
			iBonus = pPlot.getBonusType( -1 )
			iImprovement = pPlot.getImprovementType()
			bUntouched = True
			if pPlot.isOwned():
				pPlayer = gc.getPlayer( pPlot.getOwner() )
				iAlignment = pPlayer.getAlignment()
				if pPlayer.getCivilizationType() == iInfernal:
					pPlot.changePlotCounter( 100 )
					bUntouched = False
				if ( bUntouched and pPlayer.getStateReligion() == iAshenVeil or ( iCount >= 50 and iAlignment == iEvil ) or ( iCount >= 75 and iAlignment == iNeutral ) ):
					iX = pPlot.getX()
					iY = pPlot.getY()
					for iiX in range( iX - 1, iX + 2, 1 ):
						for iiY in range( iY - 1, iY + 2, 1 ):
							pAdjacentPlot = CyMap().plot( iiX, iiY )
							if pAdjacentPlot.isNone() == False:
								if pAdjacentPlot.getPlotCounter() > 10:
									pPlot.changePlotCounter( 1 )
									bUntouched = False
			if ( bUntouched and pPlot.isOwned() == False and iCount > 25 ):
				iX = pPlot.getX()
				iY = pPlot.getY()
				for iiX in range( iX - 1, iX + 2, 1 ):
					for iiY in range( iY - 1, iY + 2, 1 ):
						pAdjacentPlot = CyMap().plot( iiX, iiY )
						if pAdjacentPlot.isNone() == False:
							if pAdjacentPlot.getPlotCounter() > 10:
								pPlot.changePlotCounter( 1 )
								bUntouched = False
			iPlotCount = pPlot.getPlotCounter()
			if ( bUntouched and iPlotCount > 0 ):
				pPlot.changePlotCounter( -1 )
			if iPlotCount > 9:
				if ( iBonus == iSheep or iBonus == iPig ):
					pPlot.setBonusType( iToad )
				if ( iBonus == iHorse or iBonus == iCow ):
					pPlot.setBonusType( iNightmare )
				if ( iBonus == iCotton or iBonus == iSilk ):
					pPlot.setBonusType( iRazorweed )
				if ( iBonus == iBanana or iBonus == iSugar ):
					pPlot.setBonusType( iGulagarm )
				if ( iBonus == iMarble ):
					pPlot.setBonusType( iSheutStone )
				if ( iBonus == iCorn or iBonus == iRice or iBonus == iWheat ):
					pPlot.setBonusType( -1 )
					pPlot.setImprovementType( iSnakePillar )

				if ( iFeature == iForest or iFeature == iAForest or iFeature == iNForest or iFeature == iJungle ):
#					iRandom = CyGame().getSorenRandNum(100, "Hell Terrain Burnt Forest")
#					if iRandom < 10:
					pPlot.setFeatureType( iBForest, 0 )
#				if pPlot.isPeak() == True:
#					iRandom = CyGame().getSorenRandNum(100, "Hell Terrain Volcanos")
#					if iRandom < 2:
#						iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(), 'EVENTTRIGGER_VOLCANO_CREATION')
#						triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pPlot.getX(), pPlot.getY(), -1, -1, -1, -1, -1, -1)

			if iPlotCount < 10:
				if iBonus == iToad:
					if CyGame().getSorenRandNum( 100, "Hell Convert" ) < 50:
						pPlot.setBonusType( iSheep )
					else:
						pPlot.setBonusType( iPig )
				if iBonus == iNightmare:
					if CyGame().getSorenRandNum( 100, "Hell Convert" ) < 50:
						pPlot.setBonusType( iHorse )
					else:
						pPlot.setBonusType( iCow )
				if iBonus == iRazorweed:
					if CyGame().getSorenRandNum( 100, "Hell Convert" ) < 50:
						pPlot.setBonusType( iCotton )
					else:
						pPlot.setBonusType( iSilk )
				if iBonus == iGulagarm:
					if CyGame().getSorenRandNum( 100, "Hell Convert" ) < 50:
						pPlot.setBonusType( iBanana )
					else:
						pPlot.setBonusType( iSugar )
				if ( iBonus == iSheutStone ):
					pPlot.setBonusType( iMarble )
				if iImprovement == iSnakePillar:
					pPlot.setImprovementType( iFarm )
					iCount = CyGame().getSorenRandNum( 100, "Hell Convert" )
					if  iCount < 33:
						pPlot.setBonusType( iCorn )
					else:
						if iCount < 66:
							pPlot.setBonusType( iRice )
						else:
							pPlot.setBonusType( iWheat )
			if iTerrain == iBurningSands and not pPlot.isCity() and not pPlot.isPeak() and iFeature != iObsPlains:
				if CyGame().getSorenRandNum(100, "Flames") < iFlamesSpreadChance:
					pPlot.setFeatureType(iFlames, 0)

#AdventurerCounter Start (Imported from Rise from Erebus, modified by Terkhen)
	def getAdventurerThreshold( self, iPlayer):
		pPlayer = gc.getPlayer( iPlayer )
		# We simulate CvPlayer::greatPeopleThreshold(false) to calculate the current threshold based upon the number of spawned adventurers.
		iThresholdModifier = 0
		iSpawnedAdventurers	= pPlayer.getCivCounterMod()
		for iNumAdventurers in range(1, iSpawnedAdventurers+1):
			iThresholdModifier += gc.getDefineINT("GREAT_PEOPLE_THRESHOLD")  * ((iNumAdventurers / 10) + 1)
			iThresholdModifier = max( 0, iThresholdModifier )

		# Threshold based in internal constants and number of adventurers spawned.
		iThreshold = (gc.getDefineINT("GREAT_PEOPLE_THRESHOLD") * max(0, (iThresholdModifier + 100))) / 100
		# Game speed adjustment.
		iThreshold *= gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getGreatPeoplePercent()
		iThreshold /= 100
		#Game era adjustment.
		iThreshold *= gc.getEraInfo(gc.getGame().getStartEra()).getGreatPeoplePercent()
		iThreshold /= 100;
		
		return max(1, iThreshold)

	def getAdventurerPointRate( self, iPlayer):
		pPlayer = gc.getPlayer( iPlayer )

		# Buildings that produce adventurer points are cached only once.
		if (len(lAdventurerBuildings) == 0):
			CvUtil.pyPrint( "  Adventurer Counter: The cache of buildings that grant Adventurer points needs to be initialized." )
			for iBuilding in range(gc.getNumBuildingInfos()):
				pBuildingInfo = gc.getBuildingInfo(iBuilding)
				if (pBuildingInfo.getGreatPeopleUnitClass() == gc.getInfoTypeForString( 'UNITCLASS_ADVENTURER' )):
					CvUtil.pyPrint( "    Adventurer Counter: %s grants %i adventurer points." % (pBuildingInfo.getDescription(), pBuildingInfo.getGreatPeopleRateChange()) )
					lAdventurerBuildings.append(iBuilding)
					lAdventurerBuildingsPoints.append(pBuildingInfo.getGreatPeopleRateChange())

		# Calculate the amount of adventurer points granted by each city.
		fTotalPoints = 0.0
		apCityList = PyPlayer(iPlayer).getCityList()
		CvUtil.pyPrint( "  Adventurer Counter: Calculating the amount of points contributed by cities." )
		for pyCity in apCityList:
			pCity = pyCity.GetCy()
			if not pCity.isDisorder():
				fCityPoints = 0.0
				for i in range(len(lAdventurerBuildings)):
					fCityPoints += pCity.getNumBuilding(lAdventurerBuildings[i]) * lAdventurerBuildingsPoints[i]
				# This value already takes into account any changes to GPP caused by civics, traits, buildings...
				CvUtil.pyPrint( "    Adventurer Counter: %s contributes with %f points." % (pCity.getName(), fCityPoints))
				fCityPoints = (fCityPoints * pCity.getTotalGreatPeopleRateModifier()) / 100.0
				CvUtil.pyPrint( "    Adventurer Counter: After applying the rate modifier, %s contributes with %f points." % (pCity.getName(), fCityPoints))
				fTotalPoints += fCityPoints


		# The value is converted to integer.
		iTotalPoints = int(round(fTotalPoints))
		CvUtil.pyPrint( "  Adventurer Counter: The total number of points contributed by cities is: %i." % iTotalPoints)
		return iTotalPoints

	def doTurnGrigori( self, iPlayer ):
		CvUtil.pyPrint( "Adventurer Counter: Start." )
		pPlayer = gc.getPlayer( iPlayer )

		self.doChanceAdventurerSpawn( iPlayer )

		iSpawnedAdventurers	= pPlayer.getCivCounterMod()

		# Initialize the number of spawned adventurers in case it has not been initialized.		
		if iSpawnedAdventurers < 0:
			CvUtil.pyPrint( "  Adventurer Counter: Initializing number of already spawned adventurers to 0." )
			pPlayer.setCivCounterMod( 0 )
			iSpawnedAdventurers = 0

		CvUtil.pyPrint( "  Adventurer Counter: Number of adventurers already spawned : %i" % iSpawnedAdventurers )
		iCurrentPoints		= pPlayer.getCivCounter()
		CvUtil.pyPrint( "  Adventurer Counter: Current number of adventurer points : %i" % iCurrentPoints )
		# Calculate current adventurer threshold.
		iThreshold = self.getAdventurerThreshold(iPlayer)
		CvUtil.pyPrint( "  Adventurer Counter: Current threshold : %i" % iThreshold )
		if iCurrentPoints >= iThreshold:
			CvUtil.pyPrint( "  Adventurer Counter: The threshold has been surpassed so a new adventurer is going to be created." )
			# Spawn an adventurer in the capital.
			pCapital = pPlayer.getCapitalCity()
			pAdventurer = pPlayer.createGreatPeople( gc.getInfoTypeForString( 'UNIT_ADVENTURER' ), False, False, pCapital.getX(), pCapital.getY() )
			# Reduce the number of adventurer points.
			pPlayer.changeCivCounter( 0 - iThreshold )
			# Increase the amount of built adventurers.
			pPlayer.changeCivCounterMod( 1 )

	def doChanceAdventurerSpawn( self, iPlayer ):
		iTotalPoints = self.getAdventurerPointRate( iPlayer )
		pPlayer = gc.getPlayer( iPlayer )
		pPlayer.changeCivCounter(iTotalPoints)
#AdventurerCounter End

	def doTurnKhazad( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		if pPlayer.getNumCities() > 0:
			iVault1 = gc.getInfoTypeForString( 'BUILDING_DWARVEN_VAULT_EMPTY' )
			iVault2 = gc.getInfoTypeForString( 'BUILDING_DWARVEN_VAULT_LOW' )
			iVault3 = gc.getInfoTypeForString( 'BUILDING_DWARVEN_VAULT' )
			iVault4 = gc.getInfoTypeForString( 'BUILDING_DWARVEN_VAULT_STOCKED' )
			iVault5 = gc.getInfoTypeForString( 'BUILDING_DWARVEN_VAULT_ABUNDANT' )
			iVault6 = gc.getInfoTypeForString( 'BUILDING_DWARVEN_VAULT_FULL' )
			iVault7 = gc.getInfoTypeForString( 'BUILDING_DWARVEN_VAULT_OVERFLOWING' )
			iGold = pPlayer.getGold() / pPlayer.getNumCities()
			if iGold <= 24:
				iNewVault = iVault1
			if (iGold >= 25 and iGold <= 49):
				iNewVault = iVault2
			if (iGold >= 50 and iGold <= 74):
				iNewVault = iVault3
			if (iGold >= 75 and iGold <= 99):
				iNewVault = iVault4
			if (iGold >= 100 and iGold <= 149):
				iNewVault = iVault5
			if (iGold >= 150 and iGold <= 249):
				iNewVault = iVault6
			if iGold >= 250:
				iNewVault = iVault7
			for pyCity in PyPlayer( iPlayer ).getCityList():
				pCity = pyCity.GetCy()
				pCity.setNumRealBuilding( iVault1, 0 )
				pCity.setNumRealBuilding( iVault2, 0 )
				pCity.setNumRealBuilding( iVault3, 0 )
				pCity.setNumRealBuilding( iVault4, 0 )
				pCity.setNumRealBuilding( iVault5, 0 )
				pCity.setNumRealBuilding( iVault6, 0 )
				pCity.setNumRealBuilding( iVault7, 0 )
				pCity.setNumRealBuilding( iNewVault, 1 )

	def doTurnLuchuirp( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		if pPlayer.getUnitClassCount( gc.getInfoTypeForString( 'UNITCLASS_BARNAXUS' ) ) > 0:
			py = PyPlayer( iPlayer )
			pBarnaxus = -1
			bEmp1 = False
			bEmp2 = False
			bEmp3 = False
			bEmp4 = False
			bEmp5 = False
			iBarnaxus = gc.getInfoTypeForString( 'UNITCLASS_BARNAXUS' )
			iCombat1 = gc.getInfoTypeForString( 'PROMOTION_COMBAT1' )
			iCombat2 = gc.getInfoTypeForString( 'PROMOTION_COMBAT2' )
			iCombat3 = gc.getInfoTypeForString( 'PROMOTION_COMBAT3' )
			iCombat4 = gc.getInfoTypeForString( 'PROMOTION_COMBAT4' )
			iCombat5 = gc.getInfoTypeForString( 'PROMOTION_COMBAT5' )
			iEmpower1 = gc.getInfoTypeForString( 'PROMOTION_EMPOWER1' )
			iEmpower2 = gc.getInfoTypeForString( 'PROMOTION_EMPOWER2' )
			iEmpower3 = gc.getInfoTypeForString( 'PROMOTION_EMPOWER3' )
			iEmpower4 = gc.getInfoTypeForString( 'PROMOTION_EMPOWER4' )
			iEmpower5 = gc.getInfoTypeForString( 'PROMOTION_EMPOWER5' )
			iGolem = gc.getInfoTypeForString( 'PROMOTION_GOLEM' )

			lGolems = []
			for pUnit in py.getUnitList():
				if pUnit.getUnitClassType() == iBarnaxus :
					pBarnaxus = pUnit
				elif pUnit.isHasPromotion( iGolem ) :
					lGolems.append( pUnit )
			if pBarnaxus != -1 :
				bEmp1 = bool( pBarnaxus.isHasPromotion( iCombat1 ) )
				bEmp2 = bool( pBarnaxus.isHasPromotion( iCombat2 ) )
				bEmp3 = bool( pBarnaxus.isHasPromotion( iCombat3 ) )
				bEmp4 = bool( pBarnaxus.isHasPromotion( iCombat4 ) )
				bEmp5 = bool( pBarnaxus.isHasPromotion( iCombat5 ) )
			for pUnit in lGolems :
				pUnit.setHasPromotion( iEmpower1, False )
				pUnit.setHasPromotion( iEmpower2, False )
				pUnit.setHasPromotion( iEmpower3, False )
				pUnit.setHasPromotion( iEmpower4, False )
				pUnit.setHasPromotion( iEmpower5, False )
				if bEmp1:
					pUnit.setHasPromotion( iEmpower1, True )
				if bEmp2:
					pUnit.setHasPromotion( iEmpower2, True )
				if bEmp3:
					pUnit.setHasPromotion( iEmpower3, True )
				if bEmp4:
					pUnit.setHasPromotion( iEmpower4, True )
				if bEmp5:
					pUnit.setHasPromotion( iEmpower5, True )
		elif pPlayer.getUnitClassCount( gc.getInfoTypeForString( 'EQUIPMENTCLASS_PIECES_OF_BARNAXUS' ) ) == 1:
			if pPlayer.getNumUnits() == 1:
				py = PyPlayer( iPlayer )
				for pUnit in py.getUnitList():
					pUnit.kill( true )

	def findClearPlot( self, pUnit, plot ):
		BestPlot = -1
		iBestPlot = 0
		if pUnit == -1:
			iX = plot.getX()
			iY = plot.getY()
			for iiX in range( iX - 1, iX + 2, 1 ):
				for iiY in range( iY - 1, iY + 2, 1 ):
					iCurrentPlot = 0
					pPlot = CyMap().plot( iiX, iiY )
					if pPlot.isNone() == False:
						if pPlot.getNumUnits() == 0:
							if ( pPlot.isWater() == plot.isWater() and pPlot.isPeak() == False and pPlot.isCity() == False ):
								iCurrentPlot = iCurrentPlot + 5
						if iCurrentPlot >= 1:
							iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum( 5, "FindClearPlot" )
							if iCurrentPlot >= iBestPlot:
								BestPlot = pPlot
								iBestPlot = iCurrentPlot
			return BestPlot
		iX = pUnit.getX()
		iY = pUnit.getY()
		for iiX in range( iX - 1, iX + 2, 1 ):
			for iiY in range( iY - 1, iY + 2, 1 ):
				iCurrentPlot = 0
				pPlot = CyMap().plot( iiX, iiY )
				if pPlot.isNone() == False:
					if pPlot.getNumUnits() == 0:
						if pUnit.canMoveOrAttackInto( pPlot, False ):
							iCurrentPlot = iCurrentPlot + 5
					for i in range( pPlot.getNumUnits() ):
						if pPlot.getUnit( i ).getOwner() == pUnit.getOwner():
							if pUnit.canMoveOrAttackInto( pPlot, False ):
								iCurrentPlot = iCurrentPlot + 15
					if pPlot.isCity():
						if pPlot.getPlotCity().getOwner() == pUnit.getOwner():
							iCurrentPlot = iCurrentPlot + 50
					if ( iX == iiX and iY == iiY ):
						iCurrentPlot = 0
					if iCurrentPlot >= 1:
						iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum( 5, "FindClearPlot" )
						if iCurrentPlot >= iBestPlot:
							BestPlot = pPlot
							iBestPlot = iCurrentPlot
		return BestPlot

	def genesis( self, iPlayer ):
		iBrokenLands = gc.getInfoTypeForString( 'TERRAIN_BROKEN_LANDS' )
		iBurningSands = gc.getInfoTypeForString( 'TERRAIN_BURNING_SANDS' )
		iDesert = gc.getInfoTypeForString( 'TERRAIN_DESERT' )
		iFields = gc.getInfoTypeForString( 'TERRAIN_FIELDS_OF_PERDITION' )
		iGrass = gc.getInfoTypeForString( 'TERRAIN_GRASS' )
		iSnow = gc.getInfoTypeForString( 'TERRAIN_SNOW' )
		iTundra = gc.getInfoTypeForString( 'TERRAIN_TUNDRA' )
		iPlains = gc.getInfoTypeForString( 'TERRAIN_PLAINS' )
		iForestAncient = gc.getInfoTypeForString( 'FEATURE_FOREST_ANCIENT' )
		iForest = gc.getInfoTypeForString( 'FEATURE_FOREST' )
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			if pPlot.getOwner() == iPlayer:
				iTerrain = pPlot.getTerrainType()
				if iTerrain == iSnow:
					pPlot.setTerrainType( iTundra, True, True )
				if iTerrain == iTundra:
					pPlot.setTerrainType( iPlains, True, True )
				if ( iTerrain == iDesert or iTerrain == iBurningSands ):
					pPlot.setTerrainType( iPlains, True, True )
				if ( iTerrain == iPlains or iTerrain == iFields or iTerrain == iBrokenLands ):
					pPlot.setTerrainType( iGrass, True, True )
				if ( iTerrain == iGrass and pPlot.getImprovementType() == -1 and pPlot.getFeatureType() != iForestAncient and pPlot.isPeak() == False and pPlot.isCity() == False ):
					pPlot.setFeatureType( iForest, 0 )
				iTemp = pPlot.getFeatureType()
				pPlot.changePlotCounter( -100 )
				if iTemp != -1:
					pPlot.setFeatureType( iTemp, 0 )

	def snowgenesis( self, iPlayer ):
		iSnow = gc.getInfoTypeForString( 'TERRAIN_SNOW' )
		iTundra = gc.getInfoTypeForString( 'TERRAIN_TUNDRA' )
		iPlains = gc.getInfoTypeForString( 'TERRAIN_PLAINS' )
		iDesert = gc.getInfoTypeForString( 'TERRAIN_DESERT' )
		iGrass = gc.getInfoTypeForString( 'TERRAIN_GRASS' )
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			if pPlot.getOwner() == iPlayer:
				pPlot.changePlotCounter( 0 )
				if( pPlot.getTerrainType() == iGrass ):
					pPlot.setTerrainType( iSnow, True, True )
				elif( pPlot.getTerrainType() == iPlains ):
					pPlot.setTerrainType( iSnow, True, True )
				elif( pPlot.getTerrainType() == iDesert ):
					pPlot.setTerrainType( iTundra, True, True )

##--------		Tweaked Hyborem: Added by Denev	--------##
	def getAshenVeilCities( self, iCasterPlayer, iCasterID, iNum ):
		pCasterPlayer = gc.getPlayer( iCasterPlayer )
		pCaster = pCasterPlayer.getUnit( iCasterID )

		iVeil = gc.getInfoTypeForString( 'RELIGION_THE_ASHEN_VEIL' )
		ltVeilCities = []

		for iPlayer in range( gc.getMAX_PLAYERS() ):
			pTargetPlayer = gc.getPlayer( iPlayer )

			if not pTargetPlayer.isAlive():
				continue

			if pTargetPlayer.getTeam() == pCasterPlayer.getTeam():
				continue

			if ( gc.getTeam( pCasterPlayer.getTeam() ).isVassal( pTargetPlayer.getTeam() ) ):
				continue

			iBaseModifier = 100
			if pTargetPlayer.getStateReligion() == iVeil:
				iBaseModifier -= 20
			if pTargetPlayer.getAlignment() == gc.getInfoTypeForString( 'ALIGNMENT_EVIL' ):
				iBaseModifier -= 10

			for pyCity in PyPlayer( iPlayer ).getCityList():
				pTargetCity = pyCity.GetCy()
				if pTargetCity.isHasReligion( iVeil ) and not pTargetCity.isCapital():
					iValue = pTargetCity.getPopulation() * 100
					iValue += pTargetCity.getCulture( iPlayer ) / 3
					iValue += pTargetCity.getNumBuildings() * 10
					iValue += pTargetCity.getNumWorldWonders() * 100
					iValue += pTargetCity.countNumImprovedPlots()

					iModifier = iBaseModifier
					pCasterCapital = pCasterPlayer.getCapitalCity()
					if not pCasterCapital.isNone() and pTargetCity.area().getID() == pCasterCapital.area().getID():
						iModifier += 10
					if pTargetCity.area().getCitiesPerPlayer( iCasterPlayer ) > 0:
						iModifier += 10

					if pCasterPlayer.getNumCities() > 0:
						iMinDistance = -1
						for pyCity in PyPlayer( iCasterPlayer ).getCityList():
							pLoopCity = pyCity.GetCy()
							if pLoopCity.getID() == pTargetCity.getID():
								continue
							iDistance = stepDistance( pLoopCity.getX(), pLoopCity.getY(), pTargetCity.getX(), pTargetCity.getY() )
							if iMinDistance == -1 or iMinDistance > iDistance:
								iMinDistance = iDistance
						if iMinDistance != -1:
							iModifier -= iMinDistance

					iModifier = max( 0, iModifier )
					iValue = ( iValue * iModifier ) // 100

					ltVeilCities.append( ( iValue, pTargetCity ) )

		ltVeilCities.sort()
		ltVeilCities.reverse()
		lpVeilCities = []
		if len( ltVeilCities ) > 0:
			ltVeilCities = ltVeilCities[0:min( iNum, len( ltVeilCities ) )]
			lpVeilCities = [pCity for iValue, pCity in ltVeilCities]
		return lpVeilCities
##--------		Tweaked Hyborem: End Modify			--------##

	def getCivilization( self, iCiv ):
		i = -1
		for iPlayer in range( gc.getMAX_PLAYERS() ):
			pPlayer = gc.getPlayer( iPlayer )
			if pPlayer.getCivilizationType() == iCiv:
				i = iPlayer
		return i

	def getHero( self, pPlayer ):
		iHero = -1
		iHeroUnit = gc.getCivilizationInfo( pPlayer.getCivilizationType() ).getHero()
		if iHeroUnit != -1:
			iHero = gc.getUnitInfo( iHeroUnit ).getUnitClassType()
		return iHero

	def getLeader( self, iLeader ):
		i = -1
		for iPlayer in range( gc.getMAX_PLAYERS() ):
			pPlayer = gc.getPlayer( iPlayer )
			if pPlayer.getLeaderType() == iLeader:
				i = iPlayer
		return i

	def getOpenPlayer( self ):
		i = -1
		for iPlayer in range( gc.getMAX_PLAYERS() ):
			pPlayer = gc.getPlayer( iPlayer )
			if ( pPlayer.isEverAlive() == False and i == -1 ):
				i = iPlayer
		return i

	def getUnholyVersion( self, pUnit ):
		iUnit = -1
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_ADEPT' ):
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 2:
				iUnit = gc.getInfoTypeForString( 'UNIT_IMP' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 3:
				iUnit = gc.getInfoTypeForString( 'UNIT_MAGE' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 4:
				iUnit = gc.getInfoTypeForString( 'UNIT_LICH' )
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_ANIMAL' ) or pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_BEAST' ):
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 1:
				iUnit = gc.getInfoTypeForString( 'UNIT_SCOUT' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 2:
				iUnit = gc.getInfoTypeForString( 'UNIT_HELLHOUND' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 3:
				iUnit = gc.getInfoTypeForString( 'UNIT_ASSASSIN' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 4:
				iUnit = gc.getInfoTypeForString( 'UNIT_BEAST_OF_AGARES' )
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_ARCHER' ):
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 2:
				iUnit = gc.getInfoTypeForString( 'UNIT_ARCHER' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 3:
				iUnit = gc.getInfoTypeForString( 'UNIT_LONGBOWMAN' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 4:
				iUnit = gc.getInfoTypeForString( 'UNIT_CROSSBOWMAN' )
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_DISCIPLE' ):
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 2:
				iUnit = gc.getInfoTypeForString( 'UNIT_DISCIPLE_THE_ASHEN_VEIL' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 3:
				iUnit = gc.getInfoTypeForString( 'UNIT_PRIEST_OF_THE_VEIL' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 4:
				iUnit = gc.getInfoTypeForString( 'UNIT_EIDOLON' )
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_MELEE' ):
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 1:
				iUnit = gc.getInfoTypeForString( 'UNIT_SKELETON' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 2:
				iUnit = gc.getInfoTypeForString( 'UNIT_DISEASED_CORPSE' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 3:
				iUnit = gc.getInfoTypeForString( 'UNIT_CHAMPION' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 4:
				iUnit = gc.getInfoTypeForString( 'UNIT_BALOR' )
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_MOUNTED' ):
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 2:
				iUnit = gc.getInfoTypeForString( 'UNIT_HORSEMAN' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 3:
				iUnit = gc.getInfoTypeForString( 'UNIT_CHARIOT' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 4:
				iUnit = gc.getInfoTypeForString( 'UNIT_DEATH_KNIGHT' )
		if pUnit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_RECON' ):
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 1:
				iUnit = gc.getInfoTypeForString( 'UNIT_SCOUT' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 2:
				iUnit = gc.getInfoTypeForString( 'UNIT_HELLHOUND' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 3:
				iUnit = gc.getInfoTypeForString( 'UNIT_ASSASSIN' )
			if gc.getUnitInfo( pUnit.getUnitType() ).getTier() == 4:
				iUnit = gc.getInfoTypeForString( 'UNIT_BEASTMASTER' )
		return iUnit

	def getUnitPlayerID( self, pUnit ):
		pPlayer = gc.getPlayer( pUnit.getOwner() )
		iID = pUnit.getID()
		iUnitID = -1
		for iUnit in range( pPlayer.getNumUnits() ):
			pLoopUnit = pPlayer.getUnit( iUnit )
			if pLoopUnit.getID() == iID:
				iUnitID = iUnit
		return iUnitID

	def giftUnit( self, iUnit, iCivilization, iXP, pFromPlot, iFromPlayer ):
		iAngel = gc.getInfoTypeForString( 'UNIT_ANGEL' )
		iManes = gc.getInfoTypeForString( 'UNIT_MANES' )
		if ( iUnit == iAngel or iUnit == iManes ):
			iChance = 100 - ( CyGame().countCivPlayersAlive() * 3 )
			iChance = iChance + iXP
			if iChance < 5:
				iChance = 5
			if iChance > 95:
				iChance = 95
			if CyGame().getSorenRandNum( 100, "Gift Unit" ) > iChance:
				iUnit = -1
		if iUnit != -1:
			bValid = False
			for iPlayer in range( gc.getMAX_PLAYERS() ):
				pPlayer = gc.getPlayer( iPlayer )
				if ( pPlayer.isAlive() ):
					if pPlayer.getCivilizationType() == iCivilization:
						py = PyPlayer( iPlayer )
						if pPlayer.getNumCities() > 0:
							iRnd = CyGame().getSorenRandNum( py.getNumCities(), "Gift Unit" )
							pCity = py.getCityList()[iRnd]
							pPlot = pCity.plot()
							newUnit = pPlayer.initUnit( iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH )
							newUnit.changeExperience( iXP, -1, False, False, False )
							newUnit.setWeapons()
							if ( pFromPlot != -1 and gc.getPlayer( iFromPlayer ).isHuman() ):
								bValid = True
							if pPlayer.isHuman():
								if iUnit == iManes:
									CyInterface().addMessage( iPlayer, True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_ADD_MANES", () ), 'AS2D_UNIT_FALLS', 1, 'Art/Interface/Buttons/Promotions/Demon.dds', ColorTypes( 7 ), pPlot.getX(), pPlot.getY(), True, True )
								if iUnit == iAngel:
									CyInterface().addMessage( iPlayer, True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_ADD_ANGEL", () ), 'AS2D_UNIT_FALLS', 1, 'Art/Interface/Buttons/Promotions/Angel.dds', ColorTypes( 7 ), pPlot.getX(), pPlot.getY(), True, True )
#							if (pPlayer.isHuman() == False and iUnit == iManes and pCity != -1):
#								if CyGame().getSorenRandNum(100, "Manes") < (100 - (pCity.getPopulation() * 5)):
#									pCity.changePopulation(1)
#									newUnit.kill(True, PlayerTypes.NO_PLAYER)
			if bValid:
				if iUnit == iManes:
					CyInterface().addMessage( iFromPlayer, True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_UNIT_FALLS", () ), 'AS2D_UNIT_FALLS', 1, 'Art/Interface/Buttons/Promotions/Demon.dds', ColorTypes( 7 ), pFromPlot.getX(), pFromPlot.getY(), True, True )
				if iUnit == iAngel:
					CyInterface().addMessage( iFromPlayer, True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_UNIT_RISES", () ), 'AS2D_UNIT_FALLS', 1, 'Art/Interface/Buttons/Promotions/Angel.dds', ColorTypes( 7 ), pFromPlot.getX(), pFromPlot.getY(), True, True )

	def placeTreasure( self, iPlayer, iUnit ):
		pPlayer = gc.getPlayer( iPlayer )
		pBestPlot = -1
		iBestPlot = -1
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			iPlot = -1
			if not pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					if not pPlot.isCity():
						if not pPlot.isImpassable():
							iPlot = CyGame().getSorenRandNum( 1000, "Add Unit" )
							if pPlot.area().getNumTiles() < 8:
								iPlot += 1000
							if not pPlot.isOwned():
								iPlot += 1000
							if iPlot > iBestPlot:
								iBestPlot = iPlot
								pBestPlot = pPlot
		if iBestPlot != -1:
			newUnit = pPlayer.initUnit( iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH )
			CyInterface().addMessage( iPlayer, True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_EXPLORE_LAIR_TREASURE", () ), '', 1, 'Art/Interface/Buttons/Equipment/Treasure.dds', ColorTypes( 8 ), newUnit.getX(), newUnit.getY(), True, True )
			CyCamera().JustLookAtPlot( pBestPlot )

	def showUniqueImprovements( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		iTeam = pPlayer.getTeam()
		for i in range ( CyMap().numPlots() ):
			pPlot = CyMap().plotByIndex( i )
			if pPlot.getImprovementType() != -1:
				if gc.getImprovementInfo( pPlot.getImprovementType() ).isUnique():
					pPlot.setRevealed( iTeam, True, False, TeamTypes.NO_TEAM )

	def startWar( self, iPlayer, i2Player, iWarPlan ):
		iTeam = gc.getPlayer( iPlayer ).getTeam()
		i2Team = gc.getPlayer( i2Player ).getTeam()
		eTeam = gc.getTeam( iTeam )
		e2Team = gc.getTeam( i2Team )
		if eTeam.isAlive():
			if e2Team.isAlive():
				if not eTeam.isAtWar( i2Team ):
					if iTeam != i2Team:
						if eTeam.isHasMet( i2Team ):
							if not eTeam.isPermanentWarPeace( i2Team ):
								eTeam.declareWar( i2Team, false, iWarPlan )

	def warScript( self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		iEnemy = -1
		for iPlayer2 in range( gc.getMAX_PLAYERS() ):
			pPlayer2 = gc.getPlayer( iPlayer2 )
			if pPlayer2.isAlive():
				iTeam = gc.getPlayer( iPlayer ).getTeam()
				iTeam2 = gc.getPlayer( iPlayer2 ).getTeam()
				eTeam = gc.getTeam( iTeam )
				if eTeam.isAVassal() == False:
					if eTeam.isAtWar( iTeam2 ):
						if CyGame().getSorenRandNum( 100, "War Script" ) < 5:
							self.dogpile( iPlayer, iPlayer2 )
					if self.warScriptAllow( iPlayer, iPlayer2 ):
						if pPlayer2.getBuildingClassMaking( gc.getInfoTypeForString( 'BUILDINGCLASS_TOWER_OF_MASTERY' ) ) > 0:
							if eTeam.getAtWarCount( True ) == 0:
								self.startWar( iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL )
						if ( pPlayer2.getNumBuilding( gc.getInfoTypeForString( 'BUILDING_ALTAR_OF_THE_LUONNOTAR_DIVINE' ) ) > 0 or pPlayer2.getNumBuilding( gc.getInfoTypeForString( 'BUILDING_ALTAR_OF_THE_LUONNOTAR_EXALTED' ) ) > 0 ):
							if pPlayer.getAlignment() == gc.getInfoTypeForString( 'ALIGNMENT_EVIL' ):
								if eTeam.getAtWarCount( True ) == 0:
									self.startWar( iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL )
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_MERCURIANS' ):
							if pPlayer2.getStateReligion() == gc.getInfoTypeForString( 'RELIGION_THE_ASHEN_VEIL' ):
								self.startWar( iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL )
						if CyGame().getGlobalCounter() > 20:
							if pPlayer.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_SVARTALFAR' ):
								if ( pPlayer2.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_LJOSALFAR' ) and CyGame().getPlayerRank( iPlayer ) > CyGame().getPlayerRank( iPlayer2 ) ):
									self.startWar( iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL )
							if pPlayer.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_LJOSALFAR' ):
								if ( pPlayer2.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_SVARTALFAR' ) and CyGame().getPlayerRank( iPlayer ) > CyGame().getPlayerRank( iPlayer2 ) ):
									self.startWar( iPlayer, iPlayer2, WarPlanTypes.WARPLAN_TOTAL )
						if ( CyGame().getGlobalCounter() > 40 or pPlayer.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_INFERNAL' ) or pPlayer.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_DOVIELLO' ) ):
							if pPlayer.getAlignment() == gc.getInfoTypeForString( 'ALIGNMENT_EVIL' ):
								if ( eTeam.getAtWarCount( True ) == 0 and CyGame().getPlayerRank( iPlayer2 ) > CyGame().getPlayerRank( iPlayer ) ):
									if ( iEnemy == -1 or CyGame().getPlayerRank( iPlayer2 ) > CyGame().getPlayerRank( iEnemy ) ):
										iEnemy = iPlayer2
		if iEnemy != -1:
			if CyGame().getPlayerRank( iPlayer ) > CyGame().getPlayerRank( iEnemy ):
				self.startWar( iPlayer, iEnemy, WarPlanTypes.WARPLAN_TOTAL )

	def warScriptAllow( self, iPlayer, iPlayer2 ):
		pPlayer = gc.getPlayer( iPlayer )
		pPlayer2 = gc.getPlayer( iPlayer2 )
		iTeam = gc.getPlayer( iPlayer ).getTeam()
		iTeam2 = gc.getPlayer( iPlayer2 ).getTeam()
		eTeam = gc.getTeam( iTeam )
		if iPlayer == gc.getBARBARIAN_PLAYER():
			return False
		if eTeam.isHasMet( iTeam2 ) == False:
			return False
		if eTeam.AI_getAtPeaceCounter( iTeam2 ) < 20:
			return False
#		if pPlayer.AI_getAttitude(iPlayer2) <= gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDeclareWarRefuseAttitudeThreshold():
#			return False
		if eTeam.isAtWar( iTeam2 ):
			return False
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_INFERNAL' ):
			if pPlayer2.getStateReligion() == gc.getInfoTypeForString( 'RELIGION_THE_ASHEN_VEIL' ):
				return False
		return True

	def dogpile( self, iPlayer, iVictim ):
		pPlayer = gc.getPlayer( iPlayer )
		for iPlayer2 in range( gc.getMAX_PLAYERS() ):
			pPlayer2 = gc.getPlayer( iPlayer2 )
			iChance = -1
			if pPlayer2.isAlive():
				if ( self.dogPileAllow( iPlayer, iPlayer2 ) and self.warScriptAllow( iPlayer2, iVictim ) ):
					iChance = pPlayer2.AI_getAttitude( iPlayer ) * 5
					if iChance > 0:
						iChance = iChance - ( pPlayer2.AI_getAttitude( iVictim ) * 5 ) - 10
						if CyGame().isOption( gc.getInfoTypeForString( 'GAMEOPTION_AGGRESSIVE_AI' ) ) == False:
							iChance = iChance - 10
						if iChance > 0:
							iChance = iChance + ( CyGame().getGlobalCounter() / 3 )
							if pPlayer2.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_BALSERAPHS' ):
								iChance = CyGame().getSorenRandNum( 50, "Dogpile" )
							if CyGame().getSorenRandNum( 100, "Dogpile" ) < iChance:
								self.startWar( iPlayer2, iVictim, WarPlanTypes.WARPLAN_DOGPILE )

	def dogPileAllow( self, iPlayer, iPlayer2 ):
		pPlayer = gc.getPlayer( iPlayer )
		pPlayer2 = gc.getPlayer( iPlayer2 )
		iTeam = gc.getPlayer( iPlayer ).getTeam()
		iTeam2 = gc.getPlayer( iPlayer2 ).getTeam()
		if iPlayer == iPlayer2:
			return False
		if iTeam == iTeam2:
			return False
		if pPlayer2.isHuman():
			return False
		if pPlayer2.getCivilizationType() == gc.getInfoTypeForString( 'CIVILIZATION_ELOHIM' ):
			return False
		if gc.getTeam( iTeam2 ).isAVassal():
			return False
		return True

	def warn( self, iPlayer, szText, pPlot ):
		pPlayer = gc.getPlayer( iPlayer )
		for iPlayer2 in range( gc.getMAX_PLAYERS() ):
			pPlayer2 = gc.getPlayer( iPlayer2 )
			if ( pPlayer2.isAlive() and iPlayer != iPlayer2 ):
				if pPlayer2.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType( ButtonPopupTypes.BUTTONPOPUP_PYTHON )
					popupInfo.setText( szText )
					popupInfo.setOnClickedPythonCallback( "selectWarn" )
					popupInfo.addPythonButton( CyTranslator().getText( "TXT_KEY_MAIN_MENU_OK", () ), "" )
					popupInfo.addPopup( iPlayer2 )
				if pPlot != -1:
					CyInterface().addMessage( iPlayer2, True, 25, CyTranslator().getText( "TXT_KEY_MESSAGE_ALTAR_OF_THE_LUONNOTAR", () ), 'AS2D_DISCOVERBONUS', 1, 'Art/Interface/Buttons/Buildings/AltaroftheLuonnotar.dds', ColorTypes( 7 ), pPlot.getX(), pPlot.getY(), True, True )

	def MarnokNameGenerator( self, unit ):
		pPlayer = gc.getPlayer( unit.getOwner() )	
		pCiv = pPlayer.getCivilizationType() 
		pReligion = pPlayer.getStateReligion()
		pAlign = pPlayer.getAlignment() 

		lPre = ["ta", "go", "da", "bar", "arc", "ken", "an", "ad", "mi", "kon", "kar", "mar", "wal", "he", "ha", "re", "ar", "bal", "bel", "bo", "bri", "car", "dag", "dan", "ma", "ja", "co", "be", "ga", "qui", "sa"]
		lMid = ["ad", "z", "the", "and", "tha", "ent", "ion", "tio", "for", "tis", "oft", "che", "gan", "an", "en", "wen", "on", "d", "n", "g", "t", "ow", "dal"]
		lEnd = ["ar", "sta", "na", "is", "el", "es", "ie", "us", "un", "th", "er", "on", "an", "re", "in", "ed", "nd", "at", "en", "le", "man", "ck", "ton", "nok", "git", "us", "or", "a", "da", "u", "cha", "ir"]
	
		lEpithet = ["red", "blue", "black", "grey", "white", "strong", "brave", "old", "young", "great", "slayer", "hunter", "seeker"]
		lNoun = ["spirit", "soul", "boon", "born", "staff", "rod", "shield", "autumn", "winter", "spring", "summer", "wit", "horn", "tusk", "glory", "claw", "tooth", "head", "heart", "blood", "breath", "blade", "hand", "lover", "bringer", "maker", "taker", "river", "stream", "moon", "star", "face", "foot", "half", "one", "hundred", "thousand"]
		lSchema = ["CPME", "CPMESCPME", "CPESCPE", "CPE", "CPMME", "CPMDCME", "CPMAME", "KCPMESCUM", "CPMME[ the ]CX", "CPMESCXN", "CPMME[ of ]CPMME", "CNNSCXN"]

		if pAlign == gc.getInfoTypeForString( 'ALIGNMENT_EVIL' ):
			lNoun = lNoun + ["fear", "terror", "reign", "brood", "snare", "war", "strife", "pain", "hate", "evil", "hell", "misery", "murder", "anger", "fury", "rage", "spawn", "sly", "blood", "bone", "scythe", "slave", "bound", "ooze", "scum"]
			lEpithet = ["dark", "black", "white", "cruel", "foul"]		
	
		if pReligion == gc.getInfoTypeForString( 'RELIGION_THE_ASHEN_VEIL' ):
			lEpithet = lEpithet + ["fallen", "diseased", "infernal", "profane", "corrupt"]
			lSchema = lSchema + ["CPME[ the ]CX"]
		if pReligion == gc.getInfoTypeForString( 'RELIGION_OCTOPUS_OVERLORDS' ):
			lPre = lPre + ["cth", "cht", "shu", "az", "ts", "dag", "hy", "gla", "gh", "rh", "x", "ll"]
			lMid = lMid + ["ul", "tha", "on", "ug", "st", "oi"]
			lEnd = lEnd + ["hu", "on", "ha", "ua", "oa", "uth", "oth", "ath", "thua", "thoa", "ur", "ll", "og", "hua"]
			lEpithet = lEpithet + ["nameless", "webbed", "deep", "watery"]
			lNoun = lNoun + ["tentacle", "wind", "wave", "sea", "ocean", "dark", "crab", "abyss", "island"]
			lSchema = lSchema + ["CPMME", "CPDMME", "CPAMAME", "CPMAME", "CPAMAMEDCPAMAE"]
		if pReligion == gc.getInfoTypeForString( 'RELIGION_THE_ORDER' ):
			lPre = lPre + ["ph", "v", "j"]
			lMid = lMid + ["an", "al", "un"]
			lEnd = lEnd + ["uel", "in", "il"]
			lEpithet = lEpithet + ["confessor", "crusader", "faithful", "obedient", "good"]
			lNoun = lNoun + ["order", "faith", "heaven", "law"]
			lSchema = lSchema + ["CPESCPME", "CPMESCPE", "CPMESCPME", "CPESCPE"]
		if pReligion == gc.getInfoTypeForString( 'RELIGION_FELLOWSHIP_OF_LEAVES' ):
			lPre = lPre + ["ki", "ky", "yv"]
			lMid = lMid + ["th", "ri"]
			lEnd = lEnd + ["ra", "el", "ain"]
			lEpithet = lEpithet + ["green"]
			lNoun = lNoun + ["tree", "bush", "wood", "berry", "elm", "willow", "oak", "leaf", "flower", "blossom"]
			lSchema = lSchema + ["CPESCN", "CPMESCNN", "CPMESCXN"]
		if pReligion == gc.getInfoTypeForString( 'RELIGION_RUNES_OF_KILMORPH' ):
			lPre = lPre + ["bam", "ar", "khel", "ki"]
			lMid = lMid + ["th", "b", "en"]
			lEnd = lEnd + ["ur", "dain", "ain", "don"]
			lEpithet = lEpithet + ["deep", "guard", "miner"]
			lNoun = lNoun + ["rune", "flint", "slate", "stone", "rock", "iron", "copper", "mithril", "thane", "umber"]
			lSchema = lSchema + ["CPME", "CPMME"]
		if pReligion == gc.getInfoTypeForString( 'RELIGION_THE_EMPYREAN' ):
			lEpithet = lEpithet + ["radiant", "holy"]
			lNoun = lNoun + ["honor"]
		if pReligion == gc.getInfoTypeForString( 'RELIGION_COUNCIL_OF_ESUS' ):
			lEpithet = lEpithet + ["hidden", "dark"]
			lNoun = lNoun + ["cloak", "shadow", "mask"]
			lSchema = lSchema + ["CPME", "CPMME"]

		if unit.isHasPromotion( gc.getInfoTypeForString( 'PROMOTION_ENRAGED' ) ) == True:
			# I have left this as a copy of the Barbarian, see how it goes, this might do the trick. I plan to use it when there is a chance a unit will go Barbarian anyway.
			lPre = lPre + ["gru", "bra", "no", "os", "dir", "ka", "z"]
			lMid = lMid + ["g", "ck", "gg", "sh", "b", "bh", "aa"]
			lEnd = lEnd + ["al", "e", "ek", "esh", "ol", "olg", "alg"]
			lNoun = lNoun + ["death", "hate", "rage", "mad", "insane", "berserk"]
			lEpithet = lEpithet + ["smasher", "breaker", "mangle", "monger"]

		if unit.isHasPromotion( gc.getInfoTypeForString( 'PROMOTION_CRAZED' ) ) == True:
			# might want to tone this down, because I plan to use it as possession/driven to madness, less than madcap zaniness.
			lPre = lPre + ["mad", "pim", "zi", "zo", "fli", "mum", "dum", "odd", "slur"]
			lMid = lMid + ["bl", "pl", "gg", "ug", "bl", "b", "zz", "abb", "odd"]
			lEnd = lEnd + ["ad", "ap", "izzle", "onk", "ing", "er", "po", "eep", "oggle", "y"]

		if unit.isHasPromotion( gc.getInfoTypeForString( 'PROMOTION_VAMPIRE' ) ) == True:
			lPre = lPre + ["dra", "al", "nos", "vam", "vla", "tep", "bat", "bar", "cor", "lil", "ray", "zar", "stra", "le"]
			lMid = lMid + ["cul", "u", "car", "fer", "pir", "or", "na", "ov", "sta"]
			lEnd = lEnd + ["a", "d", "u", "e", "es", "y", "bas", "vin", "ith", "ne", "ak", "ich", "hd", "t"]

		if unit.isHasPromotion( gc.getInfoTypeForString( 'PROMOTION_DEMON' ) ) == True:
			lPre = lPre + ["aa", "ab", "adr", "ah", "al", "de", "ba", "cro", "da", "be", "eu", "el", "ha", "ib", "me", "she", "sth", "z"]
			lMid = lMid + ["rax", "lia", "ri", "al", "as", "b", "bh", "aa", "al", "ze", "phi", "sto", "phe", "cc", "ee"]
			lEnd = lEnd + ["tor", "tan", "ept", "lu", "res", "ah", "mon", "gon", "bul", "gul", "lis", "les", "uz"]
			lSchema = ["CPMMME", "CPMACME", "CPKMAUAPUE", "CPMMME[ the ]CNX"]

		if unit.getUnitType() == gc.getInfoTypeForString( 'UNIT_HILL_GIANT' ):
			lPre = lPre + ["gor", "gra", "gar", "gi", "gol"]
			lMid = lMid + ["gan", "li", "ri", "go"]
			lEnd = lEnd + ["tus", "tan", "ath", "tha"]
			lSchema = lSchema + ["CXNSCNN", "CPESCNE", "CPMME[ the ]CX"]
			lEpithet = lEpithet + ["large", "huge", "collossal", "brutal", "basher", "smasher", "crasher", "crusher"]
			lNoun = lNoun + ["fist", "tor", "hill", "brute", "stomp"]

		if unit.getUnitType() == gc.getInfoTypeForString( 'UNIT_LIZARDMAN' ):
			lPre = lPre + ["ss", "s", "th", "sth", "hss"]
			lEnd = lEnd + ["ess", "iss", "ath", "tha"]
			lEpithet = lEpithet + ["cold"]
			lNoun = lNoun + ["hiss", "tongue", "slither", "scale", "tail", "ruin"]
			lSchema = lSchema + ["CPAECPAE", "CPAKECPAU", "CPAMMAE"]
		if unit.getUnitType() == gc.getInfoTypeForString( 'UNIT_FIRE_ELEMENTAL' ) or unit.getUnitType() == gc.getInfoTypeForString( 'UNIT_AZER' ):
			lPre = lPre + ["ss", "cra", "th", "sth", "hss", "roa"]
			lMid = lMid + ["ss", "ck", "rr", "oa", "iss", "tt"]
			lEnd = lEnd + ["le", "iss", "st", "r", "er"]
			lNoun = lNoun + ["hot", "burn", "scald", "roast", "flame", "scorch", "char", "sear", "singe", "fire", "spit"]
			lSchema = ["CNN", "CNX", "CPME", "CPME[ the ]CNX", "CPMME", "CNNSCPME"]
		if unit.getUnitType() == gc.getInfoTypeForString( 'UNIT_WATER_ELEMENTAL' ):
			lPre = lPre + ["who", "spl", "dr", "sl", "spr", "sw", "b"]
			lMid = lMid + ["o", "a", "i", "ub", "ib"]
			lEnd = lEnd + ["sh", "p", "ter", "ble"]
			lNoun = lNoun + ["wave", "lap", "sea", "lake", "water", "tide", "surf", "spray", "wet", "damp", "soak", "gurgle", "bubble"]
			lSchema = ["CNN", "CNX", "CPME", "CPME[ the ]CNX", "CPMME", "CNNSCPME"]
		if unit.getUnitType() == gc.getInfoTypeForString( 'UNIT_AIR_ELEMENTAL' ):
			lPre = lPre + ["ff", "ph", "th", "ff", "ph", "th"]
			lMid = lMid + ["oo", "aa", "ee", "ah", "oh"]
			lEnd = lEnd + ["ff", "ph", "th", "ff", "ph", "th"]
			lNoun = lNoun + ["wind", "air", "zephyr", "breeze", "gust", "blast", "blow"]
			lSchema = ["CNN", "CNX", "CPME", "CPME[ the ]CNX", "CPMME", "CNNSCPME"]
		if unit.getUnitType() == gc.getInfoTypeForString( 'UNIT_EARTH_ELEMENTAL' ):
			lPre = lPre + ["gra", "gro", "kro", "ff", "ph", "th"]
			lMid = lMid + ["o", "a", "u"]
			lEnd = lEnd + ["ck", "g", "k"]
			lNoun = lNoun + ["rock", "stone", "boulder", "slate", "granite", "rumble", "quake"]
			lSchema = ["CNN", "CNX", "CPME", "CPME[ the ]CNX", "CPMME", "CNNSCPME"]

		# SEA BASED
		# Check for ships - special schemas
		if unit.getUnitCombatType() == gc.getInfoTypeForString( 'UNITCOMBAT_NAVAL' ):
			lEnd = lEnd + ["ton", "town", "port"]
			lNoun = lNoun + ["lady", "jolly", "keel", "bow", "stern", "mast", "sail", "deck", "hull", "reef", "wave"]
			lEpithet = lEpithet + ["sea", "red", "blue", "grand", "barnacle", "gull"]
			lSchema = ["[The ]CNN", "[The ]CXN", "[The ]CNX", "[The ]CNSCN", "[The ]CNSCX", "CPME['s ]CN", "[The ]CPME", "[The ]CNX", "CNX", "CN['s ]CN"]

		# # #
		# Pick a Schema
		sSchema = lSchema[CyGame().getSorenRandNum( len( lSchema ), "Name Gen" ) - 1]
		sFull = ""
		sKeep = ""
		iUpper = 0
		iKeep = 0
		iSkip = 0

		# Run through each character in schema to generate name
		for iCount in range ( 0, len( sSchema ) ):
			sAdd = ""
			iDone = 0
			sAction = sSchema[iCount]
			if iSkip == 1:
				if sAction == "]":
					iSkip = 0
				else:
					sAdd = sAction
					iDone = 1
			else:					# MAIN SECTION
				if sAction == "P": 	# Pre 	: beginnings of names
					sAdd = lPre[CyGame().getSorenRandNum( len( lPre ), "Name Gen" ) - 1]
					iDone = 1
				if sAction == "M":	# Mid 	: middle syllables
					sAdd = lMid[CyGame().getSorenRandNum( len( lMid ), "Name Gen" ) - 1]
					iDone = 1
				if sAction == "E":	# End	: end of names
					sAdd = lEnd[CyGame().getSorenRandNum( len( lEnd ), "Name Gen" ) - 1]
					iDone = 1
				if sAction == "X":	# Epithet	: epithet word part
					#epithets ("e" was taken!)
					sAdd = lEpithet[CyGame().getSorenRandNum( len( lEpithet ), "Name Gen" ) - 1]
					iDone = 1
				if sAction == "N":	# Noun	: noun word part
					#noun
					sAdd = lNoun[CyGame().getSorenRandNum( len( lNoun ), "Name Gen" ) - 1]
					iDone = 1
				if sAction == "S":	# Space	: a space character. (Introduced before [ ] was possible )
					sAdd = " "
					iDone = 1
				if sAction == "D":	# Dash	: a - character. Thought to be common and useful enough to warrant inclusion : Introduced before [-] was possible
					sAdd = "-"
					iDone = 1
				if sAction == "A":	# '		: a ' character - as for -, introduced early
					sAdd = "'"
					iDone = 1
				if sAction == "C":	# Caps	: capitalizes first letter of next phrase generated. No effect on non-letters.
					iUpper = 1
				if sAction == "K":	# Keep	: stores the next phrase generated for re-use with U
					iKeep = 1
				if sAction == "U":	# Use	: re-uses a stored phrase.
					sAdd = sKeep
					iDone = 1
				if sAction == "[":	# Print	: anything between [] is added to the final phrase "as is". Useful for [ the ] and [ of ] among others.
					iSkip = 1
			# capitalizes phrase once.
			if iUpper == 1 and iDone == 1:
				sAdd = sAdd.capitalize()
				iUpper = 0
			# stores the next phrase generated.
			if iKeep == 1 and iDone == 1:
				sKeep = sAdd
				iKeep = 0
			# only adds the phrase if a new bit was actally created.
			if iDone == 1:
				sFull = sFull + sAdd

		# trim name length
		if len( sFull ) > 25:
			sFull = sFull[:25]
		#CyInterface().addMessage(caster.getOwner(),True,25,"NAME : "+sFull,'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Rob Grave.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

		return sFull

