# DynamicCivNames
#
# by jdog5000
# Version 1.0
#


from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup as PyPopup
# --------- Revolution mod -------------
import RevDefs
import SdToolKitCustom as SDTK
import RevUtils
import LeaderCivNames
import BugCore

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
game = CyGame()
localText = CyTranslator()
RevOpt = BugCore.game.Revolution

class DynamicCivNames :

	def __init__(self, customEM, RevOpt ) :

		self.RevOpt = RevOpt
		self.customEM = customEM
		
		print "Initializing DynamicCivNames Mod"

		self.LOG_DEBUG = RevOpt.isDynamicNamesDebugMode()
		
		self.bTeamNaming = RevOpt.isTeamNaming()
		self.bLeaveHumanName = RevOpt.isLeaveHumanPlayerName()

		self.customEM.addEventHandler( "BeginPlayerTurn", self.onBeginPlayerTurn )
		self.customEM.addEventHandler( "setPlayerAlive", self.onSetPlayerAlive )
		self.customEM.addEventHandler( "kbdEvent", self.onKbdEvent )
		self.customEM.addEventHandler( "cityAcquired", self.onCityAcquired )
		self.customEM.addEventHandler( 'cityBuilt', self.onCityBuilt )
		self.customEM.addEventHandler( "vassalState", self.onVassalState )
		
		LeaderCivNames.setup()
		
		if( not game.isFinalInitialized or game.getGameTurn() == game.getStartTurn() ) :
			for idx in range(0,gc.getMAX_CIV_PLAYERS()) :
				self.onSetPlayerAlive( [idx, gc.getPlayer(idx).isAlive()] )

	def removeEventHandlers( self ) :
		print "Removing event handlers from DynamicCivNames"
		
		self.customEM.removeEventHandler( "BeginPlayerTurn", self.onBeginPlayerTurn )
		self.customEM.removeEventHandler( "setPlayerAlive", self.onSetPlayerAlive )
		self.customEM.removeEventHandler( "kbdEvent", self.onKbdEvent )
		self.customEM.removeEventHandler( "cityAcquired", self.onCityAcquired )
		self.customEM.removeEventHandler( 'cityBuilt', self.onCityBuilt )
		self.customEM.removeEventHandler( "vassalState", self.onVassalState )
	
	def blankHandler( self, playerID, netUserData, popupReturn ) :
		# Dummy handler to take the second event for popup
		return

	def onKbdEvent(self, argsList ):
		'keypress handler'
		eventType,key,mx,my,px,py = argsList

		if ( eventType == RevDefs.EventKeyDown ):
			theKey = int(key)

			# For debug or trial only
			if( theKey == int(InputTypes.KB_U) and self.customEM.bShift and self.customEM.bCtrl ) :
				pass


	def onBeginPlayerTurn( self, argsList ) :
		iGameTurn, iPlayer = argsList

		# Stuff at end of previous players turn
		iPrevPlayer = iPlayer - 1
		while( iPrevPlayer >= 0 and not gc.getPlayer(iPrevPlayer).isAlive() ) :
				iPrevPlayer -= 1

		if( iPrevPlayer < 0 ) :
			iPrevPlayer = gc.getBARBARIAN_PLAYER()

		if( iPrevPlayer >= 0 and iPrevPlayer < gc.getBARBARIAN_PLAYER() ) :
			iPlayer = iPrevPlayer
			pPlayer = gc.getPlayer( iPlayer )

			if( pPlayer.isAlive() and SDTK.sdObjectExists( "Revolution", pPlayer ) ) :
				#CvUtil.pyPrint("  Name - Object exists %d"%(iPlayer))
				prevCivics = SDTK.sdObjectGetVal( "Revolution", pPlayer, 'CivicList' )
				if( not prevCivics == None ) :
					for i in range(0,gc.getNumCivicOptionInfos()):
						if( not prevCivics[i] == pPlayer.getCivics(i) ) :
							self.setNewNameByCivics(iPlayer)
							return
							
				revTurn = SDTK.sdObjectGetVal( "Revolution", pPlayer, 'RevolutionTurn' )
				if( not revTurn == None and game.getGameTurn() - revTurn == 30 and pPlayer.getNumCities() > 0 ) :
					# "Graduate" from rebel name
					self.setNewNameByCivics(iPlayer)
					return
					
			if( pPlayer.isAlive() and SDTK.sdObjectExists( "BarbarianCiv", pPlayer ) ) :
				barbTurn = SDTK.sdObjectGetVal( "BarbarianCiv", pPlayer, 'SpawnTurn' )
				if( not barbTurn == None and game.getGameTurn() - barbTurn == 30 ) :
					# "Graduate" from barb civ name
					self.setNewNameByCivics(iPlayer)
					return
			
			if( pPlayer.isAlive() and not SDTK.sdObjectExists( "BarbarianCiv", pPlayer )) :
				if( 'Tribe' in pPlayer.getCivilizationDescription(0) ) :
					if( pPlayer.getCurrentEra() > 0 or pPlayer.getTotalPopulation() >= 3 ) :
						# Graduate from game start name
						CvUtil.pyPrint("  Name - Graduating from game start name Player %d"%(iPlayer))
						self.setNewNameByCivics(iPlayer)
						return

	def onCityAcquired( self, argsList):
		'City Acquired'

		owner,playerType,city,bConquest,bTrade = argsList

		owner = gc.getPlayer( city.getOwner() )
		
		if( owner.isAlive() and not owner.isBarbarian() and owner.getNumCities() < 5 and owner.getNumMilitaryUnits() > 0 ) :
			if( owner.getCapitalCity().getGameTurnAcquired() + 5 < game.getGameTurn() ) :
				CvUtil.pyPrint("  Name - Checking for new name by number of cities")
				self.setNewNameByCivics( owner.getID() )
	
	def onCityBuilt( self, argsList ) :
		
		city = argsList[0]

		owner = gc.getPlayer( city.getOwner() )
		
		if( owner.isAlive() and not owner.isBarbarian() and owner.getNumCities() < 5 and owner.getNumMilitaryUnits() > 0 ) :
			if( owner.getCapitalCity().getGameTurnAcquired() + 5 < game.getGameTurn() ) :
				CvUtil.pyPrint("  Name - Checking for new name by number of cities")
				self.setNewNameByCivics( owner.getID() )
	
	def onVassalState(self, argsList):
		iMaster, iVassal, bVassal = argsList

		if (bVassal):
			#CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d"%(iVassal, iMaster))
			for iPlayer in range(0,gc.getMAX_CIV_PLAYERS()) :
				if( gc.getPlayer(iPlayer).getTeam() == iVassal ) :
					self.setNewNameByCivics( iPlayer )
		else:
			#CvUtil.pyPrint("Team %d revolts and is no longer a Vassal State of Team %d"%(iVassal, iMaster))
			for iPlayer in range(0,gc.getMAX_CIV_PLAYERS()) :
				if( gc.getPlayer(iPlayer).getTeam() == iVassal ) :
					self.setNewNameByCivics( iPlayer )
	
	def setNewNameByCivics( self, iPlayer ) :
		[newCivDesc, newCivShort, newCivAdj] = self.newNameByCivics( iPlayer )

		if( gc.getPlayer(iPlayer).isHuman() or game.getActivePlayer() == iPlayer ) :
			if( self.bLeaveHumanName ) :
				CvUtil.pyPrint("  Name - Leaving name for human player")
				return
			else :
				#CvUtil.pyPrint("  Name - Changing name for human player!")
				pass

		newDesc  = CvUtil.convertToStr(newCivDesc)
		newShort = CvUtil.convertToStr(newCivShort)
		newAdj   = CvUtil.convertToStr(newCivAdj)
		
		if( not newDesc == gc.getPlayer(iPlayer).getCivilizationDescription(0) ) :
			CyInterface().addMessage(iPlayer, false, gc.getDefineINT("EVENT_MESSAGE_TIME"), "Your civilization is now known as the %s"%(newDesc), None, InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), -1, -1, False, False)
			if( self.LOG_DEBUG ) :
				CvUtil.pyPrint("  Name - Setting civ name due to civics to %s"%(newCivDesc))
		
		gc.getPlayer(iPlayer).setCivName( newDesc, newShort, newAdj )
		
		return
	
	def onSetPlayerAlive( self, argsList ) :

		iPlayerID = argsList[0]
		bNewValue = argsList[1]
		if( bNewValue == True and iPlayerID < gc.getMAX_CIV_PLAYERS() ) :
			pPlayer = gc.getPlayer( iPlayerID )

			if( pPlayer.isHuman() or game.getActivePlayer() == iPlayerID ) :
				if( self.bLeaveHumanName ) :
					CvUtil.pyPrint("  Name - Leaving name for human player")
					return
			 
			[newCivDesc, newCivShort, newCivAdj] = self.nameForNewPlayer( iPlayerID )
			
			if( self.LOG_DEBUG ) :
				CvUtil.pyPrint("  Name - Setting civ name for new civ to %s"%(newCivDesc))

			newDesc  = CvUtil.convertToStr(newCivDesc)
			newShort = CvUtil.convertToStr(newCivShort)
			newAdj   = CvUtil.convertToStr(newCivAdj)

			# Pass to pPlayer seems to require a conversion to 'ascii'
			pPlayer.setCivName( newDesc, newShort, newAdj )


	def showNewNames( self ) :

		bodStr = 'New names for all civs:\n\n'

		for i in range(0,gc.getMAX_CIV_PLAYERS()) :
			iPlayer = i

			[newName,newShort,newAdj] = self.newNameByCivics(iPlayer)

			bodStr += curDesc + '\t-> ' + newName + '\n'

		popup = PyPopup.PyPopup()
		popup.setBodyString( bodStr )
		popup.launch()


	def nameForNewPlayer( self, iPlayer ) :
		# Assigns a new name to a recently created player from either
		# BarbarianCiv or Revolution components

		pPlayer = gc.getPlayer(iPlayer)
		currentEra = 0
		for i in range(0,gc.getMAX_CIV_PLAYERS()) :
			if( gc.getPlayer(i).getCurrentEra() > currentEra ) :
				currentEra = gc.getPlayer(i).getCurrentEra()

		curDesc = pPlayer.getCivilizationDescription(0)
		curShort = pPlayer.getCivilizationShortDescription(0)
		curAdj = pPlayer.getCivilizationAdjective(0)

		civInfo = gc.getCivilizationInfo(pPlayer.getCivilizationType())
		origDesc  = civInfo.getDescription()
		
		if( not game.isOption(GameOptionTypes.GAMEOPTION_LEAD_ANY_CIV) ) :
			if( pPlayer.getLeaderType() in LeaderCivNames.LeaderCivNames.keys() ) :
				[curDesc,curShort,curAdj] = LeaderCivNames.LeaderCivNames[pPlayer.getLeaderType()]

		newName = curDesc
		if( SDTK.sdObjectExists( "Revolution", pPlayer ) ) :
			revTurn = SDTK.sdObjectGetVal( "Revolution", pPlayer, 'RevolutionTurn' )
		else :
			revTurn = None

		if( SDTK.sdObjectExists( "BarbarianCiv", pPlayer ) ) :
			barbTurn = SDTK.sdObjectGetVal( "BarbarianCiv", pPlayer, 'SpawnTurn' )
		else :
			barbTurn = None

		if( not pPlayer.isAlive() ) :
			newName = localText.getText("TXT_KEY_MOD_DCN_REFUGEES", ())%(curAdj)
		elif( pPlayer.isRebel() ) :
			# To name rebels in Revolution mod
			cityString = SDTK.sdObjectGetVal( "Revolution", pPlayer, 'CapitalName' )
			if( self.LOG_DEBUG ) : CvUtil.pyPrint("Names - player is rebel")
			
			sLiberation = localText.getText("TXT_KEY_MOD_DCN_LIBERATION_FRONT", ()).replace('%s','').strip()
			sGuerillas = localText.getText("TXT_KEY_MOD_DCN_GUERILLAS", ()).replace('%s','').strip()
			sRebels = localText.getText("TXT_KEY_MOD_DCN_REBELS", ()).replace('%s','').strip()
			
			if( sLiberation in curDesc or sGuerillas in curDesc or sRebels in curDesc ) :
				newName = curDesc
			else :
				if( currentEra > 5 and 30 > game.getSorenRandNum(100,'Rev: Naming')) :
					newName = localText.getText("TXT_KEY_MOD_DCN_LIBERATION_FRONT", ())%(curAdj)
				elif( currentEra > 4 and 30 > game.getSorenRandNum(100,'Rev: Naming') ) :
					newName = localText.getText("TXT_KEY_MOD_DCN_GUERILLAS", ())%(curAdj)
				else :
					if( not cityString == None and len(cityString) < 10 ) :
						try :
							if( cityString in curAdj or cityString in curShort ) :
								newName = localText.getText("TXT_KEY_MOD_DCN_THE_REBELS_OF", ())%(CvUtil.convertToStr(cityString))
							else :
								newName = localText.getText("TXT_KEY_MOD_DCN_REBELS_OF", ())%(curAdj,CvUtil.convertToStr(cityString))
						except :
							newName = localText.getText("TXT_KEY_MOD_DCN_REBELS", ())%(curAdj)
					else :
						newName = localText.getText("TXT_KEY_MOD_DCN_REBELS", ())%(curAdj)
		elif( not barbTurn == None and game.getGameTurn() - barbTurn < 20 ) :
			# To name BarbarianCiv created civs
			numCities = SDTK.sdObjectGetVal( "BarbarianCiv", pPlayer, 'NumCities' )
			cityString = SDTK.sdObjectGetVal( "BarbarianCiv", pPlayer, 'CapitalName' )
			if( self.LOG_DEBUG ) : CvUtil.pyPrint("Names - player is barbciv")
			
			if( pPlayer.isMinorCiv() ) :
				if( currentEra < 2 ) :
					if( 70 - 40*currentEra > game.getSorenRandNum(100,"Naming") ) : 
						newName = localText.getText("TXT_KEY_MOD_DCN_TRIBE", ())%(curAdj)
					else :
						newName = localText.getText("TXT_KEY_MOD_DCN_CITY_STATE", ())%(curAdj)
				elif( currentEra < 3 ) :
					newName = localText.getText("TXT_KEY_MOD_DCN_CITY_STATE", ())%(curAdj)
				else :
					newName = localText.getText("TXT_KEY_MOD_DCN_NATION", ())%(curAdj)
			elif( currentEra < 4 ) :
				# Early era barbs
				if( SDTK.sdObjectGetVal( 'BarbarianCiv', pPlayer, 'BarbStyle' ) == 'Military' ) :
					if( pPlayer.getNumMilitaryUnits() > 7*numCities ) :
						newName = localText.getText("TXT_KEY_MOD_DCN_HORDE", ())%(curAdj)
					else :
						if( not cityString == None and len(cityString) < 10 ) :
							if( cityString in curAdj or cityString in curShort ) :
								newName = localText.getText("TXT_KEY_MOD_DCN_THE_WARRIORS_OF", ())%(cityString)
							else :
								newName = localText.getText("TXT_KEY_MOD_DCN_WARRIORS_OF", ())%(curAdj,cityString)
						else :
							newName = localText.getText("TXT_KEY_MOD_DCN_WARRIOR_STATE", ())%(curAdj)
				else :
					if( numCities == 1 ) :
						newName = localText.getText("TXT_KEY_MOD_DCN_CITY_STATE", ())%(curAdj)
					else :
						newName = localText.getText("TXT_KEY_MOD_DCN_EMPIRE", ())%(curAdj)
					
					if( numCities < 3 ) :
						if( not cityString == None and len(cityString) < 10) :
							newName += localText.getText("TXT_KEY_MOD_DCN_OF", ()) + cityString

			else :
				
				newName = localText.getText("TXT_KEY_MOD_DCN_EMPIRE", ())%(curAdj)
				if( numCities < 3 and not cityString == None and len(cityString) < 10) :
					newName += localText.getText("TXT_KEY_MOD_DCN_OF", ()) + cityString

		else :
			if( game.getGameTurn() == game.getStartTurn() and game.getCurrentEra() < 1 ) :
				# Name civs at beginning of game
				if( self.LOG_DEBUG ) : CvUtil.pyPrint("Names - Giving game start name")
				newName = localText.getText("TXT_KEY_MOD_DCN_TRIBE", ())%(curAdj)
				return [newName, curShort, curAdj]
			
			if( self.LOG_DEBUG ) : CvUtil.pyPrint("Names - player not of special type, naming by civics")
			return self.newNameByCivics( iPlayer )

		return [newName, curShort, curAdj]


	def newNameByCivics( self, iPlayer, bVerbose = True, bForceUpdate = False ) :
		# Assigns a new name to a player based on their civics choices

		pPlayer = gc.getPlayer(iPlayer)
		capital = pPlayer.getCapitalCity()
		playerEra = pPlayer.getCurrentEra()
		pTeam = gc.getTeam(pPlayer.getTeam())
		
		cityString = None
		if( not capital == None and not capital.isNone() ) :
			try :
				# Silly game to force ascii encoding now
				cityString =  pPlayer.getCivilizationDescription(0)
				cityString += "&" + CvUtil.convertToStr(capital.getName())
				cityString =  cityString.split('&',1)[-1]
			except :
				pass

		curDesc  = pPlayer.getCivilizationDescription(0)
		curShort = pPlayer.getCivilizationShortDescription(0)
		curAdj   = pPlayer.getCivilizationAdjective(0)

		civInfo = gc.getCivilizationInfo(pPlayer.getCivilizationType())
		origDesc  = civInfo.getDescription()
		
		if( not game.isOption(GameOptionTypes.GAMEOPTION_LEAD_ANY_CIV) ) :
			if( pPlayer.getLeaderType() in LeaderCivNames.LeaderCivNames.keys() ) :
				[curDesc,curShort,curAdj] = LeaderCivNames.LeaderCivNames[pPlayer.getLeaderType()]

		newName = curDesc
		if( SDTK.sdObjectExists( "Revolution", pPlayer ) ) :
			revTurn = SDTK.sdObjectGetVal( "Revolution", pPlayer, 'RevolutionTurn' )
		else :
			revTurn = None

		if( SDTK.sdObjectExists( "BarbarianCiv", pPlayer ) ) :
			barbTurn = SDTK.sdObjectGetVal( "BarbarianCiv", pPlayer, 'SpawnTurn' )
		else :
			barbTurn = None

		if( not pPlayer.isAlive() ) :
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is not alive")
			newName = localText.getText("TXT_KEY_MOD_DCN_REFUGEES", ())%(curAdj)
			return [newName, curShort, curAdj]
		
		if( pPlayer.isRebel() ) :
			# Maintain name of rebels from Revolution Mod
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is rebel, keeping current name")
			if( bForceUpdate ) :
				return self.nameForNewPlayer(iPlayer)
			else :
				return [curDesc, curShort, curAdj]
		elif( pPlayer.isMinorCiv() and not barbTurn == None ) :
			# Maintain minor civ name
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is Minor Barb Civ, keeping current name")
			if( bForceUpdate ) :
				return self.nameForNewPlayer(iPlayer)
			else :
				return [curDesc, curShort, curAdj]
		elif( not barbTurn == None and game.getGameTurn() - barbTurn < 20 and pPlayer.getNumCities() < 4 ) :
			# Maintain name of BarbarianCiv created player
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is BarbCiv, keeping current name")
			if( bForceUpdate ) :
				return self.nameForNewPlayer(iPlayer)
			else :
				return [curDesc, curShort, curAdj]

		
		# Special options for teams and permanent alliances
		if( self.bTeamNaming and pTeam.getNumMembers() > 1 ) : # and pTeam.getPermanentAllianceTradingCount() > 0 ) :
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - Multiple players on team")
			if( self.LOG_DEBUG and bVerbose and pTeam.getPermanentAllianceTradingCount() > 0 ) : CvUtil.pyPrint("Names - Player in Permanent Alliance")
			if( pTeam.getNumMembers() == 2 ) :
				iLeader = pTeam.getLeaderID()
				newName = gc.getPlayer(iLeader).getCivilizationAdjective(0) + "-"
				for idx in range(0,gc.getMAX_CIV_PLAYERS()):
					if( not idx == iLeader and gc.getPlayer(idx).getTeam() == pTeam.getID() ) :
						newName += gc.getPlayer(idx).getCivilizationAdjective(0)
						break
				newName += localText.getText("TXT_KEY_MOD_DCN_ALLIANCE", ())
				return [newName,curShort,curAdj]
			else :
				iLeader = pTeam.getLeaderID()
				newName = gc.getPlayer(iLeader).getCivilizationAdjective(0)[0:4]
				for idx in range(0,gc.getMAX_CIV_PLAYERS()):
					if( not idx == iLeader and gc.getPlayer(idx).getTeam() == pTeam.getID() ) :
						newName += gc.getPlayer(idx).getCivilizationAdjective(0)[0:3]
				newName += localText.getText("TXT_KEY_MOD_DCN_ALLIANCE", ())
				return [newName,curShort,curAdj]
		
		sSocRep = localText.getText("TXT_KEY_MOD_DCN_SOC_REP", ()).replace('%s','').strip()
		sPeoplesRep = localText.getText("TXT_KEY_MOD_DCN_PEOPLES_REP", ()).replace('%s','').strip()
		
		# Main naming conditions
		if( RevUtils.isCommunism(iPlayer) ) :
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is communist")
			if( RevUtils.isCanDoElections(iPlayer) ) :
				if( not bForceUpdate and (sSocRep in curDesc or sPeoplesRep in curDesc) ) :
					if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - keeping prior name")
					newName = curDesc
				elif( 50 > game.getSorenRandNum(100,'Rev: Naming') ) :
					newName = localText.getText("TXT_KEY_MOD_DCN_SOC_REP", ())%(curShort)
				else :
					newName = localText.getText("TXT_KEY_MOD_DCN_PEOPLES_REP", ())%(curShort)
			elif( RevUtils.getDemocracyLevel(iPlayer)[0] == -8 ) :
				if( localText.getText("TXT_KEY_MOD_DCN_RUSSIAN_MATCH", ()) in curAdj ) :
					curAdj = localText.getText("TXT_KEY_MOD_DCN_SOVIET", ())
				newName = localText.getText("TXT_KEY_MOD_DCN_UNION", ())%(curAdj)
			else :
				newName = localText.getText("TXT_KEY_MOD_DCN_PEOPLES_REP", ())%(curShort)
		elif( RevUtils.isCanDoElections(iPlayer) ) :
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player can do elections")
			sRepOf = localText.getText("TXT_KEY_MOD_DCN_REPUBLIC_OF", ()).replace('%s','').strip()
			sRepublic = localText.getText("TXT_KEY_MOD_DCN_REPUBLIC", ())
			
			if( pPlayer.getNumCities() == 1 ) :
				if( not bForceUpdate and (curDesc.startswith(localText.getText("TXT_KEY_MOD_DCN_FREE", ())) or ((sRepOf in curDesc or sRepublic in curDesc) and cityString in curDesc)) ) :
					if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - keeping prior name")
					newName = curDesc
				elif( 40 > game.getSorenRandNum(100,'Rev: Naming') ) :
					newName = localText.getText("TXT_KEY_MOD_DCN_FREE_STATE", ())%(curAdj)
				else :
					if( not cityString == None and len(cityString) < 10 and len(cityString) > 0) :
						if( cityString in curAdj or cityString in curShort ) :
							newName = localText.getText("TXT_KEY_MOD_DCN_THE_REPUBLIC_OF", ())%(cityString)
						else :
							newName = localText.getText("TXT_KEY_MOD_DCN_REPUBLIC_OF", ())%(curAdj,cityString)
					else :
						newName = localText.getText("TXT_KEY_MOD_DCN_FREE_REPUBLIC", ())%(curAdj)
			else :
				if( not bForceUpdate and (sRepublic in curDesc and not sPeoplesRep in curDesc and not sSocRep in curDesc and curDesc.startswith(localText.getText("TXT_KEY_MOD_DCN_FREE", ()))) ) :
					if( len(curDesc) < 17 and 20 > game.getSorenRandNum(100,'Rev: Naming') and not localText.getText("TXT_KEY_MOD_DCN_NEW", ()) in curDesc ) :
						newName = localText.getText("TXT_KEY_MOD_DCN_NEW", ()) + curDesc
					else :
						if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - keeping prior name")
						newName = curDesc
				elif( 50 > game.getSorenRandNum(100,'Rev: Naming') ) :
					newName = localText.getText("TXT_KEY_MOD_DCN_REPUBLIC", ())%(curAdj)
				else :
					newName = localText.getText("TXT_KEY_MOD_DCN_THE_REPUBLIC_OF", ())%(curShort)

			if( RevUtils.isFreeSpeech(iPlayer) and RevUtils.getLaborFreedom(iPlayer)[0] > 9 ) :
				if( len(newName) < 16 and not localText.getText("TXT_KEY_MOD_DCN_FREE", ()) in newName and not localText.getText("TXT_KEY_MOD_DCN_NEW", ()) in newName ) :
					newName = localText.getText("TXT_KEY_MOD_DCN_FREE", ()) + ' ' + newName
		elif( RevUtils.getDemocracyLevel(iPlayer)[0] == -8 ) :
			if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is police state")
			empString = localText.getText("TXT_KEY_MOD_DCN_PLAIN_EMPIRE", ())
			if( localText.getText("TXT_KEY_MOD_DCN_GERMAN_MATCH", ()) in curAdj ) :
				empString = localText.getText("TXT_KEY_MOD_DCN_REICH", ())
			
			if( not bForceUpdate and empString in curDesc ) :
				if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - keeping prior name")
				newName = curDesc
			elif( 70 > game.getSorenRandNum(100,'Rev: Naming') and not localText.getText("TXT_KEY_MOD_DCN_REICH", ()) in empString ) :
				newName = localText.getText("TXT_KEY_MOD_DCN_THE_BLANK_OF", ())%(empString,curShort)
			else :
				newName = curAdj + ' ' + empString
		else :
			sGreat = localText.getText("TXT_KEY_MOD_DCN_GREAT_KINGDOM", ()).replace('%s','').strip()
			sKingdom = localText.getText("TXT_KEY_MOD_DCN_KINGDOM", ())
			if( RevUtils.getDemocracyLevel(iPlayer)[0] == -6 ) :

				if( pTeam.isAVassal() ) :
					if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is a vassal")
					sKingdom = localText.getText("TXT_KEY_MOD_DCN_DUCHY", ())
				else :
					if( localText.getText("TXT_KEY_MOD_DCN_PERSIAN_MATCH", ()) in curAdj or localText.getText("TXT_KEY_MOD_DCN_OTTOMAN_MATCH", ()) in curAdj or localText.getText("TXT_KEY_MOD_DCN_SUMERIAN_MATCH", ()) in curAdj ) :
						sKingdom = localText.getText("TXT_KEY_MOD_DCN_SULTANATE", ())
					elif( localText.getText("TXT_KEY_MOD_DCN_ARABIAN_MATCH", ()) in curAdj ) :
						sKingdom = localText.getText("TXT_KEY_MOD_DCN_CALIPHATE", ())
				
				if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is in monarchy")
				if( pPlayer.getNumCities() < 4 ) :
					if( not cityString == None and len(cityString) < 10 and len(cityString) > 0 ) :
						if( cityString in curAdj or cityString in curShort ) :
							newName = localText.getText("TXT_KEY_MOD_DCN_THE_BLANK_OF", ())%(sKingdom,cityString)
						else :
							newName = localText.getText("TXT_KEY_MOD_DCN_BLANK_OF", ())%(curAdj,sKingdom,cityString)
					else :
						newName = curAdj + ' ' + sKingdom
				elif( game.getPlayerRank(iPlayer) < game.countCivPlayersAlive()/7 and not pTeam.isAVassal() and (sGreat in curDesc or 40 > game.getSorenRandNum(100,'Rev: Naming')) ) :
					newName = localText.getText("TXT_KEY_MOD_DCN_GREAT_KINGDOM", ())%(curAdj,sKingdom)
				else :
					sOf = localText.getText("TXT_KEY_MOD_DCN_THE_BLANK_OF", ()).replace('%s','')
					if( not bForceUpdate and sKingdom in curDesc and (not sOf in curDesc or pPlayer.getNumCities < 6) and (not sGreat in curDesc) ) :
						if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - keeping prior name")
						newName = curDesc
					elif( 50 > game.getSorenRandNum(100,'Rev: Naming') ) :
						newName = curAdj + ' ' + sKingdom
					else :
						newName = localText.getText("TXT_KEY_MOD_DCN_THE_BLANK_OF", ())%(sKingdom,curShort)
			
			elif( RevUtils.getDemocracyLevel(iPlayer)[0] == -10 or playerEra == 0 ) :
				
				empString = localText.getText("TXT_KEY_MOD_DCN_PLAIN_EMPIRE", ())
				if( playerEra < 2 and pPlayer.getNumCities() < 3 ) :
					if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player has one city in early era")
					empString = localText.getText("TXT_KEY_MOD_DCN_PLAIN_CITY_STATE", ())
				if( pTeam.isAVassal() ) :
					if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is a vassal")
					empString = localText.getText("TXT_KEY_MOD_DCN_FIEFDOM", ())
				
				if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is in despotism")
				if( not bForceUpdate and empString in curDesc and not game.getGameTurn() == 0 ) :
					if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - keeping prior name")
					newName = curDesc
				elif( 50 > game.getSorenRandNum(100,'Rev: Naming') ) :
					newName = curAdj + ' ' + empString
				else :
					newName = localText.getText("TXT_KEY_MOD_DCN_THE_BLANK_OF", ())%(empString,curShort)
			
			else :
				if( self.LOG_DEBUG and bVerbose ) : 
					CvUtil.pyPrint("Names - Error: player fits no government category ... ")
					return [curDesc,curShort,curAdj]
					
			sHoly = localText.getText("TXT_KEY_MOD_DCN_HOLY", ()) + ' '
			if( RevUtils.getReligiousFreedom(iPlayer)[0] < -9 ) :
				if( self.LOG_DEBUG and bVerbose ) : CvUtil.pyPrint("Names - player is theocracy")
				if( len(newName) < 16 and not sHoly in newName and not sGreat in newName and not newName.startswith(localText.getText("TXT_KEY_MOD_DCN_HOLY_HRE_MATCH", ())) ) :
					newName = sHoly + newName
			elif( newName.startswith(sHoly) and not origDesc.startswith(sHoly) ) :
				# Cut off any inappropriately saved 'Holy ' prefix
				newName = newName[len(sHoly):]

		return [newName, curShort, curAdj]
	
	def resetName( self, iPlayer, bVerbose = True ) :
		
		pPlayer = gc.getPlayer(iPlayer)
		
		civInfo = gc.getCivilizationInfo(pPlayer.getCivilizationType())
		origDesc  = civInfo.getDescription()
		origShort = civInfo.getShortDescription(0)
		origAdj   = civInfo.getAdjective(0)

		if( not game.isOption(GameOptionTypes.GAMEOPTION_LEAD_ANY_CIV) ) :
			if( not self.bLeaveHumanName or not (pPlayer.isHuman() or game.getActivePlayer() == iPlayer) ) :
				if( pPlayer.getLeaderType() in LeaderCivNames.LeaderCivNames.keys() ) :
					[origDesc,origShort,origAdj] = LeaderCivNames.LeaderCivNames[pPlayer.getLeaderType()]

		newDesc  = CvUtil.convertToStr(origDesc)
		newShort = CvUtil.convertToStr(origShort)
		newAdj   = CvUtil.convertToStr(origAdj)
		
		if( self.LOG_DEBUG ) :
			CvUtil.pyPrint("  Name - Re-setting civ name for player %d to %s"%(iPlayer,newDesc))
		
		gc.getPlayer(iPlayer).setCivName( newDesc, newShort, newAdj )
