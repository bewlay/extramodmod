// player.cpp

#include "CvGameCoreDLL.h"
#include "CvGlobals.h"
#include "CvArea.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvRandom.h"
#include "CvTeamAI.h"
#include "CvGameCoreUtils.h"
#include "CvPlayerAI.h"
#include "CvPlayer.h"
#include "CvGameCoreUtils.h"
#include "CvArtFileMgr.h"
#include "CvDiploParameters.h"
#include "CvInitCore.h"
#include "CyArgsList.h"
#include "CvInfos.h"
#include "CvPopupInfo.h"
#include "CvDiploParameters.h"
#include "FProfiler.h"
#include "CvGameTextMgr.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CyUnit.h"
#include "CvEventReporter.h"
#include "CvMessageControl.h" // lfgr 02/2022

#include "CvDLLInterfaceIFaceBase.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLFAStarIFaceBase.h"
#include "CvDLLPythonIFaceBase.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      05/09/09                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
#include "CvDLLFlagEntityIFaceBase.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/02/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
#include "BetterBTSAI.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
// BUG - Ignore Harmless Barbarians - start
#include "CvBugOptions.h"
// BUG - Ignore Harmless Barbarians - end

// UNIVERSAL_PREREQS 08/2017 lfgr
#include "CvUniversalPrereqs.h"
// UNIVERSAL_PREREQS end


// Public Functions...

CvPlayer::CvPlayer()
{
	m_aiSeaPlotYield = new int[NUM_YIELD_TYPES];
	m_aiYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiCapitalYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiExtraYieldThreshold = new int[NUM_YIELD_TYPES];
	m_aiTradeYieldModifier = new int[NUM_YIELD_TYPES];
	m_aiFreeCityCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiCommercePercent = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceRate = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceRateModifier = new int[NUM_COMMERCE_TYPES];
	m_aiCapitalCommerceRateModifier = new int[NUM_COMMERCE_TYPES];
	m_aiStateReligionBuildingCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiSpecialistExtraCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceFlexibleCount = new int[NUM_COMMERCE_TYPES];
	m_aiGoldPerTurnByPlayer = new int[MAX_PLAYERS];
	m_aiEspionageSpendingWeightAgainstTeam = new int[MAX_TEAMS];

	m_abFeatAccomplished = new bool[NUM_FEAT_TYPES];
	m_abOptions = new bool[NUM_PLAYEROPTION_TYPES];

	m_paiBonusExport = NULL;
	m_paiBonusImport = NULL;
	m_paiImprovementCount = NULL;
	m_paiFreeBuildingCount = NULL;
	m_paiExtraBuildingHappiness = NULL;
	m_paiExtraBuildingHealth = NULL;
	m_paiFeatureHappiness = NULL;
	m_paiUnitClassCount = NULL;
	m_paiUnitClassMaking = NULL;
	m_paiBuildingClassCount = NULL;
	m_paiBuildingClassMaking = NULL;
	m_paiHurryCount = NULL;
	m_paiSpecialBuildingNotRequiredCount = NULL;
	m_paiHasCivicOptionCount = NULL;
	m_paiNoCivicUpkeepCount = NULL;
	m_paiHasReligionCount = NULL;
	m_paiHasCorporationCount = NULL;
	m_paiUpkeepCount = NULL;
	m_paiSpecialistValidCount = NULL;
/************************************************************************************************/
/* EVENT_NEW_TAGS                           12/2015                                 lfgr        */
/************************************************************************************************/
	m_paiEventTriggerDelayCounters = NULL;
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/

	m_pabResearchingTech = NULL;
	m_pabLoyalMember = NULL;

	m_paeCivics = NULL;

	m_ppaaiSpecialistExtraYield = NULL;
	m_ppaaiImprovementYieldChange = NULL;

//FfH: Added by Kael 11/06/2007
	m_pbTraits = NULL;
	m_ppaaiSpecialistTypeExtraCommerce = NULL;
//FfH: End Add

/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                        09/01/07                                MRGENIE      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	m_bDisableHuman = false;
/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                        END                                                  */
/************************************************************************************************/
/*************************************************************************************************/
/**	CivCounter			               		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	m_iCivCounter = 0;
	m_iCivCounterMod = 0;
/*************************************************************************************************/
/**	CivCounter								END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* REVOLUTION_MOD                         02/04/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	m_iFreeUnitCountdown = 0;

	m_iStabilityIndex = 500;
	m_iStabilityIndexAverage = 500;
	
	m_bRebel = false;
	m_iMotherPlayer = -1;

	// Used for DynamicCivNames
	CvWString m_szName;
	CvWString m_szCivDesc;
	CvWString m_szCivShort;
	CvWString m_szCivAdj;
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/


/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                            Emperor Fool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Free Tech Popup Fix
	m_bChoosingFreeTech = false;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  Glider1      */
/*************************************************************************************************/
	// RevolutionDCM start - new diplomacy option
	setDoNotBotherStatus(NO_PLAYER);
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/

	reset(NO_PLAYER, true);
}


CvPlayer::~CvPlayer()
{
	uninit();

	SAFE_DELETE_ARRAY(m_aiSeaPlotYield);
	SAFE_DELETE_ARRAY(m_aiYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiCapitalYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiExtraYieldThreshold);
	SAFE_DELETE_ARRAY(m_aiTradeYieldModifier);
	SAFE_DELETE_ARRAY(m_aiFreeCityCommerce);
	SAFE_DELETE_ARRAY(m_aiCommercePercent);
	SAFE_DELETE_ARRAY(m_aiCommerceRate);
	SAFE_DELETE_ARRAY(m_aiCommerceRateModifier);
	SAFE_DELETE_ARRAY(m_aiCapitalCommerceRateModifier);
	SAFE_DELETE_ARRAY(m_aiStateReligionBuildingCommerce);
	SAFE_DELETE_ARRAY(m_aiSpecialistExtraCommerce);
	SAFE_DELETE_ARRAY(m_aiCommerceFlexibleCount);
	SAFE_DELETE_ARRAY(m_aiGoldPerTurnByPlayer);
	SAFE_DELETE_ARRAY(m_aiEspionageSpendingWeightAgainstTeam);
	SAFE_DELETE_ARRAY(m_abFeatAccomplished);
	SAFE_DELETE_ARRAY(m_abOptions);
}

// Player traits game options START
void CvPlayer::addRandomTrait()
{
	// Ugly, hardcoded code. I could create XML tags in the future, but for now we'll keep it like this.
	std::vector<int> lNormalTraits;
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_PHILOSOPHICAL"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_AGGRESSIVE"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_SPIRITUAL"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_EXPANSIVE"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_INDUSTRIOUS"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_CREATIVE"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_FINANCIAL"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_ORGANIZED"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_CHARISMATIC"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_ARCANE"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_RAIDERS"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_SUMMONER"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_AGRARIAN"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_SAVAGE"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_SLAVER"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_SAGE"));
	lNormalTraits.push_back(GC.getInfoTypeForString("TRAIT_IMPERIALISTIC"));

	bool bAddedTrait = false;
	while (!bAddedTrait)
	{
		int iTraitIndex = GC.getGameINLINE().getSorenRandNum(lNormalTraits.size(), "Choosing random trait.");
		if (!hasTrait((TraitTypes)lNormalTraits[iTraitIndex]))
		{
			setHasTrait((TraitTypes)lNormalTraits[iTraitIndex], true);
			bAddedTrait = true;
		}
	}
}

void CvPlayer::setLeaderTraits()
{
	int iInsane = GC.getInfoTypeForString("TRAIT_INSANE");
	if( !isBarbarian() && ( GC.getGameINLINE().isOption(GAMEOPTION_RANDOM_TRAITS) ||
		( GC.getGameINLINE().isOption(GAMEOPTION_INSANE_LEADERS) &&
		!GC.getLeaderHeadInfo(getLeaderType()).hasTrait( (TraitTypes) iInsane ) ) ) )
	{
		int iNumNormalTraits = 2;
		bool bInsane = false;
		if ((GC.getGameINLINE().isOption(GAMEOPTION_INSANE_LEADERS) &&
			!GC.getLeaderHeadInfo(getLeaderType()).hasTrait((TraitTypes) iInsane)) ||
			GC.getGameINLINE().getSorenRandNum(100, "Chance of being an insane leader") < 3)
		{
			bInsane = true;
			iNumNormalTraits = 3;
		}

		int iChosenTraits = 0;
		while (iChosenTraits < iNumNormalTraits)
		{
			addRandomTrait();
			iChosenTraits++;
		}

		if (bInsane)
		{
			setHasTrait((TraitTypes) iInsane, true);
		}
		else
		{
			if (GC.getGameINLINE().getSorenRandNum(100, "Chance of having a third, minor trait") < 25)
			{
				std::vector<int> lThirdTraits;
				lThirdTraits.push_back(GC.getInfoTypeForString("TRAIT_MAGIC_RESISTANT"));
				lThirdTraits.push_back(GC.getInfoTypeForString("TRAIT_BARBARIAN"));
				lThirdTraits.push_back(GC.getInfoTypeForString("TRAIT_DEFENDER"));
				lThirdTraits.push_back(GC.getInfoTypeForString("TRAIT_INGENUITY"));
				lThirdTraits.push_back(GC.getInfoTypeForString("TRAIT_TOLERANT"));

				int iTraitIndex = GC.getGameINLINE().getSorenRandNum(lThirdTraits.size(), "Choosing random third trait.");
				setHasTrait((TraitTypes)lThirdTraits[iTraitIndex], true);
			}
		}
	}
	else if (GC.getGameINLINE().isOption(GAMEOPTION_INSANE_LEADERS) &&
		GC.getLeaderHeadInfo(getLeaderType()).hasTrait((TraitTypes) iInsane))
	{
		// Insane leaders are sane with this game option. Who would have suspected this?
		FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::init");
		for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
		{
			if (GC.getLeaderHeadInfo(getLeaderType()).hasTrait((TraitTypes)iI) && iInsane != iI)
			{
				setHasTrait((TraitTypes)iI, true);
			}
		}
	}
	else
	{
		// Default vanilla code for assigning traits.
		FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::init");
		for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
		{
			if (GC.getLeaderHeadInfo(getLeaderType()).hasTrait((TraitTypes)iI))
			{
				setHasTrait((TraitTypes)iI, true);
			}
		}
	}
}
// Player traits game options END

void CvPlayer::init(PlayerTypes eID)
{
	LeaderHeadTypes eBestPersonality;
	int iValue;
	int iBestValue;
	int iI, iJ;

	//--------------------------------
	// Init saved data
	reset(eID);

	//--------------------------------
	// Init containers
	m_plotGroups.init();

	m_cities.init();

	m_units.init();

	m_selectionGroups.init();

	m_eventsTriggered.init();

	//--------------------------------
	// Init non-saved data
	setupGraphical();

	//--------------------------------
	// Init other game data
	FAssert(getTeam() != NO_TEAM);
	GET_TEAM(getTeam()).changeNumMembers(1);

	if ((GC.getInitCore().getSlotStatus(getID()) == SS_TAKEN) || (GC.getInitCore().getSlotStatus(getID()) == SS_COMPUTER))
	{
		setAlive(true);

		if (GC.getGameINLINE().isOption(GAMEOPTION_RANDOM_PERSONALITIES))
		{
			if (!isBarbarian() && !isMinorCiv())
			{
				iBestValue = 0;
				eBestPersonality = NO_LEADER;

				for (iI = 0; iI < GC.getNumLeaderHeadInfos(); iI++)
				{
					if (iI != GC.getDefineINT("BARBARIAN_LEADER")) // XXX minor civ???
					{
						iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Choosing Personality"));

						for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
						{
							if (GET_PLAYER((PlayerTypes)iJ).isAlive())
							{
								if (GET_PLAYER((PlayerTypes)iJ).getPersonalityType() == ((LeaderHeadTypes)iI))
								{
									iValue /= 2;
								}
							}
						}

						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							eBestPersonality = ((LeaderHeadTypes)iI);
						}
					}
				}

				if (eBestPersonality != NO_LEADER)
				{
					setPersonalityType(eBestPersonality);
				}
			}
		}

		changeBaseFreeUnits(GC.getDefineINT("INITIAL_BASE_FREE_UNITS"));
		changeBaseFreeMilitaryUnits(GC.getDefineINT("INITIAL_BASE_FREE_MILITARY_UNITS"));
		changeFreeUnitsPopulationPercent(GC.getDefineINT("INITIAL_FREE_UNITS_POPULATION_PERCENT"));
		changeFreeMilitaryUnitsPopulationPercent(GC.getDefineINT("INITIAL_FREE_MILITARY_UNITS_POPULATION_PERCENT"));
		changeGoldPerUnit(GC.getDefineINT("INITIAL_GOLD_PER_UNIT"));
		changeTradeRoutes(GC.getDefineINT("INITIAL_TRADE_ROUTES"));
		changeStateReligionHappiness(GC.getDefineINT("INITIAL_STATE_RELIGION_HAPPINESS"));
		changeNonStateReligionHappiness(GC.getDefineINT("INITIAL_NON_STATE_RELIGION_HAPPINESS"));

		for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			changeTradeYieldModifier(((YieldTypes)iI), GC.getYieldInfo((YieldTypes)iI).getTradeModifier());
		}

		for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			setCommercePercent(((CommerceTypes)iI), GC.getCommerceInfo((CommerceTypes)iI).getInitialPercent());
		}

// Player traits game options START
		setLeaderTraits();
// Player traits game options END

//FfH: Added for FFH
	/********************************************************************************/
	/* EXTRA_CIV_TRAITS                08/2013                              lfgr    */
	/********************************************************************************/
	/* old
        if (GC.getCivilizationInfo(getCivilizationType()).getCivTrait() != NO_TRAIT)
        {
            setHasTrait((TraitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivTrait(), true);
        }
	*/
		for( int iTrait = 0; iTrait < GC.getNumTraitInfos(); iTrait++ )
			if( GC.getCivilizationInfo( getCivilizationType() ).isCivTraits( iTrait ) )
				setHasTrait( (TraitTypes) iTrait, true );
	/********************************************************************************/
	/* EXTRA_CIV_TRAITS                                                     END     */
	/********************************************************************************/
		setAlignment((AlignmentTypes) GC.getLeaderHeadInfo(getLeaderType()).getAlignment());
        GC.getGameINLINE().changeGlobalCounterLimit(GC.getDefineINT("GLOBAL_COUNTER_LIMIT_PER_PLAYER"));
//FfH: End Add

		updateMaxAnarchyTurns();

		for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			updateExtraYieldThreshold((YieldTypes)iI);
		}

		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), ((CivicTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationInitialCivics(iI))));
		}

		for (iI = 0; iI < GC.getNumEventInfos(); iI++)
		{
			resetEventOccured((EventTypes)iI, false);
		}

		for (iI = 0; iI < GC.getNumEventTriggerInfos(); iI++)
		{
			resetTriggerFired((EventTriggerTypes)iI);
		}

		for (iI = 0; iI < GC.getNumUnitClassInfos(); ++iI)
		{
			UnitTypes eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI)));

			if (NO_UNIT != eUnit)
			{
				if (GC.getUnitInfo(eUnit).isFound())
				{
					setUnitExtraCost((UnitClassTypes)iI, getNewCityProductionValue());
				}
			}
		}
	}

/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
	// RevolutionDCM start - new diplomacy option
	setDoNotBotherStatus(NO_PLAYER);
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/

	AI_init();
}

/************************************************************************************************/
/* REVOLUTION_MOD                         01/04/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// Copy of CvPlayer::init but with modifications for use in the middle of a game
// Modified to mimic changes to init for FFH by Tholal - 12/18/11
void CvPlayer::initInGame(PlayerTypes eID, bool bSetAlive)
{
	LeaderHeadTypes eBestPersonality;
	int iValue;
	int iBestValue;
	int iI, iJ;

	//--------------------------------
	// Init saved data
	reset(eID);

	//--------------------------------
	// Init containers
	m_plotGroups.init();

	m_cities.init();

	m_units.init();

	m_selectionGroups.init();

	m_eventsTriggered.init();

	//--------------------------------
	// Init non-saved data
	setupGraphical();

	//--------------------------------
	// Init other game data
	FAssert(getTeam() != NO_TEAM);

	// Some effects on team necessary if this is the only member of the team
	int iOtherTeamMembers = 0;
	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if( iI != getID() )
		{
			if( GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam() )
			{
				iOtherTeamMembers++;
			}
		}
	}

	bool bTeamInit = false;
	if( (iOtherTeamMembers == 0) || GET_TEAM(getTeam()).getNumMembers() == 0 )
	{
		bTeamInit = true;
		GET_TEAM(getTeam()).init(getTeam());
		GET_TEAM(getTeam()).resetPlotAndCityData();
	}

	if( bTeamInit || (GET_TEAM(getTeam()).getNumMembers() == iOtherTeamMembers) )
	{
		GET_TEAM(getTeam()).changeNumMembers(1);
	}

	if ((GC.getInitCore().getSlotStatus(getID()) == SS_TAKEN) || (GC.getInitCore().getSlotStatus(getID()) == SS_COMPUTER))
	{
		if( bSetAlive ) 
		{
			setAlive(true);
		}

		if (GC.getGameINLINE().isOption(GAMEOPTION_RANDOM_PERSONALITIES))
		{
			if (!isBarbarian() && !isMinorCiv())
			{
				iBestValue = 0;
				eBestPersonality = NO_LEADER;

				for (iI = 0; iI < GC.getNumLeaderHeadInfos(); iI++)
				{
					if (iI != GC.getDefineINT("BARBARIAN_LEADER")) // XXX minor civ???
					{
						iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Choosing Personality"));

						for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
						{
							if (GET_PLAYER((PlayerTypes)iJ).isAlive())
							{
								if (GET_PLAYER((PlayerTypes)iJ).getPersonalityType() == ((LeaderHeadTypes)iI))
								{
									iValue /= 2;
								}
							}
						}

						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							eBestPersonality = ((LeaderHeadTypes)iI);
						}
					}
				}

				if (eBestPersonality != NO_LEADER)
				{
					setPersonalityType(eBestPersonality);
				}
			}
		}

		changeBaseFreeUnits(GC.getDefineINT("INITIAL_BASE_FREE_UNITS"));
		changeBaseFreeMilitaryUnits(GC.getDefineINT("INITIAL_BASE_FREE_MILITARY_UNITS"));
		changeFreeUnitsPopulationPercent(GC.getDefineINT("INITIAL_FREE_UNITS_POPULATION_PERCENT"));
		changeFreeMilitaryUnitsPopulationPercent(GC.getDefineINT("INITIAL_FREE_MILITARY_UNITS_POPULATION_PERCENT"));
		changeGoldPerUnit(GC.getDefineINT("INITIAL_GOLD_PER_UNIT"));
		changeTradeRoutes(GC.getDefineINT("INITIAL_TRADE_ROUTES"));
		changeStateReligionHappiness(GC.getDefineINT("INITIAL_STATE_RELIGION_HAPPINESS"));
		changeNonStateReligionHappiness(GC.getDefineINT("INITIAL_NON_STATE_RELIGION_HAPPINESS"));

		for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			changeTradeYieldModifier(((YieldTypes)iI), GC.getYieldInfo((YieldTypes)iI).getTradeModifier());
		}

		for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			setCommercePercent(((CommerceTypes)iI), GC.getCommerceInfo((CommerceTypes)iI).getInitialPercent());
		}

// Player traits game options START
		setLeaderTraits();
// Player traits game options END

//FfH: Added for FFH
	/********************************************************************************/
	/* EXTRA_CIV_TRAITS                08/2013                              lfgr    */
	/********************************************************************************/
	/* old
        if (GC.getCivilizationInfo(getCivilizationType()).getCivTrait() != NO_TRAIT)
        {
            setHasTrait((TraitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivTrait(), true);
        }
	*/
		for( int iTrait = 0; iTrait < GC.getNumTraitInfos(); iTrait++ )
			if( GC.getCivilizationInfo( getCivilizationType() ).isCivTraits( iTrait ) )
				setHasTrait( (TraitTypes) iTrait, true );
	/********************************************************************************/
	/* EXTRA_CIV_TRAITS                                                     END     */
	/********************************************************************************/
		setAlignment((AlignmentTypes) GC.getLeaderHeadInfo(getLeaderType()).getAlignment());
        GC.getGameINLINE().changeGlobalCounterLimit(GC.getDefineINT("GLOBAL_COUNTER_LIMIT_PER_PLAYER"));
//FfH: End Add

		updateMaxAnarchyTurns();

		for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			updateExtraYieldThreshold((YieldTypes)iI);
		}

		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), ((CivicTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationInitialCivics(iI))));
		}

		// Reset all triggers at first, set those whose events have fired in next block
		for (iI = 0; iI < GC.getNumEventTriggerInfos(); iI++)
		{
			resetTriggerFired((EventTriggerTypes)iI);
		}

		for (iI = 0; iI < GC.getNumEventInfos(); iI++)
		{
/* original bts code
			resetEventOccured((EventTypes)iI, false);
*/
			// Has global trigger fired already?
				
			const EventTriggeredData* pEvent = NULL;
			for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
			{
				if( iJ != getID() )
				{
					pEvent = GET_PLAYER((PlayerTypes)iJ).getEventOccured((EventTypes)iI);
					if ( pEvent != NULL )
					{
						CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(pEvent->m_eTrigger);
						if( kTrigger.isGlobal() )
						{
							setTriggerFired( *pEvent, false, false, false );
							break;
						}
						else if( kTrigger.isTeam() && GET_PLAYER((PlayerTypes)iJ).getTeam() == getTeam() )
						{
							setTriggerFired( *pEvent, false, false, false );
							break;
						}
					}
				}
			}
			
			resetEventOccured((EventTypes)iI, false);
		}

		for (iI = 0; iI < GC.getNumUnitClassInfos(); ++iI)
		{
			UnitTypes eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI)));

			if (NO_UNIT != eUnit)
			{
				if (GC.getUnitInfo(eUnit).isFound())
				{
					setUnitExtraCost((UnitClassTypes)iI, getNewCityProductionValue());
				}
			}
		}
	}

	resetPlotAndCityData();

	AI_init();
}

//
// Reset all data for this player stored in plot and city objects
//
void CvPlayer::resetPlotAndCityData( )
{
	CvPlot* pLoopPlot;
	CvCity* pLoopCity;
	for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

		pLoopPlot->setCulture(getID(), 0, false, false);
		pLoopPlot->setFoundValue(getID(), 0);

		pLoopCity = pLoopPlot->getPlotCity();
		if( pLoopCity != NULL )
		{
			pLoopCity->setCulture(getID(), 0, false, false);
			pLoopCity->changeNumRevolts(getID(), -pLoopCity->getNumRevolts(getID()));
			pLoopCity->setEverOwned(getID(), false);
			pLoopCity->setTradeRoute(getID(), false);
		}
	}
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/


void CvPlayer::uninit()
{
	SAFE_DELETE_ARRAY(m_paiBonusExport);
	SAFE_DELETE_ARRAY(m_paiBonusImport);
	SAFE_DELETE_ARRAY(m_paiImprovementCount);
	SAFE_DELETE_ARRAY(m_paiFreeBuildingCount);
	SAFE_DELETE_ARRAY(m_paiExtraBuildingHappiness);
	SAFE_DELETE_ARRAY(m_paiExtraBuildingHealth);
	SAFE_DELETE_ARRAY(m_paiFeatureHappiness);
	SAFE_DELETE_ARRAY(m_paiUnitClassCount);
	SAFE_DELETE_ARRAY(m_paiUnitClassMaking);
	SAFE_DELETE_ARRAY(m_paiBuildingClassCount);
	SAFE_DELETE_ARRAY(m_paiBuildingClassMaking);
	SAFE_DELETE_ARRAY(m_paiHurryCount);
	SAFE_DELETE_ARRAY(m_paiSpecialBuildingNotRequiredCount);
	SAFE_DELETE_ARRAY(m_paiHasCivicOptionCount);
	SAFE_DELETE_ARRAY(m_paiNoCivicUpkeepCount);
	SAFE_DELETE_ARRAY(m_paiHasReligionCount);
	SAFE_DELETE_ARRAY(m_paiHasCorporationCount);
	SAFE_DELETE_ARRAY(m_paiUpkeepCount);
	SAFE_DELETE_ARRAY(m_paiSpecialistValidCount);
/************************************************************************************************/
/* EVENT_NEW_TAGS                           12/2015                                 lfgr        */
/************************************************************************************************/
	SAFE_DELETE_ARRAY(m_paiEventTriggerDelayCounters);
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/

	SAFE_DELETE_ARRAY(m_pabResearchingTech);
	SAFE_DELETE_ARRAY(m_pabLoyalMember);

	SAFE_DELETE_ARRAY(m_paeCivics);

	m_triggersFired.clear();

//FfH Scriptable Leader Traits: Added by Kael 08/08/2007
	SAFE_DELETE_ARRAY(m_pbTraits);
	if (m_ppaaiSpecialistTypeExtraCommerce != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiSpecialistTypeExtraCommerce[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiSpecialistTypeExtraCommerce);
	}
//FfH: End Add

	if (m_ppaaiSpecialistExtraYield != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiSpecialistExtraYield[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiSpecialistExtraYield);
	}

	if (m_ppaaiImprovementYieldChange != NULL)
	{
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiImprovementYieldChange[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiImprovementYieldChange);
	}

	m_groupCycle.clear();

	m_researchQueue.clear();

	m_cityNames.clear();


	m_plotGroups.uninit();

	m_cities.uninit();

	m_units.uninit();

	m_selectionGroups.uninit();

	m_eventsTriggered.uninit();

	clearMessages();

	clearPopups();

	clearDiplomacy();
}


// FUNCTION: reset()
// Initializes data members that are serialized.
void CvPlayer::reset(PlayerTypes eID, bool bConstructorCall)
{
	int iI, iJ;

	//--------------------------------
	// Uninit class
	uninit();

	m_iStartingX = INVALID_PLOT_COORD;
	m_iStartingY = INVALID_PLOT_COORD;
	m_iTotalPopulation = 0;
	m_iTotalLand = 0;
	m_iTotalLandScored = 0;
	m_iGold = 0;
	m_iGoldPerTurn = 0;
	m_iAdvancedStartPoints = -1;
	m_iGoldenAgeTurns = 0;
	m_iNumUnitGoldenAges = 0;
	m_iStrikeTurns = 0;
	m_iAnarchyTurns = 0;
	m_iMaxAnarchyTurns = 0;
	m_iAnarchyModifier = 0;
	m_iGoldenAgeModifier = 0;
	m_iGlobalHurryModifier = 0;
	m_iGreatPeopleCreated = 0;
	m_iGreatGeneralsCreated = 0;
	m_iGreatPeopleThresholdModifier = 0;
	m_iGreatGeneralsThresholdModifier = 0;
	m_iGreatPeopleRateModifier = 0;
	m_iGreatGeneralRateModifier = 0;
	m_iDomesticGreatGeneralRateModifier = 0;
	m_iStateReligionGreatPeopleRateModifier = 0;
	m_iMaxGlobalBuildingProductionModifier = 0;
	m_iMaxTeamBuildingProductionModifier = 0;
	m_iMaxPlayerBuildingProductionModifier = 0;
	m_iFreeExperience = 0;
	m_iFeatureProductionModifier = 0;
	m_iWorkerSpeedModifier = 0;
	m_iImprovementUpgradeRateModifier = 0;
	m_iMilitaryProductionModifier = 0;
	m_iSpaceProductionModifier = 0;
	m_iCityDefenseModifier = 0;
/************************************************************************************************/
/* REVDCM                                 09/02/10                                phungus420    */
/*                                                                                              */
/* Player Functions                                                                             */
/************************************************************************************************/
	m_iNonStateReligionCommerceCount = 0;
	m_bCanInquisition = true;
/************************************************************************************************/
/* REVDCM                                  END                                                  */
/************************************************************************************************/
	m_iNumNukeUnits = 0; 
	m_iNumOutsideUnits = 0; 
	m_iBaseFreeUnits = 0;
	m_iBaseFreeMilitaryUnits = 0;
	m_iFreeUnitsPopulationPercent = 0;
	m_iFreeMilitaryUnitsPopulationPercent = 0;
	m_iGoldPerUnit = 0;
	m_iGoldPerMilitaryUnit = 0;
	m_iExtraUnitCost = 0;
	m_iNumMilitaryUnits = 0;
	m_iHappyPerMilitaryUnit = 0;
	m_iMilitaryFoodProductionCount = 0;
	m_iConscriptCount = 0;
	m_iMaxConscript = 0;
	m_iHighestUnitLevel = 1;
	m_iOverflowResearch = 0;
	m_iNoUnhealthyPopulationCount = 0;
	m_iExpInBorderModifier = 0;
	m_iBuildingOnlyHealthyCount = 0;
	m_iDistanceMaintenanceModifier = 0;
	m_iNumCitiesMaintenanceModifier = 0;
	m_iCorporationMaintenanceModifier = 0;
	m_iTotalMaintenance = 0;
	m_iUpkeepModifier = 0;
	m_iLevelExperienceModifier = 0;
	m_iExtraHealth = 0;
	m_iBuildingGoodHealth = 0;
	m_iBuildingBadHealth = 0;
	m_iExtraHappiness = 0;
	m_iBuildingHappiness = 0;
	m_iLargestCityHappiness = 0;
	m_iWarWearinessPercentAnger = 0;
	m_iWarWearinessModifier = 0;
	m_iFreeSpecialist = 0;
	m_iNoForeignTradeCount = 0;
	m_iNoCorporationsCount = 0;
	m_iNoForeignCorporationsCount = 0;
	m_iCoastalTradeRoutes = 0;
	m_iTradeRoutes = 0;
	m_iRevolutionTimer = 0;
	m_iConversionTimer = 0;
	m_iStateReligionCount = 0;
	m_iNoNonStateReligionSpreadCount = 0;
/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
	m_iActiveSenateCount = 0;
/*************************************************************************************************/
/** Advanced Diplomacy       END                                                  			 */
/*************************************************************************************************/
	m_iStateReligionHappiness = 0;
	m_iNonStateReligionHappiness = 0;
	m_iStateReligionUnitProductionModifier = 0;
	m_iStateReligionBuildingProductionModifier = 0;
	m_iStateReligionFreeExperience = 0;
	m_iCapitalCityID = FFreeList::INVALID_INDEX;
	m_iCitiesLost = 0;
	m_iWinsVsBarbs = 0;
	m_iAssets = 0;
	m_iPower = 0;
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	m_iTechPower = 0;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	m_iPopulationScore = 0;
	m_iLandScore = 0;
	m_iTechScore = 0;
	m_iWondersScore = 0;
	m_iCombatExperience = 0;
	m_iPopRushHurryCount = 0;
	m_iInflationModifier = 0;
	m_uiStartTime = 0;

	m_bAlive = false;
	m_bEverAlive = false;
	m_bTurnActive = false;
	m_bAutoMoves = false;
	m_bEndTurn = false;
	m_bPbemNewTurn = false;
	m_bExtendedGame = false;
	m_bFoundedFirstCity = false;
	m_bStrike = false;

	m_bPuppetState = false; // MNAI - Puppet States

	// Sephi AI (New Functions Definition)
    m_eFavoriteReligion = NO_RELIGION;
    m_iTowerVicFlag = 0;
	m_bSumSuiMode = false;
	// End Sephi AI


	//FfH: Added by Kael 04/11/2008
	m_bAdaptive = false;
	m_bAgnostic = false;
	m_bAssimilation = false;
	m_bDeclaringWar = false;
	//m_bDisableHuman = false;
	m_bHideUnits = false;
	m_bIgnoreFood = false;
	m_bInsane = false;
	m_bSeeInvisible = false;
	m_bSprawling = false;
	m_eAlignment = NO_ALIGNMENT;
	m_iDisableProduction = 0;
	m_iDisableResearch = 0;
	m_iDisableSpellcasting = 0;
	m_iDiscoverRandModifier = 0;
    m_iEnslavementChance = 0;
	m_iFreeXPFromCombat = 0;
	m_iHealChange = 0;
	m_iHealChangeEnemy = 0;
	m_iMaxCities = -1;
	m_iNoDiplomacyWithEnemies = 0;
	m_iPillagingGold = 0;
	m_iPlayersKilled = 0;
	m_iRealPlayer = NO_PLAYER;
	m_iResistEnemyModify = 0;
	m_iResistModify = 0;
	m_iSanctuaryTimer = 0;
	m_iStartingGold = 0;
	m_iSummonDuration = 0;
	m_iTempPlayerTimer = 0;
	m_iUpgradeCostModifier = 0;
//FfH: End Add

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                            Emperor Fool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Free Tech Popup Fix
	m_bChoosingFreeTech = false;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                        09/01/07                            MRGENIE          */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	m_bDisableHuman = false;
/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                        END                                                  */
/************************************************************************************************/

/*************************************************************************************************/
/**	CivCounter			               		11/04/12    						Terkhen			**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	m_iCivCounter = 0;
	m_iCivCounterMod = 0;
/*************************************************************************************************/
/**	CivCounter								END													**/
/*************************************************************************************************/

/************************************************************************************************/
/* REVOLUTION_MOD                         02/04/09                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	m_iFreeUnitCountdown = 0;

	m_iStabilityIndex = 500;
	m_iStabilityIndexAverage = 500;

	m_bRebel = false;
	m_iMotherPlayer = -1;

	// Used for DynamicCivNames
	m_szName.clear();
	m_szCivDesc.clear();
	m_szCivShort.clear();
	m_szCivAdj.clear();
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	m_eID = eID;
	updateTeamType();
	updateHuman();

	if (m_eID != NO_PLAYER)
	{
		m_ePersonalityType = GC.getInitCore().getLeader(m_eID); //??? Is this repeated data???
	}
	else
	{
		m_ePersonalityType = NO_LEADER;
	}
	m_eCurrentEra = ((EraTypes)0);  //??? Is this repeated data???
// ERA_FIX 09/2017 lfgr
	m_eCurrentRealEra = (EraTypes) 0;
// ERA_FIX end
	m_eLastStateReligion = NO_RELIGION;
	m_eParent = NO_PLAYER;
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	m_eSecretaryGeneralVote = NO_TEAM;
	m_eDemandWarAgainstTeam = NO_TEAM;
	m_aiSenateVeto.clear();
/************************************************************************************************/
/* Advanced Diplomacy          END                                                            */
/************************************************************************************************/

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		m_aiSeaPlotYield[iI] = 0;
		m_aiYieldRateModifier[iI] = 0;
		m_aiCapitalYieldRateModifier[iI] = 0;
		m_aiExtraYieldThreshold[iI] = 0;
		m_aiTradeYieldModifier[iI] = 0;
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		m_aiFreeCityCommerce[iI] = 0;
		m_aiCommercePercent[iI] = 0;
		m_aiCommerceRate[iI] = 0;
		m_aiCommerceRateModifier[iI] = 0;
		m_aiCapitalCommerceRateModifier[iI] = 0;
		m_aiStateReligionBuildingCommerce[iI] = 0;
		m_aiSpecialistExtraCommerce[iI] = 0;
		m_aiCommerceFlexibleCount[iI] = 0;
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_aiGoldPerTurnByPlayer[iI] = 0;
		if (!bConstructorCall && getID() != NO_PLAYER)
		{
			GET_PLAYER((PlayerTypes) iI).m_aiGoldPerTurnByPlayer[getID()] = 0;
		}
	}

	for (iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_aiEspionageSpendingWeightAgainstTeam[iI] = 0;

		if (!bConstructorCall && getTeam() != NO_TEAM)
		{
			for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
			{
				if (GET_PLAYER((PlayerTypes) iJ).getTeam() == iI)
				{
					GET_PLAYER((PlayerTypes) iJ).setEspionageSpendingWeightAgainstTeam(getTeam(), 0);
				}
			}
		}
	}

	for (iI = 0; iI < NUM_FEAT_TYPES; iI++)
	{
		m_abFeatAccomplished[iI] = false;
	}

	for (iI = 0; iI < NUM_PLAYEROPTION_TYPES; iI++)
	{
		m_abOptions[iI] = false;
	}

	m_szScriptData = "";

	if (!bConstructorCall)
	{
		FAssertMsg(0 < GC.getNumBonusInfos(), "GC.getNumBonusInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiBonusExport==NULL, "about to leak memory, CvPlayer::m_paiBonusExport");
		m_paiBonusExport = new int [GC.getNumBonusInfos()];
		FAssertMsg(m_paiBonusImport==NULL, "about to leak memory, CvPlayer::m_paiBonusImport");
		m_paiBonusImport = new int [GC.getNumBonusInfos()];
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiBonusExport[iI] = 0;
			m_paiBonusImport[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumImprovementInfos(), "GC.getNumImprovementInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiImprovementCount==NULL, "about to leak memory, CvPlayer::m_paiImprovementCount");
		m_paiImprovementCount = new int [GC.getNumImprovementInfos()];
		for (iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			m_paiImprovementCount[iI] = 0;
		}

		FAssertMsg(m_paiFreeBuildingCount==NULL, "about to leak memory, CvPlayer::m_paiFreeBuildingCount");
		m_paiFreeBuildingCount = new int [GC.getNumBuildingInfos()];
		FAssertMsg(m_paiExtraBuildingHappiness==NULL, "about to leak memory, CvPlayer::m_paiExtraBuildingHappiness");
		m_paiExtraBuildingHappiness = new int [GC.getNumBuildingInfos()];
		FAssertMsg(m_paiExtraBuildingHealth==NULL, "about to leak memory, CvPlayer::m_paiExtraBuildingHealth");
		m_paiExtraBuildingHealth = new int [GC.getNumBuildingInfos()];
		for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
		{
			m_paiFreeBuildingCount[iI] = 0;
			m_paiExtraBuildingHappiness[iI] = 0;
			m_paiExtraBuildingHealth[iI] = 0;
		}

		FAssertMsg(m_paiFeatureHappiness==NULL, "about to leak memory, CvPlayer::m_paiFeatureHappiness");
		m_paiFeatureHappiness = new int [GC.getNumFeatureInfos()];
		for (iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			m_paiFeatureHappiness[iI] = 0;
		}

		FAssertMsg(m_paiUnitClassCount==NULL, "about to leak memory, CvPlayer::m_paiUnitClassCount");
		m_paiUnitClassCount = new int [GC.getNumUnitClassInfos()];
		FAssertMsg(m_paiUnitClassMaking==NULL, "about to leak memory, CvPlayer::m_paiUnitClassMaking");
		m_paiUnitClassMaking = new int [GC.getNumUnitClassInfos()];
		for (iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
		{
			m_paiUnitClassCount[iI] = 0;
			m_paiUnitClassMaking[iI] = 0;
		}

		FAssertMsg(m_paiBuildingClassCount==NULL, "about to leak memory, CvPlayer::m_paiBuildingClassCount");
		m_paiBuildingClassCount = new int [GC.getNumBuildingClassInfos()];
		FAssertMsg(m_paiBuildingClassMaking==NULL, "about to leak memory, CvPlayer::m_paiBuildingClassMaking");
		m_paiBuildingClassMaking = new int [GC.getNumBuildingClassInfos()];
		for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
		{
			m_paiBuildingClassCount[iI] = 0;
			m_paiBuildingClassMaking[iI] = 0;
		}

		FAssertMsg(m_paiHurryCount==NULL, "about to leak memory, CvPlayer::m_paiHurryCount");
		m_paiHurryCount = new int [GC.getNumHurryInfos()];
		for (iI = 0; iI < GC.getNumHurryInfos(); iI++)
		{
			m_paiHurryCount[iI] = 0;
		}

		FAssertMsg(m_paiSpecialBuildingNotRequiredCount==NULL, "about to leak memory, CvPlayer::m_paiSpecialBuildingNotRequiredCount");
		m_paiSpecialBuildingNotRequiredCount = new int [GC.getNumSpecialBuildingInfos()];
		for (iI = 0; iI < GC.getNumSpecialBuildingInfos(); iI++)
		{
			m_paiSpecialBuildingNotRequiredCount[iI] = 0;
		}

		FAssertMsg(m_paiHasCivicOptionCount==NULL, "about to leak memory, CvPlayer::m_paiHasCivicOptionCount");
		m_paiHasCivicOptionCount = new int[GC.getNumCivicOptionInfos()];
		FAssertMsg(m_paiNoCivicUpkeepCount==NULL, "about to leak memory, CvPlayer::m_paiNoCivicUpkeepCount");
		m_paiNoCivicUpkeepCount = new int[GC.getNumCivicOptionInfos()];
		FAssertMsg(m_paeCivics==NULL, "about to leak memory, CvPlayer::m_paeCivics");
		m_paeCivics = new CivicTypes [GC.getNumCivicOptionInfos()];
		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			m_paiHasCivicOptionCount[iI] = 0;
			m_paiNoCivicUpkeepCount[iI] = 0;
			m_paeCivics[iI] = NO_CIVIC;
		}

		FAssertMsg(m_paiHasReligionCount==NULL, "about to leak memory, CvPlayer::m_paiHasReligionCount");
		m_paiHasReligionCount = new int[GC.getNumReligionInfos()];
		for (iI = 0;iI < GC.getNumReligionInfos();iI++)
		{
			m_paiHasReligionCount[iI] = 0;
		}

		FAssertMsg(m_paiHasCorporationCount==NULL, "about to leak memory, CvPlayer::m_paiHasReligionCount");
		m_paiHasCorporationCount = new int[GC.getNumCorporationInfos()];
		for (iI = 0;iI < GC.getNumCorporationInfos();iI++)
		{
			m_paiHasCorporationCount[iI] = 0;
		}
/************************************************************************************************/
/* EVENT_NEW_TAGS                           12/2015                                 lfgr        */
/************************************************************************************************/
		FAssertMsg(m_paiEventTriggerDelayCounters==NULL, "about to leak memory, CvPlayer::m_paiEventTriggerDelayCounters");
		m_paiEventTriggerDelayCounters = new int[GC.getNumEventTriggerInfos()];
		for (iI = 0;iI < GC.getNumEventTriggerInfos();iI++)
		{
			m_paiEventTriggerDelayCounters[iI] = 0;
		}
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/

		FAssertMsg(m_pabResearchingTech==NULL, "about to leak memory, CvPlayer::m_pabResearchingTech");
		m_pabResearchingTech = new bool[GC.getNumTechInfos()];
		for (iI = 0; iI < GC.getNumTechInfos(); iI++)
		{
			m_pabResearchingTech[iI] = false;
		}

//FfH Scriptable Leader Traits: Added by Kael 08/08/2007
		FAssertMsg(m_pbTraits==NULL, "about to leak memory, CvPlayer::m_pbTraits");
		m_pbTraits = new bool[GC.getNumTraitInfos()];
		for (iI = 0; iI < GC.getNumTraitInfos(); iI++)
		{
			m_pbTraits[iI] = false;
		}
		m_ppaaiSpecialistTypeExtraCommerce = new int*[GC.getNumSpecialistInfos()];
		for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			m_ppaaiSpecialistTypeExtraCommerce[iI] = new int[NUM_COMMERCE_TYPES];
			for (iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
			{
				m_ppaaiSpecialistTypeExtraCommerce[iI][iJ] = 0;
			}
		}
//FfH: End Add

		FAssertMsg(m_pabLoyalMember==NULL, "about to leak memory, CvPlayer::m_pabLoyalMember");
		m_pabLoyalMember = new bool[GC.getNumVoteSourceInfos()];
		for (iI = 0; iI < GC.getNumVoteSourceInfos(); iI++)
		{
			m_pabLoyalMember[iI] = true;
		}

		FAssertMsg(0 < GC.getNumUpkeepInfos(), "GC.getNumUpkeepInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiUpkeepCount==NULL, "about to leak memory, CvPlayer::m_paiUpkeepCount");
		m_paiUpkeepCount = new int[GC.getNumUpkeepInfos()];
		for (iI = 0; iI < GC.getNumUpkeepInfos(); iI++)
		{
			m_paiUpkeepCount[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistInfos(), "GC.getNumSpecialistInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistValidCount==NULL, "about to leak memory, CvPlayer::m_paiSpecialistValidCount");
		m_paiSpecialistValidCount = new int[GC.getNumSpecialistInfos()];
		for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			m_paiSpecialistValidCount[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistInfos(), "GC.getNumSpecialistInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_ppaaiSpecialistExtraYield==NULL, "about to leak memory, CvPlayer::m_ppaaiSpecialistExtraYield");
		m_ppaaiSpecialistExtraYield = new int*[GC.getNumSpecialistInfos()];
		for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			m_ppaaiSpecialistExtraYield[iI] = new int[NUM_YIELD_TYPES];
			for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_ppaaiSpecialistExtraYield[iI][iJ] = 0;
			}
		}

		FAssertMsg(m_ppaaiImprovementYieldChange==NULL, "about to leak memory, CvPlayer::m_ppaaiImprovementYieldChange");
		m_ppaaiImprovementYieldChange = new int*[GC.getNumImprovementInfos()];
		for (iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			m_ppaaiImprovementYieldChange[iI] = new int[NUM_YIELD_TYPES];
			for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_ppaaiImprovementYieldChange[iI][iJ] = 0;
			}
		}

		m_mapEventsOccured.clear();
		m_mapEventCountdown.clear();
		m_aFreeUnitCombatPromotions.clear();
		m_aFreeUnitClassPromotions.clear();
		m_aVote.clear();
		m_aUnitExtraCosts.clear();
		m_triggersFired.clear();
	}

	m_plotGroups.removeAll();

	m_cities.removeAll();

	m_units.removeAll();

	m_selectionGroups.removeAll();

	m_eventsTriggered.removeAll();

	if (!bConstructorCall)
	{
		AI_reset(false);
	}
/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  Glider1      */
/*************************************************************************************************/
	// RevolutionDCM start - new diplomacy option
	setDoNotBotherStatus(NO_PLAYER);
	// RevolutionDCM end
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/

}

/************************************************************************************************/
/* CHANGE_PLAYER                          08/17/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for logging
//
void CvPlayer::logMsg(char* format, ... )
{
	static char buf[2048];
	_vsnprintf( buf, 2048-4, format, (char*)(&format+1) );
	gDLL->logMsg("sdkDbg.log", buf);
}

/************************************************************************************************/
/* CHANGE_PLAYER                           END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* CHANGE_PLAYER                          08/17/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for stripping obsolete trait bonuses
// for complete reset, use in conjunction with addTraitBonuses
//
void CvPlayer::clearTraitBonuses( )
{
	int iI, iJ;

	FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::init");
	for (iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			changeExtraHealth(-GC.getTraitInfo((TraitTypes)iI).getHealth());
			changeExtraHappiness(-GC.getTraitInfo((TraitTypes)iI).getHappiness());

			for (iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
			{
				changeExtraBuildingHappiness((BuildingTypes)iJ, -GC.getBuildingInfo((BuildingTypes)iJ).getHappinessTraits(iI));
			}

			changeUpkeepModifier(-GC.getTraitInfo((TraitTypes)iI).getUpkeepModifier());
			changeLevelExperienceModifier(-GC.getTraitInfo((TraitTypes)iI).getLevelExperienceModifier());
			changeGreatPeopleRateModifier(-GC.getTraitInfo((TraitTypes)iI).getGreatPeopleRateModifier());
			changeGreatGeneralRateModifier(-GC.getTraitInfo((TraitTypes)iI).getGreatGeneralRateModifier());
			changeDomesticGreatGeneralRateModifier(-GC.getTraitInfo((TraitTypes)iI).getDomesticGreatGeneralRateModifier());

			changeMaxGlobalBuildingProductionModifier(-GC.getTraitInfo((TraitTypes)iI).getMaxGlobalBuildingProductionModifier());
			changeMaxTeamBuildingProductionModifier(-GC.getTraitInfo((TraitTypes)iI).getMaxTeamBuildingProductionModifier());
			changeMaxPlayerBuildingProductionModifier(-GC.getTraitInfo((TraitTypes)iI).getMaxPlayerBuildingProductionModifier());

			for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeTradeYieldModifier(((YieldTypes)iJ), -GC.getTraitInfo((TraitTypes)iI).getTradeYieldModifier(iJ));
			}

			for (iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
			{
				changeFreeCityCommerce(((CommerceTypes)iJ), -GC.getTraitInfo((TraitTypes)iI).getCommerceChange(iJ));
				changeCommerceRateModifier(((CommerceTypes)iJ), -GC.getTraitInfo((TraitTypes)iI).getCommerceModifier(iJ));
			}

			for (iJ = 0; iJ < GC.getNumCivicOptionInfos(); iJ++)
			{
				if (GC.getCivicOptionInfo((CivicOptionTypes) iJ).getTraitNoUpkeep(iI))
				{
					changeNoCivicUpkeepCount(((CivicOptionTypes)iJ), -1);
				}
			}
		}
	}
}

//
// for adding new trait bonuses
//
void CvPlayer::addTraitBonuses( )
{
	int iI, iJ;

	FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::init");
	for (iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			changeExtraHealth(GC.getTraitInfo((TraitTypes)iI).getHealth());
			changeExtraHappiness(GC.getTraitInfo((TraitTypes)iI).getHappiness());

			for (iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
			{
				changeExtraBuildingHappiness((BuildingTypes)iJ, GC.getBuildingInfo((BuildingTypes)iJ).getHappinessTraits(iI));
			}

			changeUpkeepModifier(GC.getTraitInfo((TraitTypes)iI).getUpkeepModifier());
			changeLevelExperienceModifier(GC.getTraitInfo((TraitTypes)iI).getLevelExperienceModifier());
			changeGreatPeopleRateModifier(GC.getTraitInfo((TraitTypes)iI).getGreatPeopleRateModifier());
			changeGreatGeneralRateModifier(GC.getTraitInfo((TraitTypes)iI).getGreatGeneralRateModifier());
			changeDomesticGreatGeneralRateModifier(GC.getTraitInfo((TraitTypes)iI).getDomesticGreatGeneralRateModifier());

			changeMaxGlobalBuildingProductionModifier(GC.getTraitInfo((TraitTypes)iI).getMaxGlobalBuildingProductionModifier());
			changeMaxTeamBuildingProductionModifier(GC.getTraitInfo((TraitTypes)iI).getMaxTeamBuildingProductionModifier());
			changeMaxPlayerBuildingProductionModifier(GC.getTraitInfo((TraitTypes)iI).getMaxPlayerBuildingProductionModifier());

			for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeTradeYieldModifier(((YieldTypes)iJ), GC.getTraitInfo((TraitTypes)iI).getTradeYieldModifier(iJ));
			}

			for (iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
			{
				changeFreeCityCommerce(((CommerceTypes)iJ), GC.getTraitInfo((TraitTypes)iI).getCommerceChange(iJ));
				changeCommerceRateModifier(((CommerceTypes)iJ), GC.getTraitInfo((TraitTypes)iI).getCommerceModifier(iJ));
			}

			for (iJ = 0; iJ < GC.getNumCivicOptionInfos(); iJ++)
			{
				if (GC.getCivicOptionInfo((CivicOptionTypes) iJ).getTraitNoUpkeep(iI))
				{
					changeNoCivicUpkeepCount(((CivicOptionTypes)iJ), 1);
				}
			}
		}
	}

	updateMaxAnarchyTurns();

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		updateExtraYieldThreshold((YieldTypes)iI);
	}
}
/************************************************************************************************/
/* CHANGE_PLAYER                           END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* CHANGE_PLAYER                          08/17/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for changing the personality of the player
//
void CvPlayer::changePersonalityType( )
{
	LeaderHeadTypes eBestPersonality;
	int iValue;
	int iBestValue;
	int iI, iJ;

	if (GC.getGameINLINE().isOption(GAMEOPTION_RANDOM_PERSONALITIES))
	{
		if (!isBarbarian())
		{
			iBestValue = 0;
			eBestPersonality = NO_LEADER;

			for (iI = 0; iI < GC.getNumLeaderHeadInfos(); iI++)
			{
				if (iI != GC.getDefineINT("BARBARIAN_LEADER")) // XXX minor civ???
				{
					iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Choosing Personality"));

					for (iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iJ).getPersonalityType() == ((LeaderHeadTypes)iI))
							{
								iValue /= 2;
							}
						}
					}

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						eBestPersonality = ((LeaderHeadTypes)iI);
					}
				}
			}

			if (eBestPersonality != NO_LEADER)
			{
				setPersonalityType(eBestPersonality);
			}
		}
	}
	else
	{
		setPersonalityType( getLeaderType() );
	}
}
/************************************************************************************************/
/* CHANGE_PLAYER                           END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* CHANGE_PLAYER                          08/17/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// reset state of event logic, unit prices
//
void CvPlayer::resetCivTypeEffects( )
{
	int iI;

	if( !isAlive() ) 
	{
		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), ((CivicTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationInitialCivics(iI))));
		}

		for (iI = 0; iI < GC.getNumEventInfos(); iI++)
		{
			resetEventOccured((EventTypes)iI, false);
		}

		for (iI = 0; iI < GC.getNumEventTriggerInfos(); iI++)
		{
			if( (!GC.getEventTriggerInfo((EventTriggerTypes)iI).isGlobal()) && (!GC.getEventTriggerInfo((EventTriggerTypes)iI).isTeam() || GET_TEAM(getTeam()).getNumMembers() == 1) )
			{
				resetTriggerFired((EventTriggerTypes)iI);
			}
		}
	}

	for (iI = 0; iI < GC.getNumUnitClassInfos(); ++iI)
	{
		UnitTypes eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI)));

		if (NO_UNIT != eUnit)
		{
			if (GC.getUnitInfo(eUnit).isFound())
			{
				setUnitExtraCost((UnitClassTypes)iI, getNewCityProductionValue());
			}
		}
	}
}
/************************************************************************************************/
/* CHANGE_PLAYER                           END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* CHANGE_PLAYER                          08/17/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for switching the leaderhead of this player
//
void CvPlayer::changeLeader( LeaderHeadTypes eNewLeader )
{
	LeaderHeadTypes eOldLeader = getLeaderType();

	if( eOldLeader == eNewLeader )
		return;

	// Clear old traits
	clearTraitBonuses();

	GC.getInitCore().setLeader( getID(), eNewLeader );

	// Add new traits
	addTraitBonuses();

	// Set new personality
	changePersonalityType();

	if( isAlive() || isEverAlive() )
	{
		gDLL->getInterfaceIFace()->setDirty(HighlightPlot_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
	}

	AI_init();
}
/************************************************************************************************/
/* CHANGE_PLAYER                           END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* CHANGE_PLAYER                          05/09/09                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for changing the civilization of this player
//
void CvPlayer::changeCiv( CivilizationTypes eNewCiv )
{
	CivilizationTypes eOldCiv = getCivilizationType();
	PlayerColorTypes eColor = (PlayerColorTypes)GC.getCivilizationInfo(eNewCiv).getDefaultPlayerColor();

	if( eOldCiv == eNewCiv )
		return;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (eColor == NO_PLAYERCOLOR || (GET_PLAYER((PlayerTypes)iI).getPlayerColor() == eColor && iI != getID()) )
		{
			for (int iK = 0; iK < GC.getNumPlayerColorInfos(); iK++)
			{
				if (iK != GC.getCivilizationInfo((CivilizationTypes)GC.getDefineINT("BARBARIAN_CIVILIZATION")).getDefaultPlayerColor())
				{
					bool bValid = true;

					for (int iL = 0; iL < MAX_CIV_PLAYERS; iL++)
					{
						if (GET_PLAYER((PlayerTypes)iL).getPlayerColor() == iK)
						{
							bValid = false;
							break;
						}
					}

					if (bValid)
					{
						eColor = (PlayerColorTypes)iK;
						iI = MAX_CIV_PLAYERS;
						break;
					}
				}
			}
		}
	}

	GC.getInitCore().setCiv( getID(), eNewCiv );
	GC.getInitCore().setColor( getID(), eColor );

	resetCivTypeEffects();

	if( isAlive() )
	{
		// if the player is alive and showing on scoreboard, etc
		// change colors, graphics, flags, units
		GC.getInitCore().setFlagDecal( getID(), (CvWString)GC.getCivilizationInfo(eNewCiv).getFlagTexture() );
		GC.getInitCore().setArtStyle( getID(), (ArtStyleTypes)GC.getCivilizationInfo(eNewCiv).getArtStyleType() );

		// Forces update of units flags
		EraTypes eEra = getCurrentRealEra(); // LFGR_TODO: Non-real era?
		bool bAuto = m_bDisableHuman;
		m_bDisableHuman = true;
		//setCurrentEra((EraTypes)((eEra + 1)%GC.getNumEraInfos()));
		setCurrentEra((EraTypes)0);
		setCurrentEra((EraTypes)(GC.getNumEraInfos() - 1));

		setCurrentEra(eEra);
		m_bDisableHuman = bAuto;
		gDLL->getInterfaceIFace()->makeInterfaceDirty();
		

		int iLoop;
		CvCity* pLoopCity;
		// dirty all of this player's cities...
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getOwnerINLINE() == getID())
			{
				pLoopCity->setLayoutDirty(true);
			}
		}

		//update unit eras
		CvUnit* pLoopUnit;
		CvPlot* pLoopPlot;
		for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			pLoopUnit->reloadEntity();
			pLoopPlot = pLoopUnit->plot();
/*
			if( pLoopPlot != NULL )
			{
				
				CvFlagEntity* pFlag = pLoopPlot->getFlagSymbol();

				if( pFlag != NULL )
				{

					if( gDLL->getFlagEntityIFace()->getPlayer(pFlag) == getID() )
					{
						gDLL->getFlagEntityIFace()->destroy(pFlag);
						CvFlagEntity* pNewFlag = gDLL->getFlagEntityIFace()->create(getID());
						if (pFlag != NULL)
						{
							gDLL->getFlagEntityIFace()->setPlot(pNewFlag, pLoopPlot, false);
						}

						gDLL->getFlagEntityIFace()->updateGraphicEra(pNewFlag);
					}

				}
				
				pLoopPlot->setFlagDirty(true);
				//pLoopPlot->updateGraphicEra();
			}
*/
		}

		//update flag eras
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Soundtrack_DIRTY_BIT, true);
		}

		gDLL->getInterfaceIFace()->makeInterfaceDirty();

		// Need to force redraw
		gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(GlobePartialTexture_DIRTY_BIT, true);

		gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(HighlightPlot_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
		gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(SelectionSound_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GlobeInfo_DIRTY_BIT, true);
	}
	else if( isEverAlive() )
	{
		// Not currently alive, but may show on some people's scoreboard
		// or graphs
		// change colors
		gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}

	setupGraphical();
}
/************************************************************************************************/
/* CHANGE_PLAYER                           END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* CHANGE_PLAYER                          08/17/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for changing whether this player is human or not
//
void CvPlayer::setIsHuman( bool bNewValue )
{
	if( bNewValue == isHuman() )
		return;

	if( bNewValue )
		GC.getInitCore().setSlotStatus( getID(), SS_TAKEN );
	else
		GC.getInitCore().setSlotStatus( getID(), SS_COMPUTER ); // or SS_OPEN for multiplayer?

}
/************************************************************************************************/
/* CHANGE_PLAYER                          END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for setting status of player to rebel, which affords some benefits
//
void CvPlayer::setIsRebel( bool bNewValue )
{
	if( bNewValue == isRebel() )
		return;
	else
		m_bRebel = bNewValue;
}

bool CvPlayer::isRebel() const
{
	return m_bRebel;
}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* REVOLUTION_MOD                         06/11/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
int CvPlayer::getStabilityIndex( ) const
{
	return m_iStabilityIndex;
}

void CvPlayer::setStabilityIndex( int iNewValue )
{
	m_iStabilityIndex = range(iNewValue,0,1000);
}

void CvPlayer::changeStabilityIndex( int iChange )
{
	setStabilityIndex( getStabilityIndex() + iChange );
}

int CvPlayer::getStabilityIndexAverage( ) const
{
	return m_iStabilityIndexAverage;
}

void CvPlayer::setStabilityIndexAverage( int iNewValue )
{
	m_iStabilityIndexAverage = range(iNewValue,0,1000);
}

void CvPlayer::updateStabilityIndexAverage( )
{
	setStabilityIndexAverage( (2*getStabilityIndexAverage() + getStabilityIndex())/3 );
}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

//////////////////////////////////////
// graphical only setup
//////////////////////////////////////
void CvPlayer::setupGraphical()
{
	if (!GC.IsGraphicsInitialized())
		return;

	CvCity* pLoopCity;
	CvUnit* pLoopUnit;

	// Setup m_cities
	int iLoop;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->setupGraphical();
	}

	// Setup m_units
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		pLoopUnit->setupGraphical();
	}
}


void CvPlayer::initFreeState()
{
	setGold(0);
	changeGold(GC.getHandicapInfo(getHandicapType()).getStartingGold());
	changeGold(GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingGold());

//FfH Traits: Added by Kael 08/02/2007
    changeGold(getStartingGold());
//FfH: End Add

	clearResearchQueue();
}


void CvPlayer::initFreeUnits()
{
	UnitTypes eLoopUnit;
	int iFreeCount;
	int iI, iJ;

	if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_START) && !isBarbarian())
	{
		int iPoints = GC.getGameINLINE().getNumAdvancedStartPoints();

		iPoints *= GC.getHandicapInfo(getHandicapType()).getAdvancedStartPointsMod();
		iPoints /= 100;

		if (!isHuman())
		{
			iPoints *= GC.getHandicapInfo(getHandicapType()).getAIAdvancedStartPercent();
			iPoints /= 100;
		}

		setAdvancedStartPoints(iPoints);

		// Starting visibility
		CvPlot* pStartingPlot = getStartingPlot();
		if (NULL != pStartingPlot)
		{
			for (int iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); ++iPlotLoop)
			{
				CvPlot* pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

				if (plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE()) <= GC.getDefineINT("ADVANCED_START_SIGHT_RANGE"))
				{
					pPlot->setRevealed(getTeam(), true, false, NO_TEAM, false);
				}
			}
		}
	}
	else
	{
		for (iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
		{
			eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);

			if (eLoopUnit != NO_UNIT)
			{
				iFreeCount = GC.getCivilizationInfo(getCivilizationType()).getCivilizationFreeUnitsClass(iI);

				// dont increase unit count if it's a World Unit (ie Lucian)
				if  (!isWorldUnitClass((UnitClassTypes)GC.getUnitInfo((UnitTypes)eLoopUnit).getUnitClassType()))
				{
					iFreeCount *= (GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingUnitMultiplier() + ((!isHuman()) ? GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingUnitMultiplier() : 0));
				}

				for (iJ = 0; iJ < iFreeCount; iJ++)
				{
					addFreeUnit(eLoopUnit);
				}
			}
		}

		iFreeCount = GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingDefenseUnits();
		iFreeCount += GC.getHandicapInfo(getHandicapType()).getStartingDefenseUnits();

		if (!isHuman())
		{
			iFreeCount += GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingDefenseUnits();
		}

		if (iFreeCount > 0)
		{
			addFreeUnitAI(UNITAI_CITY_DEFENSE, iFreeCount);
		}

		iFreeCount = GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingWorkerUnits();
		iFreeCount += GC.getHandicapInfo(getHandicapType()).getStartingWorkerUnits();

		if (!isHuman())
		{
			iFreeCount += GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingWorkerUnits();
		}

		if (iFreeCount > 0)
		{
			addFreeUnitAI(UNITAI_WORKER, iFreeCount);
		}

		iFreeCount = GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingExploreUnits();
		iFreeCount += GC.getHandicapInfo(getHandicapType()).getStartingExploreUnits();

		if (!isHuman())
		{
			iFreeCount += GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingExploreUnits();
		}

		if (iFreeCount > 0)
		{
			addFreeUnitAI(UNITAI_EXPLORE, iFreeCount);
		}
	}
}


/************************************************************************************************/
/* LoR                                        11/03/10                          phungus420      */
/*                                                                                              */
/* Colonists                                                                                    */
/************************************************************************************************/
UnitTypes CvPlayer::getBestUnitType(UnitAITypes eUnitAI) const
{
	UnitTypes eLoopUnit;
	UnitTypes eBestUnit = NO_UNIT;
	bool bValid;
	int iValue;
	int iBestValue = 0;
	int iI, iJ;

	for (iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
	{
		eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);

		if (eLoopUnit != NO_UNIT)
		{
			if (canTrain(eLoopUnit))
			{
				bValid = true;

				if (GC.getUnitInfo(eLoopUnit).getPrereqAndBonus() != NO_BONUS)
				{
					bValid = false;
				}

				for (iJ = 0; iJ < GC.getNUM_UNIT_PREREQ_OR_BONUSES(); iJ++)
				{
					if (GC.getUnitInfo(eLoopUnit).getPrereqOrBonuses(iJ) != NO_BONUS)
					{
						bValid = false;
					}
				}

				if (bValid)
				{
					iValue = AI_unitValue(eLoopUnit, eUnitAI, NULL);

					if (iValue > iBestValue)
					{
						eBestUnit = eLoopUnit;
						iBestValue = iValue;
					}
				}
			}
		}
	}

	return eBestUnit;
}
/************************************************************************************************/
/* LoR                            END                                                           */
/************************************************************************************************/


void CvPlayer::addFreeUnitAI(UnitAITypes eUnitAI, int iCount)
{
	UnitTypes eLoopUnit;
	UnitTypes eBestUnit;
	bool bValid;
	int iValue;
	int iBestValue;
	int iI, iJ;

	eBestUnit = NO_UNIT;
	iBestValue = 0;

	for (iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
	{
		eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);

		if (eLoopUnit != NO_UNIT)
		{
			if (canTrain(eLoopUnit)

//FfH: Added by Kael 07/30/2009
              && !isWorldUnitClass((UnitClassTypes)iI)
//FfH: End Add

			)
			{
				bValid = true;

				if (GC.getUnitInfo(eLoopUnit).getPrereqAndBonus() != NO_BONUS)
				{
					bValid = false;
				}

				for (iJ = 0; iJ < GC.getNUM_UNIT_PREREQ_OR_BONUSES(); iJ++)
				{
					if (GC.getUnitInfo(eLoopUnit).getPrereqOrBonuses(iJ) != NO_BONUS)
					{
						bValid = false;
					}
				}

				if (bValid)
				{
					iValue = AI_unitValue(eLoopUnit, eUnitAI, NULL);

					if (iValue > iBestValue)
					{
						eBestUnit = eLoopUnit;
						iBestValue = iValue;
					}
				}
			}
		}
	}

	if (eBestUnit != NO_UNIT)
	{
		for (iI = 0; iI < iCount; iI++)
		{
			addFreeUnit(eBestUnit, eUnitAI);
		}
	}
}


void CvPlayer::addFreeUnit(UnitTypes eUnit, UnitAITypes eUnitAI)
{
	CvPlot* pStartingPlot;
	CvPlot* pBestPlot;
	CvPlot* pLoopPlot;
	int iRandOffset;
	int iI;

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		if ((eUnitAI == UNITAI_SETTLE) || (GC.getUnitInfo(eUnit).getDefaultUnitAIType() == UNITAI_SETTLE))
		{
			if (AI_getNumAIUnits(UNITAI_SETTLE) >= 1)
			{
				return;
			}
		}
	}

	pStartingPlot = getStartingPlot();

	// MNAI - Puppet States - used for adding units to a newly created Puppet State
	if (pStartingPlot == NULL)
	{
		if (getCapitalCity() != NULL)
		{
			pStartingPlot = getCapitalCity()->plot();
		}
	}
	// MNAI - End Puppet States

	if (pStartingPlot != NULL)
	{
		pBestPlot = NULL;

		if (isHuman())
		{
			long lResult=0;
			gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "startHumansOnSameTile", NULL, &lResult);
			if (lResult == 0)
			{
				if (!(GC.getUnitInfo(eUnit).isFound()))
				{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
/*
					iRandOffset = GC.getGameINLINE().getSorenRandNum(NUM_CITY_PLOTS, "Place Units (Player)");
					for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
					{
						pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), ((iI + iRandOffset) % NUM_CITY_PLOTS));
*/
					const int iNextCityPlots = ::calculateNumCityPlots(getNextCityRadius());

					iRandOffset = GC.getGameINLINE().getSorenRandNum(iNextCityPlots, "Place Units (Player)");
					for (iI = 0; iI < iNextCityPlots; iI++)
					{
						pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), ((iI + iRandOffset) % iNextCityPlots));
//<<<<Unofficial Bug Fix: End Modify

						if (pLoopPlot != NULL)
						{
							if (pLoopPlot->getArea() == pStartingPlot->getArea())
							{
								if (!(pLoopPlot->isImpassable()))
								{
									if (!(pLoopPlot->isUnit()))
									{

//FfH: Modified by Kael 09/16/2008
//										if (!(pLoopPlot->isGoody()))
										if (pLoopPlot->getImprovementType() == NO_IMPROVEMENT)
//FfH: End Modify

										{
											pBestPlot = pLoopPlot;
											break;
										}
									}
								}
							}
						}
					}
				}
			}
		}

		if (pBestPlot == NULL)
		{
			pBestPlot = pStartingPlot;
		}

//FfH: Modified by Kael 08/13/2007
//		initUnit(eUnit, pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), eUnitAI);
        CvUnit* pUnit = initUnit(eUnit, pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), eUnitAI);
        if (GC.getUnitInfo(eUnit).getDefaultUnitAIType() == UNITAI_SETTLE)
        {
            if (GC.getDefineINT("STARTING_SETTLER_PROMOTION") != NO_PROMOTION)
            {
                pUnit->setHasPromotion((PromotionTypes)GC.getDefineINT("STARTING_SETTLER_PROMOTION"), true);
            }
        }
//FfH: End Add

	}
}


int CvPlayer::startingPlotRange() const
{
	int iRange;

	iRange = (GC.getMapINLINE().maxStepDistance() + 10);

	iRange *= GC.getDefineINT("STARTING_DISTANCE_PERCENT");
	iRange /= 100;

	iRange *= (GC.getMapINLINE().getLandPlots() / (GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getTargetNumCities() * GC.getGameINLINE().countCivPlayersAlive()));

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	iRange /= NUM_CITY_PLOTS;
	iRange /= ::calculateNumCityPlots(getNextCityRadius());
//<<<<Unofficial Bug Fix: End Modify

	iRange += std::min(((GC.getMapINLINE().getNumAreas() + 1) / 2), GC.getGameINLINE().countCivPlayersAlive());

	long lResult=0;
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "minStartingDistanceModifier", NULL, &lResult))
	{
		iRange *= std::max<int>(0, (lResult + 100));
		iRange /= 100;
	}

	return std::max(iRange, GC.getDefineINT("MIN_CIV_STARTING_DISTANCE"));
}


bool CvPlayer::startingPlotWithinRange(CvPlot* pPlot, PlayerTypes ePlayer, int iRange, int iPass) const
{
	PROFILE_FUNC();

	//XXX changes to AI_foundValue (which are far more flexible) make this function
	//    redundant but it is still called from Python.
	return false;
}

int CvPlayer::startingPlotDistanceFactor(CvPlot* pPlot, PlayerTypes ePlayer, int iRange) const
{
	PROFILE_FUNC();

	FAssert(ePlayer != getID());

	CvPlot* pStartingPlot;

	int iValue = 1000;

	pStartingPlot = getStartingPlot();

	if (pStartingPlot != NULL)
	{
		if (GC.getGameINLINE().isTeamGame())
		{
			if (GET_PLAYER(ePlayer).getTeam() == getTeam())
			{
				iRange *= GC.getDefineINT("OWN_TEAM_STARTING_MODIFIER");
				iRange /= 100;
			}
			else
			{
				iRange *= GC.getDefineINT("RIVAL_TEAM_STARTING_MODIFIER");
				iRange /= 100;
			}
		}

		int iDistance = stepDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE());
		if (pStartingPlot->getArea() != pPlot->getArea())
		{
			iDistance *= 4;
			iDistance /= 3;
		}

		iValue *= iDistance;
		iValue /= iRange ;

	}

	return std::max(1, iValue);

}


// Returns the id of the best area, or -1 if it doesn't matter:
int CvPlayer::findStartingArea() const
{
	PROFILE_FUNC();

	long result = -1;
	CyArgsList argsList;
	argsList.add(getID());		// pass in this players ID
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "findStartingArea", argsList.makeFunctionArgs(), &result))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl()) // Python override
		{
			if (result == -1 || GC.getMapINLINE().getArea(result) != NULL)
			{
				return result;
			}
			else
			{
				FAssertMsg(false, "python findStartingArea() must return -1 or the ID of a valid area");
			}
		}
	}

	int iBestValue = 0;
	int iBestArea = -1;
	int iValue;
	int iLoop = 0;

	CvArea *pLoopArea = NULL;

	// find best land area
	for(pLoopArea = GC.getMapINLINE().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoop))
	{
		if (!(pLoopArea->isWater()))
		{
			// iNumPlayersOnArea is the number of players starting on the area, plus this player
			int iNumPlayersOnArea = (pLoopArea->getNumStartingPlots() + 1);
			int iTileValue = ((pLoopArea->calculateTotalBestNatureYield() + (pLoopArea->countCoastalLand() * 2) + pLoopArea->getNumRiverEdges() + (pLoopArea->getNumTiles())) + 1);
			iValue = iTileValue / iNumPlayersOnArea;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
/*
			iValue *= std::min(NUM_CITY_PLOTS + 1, pLoopArea->getNumTiles() + 1);
			iValue /= (NUM_CITY_PLOTS + 1);
*/
			const int iNextCityPlots = ::calculateNumCityPlots(getNextCityRadius());

			iValue *= std::min(iNextCityPlots + 1, pLoopArea->getNumTiles() + 1);
			iValue /= (iNextCityPlots + 1);
//<<<<Unofficial Bug Fix: End Modify

			if (iNumPlayersOnArea <= 2)
			{
				iValue *= 4;
				iValue /= 3;
			}

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				iBestArea = pLoopArea->getID();
			}
		}
	}

	return iBestArea;
}


CvPlot* CvPlayer::findStartingPlot(bool bRandomize)
{
	PROFILE_FUNC();

	long result = -1;
	CyArgsList argsList;
	argsList.add(getID());		// pass in this players ID
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "findStartingPlot", argsList.makeFunctionArgs(), &result))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl()) // Python override
		{
			CvPlot *pPlot = GC.getMapINLINE().plotByIndexINLINE(result);
			if (pPlot != NULL)
			{
				return pPlot;
			}
			else
			{
				FAssertMsg(false, "python findStartingPlot() returned an invalid plot index!");
			}
		}
	}

	CvPlot* pLoopPlot;
	bool bValid;
	int iBestArea = -1;
	int iValue;
	int iRange;
	int iI;

	bool bNew = false;
	if (getStartingPlot() != NULL)
	{
		iBestArea = getStartingPlot()->getArea();
		setStartingPlot(NULL, true);
		bNew = true;
	}

	AI_updateFoundValues(true);//this sets all plots found values to -1

	if (!bNew)
	{
		iBestArea = findStartingArea();
	}

	iRange = startingPlotRange();
	for(int iPass = 0; iPass < GC.getMapINLINE().maxPlotDistance(); iPass++)
	{
		CvPlot *pBestPlot = NULL;
		int iBestValue = 0;

		for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
		{
			pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

			if ((iBestArea == -1) || (pLoopPlot->getArea() == iBestArea))
			{
				//the distance factor is now done inside foundValue
				iValue = pLoopPlot->getFoundValue(getID());

				if (bRandomize && iValue > 0)
				{
					iValue += GC.getGameINLINE().getSorenRandNum(10000, "Randomize Starting Location");
				}

				if (iValue > iBestValue)
				{
					bValid = true;

					if (bValid)
					{
						iBestValue = iValue;
						pBestPlot = pLoopPlot;
					}
				}
			}
		}

		if (pBestPlot != NULL)
		{
			return pBestPlot;
		}

		FAssertMsg(iPass != 0, "CvPlayer::findStartingPlot - could not find starting plot in first pass.");
	}

	FAssertMsg(false, "Could not find starting plot.");
	return NULL;
}


CvPlotGroup* CvPlayer::initPlotGroup(CvPlot* pPlot)
{
	CvPlotGroup* pPlotGroup;

	pPlotGroup = addPlotGroup();

	FAssertMsg(pPlotGroup != NULL, "PlotGroup is not assigned a valid value");

	pPlotGroup->init(pPlotGroup->getID(), getID(), pPlot);

	return pPlotGroup;
}


CvCity* CvPlayer::initCity(int iX, int iY, bool bBumpUnits, bool bUpdatePlotGroups)
{
	PROFILE_FUNC();

	CvCity* pCity;

	pCity = addCity();

	FAssertMsg(pCity != NULL, "City is not assigned a valid value");
	FAssertMsg(!(GC.getMapINLINE().plotINLINE(iX, iY)->isCity()), "No city is expected at this plot when initializing new city");

	pCity->init(pCity->getID(), getID(), iX, iY, bBumpUnits, bUpdatePlotGroups);

	return pCity;
}


void CvPlayer::acquireCity(CvCity* pOldCity, bool bConquest, bool bTrade, bool bUpdatePlotGroups)
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* Copy over city data                                                                          */
/************************************************************************************************/
	std::string scriptData;
	int iRevIdx;
	int iLocalRevIdx;
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

	CLLNode<IDInfo>* pUnitNode;
	CvCity* pNewCity;
	CvUnit* pLoopUnit;
	CvPlot* pCityPlot;
	CvPlot* pLoopPlot;
	bool* pabHasReligion;
	bool* pabHolyCity;
	bool* pabHasCorporation;
	bool* pabHeadquarters;
	int* paiNumRealBuilding;
	int* paiBuildingOriginalOwner;
	int* paiBuildingOriginalTime;
	CvWString szBuffer;
	CvWString szName;
	CvWString szTempBuffer; // MNAI - Puppet States
	bool abEverOwned[MAX_PLAYERS];
	int aiCulture[MAX_PLAYERS];
/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
	int aiOriginalPopulation[MAX_PLAYERS];
/*************************************************************************************************/
/** Advanced Diplomacy       END                                                  			 */
/*************************************************************************************************/
	PlayerTypes eOldOwner;
	PlayerTypes eOriginalOwner;
	PlayerTypes eHighestCulturePlayer;
	BuildingTypes eBuilding;
	bool bRecapture;
	bool bRaze;
	bool bGift;
	int iRange;
	int iCaptureGold;
	int iGameTurnFounded;
	int iPopulation;
	int iHighestPopulation;
	int iHurryAngerTimer;
	int iConscriptAngerTimer;
	int iDefyResolutionAngerTimer;
	int iOccupationTimer;
	int iTeamCulturePercent;
	int iDamage;
	int iDX, iDY;
	int iI;
	CLinkList<IDInfo> oldUnits;
	std::vector<int> aeFreeSpecialists;

	pCityPlot = pOldCity->plot();

	pUnitNode = pCityPlot->headUnitNode();

	while (pUnitNode != NULL)
	{
		oldUnits.insertAtEnd(pUnitNode->m_data);
		pUnitNode = pCityPlot->nextUnitNode(pUnitNode);
	}

	pUnitNode = oldUnits.head();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = oldUnits.next(pUnitNode);

		if (pLoopUnit && pLoopUnit->getTeam() != getTeam())
		{
			if (pLoopUnit->getDomainType() == DOMAIN_IMMOBILE)
			{
				logBBAI("    Killing %S -- immobile in acquired city (Unit %d - plot: %d, %d)",
						pLoopUnit->getName().GetCString(), pLoopUnit->getID(), pLoopUnit->getX(), pLoopUnit->getY());
				pLoopUnit->kill(false, getID());
			}
		}
	}

	if (bConquest)
	{
		iRange = pOldCity->getCultureLevel();

		for (iDX = -(iRange); iDX <= iRange; iDX++)
		{
			for (iDY = -(iRange); iDY <= iRange; iDY++)
			{
				if (pOldCity->cultureDistance(iDX, iDY) <= iRange)
				{
					pLoopPlot = plotXY(pOldCity->getX_INLINE(),pOldCity-> getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot->getOwnerINLINE() == pOldCity->getOwnerINLINE())
						{
							if (pLoopPlot->getNumCultureRangeCities(pOldCity->getOwnerINLINE()) == 1)
							{
								bool bForceUnowned = false;

								for (iI = 0; iI < MAX_PLAYERS; iI++)
								{
									if (GET_PLAYER((PlayerTypes)iI).isAlive())
									{
										if ((GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam()) && (GET_PLAYER((PlayerTypes)iI).getTeam() != pOldCity->getTeam()))
										{
											if (pLoopPlot->getNumCultureRangeCities((PlayerTypes)iI) > 0)
											{
												bForceUnowned = true;
												break;
											}
										}
									}
								}

								if (bForceUnowned)
								{
									pLoopPlot->setForceUnownedTimer(GC.getDefineINT("FORCE_UNOWNED_CITY_TIMER"));
								}
							}
						}
					}
				}
			}
		}
	}

	if (pOldCity->getOriginalOwner() == pOldCity->getOwnerINLINE())
	{
		GET_PLAYER(pOldCity->getOriginalOwner()).changeCitiesLost(1);
	}
	else if (pOldCity->getOriginalOwner() == getID())
	{
		GET_PLAYER(pOldCity->getOriginalOwner()).changeCitiesLost(-1);
	}

	if (bConquest)
	{
		szBuffer = gDLL->getText("TXT_KEY_MISC_CAPTURED_CITY", pOldCity->getNameKey()).GetCString();
		gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYCAPTURE", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_GREEN"), pOldCity->getX_INLINE(), pOldCity->getY_INLINE(), true, true);

		szName.Format(L"%s (%s)", pOldCity->getName().GetCString(), GET_PLAYER(pOldCity->getOwnerINLINE()).getName());

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (iI != getID())
				{
					if (pOldCity->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
					{
						szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_CAPTURED_BY", szName.GetCString(), getCivilizationDescriptionKey());
						gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYCAPTURED", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pOldCity->getX_INLINE(), pOldCity->getY_INLINE(), true, true);
					}
				/************************************************************************************************/
				/* Advanced Diplomacy	                  Start		 12/9/09                                                */
				/************************************************************************************************/
					else if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isHasEmbassy(getTeam()))
					{
						szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_CAPTURED_BY", szName.GetCString(), getCivilizationDescriptionKey());
						gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYCAPTURED", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_RED"));
					}
				/************************************************************************************************/
				/* Advanced Diplomacy	                     END                                                            */
				/************************************************************************************************/
				}
			}
		}

		szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_WAS_CAPTURED_BY", szName.GetCString(), getCivilizationDescriptionKey());
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, pOldCity->getX_INLINE(), pOldCity->getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
	}

	iCaptureGold = 0;

	if (bConquest)
	{
		long lCaptureGold;
		// Use python to determine city capture gold amounts...
		lCaptureGold = 0;

		CyCity* pyOldCity = new CyCity(pOldCity);

		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyOldCity));	// pass in plot class

		gDLL->getPythonIFace()->callFunction(PYGameModule, "doCityCaptureGold", argsList.makeFunctionArgs(),&lCaptureGold);

		delete pyOldCity;	// python fxn must not hold on to this pointer

		iCaptureGold = (int)lCaptureGold;
	}

	changeGold(iCaptureGold);

	pabHasReligion = new bool[GC.getNumReligionInfos()];
	pabHolyCity = new bool[GC.getNumReligionInfos()];
	pabHasCorporation = new bool[GC.getNumCorporationInfos()];
	pabHeadquarters = new bool[GC.getNumCorporationInfos()];
	paiNumRealBuilding = new int[GC.getNumBuildingInfos()];
	paiBuildingOriginalOwner = new int[GC.getNumBuildingInfos()];
	paiBuildingOriginalTime = new int[GC.getNumBuildingInfos()];

	for (iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
		pOldCity->processVoteSourceBonus((VoteSourceTypes)iI, false);
	}

	eOldOwner = pOldCity->getOwnerINLINE();
	eOriginalOwner = pOldCity->getOriginalOwner();
	eHighestCulturePlayer = pOldCity->findHighestCulture();
	iGameTurnFounded = pOldCity->getGameTurnFounded();
	iPopulation = pOldCity->getPopulation();
	iHighestPopulation = pOldCity->getHighestPopulation();
	iHurryAngerTimer = pOldCity->getHurryAngerTimer();
	iConscriptAngerTimer = pOldCity->getConscriptAngerTimer();
	iDefyResolutionAngerTimer = pOldCity->getDefyResolutionAngerTimer();
	iOccupationTimer = pOldCity->getOccupationTimer();
	szName = pOldCity->getNameKey();
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	scriptData = pOldCity->getScriptData();
	iRevIdx = pOldCity->getRevolutionIndex();
	iLocalRevIdx = pOldCity->getLocalRevIndex();
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	iDamage = pOldCity->getDefenseDamage();
	int iOldCityId = pOldCity->getID();

//FfH: Added by Kael 07/02/2008
	int iCiv = pOldCity->getTrueCivilizationType();
	if (iCiv == GC.getDefineINT("BARBARIAN_CIVILIZATION"))
	{
		iCiv = NO_CIVILIZATION;
	}
//FfH: End Add

	for (iI = 0; iI < GC.getNumSpecialistInfos(); ++iI)
	{
		aeFreeSpecialists.push_back(pOldCity->getAddedFreeSpecialistCount((SpecialistTypes)iI));
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		abEverOwned[iI] = pOldCity->isEverOwned((PlayerTypes)iI);
		aiCulture[iI] = pOldCity->getCultureTimes100((PlayerTypes)iI);
/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
		aiOriginalPopulation[iI] = pOldCity->getOriginalPopulation((PlayerTypes)iI);
/*************************************************************************************************/
/** Advanced Diplomacy       END                                                  			 */
/*************************************************************************************************/
	}

	abEverOwned[getID()] = true;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		pabHasReligion[iI] = pOldCity->isHasReligion((ReligionTypes)iI);
		pabHolyCity[iI] = pOldCity->isHolyCity((ReligionTypes)iI);
	}

	for (iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		pabHasCorporation[iI] = pOldCity->isHasCorporation((CorporationTypes)iI);
		pabHeadquarters[iI] = pOldCity->isHeadquarters((CorporationTypes)iI);
	}

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		paiNumRealBuilding[iI] = pOldCity->getNumRealBuilding((BuildingTypes)iI);
		paiBuildingOriginalOwner[iI] = pOldCity->getBuildingOriginalOwner((BuildingTypes)iI);
		paiBuildingOriginalTime[iI] = pOldCity->getBuildingOriginalTime((BuildingTypes)iI);
	}

	std::vector<BuildingYieldChange> aBuildingYieldChange;
	std::vector<BuildingCommerceChange> aBuildingCommerceChange;
	BuildingChangeArray aBuildingHappyChange;
	BuildingChangeArray aBuildingHealthChange;
	for (iI = 0; iI < GC.getNumBuildingClassInfos(); ++iI)
	{
		for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
		{
			BuildingYieldChange kChange;
			kChange.eBuildingClass = (BuildingClassTypes)iI;
			kChange.eYield = (YieldTypes)iYield;
			kChange.iChange = pOldCity->getBuildingYieldChange((BuildingClassTypes)iI, (YieldTypes)iYield);
			if (0 != kChange.iChange)
			{
				aBuildingYieldChange.push_back(kChange);
			}
		}

		for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
		{
			BuildingCommerceChange kChange;
			kChange.eBuildingClass = (BuildingClassTypes)iI;
			kChange.eCommerce = (CommerceTypes)iCommerce;
			kChange.iChange = pOldCity->getBuildingCommerceChange((BuildingClassTypes)iI, (CommerceTypes)iCommerce);
			if (0 != kChange.iChange)
			{
				aBuildingCommerceChange.push_back(kChange);
			}
		}

		int iChange = pOldCity->getBuildingHappyChange((BuildingClassTypes)iI);
		if (0 != iChange)
		{
			aBuildingHappyChange.push_back(std::make_pair((BuildingClassTypes)iI, iChange));
		}

		iChange = pOldCity->getBuildingHealthChange((BuildingClassTypes)iI);
		if (0 != iChange)
		{
			aBuildingHealthChange.push_back(std::make_pair((BuildingClassTypes)iI, iChange));
		}
	}

	bRecapture = ((eHighestCulturePlayer != NO_PLAYER) ? (GET_PLAYER(eHighestCulturePlayer).getTeam() == getTeam()) : false);

//FfH: Added by Kael 09/21/2008
	if (GET_PLAYER(pOldCity->getOwner()).getNumCities() == 1)
	{
		changePlayersKilled(1);
	}
//FfH: End Add

	pOldCity->kill(false);

	if (bTrade)
	{
		for (iDX = -1; iDX <= 1; iDX++)
		{
			for (iDY = -1; iDY <= 1; iDY++)
			{
				pLoopPlot	= plotXY(pCityPlot->getX_INLINE(), pCityPlot->getY_INLINE(), iDX, iDY);

				if (pLoopPlot != NULL)
				{
					pLoopPlot->setCulture(eOldOwner, 0, false, false);
				}
			}
		}
	}

	pNewCity = initCity(pCityPlot->getX_INLINE(), pCityPlot->getY_INLINE(), !bConquest, false);

	FAssertMsg(pNewCity != NULL, "NewCity is not assigned a valid value");

/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
	if (!bRecapture)
	{
		pNewCity->setOriginalPopulation(eOldOwner, iPopulation);
	}
/*************************************************************************************************/
/** Advanced Diplomacy       END                                                 			 */
/*************************************************************************************************/
	pNewCity->setPreviousOwner(eOldOwner);
	pNewCity->setOriginalOwner(eOriginalOwner);
	pNewCity->setGameTurnFounded(iGameTurnFounded);
	pNewCity->setPopulation((bConquest && !bRecapture) ? std::max(1, (iPopulation - 1)) : iPopulation);
	pNewCity->setHighestPopulation(iHighestPopulation);
	pNewCity->setName(szName);
	pNewCity->setNeverLost(false);
	pNewCity->changeDefenseDamage(iDamage);

//FfH: Added by Kael 07/05/2008
	if (iCiv != NO_CIVILIZATION)
	{
		pNewCity->setCivilizationType(iCiv);
	}
//FfH: End Add

/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	pNewCity->setScriptData(scriptData);
	pNewCity->setRevolutionIndex( iRevIdx );
	pNewCity->setLocalRevIndex( iLocalRevIdx );
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		pNewCity->setEverOwned(((PlayerTypes)iI), abEverOwned[iI]);
		pNewCity->setCultureTimes100(((PlayerTypes)iI), aiCulture[iI], false, false);
	}

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		int iNum = 0;

		if (paiNumRealBuilding[iI] > 0)
		{
//>>>>Unofficial Bug Fix: Added by Denev 2010/02/26
//*** Unique buildings can not be kept by other civilization.
			const CivilizationTypes ePrereqCiv = (CivilizationTypes)GC.getBuildingInfo((BuildingTypes)iI).getPrereqCiv();
			if (ePrereqCiv == NO_CIVILIZATION || ePrereqCiv == pNewCity->getCivilizationType() || isAssimilation())
			{
//<<<<Unofficial Bug Fix: End Add
				BuildingClassTypes eBuildingClass = (BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType();
				if (::isWorldWonderClass(eBuildingClass))
				{
					eBuilding = (BuildingTypes)iI;
				}
				else
				{
					eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
				}

			if (eBuilding != NO_BUILDING)
			{
				if (bTrade || !(GC.getBuildingInfo((BuildingTypes)iI).isNeverCapture()))
				{
					if (!isProductionMaxedBuildingClass(((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())), true))
					{
						if (pNewCity->isValidBuildingLocation(eBuilding))
						{
							// MNAI - Revolutions - rebels have increased chance of keeping buildings if captured from civ they are rebelling against
							int iBuildingCaptureProb = GC.getBuildingInfo((BuildingTypes)iI).getConquestProbability();
							if (GET_TEAM(getTeam()).isRebelAgainst(GET_PLAYER(eOldOwner).getTeam()))
							{
								iBuildingCaptureProb *= 2;
							}
							// MNAI End

							if (!bConquest || bRecapture || GC.getGameINLINE().getSorenRandNum(100, "Capture Probability") < iBuildingCaptureProb)
							{
								iNum += paiNumRealBuilding[iI];
							}
						}
					}
				}

					pNewCity->setNumRealBuildingTimed(eBuilding, std::min(pNewCity->getNumRealBuilding(eBuilding) + iNum, GC.getCITY_MAX_NUM_BUILDINGS()), false, ((PlayerTypes)(paiBuildingOriginalOwner[iI])), paiBuildingOriginalTime[iI]);
				}
//>>>>Unofficial Bug Fix: Added by Denev 2010/02/26
//*** Unique buildings can not be kept by other civilization.
			}
//<<<<Unofficial Bug Fix: End Add
		}
	}

	for (std::vector<BuildingYieldChange>::iterator it = aBuildingYieldChange.begin(); it != aBuildingYieldChange.end(); ++it)
	{
		pNewCity->setBuildingYieldChange((*it).eBuildingClass, (*it).eYield, (*it).iChange);
	}

	for (std::vector<BuildingCommerceChange>::iterator it = aBuildingCommerceChange.begin(); it != aBuildingCommerceChange.end(); ++it)
	{
		pNewCity->setBuildingCommerceChange((*it).eBuildingClass, (*it).eCommerce, (*it).iChange);
	}

	for (BuildingChangeArray::iterator it = aBuildingHappyChange.begin(); it != aBuildingHappyChange.end(); ++it)
	{
		pNewCity->setBuildingHappyChange((*it).first, (*it).second);
	}

	for (BuildingChangeArray::iterator it = aBuildingHealthChange.begin(); it != aBuildingHealthChange.end(); ++it)
	{
		pNewCity->setBuildingHealthChange((*it).first, (*it).second);
	}

	for (iI = 0; iI < GC.getNumSpecialistInfos(); ++iI)
	{
		pNewCity->changeFreeSpecialistCount((SpecialistTypes)iI, aeFreeSpecialists[iI]);
	}

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (pabHasReligion[iI])
		{
			pNewCity->setHasReligion(((ReligionTypes)iI), true, false, true);
		}

		if (pabHolyCity[iI])
		{
			GC.getGameINLINE().setHolyCity(((ReligionTypes)iI), pNewCity, false);
		}
	}

	for (iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (pabHasCorporation[iI])
		{
			pNewCity->setHasCorporation(((CorporationTypes)iI), true, false);
		}

		if (pabHeadquarters[iI])
		{
			GC.getGameINLINE().setHeadquarters(((CorporationTypes)iI), pNewCity, false);
		}
	}

	if (bTrade)
	{
		if (isHuman() || (getTeam() == GET_PLAYER(eOldOwner).getTeam()))
		{
			pNewCity->changeHurryAngerTimer(iHurryAngerTimer);
			pNewCity->changeConscriptAngerTimer(iConscriptAngerTimer);
			pNewCity->changeDefyResolutionAngerTimer(iDefyResolutionAngerTimer);
		}

		if (!bRecapture)
		{
			pNewCity->changeOccupationTimer(iOccupationTimer);
		}
	}

	if (bConquest)
	{
		iTeamCulturePercent = pNewCity->calculateTeamCulturePercent(getTeam());

		if (iTeamCulturePercent < GC.getDefineINT("OCCUPATION_CULTURE_PERCENT_THRESHOLD"))
		{
			pNewCity->changeOccupationTimer(((GC.getDefineINT("BASE_OCCUPATION_TURNS") + ((pNewCity->getPopulation() * GC.getDefineINT("OCCUPATION_TURNS_POPULATION_PERCENT")) / 100)) * (100 - iTeamCulturePercent)) / 100);
		}

		GC.getMapINLINE().verifyUnitValidPlot();
	}

	pCityPlot->setRevealed(GET_PLAYER(eOldOwner).getTeam(), true, false, NO_TEAM, false);

	pNewCity->updateEspionageVisibility(false);

	if (bUpdatePlotGroups)
	{
		GC.getGameINLINE().updatePlotGroups();
	}

	CvEventReporter::getInstance().cityAcquired(eOldOwner, getID(), pNewCity, bConquest, bTrade);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/02/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
	if( gPlayerLogLevel >= 1 )
	{
		logBBAI("  %S acquires city %S bConq %d bTrade %d", getCivilizationDescription(0), pNewCity->getName(0).GetCString(), bConquest, bTrade );
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	SAFE_DELETE_ARRAY(pabHasReligion);
	SAFE_DELETE_ARRAY(pabHolyCity);
	SAFE_DELETE_ARRAY(pabHasCorporation);
	SAFE_DELETE_ARRAY(pabHeadquarters);
	SAFE_DELETE_ARRAY(paiNumRealBuilding);
	SAFE_DELETE_ARRAY(paiBuildingOriginalOwner);
	SAFE_DELETE_ARRAY(paiBuildingOriginalTime);

	// Sephi default value for avoid angry Citizens
	// lfgr 10/2020: Made optional, added unhealthy citizens
	if( GC.getInfoTypeForString("EMPHASIZE_AVOID_ANGRY_CITIZENS")!=NO_EMPHASIZE
			&& getBugOptionBOOL( "FfHUI__AvoidAngryCitizensDefault", true, "BUG_AVOID_ANGRY_CITIZENS_DEFAULT" ) ) {
		CvMessageControl::getInstance().sendDoTask(pNewCity->getID(), TASK_SET_EMPHASIZE, GC.getInfoTypeForString("EMPHASIZE_AVOID_ANGRY_CITIZENS"), -1, true, false, false, false);
	}
	if( GC.getInfoTypeForString("EMPHASIZE_AVOID_UNHEALTHY_CITIZENS")!=NO_EMPHASIZE
			&& getBugOptionBOOL( "FfHUI__AvoidUnhealthyCitizensDefault", false, "BUG_AVOID_UNHEALTHY_CITIZENS_DEFAULT" ) ) {
		CvMessageControl::getInstance().sendDoTask(pNewCity->getID(), TASK_SET_EMPHASIZE, GC.getInfoTypeForString("EMPHASIZE_AVOID_UNHEALTHY_CITIZENS"), -1, true, false, false, false);
	}

	if (bConquest)
	{
		CyCity* pyCity = new CyCity(pNewCity);
		CyArgsList argsList;
		argsList.add(getID());	// Player ID
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canRazeCity", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer

		if (lResult == 1)
		{
			//auto raze based on game rules
			if (pNewCity->isAutoRaze())
			{
				if (iCaptureGold > 0)
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_PILLAGED_CITY", iCaptureGold, pNewCity->getNameKey());
					gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYRAZE", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_GREEN"), pNewCity->getX_INLINE(), pNewCity->getY_INLINE(), true, true);
				}

				pNewCity->doTask(TASK_RAZE);
			}
			else if (!isHuman())
			{
				AI_conquerCity(pNewCity); // could delete the pointer...
			}
			else
			{
				//popup raze option
				eHighestCulturePlayer = pNewCity->getLiberationPlayer(true);
				bRaze = canRaze(pNewCity);
				bGift = ((eHighestCulturePlayer != NO_PLAYER)
						&& (eHighestCulturePlayer != getID())
						&& ((getTeam() == GET_PLAYER(eHighestCulturePlayer).getTeam())
							|| GET_TEAM(getTeam()).isOpenBorders(GET_PLAYER(eHighestCulturePlayer).getTeam())
							|| GET_TEAM(GET_PLAYER(eHighestCulturePlayer).getTeam()).isVassal(getTeam())));

				if (bRaze || bGift)
				{
					CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_RAZECITY);
					pInfo->setData1(pNewCity->getID());
					pInfo->setData2(eHighestCulturePlayer);
					pInfo->setData3(iCaptureGold);
					gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
				}
				else
				{
					pNewCity->chooseProduction();
					CvEventReporter::getInstance().cityAcquiredAndKept(getID(), pNewCity);
				}
			}
		}
	}
/************************************************************************************************/
/* REVOLUTION_MOD                         06/27/10                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/* original code
	else if (!bTrade)
*/
	// Silences double ask for accepting new city from Revolution mod
	else if (!bTrade && (!GC.getGameINLINE().isOption(GAMEOPTION_REVOLUTIONS)) )
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	{
		if (isHuman())
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DISBANDCITY);
			pInfo->setData1(pNewCity->getID());
			gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
		}
		else
		{
			CvEventReporter::getInstance().cityAcquiredAndKept(getID(), pNewCity);
		}
	}
	// Tholal AI - not sure why this wasnt being called for traded cities - they are acquired and kept also...
	else if (bTrade)
	{
		CvEventReporter::getInstance().cityAcquiredAndKept(getID(), pNewCity);
	}

	// Forcing events that deal with the old city not to expire just because we conquered that city
	for (CvEventMap::iterator it = m_mapEventsOccured.begin(); it != m_mapEventsOccured.end(); ++it)
	{
		EventTriggeredData &triggerData = it->second;
		if((triggerData.m_eOtherPlayer == eOldOwner) && (triggerData.m_iOtherPlayerCityId == iOldCityId))
		{
			triggerData.m_iOtherPlayerCityId = -1;
		}
	}
}


void CvPlayer::killCities()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->kill(false);
	}

	// Super Forts begin *culture* - Clears culture from forts when a player dies
	PlayerTypes ePlayer = getID();
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		if (pLoopPlot->getOwner() == ePlayer)
		{
			pLoopPlot->setOwner(pLoopPlot->calculateCulturalOwner(), true, false);
		}
	}
	// Super Forts end

	GC.getGameINLINE().updatePlotGroups();
}


CvWString CvPlayer::getNewCityName() const
{
	CLLNode<CvWString>* pNode;
	CvWString szName;
	int iI;

	for (pNode = headCityNameNode(); (pNode != NULL); pNode = nextCityNameNode(pNode))
	{
		szName = gDLL->getText(pNode->m_data);
		if (isCityNameValid(szName, true))
		{
			szName = pNode->m_data;
			break;
		}
	}

	if (szName.empty())
	{
		getCivilizationCityName(szName, getCivilizationType());
	}

	if (szName.empty())
	{
		// Pick a name from another random civ
		int iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumCivilizationInfos(), "Place Units (Player)");
		for (iI = 0; iI < GC.getNumCivilizationInfos(); iI++)
		{
			int iLoopName = ((iI + iRandOffset) % GC.getNumCivilizationInfos());

			getCivilizationCityName(szName, ((CivilizationTypes)iLoopName));

			if (!szName.empty())
			{
				break;
			}
		}
	}

	if (szName.empty())
	{
		szName = "TXT_KEY_CITY";
	}

	return szName;
}


void CvPlayer::getCivilizationCityName(CvWString& szBuffer, CivilizationTypes eCivilization) const
{
	int iRandOffset;
	int iLoopName;
	int iI;

/************************************************************************************************/
/* REVOLUTION_MOD                         02/29/08                                jdog5000      */
/*                                                                                              */
/* Minor Civs                                                                                   */
/************************************************************************************************/
/* original code
	if (isBarbarian() || isMinorCiv())
	{
		iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getCivilizationInfo(eCivilization).getNumCityNames(), "Place Units (Player)");
	}
	else
	{
		iRandOffset = 0;
	}
*/
	iRandOffset = 0;

	if( GC.getGameINLINE().isOption(GAMEOPTION_REVOLUTIONS))// || !GC.getGameINLINE().isOption(GAMEOPTION_NO_BARBARIANS) )
	{
		if( isBarbarian() )
		{
			iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getCivilizationInfo(eCivilization).getNumCityNames(), "Place Units (Player)");
		}
	}
	else 
	{
		if (isBarbarian() || isMinorCiv())
		{
			iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getCivilizationInfo(eCivilization).getNumCityNames(), "Place Units (Player)");
		}
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

	for (iI = 0; iI < GC.getCivilizationInfo(eCivilization).getNumCityNames(); iI++)
	{
		iLoopName = ((iI + iRandOffset) % GC.getCivilizationInfo(eCivilization).getNumCityNames());

		CvWString szName = gDLL->getText(GC.getCivilizationInfo(eCivilization).getCityNames(iLoopName));

		if (isCityNameValid(szName, true))
		{
			szBuffer = GC.getCivilizationInfo(eCivilization).getCityNames(iLoopName);
			break;
		}
	}
}


bool CvPlayer::isCityNameValid(CvWString& szName, bool bTestDestroyed) const
{
	CvCity* pLoopCity;
	int iLoop;

	if (bTestDestroyed)
	{
		if (GC.getGameINLINE().isDestroyedCityName(szName))
		{
			return false;
		}

		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
			for (pLoopCity = kLoopPlayer.firstCity(&iLoop); pLoopCity != NULL; pLoopCity = kLoopPlayer.nextCity(&iLoop))
			{
				if (pLoopCity->getName() == szName)
				{
					return false;
				}
			}
		}
	}
	else
	{
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getName() == szName)
			{
				return false;
			}
		}
	}

	return true;
}


/************************************************************************************************/
/* GP_NAMES                                 07/2013                                 lfgr        */
/* Added parameter eName                                                                        */
/************************************************************************************************/
/*
//>>>>Unofficial Bug Fix: Modified by Denev 2010/02/22
//CvUnit* CvPlayer::initUnit(UnitTypes eUnit, int iX, int iY, UnitAITypes eUnitAI, DirectionTypes eFacingDirection)
// lfgr 04/2014 bugfix
//CvUnit* CvPlayer::initUnit(UnitTypes eUnit, int iX, int iY, UnitAITypes eUnitAI, DirectionTypes eFacingDirection, bool bPushOutExistingUnit)
// lfgr end
//<<<<Unofficial Bug Fix: End Modify
*/
CvUnit* CvPlayer::initUnit(UnitTypes eUnit, int iX, int iY, UnitAITypes eUnitAI, DirectionTypes eFacingDirection, bool bPushOutExistingUnit, bool bGift, int eName)
/************************************************************************************************/
/* GP_NAMES                                END                                                  */
/************************************************************************************************/
{
	PROFILE_FUNC();

	FAssertMsg(eUnit != NO_UNIT, "Unit is not assigned a valid value");

	CvUnit* pUnit = addUnit();
	FAssertMsg(pUnit != NULL, "Unit is not assigned a valid value");
	if (NULL != pUnit)
	{
/************************************************************************************************/
/* GP_NAMES                                 07/2013                                 lfgr        */
/* Added parameter eName                                                                        */
/************************************************************************************************/
/*
//>>>>Unofficial Bug Fix: Modified by Denev 2010/02/22
//		pUnit->init(pUnit->getID(), eUnit, ((eUnitAI == NO_UNITAI) ? ((UnitAITypes)(GC.getUnitInfo(eUnit).getDefaultUnitAIType())) : eUnitAI), getID(), iX, iY, eFacingDirection);
// lfgr 04/2014 bugfix
//		pUnit->init(pUnit->getID(), eUnit, ((eUnitAI == NO_UNITAI) ? (UnitAITypes)GC.getUnitInfo(eUnit).getDefaultUnitAIType() : eUnitAI), getID(), iX, iY, eFacingDirection, bPushOutExistingUnit);
		pUnit->init(pUnit->getID(), eUnit, ((eUnitAI == NO_UNITAI) ? (UnitAITypes)GC.getUnitInfo(eUnit).getDefaultUnitAIType() : eUnitAI), getID(), iX, iY, eFacingDirection, bPushOutExistingUnit, bGift);
// lfgr end
//<<<<Unofficial Bug Fix: End Modify
*/
		pUnit->init(pUnit->getID(), eUnit, ((eUnitAI == NO_UNITAI) ? (UnitAITypes)GC.getUnitInfo(eUnit).getDefaultUnitAIType() : eUnitAI), getID(), iX, iY, eFacingDirection, bPushOutExistingUnit, bGift, eName);
/************************************************************************************************/
/* GP_NAMES                                END                                                  */
/************************************************************************************************/
	}

	return pUnit;
}


void CvPlayer::disbandUnit(bool bAnnounce)
{
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;
	wchar szBuffer[1024];
	int iValue;
	int iBestValue;
	int iLoop;

	iBestValue = MAX_INT;
	pBestUnit = NULL;

	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (!(pLoopUnit->hasCargo())

//FfH: Added by Kael 11/24/2007
          && pLoopUnit->getUnitInfo().isMilitarySupport()
//FfH: End Add

		  )
		{
			if (!(pLoopUnit->isGoldenAge()))
			{
				if (pLoopUnit->getUnitInfo().getProductionCost() > 0)
				{
					if (!(pLoopUnit->isMilitaryHappiness()) || !(pLoopUnit->plot()->isCity()) || (pLoopUnit->plot()->plotCount(PUF_isMilitaryHappiness, -1, -1, getID()) > 1))
					{
						iValue = (10000 + GC.getGameINLINE().getSorenRandNum(1000, "Disband Unit"));

						iValue += (pLoopUnit->getUnitInfo().getProductionCost() * 5);

						iValue += (pLoopUnit->getExperience() * 20);
						iValue += (pLoopUnit->getLevel() * 100);

						if (pLoopUnit->canDefend() && pLoopUnit->plot()->isCity())
						{
							iValue *= 2;
						}

						if (pLoopUnit->plot()->getTeam() == pLoopUnit->getTeam())
						{
							iValue *= 3;
						}

						switch (pLoopUnit->AI_getUnitAIType())
						{
						case UNITAI_UNKNOWN:
						case UNITAI_ANIMAL:
							break;

						case UNITAI_SETTLE:
/*************************************************************************************************/
/**	BETTER AI (New UNITAI) Sephi                                 					            **/
/**																								**/
/**						                                            							**/
/*************************************************************************************************/
                        case UNITAI_WARWIZARD:
                        case UNITAI_TERRAFORMER:
                        case UNITAI_MANA_UPGRADE:
                        case UNITAI_MAGE:
						case UNITAI_HERO:
						case UNITAI_FEASTING:
						case UNITAI_MEDIC:
						case UNITAI_INQUISITOR:
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/
							iValue *= 20;
							break;

						case UNITAI_WORKER:
							iValue *= 10;
							break;

						case UNITAI_ATTACK:
						case UNITAI_ATTACK_CITY:
						case UNITAI_COLLATERAL:
						case UNITAI_PILLAGE:
						case UNITAI_RESERVE:
						case UNITAI_COUNTER:
							iValue *= 2;
							break;

						case UNITAI_CITY_DEFENSE:
						case UNITAI_CITY_COUNTER:
						case UNITAI_CITY_SPECIAL:
						case UNITAI_PARADROP:
							iValue *= 6;
							break;

						case UNITAI_EXPLORE:
							iValue *= 15;
							break;

						case UNITAI_MISSIONARY:
							iValue *= 8;
							if (pLoopUnit->isAIControl())
							{
								iValue = 0;
							}
							break;

						case UNITAI_PROPHET:
						case UNITAI_ARTIST:
						case UNITAI_SCIENTIST:
						case UNITAI_GENERAL:
						case UNITAI_MERCHANT:
						case UNITAI_ENGINEER:
							break;

						case UNITAI_SPY:
							iValue *= 12;
							break;

						case UNITAI_ICBM:
							iValue *= 4;
							break;

						case UNITAI_WORKER_SEA:
							iValue *= 18;
							break;

						case UNITAI_ATTACK_SEA:
						case UNITAI_RESERVE_SEA:
						case UNITAI_ESCORT_SEA:
							break;

						case UNITAI_EXPLORE_SEA:
							iValue *= 25;
							break;

						case UNITAI_ASSAULT_SEA:
						case UNITAI_SETTLER_SEA:
						case UNITAI_MISSIONARY_SEA:
						case UNITAI_SPY_SEA:
						case UNITAI_CARRIER_SEA:
						case UNITAI_MISSILE_CARRIER_SEA:
							iValue *= 5;
							break;

						case UNITAI_PIRATE_SEA:
						case UNITAI_ATTACK_AIR:
							break;

						case UNITAI_DEFENSE_AIR:
						case UNITAI_CARRIER_AIR:
						case UNITAI_MISSILE_AIR:
							iValue *= 3;
							break;

						default:
							FAssert(false);
							break;
						}

						if (pLoopUnit->getUnitInfo().getExtraCost() > 0)
						{
							iValue /= (pLoopUnit->getUnitInfo().getExtraCost() + 1);
						}

						if (iValue < iBestValue)
						{
							iBestValue = iValue;
							pBestUnit = pLoopUnit;
						}
					}
				}
			}
		}
	}

	if (pBestUnit != NULL)
	{
		swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_UNIT_DISBANDED_NO_MONEY", pBestUnit->getNameKey()).GetCString());
		gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_UNITDISBANDED", MESSAGE_TYPE_MINOR_EVENT, pBestUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pBestUnit->getX_INLINE(), pBestUnit->getY_INLINE(), true, true);

		FAssert(!(pBestUnit->isGoldenAge()));
		
		logBBAI("    Killing %S -- disbanded, no money (Unit %d - plot: %d, %d)",
				pBestUnit->getName().GetCString(), pBestUnit->getID(), pBestUnit->getX(), pBestUnit->getY());
		pBestUnit->kill(false);
	}
}


void CvPlayer::killUnits()
{
	CvUnit* pLoopUnit;
	int iLoop;

	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{

//FfH: Modified by Kael 06/13/2008
//		pLoopUnit->kill(false);
//	}
        for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
        {
            if (pLoopUnit->isHasPromotion((PromotionTypes)iI))
            {
                if (GC.getPromotionInfo((PromotionTypes)iI).isEquipment())
                {
                    pLoopUnit->setHasPromotion((PromotionTypes)iI, false);
                }
            }
        }
        if (pLoopUnit->isImmortal())
        {
            pLoopUnit->makeMortal(); // lfgr fix 01/2021: Reliably set counter to 0.
        }
        if (pLoopUnit->canScrap())
        {
			logBBAI("    Killing %S -- scrappable unit with eliminated owner (Unit %d - plot: %d, %d)",
					pLoopUnit->getName().GetCString(), pLoopUnit->getID(), pLoopUnit->getX(), pLoopUnit->getY());
            pLoopUnit->kill(false);
        }
        else
        {
			// HARDCODE - kill treasure chests on civ elimination
			if (pLoopUnit->getUnitClassType() == GC.getInfoTypeForString("EQUIPMENTCLASS_TREASURE"))
			{
				logBBAI("    Killing %S -- treasure chest with eliminated owner (Unit %d - plot: %d, %d)",
						pLoopUnit->getName().GetCString(), pLoopUnit->getID(), pLoopUnit->getX(), pLoopUnit->getY());
				pLoopUnit->kill(false);
			}
			else
			{
	            pLoopUnit->betray(BARBARIAN_PLAYER);
			}
        }
	}
//FfH: End Modify

}


// XXX should pUnit be a CvSelectionGroup???
// Returns the next unit in the cycle...
CvSelectionGroup* CvPlayer::cycleSelectionGroups(CvUnit* pUnit, bool bForward, bool bWorkers, bool* pbWrap)
{
	CLLNode<int>* pSelectionGroupNode;
	CLLNode<int>* pFirstSelectionGroupNode;
	CvSelectionGroup* pLoopSelectionGroup;

	if (pbWrap != NULL)
	{
		*pbWrap = false;
	}

	pSelectionGroupNode = headGroupCycleNode();

	if (pUnit != NULL)
	{
		while (pSelectionGroupNode != NULL)
		{
			if (getSelectionGroup(pSelectionGroupNode->m_data) == pUnit->getGroup())
			{
				if (bForward)
				{
					pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
				}
				else
				{
					pSelectionGroupNode = previousGroupCycleNode(pSelectionGroupNode);
				}
				break;
			}

			pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
		}
	}

	if (pSelectionGroupNode == NULL)
	{
		if (bForward)
		{
			pSelectionGroupNode = headGroupCycleNode();
		}
		else
		{
			pSelectionGroupNode = tailGroupCycleNode();
		}

		if (pbWrap != NULL)
		{
			*pbWrap = true;
		}
	}

	if (pSelectionGroupNode != NULL)
	{
		pFirstSelectionGroupNode = pSelectionGroupNode;

		while (true)
		{
			pLoopSelectionGroup = getSelectionGroup(pSelectionGroupNode->m_data);
			FAssertMsg(pLoopSelectionGroup != NULL, "LoopSelectionGroup is not assigned a valid value");

			if (pLoopSelectionGroup->readyToSelect())
			{
				if (!bWorkers || pLoopSelectionGroup->hasWorker())
				{
					if (pUnit && pLoopSelectionGroup == pUnit->getGroup())
					{
						if (pbWrap != NULL)
						{
							*pbWrap = true;
						}
					}

					return pLoopSelectionGroup;
				}
			}

			if (bForward)
			{
				pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);

				if (pSelectionGroupNode == NULL)
				{
					pSelectionGroupNode = headGroupCycleNode();

					if (pbWrap != NULL)
					{
						*pbWrap = true;
					}
				}
			}
			else
			{
				pSelectionGroupNode = previousGroupCycleNode(pSelectionGroupNode);

				if (pSelectionGroupNode == NULL)
				{
					pSelectionGroupNode = tailGroupCycleNode();

					if (pbWrap != NULL)
					{
						*pbWrap = true;
					}
				}
			}

			if (pSelectionGroupNode == pFirstSelectionGroupNode)
			{
				break;
			}
		}
	}

	return NULL;
}


bool CvPlayer::hasTrait(TraitTypes eTrait) const
{
// lfgr bugfix 08/2015
// Assert no longer valid. A leader type isn't needed to determine traits
//	FAssertMsg((getLeaderType() >= 0), "getLeaderType() is less than zero");
// lfgr end
	FAssertMsg((eTrait >= 0), "eTrait is less than zero");

//FfH: Scriptable Leader Traits: Modified by Kael 08/08/2007
//	return GC.getLeaderHeadInfo(getLeaderType()).hasTrait(eTrait);
	return m_pbTraits[(int)eTrait];
//FfH: End Modify

}

//FfH: Scriptable Leader Traits: Added by Kael 08/08/2007
void CvPlayer::setHasTrait(TraitTypes eTrait, bool bNewValue)
{
	FAssertMsg((eTrait >= 0), "eTrait is less than zero");

	int iI, iChange;

    if (bNewValue)
    {
        iChange = 1;
    }
    else
    {
        iChange = -1;
    }

	if (m_pbTraits[(int)eTrait] == bNewValue)
	{
		return;
	}

	m_pbTraits[(int)eTrait] = bNewValue;

	CvTraitInfo& kTraitInfo = GC.getTraitInfo(eTrait);

	changeExtraHealth(kTraitInfo.getHealth() * iChange);
	changeExtraHappiness(kTraitInfo.getHappiness() * iChange);

	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		changeExtraBuildingHappiness((BuildingTypes)iI, GC.getBuildingInfo((BuildingTypes)iI).getHappinessTraits((int)eTrait) * iChange);
	}

	changeUpkeepModifier(kTraitInfo.getUpkeepModifier() * iChange);
	changeLevelExperienceModifier(kTraitInfo.getLevelExperienceModifier() * iChange);
	changeGreatPeopleRateModifier(kTraitInfo.getGreatPeopleRateModifier() * iChange);
	changeGreatGeneralRateModifier(kTraitInfo.getGreatGeneralRateModifier() * iChange);
	changeDomesticGreatGeneralRateModifier(kTraitInfo.getDomesticGreatGeneralRateModifier() * iChange);

	changeMaxGlobalBuildingProductionModifier(kTraitInfo.getMaxGlobalBuildingProductionModifier() * iChange);
	changeMaxTeamBuildingProductionModifier(kTraitInfo.getMaxTeamBuildingProductionModifier() * iChange);
	changeMaxPlayerBuildingProductionModifier(kTraitInfo.getMaxPlayerBuildingProductionModifier() * iChange);

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeTradeYieldModifier(((YieldTypes)iI), kTraitInfo.getTradeYieldModifier(iI) * iChange);
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
    {
		changeFreeCityCommerce(((CommerceTypes)iI), kTraitInfo.getCommerceChange(iI) * iChange);
		changeCommerceRateModifier(((CommerceTypes)iI), kTraitInfo.getCommerceModifier(iI) * iChange);
	}

	for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (GC.getCivicOptionInfo((CivicOptionTypes) iI).getTraitNoUpkeep(int(eTrait)))
		{
			changeNoCivicUpkeepCount(((CivicOptionTypes)iI), iChange);
		}
	}

    if (kTraitInfo.isAdaptive())
    {
        setAdaptive(bNewValue);
    }
    if (kTraitInfo.isAgnostic())
    {
        setAgnostic(bNewValue);
    }
    if (kTraitInfo.isAssimilation())
    {
        setAssimilation(bNewValue);
    }
    if (kTraitInfo.isBarbarianAlly())
    {
        GET_TEAM(getTeam()).setBarbarianAlly(bNewValue);
    }
    if (kTraitInfo.isIgnoreFood())
    {
        setIgnoreFood(bNewValue);
    }
    if (kTraitInfo.isInsane())
    {
        setInsane(bNewValue);
    }
    if (kTraitInfo.isSprawling())
    {
        setSprawling(bNewValue);
    }
	changeFreeXPFromCombat(kTraitInfo.getFreeXPFromCombat() * iChange);
    if (kTraitInfo.getMaxCities() != -1)
    {
        if (iChange == 1)
        {
            setMaxCities(kTraitInfo.getMaxCities() + GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getMaxCitiesMod());
        }
        else
        {
            setMaxCities(-1);
        }
    }
	changePillagingGold(kTraitInfo.getPillagingGold() * iChange);
	changeStartingGold(kTraitInfo.getStartingGold() * iChange);
	changeSummonDuration(kTraitInfo.getSummonDuration() * iChange);
	changeUpgradeCostModifier(kTraitInfo.getUpgradeCostModifier() * iChange);

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		updateExtraYieldThreshold((YieldTypes)iI);
	}

	updateMaxAnarchyTurns();
}

/*
void CvPlayer::setDisableHuman(bool bNewValue)
{
	m_bDisableHuman = bNewValue;
	updateHuman();
}

bool CvPlayer::getDisableHuman() const
{
	return m_bDisableHuman;
}
*/
//FfH: End Add

/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                           07/09/08                            jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
void CvPlayer::setHumanDisabled( bool newVal )
{
	m_bDisableHuman = newVal;
	updateHuman();
}
bool CvPlayer::isHumanDisabled()
{
	return m_bDisableHuman;
}
/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                            END                                              */
/************************************************************************************************/

bool CvPlayer::isHuman() const
{
	return m_bHuman;
}

void CvPlayer::updateHuman()
{
	if (getID() == NO_PLAYER)
	{
		m_bHuman = false;
	}
	else
	{
/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                            09/01/07                        MRGENIE          */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/*
		m_bHuman = GC.getInitCore().getHuman(getID());
*/
		if( m_bDisableHuman )
		{
			m_bHuman = false;
		}
		else
		{
			m_bHuman = GC.getInitCore().getHuman(getID());
		}
/************************************************************************************************/
/* AI_AUTO_PLAY_MOD                            END                                              */
/************************************************************************************************/	
	}
}

bool CvPlayer::isBarbarian() const
{
#ifdef USE_OLD_CODE
	return (getID() == BARBARIAN_PLAYER);
#else
	return (getIDINLINE() == BARBARIAN_PLAYER);
#endif
}


const wchar* CvPlayer::getName(uint uiForm) const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
/* original code
	if (GC.getInitCore().getLeaderName(getID(), uiForm).empty() || (GC.getGameINLINE().isMPOption(MPOPTION_ANONYMOUS) && isAlive() && GC.getGameINLINE().getGameState() == GAMESTATE_ON))
	{
		return GC.getLeaderHeadInfo(getLeaderType()).getDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getLeaderName(getID(), uiForm);
	}
*/
	if( !(m_szName.empty()) )
	{
		return m_szName;
	}
	else if( GC.getInitCore().getLeaderName(getID(), uiForm).empty() || (GC.getGameINLINE().isMPOption(MPOPTION_ANONYMOUS) && isAlive() && GC.getGameINLINE().getGameState() == GAMESTATE_ON))
	{
		return GC.getLeaderHeadInfo(getLeaderType()).getDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getLeaderName(getID(), uiForm);
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}

/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
// This sets the name of the player, ie Peter or Montezuma
void CvPlayer::setName(std::wstring szNewValue)
{
	if ( isCityNameValid(CvWString(szNewValue), false)) // LFGR_TODO: Why city?
	{
		m_szName = szNewValue;
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
	}
}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

const wchar* CvPlayer::getNameKey() const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
/*
	if (GC.getInitCore().getLeaderNameKey(getID()).empty() || (GC.getGameINLINE().isMPOption(MPOPTION_ANONYMOUS) && isAlive()))
	{
		return GC.getLeaderHeadInfo(getLeaderType()).getTextKeyWide();
	}
	else
	{
		return GC.getInitCore().getLeaderNameKey(getID());
	}
*/
	if( !(m_szName.empty()) )
	{
		return m_szName;
	}
	else if (GC.getInitCore().getLeaderNameKey(getID()).empty() || (GC.getGameINLINE().isMPOption(MPOPTION_ANONYMOUS) && isAlive()))
	{
		return GC.getLeaderHeadInfo(getLeaderType()).getTextKeyWide();
	}
	else
	{
		return GC.getInitCore().getLeaderNameKey(getID());
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}


const wchar* CvPlayer::getCivilizationDescription(uint uiForm) const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
/*
	if (GC.getInitCore().getCivDescription(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivDescription(getID(), uiForm);
	}
*/
	if( !(m_szCivDesc.empty()) )
	{
		return m_szCivDesc;
	}
	else if (GC.getInitCore().getCivDescription(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivDescription(getID(), uiForm);
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}

/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
void CvPlayer::setCivName(std::wstring szNewDesc, std::wstring szNewShort, std::wstring szNewAdj)
{
	m_szCivDesc = szNewDesc;
	m_szCivShort = szNewShort;
	m_szCivAdj = szNewAdj;
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
	gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

const wchar* CvPlayer::getCivilizationDescriptionKey() const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
/*
	if (GC.getInitCore().getCivDescriptionKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getTextKeyWide();
	}
	else
	{
		return GC.getInitCore().getCivDescriptionKey(getID());
	}
*/
	if( !(m_szCivDesc.empty()) )
	{
		return m_szCivDesc;
	}
	else if (GC.getInitCore().getCivDescriptionKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getTextKeyWide();
	}
	else
	{
		return GC.getInitCore().getCivDescriptionKey(getID());
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}


const wchar* CvPlayer::getCivilizationShortDescription(uint uiForm) const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
/*
	if (GC.getInitCore().getCivShortDesc(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getShortDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivShortDesc(getID(), uiForm);
	}
*/
	if( !(m_szCivShort.empty()) )
	{
		return m_szCivShort;
	}
	else if (GC.getInitCore().getCivShortDesc(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getShortDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivShortDesc(getID(), uiForm);
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}


const wchar* CvPlayer::getCivilizationShortDescriptionKey() const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
/*
	if (GC.getInitCore().getCivShortDescKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getShortDescriptionKey();
	}
	else
	{
		return GC.getInitCore().getCivShortDescKey(getID());
	}
*/
	if( !(m_szCivShort.empty()) )
	{
		return m_szCivShort;
	}
	else if (GC.getInitCore().getCivShortDescKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getShortDescriptionKey();
	}
	else
	{
		return GC.getInitCore().getCivShortDescKey(getID());
	}

/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}


const wchar* CvPlayer::getCivilizationAdjective(uint uiForm) const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/* dynamic civ names                                                                            */
/************************************************************************************************/
/*
	if (GC.getInitCore().getCivAdjective(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getAdjective(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivAdjective(getID(), uiForm);
	}
*/
	if( !(m_szCivAdj.empty()) )
	{
		return m_szCivAdj;
	}
	else if (GC.getInitCore().getCivAdjective(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getAdjective(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivAdjective(getID(), uiForm);
	}

/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}

const wchar* CvPlayer::getCivilizationAdjectiveKey() const
{
/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/*
	if (GC.getInitCore().getCivAdjectiveKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getAdjectiveKey();
	}
	else
	{
		return GC.getInitCore().getCivAdjectiveKey(getID());
	}
*/
	if( !(m_szCivAdj.empty()) )
	{
		return m_szCivAdj;
	}
	else if (GC.getInitCore().getCivAdjectiveKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getAdjectiveKey();
	}
	else
	{
		return GC.getInitCore().getCivAdjectiveKey(getID());
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
}


CvWString CvPlayer::getFlagDecal() const
{
	if (GC.getInitCore().getFlagDecal(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getFlagTexture();
	}
	else
	{
		return GC.getInitCore().getFlagDecal(getID());
	}
}

bool CvPlayer::isWhiteFlag() const
{
	if (GC.getInitCore().getFlagDecal(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getArtInfo()->isWhiteFlag();
	}
	else
	{
		return GC.getInitCore().getWhiteFlag(getID());
	}
}


const wchar* CvPlayer::getStateReligionName(uint uiForm) const
{
	return GC.getReligionInfo(getStateReligion()).getDescription(uiForm);
}

const wchar* CvPlayer::getStateReligionKey() const
{
	if (getStateReligion() != NO_RELIGION)
	{
		return GC.getReligionInfo(getStateReligion()).getTextKeyWide();
	}

	return L"TXT_KEY_MISC_NO_STATE_RELIGION";
}


const CvWString CvPlayer::getBestAttackUnitName(uint uiForm) const
{
	return gDLL->getObjectText((CvString)getBestAttackUnitKey(), uiForm, true);
}


const CvWString CvPlayer::getWorstEnemyName() const
{
	TeamTypes eWorstEnemy;

	eWorstEnemy = GET_TEAM(getTeam()).AI_getWorstEnemy();

	if (eWorstEnemy != NO_TEAM)
	{
		return GET_TEAM(eWorstEnemy).getName();
	}

	return "";
}

/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
const CvWString CvPlayer::getClosestAllyName() const
{
	TeamTypes eClosestAlly;

	eClosestAlly = GET_TEAM(getTeam()).AI_getClosestAlly();

	if (eClosestAlly != NO_TEAM)
	{
		return GET_TEAM(eClosestAlly).getName();
	}

	return "";
}
/*************************************************************************************************/
/** Advanced Diplomacy       EBD                                                 			 */
/*************************************************************************************************/

const wchar* CvPlayer::getBestAttackUnitKey() const
{
	CvCity* pCapitalCity;
	CvCity* pLoopCity;
	UnitTypes eBestUnit;
	int iLoop;

	eBestUnit = NO_UNIT;

	pCapitalCity = getCapitalCity();

	if (pCapitalCity != NULL)
	{
		eBestUnit = pCapitalCity->AI_bestUnitAI(UNITAI_ATTACK, true);
	}

	if (eBestUnit == NO_UNIT)
	{
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			eBestUnit = pLoopCity->AI_bestUnitAI(UNITAI_ATTACK, true);

			if (eBestUnit != NO_UNIT)
			{
				break;
			}
		}
	}

	if (eBestUnit != NO_UNIT)
	{
		return GC.getUnitInfo(eBestUnit).getTextKeyWide();
	}

	return L"TXT_KEY_MISC_NO_UNIT";
}


ArtStyleTypes CvPlayer::getArtStyleType() const
{
	if (GC.getInitCore().getArtStyle(getID()) == NO_ARTSTYLE)
	{
		return ((ArtStyleTypes)(GC.getCivilizationInfo(getCivilizationType()).getArtStyleType()));
	}
	else
	{
		return GC.getInitCore().getArtStyle(getID());
	}
}

const TCHAR* CvPlayer::getUnitButton(UnitTypes eUnit) const
{
//>>>>Unofficial Bug Fix: Modified by Denev 2009/09/28
//*** Assimilated city produces a unit with original civilization artstyle.
//	return GC.getUnitInfo(eUnit).getArtInfo(0, getCurrentEra(), (UnitArtStyleTypes) GC.getCivilizationInfo(getCivilizationType()).getUnitArtStyleType())->getButton();
	return GC.getUnitInfo(eUnit).getArtInfo(0, getCurrentRealEra(), getUnitArtStyleType())->getButton();
//<<<<Unofficial Bug Fix: End Modify
}

// Automatic OOS detection START
#ifdef AUTOMATIC_OOS_DETECTION
#include <windows.h>
#endif //AUTOMATIC_OOS_DETECTION
// Automatic OOS detection END


void CvPlayer::doTurn()
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	int iLoop;

	FAssertMsg(isAlive(), "isAlive is expected to be true");
	FAssertMsg(!hasBusyUnit() || GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS)  || GC.getGameINLINE().isSimultaneousTeamTurns(), "End of turn with busy units in a sequential-turn game");

	CvEventReporter::getInstance().beginPlayerTurn( GC.getGameINLINE().getGameTurn(),  getID());

	doUpdateCacheOnTurn();

	// Sephi AI (new Player::DoTurn Functions)
    if (!isHuman())
    {
        AI_doTowerMastery();
    }
	// End Sephi AI

	// MNAI - Puppet States
	if (isPuppetState())
	{
		// check for legitimacy - requires that we be the only civ of our type left in the game
		bool bLegitimateCiv = true;
		
		for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive() && (iI!= getID()))
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == getCivilizationType())
				{
					bLegitimateCiv = false;
					break;
				}
			}
		}

		if (bLegitimateCiv)
		{
			setPuppetState(false);
			findNewCapital();

			CvWString szBuffer;
			szBuffer = gDLL->getText("TXT_KEY_MISC_PUPPET_STATE_LEGITIMIZED", getCivilizationDescriptionKey());
			GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, getCapitalCity()->getX(), getCapitalCity()->getY(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"));

			for (iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()) || (getTeam() == GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						szBuffer = gDLL->getText("TXT_KEY_MISC_PUPPET_STATE_LEGITIMIZED", getCivilizationDescriptionKey());
						gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDER_BUILDING_BUILD", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_PLAYER_LIGHT_ORANGE_TEXT"), getCapitalCity()->getX(), getCapitalCity()->getY(), true, true);
					}
				}
			}
		}
	}
	// MNAI - End Puppet States

	GC.getGameINLINE().verifyDeals();
	AI_doTurnPre();
	if (getRevolutionTimer() > 0)
	{
		changeRevolutionTimer(-1);
	}

	if (getConversionTimer() > 0)
	{
		changeConversionTimer(-1);
	}

/************************************************************************************************/
/* REVOLUTION_MOD                         02/04/09                                jdog5000      */
/*                                                                                              */
/* For rebels and BarbarianCiv                                                                  */
/************************************************************************************************/
	if( getFreeUnitCountdown() > 0 )
	{
		setFreeUnitCountdown(getFreeUnitCountdown() - 1);
	}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

	setConscriptCount(0);

	AI_assignWorkingPlots();

	if (0 == GET_TEAM(getTeam()).getHasMetCivCount(true) || GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		setCommercePercent(COMMERCE_ESPIONAGE, 0);
	}

/************************************************************************************************/
/* Advanced Diplomacy          END                                                            */
/************************************************************************************************/
	if (isActiveSenate())
	{
		for (int i = 0; i < MAX_TEAMS; i++)
		{
			if (getSenateVeto((TeamTypes)i) != -1)
			{
				setSenateVeto((TeamTypes)i, -1);
			}
		}
	}
/************************************************************************************************/
/* Advanced Diplomacy          END                                                            */
/************************************************************************************************/

	verifyGoldCommercePercent();

	doGold();

	doResearch();

	doEspionagePoints();

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      05/08/09                                jdog5000      */
/*                                                                                              */
/* City AI                                                                                      */
/************************************************************************************************/
    // New function to handle wonder construction in a centralized manner
	//GET_PLAYER(getID()).AI_doCentralizedProduction();
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->doTurn();
	}

/*************************************************************************************************/
/**	Xienwolf Tweak							12/27/08											**/
/**	ADDON (Stasis Pauses Golden Ages) merged Sephi																				**/
/**									Stasis Pauses Golden Ages									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (getGoldenAgeTurns() > 0)
/**								----  End Original Code  ----									**/
	if (getGoldenAgeTurns() > 0 && !(getDisableProduction() > 0 && getDisableResearch() > 0))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	{
		changeGoldenAgeTurns(-1);
	}

	if (getAnarchyTurns() > 0)
	{
		changeAnarchyTurns(-1);
	}

	verifyCivics();

	updateTradeRoutes();

	updateWarWearinessPercentAnger();

//FfH: Added by Kael 11/02/2007
    if (getTempPlayerTimer() > 0)
    {
        changeTempPlayerTimer(-1);
        if (getTempPlayerTimer() == 0)
        {
            GC.getInitCore().reassignPlayerAdvanced(getID(), (PlayerTypes)getRealPlayer(), -1);
        }
    }
    if (getSanctuaryTimer() > 0)
    {
        changeSanctuaryTimer(-1);
    }
    if (getDisableProduction() > 0)
    {
        changeDisableProduction(-1);
        updateMaintenance();

		if( getDisableProduction() == 0 )
		{
			updateCommerce();
		}
    }
    if (getDisableResearch() > 0)
    {
        changeDisableResearch(-1);
    }
    if (getDisableSpellcasting() > 0)
    {
        changeDisableSpellcasting(-1);
    }
//FfH: End Add

	doEvents();

	updateEconomyHistory(GC.getGameINLINE().getGameTurn(), calculateTotalCommerce());
	updateIndustryHistory(GC.getGameINLINE().getGameTurn(), calculateTotalYield(YIELD_PRODUCTION));
	updateAgricultureHistory(GC.getGameINLINE().getGameTurn(), calculateTotalYield(YIELD_FOOD));
	updatePowerHistory(GC.getGameINLINE().getGameTurn(), getPower());
	updateCultureHistory(GC.getGameINLINE().getGameTurn(), countTotalCulture());

//FfH: Modified by Kael 09/28/2008
//	updateEspionageHistory(GC.getGameINLINE().getGameTurn(), GET_TEAM(getTeam()).getEspionagePointsEver());
    if (!GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
    {
        updateEspionageHistory(GC.getGameINLINE().getGameTurn(), GET_TEAM(getTeam()).getEspionagePointsEver());
    }
/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         02/04/08                            Glider1        */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	//RevolutionDCM - revolution stability history
	updateRevolutionStabilityHistory(GC.getGameINLINE().getGameTurn(), getStabilityIndexAverage());
/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         END                                 Glider1        */
/************************************************************************************************/

	expireMessages();  // turn log

	gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);

	AI_doTurnPost();

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      07/08/09                                jdog5000      */
/*                                                                                              */
/* Debug                                                                                        */
/************************************************************************************************/
    if( GC.getGameINLINE().isDebugMode() )
	{
		GC.getGameINLINE().updateColoredPlots();
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

// Automatic OOS detection START
#ifdef AUTOMATIC_OOS_DETECTION
	if (getID() == GC.getGameINLINE().getActivePlayer() && GC.getGameINLINE().isGameMultiPlayer()) {
		// If human players don't take some time to do their stuff, Civilization IV engine goes awry.
		Sleep(1000);
	}
#endif //AUTOMATIC_OOS_DETECTION
// Automatic OOS detection END

	CvEventReporter::getInstance().endPlayerTurn( GC.getGameINLINE().getGameTurn(),  getID());
}


void CvPlayer::doTurnUnits()
{
	PROFILE_FUNC();

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	AI_doTurnUnitsPre();

//FfH: Added By Kael 09/13/2007
	CvUnit* pLoopUnit;
    int iSpell = GC.getDefineINT("SPECIALUNIT_SPELL");
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isEverAlive())
		{
            for (pLoopUnit = GET_PLAYER((PlayerTypes)iI).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)iI).nextUnit(&iLoop))
            {
                if (pLoopUnit->getSpecialUnitType() == iSpell)
                {
					logBBAI("    Killing %S -- SPECIALUNIT_SPELL killed each turn (Unit %d - plot: %d, %d)",
							pLoopUnit->getName().GetCString(), pLoopUnit->getID(), pLoopUnit->getX(), pLoopUnit->getY());
                    pLoopUnit->kill(false);
                }
            }
		}
	}
//FfH: End Add

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup != NULL; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		pLoopSelectionGroup->doDelayedDeath();
	}

	for (int iPass = 0; iPass < 4; iPass++)
	{
		for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup != NULL; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
		{
			switch (pLoopSelectionGroup->getDomainType())
			{
			case DOMAIN_AIR:
				if (iPass == 1)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case DOMAIN_SEA:
				if (iPass == 2)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case DOMAIN_LAND:
				if (iPass == 3)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case DOMAIN_IMMOBILE:
				if (iPass == 0)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case NO_DOMAIN:
				FAssertMsg(NULL == pLoopSelectionGroup->getHeadUnit(), "Unit with no Domain");
			default:
				if (iPass == 3)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			}
		}
	}

	if (getID() == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getFAStarIFace()->ForceReset(&GC.getInterfacePathFinder());

		gDLL->getInterfaceIFace()->setDirty(Waypoints_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
	}

	gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);

	AI_doTurnUnitsPost();
}

/************************************************************************************************/
/* Advanced Diplomacy          START                                                           */
/************************************************************************************************/
int CvPlayer::getSenateVeto(TeamTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (m_aiSenateVeto.size() <= 0)
	{
		return 0;
	}

	return m_aiSenateVeto[eIndex];
}

bool CvPlayer::isSenateVeto(TeamTypes eIndex, bool bVerify)
{
	if (!isActiveSenate())
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isWarPretextAgainst(eIndex))
	{
		return false;
	}

	if (bVerify && getSenateVeto(eIndex) == -1)
	{
		setSenateVeto(eIndex, isSenateWarOpposition(eIndex) ? 1 : 0);
	}

	return (getSenateVeto(eIndex) > 0);
}

void CvPlayer::setSenateVeto(TeamTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iNewValue != getSenateVeto(eIndex))
	{
		if (m_aiSenateVeto.size() <= 0)
		{
			m_aiSenateVeto.clear();
			for (int iI = 0; iI < MAX_TEAMS; iI++)
			{
				m_aiSenateVeto.push_back(0);
			}
		}

		m_aiSenateVeto[eIndex] = iNewValue;

		// keep the array ?
		bool bErase = getSenateVeto(eIndex) == 0;
		if (bErase)
		{
			for (int i = 0; i < MAX_TEAMS; ++i)
			{
				if (getSenateVeto((TeamTypes)i) != 0)
				{
					bErase = false;
					break;
				}
			}

			if (bErase)
			{
				m_aiSenateVeto.clear();
			}
		}
	}
}
/************************************************************************************************/
/* Advanced Diplomacy          END                                                            */
/************************************************************************************************/

void CvPlayer::verifyCivics()
{
	int iI, iJ;

	if (!isAnarchy())
	{
		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			if (!canDoCivics(getCivics((CivicOptionTypes)iI)))
			{
				for (iJ = 0; iJ < GC.getNumCivicInfos(); iJ++)
				{
					if (GC.getCivicInfo((CivicTypes)iJ).getCivicOptionType() == iI)
					{
						if (canDoCivics((CivicTypes)iJ))
						{
							setCivics(((CivicOptionTypes)iI), ((CivicTypes)iJ));
							break;
						}
					}
				}
			}
		}
	}
}


void CvPlayer::updatePlotGroups()
{
	PROFILE_FUNC();

	CvPlotGroup* pLoopPlotGroup;
	int iLoop;
	int iI;

	if (!(GC.getGameINLINE().isFinalInitialized()))
	{
		return;
	}

	for(pLoopPlotGroup = firstPlotGroup(&iLoop); pLoopPlotGroup != NULL; pLoopPlotGroup = nextPlotGroup(&iLoop))
	{
		pLoopPlotGroup->recalculatePlots();
	}

	for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		GC.getMapINLINE().plotByIndexINLINE(iI)->updatePlotGroup(getID(), false);
	}

	updateTradeRoutes();
}


void CvPlayer::updateYield()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateYield();
	}
}


void CvPlayer::updateMaintenance()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateMaintenance();
	}
}


void CvPlayer::updatePowerHealth()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updatePowerHealth();
	}
}


void CvPlayer::updateExtraBuildingHappiness()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateExtraBuildingHappiness();
	}
}


void CvPlayer::updateExtraBuildingHealth()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateExtraBuildingHealth();
	}
}


void CvPlayer::updateFeatureHappiness()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateFeatureHappiness();
	}
}


void CvPlayer::updateReligionHappiness()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateReligionHappiness();
	}
}


void CvPlayer::updateExtraSpecialistYield()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateExtraSpecialistYield();
	}
}


void CvPlayer::updateCommerce(CommerceTypes eCommerce)
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateCommerce(eCommerce);
	}
}


void CvPlayer::updateCommerce()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateCommerce();
	}
}


void CvPlayer::updateBuildingCommerce()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateBuildingCommerce();
	}
}


void CvPlayer::updateReligionCommerce()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateReligionCommerce();
	}
}


void CvPlayer::updateCorporation()
{
	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateCorporation();
	}
}


void CvPlayer::updateCityPlotYield()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->plot()->updateYield();
	}
}


void CvPlayer::updateCitySight(bool bIncrement, bool bUpdatePlotGroups)
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->plot()->updateSight(bIncrement, bUpdatePlotGroups);
	}
}


void CvPlayer::updateTradeRoutes()
{
	CLLNode<int>* pCityNode;
	CvCity* pLoopCity;
	CvCity* pListCity;
	CLinkList<int> cityList;
	int iTotalTradeModifier;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->clearTradeRoutes();
	}

	cityList.clear();

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalTradeModifier = pLoopCity->totalTradeModifier();

		pCityNode = cityList.head();

		while (pCityNode != NULL)
		{
			pListCity = getCity(pCityNode->m_data);

			if (iTotalTradeModifier > pListCity->totalTradeModifier())
			{
				cityList.insertBefore(pLoopCity->getID(), pCityNode);
				break;
			}
			else
			{
				pCityNode = cityList.next(pCityNode);
			}
		}

		if (pCityNode == NULL)
		{
			cityList.insertAtEnd(pLoopCity->getID());
		}
	}

	pCityNode = cityList.head();

	while (pCityNode != NULL)
	{
		getCity(pCityNode->m_data)->updateTradeRoutes();
		pCityNode = cityList.next(pCityNode);
	}
}

void CvPlayer::updatePlunder(int iChange, bool bUpdatePlotGroups)
{
	int iLoop;
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->isBlockading())
		{
			pLoopUnit->updatePlunder(iChange, bUpdatePlotGroups);
		}
	}
}

void CvPlayer::updateTimers()
{
	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		pLoopSelectionGroup->updateTimers(); // could destroy the selection group...
	}

	// if a unit was busy, perhaps it was not quite deleted yet, give it one more try
	if (getNumSelectionGroups() > getNumUnits())
	{
		for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
		{
			pLoopSelectionGroup->doDelayedDeath(); // could destroy the selection group...
		}
	}

	FAssertMsg(getNumSelectionGroups() <= getNumUnits(), "The number of Units is expected not to exceed the number of Selection Groups");
}


bool CvPlayer::hasReadyUnit(bool bAny) const
{
	PROFILE_FUNC();

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		if (pLoopSelectionGroup->readyToMove(bAny))
		{
			return true;
		}
	}

	return false;
}


bool CvPlayer::hasAutoUnit() const
{
	PROFILE_FUNC();

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		if (pLoopSelectionGroup->readyToAuto())
		{
			return true;
		}
	}

	return false;
}


bool CvPlayer::hasBusyUnit() const
{
	PROFILE_FUNC();

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		if (pLoopSelectionGroup->isBusy())
		{
		    if (pLoopSelectionGroup->getNumUnits() == 0)
		    {
		        pLoopSelectionGroup->kill();
		        return false;
		    }

			return true;
		}
	}

	return false;
}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                             EmperorFool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
// Free Tech Popup Fix
bool CvPlayer::isChoosingFreeTech() const
{
	return m_bChoosingFreeTech;
}

void CvPlayer::setChoosingFreeTech(bool bValue)
{
	m_bChoosingFreeTech = bValue;
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

void CvPlayer::chooseTech(int iDiscover, CvWString szText, bool bFront)
{
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                             EmperorFool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Free Tech Popup Fix
	if (iDiscover > 0)
	{
		setChoosingFreeTech(true);
	}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHOOSETECH);
	if (NULL != pInfo)
	{
		pInfo->setData1(iDiscover);
		pInfo->setText(szText);
		gDLL->getInterfaceIFace()->addPopup(pInfo, getID(), false, bFront);
	}
}


int CvPlayer::calculateScore(bool bFinal, bool bVictory)
{
	PROFILE_FUNC();

	if (!isAlive())
	{
		return 0;
	}

	if (GET_TEAM(getTeam()).getNumMembers() == 0)
	{
		return 0;
	}

	long lScore = 0;

	CyArgsList argsList;
	argsList.add((int) getID());
	argsList.add(bFinal);
	argsList.add(bVictory);
	gDLL->getPythonIFace()->callFunction(PYGameModule, "calculateScore", argsList.makeFunctionArgs(), &lScore);

	return ((int)lScore);
}


int CvPlayer::findBestFoundValue() const
{
	CvArea* pLoopArea;
	int iValue;
	int iBestValue;
	int iLoop;

	iBestValue = 0;

	for(pLoopArea = GC.getMapINLINE().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoop))
	{
		iValue = pLoopArea->getBestFoundValue(getID());

		if (iValue > iBestValue)
		{
			iBestValue = iValue;
		}
	}

	return iBestValue;
}


int CvPlayer::upgradeAllPrice(UnitTypes eUpgradeUnit, UnitTypes eFromUnit)
{
	CvUnit* pLoopUnit;
	int iPrice;
	int iLoop;

	iPrice = 0;

	// Loop through units and determine the total power of this player's military
	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->getUnitType() == eFromUnit)
		{
			if (pLoopUnit->canUpgrade(eUpgradeUnit, true))
			{
				iPrice += pLoopUnit->upgradePrice(eUpgradeUnit);
			}
		}
	}

	return iPrice;
}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      11/14/09                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
int CvPlayer::countReligionSpreadUnits(CvArea* pArea, ReligionTypes eReligion, bool bIncludeTraining) const
{
	PROFILE_FUNC();

	CvUnit* pLoopUnit;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->getArea() == pArea->getID())
		{
			if (pLoopUnit->getUnitInfo().getReligionSpreads(eReligion) > 0)
			{
				iCount++;
			}
		}
	}

	if( bIncludeTraining )
	{
		CvCity* pLoopCity;
		for( pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop) )
		{
			UnitTypes eUnit = pLoopCity->getProductionUnit();

			if( eUnit != NO_UNIT )
			{
				if(GC.getUnitInfo(eUnit).getReligionSpreads(eReligion) > 0)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}

int CvPlayer::countCorporationSpreadUnits(CvArea* pArea, CorporationTypes eCorporation, bool bIncludeTraining) const
{
	PROFILE_FUNC();

	int iCount = 0;
	int iLoop;
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->area() == pArea)
		{
			if (pLoopUnit->getUnitInfo().getCorporationSpreads(eCorporation) > 0)
			{
				++iCount;
			}
		}
	}

	if( bIncludeTraining )
	{
		CvCity* pLoopCity;
		for( pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop) )
		{
			UnitTypes eUnit = pLoopCity->getProductionUnit();

			if( eUnit != NO_UNIT )
			{
				if(GC.getUnitInfo(eUnit).getCorporationSpreads(eCorporation) > 0)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

int CvPlayer::countNumCoastalCities() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
		{
			iCount++;
		}
	}

	return iCount;
}


int CvPlayer::countNumCoastalCitiesByArea(CvArea* pArea) const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	int iAreaID = pArea->getID();
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
		{
			if ((pLoopCity->getArea() == iAreaID) || pLoopCity->plot()->isAdjacentToArea(iAreaID))
			{
				iCount++;
			}
		}
	}

	return iCount;
}


int CvPlayer::countTotalCulture() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iCount += pLoopCity->getCultureTimes100(getID());
	}

	return iCount/100;
}


int CvPlayer::countOwnedBonuses(BonusTypes eBonus, bool bCheckBlockingFeatures) const
{
	PROFILE("CvPlayer::countOwnedBonuses");
    //CvCity* pLoopCity;
	CvPlot* pLoopPlot;
	int iCount;
	int iI;
	//int iLoop;

	// lfgr_todo: (getCurrentRealEra() < 3) always true in FfH/MNAI. What is this even supposed to do (same in vanilla bts)?
    bool bAdvancedStart = (getAdvancedStartPoints() >= 0) && (getCurrentRealEra() < 3);
	bool bCanWork;

	iCount = 0;

	for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->getOwnerINLINE() == getID())
		{
			if (pLoopPlot->getBonusType(getTeam()) == eBonus)
			{
				// this section is used in tech valuation - dont want to research techs for resources we cant exploit due to blocking features
				if (bCheckBlockingFeatures)
				{
					bCanWork = false;
					if (pLoopPlot->getFeatureType() == NO_FEATURE)
					{
						bCanWork = true;
					}
					else if (GC.getCivilizationInfo(getCivilizationType()).isMaintainFeatures(pLoopPlot->getFeatureType()))
					{
						bCanWork = true;
					}
					else
					{
						for (int iJ = 0; iJ < GC.getNumBuildInfos(); iJ++)
						{
							BuildTypes eBuild = ((BuildTypes)iJ);
							if (eBuild != NO_BUILD)
							{
								ImprovementTypes eImp = (ImprovementTypes)GC.getBuildInfo(eBuild).getImprovement();
								if ( eImp != NO_IMPROVEMENT && GC.getImprovementInfo(eImp).isImprovementBonusTrade(eBonus) )
								{
									if (GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo(eBuild).getFeatureTech(pLoopPlot->getFeatureType())))
									{
										bCanWork = true;
										break;
									}
								}
							}
						}
					}
				}

				if (!bCheckBlockingFeatures || bCanWork)
				{
					iCount++;
				}
			}
		}
	}

	/*
	//count bonuses outside city radius
	for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if ((pLoopPlot->getOwnerINLINE() == getID()) && !pLoopPlot->isCityRadius())
		{
			if (pLoopPlot->getBonusType(getTeam()) == eBonus)
			{
				iCount++;
			}
		}
		else if (bAdvancedStart && pLoopPlot->isRevealed(getTeam(), false))
		{
			if (pLoopPlot->getBonusType(getTeam()) == eBonus)
			{
				iCount++;
			}
		}
	}



	//count bonuses inside city radius or easily claimed
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iCount += pLoopCity->AI_countNumBonuses(eBonus, true, pLoopCity->getCommerceRate(COMMERCE_CULTURE) > 0, -1, true, true);
	}
	*/

	return iCount;
}


// K-Mod. I've rearranged some stuff in this function to fix a couple of minor bugs; and to make the code neater and less error prone.
int CvPlayer::countUnimprovedBonuses(CvArea* pArea, CvPlot* pFromPlot) const
{
	PROFILE_FUNC();

	gDLL->getFAStarIFace()->ForceReset(&GC.getBorderFinder());

	int iCount = 0;

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->getOwnerINLINE() == getID() && pLoopPlot->area() == pArea && !pLoopPlot->isCity())
		{
			BonusTypes eNonObsoleteBonus = pLoopPlot->getNonObsoleteBonusType(getTeam());

			if (eNonObsoleteBonus != NO_BONUS)
			{
				if (!doesImprovementConnectBonus(pLoopPlot->getImprovementType(), eNonObsoleteBonus))
				{
					if ((pFromPlot == NULL) || gDLL->getFAStarIFace()->GeneratePath(&GC.getBorderFinder(), pFromPlot->getX_INLINE(), pFromPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), false, getID(), true))
					{
						for (int iJ = 0; iJ < GC.getNumBuildInfos(); iJ++)
						{
							BuildTypes eBuild = ((BuildTypes)iJ);

							if (doesImprovementConnectBonus((ImprovementTypes)GC.getBuildInfo(eBuild).getImprovement(), eNonObsoleteBonus) && canBuild(pLoopPlot, eBuild))
							{
								iCount++;
								break; // K-Mod!
							}
						}
					}
				}
			}
		}
	}

	return iCount;
}


int CvPlayer::countCityFeatures(FeatureTypes eFeature) const
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	CvPlot* pLoopPlot;
	int iCount;
	int iLoop;
	int iI;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//		for (iI = 0; iI < NUM_CITY_PLOTS; iI++)
		for (iI = 0; iI < ::calculateNumCityPlots(getNextCityRadius()); iI++)
//<<<<Unofficial Bug Fix: End Modify
		{
			pLoopPlot = plotCity(pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE(), iI);

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->getFeatureType() == eFeature)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}


int CvPlayer::countNumBuildings(BuildingTypes eBuilding) const
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->getNumBuilding(eBuilding) > 0)
		{
			iCount += pLoopCity->getNumBuilding(eBuilding);
		}
	}

	return iCount;
}


int CvPlayer::countNumCitiesConnectedToCapital() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isConnectedToCapital())
		{
			iCount++;
		}
	}

	return iCount;
}

// K-Mod
bool CvPlayer::doesImprovementConnectBonus(ImprovementTypes eImprovement, BonusTypes eBonus) const
{
	return GET_TEAM(getTeam()).doesImprovementConnectBonus(eImprovement, eBonus);
}
// K-Mod end

int CvPlayer::countPotentialForeignTradeCities(CvArea* pIgnoreArea) const
{
	int iTempValue;
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (iI != getTeam())
			{
				if (GET_TEAM(getTeam()).isFreeTrade((TeamTypes)iI))
				{
					iTempValue = GET_TEAM((TeamTypes)iI).getNumCities();

					if (pIgnoreArea != NULL)
					{
						iTempValue -= GET_TEAM((TeamTypes)iI).countNumCitiesByArea(pIgnoreArea);
					}

					iCount += iTempValue;
				}
			}
		}
	}

	return iCount;
}


int CvPlayer::countPotentialForeignTradeCitiesConnected() const
{
	CvCity* pCapitalCity;
	CvCity* pLoopCity;
	int iCount;
	int iLoop;
	int iI;

	iCount = 0;

	pCapitalCity = getCapitalCity();

	if (pCapitalCity != NULL)
	{
		for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam())
				{
					if (GET_TEAM(getTeam()).isFreeTrade(GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
						{
							FAssert(pLoopCity->getOwnerINLINE() != getID());
							FAssert(pLoopCity->getTeam() != getTeam());

							if (pLoopCity->plotGroup(getID()) == pCapitalCity->plotGroup(getID()))
							{
								iCount++;
							}
						}
					}
				}
			}
		}
	}

	return iCount;
}



bool CvPlayer::canContact(PlayerTypes ePlayer) const
{
	if (ePlayer == getID())
	{
		return false;
	}

	CvPlayer &kPlayer = GET_PLAYER(ePlayer);

	if (!isAlive() || !(kPlayer.isAlive()))
	{
		return false;
	}

	if (isBarbarian() || kPlayer.isBarbarian())
	{
		return false;
	}

	if (isMinorCiv() || kPlayer.isMinorCiv())
	{
		return false;
	}

	if (getTeam() != kPlayer.getTeam())
	{
		CvTeam &kTeam = GET_TEAM(getTeam());

		if (!(kTeam.isHasMet(kPlayer.getTeam())))
		{
			return false;
		}

		if (atWar(getTeam(), kPlayer.getTeam()))
		{

//FfH: Added by Kael 08/14/2007
            if (isNoDiplomacyWithEnemies())
            {
                return false;
            }
//FfH: End Add

			if (!(kTeam.canChangeWarPeace(kPlayer.getTeam())))
			{
				return false;
			}
		}

		if (isHuman() || kPlayer.isHuman())
		{
			if (GC.getGameINLINE().isOption(GAMEOPTION_ALWAYS_WAR))
			{
				return false;
			}
		}
	}

//FfH: Added by Kael 11/06/2007
    if (getTempPlayerTimer() > 0)
    {
        return false;
    }
//FfH: End Add

	return true;
}


void CvPlayer::contact(PlayerTypes ePlayer)
{
	CvDiploParameters* pDiplo;

	if (!canContact(ePlayer) || isTurnDone())
	{
		return;
	}

	if (GET_PLAYER(ePlayer).isHuman())
	{
		if (GC.getGameINLINE().isPbem() || GC.getGameINLINE().isHotSeat() || (GC.getGameINLINE().isPitboss() && !gDLL->isConnected(GET_PLAYER(ePlayer).getNetID())))
		{
			if (gDLL->isMPDiplomacy())
			{
				gDLL->beginMPDiplomacy(ePlayer, false, false);
			}
		}
		else
		{
			if (gDLL->getInterfaceIFace()->isFlashing(ePlayer))
			{
				if (!gDLL->getInterfaceIFace()->isDiplomacyLocked())
				{
					gDLL->getInterfaceIFace()->setDiplomacyLocked(true);
					gDLL->sendContactCiv(NETCONTACT_RESPONSE, ePlayer);
				}
			}
			else
			{
				gDLL->sendContactCiv(NETCONTACT_INITIAL, ePlayer);
			}
		}
	}
	else
	{
		pDiplo = new CvDiploParameters(ePlayer);
		FAssert(pDiplo != NULL);
		if (gDLL->ctrlKey())
		{
			pDiplo->setDiploComment((DiploCommentTypes)GC.getInfoTypeForString("AI_DIPLOCOMMENT_TRADING"));
		}
		gDLL->getInterfaceIFace()->setDiploQueue(pDiplo, GC.getGameINLINE().getActivePlayer());
	}
}


void CvPlayer::handleDiploEvent(DiploEventTypes eDiploEvent, PlayerTypes ePlayer, int iData1, int iData2)
{
	CivicTypes* paeNewCivics;
	CvCity* pCity;
	int iI;

/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  Glider1      */
/*************************************************************************************************/
	// RevolutionDCM start - new diplomacy option
	//FAssertMsg(ePlayer != getID(), "shouldn't call this function on ourselves");
	// RevolutionDCM end
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/

	FAssertMsg(ePlayer != getID(), "shouldn't call this function on ourselves");

	switch (eDiploEvent)
	{
	case DIPLOEVENT_CONTACT:
		AI_setFirstContact(ePlayer, true);
		GET_PLAYER(ePlayer).AI_setFirstContact(getID(), true);
		break;

	case DIPLOEVENT_AI_CONTACT:
		break;

	case DIPLOEVENT_FAILED_CONTACT:
		AI_setFirstContact(ePlayer, true);
		GET_PLAYER(ePlayer).AI_setFirstContact(getID(), true);
		break;

	case DIPLOEVENT_GIVE_HELP:
		AI_changeMemoryCount(ePlayer, MEMORY_GIVE_HELP, 1);
		forcePeace(ePlayer);
		break;

	case DIPLOEVENT_REFUSED_HELP:
		AI_changeMemoryCount(ePlayer, MEMORY_REFUSED_HELP, 1);
		break;

	case DIPLOEVENT_ACCEPT_DEMAND:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPT_DEMAND, 1);
		forcePeace(ePlayer);
		break;

	case DIPLOEVENT_REJECTED_DEMAND:
		FAssertMsg(GET_PLAYER(ePlayer).getTeam() != getTeam(), "shouldn't call this function on our own team");

		AI_changeMemoryCount(ePlayer, MEMORY_REJECTED_DEMAND, 1);

		if (AI_demandRebukedSneak(ePlayer))
		{
			GET_TEAM(getTeam()).AI_setWarPlan(GET_PLAYER(ePlayer).getTeam(), WARPLAN_PREPARING_LIMITED);
		}
		break;

	case DIPLOEVENT_DEMAND_WAR:
		FAssertMsg(GET_PLAYER(ePlayer).getTeam() != getTeam(), "shouldn't call this function on our own team");
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/02/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("    Team %d (%S) declares war on team %d due to DIPLOEVENT", getTeam(), getCivilizationDescription(0), ePlayer );
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		GET_TEAM(getTeam()).declareWar(GET_PLAYER(ePlayer).getTeam(), false, WARPLAN_LIMITED);
		break;

	case DIPLOEVENT_CONVERT:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_RELIGION, 1);
		GET_PLAYER(ePlayer).convert(getStateReligion());
		break;

	case DIPLOEVENT_NO_CONVERT:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_RELIGION, 1);
		break;

	case DIPLOEVENT_REVOLUTION:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_CIVIC, 1);

		paeNewCivics = new CivicTypes[GC.getNumCivicOptionInfos()];

		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			paeNewCivics[iI] = GET_PLAYER(ePlayer).getCivics((CivicOptionTypes)iI);
		}

		FAssertMsg(GC.getLeaderHeadInfo(getPersonalityType()).getFavoriteCivic() != NO_CIVIC, "getFavoriteCivic() must be valid");

		paeNewCivics[GC.getCivicInfo((CivicTypes)(GC.getLeaderHeadInfo(getPersonalityType())).getFavoriteCivic()).getCivicOptionType()] = ((CivicTypes)(GC.getLeaderHeadInfo(getPersonalityType()).getFavoriteCivic()));

		GET_PLAYER(ePlayer).revolution(paeNewCivics, true);

		SAFE_DELETE_ARRAY(paeNewCivics);
		break;

	case DIPLOEVENT_NO_REVOLUTION:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_CIVIC, 1);
		break;

	case DIPLOEVENT_JOIN_WAR:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_JOIN_WAR, 1);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/02/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("    Team %d (%S) declares war on team %d due to DIPLOEVENT", getTeam(), getCivilizationDescription(0), ePlayer );
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		GET_TEAM(GET_PLAYER(ePlayer).getTeam()).declareWar(((TeamTypes)iData1), false, WARPLAN_DOGPILE);

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == ((TeamTypes)iData1))
				{
					GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_HIRED_WAR_ALLY, 1);
				}
			}
		}
		break;

	case DIPLOEVENT_NO_JOIN_WAR:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_JOIN_WAR, 1);
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/		
		if (m_eDemandWarAgainstTeam != NO_TEAM)
		{
			for (iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (GET_PLAYER((PlayerTypes)iI).getTeam() == m_eDemandWarAgainstTeam)
					{
						if (GET_PLAYER((PlayerTypes)iI).AI_getMemoryCount(ePlayer, MEMORY_EVENT_GOOD_TO_US) < 3)
						{
							GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(ePlayer, MEMORY_EVENT_GOOD_TO_US, 1);
						}
					}
				}
			}
			m_eDemandWarAgainstTeam = NO_TEAM;
		}					
/************************************************************************************************/
/* Advanced Diplomacy          END																*/
/************************************************************************************************/
		break;

	case DIPLOEVENT_STOP_TRADING:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_STOP_TRADING, 1);
		GET_PLAYER(ePlayer).stopTradingWithTeam((TeamTypes)iData1);

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == ((TeamTypes)iData1))
				{
					GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_HIRED_TRADE_EMBARGO, 1);
				}
			}
		}
		break;

	case DIPLOEVENT_NO_STOP_TRADING:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_STOP_TRADING, 1);
		break;

	case DIPLOEVENT_ASK_HELP:
		AI_changeMemoryCount(ePlayer, MEMORY_MADE_DEMAND_RECENT, 1);
		break;

	case DIPLOEVENT_MADE_DEMAND:
		if (AI_getMemoryCount(ePlayer, MEMORY_MADE_DEMAND) < 10)
		{
			AI_changeMemoryCount(ePlayer, MEMORY_MADE_DEMAND, 1);
		}
		AI_changeMemoryCount(ePlayer, MEMORY_MADE_DEMAND_RECENT, 1);
		break;

	case DIPLOEVENT_MADE_DEMAND_VASSAL:
		break;

	case DIPLOEVENT_RESEARCH_TECH:
		pushResearch(((TechTypes)iData1), true);
		break;

	case DIPLOEVENT_TARGET_CITY:
		pCity = GET_PLAYER((PlayerTypes)iData1).getCity(iData2);
		if (pCity != NULL)
		{
			pCity->area()->setTargetCity(getID(), pCity);
		}
		break;
/************************************************************************************************/
/* Afforess	                  Start		 08/01/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
   case DIPLOEVENT_MAKE_PEACE_WITH:
		if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAtWar((TeamTypes)iData1))
		{
			if (AI_getMemoryCount(ePlayer, MEMORY_EVENT_GOOD_TO_US) < 3)
			{
				AI_changeMemoryCount(ePlayer, MEMORY_EVENT_GOOD_TO_US, 1);
			}
			GET_TEAM(GET_PLAYER(ePlayer).getTeam()).makePeace((TeamTypes)iData1);
		}
        break;
    case DIPLOEVENT_NO_MAKE_PEACE_WITH:
		if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAtWar((TeamTypes)iData1))
		{
			if (AI_getMemoryCount(ePlayer, MEMORY_REFUSED_HELP) < 3)
			{
				AI_changeMemoryCount(ePlayer, MEMORY_REFUSED_HELP, 1);
			}
		}
        break;
	// RevolutionDCM start - new diplomacy option
	case DIPLOEVENT_DO_NOT_BOTHER:
		if (!isHuman())	setDoNotBotherStatus((PlayerTypes)iData1);
		break;

	case DIPLOEVENT_RESUME_BOTHER:
		setDoNotBotherStatus(NO_PLAYER);
		break;
	// RevolutionDCM end
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	default:
		FAssert(false);
		break;
	}
}


bool CvPlayer::canTradeWith(PlayerTypes eWhoTo) const
{
	CvTeam& kOurTeam = GET_TEAM(getTeam());
	CvTeam& kTheirTeam = GET_TEAM(GET_PLAYER(eWhoTo).getTeam());

	if (!canContact(eWhoTo))
	{
		return false;
	}

	if (kTheirTeam.getNumCities() == 0)
	{
		if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
		{
			return false;
		}
	}

	if (atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
	{
		return true;
	}

	if (kOurTeam.isTechTrading() || kTheirTeam.isTechTrading())
	{
		return true;
	}

	if (kOurTeam.isGoldTrading() || kTheirTeam.isGoldTrading())
	{
		return true;
	}

	if (kOurTeam.isMapTrading() || kTheirTeam.isMapTrading())
	{
		return true;
	}

	if (canTradeNetworkWith(eWhoTo))
	{
		return true;
	}

	if (kOurTeam.isOpenBordersTrading() || kTheirTeam.isOpenBordersTrading())
	{
		return true;
	}

	if (kOurTeam.isDefensivePactTrading() || kTheirTeam.isDefensivePactTrading())
	{
		return true;
	}

	if (kOurTeam.isPermanentAllianceTrading() || kTheirTeam.isPermanentAllianceTrading())
	{
		return true;
	}

	if (kOurTeam.isVassalStateTrading() || kTheirTeam.isVassalStateTrading())
	{
		return true;
	}

/************************************************************************************************/
/* Advanced Diplomacy         START                                                             */
/************************************************************************************************/
	
	if (GET_TEAM(getTeam()).isLimitedBordersTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isLimitedBordersTrading())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isEmbassyTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isEmbassyTrading())
	{
		return true;
	}
	
	if (GET_TEAM(getTeam()).isFreeTradeAgreementTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isFreeTradeAgreementTrading())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isNonAggressionTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isNonAggressionTrading())
	{
		return true;
	}
	
	if (GET_TEAM(getTeam()).isPOWTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isPOWTrading())
	{
		return true;
	}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

// MNAI - Puppet States
	if (GET_TEAM(getTeam()).isPuppetStateTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isPuppetStateTrading())
	{
		return true;
	}
// MNAI - End Puppet States

	return false;
}

bool CvPlayer::canReceiveTradeCity() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	return true;
}

bool CvPlayer::canTradeItem(PlayerTypes eWhoTo, TradeData item, bool bTestDenial) const
{
	// Bugfix: Cannot trade items with enemies while in crusade.
	if(isNoDiplomacyWithEnemies() && GET_TEAM(getTeam()).isAtWar(GET_PLAYER(eWhoTo).getTeam()))
	{
		return false;
	}

	CvCity *pOurCapitalCity;
/************************************************************************************************/
/* Afforess	                  Start		 07/29/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
    CvCity* pTheirCapitalCity;
    CvCity* pTradingCity;
    CvUnit* pUnitTraded;
	//int iI;

	//	KOSHLING - do denial check at the end because it's expensive and 95% of the time we detrmien the trade is
	//	not possible before having to make the denail check that way
	bool bResult = false;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

	if (bTestDenial)
	{
		if (getTradeDenial(eWhoTo, item) != NO_DENIAL)
		{
			return false;
		}
	}

//FfH: Added by Kael 11/20/2007
    bool bCanTrade = true;
	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); iI++)
	{
	    if (isFullMember((VoteSourceTypes)iI))
	    {
	        if (GC.getGameINLINE().isNoOutsideTechTrades((VoteSourceTypes)iI))
	        {
	            if (!GET_PLAYER(eWhoTo).isFullMember((VoteSourceTypes)iI))
	            {
	                bCanTrade = false;
	            }
	        }
	    }
	}
//FfH: End Add

	switch (item.m_eItemType)
	{
	case TRADE_TECHNOLOGIES:
		if (!(GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_TRADING)))
		{
			if (GC.getTechInfo((TechTypes)(item.m_iData)).isTrade())
			{
				if (GET_TEAM(getTeam()).isHasTech((TechTypes)(item.m_iData)) && !(GET_TEAM(getTeam()).isNoTradeTech((TechTypes)(item.m_iData)))

//FfH: Added by Kael 11/20/2007
                  && bCanTrade
//FfH: End Add

				  )
				{
					if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasTech((TechTypes)(item.m_iData)))
					{
						//if (GET_PLAYER(eWhoTo).isHuman() || (GET_PLAYER(eWhoTo).getCurrentResearch() != item.m_iData))
						{
							if (GET_TEAM(getTeam()).isTechTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isTechTrading())
							{
								FAssertMsg(item.m_iData >= 0, "item.m_iData is expected to be non-negative (invalid Index)");

								if (GET_PLAYER(eWhoTo).canResearch(((TechTypes)item.m_iData), true))
								{
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
									bResult = true;
								}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
							}
						}
					}
				}
			}
		}
		break;

	case TRADE_RESOURCES:
		FAssertMsg(item.m_iData > -1, "iData is expected to be non-negative");
		
		// MNAI - Puppet States - barred from trading mana
		if (GC.getBonusInfo((BonusTypes) item.m_iData).isMana() && 
			(GET_PLAYER(eWhoTo).isPuppetState() || isPuppetState()))
		{
			return false;
		}
		// MNAI - End Puppet States

		if (canTradeNetworkWith(eWhoTo))
		{
			if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isBonusObsolete((BonusTypes) item.m_iData) && !GET_TEAM(getTeam()).isBonusObsolete((BonusTypes) item.m_iData))
			{
				bool bCanTradeAll = (isHuman() || getTeam() == GET_PLAYER(eWhoTo).getTeam() || GET_TEAM(getTeam()).isVassal(GET_PLAYER(eWhoTo).getTeam()));
				if (getNumTradeableBonuses((BonusTypes) item.m_iData) > (bCanTradeAll ? 0 : 1))
				{
					// if (GET_PLAYER(eWhoTo).getNumAvailableBonuses(eBonus) == 0)
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_CITIES:
		{
			if (getNumCities() == 1)
			{
				return false;
			}

			CvCity* pCityTraded = getCity(item.m_iData);

			if (NULL != pCityTraded && pCityTraded->getLiberationPlayer(false) == eWhoTo)
			{
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
				bResult = true;
			}
			else if (GET_PLAYER(eWhoTo).canReceiveTradeCity())
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
			{
				if (0 == GC.getGameINLINE().getMaxCityElimination())
				{
					//if (!GET_TEAM(getTeam()).isAVassal() && !GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassal(getTeam()))
					if (!GET_TEAM(getTeam()).isAVassal())
					{
						if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isAVassal() ||
							GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassal(getTeam()))
						{
							pOurCapitalCity = getCapitalCity();
							if (pOurCapitalCity != NULL)
							{
								if (pOurCapitalCity->getID() != item.m_iData)
								{
									return true;
								}
							}
						}
					}
				}
			}
		}
		break;
/************************************************************************************************/
/* Afforess	                  Start		 07/29/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
    case TRADE_WORKER:
        {
            pUnitTraded = getUnit(item.m_iData);
            pTheirCapitalCity = GET_PLAYER(eWhoTo).getCapitalCity();
			if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
			{
				if (GC.getDefineINT("CAN_TRADE_WORKERS") > 0)
				{
					if (GET_TEAM(getTeam()).isHasEmbassy(GET_PLAYER(eWhoTo).getTeam()))
					{
						if (pUnitTraded != NULL)
						{
							if (GC.getUnitInfo(pUnitTraded->getUnitType()).isWorkerTrade() && pUnitTraded->canMove()/* && (pTradingCity != NULL) */&& (pTheirCapitalCity != NULL))
							{
								if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isUnitClassMaxedOut(pUnitTraded->getUnitClassType(), GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).getUnitClassMaking(pUnitTraded->getUnitClassType())))
								{
									if (!GET_PLAYER(eWhoTo).isUnitClassMaxedOut(pUnitTraded->getUnitClassType(), GET_PLAYER(eWhoTo).getUnitClassMaking(pUnitTraded->getUnitClassType())))
									{
										return true;
									}
								}
							}
						}
					}
				}
			}
		}
        break;

    case TRADE_MILITARY_UNIT:
        {
            pUnitTraded = getUnit(item.m_iData);
            pTheirCapitalCity = GET_PLAYER(eWhoTo).getCapitalCity();
			
			if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
			{
				if (GET_TEAM(getTeam()).isHasEmbassy(GET_PLAYER(eWhoTo).getTeam()))
				{
					if (pUnitTraded != NULL)
					{
						UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(GET_PLAYER(eWhoTo).getCivilizationType()).getCivilizationUnits(pUnitTraded->getUnitClassType());
						if ( NO_UNIT != eUnit )
				//		if (GET_PLAYER(eWhoTo).canTrain(eUnit))
						{
							pTradingCity = pUnitTraded->plot()->getPlotCity();
							if (GC.getUnitInfo(pUnitTraded->getUnitType()).isMilitaryTrade() && pUnitTraded->canMove() && (pTradingCity != NULL) && (pTheirCapitalCity != NULL))
							{
								if (pTradingCity->getOwnerINLINE() == getID())
								{
									if (pTradingCity->isConnectedTo(pTheirCapitalCity))
									{
										if (pTradingCity->isRevealed(GET_PLAYER(eWhoTo).getTeam(), true))
										{
											if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isUnitClassMaxedOut(pUnitTraded->getUnitClassType(), GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).getUnitClassMaking(pUnitTraded->getUnitClassType())))
											{
												if (!GET_PLAYER(eWhoTo).isUnitClassMaxedOut(pUnitTraded->getUnitClassType(), GET_PLAYER(eWhoTo).getUnitClassMaking(pUnitTraded->getUnitClassType())))
												{
													return true;
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
        break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	case TRADE_GOLD:
		if (GET_TEAM(getTeam()).isGoldTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isGoldTrading())
		{
			if (getGold() >= item.m_iData)
			{
				return true;
			}
		}
		break;

	case TRADE_GOLD_PER_TURN:
		if (GET_TEAM(getTeam()).isGoldTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isGoldTrading())
		{
			return true;
		}
		break;

	case TRADE_MAPS:
		if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
		{
			if (GET_TEAM(getTeam()).isMapTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isMapTrading())
			{
				return true;
			}
		}
		break;

	case TRADE_VASSAL:
	case TRADE_SURRENDER:
		//if (!isHuman() || GET_PLAYER(eWhoTo).isHuman()) //  human can't be vassal of AI
		if (1 < 2) // human as vassal
		{
			CvTeam& kVassalTeam = GET_TEAM(getTeam());
			CvTeam& kMasterTeam = GET_TEAM(GET_PLAYER(eWhoTo).getTeam());
			if (kMasterTeam.isVassalStateTrading()) // the master must possess the tech
			{
				if (!kVassalTeam.isAVassal() && !kMasterTeam.isAVassal() && getTeam() != GET_PLAYER(eWhoTo).getTeam())
				{
					if ((kMasterTeam.isAtWar(getTeam()) || item.m_iData == 1) && item.m_eItemType == TRADE_SURRENDER)
					{
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
						bResult = true;
					}
					else if (!kMasterTeam.isAtWar(getTeam()) && item.m_eItemType == TRADE_VASSAL)
					{
						bResult = true;
					}
				}
			}
		}
		break;

    case TRADE_EMBASSY:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (getNumCities() == 0)
			{
				return false;
			}

			if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
			{
				if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
				{
					if (!(GET_TEAM(getTeam()).isHasEmbassy(GET_PLAYER(eWhoTo).getTeam())))
					{
						if (GET_TEAM(getTeam()).isEmbassyTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isEmbassyTrading())
						{
							if (getCapitalCity() != NULL && GET_PLAYER(eWhoTo).getCapitalCity() != NULL)
							{
								return true;
							}
						}
					}
				}
			}
		}
		break;

    case TRADE_CONTACT:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (!GET_TEAM((TeamTypes)item.m_iData).isMinorCiv())
			{
				if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)))
				{
					return true;
				}
			}
		}
        break;

	case TRADE_WAR_REPARATIONS:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS) && GC.getDefineINT("CAN_TRADE_WAR_REPARATIONS") > 0)
		{
			if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isAtWar(getTeam()))
			{
				if (GET_PLAYER(eWhoTo).canTradeWarReparations((PlayerTypes)getID()))
				{
					bResult = true;
				}
			}
		}
        break;

    case TRADE_CORPORATION:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (hasHeadquarters((CorporationTypes)(item.m_iData)))
			{
				if (GET_PLAYER(eWhoTo).getBestHQCity((CorporationTypes)(item.m_iData)) != NULL)
				{
					if (GET_PLAYER(eWhoTo).isActiveCorporation((CorporationTypes)(item.m_iData)))
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_SECRETARY_GENERAL_VOTE:
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	case TRADE_PEACE:
		if (!(GET_TEAM(getTeam()).isHuman()))
		{
			if (!(GET_TEAM(getTeam()).isAVassal()))
			{
				if (GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)))
				{
					if (atWar(getTeam(), ((TeamTypes)(item.m_iData))))
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_WAR:
		// lfgr 08/2023
		if( GC.getDefineINT( "NO_WAR_TRADE", 0 ) ) {
			return false;
		}
		if (!(GET_TEAM(getTeam()).isHuman()))
		{
			if (!(GET_TEAM(getTeam()).isAVassal()))
			{
				if (!GET_TEAM((TeamTypes)item.m_iData).isAVassal())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)))
					{
/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
					// lfgr 06/2019: Cannot trade war against somebody with whom we are already at war
					// lfgr 04/2022: Change to canDeclareWar(), since canDeclareWarWithoutSenate() does nothing.
					//	if (GET_TEAM(getTeam()).canDeclareWarWithoutSenate((TeamTypes)(item.m_iData)))
						if( !atWar(getTeam(), ((TeamTypes)(item.m_iData))) &&
							GET_TEAM(getTeam()).canDeclareWar((TeamTypes)(item.m_iData)) )
					// lfgr END
						{
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/
							return true;
						}
					}
				}
			}
		}
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	case TRADE_WAR_PREPARE: // byFra
		// lfgr 08/2023
		if( GC.getDefineINT( "NO_WAR_TRADE", 0 ) ) {
			return false;
		}
		if (!(GET_TEAM(getTeam()).isHuman()))
		{
			if (!(GET_TEAM(getTeam()).isAVassal()))
			{
				if (!GET_TEAM((TeamTypes)item.m_iData).isAVassal())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)))
					{
						if (GET_TEAM(getTeam()).canDeclareWar((TeamTypes)(item.m_iData)))
						{
							if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasPrepareWar((TeamTypes)(item.m_iData)))
							{
								return true;
							}
						}
					}
				}
			}
		}
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/
	case TRADE_EMBARGO:
		if (!(GET_TEAM(getTeam()).isHuman()))
		{
			if (GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)))
			{
				if (canStopTradingWithTeam((TeamTypes)(item.m_iData)))
				{
					return true;
				}
			}
		}
		break;

	case TRADE_CIVIC:
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                          denev & jdog5000    */
/*                                                                                              */
/* Diplomacy                                                                                    */
/************************************************************************************************/
/* original bts code
		if (!(GET_TEAM(getTeam()).isHuman()))
*/
		if (!(GET_TEAM(getTeam()).isHuman()) || (getTeam() == GET_PLAYER(eWhoTo).getTeam()))
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
		{
			if (GET_PLAYER(eWhoTo).isCivic((CivicTypes)(item.m_iData)))
			{
				if (canDoCivics((CivicTypes)(item.m_iData)) && !isCivic((CivicTypes)(item.m_iData)))
				{
					if (canRevolution(NULL))
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_RELIGION:
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                          denev & jdog5000    */
/*                                                                                              */
/* Diplomacy                                                                                    */
/************************************************************************************************/
/* original bts code
		if (!(GET_TEAM(getTeam()).isHuman()))
*/
		if (!(GET_TEAM(getTeam()).isHuman()) || (getTeam() == GET_PLAYER(eWhoTo).getTeam()))
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
		{
			if (GET_PLAYER(eWhoTo).getStateReligion() == ((ReligionTypes)(item.m_iData)))
			{
				if (canConvert((ReligionTypes)(item.m_iData)))
				{
					return true;
				}
			}
		}
		break;

	case TRADE_OPEN_BORDERS:
		if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
		{
			if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
			{
				if (!(GET_TEAM(getTeam()).isOpenBorders(GET_PLAYER(eWhoTo).getTeam())))
				{
					if (GET_TEAM(getTeam()).isOpenBordersTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isOpenBordersTrading())
					{
/************************************************************************************************/
/* Afforess	                  Start		 06/16/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
						if (GET_TEAM(getTeam()).canSignOpenBorders(GET_PLAYER(eWhoTo).getTeam()))
						{
							return true;
						}
					}
				}
			}
		}
		break;
	
	case TRADE_RIGHT_OF_PASSAGE:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (getNumCities() == 0)
			{
				return false;
			}

			if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
			{
				if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
				{
					if (!(GET_TEAM(getTeam()).isOpenBorders(GET_PLAYER(eWhoTo).getTeam())) && !(GET_TEAM(getTeam()).isLimitedBorders(GET_PLAYER(eWhoTo).getTeam())))
					{
						if (GET_TEAM(getTeam()).isLimitedBordersTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isLimitedBordersTrading())
						{
							return true;
						}
					}
				}
			}
		}
		break;

	case TRADE_FREE_TRADE_ZONE:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
			{
				if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
				{
					if (GET_TEAM(getTeam()).canSignFreeTradeAgreement(GET_PLAYER(eWhoTo).getTeam()))
					{
						if (GET_TEAM(getTeam()).isFreeTradeAgreementTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isFreeTradeAgreementTrading())
						{
							if (!GET_TEAM(getTeam()).isFreeTradeAgreement(GET_PLAYER(eWhoTo).getTeam()))
							{
								return true;
							}
						}
					}
				}
			}
		}
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */	
/************************************************************************************************/

	case TRADE_DEFENSIVE_PACT:
		if (!(GET_TEAM(getTeam()).isAVassal()) && !(GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isAVassal()))
		{
			if (getTeam() != GET_PLAYER(eWhoTo).getTeam() && !GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassal(getTeam()))
			{
				if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
				{
					if (!(GET_TEAM(getTeam()).isDefensivePact(GET_PLAYER(eWhoTo).getTeam())))
					{
						if (GET_TEAM(getTeam()).isDefensivePactTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isDefensivePactTrading())
						{
							if ((GET_TEAM(getTeam()).getAtWarCount(true) == 0) && (GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).getAtWarCount(true) == 0))
							{
								if (GET_TEAM(getTeam()).canSignDefensivePact(GET_PLAYER(eWhoTo).getTeam()))
								{
									return true;
								}
							}
						}
					}
				}
			}
		}
		break;

	case TRADE_PERMANENT_ALLIANCE:
		if (!(GET_TEAM(getTeam()).isAVassal()) && !(GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isAVassal()))
		{
			if (getTeam() != GET_PLAYER(eWhoTo).getTeam() && !GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassal(getTeam()))
			{
				if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
				{
					if (GET_TEAM(getTeam()).isPermanentAllianceTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isPermanentAllianceTrading())
					{
						if ((GET_TEAM(getTeam()).getNumMembers() == 1) && (GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).getNumMembers() == 1))
						{
							return true;
						}
					}
				}
			}
		}
		break;
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	case TRADE_PEACE_TREATY:
		bResult = true;
		break;

	case TRADE_NON_AGGRESSION:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			// lfgr 04/2021: Removed unncessary loop, don't allow for vassals
			if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
			{
				if ( !GET_TEAM(getTeam()).isAVassal() && !GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isAVassal() )
				{
					if (GET_TEAM(getTeam()).isHasEmbassy(GET_PLAYER(eWhoTo).getTeam()))
					{
						if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
						{	
							if (!(GET_TEAM(getTeam()).isHasNonAggression(GET_PLAYER(eWhoTo).getTeam())))
							{
								if (GET_TEAM(getTeam()).canSignNonAggression(GET_PLAYER(eWhoTo).getTeam()))
								{
									if (GET_TEAM(getTeam()).isNonAggressionTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isNonAggressionTrading())
									{
										if (getCapitalCity() != NULL && GET_PLAYER(eWhoTo).getCapitalCity() != NULL)
										{
											return true;								
										}
									}
								}
							}
						}
					}
				}
			}
		}
		break;
	
	case TRADE_POW:
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
			{
				if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
				{
					if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
					{	
						if (!(GET_TEAM(getTeam()).isHasPOW(GET_PLAYER(eWhoTo).getTeam())))
						{
							if (GET_TEAM(getTeam()).canSignPOW(GET_PLAYER(eWhoTo).getTeam()))
							{							
								if (GET_TEAM(getTeam()).isPOWTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isPOWTrading())
								{
									if (GET_TEAM(getTeam()).AI_getMemoryCount(GET_PLAYER(eWhoTo).getTeam(), MEMORY_DECLARED_WAR) > 0 || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).AI_getMemoryCount(getTeam(), MEMORY_DECLARED_WAR) > 0)
									{
										if (!(GET_TEAM(getTeam()).AI_getMemoryCount(GET_PLAYER(eWhoTo).getTeam(), MEMORY_TRADED_POW) > 0))
										{	
											if (!(GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).AI_getMemoryCount(getTeam(), MEMORY_TRADED_POW) > 0))
											{
												if (getCapitalCity() != NULL && GET_PLAYER(eWhoTo).getCapitalCity() != NULL)
												{
													return true;								
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
		break;
	}
	if (bTestDenial && bResult)
	{
		bResult &= (getTradeDenial(eWhoTo, item) == NO_DENIAL);
	}

	return bResult;
}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

DenialTypes CvPlayer::getTradeDenial(PlayerTypes eWhoTo, TradeData item) const
{
	CvCity* pCity;
	
	const CvTeamAI& kOurTeam = GET_TEAM(getTeam());

	switch (item.m_eItemType)
	{
	case TRADE_TECHNOLOGIES:
		return kOurTeam.AI_techTrade(((TechTypes)(item.m_iData)), GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_RESOURCES:
		return AI_bonusTrade(((BonusTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_CITIES:
		pCity = getCity(item.m_iData);
		if (pCity != NULL)
		{
			return AI_cityTrade(pCity, eWhoTo);
		}
		break;

	case TRADE_GOLD:
	case TRADE_GOLD_PER_TURN:
		break;

	case TRADE_MAPS:
		return kOurTeam.AI_mapTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_SURRENDER:
		return kOurTeam.AI_surrenderTrade(GET_PLAYER(eWhoTo).getTeam(), 140);
		break;

	case TRADE_VASSAL:
		return kOurTeam.AI_vassalTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_PEACE:
		return kOurTeam.AI_makePeaceTrade(((TeamTypes)(item.m_iData)), GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_WAR:
		return kOurTeam.AI_declareWarTrade(((TeamTypes)(item.m_iData)), GET_PLAYER(eWhoTo).getTeam());
		break;
		
/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	case TRADE_WAR_PREPARE:
		return GET_TEAM(getTeam()).AI_declareWarTrade(((TeamTypes)(item.m_iData)), GET_PLAYER(eWhoTo).getTeam());
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/

	case TRADE_EMBARGO:
		return AI_stopTradingTrade(((TeamTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_CIVIC:
		return AI_civicTrade(((CivicTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_RELIGION:
		return AI_religionTrade(((ReligionTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_OPEN_BORDERS:
		return kOurTeam.AI_openBordersTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_DEFENSIVE_PACT:
		return kOurTeam.AI_defensivePactTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_PERMANENT_ALLIANCE:
		return kOurTeam.AI_permanentAllianceTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_PEACE_TREATY:
		break;
		
/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
	case TRADE_NON_AGGRESSION:
		return GET_TEAM(getTeam()).AI_NonAggressionTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_POW:
		return GET_TEAM(getTeam()).AI_POWTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_RIGHT_OF_PASSAGE:
		return GET_TEAM(getTeam()).AI_LimitedBordersTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_FREE_TRADE_ZONE:
		return GET_TEAM(getTeam()).AI_FreeTradeAgreement(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_WORKER:
		{
			CvUnit* pUnit = getUnit(item.m_iData);
			if (pUnit != NULL)
			{
				return AI_workerTrade(pUnit, eWhoTo);
			}
		}
		break;

	case TRADE_MILITARY_UNIT:
		{
			CvUnit* pUnit = getUnit(item.m_iData);
			if (pUnit != NULL)
			{
				return AI_militaryUnitTrade(pUnit, eWhoTo);
			}
		}
		break;

	case TRADE_EMBASSY:
		return GET_TEAM(getTeam()).AI_embassyTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_CONTACT:
		return GET_TEAM(getTeam()).AI_contactTrade(((TeamTypes)item.m_iData), GET_PLAYER(eWhoTo).getTeam());
		break;
	case TRADE_WAR_REPARATIONS:
		return AI_tradeWarReparations((PlayerTypes)eWhoTo);
		break;
	case TRADE_CORPORATION:
		return AI_corporationTrade(((CorporationTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_SECRETARY_GENERAL_VOTE:
		return AI_secretaryGeneralTrade(((VoteSourceTypes)(item.m_iData)), eWhoTo);
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	}

	return NO_DENIAL;
}


bool CvPlayer::canTradeNetworkWith(PlayerTypes ePlayer) const
{
	CvCity* pOurCapitalCity;

	pOurCapitalCity = getCapitalCity();

	if (pOurCapitalCity != NULL)
	{
		if (pOurCapitalCity->isConnectedToCapital(ePlayer))
		{
			return true;
		}
	}

	return false;
}


int CvPlayer::getNumAvailableBonuses(BonusTypes eBonus) const
{

//FfH: Added by Kael 11/14/2007
// lfgr 06/2019: Fix NoBonus to apply to correct VoteSource
	for( int eVoteSource = 0; eVoteSource < GC.getNumVoteSourceInfos(); eVoteSource++ )
	{
		if( isFullMember( (VoteSourceTypes) eVoteSource ) )
		{
			if( GC.getGameINLINE().isNoBonus( (VoteSourceTypes) eVoteSource, eBonus ) )
			{
				return 0;
			}
		}
	}
//FfH: End Add

	CvPlotGroup* pPlotGroup;
	CvCity* pCity = getCapitalCity();
	pPlotGroup = ((pCity) ? pCity->plot()->getOwnerPlotGroup() : NULL);

	if (pPlotGroup != NULL)
	{
		return pPlotGroup->getNumBonuses(eBonus);
	}

	return 0;
}


int CvPlayer::getNumTradeableBonuses(BonusTypes eBonus) const
{
	return (getNumAvailableBonuses(eBonus) - getBonusImport(eBonus));
}

bool CvPlayer::hasBonus(BonusTypes eBonus) const
{
	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->hasBonus(eBonus))
		{
			return true;
		}
	}

	return false;
}

int CvPlayer::getNumTradeBonusImports(PlayerTypes ePlayer) const
{
	CLLNode<TradeData>* pNode;
	CvDeal* pLoopDeal;
	int iCount;
	int iLoop;

	FAssert(ePlayer != getID());

	iCount = 0;

	for(pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if ((pLoopDeal->getFirstPlayer() == getID()) && (pLoopDeal->getSecondPlayer() == ePlayer))
		{
			for (pNode = pLoopDeal->headSecondTradesNode(); (pNode != NULL); pNode = pLoopDeal->nextSecondTradesNode(pNode))
			{
				if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
				{
					iCount++;
				}
			}
		}

		if ((pLoopDeal->getFirstPlayer() == ePlayer) && (pLoopDeal->getSecondPlayer() == getID()))
		{
			for (pNode = pLoopDeal->headFirstTradesNode(); (pNode != NULL); pNode = pLoopDeal->nextFirstTradesNode(pNode))
			{
				if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}


bool CvPlayer::isTradingWithTeam(TeamTypes eTeam, bool bIncludeCancelable) const
{
	int iLoop;

	if (eTeam == getTeam())
	{
		return false;
	}

	for (CvDeal* pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if (bIncludeCancelable || pLoopDeal->isCancelable(getID()))
		{
			if (!pLoopDeal->isPeaceDeal())
			{
				if ((pLoopDeal->getFirstPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getSecondPlayer()).getTeam() == eTeam))
				{
					if (pLoopDeal->getLengthFirstTrades() > 0)
					{
						return true;
					}
				}

				if ((pLoopDeal->getSecondPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getFirstPlayer()).getTeam() == eTeam))
				{
					if (pLoopDeal->getLengthSecondTrades() > 0)
					{
						return true;
					}
				}
			}
		}
	}

	return false;
}


bool CvPlayer::canStopTradingWithTeam(TeamTypes eTeam, bool bContinueNotTrading) const
{
	if (eTeam == getTeam())
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isVassal(eTeam))
	{
		return false;
	}

	if (!isTradingWithTeam(eTeam, false))
	{
		if (bContinueNotTrading && !isTradingWithTeam(eTeam, true))
		{
			return true;
		}

		return false;
	}

	return true;
}


void CvPlayer::stopTradingWithTeam(TeamTypes eTeam)
{
	CvDeal* pLoopDeal;
	int iLoop;
	int iI;

	FAssert(eTeam != getTeam());

	for(pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if (pLoopDeal->isCancelable(getID()) && !(pLoopDeal->isPeaceDeal()))
		{
			if (((pLoopDeal->getFirstPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getSecondPlayer()).getTeam() == eTeam)) ||
				  ((pLoopDeal->getSecondPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getFirstPlayer()).getTeam() == eTeam)))
			{
				pLoopDeal->kill();
			}
		}
	}

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam)
			{
				GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_STOPPED_TRADING, 1);
				GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_STOPPED_TRADING_RECENT, 1);
			}
		}
	}
}


void CvPlayer::killAllDeals()
{
	CvDeal* pLoopDeal;
	int iLoop;

	for(pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if ((pLoopDeal->getFirstPlayer() == getID()) || (pLoopDeal->getSecondPlayer() == getID()))
		{
			pLoopDeal->kill();
		}
	}
}


void CvPlayer::findNewCapital()
{
	CvCity* pOldCapital;
	CvCity* pLoopCity;
	CvCity* pBestCity;
	BuildingTypes eCapitalBuilding;
	int iValue;
	int iBestValue;
	int iLoop;
	
	eCapitalBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(GC.getDefineINT("CAPITAL_BUILDINGCLASS"))));

	if (eCapitalBuilding == NO_BUILDING)
	{
		return;
	}

	pOldCapital = getCapitalCity();

	iBestValue = 0;
	pBestCity = NULL;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity != pOldCapital)
		{
			if (0 == pLoopCity->getNumRealBuilding(eCapitalBuilding))
			{
				iValue = (pLoopCity->getPopulation() * 4);

				iValue += pLoopCity->getYieldRate(YIELD_FOOD);
				iValue += (pLoopCity->getYieldRate(YIELD_PRODUCTION) * 3);
				iValue += (pLoopCity->getYieldRate(YIELD_COMMERCE) * 2);
				iValue += pLoopCity->getCultureLevel();
				iValue += pLoopCity->getReligionCount();
				iValue += pLoopCity->getCorporationCount();
				iValue += (pLoopCity->getNumGreatPeople() * 2);

				iValue *= (pLoopCity->calculateCulturePercent(getID()) + 100);
				iValue /= 100;

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestCity = pLoopCity;
				}
			}
		}
	}

	if (pBestCity != NULL)
	{
		if (pOldCapital != NULL)
		{
			pOldCapital->setNumRealBuilding(eCapitalBuilding, 0);
		}
		FAssertMsg(!(pBestCity->getNumRealBuilding(eCapitalBuilding)), "(pBestCity->getNumRealBuilding(eCapitalBuilding)) did not return false as expected");
		pBestCity->setNumRealBuilding(eCapitalBuilding, 1);
	}
}


int CvPlayer::getNumGovernmentCenters() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isGovernmentCenter())
		{
			iCount++;
		}
	}

	return iCount;
}


bool CvPlayer::canRaze(CvCity* pCity) const
{
	if (!pCity->isAutoRaze())
	{
		if (GC.getGameINLINE().isOption(GAMEOPTION_NO_CITY_RAZING))
		{
			return false;
		}

		if (pCity->getOwnerINLINE() != getID())
		{
			return false;
		}

		if (pCity->calculateTeamCulturePercent(getTeam()) >= GC.getDefineINT("RAZING_CULTURAL_PERCENT_THRESHOLD"))
		{
			return false;
		}
	}

	CyCity* pyCity = new CyCity(pCity);
	CyArgsList argsList;
	argsList.add(getID());	// Player ID
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "canRazeCity", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 0)
	{
		return (false);
	}

	return true;
}


void CvPlayer::raze(CvCity* pCity)
{
	wchar szBuffer[1024];
	PlayerTypes eHighestCulturePlayer;
	int iI, iJ;

	if (!canRaze(pCity))
	{
		return;
	}

	FAssert(pCity->getOwnerINLINE() == getID());

	eHighestCulturePlayer = pCity->findHighestCulture();

	if (eHighestCulturePlayer != NO_PLAYER)
	{
		if (GET_PLAYER(eHighestCulturePlayer).getTeam() != getTeam())
		{
			GET_PLAYER(eHighestCulturePlayer).AI_changeMemoryCount(getID(), MEMORY_RAZED_CITY, 1);
		}
	}

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (pCity->isHolyCity((ReligionTypes)iI))
		{
			for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
			{
				if (GET_PLAYER((PlayerTypes)iJ).isAlive())
				{
					if (iJ != getID())
					{
						if (GET_PLAYER((PlayerTypes)iJ).getStateReligion() == ((ReligionTypes)iI))
						{
							GET_PLAYER((PlayerTypes)iJ).AI_changeMemoryCount(getID(), MEMORY_RAZED_HOLY_CITY, 1);
						}
					}
				}
			}
		}
	}

	swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_DESTROYED_CITY", pCity->getNameKey()).GetCString());
	gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYRAZE", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_GREEN"), pCity->getX_INLINE(), pCity->getY_INLINE(), true, true);

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (iI != getID())
			{
				if (pCity->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
				{
					swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_CITY_HAS_BEEN_RAZED_BY", pCity->getNameKey(), getCivilizationDescriptionKey()).GetCString());
					gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYRAZED", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pCity->getX_INLINE(), pCity->getY_INLINE(), true, true);
				}
			}
		}
	}

	swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_CITY_RAZED_BY", pCity->getNameKey(), getCivilizationDescriptionKey()).GetCString());
	GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, pCity->getX_INLINE(), pCity->getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));

//FfH Global Counter: Added by Kael 08/11/2007
    bool bValid = true;
   	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (pCity->isHasReligion((ReligionTypes)iI))
		{
		    if (GC.getReligionInfo((ReligionTypes)iI).getGlobalCounterSpread() > 0)
		    {
		        bValid = false;
		    }
		}
	}
    if (bValid)
    {
        int iCost = GC.getDefineINT("RAZE_COST_BASE");
        if ((pCity->getPopulation() - GC.getDefineINT("RAZE_COST_PER_POPULATION_OVER")) > 0)
        {
            iCost += (pCity->getPopulation() - GC.getDefineINT("RAZE_COST_PER_POPULATION_OVER")) * GC.getDefineINT("RAZE_COST_PER_POPULATION");
        }
        GC.getGameINLINE().changeGlobalCounter(iCost);
    }
   	for (iI = 0; iI < GC.getNumBuildingInfos(); iI++)
   	{
   	    if (pCity->getNumRealBuilding((BuildingTypes)iI) > 0)
   	    {
   	        if (GC.getBuildingInfo((BuildingTypes)iI).isEquipment())
   	        {
                for (int iJ = 0; iJ < GC.getNumUnitInfos(); iJ++)
                {
                    if (GC.getUnitInfo((UnitTypes)iJ).getBuildings(iI))
                    {
                        initUnit((UnitTypes)iJ, pCity->getX(), pCity->getY());
                    }
                }
   	        }
   	    }
   	}
//FfH: End Add

	// Report this event
	CvEventReporter::getInstance().cityRazed(pCity, getID());

	disband(pCity);
}


void CvPlayer::disband(CvCity* pCity)
{
	if (getNumCities() == 1)
	{
		setFoundedFirstCity(false);
	}

	GC.getGameINLINE().addDestroyedCityName(pCity->getName());

	pCity->kill(true);
}


bool CvPlayer::canReceiveGoody(CvPlot* pPlot, GoodyTypes eGoody, CvUnit* pUnit) const
{
	CvCity* pCity;
	UnitTypes eUnit;
	bool bTechFound;
	int iI;

	if (GC.getGoodyInfo(eGoody).getExperience() > 0)
	{
		if ((pUnit == NULL) || !(pUnit->canAcquirePromotionAny()) || (GC.getGameINLINE().getElapsedGameTurns() < 10))
		{
			return false;
		}
	}

	if (GC.getGoodyInfo(eGoody).getDamagePrereq() > 0)
	{
		if ((pUnit == NULL) || (pUnit->getDamage() < ((pUnit->maxHitPoints() * GC.getGoodyInfo(eGoody).getDamagePrereq()) / 100)))
		{
			return false;
		}
	}

	if (GC.getGoodyInfo(eGoody).isTech())
	{
		bTechFound = false;

		for (iI = 0; iI < GC.getNumTechInfos(); iI++)
		{
			if (GC.getTechInfo((TechTypes) iI).isGoodyTech())
			{
				if (canResearch((TechTypes)iI))
				{
					bTechFound = true;
					break;
				}
			}
		}

		if (!bTechFound)
		{
			return false;
		}
	}

	if (GC.getGoodyInfo(eGoody).isBad())
	{
		if ((pUnit == NULL) || pUnit->isNoBadGoodies())
		{
			return false;
		}
	}

	if (GC.getGoodyInfo(eGoody).getUnitClassType() != NO_UNITCLASS)
	{
	/************************************************************************************************/
	/* WILDERNESS                             08/2013                                 lfgr          */
	/* WildernessMisc                                                                               */
	/* Don't give world equipments twice                                                            */
	/************************************************************************************************/
		if( GC.getGameINLINE().isUnitClassMaxedOut( (UnitClassTypes) GC.getGoodyInfo(eGoody).getUnitClassType() ) )
			return false;
	/************************************************************************************************/
	/* WILDERNESS                                                                     END           */
	/************************************************************************************************/
		eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getGoodyInfo(eGoody).getUnitClassType())));

		if (eUnit == NO_UNIT)
		{
			return false;
		}

		if ((GC.getUnitInfo(eUnit).getCombat() > 0) && !(GC.getUnitInfo(eUnit).isOnlyDefensive()))
		{
			if (GC.getGameINLINE().isGameMultiPlayer() || (GC.getGameINLINE().getElapsedGameTurns() < 20))
			{
				return false;
			}
		}

		if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
		{
			if (GC.getUnitInfo(eUnit).isFound())
			{
				return false;
			}
		}
	}

	if (GC.getGoodyInfo(eGoody).getBarbarianUnitClass() != NO_UNITCLASS)
	{
		if (GC.getGameINLINE().isOption(GAMEOPTION_NO_BARBARIANS))
		{
			return false;
		}

		if (getNumCities() == 0)
		{
			return false;
		}

		if (getNumCities() == 1)
		{
			pCity = GC.getMapINLINE().findCity(pPlot->getX_INLINE(), pPlot->getY_INLINE(), NO_PLAYER, getTeam());

			if (pCity != NULL)
			{
				if (plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pCity->getX_INLINE(), pCity->getY_INLINE()) <= (8 - getNumCities()))
				{
					return false;
				}
			}
		}
	}

	return true;
}


void CvPlayer::receiveGoody(CvPlot* pPlot, GoodyTypes eGoody, CvUnit* pUnit)
{
	CvPlot* pLoopPlot;
	CvPlot* pBestPlot = NULL;
	CvWString szBuffer;
	CvWString szTempBuffer;
	TechTypes eBestTech;
	UnitTypes eUnit;
	int iGold;
	int iOffset;
	int iRange;
	int iBarbCount;
	int iValue;
	int iBestValue;
	int iPass;
	int iDX, iDY;
	int iI;

//FfH: Added by Kael 08/31/2008
    CvUnit* pNewUnit;
//FfH: End Add

//	FAssertMsg(canReceiveGoody(pPlot, eGoody, pUnit), "Instance is expected to be able to recieve goody"); //graveyards can also give goodys Sephi

	szBuffer = GC.getGoodyInfo(eGoody).getDescription();

	iGold = GC.getGoodyInfo(eGoody).getGold() + GC.getGameINLINE().getSorenRandNum(GC.getGoodyInfo(eGoody).getGoldRand1(), "Goody Gold 1") + GC.getGameINLINE().getSorenRandNum(GC.getGoodyInfo(eGoody).getGoldRand2(), "Goody Gold 2");
	iGold  = (iGold * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent()) / 100;

	if (iGold != 0)
	{
		changeGold(iGold);

		szBuffer += gDLL->getText("TXT_KEY_MISC_RECEIVED_GOLD", iGold);
	}

	iRange = GC.getGoodyInfo(eGoody).getMapRange();

	if (iRange > 0)
	{
		iOffset = GC.getGoodyInfo(eGoody).getMapOffset();

		if (iOffset > 0)
		{
			iBestValue = 0;
			pBestPlot = NULL;

			for (iDX = -(iOffset); iDX <= iOffset; iDX++)
			{
				for (iDY = -(iOffset); iDY <= iOffset; iDY++)
				{
					pLoopPlot = plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						if (!(pLoopPlot->isRevealed(getTeam(), false)))
						{
							iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Goody Map"));

							iValue *= plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());

							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								pBestPlot = pLoopPlot;
							}
						}
					}
				}
			}
		}

		if (pBestPlot == NULL)
		{
			pBestPlot = pPlot;
		}

		for (iDX = -(iRange); iDX <= iRange; iDX++)
		{
			for (iDY = -(iRange); iDY <= iRange; iDY++)
			{
				pLoopPlot = plotXY(pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), iDX, iDY);

				if (pLoopPlot != NULL)
				{
					if (plotDistance(pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE()) <= iRange)
					{
						if (GC.getGameINLINE().getSorenRandNum(100, "Goody Map") < GC.getGoodyInfo(eGoody).getMapProb())
						{
							pLoopPlot->setRevealed(getTeam(), true, false, NO_TEAM, true);
						}
					}
				}
			}
		}
	}

	if (pUnit != NULL)
	{

//FfH: Modified by Kael 08/31/2008
//        pUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());
        if (GC.getGoodyInfo(eGoody).getUnitClassType() == NO_UNITCLASS && GC.getGoodyInfo(eGoody).getBarbarianUnitClass() == NO_UNITCLASS)
        {
            pUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());
        }
//FfH: End Modify

	}

	if (pUnit != NULL)
	{
		pUnit->changeDamage(-(GC.getGoodyInfo(eGoody).getHealing()));
	}

	if (GC.getGoodyInfo(eGoody).isTech())
	{
		iBestValue = 0;
		eBestTech = NO_TECH;

		for (iI = 0; iI < GC.getNumTechInfos(); iI++)
		{
			if (GC.getTechInfo((TechTypes) iI).isGoodyTech())
			{
				if (canResearch((TechTypes)iI))
				{
					iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Goody Tech"));

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						eBestTech = ((TechTypes)iI);
					}
				}
			}
		}

		FAssertMsg(eBestTech != NO_TECH, "BestTech is not assigned a valid value");

		GET_TEAM(getTeam()).setHasTech(eBestTech, true, getID(), true, true);
		GET_TEAM(getTeam()).setNoTradeTech(eBestTech, true);

		szBuffer = gDLL->getText("TXT_KEY_GOODY_TECH", GC.getTechInfo((TechTypes)eBestTech).getDescription());
	}

	if (!szBuffer.empty())
	{
// BUG - Goody Hut Log - start
		// keep messages in event log forever
		gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getGoodyInfo(eGoody).getSound(), MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getImprovementArtInfo("ART_DEF_IMPROVEMENT_GOODY_HUT")->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), pPlot->getX_INLINE(), pPlot->getY_INLINE());
// BUG - Goody Hut Log - end
	}


	if (GC.getGoodyInfo(eGoody).getUnitClassType() != NO_UNITCLASS)
	{
		eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getGoodyInfo(eGoody).getUnitClassType());

//FfH: Modified by Kael 08/31/2008
//		if (eUnit != NO_UNIT)
//		{
//			initUnit(eUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE());
//		}
		if (eUnit == NO_UNIT)
		{
			eUnit = ((UnitTypes)(GC.getUnitClassInfo((UnitClassTypes)GC.getGoodyInfo(eGoody).getUnitClassType()).getDefaultUnitIndex()));
		}
	/************************************************************************************************/
	/* GP_NAMES                                 07/2013                                 lfgr        */
	/* Random name for GPs                                                                          */
	/************************************************************************************************/
	/*
        pNewUnit = initUnit(eUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE());
	*/
		int eName = getNewGreatPersonBornName( eUnit );
        pNewUnit = initUnit(eUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE(), NO_UNITAI, NO_DIRECTION, true, eName);
	/************************************************************************************************/
	/* GP_NAMES                                END                                                  */
	/************************************************************************************************/
        pNewUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());
//FfH: End Modify

	}

	if (GC.getGoodyInfo(eGoody).getBarbarianUnitClass() != NO_UNITCLASS)
	{
		iBarbCount = 0;
		eUnit = (UnitTypes)GC.getCivilizationInfo(GET_PLAYER(BARBARIAN_PLAYER).getCivilizationType()).getCivilizationUnits(GC.getGoodyInfo(eGoody).getBarbarianUnitClass());

		if (eUnit != NO_UNIT)
		{
			for (iPass = 0; iPass < 2; iPass++)
			{
				if (iBarbCount < GC.getGoodyInfo(eGoody).getMinBarbarians())
				{
					for (iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
					{
						pLoopPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), ((DirectionTypes)iI));

						if (pLoopPlot != NULL)
						{
							if (pLoopPlot->getArea() == pPlot->getArea())
							{
								if (!(pLoopPlot->isImpassable()))
								{
									if (pLoopPlot->getNumUnits() == 0)
									{
										if ((iPass > 0) || (GC.getGameINLINE().getSorenRandNum(100, "Goody Barbs") < GC.getGoodyInfo(eGoody).getBarbarianUnitProb()))
										{

//FfH: Modified by Kael 08/31/2008
//											GET_PLAYER(BARBARIAN_PLAYER).initUnit(eUnit, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), ((pLoopPlot->isWater()) ? UNITAI_ATTACK_SEA : UNITAI_ATTACK));
											pNewUnit = GET_PLAYER(BARBARIAN_PLAYER).initUnit(eUnit, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), ((pLoopPlot->isWater()) ? UNITAI_ATTACK_SEA : UNITAI_ATTACK));
                                            pNewUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());
//FfH: End Modify

											iBarbCount++;

											if ((iPass > 0) && (iBarbCount == GC.getGoodyInfo(eGoody).getMinBarbarians()))
											{
												break;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}


void CvPlayer::doGoody(CvPlot* pPlot, CvUnit* pUnit)
{
	CyPlot kGoodyPlot(pPlot);
	CyUnit kGoodyUnit(pUnit);
	CyArgsList argsList;
	argsList.add(getID());		// pass in this players ID
	argsList.add(gDLL->getPythonIFace()->makePythonObject(&kGoodyPlot));
	argsList.add(gDLL->getPythonIFace()->makePythonObject(&kGoodyUnit));

	long result=0;
	bool ok = gDLL->getPythonIFace()->callFunction(PYGameModule, "doGoody", argsList.makeFunctionArgs(), &result);
	if (ok && result)
	{
		return;
	}

	FAssertMsg(pPlot->isGoody(), "pPlot->isGoody is expected to be true");

	pPlot->removeGoody();
	if (!isBarbarian())
	{
		for (int iI = 0; iI < GC.getDefineINT("NUM_DO_GOODY_ATTEMPTS"); iI++)
		{
			if (GC.getHandicapInfo(getHandicapType()).getNumGoodies() > 0)
			{
				GoodyTypes eGoody = (GoodyTypes)GC.getHandicapInfo(getHandicapType()).getGoodies(GC.getGameINLINE().getSorenRandNum(GC.getHandicapInfo(getHandicapType()).getNumGoodies(), "Goodies"));

				FAssert(eGoody >= 0);
				FAssert(eGoody < GC.getNumGoodyInfos());

				if (canReceiveGoody(pPlot, eGoody, pUnit))
				{
					receiveGoody(pPlot, eGoody, pUnit);

					// Python Event
					CvEventReporter::getInstance().goodyReceived(getID(), pPlot, pUnit, eGoody);
					break;
				}
			}
		}
	}
}


bool CvPlayer::canFound(int iX, int iY, bool bTestVisible) const
{
	CvPlot* pPlot;
	CvPlot* pLoopPlot;
	bool bValid;
	int iRange;
	int iDX, iDY;

	pPlot = GC.getMapINLINE().plotINLINE(iX, iY);

	long lResult=0;
	if(GC.getUSE_CANNOT_FOUND_CITY_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add((int)getID());
		argsList.add(iX);
		argsList.add(iY);
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotFoundCity", argsList.makeFunctionArgs(), &lResult);

		if (lResult == 1)
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isFinalInitialized())
	{
		if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
		{
			if (getNumCities() > 0)
			{
				return false;
			}
		}
	}

	// lfgr fix 05/2020
	if( pPlot->isFoundDisabled() ) {
		return false;
	}

	if (pPlot->isImpassable())
	{
		return false;
	}

	if (pPlot->getFeatureType() != NO_FEATURE)
	{
		if (GC.getFeatureInfo(pPlot->getFeatureType()).isNoCity())
		{
			return false;
		}
	}

	if (pPlot->isOwned() && (pPlot->getOwnerINLINE() != getID()))
	{
		return false;
	}

	bValid = false;

	if (!bValid)
	{
		if (GC.getTerrainInfo(pPlot->getTerrainType()).isFound())
		{
			bValid = true;
		}
	}

	if (!bValid)
	{
		if (GC.getTerrainInfo(pPlot->getTerrainType()).isFoundCoast())
		{
			if (pPlot->isCoastalLand())
			{
				bValid = true;
			}
		}
	}

	if (!bValid)
	{
		if (GC.getTerrainInfo(pPlot->getTerrainType()).isFoundFreshWater())
		{
			if (pPlot->isFreshWater())
			{
				bValid = true;
			}
		}
	}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       02/16/10                    EmperorFool & jdog5000    */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// EF: canFoundCitiesOnWater callback handling was incorrect and ignored isWater() if it returned true
	if (pPlot->isWater())
	{
		if(GC.getUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK())
		{
			bValid = false;

			CyArgsList argsList2;
			argsList2.add(iX);
			argsList2.add(iY);
			lResult=0;
			gDLL->getPythonIFace()->callFunction(PYGameModule, "canFoundCitiesOnWater", argsList2.makeFunctionArgs(), &lResult);

			if (lResult == 1)
			{
				bValid = true;
			}
		}
	}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	if (!bValid)
	{
		return false;
	}

	if (!bTestVisible)
	{
		iRange = GC.getMIN_CITY_RANGE();

		for (iDX = -(iRange); iDX <= iRange; iDX++)
		{
			for (iDY = -(iRange); iDY <= iRange; iDY++)
			{
				pLoopPlot	= plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY);

				if (pLoopPlot != NULL)
				{
					if (pLoopPlot->isCity())
					{
						if (pLoopPlot->area() == pPlot->area())
						{
							return false;
						}
					}
				}
			}
		}
	}

//FfH: Added by Kael 04/06/2010
	if (pPlot->getImprovementType() != NO_IMPROVEMENT)
	{
	    if (GC.getImprovementInfo((ImprovementTypes)pPlot->getImprovementType()).isPermanent())
	    {
	        return false;
	    }
	}
	if (pPlot->getBonusType() != NO_BONUS)
	{
        if (GC.getDefineINT("BONUSCLASS_MANA") != -1)
        {
            if (GC.getBonusInfo((BonusTypes)pPlot->getBonusType()).getBonusClassType()==GC.getDefineINT("BONUSCLASS_MANA"))
            {
                return false;
            }
	    }
        if (GC.getDefineINT("BONUSCLASS_MANA_RAW") != -1)
        {
            if (GC.getBonusInfo((BonusTypes)pPlot->getBonusType()).getBonusClassType()==GC.getDefineINT("BONUSCLASS_MANA_RAW"))
            {
                return false;
            }
	    }
	}
    if (pPlot->isVisibleEnemyUnit(getID()))
    {
        return false;
    }
//FfH: End Add

	return true;
}


void CvPlayer::found(int iX, int iY)
{
	CvCity* pCity;
	BuildingTypes eLoopBuilding;
	UnitTypes eDefenderUnit;
	int iI;

	if (!canFound(iX, iY))
	{
		return;
	}

	pCity = initCity(iX, iY, true, true);
	FAssertMsg(pCity != NULL, "City is not assigned a valid value");

	if (isBarbarian())
	{
		eDefenderUnit = pCity->AI_bestUnitAI(UNITAI_CITY_DEFENSE);

		if (eDefenderUnit == NO_UNIT)
		{
			eDefenderUnit = pCity->AI_bestUnitAI(UNITAI_ATTACK);
		}

		if (eDefenderUnit != NO_UNIT)
		{
			for (iI = 0; iI < GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getBarbarianInitialDefenders(); iI++)
			{
				initUnit(eDefenderUnit, iX, iY, UNITAI_CITY_DEFENSE);
			}
		}
	}

	for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		eLoopBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI)));

		if (eLoopBuilding != NO_BUILDING)
		{
			if (GC.getBuildingInfo(eLoopBuilding).getFreeStartEra() != NO_ERA)
			{
				if (GC.getGameINLINE().getStartEra() >= GC.getBuildingInfo(eLoopBuilding).getFreeStartEra())
				{
					if (pCity->canConstruct(eLoopBuilding))
					{
						pCity->setNumRealBuilding(eLoopBuilding, 1);
					}
				}
			}
		}
	}

	if (getAdvancedStartPoints() >= 0)
	{
		// Free border expansion for Creative
		bool bCreative = false;
		for (iI = 0; iI < GC.getNumTraitInfos(); ++iI)
		{
			if (hasTrait((TraitTypes)iI))
			{
				if (GC.getTraitInfo((TraitTypes)iI).getCommerceChange(COMMERCE_CULTURE) > 0)
				{
					bCreative = true;
					break;
				}

			}
		}

		if (bCreative)
		{
			for (iI = 0; iI < GC.getNumCultureLevelInfos(); ++iI)
			{
				int iCulture = GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)iI);
				if (iCulture > 0)
				{
					pCity->setCulture(getID(), iCulture, true, true);
					break;
				}
			}
		}
	}

	// lfgr: merged from MoM
	// Sephi default value for avoid angry Citizens
	// lfgr 10/2020: Made optional, added unhealthy citizens
	if( GC.getInfoTypeForString("EMPHASIZE_AVOID_ANGRY_CITIZENS")!=NO_EMPHASIZE
			&& getBugOptionBOOL( "FfHUI__AvoidAngryCitizensDefault", true, "BUG_AVOID_ANGRY_CITIZENS_DEFAULT" ) ) {
		CvMessageControl::getInstance().sendDoTask(pCity->getID(), TASK_SET_EMPHASIZE, GC.getInfoTypeForString("EMPHASIZE_AVOID_ANGRY_CITIZENS"), -1, true, false, false, false);
	}
	if( GC.getInfoTypeForString("EMPHASIZE_AVOID_UNHEALTHY_CITIZENS")!=NO_EMPHASIZE
			&& getBugOptionBOOL( "FfHUI__AvoidUnhealthyCitizensDefault", false, "BUG_AVOID_UNHEALTHY_CITIZENS_DEFAULT" ) ) {
		CvMessageControl::getInstance().sendDoTask(pCity->getID(), TASK_SET_EMPHASIZE, GC.getInfoTypeForString("EMPHASIZE_AVOID_UNHEALTHY_CITIZENS"), -1, true, false, false, false);
	}
	// lfgr end

	if (isHuman() && getAdvancedStartPoints() < 0)
	{
		pCity->chooseProduction();
	}
	else
	{
		pCity->doFoundMessage();
	}

	CvEventReporter::getInstance().cityBuilt(pCity);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/02/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
	if( gPlayerLogLevel >= 1 )
	{
		logBBAI("  Player %d (%S) founds new city %S at %d, %d", getID(), getCivilizationDescription(0), pCity->getName(0).GetCString(), iX, iY );
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
}


// bTestVisible: only testing whether visible e.g. in city screen (weaker conditions!)
bool CvPlayer::canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible, bool bIgnoreCost) const
{
	PROFILE_FUNC();

	CvUnitInfo& kUnit = GC.getUnitInfo(eUnit);
	UnitClassTypes eUnitClass = (UnitClassTypes)kUnit.getUnitClassType();
	int iI;

	//FAssert(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) == eUnit);

//FfH: Modified by Kael 05/09/2008
//	if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) != eUnit)
//	{
//		return false;
//	}
//FfH: End Modify

	if (GC.getUnitClassInfo(eUnitClass).getMaxGlobalInstances() == 1)
	{
		if (isPuppetState())
		{
			return false;
		}
	}

	if (!bIgnoreCost)
	{
		if (kUnit.getProductionCost() == -1)
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		if (kUnit.isFound())
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		if (kUnit.isSpy() || kUnit.getEspionagePoints() > 0)
		{
			return false;
		}
	}

	if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(kUnit.getPrereqAndTech()))))
	{
		return false;
	}

	for (iI = 0; iI < GC.getNUM_UNIT_AND_TECH_PREREQS(); iI++)
	{
		if (kUnit.getPrereqAndTechs(iI) != NO_TECH)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(kUnit.getPrereqAndTechs(iI)))))
			{
				return false;
			}
		}
	}

	if (kUnit.getStateReligion() != NO_RELIGION)
	{
		if (getStateReligion() != kUnit.getStateReligion())
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isUnitClassMaxedOut(eUnitClass))
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isUnitClassMaxedOut(eUnitClass))
	{
		return false;
	}

	if (isUnitClassMaxedOut(eUnitClass))
	{
		return false;
	}

	if (!bTestVisible)
	{
		if (GC.getGameINLINE().isUnitClassMaxedOut(eUnitClass, (GET_TEAM(getTeam()).getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GET_TEAM(getTeam()).isUnitClassMaxedOut(eUnitClass, (GET_TEAM(getTeam()).getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (isUnitClassMaxedOut(eUnitClass, (getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GC.getGameINLINE().isNoNukes() || !GC.getGameINLINE().isNukesValid())
		{
			if (kUnit.getNukeRange() != -1)
			{
				return false;
			}
		}

		if (kUnit.getSpecialUnitType() != NO_SPECIALUNIT)
		{
			if (!(GC.getGameINLINE().isSpecialUnitValid((SpecialUnitTypes)(kUnit.getSpecialUnitType()))))
			{
				return false;
			}
		}
	}

//FfH Units: Added by Kael 08/04/2007
	if (kUnit.getPrereqCivic() != NO_CIVIC)
	{
	    bool bValid = false;
        for (iI = 0; iI < GC.getDefineINT("MAX_CIVIC_OPTIONS"); iI++)
        {
            if (getCivics((CivicOptionTypes)iI) == kUnit.getPrereqCivic())
            {
                bValid = true;
            }
        }
        if (bValid == false)
        {
            return false;
        }
	}
	if (kUnit.getPrereqGlobalCounter() != 0)
	{
        if (GC.getGameINLINE().getGlobalCounter() < kUnit.getPrereqGlobalCounter())
        {
            return false;
        }
	}
	if (kUnit.getPrereqAlignment() != NO_ALIGNMENT)
	{
        if (getAlignment() != kUnit.getPrereqAlignment())
        {
            return false;
        }
	}

	// Tholal AI - prereq civs
	if (kUnit.getPrereqCiv() != NO_CIVILIZATION)
	{
        if (getCivilizationType() != kUnit.getPrereqCiv())
        {
			if (!isAssimilation() || (GC.getUnitClassInfo(eUnitClass).getMaxGlobalInstances() > 0))
			{
	            return false;
			}
        }
//FfH: End Add
	}


	return true;
}


bool CvPlayer::canConstruct(BuildingTypes eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost) const
{
	BuildingClassTypes eBuildingClass;
	int iI;
	CvTeamAI& currentTeam = GET_TEAM(getTeam());

	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);

	eBuildingClass = ((BuildingClassTypes)(kBuilding.getBuildingClassType()));

//	FAssert(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass) == eBuilding); //modified Sephi

//FfH: Modified by Kael 07/05/2008
//	if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass) != eBuilding)
//	{
//		return false;
//	}
//FfH: End Modify

	if (!bIgnoreCost)
	{
		if (kBuilding.getProductionCost() == -1)
		{
			return false;
		}
	}

	if (!(currentTeam.isHasTech((TechTypes)(kBuilding.getPrereqAndTech()))))
	{
		return false;
	}

	for (iI = 0; iI < GC.getNUM_BUILDING_AND_TECH_PREREQS(); iI++)
	{
		if (kBuilding.getPrereqAndTechs(iI) != NO_TECH)
		{
			if (!(currentTeam.isHasTech((TechTypes)(kBuilding.getPrereqAndTechs(iI)))))
			{
				return false;
			}
		}
	}

	if (currentTeam.isObsoleteBuilding(eBuilding))
	{
		return false;
	}

	if (kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING)
	{
		if (!(currentTeam.isHasTech((TechTypes)(GC.getSpecialBuildingInfo((SpecialBuildingTypes) kBuilding.getSpecialBuildingType()).getTechPrereq()))))
		{
			return false;
		}
	}

	if (kBuilding.getStateReligion() != NO_RELIGION)
	{
		if (getStateReligion() != kBuilding.getStateReligion())
		{
			return false;
		}
	}

	if (GC.getGameINLINE().countCivTeamsEverAlive() < kBuilding.getNumTeamsPrereq())
	{
		return false;
	}

	if (kBuilding.getVictoryPrereq() != NO_VICTORY)
	{
		if (!(GC.getGameINLINE().isVictoryValid((VictoryTypes)(kBuilding.getVictoryPrereq()))))
		{
			return false;
		}

		if (isMinorCiv())
		{
			return false;
		}

		if (currentTeam.getVictoryCountdown((VictoryTypes)kBuilding.getVictoryPrereq()) >= 0)
		{
			return false;
		}
	}

	if (kBuilding.getMaxStartEra() != NO_ERA)
	{
		if (GC.getGameINLINE().getStartEra() > kBuilding.getMaxStartEra())
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isBuildingClassMaxedOut(eBuildingClass))
	{
		return false;
	}

	if (currentTeam.isBuildingClassMaxedOut(eBuildingClass))
	{
		return false;
	}

	if (isBuildingClassMaxedOut(eBuildingClass))
	{
		return false;
	}

	CvCivilizationInfo &civilizationInfo = GC.getCivilizationInfo(getCivilizationType());
	int numBuildingClassInfos = GC.getNumBuildingClassInfos();
	for (iI = 0; iI < numBuildingClassInfos; iI++)
	{
		BuildingTypes ePrereqBuilding = (BuildingTypes)civilizationInfo.getCivilizationBuildings(iI);

		if (NO_BUILDING != ePrereqBuilding && currentTeam.isObsoleteBuilding(ePrereqBuilding))
		{
			// MNAI - check team if prereq building is flagged as teamshare
			if (GC.getBuildingInfo(ePrereqBuilding).isTeamShare())
			{
				if (currentTeam.getBuildingClassCount((BuildingClassTypes)iI) < getBuildingClassPrereqBuilding(eBuilding, (BuildingClassTypes)iI, 0))
				{
					return false;
				}
			}
			else
			{
				if (getBuildingClassCount((BuildingClassTypes)iI) < getBuildingClassPrereqBuilding(eBuilding, (BuildingClassTypes)iI, 0))
				{
					return false;
				}
			}
		}
	}

	if (!bTestVisible)
	{
		if (GC.getGameINLINE().isBuildingClassMaxedOut(eBuildingClass, (currentTeam.getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (currentTeam.isBuildingClassMaxedOut(eBuildingClass, (currentTeam.getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (isBuildingClassMaxedOut(eBuildingClass, (getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GC.getGameINLINE().isNoNukes())
		{
			if (kBuilding.isAllowsNukes())
			{
				for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
				{
					if (GC.getUnitInfo((UnitTypes)iI).getNukeRange() != -1)
					{
						return false;
					}
				}
			}
		}

		if (kBuilding.getSpecialBuildingType() != NO_SPECIALBUILDING)
		{
			if (!(GC.getGameINLINE().isSpecialBuildingValid((SpecialBuildingTypes)(kBuilding.getSpecialBuildingType()))))
			{
				return false;
			}
		}
/*************************************************************************************************/
/**	Xienwolf Tweak							01/04/09											**/
/**																								**/
/**						Fixes Kuriotates on small maps for certain buildings					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (getNumCities() < GC.getBuildingInfo(eBuilding).getNumCitiesPrereq())
/**								----  End Original Code  ----									**/
		if (getNumCities() < kBuilding.getNumCitiesPrereq() || (getMaxCities() != -1 && (getMaxCities() < kBuilding.getNumCitiesPrereq()) && (getNumCities() != getMaxCities())))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}

		if (getHighestUnitLevel() < kBuilding.getUnitLevelPrereq())
		{
			return false;
		}

		for (iI = 0; iI < numBuildingClassInfos; iI++)
		{
			// MNAI - check if Prereq Building Class is a team building
			if (GC.getBuildingClassInfo((BuildingClassTypes)iI).getMaxTeamInstances() == 1)
			{
				if (currentTeam.getBuildingClassCount((BuildingClassTypes)iI) < getBuildingClassPrereqBuilding(eBuilding, ((BuildingClassTypes)iI), ((bContinue) ? 0 : getBuildingClassMaking(eBuildingClass))))
				{
					return false;
				}
			}
			else
			{
				if (getBuildingClassCount((BuildingClassTypes)iI) < getBuildingClassPrereqBuilding(eBuilding, ((BuildingClassTypes)iI), ((bContinue) ? 0 : getBuildingClassMaking(eBuildingClass))))
				{
					return false;
				}
			}
		}
	}

	return true;
}


bool CvPlayer::canCreate(ProjectTypes eProject, bool bContinue, bool bTestVisible) const
{
	int iI;
	CvProjectInfo& kProject = GC.getProjectInfo(eProject);

	if (isBarbarian())
	{
		return false;
	}

	if (kProject.getProductionCost() == -1)
	{
		return false;
	}

	if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(kProject.getTechPrereq()))))
	{
		return false;
	}

	if (kProject.getVictoryPrereq() != NO_VICTORY)
	{
		if (!(GC.getGameINLINE().isVictoryValid((VictoryTypes)(kProject.getVictoryPrereq()))))
		{
			return false;
		}

		if (isMinorCiv())
		{
			return false;
		}

		if (GET_TEAM(getTeam()).getVictoryCountdown((VictoryTypes)kProject.getVictoryPrereq()) >= 0)
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isProjectMaxedOut(eProject))
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isProjectMaxedOut(eProject))
	{
		return false;
	}

	if (!bTestVisible)
	{
		if (GC.getGameINLINE().isProjectMaxedOut(eProject, (GET_TEAM(getTeam()).getProjectMaking(eProject) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GET_TEAM(getTeam()).isProjectMaxedOut(eProject, (GET_TEAM(getTeam()).getProjectMaking(eProject) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GC.getGameINLINE().isNoNukes())
		{
			if (kProject.isAllowsNukes())
			{
				for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
				{
					if (GC.getUnitInfo((UnitTypes)iI).getNukeRange() != -1)
					{
						return false;
					}
				}
			}
		}

		if (kProject.getAnyoneProjectPrereq() != NO_PROJECT)
		{
			if (GC.getGameINLINE().getProjectCreatedCount((ProjectTypes)(kProject.getAnyoneProjectPrereq())) == 0)
			{
				return false;
			}
		}

		for (iI = 0; iI < GC.getNumProjectInfos(); iI++)
		{
			if (GET_TEAM(getTeam()).getProjectCount((ProjectTypes)iI) < kProject.getProjectsNeeded(iI))
			{
				return false;
			}
		}
	}

	return true;
}


bool CvPlayer::canMaintain(ProcessTypes eProcess, bool bContinue) const
{
	if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getProcessInfo(eProcess).getTechPrereq()))))
	{
		return false;
	}

	return true;
}


bool CvPlayer::isProductionMaxedUnitClass(UnitClassTypes eUnitClass) const
{
	if (eUnitClass == NO_UNITCLASS)
	{
		return false;
	}

	if (GC.getGameINLINE().isUnitClassMaxedOut(eUnitClass))
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isUnitClassMaxedOut(eUnitClass))
	{
		return true;
	}

	if (isUnitClassMaxedOut(eUnitClass))
	{
		return true;
	}

	return false;
}


bool CvPlayer::isProductionMaxedBuildingClass(BuildingClassTypes eBuildingClass, bool bAcquireCity) const
{
	if (eBuildingClass == NO_BUILDINGCLASS)
	{
		return false;
	}

	if (!bAcquireCity)
	{
		if (GC.getGameINLINE().isBuildingClassMaxedOut(eBuildingClass))
		{
			return true;
		}
	}

	if (GET_TEAM(getTeam()).isBuildingClassMaxedOut(eBuildingClass))
	{
		return true;
	}

	if (isBuildingClassMaxedOut(eBuildingClass, ((bAcquireCity) ? GC.getBuildingClassInfo(eBuildingClass).getExtraPlayerInstances() : 0)))
	{
		return true;
	}

	return false;
}


bool CvPlayer::isProductionMaxedProject(ProjectTypes eProject) const
{
	if (eProject == NO_PROJECT)
	{
		return false;
	}

	if (GC.getGameINLINE().isProjectMaxedOut(eProject))
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isProjectMaxedOut(eProject))
	{
		return true;
	}

	return false;
}


int CvPlayer::getProductionNeeded( UnitTypes eUnit, bool bAdvStartRefund ) const
{
	UnitClassTypes eUnitClass = (UnitClassTypes)GC.getUnitInfo(eUnit).getUnitClassType();
	FAssert(NO_UNITCLASS != eUnitClass);

	int iProductionNeeded = GC.getUnitInfo(eUnit).getProductionCost();

//>>>>Unofficial Bug Fix: Added by Denev 2009/11/01
//*** -1 is special value that means unconstructible.
	if (iProductionNeeded < 0)
	{
		return iProductionNeeded;
	}
//<<<<Unofficial Bug Fix: End Add

	// lfgr fix 05/2020: Don't refund more than we payed.
	int iUnitClassCount = getUnitClassCount( eUnitClass );
	if( bAdvStartRefund ) {
		if( iUnitClassCount <= 0 ) {
			// Cannot remove a unit we don't have (a player clicked remove on an empty plot)
			return -1;
		}
		iUnitClassCount -= 1;
	}
	iProductionNeeded *= 100 + iUnitClassCount * GC.getUnitClassInfo(eUnitClass).getInstanceCostModifier();
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getDefineINT("UNIT_PRODUCTION_PERCENT");
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getTrainPercent();
	iProductionNeeded /= 100;

	if (!isHuman() && !isBarbarian())
	{
		if (isWorldUnitClass(eUnitClass))
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWorldTrainPercent();
			iProductionNeeded /= 100;
		}
		else
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAITrainPercent();
			iProductionNeeded /= 100;
		}

		iProductionNeeded *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentRealEra()) + 100));
		iProductionNeeded /= 100;
	}

	iProductionNeeded += getUnitExtraCost(eUnitClass);

	// Python cost modifier
	if(GC.getUSE_GET_UNIT_COST_MOD_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());	// Player ID
		argsList.add((int)eUnit);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "getUnitCostMod", argsList.makeFunctionArgs(), &lResult);

		if (lResult > 1)
		{
			iProductionNeeded *= lResult;
			iProductionNeeded /= 100;
		}
	}

//>>>>Unofficial Bug Fix: Modified by Denev 2009/10/30
//	return std::max(1, iProductionNeeded);
	return iProductionNeeded;
//<<<<Unofficial Bug Fix: End Modify
}

int CvPlayer::getProductionNeeded(UnitTypes eUnit) const
{
	return getProductionNeeded( eUnit, false );
}


int CvPlayer::getProductionNeeded(BuildingTypes eBuilding) const
{
	int iProductionNeeded;

	iProductionNeeded = GC.getBuildingInfo(eBuilding).getProductionCost();

//>>>>Unofficial Bug Fix: Added by Denev 2009/11/01
//*** -1 is special value that means unconstructible.
	if (iProductionNeeded < 0)
	{
		return iProductionNeeded;
	}
//<<<<Unofficial Bug Fix: End Add

	iProductionNeeded *= GC.getDefineINT("BUILDING_PRODUCTION_PERCENT");
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getConstructPercent();
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getConstructPercent();
	iProductionNeeded /= 100;

	if (!isHuman() && !isBarbarian())
	{
		if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWorldConstructPercent();
			iProductionNeeded /= 100;
		}
		else
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIConstructPercent();
			iProductionNeeded /= 100;
		}

		iProductionNeeded *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentRealEra()) + 100));
		iProductionNeeded /= 100;
	}

//>>>>Unofficial Bug Fix: Modified by Denev 2009/10/30
//	return std::max(1, iProductionNeeded);
	return iProductionNeeded;
//<<<<Unofficial Bug Fix: End Modify
}


int CvPlayer::getProductionNeeded(ProjectTypes eProject) const
{
	int iProductionNeeded;

	iProductionNeeded = GC.getProjectInfo(eProject).getProductionCost();

//>>>>Unofficial Bug Fix: Added by Denev 2009/11/01
//*** -1 is special value that means unconstructible.
	if (iProductionNeeded < 0)
	{
		return iProductionNeeded;
	}
//<<<<Unofficial Bug Fix: End Add

	iProductionNeeded *= GC.getDefineINT("PROJECT_PRODUCTION_PERCENT");
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getCreatePercent();
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getCreatePercent();
	iProductionNeeded /= 100;

	if (!isHuman() && !isBarbarian())
	{
		if (isWorldProject(eProject))
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWorldCreatePercent();
			iProductionNeeded /= 100;
		}
		else
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAICreatePercent();
			iProductionNeeded /= 100;
		}

		iProductionNeeded *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentRealEra()) + 100));
		iProductionNeeded /= 100;
	}

//>>>>Unofficial Bug Fix: Modified by Denev 2009/10/30
//	return std::max(1, iProductionNeeded);
	return iProductionNeeded;
//<<<<Unofficial Bug Fix: End Modify
}

int CvPlayer::getProductionModifier(UnitTypes eUnit) const
{
	int iMultiplier = 0;
	CvUnitInfo& kUnitInfo = GC.getUnitInfo(eUnit);

	if (kUnitInfo.isMilitaryProduction())
	{
		iMultiplier += getMilitaryProductionModifier();
	}

	for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			iMultiplier += kUnitInfo.getProductionTraits(iI);

			if (kUnitInfo.getSpecialUnitType() != NO_SPECIALUNIT)
			{
				iMultiplier += GC.getSpecialUnitInfo((SpecialUnitTypes) kUnitInfo.getSpecialUnitType()).getProductionTraits(iI);
			}
		}
	}

	return iMultiplier;
}

int CvPlayer::getProductionModifier(BuildingTypes eBuilding) const
{
	int iMultiplier = 0;
	for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			iMultiplier += GC.getBuildingInfo(eBuilding).getProductionTraits(iI);

			if (GC.getBuildingInfo(eBuilding).getSpecialBuildingType() != NO_SPECIALBUILDING)
			{
				iMultiplier += GC.getSpecialBuildingInfo((SpecialBuildingTypes) GC.getBuildingInfo(eBuilding).getSpecialBuildingType()).getProductionTraits(iI);
			}
		}
	}

	if (::isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
	{
		iMultiplier += getMaxGlobalBuildingProductionModifier();
	}

	if (::isTeamWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
	{
		iMultiplier += getMaxTeamBuildingProductionModifier();
	}

	if (::isNationalWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
	{
		iMultiplier += getMaxPlayerBuildingProductionModifier();
	}

	return iMultiplier;
}

int CvPlayer::getProductionModifier(ProjectTypes eProject) const
{
	int iMultiplier = 0;

	if (GC.getProjectInfo(eProject).isSpaceship())
	{
		iMultiplier += getSpaceProductionModifier();
	}

	return iMultiplier;
}

int CvPlayer::getBuildingClassPrereqBuilding(BuildingTypes eBuilding, BuildingClassTypes ePrereqBuildingClass, int iExtra) const
{
	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);

	int iPrereqs = kBuilding.getPrereqNumOfBuildingClass(ePrereqBuildingClass);

	// dont bother with the rest of the calcs if we have no prereqs
	if (iPrereqs < 1)
	{
		return 0;
	}

	BuildingClassTypes eBuildingClass = (BuildingClassTypes)kBuilding.getBuildingClassType();

	iPrereqs *= std::max(0, (GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getBuildingClassPrereqModifier() + 100));
	iPrereqs /= 100;

	if (!isLimitedWonderClass(eBuildingClass))
	{
		iPrereqs *= (getBuildingClassCount((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())) + iExtra + 1);
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		iPrereqs = std::min(1, iPrereqs);
	}

	return iPrereqs;
}


void CvPlayer::removeBuildingClass(BuildingClassTypes eBuildingClass)
{
	CvCity* pLoopCity;
	int iLoop;

//FfH: Modified by Kael 02/26/2009
//	BuildingTypes eBuilding;
//	eBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass)));
//	if (eBuilding != NO_BUILDING)
//	{
//		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
//		{
//			if (pLoopCity->getNumRealBuilding(eBuilding) > 0)
//			{
//				pLoopCity->setNumRealBuilding(eBuilding, 0);
//				break;
//			}
//		}
//	}
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
        for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
        {
            if (GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType() == eBuildingClass)
            {
                if (pLoopCity->getNumRealBuilding((BuildingTypes)iI) > 0)
                {
                    pLoopCity->setNumRealBuilding((BuildingTypes)iI, 0);
                }
            }
        }
	}
//FfH: End Modify

}


// courtesy of the Gourd Bros...
void CvPlayer::processBuilding(BuildingTypes eBuilding, int iChange, CvArea* pArea)
{
	int iI, iJ;

	if (GC.getBuildingInfo(eBuilding).getFreeBuildingClass() != NO_BUILDINGCLASS)
	{
		BuildingTypes eFreeBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(GC.getBuildingInfo(eBuilding).getFreeBuildingClass());
/*************************************************************************************************/
/**	BUGFIX (FreeBuilding from Buildings can be -1)                             				    **/
/*************************************************************************************************/
//		changeFreeBuildingCount(eFreeBuilding, iChange);
		if(eFreeBuilding!=NO_BUILDING)
		{
			changeFreeBuildingCount(eFreeBuilding, iChange);
		}
/*************************************************************************************************/
/**	END	                                        												**/
/*************************************************************************************************/
	}

	if (GC.getBuildingInfo(eBuilding).getCivicOption() != NO_CIVICOPTION)
	{
		changeHasCivicOptionCount(((CivicOptionTypes)GC.getBuildingInfo(eBuilding).getCivicOption()), iChange);
	}

	changeGreatPeopleRateModifier(GC.getBuildingInfo(eBuilding).getGlobalGreatPeopleRateModifier() * iChange);
	changeGreatGeneralRateModifier(GC.getBuildingInfo(eBuilding).getGreatGeneralRateModifier() * iChange);
	changeDomesticGreatGeneralRateModifier(GC.getBuildingInfo(eBuilding).getDomesticGreatGeneralRateModifier() * iChange);
	changeAnarchyModifier(GC.getBuildingInfo(eBuilding).getAnarchyModifier() * iChange);
	changeGoldenAgeModifier(GC.getBuildingInfo(eBuilding).getGoldenAgeModifier() * iChange);
	changeHurryModifier(GC.getBuildingInfo(eBuilding).getGlobalHurryModifier() * iChange);
	changeFreeExperience(GC.getBuildingInfo(eBuilding).getGlobalFreeExperience() * iChange);
	changeWarWearinessModifier(GC.getBuildingInfo(eBuilding).getGlobalWarWearinessModifier() * iChange);
	pArea->changeFreeSpecialist(getID(), (GC.getBuildingInfo(eBuilding).getAreaFreeSpecialist() * iChange));
	changeFreeSpecialist(GC.getBuildingInfo(eBuilding).getGlobalFreeSpecialist() * iChange);
	changeCoastalTradeRoutes(GC.getBuildingInfo(eBuilding).getCoastalTradeRoutes() * iChange);
	changeTradeRoutes(GC.getBuildingInfo(eBuilding).getGlobalTradeRoutes() * iChange);

//FfH: Added by Kael 04/11/2008
    bool bChange;
    if (iChange > 0)
    {
        bChange = true;
    }
    if (iChange < 0)
    {
        bChange = false;
    }
    if (GC.getBuildingInfo(eBuilding).isHideUnits())
    {
        setHideUnits(bChange);
    }
    if (GC.getBuildingInfo(eBuilding).isSeeInvisible())
    {
        setSeeInvisible(bChange);
    }
    changeResistEnemyModify(GC.getBuildingInfo(eBuilding).getGlobalResistEnemyModify());
    changeResistModify(GC.getBuildingInfo(eBuilding).getGlobalResistModify());
//FfH: End Add

	if (GC.getBuildingInfo(eBuilding).getAreaHealth() > 0)
	{
		pArea->changeBuildingGoodHealth(getID(), (GC.getBuildingInfo(eBuilding).getAreaHealth() * iChange));
	}
	else
	{
		pArea->changeBuildingBadHealth(getID(), (GC.getBuildingInfo(eBuilding).getAreaHealth() * iChange));
	}
	if (GC.getBuildingInfo(eBuilding).getGlobalHealth() > 0)
	{
		changeBuildingGoodHealth(GC.getBuildingInfo(eBuilding).getGlobalHealth() * iChange);
	}
	else
	{
		changeBuildingBadHealth(GC.getBuildingInfo(eBuilding).getGlobalHealth() * iChange);
	}
	pArea->changeBuildingHappiness(getID(), (GC.getBuildingInfo(eBuilding).getAreaHappiness() * iChange));
	changeBuildingHappiness(GC.getBuildingInfo(eBuilding).getGlobalHappiness() * iChange);
	changeWorkerSpeedModifier(GC.getBuildingInfo(eBuilding).getWorkerSpeedModifier() * iChange);
	changeSpaceProductionModifier(GC.getBuildingInfo(eBuilding).getGlobalSpaceProductionModifier() * iChange);
	changeCityDefenseModifier(GC.getBuildingInfo(eBuilding).getAllCityDefenseModifier() * iChange);
	pArea->changeCleanPowerCount(getTeam(), ((GC.getBuildingInfo(eBuilding).isAreaCleanPower()) ? iChange : 0));
	pArea->changeBorderObstacleCount(getTeam(), ((GC.getBuildingInfo(eBuilding).isAreaBorderObstacle()) ? iChange : 0));

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeSeaPlotYield(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getGlobalSeaPlotYieldChange(iI) * iChange));
		pArea->changeYieldRateModifier(getID(), ((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getAreaYieldModifier(iI) * iChange));
		changeYieldRateModifier(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getGlobalYieldModifier(iI) * iChange));
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeCommerceRateModifier(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getGlobalCommerceModifier(iI) * iChange));
		changeSpecialistExtraCommerce(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getSpecialistExtraCommerce(iI) * iChange));
		changeStateReligionBuildingCommerce(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getStateReligionCommerce(iI) * iChange));
		changeCommerceFlexibleCount(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).isCommerceFlexible(iI)) ? iChange : 0);
	}

	for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		BuildingTypes eOurBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI);
		if (NO_BUILDING != eOurBuilding)
		{
			changeExtraBuildingHappiness(eOurBuilding, (GC.getBuildingInfo(eBuilding).getBuildingHappinessChanges(iI) * iChange));
		}
	}

	for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeSpecialistExtraYield(((SpecialistTypes)iI), ((YieldTypes)iJ), (GC.getBuildingInfo(eBuilding).getSpecialistYieldChange(iI, iJ) * iChange));
		}

//FfH: Added by Kael 11/06/2007
		for (iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
		{
			changeSpecialistTypeExtraCommerce(((SpecialistTypes)iI), ((CommerceTypes)iJ), (GC.getBuildingInfo(eBuilding).getSpecialistCommerceChange(iI, iJ) * iChange));
		}
//FfH: End Add

	}
}


bool CvPlayer::canBuild(const CvPlot* pPlot, BuildTypes eBuild, bool bTestEra, bool bTestVisible) const
{
	PROFILE_FUNC();

	if (!(pPlot->canBuild(eBuild, getID(), bTestVisible)))
	{
		return false;
	}

	if (GC.getBuildInfo(eBuild).getTechPrereq() != NO_TECH)
	{
		if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo(eBuild).getTechPrereq())))
		{
			if ((!bTestEra && !bTestVisible) || ((getCurrentRealEra() + 1) < GC.getTechInfo((TechTypes) GC.getBuildInfo(eBuild).getTechPrereq()).getEra()))
			{
				return false;
			}
		}
	}

	if (!bTestVisible)
	{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/02/21
//*** Elvish civilization can see the amount of production from forest chopping.
/*
		if (pPlot->getFeatureType() != NO_FEATURE

//FfH: Added by Kael 12/16/2007
		  && !GC.getCivilizationInfo(getCivilizationType()).isMaintainFeatures(pPlot->getFeatureType())
//FfH: End Add

		)
*/
		if (pPlot->isFeatureRemove(eBuild))
//<<<<Unofficial Bug Fix: End Modify
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo(eBuild).getFeatureTech(pPlot->getFeatureType()))))
			{
				return false;
			}
		}

		if (std::max(0, getGold()) < getBuildCost(pPlot, eBuild))
		{
			return false;
		}
	}

	return true;
}

// Returns the cost
int CvPlayer::getBuildCost(const CvPlot* pPlot, BuildTypes eBuild) const
{
	FAssert(eBuild >= 0 && eBuild < GC.getNumBuildInfos());

	if (pPlot->getBuildProgress(eBuild) > 0)
	{
		return 0;
	}

	return std::max(0, GC.getBuildInfo(eBuild).getCost() * (100 + calculateInflationRate())) / 100;
}


RouteTypes CvPlayer::getBestRoute(CvPlot* pPlot) const
{
	PROFILE_FUNC();

	RouteTypes eRoute;
	RouteTypes eBestRoute;
	int iValue;
	int iBestValue;
	int iI;

	iBestValue = 0;
	eBestRoute = NO_ROUTE;

	for (iI = 0; iI < GC.getNumBuildInfos(); iI++)
	{
		eRoute = ((RouteTypes)(GC.getBuildInfo((BuildTypes)iI).getRoute()));

		if (eRoute != NO_ROUTE)
		{
			if ((pPlot != NULL) ? ((pPlot->getRouteType() == eRoute) || canBuild(pPlot, ((BuildTypes)iI))) : GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getBuildInfo((BuildTypes)iI).getTechPrereq())))
			{
				iValue = GC.getRouteInfo(eRoute).getValue();

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestRoute = eRoute;
				}
			}
		}
	}

	return eBestRoute;
}


int CvPlayer::getImprovementUpgradeRate() const
{
	int iRate;

	iRate = 1; // XXX

	iRate *= std::max(0, (getImprovementUpgradeRateModifier() + 100));
	iRate /= 100;

	return iRate;
}


int CvPlayer::calculateTotalYield(YieldTypes eYield) const
{
	CvCity* pLoopCity;
	int iTotalCommerce = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalCommerce += pLoopCity->getYieldRate(eYield);
	}

	return iTotalCommerce;
}


int CvPlayer::calculateTotalCityHappiness() const
{
	CvCity* pLoopCity;
	int iTotalHappiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalHappiness += pLoopCity->happyLevel();
	}

	return iTotalHappiness;
}


int CvPlayer::calculateTotalExports(YieldTypes eYield) const
{
	CvCity* pLoopCity;
	CvCity* pTradeCity;
	int iTotalExports = 0;
	int iLoop = 0, iTradeLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
// BUG - Fractional Trade Routes - start
		int iCityExports = 0;

		for (iTradeLoop = 0; iTradeLoop < pLoopCity->getTradeRoutes(); iTradeLoop++)
		{
			pTradeCity = pLoopCity->getTradeCity(iTradeLoop);
			if (pTradeCity != NULL)
			{
				if (pTradeCity->getOwnerINLINE() != getID())
				{
					iCityExports += pLoopCity->calculateTradeYield(eYield, pLoopCity->calculateTradeProfitTimes100(pTradeCity));
					// iTotalExports += pLoopCity->calculateTradeYield(eYield, pLoopCity->calculateTradeProfit(pTradeCity));
				}
			}
		}

		iTotalExports += iCityExports / 100;
// BUG - Fractional Trade Routes - end
	}

	return iTotalExports;
}


int CvPlayer::calculateTotalImports(YieldTypes eYield) const
{
	CvCity* pLoopCity;
	CvCity* pTradeCity;
	int iTotalImports = 0;
	int iPlayerLoop = 0, iLoop = 0, iTradeLoop = 0;

	// Loop through players
	for (iPlayerLoop = 0; iPlayerLoop < MAX_CIV_PLAYERS; iPlayerLoop++)
	{
		if (iPlayerLoop != getID())
		{
// BUG - Fractional Trade Routes - start
			int iCityImports = 0;

			for (pLoopCity = GET_PLAYER((PlayerTypes) iPlayerLoop).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes) iPlayerLoop).nextCity(&iLoop))
			{
				for (iTradeLoop = 0; iTradeLoop < pLoopCity->getTradeRoutes(); iTradeLoop++)
				{
					pTradeCity = pLoopCity->getTradeCity(iTradeLoop);
					if (pTradeCity != NULL)
					{
						if (pTradeCity->getOwnerINLINE() == getID())
						{
							// iTotalImports += pLoopCity->calculateTradeYield(eYield, pLoopCity->calculateTradeProfit(pTradeCity));
						}
					}
				}
			}

			iTotalImports += iCityImports / 100;
// BUG - Fractional Trade Routes - end
		}
	}
	return iTotalImports;
}


int CvPlayer::calculateTotalCityUnhappiness() const
{
	CvCity* pLoopCity;
	int iTotalUnhappiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalUnhappiness += pLoopCity->unhappyLevel();
	}

	return iTotalUnhappiness;
}


int CvPlayer::calculateTotalCityHealthiness() const
{
	CvCity* pLoopCity;
	int iTotalHealthiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalHealthiness += pLoopCity->goodHealth();
	}

	return iTotalHealthiness;
}

int CvPlayer::calculateTotalCityUnhealthiness() const
{
	CvCity* pLoopCity;
	int iTotalUnhealthiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalUnhealthiness += pLoopCity->badHealth();
	}

	return iTotalUnhealthiness;
}


int CvPlayer::calculateUnitCost(int& iFreeUnits, int& iFreeMilitaryUnits, int& iPaidUnits, int& iPaidMilitaryUnits, int& iBaseUnitCost, int& iMilitaryCost, int& iExtraCost) const
{
	int iSupport;

	iFreeUnits = GC.getHandicapInfo(getHandicapType()).getFreeUnits();

	iFreeUnits += getBaseFreeUnits();
	iFreeUnits += ((getTotalPopulation() * getFreeUnitsPopulationPercent()) / 100);

//FfH: Added by Kael 04/19/2009
	// dont count summons or objects for unit maintenance
	int iNoUpkeepUnits = 0; // lfgr 01/2022: Don't count units with no upkeep as free units for display purposes
	CvUnit* pLoopUnit;
	int iLoop;
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
	    if (pLoopUnit->isNoUpkeep()) // lfgr 01/2022: Refactoring
	    {
			iNoUpkeepUnits += 1;
	    }
	}
//FfH: End Add

	iFreeMilitaryUnits = getBaseFreeMilitaryUnits();
	iFreeMilitaryUnits += ((getTotalPopulation() * getFreeMilitaryUnitsPopulationPercent()) / 100);

/************************************************************************************************/
/* REVOLUTION_MOD                         02/04/09                                jdog5000      */
/*                                                                                              */
/* For rebels and BarbarianCiv                                                                  */
/************************************************************************************************/
	iFreeUnits += getFreeUnitCountdown();
	iFreeMilitaryUnits += getFreeUnitCountdown();
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/


/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/17/09                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/* original BTS code
	if (!isHuman())
	{
		if (GET_TEAM(getTeam()).hasMetHuman())
		{
			iFreeUnits += getNumCities(); // XXX
			iFreeMilitaryUnits += getNumCities(); // XXX
		}
	}
*/
	// Removed hidden AI bonus
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	iPaidUnits = std::max(0, getNumUnits() - iFreeUnits - iNoUpkeepUnits); // lfgr 01/2022
	iPaidMilitaryUnits = std::max(0, getNumMilitaryUnits() - iFreeMilitaryUnits);

	iSupport = 0;

	iBaseUnitCost = iPaidUnits * getGoldPerUnit();
	iMilitaryCost = iPaidMilitaryUnits * getGoldPerMilitaryUnit();
	iExtraCost = getExtraUnitCost();

	iSupport = iMilitaryCost + iBaseUnitCost + iExtraCost;

	iSupport *= GC.getHandicapInfo(getHandicapType()).getUnitCostPercent();
	iSupport /= 100;

	if (!isHuman() && !isBarbarian())
	{
		iSupport *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIUnitCostPercent();
		iSupport /= 100;

		iSupport *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * GC.getGameINLINE().getCurrentEra()) + 100));
		iSupport /= 100;
	}

	FAssert(iSupport >= 0);

	return std::max(0, iSupport);
}


int CvPlayer::calculateUnitCost() const
{
	if (isAnarchy())
	{
		return 0;
	}

//FfH: Added by Kael 10/03/2008
    if (getDisableProduction() > 0 || GC.getGameINLINE().isOption(GAMEOPTION_NO_MAINTENANCE))
    {
        return 0;
    }
//FfH: End Add

	int iFreeUnits;
	int iFreeMilitaryUnits;
	int iPaidUnits;
	int iPaidMilitaryUnits;
	int iMilitaryCost;
	int iBaseUnitCost;
	int iExtraCost;

	return calculateUnitCost(iFreeUnits, iFreeMilitaryUnits, iPaidUnits, iPaidMilitaryUnits, iBaseUnitCost, iMilitaryCost, iExtraCost);
}

int CvPlayer::calculateUnitSupply() const
{
	int iPaidUnits;
	int iBaseSupplyCost;

	if (isAnarchy())
	{
		return 0;
	}

//FfH: Added by Kael 10/03/2008
    if (getDisableProduction() > 0 || GC.getGameINLINE().isOption(GAMEOPTION_NO_MAINTENANCE))
    {
        return 0;
    }
//FfH: End Add

	return calculateUnitSupply(iPaidUnits, iBaseSupplyCost);
}

int CvPlayer::calculateUnitSupply(int& iPaidUnits, int& iBaseSupplyCost) const
{
	int iSupply;

	iPaidUnits = std::max(0, (getNumOutsideUnits() - GC.getDefineINT("INITIAL_FREE_OUTSIDE_UNITS")));

	iBaseSupplyCost = iPaidUnits * GC.getDefineINT("INITIAL_OUTSIDE_UNIT_GOLD_PERCENT");
	iBaseSupplyCost /= 100;

	iSupply = iBaseSupplyCost;

	if (!isHuman() && !isBarbarian())
	{
		iSupply *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIUnitSupplyPercent();
		iSupply /= 100;

		iSupply *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * GC.getGameINLINE().getCurrentEra()) + 100));
		iSupply /= 100;
	}

	FAssert(iSupply >= 0);

	return iSupply;
}


int CvPlayer::calculatePreInflatedCosts() const
{
	CyArgsList argsList;
	argsList.add(getID());
	long lResult;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "getExtraCost", argsList.makeFunctionArgs(), &lResult);

	return (calculateUnitCost() + calculateUnitSupply() + getTotalMaintenance() + getCivicUpkeep() + (int)lResult);
}


int CvPlayer::calculateInflationRate() const
{

//FfH: Added by Kael 11/18/2008
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_INFLATION))
	{
	    return 0;
	}
//FfH: End Add

	int iTurns = ((GC.getGameINLINE().getGameTurn() + GC.getGameINLINE().getElapsedGameTurns()) / 2);

	if (GC.getGameINLINE().getMaxTurns() > 0)
	{
		iTurns = std::min(GC.getGameINLINE().getMaxTurns(), iTurns);
	}

	iTurns += GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getInflationOffset();

	if (iTurns <= 0)
	{
		return 0;
	}

	int iInflationPerTurnTimes10000 = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getInflationPercent();
	iInflationPerTurnTimes10000 *= GC.getHandicapInfo(getHandicapType()).getInflationPercent();
	iInflationPerTurnTimes10000 /= 100;

	int iModifier = getInflationModifier(); // lfgr 05/2022
	if (!isHuman() && !isBarbarian())
	{
		int iAIModifier = GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIInflationPercent();
		iAIModifier *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * GC.getGameINLINE().getCurrentEra()) + 100));
		iAIModifier /= 100;

		iModifier += iAIModifier - 100;
	}

/************************************************************************************************/
/* REVOLUTION_MOD                         01/31/08                                jdog5000      */
/*                                                                                              */
/* Reduced inflation cost for rebels                                                            */
/************************************************************************************************/
	if( isRebel() )
		iModifier -= 50;
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	iInflationPerTurnTimes10000 *= std::max(0, 100 + iModifier);
	iInflationPerTurnTimes10000 /= 100;

	// Keep up to second order terms in binomial series
	int iRatePercent = (iTurns * iInflationPerTurnTimes10000) / 100;
	iRatePercent += (iTurns * (iTurns - 1) * iInflationPerTurnTimes10000 * iInflationPerTurnTimes10000) / 2000000;

	FAssert(iRatePercent >= 0);

	return iRatePercent;
}


int CvPlayer::calculateInflatedCosts() const
{
	int iCosts;

	iCosts = calculatePreInflatedCosts();

	iCosts *= std::max(0, (calculateInflationRate() + 100));
	iCosts /= 100;

	return iCosts;
}

/************************************************************************************************/
/* REVOLUTION_MOD                         02/04/09                                jdog5000      */
/*                                                                                              */
/* For rebels and BarbarianCiv                                                                  */
/************************************************************************************************/
int CvPlayer::getFreeUnitCountdown() const
{
	return m_iFreeUnitCountdown;
}

void CvPlayer::setFreeUnitCountdown( int iValue )
{
	m_iFreeUnitCountdown = std::max(0, iValue);
}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/


int CvPlayer::calculateBaseNetGold() const
{
	int iNetGold;

	iNetGold = (getCommerceRate(COMMERCE_GOLD) + getGoldPerTurn());

	iNetGold -= calculateInflatedCosts();

	return iNetGold;
}

// ExtraModMod technology propagation START
int CvPlayer::calculateTechPropagationResearchModifier(TechTypes eTech) const
{
	int iModPropagationTeams = 0;

	if (GC.getGameINLINE().isOption(GAMEOPTION_TECHNOLOGY_PROPAGATION))
	{
		// Number of teams which have researched the technology.
		int iTeamsResearchedCount = 0;
		// Value to store the technology diffusion contribution of each team.
		int iRawPropagationTeams = 0;
		TeamTypes iTeam = getTeam();
		CvTeam& kTeam = GET_TEAM(iTeam);
		// Technology diffusion is calculated depending on all other teams.
		for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			TeamTypes iOtherTeam = (TeamTypes)iI;
			CvTeam& kOtherTeam = GET_TEAM(iOtherTeam);
			if (kOtherTeam.isAlive() && kOtherTeam.isHasTech(eTech))
			{
				/*
				 * The total technology diffusion rate depends on the number of teams who know the tech,
				 * regardless of if they have been met or not.
				 */
				iTeamsResearchedCount++;
				// Only teams that have been met can contribute to tech diffusion.
				if (kOtherTeam.isHasMet(getTeam()))
				{
					int iCurrTeamPropagation = 0;
					if (kTeam.isLimitedBorders(iOtherTeam)) // Right of Passage.
					{
						iCurrTeamPropagation = GC.getTECH_PROPAGATION_TEAMS_RIGHT_OF_PASSAGE();
					}
					else if (kTeam.isVassal(iOtherTeam)) // Master.
					{
						iCurrTeamPropagation = GC.getTECH_PROPAGATION_TEAMS_MASTER();
					}
					else if (kTeam.isOpenBorders(iOtherTeam)) // Open borders
					{
						iCurrTeamPropagation = GC.getTECH_PROPAGATION_TEAMS_OPEN_BORDERS();
					}
					else if (kOtherTeam.isVassal(iTeam)) // Vassal.
					{
						iCurrTeamPropagation = GC.getTECH_PROPAGATION_TEAMS_VASSAL();
					}

					// If the team can contribute to technology propagation, its contribution can be increased by other factors.
					if (iCurrTeamPropagation > 0)
					{
						if (kTeam.isHasEmbassy(iOtherTeam)) // Embassy.
						{
							iCurrTeamPropagation += GC.getTECH_PROPAGATION_TEAMS_EMBASSY();
						}

						if (kTeam.isDefensivePact(iOtherTeam)) // Defensive pact.
						{
							iCurrTeamPropagation += GC.getTECH_PROPAGATION_TEAMS_DEFENSIVE_PACT();
						}

						// Similarity values depend on the players of the team.
						bool bAlignment = false;
						bool bReligion = false;
						for (int iJ = 0; iJ < MAX_PLAYERS; iJ++)
						{
							CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iJ);
							if (kPlayer.getTeam() == iOtherTeam && kPlayer.isAlive()) {
								if (getAlignment() == kPlayer.getAlignment())
								{
									bAlignment = true;
								}
								if (getStateReligion() == kPlayer.getStateReligion())
								{
									bReligion = true;
								}
								if (bReligion && bAlignment)
								{
									break;
								}
							}
						}

						if (bReligion) // One member of the other team shares alignment with the researcher.
						{
							iCurrTeamPropagation += GC.getTECH_PROPAGATION_TEAMS_ALIGMENT();
						}

						if (bReligion) // One member of the other team shares religion with the researcher.
						{
							iCurrTeamPropagation += GC.getTECH_PROPAGATION_TEAMS_RELIGION();
						}

						// The contribution of this team is added to the total.
						iRawPropagationTeams += iCurrTeamPropagation;
					}
				}
			}
		}

		if (iRawPropagationTeams > 0)
		{
			iModPropagationTeams = (GC.getTECH_PROPAGATION_TEAMS_MAX() * iRawPropagationTeams) / (100 * iTeamsResearchedCount);
		}
	}

	return iModPropagationTeams;
}
// ExtraModMod technology propagation END

int CvPlayer::calculateResearchModifier(TechTypes eTech) const
{
	int iModifier = 100;

	if (NO_TECH == eTech)
	{
		return iModifier;
	}


// ExtraModMod technology propagation START
	iModifier += calculateTechPropagationResearchModifier(eTech);
// ExtraModMod technology propagation END

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      07/27/09                                jdog5000      */
/*                                                                                              */
/* Tech Diffusion                                                                               */
/************************************************************************************************/
// Removed by Terkhen, ExtraModMod technology propagation
/*
	int iKnownCount = 0;
	int iPossibleKnownCount = 0;

	if( GC.getDefineINT("TECH_DIFFUSION_ENABLE") && GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
	{
		double knownExp = 0.0;
		// Tech flows better through open borders
		for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			if (GET_TEAM((TeamTypes)iI).isAlive())
			{
				if (GET_TEAM((TeamTypes)iI).isHasTech(eTech))
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iI))
					{
						knownExp += 0.5;

						if( GET_TEAM(getTeam()).isOpenBorders((TeamTypes)iI) || GET_TEAM((TeamTypes)iI).isVassal(getTeam()) )
						{
							knownExp += 1.5;
						}
						else if( GET_TEAM(getTeam()).isAtWar((TeamTypes)iI) || GET_TEAM(getTeam()).isVassal((TeamTypes)iI) )
						{
							knownExp += 0.5;
						}
						
						// MNAI - Advanced Diplomacy
						if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
						{
							if (GET_TEAM(getTeam()).isLimitedBorders((TeamTypes)iI)) // Rights of Passage
							{
								knownExp += 0.5;
							}
							if (GET_TEAM(getTeam()).isHasEmbassy((TeamTypes)iI)) // Embassy
							{
								knownExp += 1.0;
							}
						}
						// End MNAI

					}
				}
			}
		}

		int techDiffMod = GC.getTECH_DIFFUSION_KNOWN_TEAM_MODIFIER();
		if (knownExp > 0.0)
		{
			iModifier += techDiffMod - (int)(techDiffMod * pow(0.85, knownExp) + 0.5);
		}

		// Tech flows downhill to those who are far behind
		int iTechScorePercent = GET_TEAM(getTeam()).getBestKnownTechScorePercent();
		int iWelfareThreshold = GC.getTECH_DIFFUSION_WELFARE_THRESHOLD();
		if( iTechScorePercent < iWelfareThreshold )
		{
			if( knownExp > 0.0 )
			{
				iModifier += (GC.getTECH_DIFFUSION_WELFARE_MODIFIER() * GC.getGameINLINE().getCurrentEra() * (iWelfareThreshold - iTechScorePercent))/200;
			}
		}
		
		iModifier -= GC.getTECH_COST_MODIFIER();
	}
	// End Tech Diffusion
	else
	{
		// Default BTS code
		for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			if (GET_TEAM((TeamTypes)iI).isAlive())
			{
				if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iI))
				{
					if (GET_TEAM((TeamTypes)iI).isHasTech(eTech))
					{
						iKnownCount++;
					}
				}

				iPossibleKnownCount++;
			}
		}

		if (iPossibleKnownCount > 0)
		{
			iModifier += (GC.getDefineINT("TECH_COST_TOTAL_KNOWN_TEAM_MODIFIER") * iKnownCount) / iPossibleKnownCount;
		}
	}
*/

	int iPossiblePaths = 0;
	int iUnknownPaths = 0;

	for (int iI = 0; iI < GC.getNUM_OR_TECH_PREREQS(); iI++)
	{
		if (GC.getTechInfo(eTech).getPrereqOrTechs(iI) != NO_TECH)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getTechInfo(eTech).getPrereqOrTechs(iI)))))
			{
				iUnknownPaths++;
			}

			iPossiblePaths++;
		}
	}

	FAssertMsg(iPossiblePaths >= iUnknownPaths, "The number of possible paths is expected to match or exceed the number of unknown ones");

	iModifier += (iPossiblePaths - iUnknownPaths) * GC.getDefineINT("TECH_COST_KNOWN_PREREQ_MODIFIER");

	return iModifier;
}

int CvPlayer::calculateBaseNetResearch(TechTypes eTech) const
{
	TechTypes eResearchTech;

	if (eTech != NO_TECH)
	{
		eResearchTech = eTech;
	}
	else
	{
		eResearchTech = getCurrentResearch();
	}

	return (((GC.getDefineINT("BASE_RESEARCH_RATE") + getCommerceRate(COMMERCE_RESEARCH)) * calculateResearchModifier(eResearchTech)) / 100);
}


int CvPlayer::calculateGoldRate() const
{
	int iRate = 0;

	if (isCommerceFlexible(COMMERCE_RESEARCH))
	{
		iRate = calculateBaseNetGold();
	}
	else
	{
		iRate = std::min(0, (calculateBaseNetResearch() + calculateBaseNetGold()));
	}

	return iRate;
}


int CvPlayer::calculateResearchRate(TechTypes eTech) const
{
	int iRate = 0;

	if (isCommerceFlexible(COMMERCE_RESEARCH))
	{
		iRate = calculateBaseNetResearch(eTech);
	}
	else
	{
		iRate = std::max(1, (calculateBaseNetResearch(eTech) + calculateBaseNetGold()));
	}

	return iRate;
}

int CvPlayer::calculateTotalCommerce() const
{
	int iTotalCommerce = calculateBaseNetGold() + calculateBaseNetResearch();

	for (int i = 0; i < NUM_COMMERCE_TYPES; ++i)
	{
		if (COMMERCE_GOLD != i && COMMERCE_RESEARCH != i)
		{
			iTotalCommerce += getCommerceRate((CommerceTypes)i);
		}
	}

	return iTotalCommerce;
}

bool CvPlayer::isResearch() const
{
	if(GC.getUSE_IS_PLAYER_RESEARCH_CALLBACK())
	{
		CyArgsList argsList;
		long lResult;
		argsList.add(getID());
		lResult = 1;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "isPlayerResearch", argsList.makeFunctionArgs(), &lResult);
		if (lResult == 0)
		{
			return false;
		}
	}

	if (!isFoundedFirstCity())
	{
		return false;
	}

	return true;
}


bool CvPlayer::canEverResearch(TechTypes eTech) const
{
	if (GC.getTechInfo(eTech).isDisable())
	{
		return false;
	}

	if (GC.getCivilizationInfo(getCivilizationType()).isCivilizationDisableTechs(eTech))
	{
		return false;
	}

//FfH Techs: Added by Kael 08/09/2007
    if (GC.getTechInfo(eTech).getPrereqReligion() != NO_RELIGION)
    {
        if (getStateReligion() != GC.getTechInfo(eTech).getPrereqReligion())
        {
            return false;
        }
    }
//FfH: End Add

	if (GC.getUSE_CANNOT_RESEARCH_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());
		argsList.add(eTech);
		argsList.add(false);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotResearch", argsList.makeFunctionArgs(), &lResult);

		if (lResult == 1)
		{
			return false;
		}
	}

	return true;
}


bool CvPlayer::canResearch(TechTypes eTech, bool bTrade) const
{
	bool bFoundPossible;
	bool bFoundValid;
	int iI;

	if(GC.getUSE_CAN_RESEARCH_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());
		argsList.add(eTech);
		argsList.add(bTrade);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canResearch", argsList.makeFunctionArgs(), &lResult);
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!isResearch() && getAdvancedStartPoints() < 0)
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isHasTech(eTech))
	{
		return false;
	}

	bFoundPossible = false;
	bFoundValid = false;

	for (iI = 0; iI < GC.getNUM_OR_TECH_PREREQS(); iI++)
	{
		TechTypes ePrereq = (TechTypes)GC.getTechInfo(eTech).getPrereqOrTechs(iI);
		if (ePrereq != NO_TECH)
		{
			bFoundPossible = true;

			if (GET_TEAM(getTeam()).isHasTech(ePrereq))
			{
				if (!bTrade || GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING) || !GET_TEAM(getTeam()).isNoTradeTech(ePrereq))
				{
					bFoundValid = true;
					break;
				}
			}
		}
	}

	if (bFoundPossible && !bFoundValid)
	{
		return false;
	}

	for (iI = 0; iI < GC.getNUM_AND_TECH_PREREQS(); iI++)
	{
		TechTypes ePrereq = (TechTypes)GC.getTechInfo(eTech).getPrereqAndTechs(iI);
		if (ePrereq != NO_TECH)
		{
			if (!GET_TEAM(getTeam()).isHasTech(ePrereq))
			{
				return false;
			}

			if (bTrade && !GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING) && GET_TEAM(getTeam()).isNoTradeTech(ePrereq))
			{
				return false;
			}
		}
	}

	if (!canEverResearch(eTech))
	{
		return false;
	}

	return true;
}


TechTypes CvPlayer::getCurrentResearch() const
{
	CLLNode<TechTypes>* pResearchNode;

	pResearchNode = headResearchQueueNode();

	if (pResearchNode != NULL)
	{
		return pResearchNode->m_data;
	}
	else
	{
		return NO_TECH;
	}
}


bool CvPlayer::isCurrentResearchRepeat() const
{
	TechTypes eCurrentResearch;

	eCurrentResearch = getCurrentResearch();

	if (eCurrentResearch == NO_TECH)
	{
		return false;
	}

	return GC.getTechInfo(eCurrentResearch).isRepeat();
}


bool CvPlayer::isNoResearchAvailable() const
{
	int iI;

	if (getCurrentResearch() != NO_TECH)
	{
		return false;
	}

	for (iI = 0; iI < GC.getNumTechInfos(); iI++)
	{
		if (canResearch((TechTypes)iI))
		{
			return false;
		}
	}

	return true;
}


int CvPlayer::getResearchTurnsLeft(TechTypes eTech, bool bOverflow) const
{
	int iTurnsLeft = getResearchTurnsLeftTimes100(eTech, bOverflow);

	iTurnsLeft = (iTurnsLeft + 99) / 100; // round up

	return std::max(1, iTurnsLeft);
}

int CvPlayer::getResearchTurnsLeftTimes100(TechTypes eTech, bool bOverflow) const
{
    int iResearchRate;
	int iOverflow;
	int iResearchLeft;
	int iTurnsLeft;
	int iI;

	iResearchRate = 0;
	iOverflow = 0;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				if ((iI == getID()) || (GET_PLAYER((PlayerTypes)iI).getCurrentResearch() == eTech))
				{
					iResearchRate += GET_PLAYER((PlayerTypes)iI).calculateResearchRate(eTech);
					iOverflow += (GET_PLAYER((PlayerTypes)iI).getOverflowResearch() * calculateResearchModifier(eTech)) / 100;
				}
			}
		}
	}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      03/18/10                                jdog5000      */
/*                                                                                              */
/* Tech AI                                                                                      */
/************************************************************************************************/
	// Mainly just so debug display shows sensible value
	iResearchLeft = GET_TEAM(getTeam()).getResearchLeft(eTech);
	
	if (bOverflow)
	{
		iResearchLeft -= iOverflow;
	}
	
	iResearchLeft *= 100;

	if (iResearchRate == 0)
	{
		return iResearchLeft;
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	iTurnsLeft = (iResearchLeft / iResearchRate);

	if (iTurnsLeft * iResearchRate < iResearchLeft)
	{
		++iTurnsLeft;
	}

	return std::max(1, iTurnsLeft);
    
    
}


bool CvPlayer::isCivic(CivicTypes eCivic) const
{
#ifdef USE_OLD_CODE
	int iI;

	for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (getCivics((CivicOptionTypes)iI) == eCivic)
		{
			return true;
		}
	}

	return false;
#else
	for(int i=0; i< GC.getNumCivicOptionInfos(); ++i)
		if( m_paeCivics[i] == eCivic )
			return true;
	return false;
#endif
}


bool CvPlayer::canDoCivics(CivicTypes eCivic) const
{
	PROFILE_FUNC();


/************************************************************************************************/
/* Advanced Diplomacy         START                                                             */
/************************************************************************************************/
	/*
	if (GC.getGameINLINE().isNetworkMultiPlayer())
	{
		if (GC.getGameINLINE().isCondemnCivic(eCivic))
		{
			return false;
		}
	}
	*/
/************************************************************************************************/
/* Advanced Diplomacy         END																*/
/************************************************************************************************/

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       02/16/10                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Circumvents second crash bug in simultaneous turns MP games
	if( eCivic == NO_CIVIC )
	{
		return true;
	}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/	

	CvCivicInfo &kCivic = GC.getCivicInfo(eCivic);

// lfgr 06/2019 / Kael 11/2007: ForceCivic applies only to the respective VoteSource
	for( int i = 0; i < GC.getNumVoteSourceInfos(); i++ )
	{
		VoteSourceTypes eVoteSource = (VoteSourceTypes) i;
		if( isFullMember( eVoteSource )
				&& GC.getGameINLINE().isForceCivicOption(
						eVoteSource, (CivicOptionTypes) kCivic.getCivicOptionType() ) )
		{
			return GC.getGameINLINE().isForceCivic( eVoteSource, eCivic );
		}
	}
// lfgr end

	if(GC.getUSE_CAN_DO_CIVIC_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());
		argsList.add(eCivic);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canDoCivic", argsList.makeFunctionArgs(), &lResult);
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!isHasCivicOption((CivicOptionTypes)(kCivic.getCivicOptionType())) && !(GET_TEAM(getTeam()).isHasTech((TechTypes)(kCivic.getTechPrereq()))))
	{
		return false;
	}

//FfH Civics: Added by Kael 08/11/2007
    if (kCivic.isPrereqWar())
    {
        if (GET_TEAM(getTeam()).getAtWarCount(true) == 0)
        {
            return false;
		}
    }
    if (kCivic.getBlockAlignment() != NO_ALIGNMENT)
    {
        if (getAlignment() == kCivic.getBlockAlignment())
        {
            return false;
        }
    }
    if (kCivic.getPrereqAlignment() != NO_ALIGNMENT)
    {
        if (getAlignment() != kCivic.getPrereqAlignment())
        {
            return false;
        }
    }
    if (kCivic.getPrereqCivilization() != NO_CIVILIZATION)
    {
        if (getCivilizationType() != kCivic.getPrereqCivilization())
        {
            return false;
        }
    }
    if (kCivic.getPrereqReligion() != NO_RELIGION)
    {
        if (getStateReligion() != kCivic.getPrereqReligion())
        {
            return false;
        }
    }
//FfH: End Add

	if(GC.getUSE_CANNOT_DO_CIVIC_CALLBACK())
	{
		CyArgsList argsList2; // XXX
		argsList2.add(getID());
		argsList2.add(eCivic);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotDoCivic", argsList2.makeFunctionArgs(), &lResult);
		if (lResult == 1)
		{
			return false;
		}
	}

	return true;
}


bool CvPlayer::canRevolution(CivicTypes* paeNewCivics) const
{
	int iI;

	if (isAnarchy())
	{
		return false;
	}

	if (getRevolutionTimer() > 0)
	{
		return false;
	}

	if (paeNewCivics == NULL)
	{
		// XXX is this necessary?
		for (iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			if (canDoCivics((CivicTypes)iI))
			{
				if (getCivics((CivicOptionTypes)GC.getCivicInfo((CivicTypes) iI).getCivicOptionType()) != iI)
				{
					return true;
				}
			}
		}
	}
	else
	{
	// lfgr 06/2019 / Kael 12/2007: ForceCivic applies only to the respective VoteSource LFGR_TODO: Optimize by putting isFullMember first?
		// Check that we honor forced civics
		for( int i = 0; i < GC.getNumVoteSourceInfos(); i++ )
		{
			VoteSourceTypes eVoteSource = (VoteSourceTypes) i;
			if( isFullMember( eVoteSource )  )
			{
				for( int iCivicOption = 0; iCivicOption < GC.getNumCivicOptionInfos(); ++iCivicOption )
				{
					if( GC.getGameINLINE().isForceCivicOption(
								eVoteSource, (CivicOptionTypes) iCivicOption )
						&& ! GC.getGameINLINE().isForceCivic( eVoteSource, paeNewCivics[iCivicOption] ) )
					{
						// CivicOption is forced to another civic than the one we want to switch to
						return false;
					}
				}
			}
		}
	// lfgr end

		// Check that we actually want to change something
		for (iI = 0; iI < GC.getNumCivicOptionInfos(); ++iI)
		{
			if (getCivics((CivicOptionTypes)iI) != paeNewCivics[iI])
			{
				return true;
			}
		}
	}

	return false;
}


void CvPlayer::revolution(CivicTypes* paeNewCivics, bool bForce)
{
	int iAnarchyLength;
	int iI;

	if (!bForce && !canRevolution(paeNewCivics))
	{
		return;
	}

// BUG - Revolution Event - start
	CivicTypes* paeOldCivics = new CivicTypes[GC.getNumCivicOptionInfos()];

	for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		paeOldCivics[iI] = getCivics(((CivicOptionTypes)iI));
	}
// BUG - Revolution Event - end

	iAnarchyLength = getCivicAnarchyLength(paeNewCivics);

	if (iAnarchyLength > 0)
	{
		changeAnarchyTurns(iAnarchyLength);

		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), paeNewCivics[iI]);
		}
	}
	else
	{
		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), paeNewCivics[iI]);
		}
	}

	setRevolutionTimer(std::max(1, ((100 + getAnarchyModifier()) * GC.getDefineINT("MIN_REVOLUTION_TURNS")) / 100) + iAnarchyLength);

	if (getID() == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getInterfaceIFace()->setDirty(Popup_DIRTY_BIT, true); // to force an update of the civic chooser popup
	}

// BUG - Revolution Event - start
	CvEventReporter::getInstance().playerRevolution(getID(), iAnarchyLength, paeOldCivics, paeNewCivics);
	delete [] paeOldCivics;
// BUG - Revolution Event - end
}


int CvPlayer::getCivicPercentAnger(CivicTypes eCivic, bool bIgnore) const
{
	int iCount;
	int iPossibleCount;
	int iI;

//FfH: Added by Kael 11/25/2007
    if (GET_TEAM(getTeam()).isNoCivicAnger())
    {
        return 0;
    }
//FfH: End Add

	if (GC.getCivicInfo(eCivic).getCivicPercentAnger() == 0)
	{
		return 0;
	}

	if (!bIgnore && (getCivics((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())) == eCivic))
	{
		return 0;
	}

	iCount = 0;
	iPossibleCount = 0;

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam())
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivics((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())) == eCivic)
				{
					iCount += GET_PLAYER((PlayerTypes)iI).getNumCities();
				}

				iPossibleCount += GET_PLAYER((PlayerTypes)iI).getNumCities();
			}
		}
	}

	if (iPossibleCount == 0)
	{
		return 0;
	}

	return ((GC.getCivicInfo(eCivic).getCivicPercentAnger() * iCount) / iPossibleCount);
}


bool CvPlayer::canDoReligion(ReligionTypes eReligion) const
{
	if (GET_TEAM(getTeam()).getHasReligionCount(eReligion) == 0)
	{
		return false;
	}

//FfH Traits: Added by Kael 08/02/2007
    if (isAgnostic())
    {
        return false;
    }

	if (!isHuman())
	{
		if (GC.getLeaderHeadInfo(getPersonalityType()).getReligionWeightModifier(eReligion) <= -100)
		{
			return false;
		}
	}
//FfH: End Add

	return true;
}


bool CvPlayer::canChangeReligion() const
{
	int iI;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (canConvert((ReligionTypes)iI))
		{
			return true;
		}
	}

	return false;
}


bool CvPlayer::canConvert(ReligionTypes eReligion) const
{

	if (isBarbarian())
	{
		return false;
	}

	if (isAnarchy())
	{
		return false;
	}

	if (getConversionTimer() > 0)
	{
		return false;
	}

	if (!isStateReligion())
	{
		return false;
	}

	if (getLastStateReligion() == eReligion)
	{
		return false;
	}

	if (eReligion != NO_RELIGION)
	{
		if (!canDoReligion(eReligion))
		{
			return false;
		}
	}

	return true;
}


void CvPlayer::convert(ReligionTypes eReligion)
{
	int iAnarchyLength;

	if (!canConvert(eReligion))
	{
		return;
	}

	iAnarchyLength = getReligionAnarchyLength();

	changeAnarchyTurns(iAnarchyLength);

	setLastStateReligion(eReligion);

	setConversionTimer(std::max(1, ((100 + getAnarchyModifier()) * GC.getDefineINT("MIN_CONVERSION_TURNS")) / 100) + iAnarchyLength);

//FfH Religion: Added by Kael 08/09/2007
	if (eReligion!=NO_RELIGION)
	{
		if (getAlignment() < GC.getReligionInfo(eReligion).getAlignmentBest())
		{
			setAlignment((AlignmentTypes) GC.getReligionInfo(eReligion).getAlignmentBest());
		}
		if (getAlignment() > GC.getReligionInfo(eReligion).getAlignmentWorst())
		{
			setAlignment((AlignmentTypes) GC.getReligionInfo(eReligion).getAlignmentWorst());
		}
	}
//FfH: End Add

//>>>>Unofficial Bug Fix: Added by Denev 2010/02/20
//*** Validate queued research requirements because some techs requires certain state religion.
	for (CLLNode<TechTypes>* pResearchNode = headResearchQueueNode(); pResearchNode; pResearchNode = nextResearchQueueNode(pResearchNode))
	{
		if (!canEverResearch(pResearchNode->m_data))
		{
			bool bFinished = false;
			while (!bFinished)
			{
				bFinished = (tailResearchQueueNode()->m_data == pResearchNode->m_data);
				popResearch(tailResearchQueueNode()->m_data);
			}
			break;
		}
	}
//<<<<Unofficial Bug Fix: End Add
}


bool CvPlayer::hasHolyCity(ReligionTypes eReligion) const
{
	CvCity* pHolyCity;

	FAssertMsg(eReligion != NO_RELIGION, "Religion is not assigned a valid value");

	pHolyCity = GC.getGameINLINE().getHolyCity(eReligion);

	if (pHolyCity != NULL)
	{
		return (pHolyCity->getOwnerINLINE() == getID());
	}

	return false;
}


int CvPlayer::countHolyCities() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (hasHolyCity((ReligionTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}


void CvPlayer::foundReligion(ReligionTypes eReligion, ReligionTypes eSlotReligion, bool bAward)
{
	CvCity* pLoopCity;
	CvCity* pBestCity;
	UnitTypes eFreeUnit;
	bool bStarting;
	int iValue;
	int iBestValue;
	int iLoop;

	if (NO_RELIGION == eReligion)
	{
		return;
	}

//FfH: Added by Kael 10/29/2007
    if (GC.getGameINLINE().isReligionDisabled(eReligion))
    {
        return;
    }
//FfH: End Add

	if (GC.getGameINLINE().isReligionFounded(eReligion))
	{

//FfH: Modified by Kael 12/20/2008
//		if (isHuman())
//		{
//			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_FOUND_RELIGION, eSlotReligion);
//			if (NULL != pInfo)
//			{
//				gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
//			}
//		}
//		else
//		{
//			foundReligion(AI_chooseReligion(), eSlotReligion, bAward);
//		}
//FfH: End Modify

		return;
	}

	GC.getGameINLINE().setReligionSlotTaken(eSlotReligion, true);

	bStarting = ((GC.getReligionInfo(eSlotReligion).getTechPrereq() == NO_TECH) || (GC.getTechInfo((TechTypes) GC.getReligionInfo(eSlotReligion).getTechPrereq()).getEra() < GC.getGameINLINE().getStartEra()));

	iBestValue = 0;
	pBestCity = NULL;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (!bStarting || !(pLoopCity->isHolyCity()))
		{
			iValue = 10;
			iValue += pLoopCity->getPopulation();
			iValue += GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("FOUND_RELIGION_CITY_RAND"), "Found Religion");

			iValue /= (pLoopCity->getReligionCount() + 1);

			if (pLoopCity->isCapital())
			{
				iValue /= 8;
			}

//FfH: Added by Kael 11/18/2007
			if (pLoopCity->isSettlement())
			{
				iValue /= 8;
			}
//FfH: End Add

			iValue = std::max(1, iValue);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestCity = pLoopCity;
			}
		}
	}

	if (pBestCity != NULL)
	{
		GC.getGameINLINE().setHolyCity(eReligion, pBestCity, true);

		if (bAward)
		{
			if (GC.getReligionInfo(eSlotReligion).getNumFreeUnits() > 0)
			{
				eFreeUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getReligionInfo(eReligion).getFreeUnitClass())));

				if (eFreeUnit != NO_UNIT)
				{
					for (int i = 0; i < GC.getReligionInfo(eSlotReligion).getNumFreeUnits(); ++i)
					{
						initUnit(eFreeUnit, pBestCity->getX_INLINE(), pBestCity->getY_INLINE());
					}
				}
			}
		}
	}
}


bool CvPlayer::hasHeadquarters(CorporationTypes eCorporation) const
{
	CvCity* pHeadquarters = GC.getGameINLINE().getHeadquarters(eCorporation);

	FAssert(eCorporation != NO_CORPORATION);

	if (pHeadquarters != NULL)
	{
		return (pHeadquarters->getOwnerINLINE() == getID());
	}

	return false;
}


int CvPlayer::countHeadquarters() const
{
	int iCount = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (hasHeadquarters((CorporationTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}


int CvPlayer::countCorporations(CorporationTypes eCorporation) const
{
	int iCount = 0;

	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isHasCorporation(eCorporation))
		{
			++iCount;
		}
	}

	return iCount;
}


void CvPlayer::foundCorporation(CorporationTypes eCorporation)
{
	CvCity* pLoopCity;
	CvCity* pBestCity;
	bool bStarting;
	int iValue;
	int iBestValue;
	int iLoop;

	if (GC.getGameINLINE().isCorporationFounded(eCorporation))
	{
		return;
	}

	bStarting = ((GC.getCorporationInfo(eCorporation).getTechPrereq() == NO_TECH) || (GC.getTechInfo((TechTypes) GC.getCorporationInfo(eCorporation).getTechPrereq()).getEra() < GC.getGameINLINE().getStartEra()));

	iBestValue = 0;
	pBestCity = NULL;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (!bStarting || !(pLoopCity->isHeadquarters()))
		{
			iValue = 10;
			iValue += pLoopCity->getPopulation();

			for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
			{
				if (NO_BONUS != GC.getCorporationInfo(eCorporation).getPrereqBonus(i))
				{
					iValue += 10 * pLoopCity->getNumBonuses((BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i));
				}
			}

			iValue += GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("FOUND_CORPORATION_CITY_RAND"), "Found Corporation");

			iValue /= (pLoopCity->getCorporationCount() + 1);

			iValue = std::max(1, iValue);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestCity = pLoopCity;
			}
		}
	}

	if (pBestCity != NULL)
	{
		pBestCity->setHeadquarters(eCorporation);
	}
}


int CvPlayer::getCivicAnarchyLength(CivicTypes* paeNewCivics) const
{
	bool bChange;
	int iAnarchyLength;
	int iI;

	if (getMaxAnarchyTurns() == 0)
	{
		return 0;
	}

	if (isGoldenAge())
	{
		return 0;
	}

	iAnarchyLength = 0;

	bChange = false;

	for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (paeNewCivics[iI] != getCivics((CivicOptionTypes)iI))
		{
			iAnarchyLength += GC.getCivicInfo(paeNewCivics[iI]).getAnarchyLength();

			bChange = true;
		}
	}

	if (bChange)
	{
		iAnarchyLength += GC.getDefineINT("BASE_CIVIC_ANARCHY_LENGTH");

		iAnarchyLength += ((getNumCities() * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getNumCitiesAnarchyPercent()) / 100);
	}

	iAnarchyLength = ((iAnarchyLength * std::max(0, (getAnarchyModifier() + 100))) / 100);

	if (iAnarchyLength == 0)
	{
		return 0;
	}

	iAnarchyLength *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent();
	iAnarchyLength /= 100;

	iAnarchyLength *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getAnarchyPercent();
	iAnarchyLength /= 100;

/************************************************************************************************/
/* REVOLUTION_MOD                         02/01/08                                jdog5000      */
/*                                                                                              */
/* Rebels suffer less civic switch anarchy                                                      */
/************************************************************************************************/
	if( isRebel() )
		iAnarchyLength /= 2;
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	return range(iAnarchyLength, 1, getMaxAnarchyTurns());
}


int CvPlayer::getReligionAnarchyLength() const
{
	int iAnarchyLength;

	if (getMaxAnarchyTurns() == 0)
	{
		return 0;
	}

	if (isGoldenAge())
	{
		return 0;
	}

	iAnarchyLength = GC.getDefineINT("BASE_RELIGION_ANARCHY_LENGTH");

	iAnarchyLength += ((getNumCities() * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getNumCitiesAnarchyPercent()) / 100);

	iAnarchyLength = ((iAnarchyLength * std::max(0, (getAnarchyModifier() + 100))) / 100);

	if (iAnarchyLength == 0)
	{
		return 0;
	}

	iAnarchyLength *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent();
	iAnarchyLength /= 100;

	iAnarchyLength *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getAnarchyPercent();
	iAnarchyLength /= 100;

	return range(iAnarchyLength, 1, getMaxAnarchyTurns());
}



int CvPlayer::unitsRequiredForGoldenAge() const
{
	return (GC.getDefineINT("BASE_GOLDEN_AGE_UNITS") + (getNumUnitGoldenAges() * GC.getDefineINT("GOLDEN_AGE_UNITS_MULTIPLIER")));
}


int CvPlayer::unitsGoldenAgeCapable() const
{
	CvUnit* pLoopUnit;
	int iCount;
	int iLoop;

	iCount = 0;

	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->isGoldenAge())
		{
			iCount++;
		}
	}

	return iCount;
}


int CvPlayer::unitsGoldenAgeReady() const
{
	PROFILE_FUNC();

	CvUnit* pLoopUnit;
	bool* pabUnitUsed;
	int iCount;
	int iLoop;
	int iI;

	pabUnitUsed = new bool[GC.getNumUnitInfos()];

	for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		pabUnitUsed[iI] = false;
	}

	iCount = 0;

	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (!(pabUnitUsed[pLoopUnit->getUnitType()]))
		{
		if (pLoopUnit->isGoldenAge())
		{
				pabUnitUsed[pLoopUnit->getUnitType()] = true;
				iCount++;
			}
		}
	}

	SAFE_DELETE_ARRAY(pabUnitUsed);

	return iCount;
}


void CvPlayer::killGoldenAgeUnits(CvUnit* pUnitAlive)
{
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;
	bool* pabUnitUsed;
	int iUnitsRequired;
	int iValue;
	int iBestValue;
	int iLoop;
	int iI;

	pabUnitUsed = new bool[GC.getNumUnitInfos()];

	for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		pabUnitUsed[iI] = false;
	}

	iUnitsRequired = unitsRequiredForGoldenAge();

	if (pUnitAlive != NULL)
	{
		pabUnitUsed[pUnitAlive->getUnitType()] = true;
		iUnitsRequired--;
	}

	for (iI = 0; iI < iUnitsRequired; iI++)
	{
		iBestValue = 0;
		pBestUnit = NULL;

		for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (pLoopUnit->isGoldenAge())
			{
				if (!(pabUnitUsed[pLoopUnit->getUnitType()]))
				{
					iValue = 10000;

					iValue /= (plotDistance(pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE(), pUnitAlive->getX_INLINE(), pUnitAlive->getY_INLINE()) + 1);

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestUnit = pLoopUnit;
					}
				}
			}
		}

		FAssert(pBestUnit != NULL);
		if (pBestUnit != NULL)
		{
			pabUnitUsed[pBestUnit->getUnitType()] = true;
			
			// lfgr 07/2019: transport units unload cargo when they start a golden age
			if (pBestUnit->getCargo() > 0)
			{
				pBestUnit->unloadAll();
			}
			
			logBBAI("    Killing %S (delayed) -- golden age (Unit %d - plot: %d, %d)",
					pBestUnit->getName().GetCString(), pBestUnit->getID(), pBestUnit->getX(), pBestUnit->getY());
			pBestUnit->kill(true);

			//play animations
			if (pBestUnit->plot()->isActiveVisible(false))
			{
				//kill removes bestUnit from any groups
				pBestUnit->getGroup()->pushMission(MISSION_GOLDEN_AGE, 0);
			}
		}
	}

	SAFE_DELETE_ARRAY(pabUnitUsed);
}


int CvPlayer::greatPeopleThreshold(bool bMilitary) const
{
	int iThreshold;

	if (bMilitary)
	{
		iThreshold = ((GC.getDefineINT("GREAT_GENERALS_THRESHOLD") * std::max(0, (getGreatGeneralsThresholdModifier() + 100))) / 100);
	}
	else
	{
		iThreshold = ((GC.getDefineINT("GREAT_PEOPLE_THRESHOLD") * std::max(0, (getGreatPeopleThresholdModifier() + 100))) / 100);
	}

	iThreshold *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGreatPeoplePercent();
	if (bMilitary)
	{
		iThreshold /= std::max(1, GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent());
	}
	else
	{
		iThreshold /= 100;
	}

	iThreshold *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getGreatPeoplePercent();
	iThreshold /= 100;


	return std::max(1, iThreshold);
}


int CvPlayer::specialistYield(SpecialistTypes eSpecialist, YieldTypes eYield) const
{
	return (GC.getSpecialistInfo(eSpecialist).getYieldChange(eYield) + getSpecialistExtraYield(eSpecialist, eYield));
}


int CvPlayer::specialistCommerce(SpecialistTypes eSpecialist, CommerceTypes eCommerce) const
{

//FfH: Modified by Kael 11/08/2007
//	return (GC.getSpecialistInfo(eSpecialist).getCommerceChange(eCommerce) + getSpecialistExtraCommerce(eCommerce));
	return (GC.getSpecialistInfo(eSpecialist).getCommerceChange(eCommerce) + getSpecialistExtraCommerce(eCommerce) + getSpecialistTypeExtraCommerce(eSpecialist, eCommerce));
//FfH: End Modify

}


CvPlot* CvPlayer::getStartingPlot() const
{
	return GC.getMapINLINE().plotSorenINLINE(m_iStartingX, m_iStartingY);
}


void CvPlayer::setStartingPlot(CvPlot* pNewValue, bool bUpdateStartDist)
{
	CvPlot* pOldStartingPlot;

	pOldStartingPlot = getStartingPlot();

	if (pOldStartingPlot != pNewValue)
	{
		if (pOldStartingPlot != NULL)
		{
			pOldStartingPlot->area()->changeNumStartingPlots(-1);

			if (bUpdateStartDist)
			{
				GC.getMapINLINE().updateMinOriginalStartDist(pOldStartingPlot->area());
			}
		}

		if (pNewValue == NULL)
		{
			m_iStartingX = INVALID_PLOT_COORD;
			m_iStartingY = INVALID_PLOT_COORD;
		}
		else
		{
			m_iStartingX = pNewValue->getX_INLINE();
			m_iStartingY = pNewValue->getY_INLINE();

			getStartingPlot()->area()->changeNumStartingPlots(1);

			if (bUpdateStartDist)
			{
				GC.getMapINLINE().updateMinOriginalStartDist(getStartingPlot()->area());
			}
		}
	}
}


int CvPlayer::getTotalPopulation() const
{
	return m_iTotalPopulation;
}


int CvPlayer::getAveragePopulation() const
{
	if (getNumCities() == 0)
	{
		return 0;
	}

	return ((getTotalPopulation() / getNumCities()) + 1);
}


void CvPlayer::changeTotalPopulation(int iChange)
{
	changeAssets(-(getPopulationAsset(getTotalPopulation())));
	changePower(-(getPopulationPower(getTotalPopulation())));
	changePopScore(-(getPopulationScore(getTotalPopulation())));

	m_iTotalPopulation = (m_iTotalPopulation + iChange);
	FAssert(getTotalPopulation() >= 0);

	changeAssets(getPopulationAsset(getTotalPopulation()));
	changePower(getPopulationPower(getTotalPopulation()));
	changePopScore(getPopulationScore(getTotalPopulation()));
}


long CvPlayer::getRealPopulation() const
{
	CvCity* pLoopCity;
	__int64 iTotalPopulation = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalPopulation += pLoopCity->getRealPopulation();
	}

	if (iTotalPopulation > MAX_INT)
	{
		iTotalPopulation = MAX_INT;
	}

	return ((long)(iTotalPopulation));
}


int CvPlayer::getTotalLand() const
{
	return m_iTotalLand;
}


void CvPlayer::changeTotalLand(int iChange)
{
	m_iTotalLand = (m_iTotalLand + iChange);
	FAssert(getTotalLand() >= 0);
}


int CvPlayer::getTotalLandScored() const
{
	return m_iTotalLandScored;
}


void CvPlayer::changeTotalLandScored(int iChange)
{
	if (iChange != 0)
	{
		changeAssets(-(getLandPlotsAsset(getTotalLandScored())));
		changeLandScore(-(getLandPlotsScore(getTotalLandScored())));

		m_iTotalLandScored = (m_iTotalLandScored + iChange);
		FAssert(getTotalLandScored() >= 0);

		changeAssets(getLandPlotsAsset(getTotalLandScored()));
		changeLandScore(getLandPlotsScore(getTotalLandScored()));
	}
}


int CvPlayer::getGold() const
{
	return m_iGold;
}


void CvPlayer::setGold(int iNewValue)
{
	if (getGold() != iNewValue)
	{
		m_iGold = iNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

void CvPlayer::changeGold(int iChange)
{
	setGold(getGold() + iChange);
}

int CvPlayer::getGoldPerTurn() const
{
	return m_iGoldPerTurn;
}

int CvPlayer::getAdvancedStartPoints() const
{
	return m_iAdvancedStartPoints;
}


void CvPlayer::setAdvancedStartPoints(int iNewValue)
{
	if (getAdvancedStartPoints() != iNewValue)
	{
		m_iAdvancedStartPoints = iNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

void CvPlayer::changeAdvancedStartPoints(int iChange)
{
	setAdvancedStartPoints(getAdvancedStartPoints() + iChange);
}


int CvPlayer::getGoldenAgeTurns() const
{
	return m_iGoldenAgeTurns;
}


bool CvPlayer::isGoldenAge() const
{
	return (getGoldenAgeTurns() > 0);
}


void CvPlayer::changeGoldenAgeTurns(int iChange)
{
	CvWString szBuffer;
	bool bOldGoldenAge;
	int iI;

	if (iChange != 0)
	{
		bOldGoldenAge = isGoldenAge();

		m_iGoldenAgeTurns = (m_iGoldenAgeTurns + iChange);
		FAssert(getGoldenAgeTurns() >= 0);

		if (bOldGoldenAge != isGoldenAge())
		{
			if (isGoldenAge())
			{
				changeAnarchyTurns(-getAnarchyTurns());
			}

			updateYield();

			if (isGoldenAge())
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_GOLDEN_AGE_BEGINS", getNameKey());
				GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

				CvEventReporter::getInstance().goldenAge(getID());
			}
			else
			{
				CvEventReporter::getInstance().endGoldenAge(getID());
			}

			for (iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						if (isGoldenAge())
						{
							szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_GOLDEN_AGE_HAS_BEGUN", getNameKey());
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), (((PlayerTypes)iI) == getID()), GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_GOLDAGESTART", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_PLAYER_YELLOW"));
						}
						else
						{
							szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_GOLDEN_AGE_ENDED", getNameKey());
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_GOLDAGEEND", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_PLAYER_YELLOW"));
						}
					}
				}
			}
		}

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

int CvPlayer::getGoldenAgeLength() const
{
	return (GC.getGameINLINE().goldenAgeLength() * std::max(0, 100 + getGoldenAgeModifier())) / 100;
}

int CvPlayer::getNumUnitGoldenAges() const
{
	return m_iNumUnitGoldenAges;
}


void CvPlayer::changeNumUnitGoldenAges(int iChange)
{
	m_iNumUnitGoldenAges = (m_iNumUnitGoldenAges + iChange);
	FAssert(getNumUnitGoldenAges() >= 0);
}


int CvPlayer::getStrikeTurns() const
{
	return m_iStrikeTurns;
}


void CvPlayer::changeStrikeTurns(int iChange)
{
	m_iStrikeTurns = (m_iStrikeTurns + iChange);
	FAssert(getStrikeTurns() >= 0);
}


int CvPlayer::getAnarchyTurns() const
{
	return m_iAnarchyTurns;
}


bool CvPlayer::isAnarchy() const
{
	return (getAnarchyTurns() > 0);
}


void CvPlayer::changeAnarchyTurns(int iChange)
{
	bool bOldAnarchy;

	if (iChange != 0)
	{
		bOldAnarchy = isAnarchy();

		m_iAnarchyTurns = (m_iAnarchyTurns + iChange);
		FAssert(getAnarchyTurns() >= 0);

		if (bOldAnarchy != isAnarchy())
		{
			updateCommerce();
			updateMaintenance();
			updateTradeRoutes();
			updateCorporation();

			AI_makeAssignWorkDirty();

			if (isAnarchy())
			{
				gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_REVOLUTION_HAS_BEGUN").GetCString(), "AS2D_REVOLTSTART", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
			}
			else
			{
				gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_REVOLUTION_OVER").GetCString(), "AS2D_REVOLTEND", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
			}

			if (getTeam() == GC.getGameINLINE().getActiveTeam())
			{
				gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
			}
		}

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getMaxAnarchyTurns() const
{
	return m_iMaxAnarchyTurns;
}


void CvPlayer::updateMaxAnarchyTurns()
{
	int iBestValue;
	int iI;

	iBestValue = GC.getDefineINT("MAX_ANARCHY_TURNS");

	FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::updateMaxAnarchyTurns");
	for (iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			if (GC.getTraitInfo((TraitTypes)iI).getMaxAnarchy() >= 0)
			{
				if (GC.getTraitInfo((TraitTypes)iI).getMaxAnarchy() < iBestValue)
				{
					iBestValue = GC.getTraitInfo((TraitTypes)iI).getMaxAnarchy();
				}
			}
		}
	}

	m_iMaxAnarchyTurns = iBestValue;
	FAssert(getMaxAnarchyTurns() >= 0);
}


int CvPlayer::getAnarchyModifier() const
{
	return m_iAnarchyModifier;
}


void CvPlayer::changeAnarchyModifier(int iChange)
{
	if (0 != iChange)
	{
	m_iAnarchyModifier += iChange;

		setRevolutionTimer(std::max(0, ((100 + iChange) * getRevolutionTimer()) / 100));
		setConversionTimer(std::max(0, ((100 + iChange) * getConversionTimer()) / 100));
	}
}


int CvPlayer::getGoldenAgeModifier() const
{
	return m_iGoldenAgeModifier;
}


void CvPlayer::changeGoldenAgeModifier(int iChange)
{
	m_iGoldenAgeModifier += iChange;
}


int CvPlayer::getHurryModifier() const
{
	return m_iGlobalHurryModifier;
}


void CvPlayer::changeHurryModifier(int iChange)
{
	m_iGlobalHurryModifier = (m_iGlobalHurryModifier + iChange);
}


int CvPlayer::getGreatPeopleCreated() const
{
	return m_iGreatPeopleCreated;
}


void CvPlayer::incrementGreatPeopleCreated()
{
	m_iGreatPeopleCreated++;
}

int CvPlayer::getGreatGeneralsCreated() const
{
	return m_iGreatGeneralsCreated;
}

void CvPlayer::incrementGreatGeneralsCreated()
{
	m_iGreatGeneralsCreated++;
}

int CvPlayer::getGreatPeopleThresholdModifier() const
{
	return m_iGreatPeopleThresholdModifier;
}


void CvPlayer::changeGreatPeopleThresholdModifier(int iChange)
{
	m_iGreatPeopleThresholdModifier = (m_iGreatPeopleThresholdModifier + iChange);
}


int CvPlayer::getGreatGeneralsThresholdModifier() const
{
	return m_iGreatGeneralsThresholdModifier;
}


void CvPlayer::changeGreatGeneralsThresholdModifier(int iChange)
{
	m_iGreatGeneralsThresholdModifier += iChange;
}


int CvPlayer::getGreatPeopleRateModifier() const
{
	return m_iGreatPeopleRateModifier;
}


void CvPlayer::changeGreatPeopleRateModifier(int iChange)
{
	m_iGreatPeopleRateModifier = (m_iGreatPeopleRateModifier + iChange);
}


int CvPlayer::getGreatGeneralRateModifier() const
{
	return m_iGreatGeneralRateModifier;
}


void CvPlayer::changeGreatGeneralRateModifier(int iChange)
{
	m_iGreatGeneralRateModifier += iChange;
}


int CvPlayer::getDomesticGreatGeneralRateModifier() const
{
	return (GC.getDefineINT("COMBAT_EXPERIENCE_IN_BORDERS_PERCENT") + m_iDomesticGreatGeneralRateModifier);
}


void CvPlayer::changeDomesticGreatGeneralRateModifier(int iChange)
{
	m_iDomesticGreatGeneralRateModifier += iChange;
}


int CvPlayer::getStateReligionGreatPeopleRateModifier() const
{
	return m_iStateReligionGreatPeopleRateModifier;
}


void CvPlayer::changeStateReligionGreatPeopleRateModifier(int iChange)
{
	m_iStateReligionGreatPeopleRateModifier = (m_iStateReligionGreatPeopleRateModifier + iChange);
}


int CvPlayer::getMaxGlobalBuildingProductionModifier() const
{
	return m_iMaxGlobalBuildingProductionModifier;
}


void CvPlayer::changeMaxGlobalBuildingProductionModifier(int iChange)
{
	m_iMaxGlobalBuildingProductionModifier = (m_iMaxGlobalBuildingProductionModifier + iChange);
}


int CvPlayer::getMaxTeamBuildingProductionModifier() const
{
	return m_iMaxTeamBuildingProductionModifier;
}


void CvPlayer::changeMaxTeamBuildingProductionModifier(int iChange)
{
	m_iMaxTeamBuildingProductionModifier = (m_iMaxTeamBuildingProductionModifier + iChange);
}


int CvPlayer::getMaxPlayerBuildingProductionModifier() const
{
	return m_iMaxPlayerBuildingProductionModifier;
}


void CvPlayer::changeMaxPlayerBuildingProductionModifier(int iChange)
{
	m_iMaxPlayerBuildingProductionModifier = (m_iMaxPlayerBuildingProductionModifier + iChange);
}


int CvPlayer::getFreeExperience() const
{
	return m_iFreeExperience;
}


void CvPlayer::changeFreeExperience(int iChange)
{
	m_iFreeExperience = (m_iFreeExperience + iChange);
}


int CvPlayer::getFeatureProductionModifier() const
{
	return m_iFeatureProductionModifier;
}


void CvPlayer::changeFeatureProductionModifier(int iChange)
{
	m_iFeatureProductionModifier = (m_iFeatureProductionModifier + iChange);
}


int CvPlayer::getWorkerSpeedModifier() const
{
	return m_iWorkerSpeedModifier;
}


void CvPlayer::changeWorkerSpeedModifier(int iChange)
{
	m_iWorkerSpeedModifier = (m_iWorkerSpeedModifier + iChange);
}

// BUG - Partial Builds - start
/*
 * Returns the work rate for the first unit that can build <eBuild>.
 */
int CvPlayer::getWorkRate(BuildTypes eBuild) const
{
	int iRate = 0;
	CvCivilizationInfo& kCiv = GC.getCivilizationInfo(getCivilizationType());

	for (int iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
	{
		UnitTypes kUnit = (UnitTypes)kCiv.getCivilizationUnits(iI);
		if (kUnit != NO_UNIT)
		{
			CvUnitInfo& kUnitInfo = GC.getUnitInfo(kUnit);

			if (kUnitInfo.getBuilds(eBuild))
			{
				iRate = kUnitInfo.getWorkRate();
				break;
			}
		}
	}

	iRate *= std::max(0, getWorkerSpeedModifier() + 100);
	iRate /= 100;

	if (!isHuman() && !isBarbarian())
	{
		iRate *= std::max(0, (GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWorkRateModifier() + 100));
		iRate /= 100;
	}

	return iRate;
}
// BUG - Partial Builds - end


int CvPlayer::getImprovementUpgradeRateModifier() const
{
	return m_iImprovementUpgradeRateModifier;
}


void CvPlayer::changeImprovementUpgradeRateModifier(int iChange)
{
	m_iImprovementUpgradeRateModifier = (m_iImprovementUpgradeRateModifier + iChange);
}


int CvPlayer::getMilitaryProductionModifier() const
{
	return m_iMilitaryProductionModifier;
}


void CvPlayer::changeMilitaryProductionModifier(int iChange)
{
	m_iMilitaryProductionModifier = (m_iMilitaryProductionModifier + iChange);
}


int CvPlayer::getSpaceProductionModifier() const
{
	return m_iSpaceProductionModifier;
}


void CvPlayer::changeSpaceProductionModifier(int iChange)
{
	m_iSpaceProductionModifier = (m_iSpaceProductionModifier + iChange);
}


int CvPlayer::getCityDefenseModifier() const
{
	return m_iCityDefenseModifier;
}


void CvPlayer::changeCityDefenseModifier(int iChange)
{
	m_iCityDefenseModifier = (m_iCityDefenseModifier + iChange);
}


/************************************************************************************************/
/* REVDCM                                 09/02/10                                phungus420    */
/*                                                                                              */
/* Player Functions                                                                             */
/************************************************************************************************/
bool CvPlayer::isNonStateReligionCommerce() const
{
	if (m_iNonStateReligionCommerceCount > 0)
	{
		return true;
	}
	return false;
}

void CvPlayer::changeNonStateReligionCommerce(int iNewValue)
{
	FAssert(m_iNonStateReligionCommerceCount >= 0 && m_iNonStateReligionCommerceCount <= 2);

    m_iNonStateReligionCommerceCount += iNewValue;

	if(iNewValue != 0)
	{
		updateReligionCommerce();
		AI_makeAssignWorkDirty();
    }
}

// MNAI  - defaults to true
bool CvPlayer::canInquisition() const
{
	return m_bCanInquisition;
}

void CvPlayer::setCanInquisition(bool bNewValue)
{
	m_bCanInquisition = bNewValue;
}
// End MNAI
/************************************************************************************************/
/* REVDCM                                  END                                                  */
/************************************************************************************************/


int CvPlayer::getNumNukeUnits() const
{
	return m_iNumNukeUnits;
}


void CvPlayer::changeNumNukeUnits(int iChange)
{
	m_iNumNukeUnits = (m_iNumNukeUnits + iChange);
	FAssert(getNumNukeUnits() >= 0);
}


int CvPlayer::getNumOutsideUnits() const
{
	return m_iNumOutsideUnits;
}


void CvPlayer::changeNumOutsideUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iNumOutsideUnits += iChange;
		//FAssert(getNumOutsideUnits() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getBaseFreeUnits() const
{
	return m_iBaseFreeUnits;
}


void CvPlayer::changeBaseFreeUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iBaseFreeUnits = (m_iBaseFreeUnits + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getBaseFreeMilitaryUnits() const
{
	return m_iBaseFreeMilitaryUnits;
}


void CvPlayer::changeBaseFreeMilitaryUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iBaseFreeMilitaryUnits = (m_iBaseFreeMilitaryUnits + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getFreeUnitsPopulationPercent() const
{
	return m_iFreeUnitsPopulationPercent;
}


void CvPlayer::changeFreeUnitsPopulationPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeUnitsPopulationPercent = (m_iFreeUnitsPopulationPercent + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getFreeMilitaryUnitsPopulationPercent() const
{
	return m_iFreeMilitaryUnitsPopulationPercent;
}


void CvPlayer::changeFreeMilitaryUnitsPopulationPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeMilitaryUnitsPopulationPercent = (m_iFreeMilitaryUnitsPopulationPercent + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getGoldPerUnit() const
{
	return m_iGoldPerUnit;
}


void CvPlayer::changeGoldPerUnit(int iChange)
{
	if (iChange != 0)
	{
		m_iGoldPerUnit = (m_iGoldPerUnit + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getGoldPerMilitaryUnit() const
{
	return m_iGoldPerMilitaryUnit;
}


void CvPlayer::changeGoldPerMilitaryUnit(int iChange)
{
	if (iChange != 0)
	{
		m_iGoldPerMilitaryUnit = (m_iGoldPerMilitaryUnit + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getExtraUnitCost() const
{
	return m_iExtraUnitCost;
}


void CvPlayer::changeExtraUnitCost(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraUnitCost = (m_iExtraUnitCost + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getNumMilitaryUnits() const
{
	return m_iNumMilitaryUnits;
}


void CvPlayer::changeNumMilitaryUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iNumMilitaryUnits = (m_iNumMilitaryUnits + iChange);
		FAssert(getNumMilitaryUnits() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getHappyPerMilitaryUnit() const
{
	return m_iHappyPerMilitaryUnit;
}


void CvPlayer::changeHappyPerMilitaryUnit(int iChange)
{
	if (iChange != 0)
	{
		m_iHappyPerMilitaryUnit = (m_iHappyPerMilitaryUnit + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getMilitaryFoodProductionCount() const
{
	return m_iMilitaryFoodProductionCount;
}


bool CvPlayer::isMilitaryFoodProduction() const
{
	return (getMilitaryFoodProductionCount() > 0);
}


void CvPlayer::changeMilitaryFoodProductionCount(int iChange)
{
	if (iChange != 0)
	{
		m_iMilitaryFoodProductionCount = (m_iMilitaryFoodProductionCount + iChange);
		FAssert(getMilitaryFoodProductionCount() >= 0);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getHighestUnitLevel()	const
{
	return m_iHighestUnitLevel;
}


void CvPlayer::setHighestUnitLevel(int iNewValue)
{
	m_iHighestUnitLevel = iNewValue;
	FAssert(getHighestUnitLevel() >= 0);
}


int CvPlayer::getMaxConscript() const
{
	return m_iMaxConscript;
}


void CvPlayer::changeMaxConscript(int iChange)
{
	m_iMaxConscript = (m_iMaxConscript + iChange);
	FAssert(getMaxConscript() >= 0);
}


int CvPlayer::getConscriptCount() const
{
	return m_iConscriptCount;
}


void CvPlayer::setConscriptCount(int iNewValue)
{
	m_iConscriptCount = iNewValue;
	FAssert(getConscriptCount() >= 0);
}


void CvPlayer::changeConscriptCount(int iChange)
{
	setConscriptCount(getConscriptCount() + iChange);
}


int CvPlayer::getOverflowResearch() const
{
	return m_iOverflowResearch;
}


void CvPlayer::setOverflowResearch(int iNewValue)
{
	m_iOverflowResearch = iNewValue;
	FAssert(getOverflowResearch() >= 0);
}


void CvPlayer::changeOverflowResearch(int iChange)
{
	setOverflowResearch(getOverflowResearch() + iChange);
}


int CvPlayer::getNoUnhealthyPopulationCount() const
{
	return m_iNoUnhealthyPopulationCount;
}


bool CvPlayer::isNoUnhealthyPopulation() const
{
	return (getNoUnhealthyPopulationCount() > 0);
}


void CvPlayer::changeNoUnhealthyPopulationCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhealthyPopulationCount = (m_iNoUnhealthyPopulationCount + iChange);
		FAssert(getNoUnhealthyPopulationCount() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getExpInBorderModifier() const
{
	return m_iExpInBorderModifier;
}


void CvPlayer::changeExpInBorderModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iExpInBorderModifier += iChange;
		FAssert(getExpInBorderModifier() >= 0);
	}
}


int CvPlayer::getBuildingOnlyHealthyCount() const
{
	return m_iBuildingOnlyHealthyCount;
}


bool CvPlayer::isBuildingOnlyHealthy() const
{
	return (getBuildingOnlyHealthyCount() > 0);
}


void CvPlayer::changeBuildingOnlyHealthyCount(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingOnlyHealthyCount = (m_iBuildingOnlyHealthyCount + iChange);
		FAssert(getBuildingOnlyHealthyCount() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getDistanceMaintenanceModifier() const
{
	return m_iDistanceMaintenanceModifier;
}


void CvPlayer::changeDistanceMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iDistanceMaintenanceModifier += iChange;

		updateMaintenance();
	}
}


int CvPlayer::getNumCitiesMaintenanceModifier() const
{
	return m_iNumCitiesMaintenanceModifier;
}


void CvPlayer::changeNumCitiesMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iNumCitiesMaintenanceModifier += iChange;

		updateMaintenance();
	}
}


int CvPlayer::getCorporationMaintenanceModifier() const
{
	return m_iCorporationMaintenanceModifier;
}


void CvPlayer::changeCorporationMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iCorporationMaintenanceModifier += iChange;

		updateMaintenance();
	}
}


int CvPlayer::getTotalMaintenance() const
{
	return m_iTotalMaintenance / 100;
}


void CvPlayer::changeTotalMaintenance(int iChange)
{
	m_iTotalMaintenance += iChange;
	FAssert(m_iTotalMaintenance >= 0);
}


int CvPlayer::getUpkeepModifier() const
{
	return m_iUpkeepModifier;
}


void CvPlayer::changeUpkeepModifier(int iChange)
{
	m_iUpkeepModifier = (m_iUpkeepModifier + iChange);
}


int CvPlayer::getLevelExperienceModifier() const
{
	return m_iLevelExperienceModifier;
}

void CvPlayer::changeLevelExperienceModifier(int iChange)
{
	m_iLevelExperienceModifier += iChange;
}



int CvPlayer::getExtraHealth() const
{
	return m_iExtraHealth;
}


void CvPlayer::changeExtraHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHealth = (m_iExtraHealth + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getBuildingGoodHealth() const
{
	return m_iBuildingGoodHealth;
}


void CvPlayer::changeBuildingGoodHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingGoodHealth = (m_iBuildingGoodHealth + iChange);
		FAssert(getBuildingGoodHealth() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getBuildingBadHealth() const
{
	return m_iBuildingBadHealth;
}


void CvPlayer::changeBuildingBadHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBadHealth = (m_iBuildingBadHealth + iChange);
		FAssert(getBuildingBadHealth() <= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getExtraHappiness() const
{
	return m_iExtraHappiness;
}


void CvPlayer::changeExtraHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHappiness = (m_iExtraHappiness + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getBuildingHappiness() const
{
	return m_iBuildingHappiness;
}


void CvPlayer::changeBuildingHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingHappiness = (m_iBuildingHappiness + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getLargestCityHappiness() const
{
	return m_iLargestCityHappiness;
}


void CvPlayer::changeLargestCityHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iLargestCityHappiness = (m_iLargestCityHappiness + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getWarWearinessPercentAnger() const
{

//FfH: Added by Kael 11/17/2008
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_WAR_WEARINESS))
	{
	    return 0;
	}
//FfH: End Add

	return m_iWarWearinessPercentAnger;
}


void CvPlayer::updateWarWearinessPercentAnger()
{
	int iNewWarWearinessPercentAnger;
	int iI;

	iNewWarWearinessPercentAnger = 0;

	if (!isBarbarian() && !isMinorCiv())
	{
		for (iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iI);
			if (kTeam.isAlive() && !kTeam.isMinorCiv())
			{
				if (kTeam.isAtWar(getTeam()))
				{
					iNewWarWearinessPercentAnger += (GET_TEAM(getTeam()).getWarWeariness((TeamTypes)iI) * std::max(0, 100 + kTeam.getEnemyWarWearinessModifier())) / 10000;
				}
			}
		}
	}

	iNewWarWearinessPercentAnger = getModifiedWarWearinessPercentAnger(iNewWarWearinessPercentAnger);

	if (getWarWearinessPercentAnger() != iNewWarWearinessPercentAnger)
	{
		m_iWarWearinessPercentAnger = iNewWarWearinessPercentAnger;

		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getModifiedWarWearinessPercentAnger(int iWarWearinessPercentAnger) const
{
	iWarWearinessPercentAnger *= GC.getDefineINT("BASE_WAR_WEARINESS_MULTIPLIER");

	if (GC.getGameINLINE().isOption(GAMEOPTION_ALWAYS_WAR) || GC.getGameINLINE().isOption(GAMEOPTION_NO_CHANGING_WAR_PEACE))
	{
		iWarWearinessPercentAnger *= std::max(0, (GC.getDefineINT("FORCED_WAR_WAR_WEARINESS_MODIFIER") + 100));
		iWarWearinessPercentAnger /= 100;
	}

	if (GC.getGameINLINE().isGameMultiPlayer())
	{
		iWarWearinessPercentAnger *= std::max(0, (GC.getDefineINT("MULTIPLAYER_WAR_WEARINESS_MODIFIER") + 100));
		iWarWearinessPercentAnger /= 100;
	}

	iWarWearinessPercentAnger *= std::max(0, (GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getWarWearinessModifier() + 100));
	iWarWearinessPercentAnger /= 100;

	if (!isHuman() && !isBarbarian() && !isMinorCiv())
	{
		iWarWearinessPercentAnger *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWarWearinessPercent();
		iWarWearinessPercentAnger /= 100;

		iWarWearinessPercentAnger *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * GC.getGameINLINE().getCurrentEra()) + 100));
		iWarWearinessPercentAnger /= 100;
	}

	return iWarWearinessPercentAnger;
}


int CvPlayer::getWarWearinessModifier() const
{
	return m_iWarWearinessModifier;
}


void CvPlayer::changeWarWearinessModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iWarWearinessModifier = (m_iWarWearinessModifier + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getFreeSpecialist() const
{
	return m_iFreeSpecialist;
}


void CvPlayer::changeFreeSpecialist(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeSpecialist = (m_iFreeSpecialist + iChange);
		FAssert(getFreeSpecialist() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getNoForeignTradeCount() const
{
	return m_iNoForeignTradeCount;
}


bool CvPlayer::isNoForeignTrade() const
{
	return (getNoForeignTradeCount() > 0);
}


void CvPlayer::changeNoForeignTradeCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoForeignTradeCount = (m_iNoForeignTradeCount + iChange);
		FAssert(getNoForeignTradeCount() >= 0);

		GC.getGameINLINE().updateTradeRoutes();
	}
}


int CvPlayer::getNoCorporationsCount() const
{
	return m_iNoCorporationsCount;
}


bool CvPlayer::isNoCorporations() const
{
	return (getNoCorporationsCount() > 0);
}


void CvPlayer::changeNoCorporationsCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoCorporationsCount += iChange;
		FAssert(getNoCorporationsCount() >= 0);

		updateCorporation();
	}
}


int CvPlayer::getNoForeignCorporationsCount() const
{
	return m_iNoForeignCorporationsCount;
}


bool CvPlayer::isNoForeignCorporations() const
{
	return (getNoForeignCorporationsCount() > 0);
}


void CvPlayer::changeNoForeignCorporationsCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoForeignCorporationsCount += iChange;
		FAssert(getNoForeignCorporationsCount() >= 0);

		updateCorporation();
	}
}


int CvPlayer::getCoastalTradeRoutes() const
{
	return m_iCoastalTradeRoutes;
}


void CvPlayer::changeCoastalTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iCoastalTradeRoutes = (m_iCoastalTradeRoutes + iChange);
		FAssert(getCoastalTradeRoutes() >= 0);

		updateTradeRoutes();
	}
}


int CvPlayer::getTradeRoutes() const
{
	return m_iTradeRoutes;
}


void CvPlayer::changeTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iTradeRoutes = (m_iTradeRoutes + iChange);
		FAssert(getTradeRoutes() >= 0);

		updateTradeRoutes();
	}
}


int CvPlayer::getRevolutionTimer() const
{
	return m_iRevolutionTimer;
}


void CvPlayer::setRevolutionTimer(int iNewValue)
{
	if (getRevolutionTimer() != iNewValue)
	{
		m_iRevolutionTimer = iNewValue;
		FAssert(getRevolutionTimer() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
		}
	}
}


void CvPlayer::changeRevolutionTimer(int iChange)
{
	setRevolutionTimer(getRevolutionTimer() + iChange);
}


int CvPlayer::getConversionTimer() const
{
	return m_iConversionTimer;
}


void CvPlayer::setConversionTimer(int iNewValue)
{
	if (getConversionTimer() != iNewValue)
	{
		m_iConversionTimer = iNewValue;
		FAssert(getConversionTimer() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
		}
	}
}


void CvPlayer::changeConversionTimer(int iChange)
{
	setConversionTimer(getConversionTimer() + iChange);
}


int CvPlayer::getStateReligionCount() const
{
	return m_iStateReligionCount;
}


bool CvPlayer::isStateReligion() const
{
	return (getStateReligionCount() > 0);
}


void CvPlayer::changeStateReligionCount(int iChange)
{
	if (iChange != 0)
	{
		// religion visibility now part of espionage
		//GC.getGameINLINE().updateCitySight(false);

		m_iStateReligionCount = (m_iStateReligionCount + iChange);
		FAssert(getStateReligionCount() >= 0);

		// religion visibility now part of espionage
		//GC.getGameINLINE().updateCitySight(true);

		updateMaintenance();
		updateReligionHappiness();
		updateReligionCommerce();

		GC.getGameINLINE().AI_makeAssignWorkDirty();

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


int CvPlayer::getNoNonStateReligionSpreadCount() const
{
	return m_iNoNonStateReligionSpreadCount;
}


bool CvPlayer::isNoNonStateReligionSpread() const
{
	return (getNoNonStateReligionSpreadCount() > 0);
}


void CvPlayer::changeNoNonStateReligionSpreadCount(int iChange)
{
	m_iNoNonStateReligionSpreadCount = (m_iNoNonStateReligionSpreadCount + iChange);
	FAssert(getNoNonStateReligionSpreadCount() >= 0);
}

/************************************************************************************************/
/* Advanced Diplomacy          START                                                          */
/************************************************************************************************/
int CvPlayer::getActiveSenateCount() const
{
	return m_iActiveSenateCount;
}


bool CvPlayer::isActiveSenate() const
{
	return (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS) && getActiveSenateCount() > 0);
}


void CvPlayer::changeActiveSenateCount(int iChange)
{
	if (iChange != 0)
	{
		m_iActiveSenateCount += iChange;
		FAssert(getActiveSenateCount() >= 0);

		GET_TEAM(getTeam()).changeActiveSenateCount(GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS) ? iChange : 0);
	}
}
/************************************************************************************************/
/* Advanced Diplomacy          END                                                            */
/************************************************************************************************/


int CvPlayer::getStateReligionHappiness() const
{
	return m_iStateReligionHappiness;
}


void CvPlayer::changeStateReligionHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iStateReligionHappiness = (m_iStateReligionHappiness + iChange);

		updateReligionHappiness();
	}
}


int CvPlayer::getNonStateReligionHappiness() const
{
	return m_iNonStateReligionHappiness;
}


void CvPlayer::changeNonStateReligionHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iNonStateReligionHappiness = (m_iNonStateReligionHappiness + iChange);

		updateReligionHappiness();
	}
}


int CvPlayer::getStateReligionUnitProductionModifier() const
{
	return m_iStateReligionUnitProductionModifier;
}


void CvPlayer::changeStateReligionUnitProductionModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStateReligionUnitProductionModifier = (m_iStateReligionUnitProductionModifier + iChange);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getStateReligionBuildingProductionModifier() const
{
	return m_iStateReligionBuildingProductionModifier;
}


void CvPlayer::changeStateReligionBuildingProductionModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStateReligionBuildingProductionModifier = (m_iStateReligionBuildingProductionModifier + iChange);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getStateReligionFreeExperience() const
{
	return m_iStateReligionFreeExperience;
}


void CvPlayer::changeStateReligionFreeExperience(int iChange)
{
	m_iStateReligionFreeExperience = (m_iStateReligionFreeExperience + iChange);
}


CvCity* CvPlayer::getCapitalCity() const
{
	return getCity(m_iCapitalCityID);
}


void CvPlayer::setCapitalCity(CvCity* pNewCapitalCity)
{
	CvCity* pOldCapitalCity;
	bool bUpdatePlotGroups;

	pOldCapitalCity = getCapitalCity();

	if (pOldCapitalCity != pNewCapitalCity)
	{
		bUpdatePlotGroups = ((pOldCapitalCity == NULL) || (pNewCapitalCity == NULL) || (pOldCapitalCity->plot()->getOwnerPlotGroup() != pNewCapitalCity->plot()->getOwnerPlotGroup()));

		if (bUpdatePlotGroups)
		{
			if (pOldCapitalCity != NULL)
			{
				pOldCapitalCity->plot()->updatePlotGroupBonus(false);
			}
			if (pNewCapitalCity != NULL)
			{
				pNewCapitalCity->plot()->updatePlotGroupBonus(false);
			}
		}

		if (pNewCapitalCity != NULL)
		{
			m_iCapitalCityID = pNewCapitalCity->getID();
		}
		else
		{
			m_iCapitalCityID = FFreeList::INVALID_INDEX;
		}

		if (bUpdatePlotGroups)
		{
			if (pOldCapitalCity != NULL)
			{
				pOldCapitalCity->plot()->updatePlotGroupBonus(true);
			}
			if (pNewCapitalCity != NULL)
			{
				pNewCapitalCity->plot()->updatePlotGroupBonus(true);
			}
		}

		updateMaintenance();
		updateTradeRoutes();

		if (pOldCapitalCity != NULL)
		{
			pOldCapitalCity->updateCommerce();

			pOldCapitalCity->setInfoDirty(true);
		}
		if (pNewCapitalCity != NULL)
		{
			pNewCapitalCity->updateCommerce();

			pNewCapitalCity->setInfoDirty(true);
		}
	}
}


int CvPlayer::getCitiesLost() const
{
	return m_iCitiesLost;
}


void CvPlayer::changeCitiesLost(int iChange)
{
	m_iCitiesLost = (m_iCitiesLost + iChange);
}


int CvPlayer::getWinsVsBarbs() const
{
	return m_iWinsVsBarbs;
}


void CvPlayer::changeWinsVsBarbs(int iChange)
{
	m_iWinsVsBarbs = (m_iWinsVsBarbs + iChange);
	FAssert(getWinsVsBarbs() >= 0);
}


int CvPlayer::getAssets() const
{
	return m_iAssets;
}


void CvPlayer::changeAssets(int iChange)
{
	m_iAssets = (m_iAssets + iChange);
	FAssert(getAssets() >= 0);
}


/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
int CvPlayer::getPower() const
{
	return m_iPower + m_iTechPower;
}


int CvPlayer::getTechPower() const
{
	return m_iTechPower;
}


bool CvPlayer::isSenateWarOpposition(TeamTypes eAgainstTeam) const
{
	return GET_TEAM(getTeam()).isSenateWarOpposition(eAgainstTeam);
}


void CvPlayer::changeTechPower(int iChange)
{
	m_iTechPower = (m_iTechPower + iChange);
	FAssert(getTechPower() >= 0);
}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/


void CvPlayer::changePower(int iChange)
{
	m_iPower = (m_iPower + iChange);
	FAssert(getPower() >= 0);
}


int CvPlayer::getPopScore(bool bCheckVassal) const
{
	if (bCheckVassal && GET_TEAM(getTeam()).isAVassal())
	{
		return m_iPopulationScore / 2;
	}

	int iVassalScore = 0;

	if (bCheckVassal)
	{
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (i != getID())
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
				if (kLoopPlayer.isAlive() && GET_TEAM(kLoopPlayer.getTeam()).isVassal(getTeam()))
				{
					iVassalScore += kLoopPlayer.getPopScore(false) / 2;
				}
			}
		}
	}

	return (m_iPopulationScore + iVassalScore / std::max(1, GET_TEAM(getTeam()).getNumMembers()));
}

void CvPlayer::changePopScore(int iChange)
{
	if (iChange != 0)
	{
		m_iPopulationScore += iChange;
		FAssert(getPopScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}


int CvPlayer::getLandScore(bool bCheckVassal) const
{
	if (bCheckVassal && GET_TEAM(getTeam()).isAVassal())
	{
		return m_iLandScore / 2;
	}

	int iVassalScore = 0;

	if (bCheckVassal)
	{
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (i != getID())
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
				if (kLoopPlayer.isAlive() && GET_TEAM(kLoopPlayer.getTeam()).isVassal(getTeam()))
				{
					iVassalScore += kLoopPlayer.getLandScore(false) / 2;
				}
			}
		}
	}

	return (m_iLandScore + iVassalScore  / std::max(1, GET_TEAM(getTeam()).getNumMembers()));
}


void CvPlayer::changeLandScore(int iChange)
{
	if (iChange != 0)
	{
		m_iLandScore += iChange;
		FAssert(getLandScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}


int CvPlayer::getWondersScore() const
{
	return m_iWondersScore;
}


void CvPlayer::changeWondersScore(int iChange)
{
	if (iChange != 0)
	{
		m_iWondersScore += iChange;
		FAssert(getWondersScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}


int CvPlayer::getTechScore() const
{
	return m_iTechScore;
}


void CvPlayer::changeTechScore(int iChange)
{
	if (iChange != 0)
	{
		m_iTechScore += iChange;
		FAssert(getTechScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}

int CvPlayer::getCombatExperience() const
{
	return m_iCombatExperience;
}

void CvPlayer::setCombatExperience(int iExperience)
{
	FAssert(iExperience >= 0);

	if (iExperience != getCombatExperience())
	{
		m_iCombatExperience = iExperience;

		if (!isBarbarian())
		{
			int iExperienceThreshold = greatPeopleThreshold(true);
			if (m_iCombatExperience >= iExperienceThreshold && iExperienceThreshold > 0)
			{
				// create great person
				CvCity* pBestCity = NULL;
				int iBestValue = MAX_INT;
				int iLoop;
				for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
				{
					int iValue = 4 * GC.getGameINLINE().getSorenRandNum(getNumCities(), "Warlord City Selection");

					for (int i = 0; i < NUM_YIELD_TYPES; i++)
					{
						iValue += pLoopCity->findYieldRateRank((YieldTypes)i);
					}
					iValue += pLoopCity->findPopulationRank();

					if (iValue < iBestValue)
					{
						pBestCity = pLoopCity;
						iBestValue = iValue;
					}
				}

				if (pBestCity)
				{
// edead: start unit class fix for Great Generals
					int iI;
					for (iI = 0; iI < GC.getNumUnitInfos(); iI++)
					{
						if (GC.getUnitInfo((UnitTypes)iI).getLeaderExperience() > 0 || GC.getUnitInfo((UnitTypes)iI).getLeaderPromotion() != NO_PROMOTION)
						{
							break;
						}
					}
					UnitTypes eGreatGeneralType = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits((UnitClassTypes)(GC.getUnitInfo((UnitTypes)iI).getUnitClassType()))));
					pBestCity->createGreatPeople(eGreatGeneralType, false, true);
					setCombatExperience(getCombatExperience() - iExperienceThreshold);
					/* Leoreth: original code, replaced by edead's adjustment to achieve unique GGs
					int iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumUnitInfos(), "Warlord Unit Generation");
					for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
					{
						UnitTypes eLoopUnit = (UnitTypes)((iI + iRandOffset) % GC.getNumUnitInfos());
						if (GC.getUnitInfo(eLoopUnit).getLeaderExperience() > 0 || GC.getUnitInfo(eLoopUnit).getLeaderPromotion() != NO_PROMOTION)
						{
							pBestCity->createGreatPeople(eLoopUnit, false, true);
							setCombatExperience(getCombatExperience() - iExperienceThreshold);
							break;
						}
					}*/
				}
			}
		}
	}
}

void CvPlayer::changeCombatExperience(int iChange)
{
	setCombatExperience(getCombatExperience() + iChange);
}


bool CvPlayer::isConnected() const
{
	return gDLL->isConnected( getNetID() );
}

int CvPlayer::getNetID() const
{
	return GC.getInitCore().getNetID(getID());
}


void CvPlayer::setNetID(int iNetID)
{
	GC.getInitCore().setNetID(getID(), iNetID);
}

void CvPlayer::sendReminder()
{
	CvWString szYearStr;

	// Only perform this step if we have a valid email address on record,
	// and we have provided information about how to send emails
	if ( !getPbemEmailAddress().empty() &&
		!gDLL->GetPitbossSmtpHost().empty() )
	{
		GAMETEXT.setTimeStr(szYearStr, GC.getGameINLINE().getGameTurn(), true);

		// Generate our arguments
		CyArgsList argsList;
		argsList.add(getPbemEmailAddress());
		argsList.add(gDLL->GetPitbossSmtpHost());
		argsList.add(gDLL->GetPitbossSmtpLogin());
		argsList.add(gDLL->GetPitbossSmtpPassword());
		argsList.add(GC.getGameINLINE().getName());
		argsList.add(GC.getGameINLINE().isMPOption(MPOPTION_TURN_TIMER));
		argsList.add(GC.getGameINLINE().getPitbossTurnTime());
		argsList.add(gDLL->GetPitbossEmail());
		argsList.add(szYearStr);

		// Now send our email via Python
		long iResult;
		bool bOK = gDLL->getPythonIFace()->callFunction(PYPitBossModule, "sendEmail", argsList.makeFunctionArgs(), &iResult);

		FAssertMsg( bOK, "Pitboss Python call to onSendEmail failed!" );
		FAssertMsg( iResult == 0, "Pitboss Python fn onSendEmail encountered an error" );
	}
}

uint CvPlayer::getStartTime() const
{
	return m_uiStartTime;
}


void CvPlayer::setStartTime(uint uiStartTime)
{
	m_uiStartTime = uiStartTime;
}


uint CvPlayer::getTotalTimePlayed() const
{
	return ((timeGetTime() - m_uiStartTime)/1000);
}


bool CvPlayer::isMinorCiv() const
{
	return GC.getInitCore().getMinorNationCiv(m_eID);
}


bool CvPlayer::isAlive() const
{
	return m_bAlive;
}


bool CvPlayer::isEverAlive() const
{
	return m_bEverAlive;
}


void CvPlayer::setAlive(bool bNewValue)
{
	CvWString szBuffer;
	int iI;

	if (isAlive() != bNewValue)
	{
		m_bAlive = bNewValue;

		GET_TEAM(getTeam()).changeAliveCount((isAlive()) ? 1 : -1);

		// Report event to Python
		CvEventReporter::getInstance().setPlayerAlive(getID(), bNewValue);

		if (isAlive())
		{
			logBBAI( "Player %d (%S - %S) becomes alive on turn %d.", getIDINLINE(), getName(),
				getCivilizationShortDescription(), GC.getGameINLINE().getGameTurn() );

			if (!isEverAlive())
			{
				m_bEverAlive = true;

				GET_TEAM(getTeam()).changeEverAliveCount(1);
			}

			if (getNumCities() == 0)
			{
				setFoundedFirstCity(false);
			}

			updatePlotGroups();

			if (GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || (GC.getGameINLINE().getNumGameTurnActive() == 0) || (GC.getGameINLINE().isSimultaneousTeamTurns() && GET_TEAM(getTeam()).isTurnActive()))
			{
				setTurnActive(true);
			}

			gDLL->openSlot(getID());

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
			// From Sanguo Mod Performance, ie the CAR Mod
			// Attitude cache
			for( int iI = 0; iI < MAX_PLAYERS; iI++ )
			{
				GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
				GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		}
		else
		{
			logBBAI( "Player %d (%S - %S) eliminated on turn %d.", getIDINLINE(), getName(),
				getCivilizationShortDescription(), GC.getGameINLINE().getGameTurn() );

			clearResearchQueue();
			killUnits();
			killCities();
			killAllDeals();

			setTurnActive(false);

			gDLL->endMPDiplomacy();
			gDLL->endDiplomacy();

			if (!isHuman())
			{
				gDLL->closeSlot(getID());
			}

			if (GC.getGameINLINE().getElapsedGameTurns() > 0)
			{
				if (!isBarbarian())// && !isRebel())
				{
					//szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_DESTROYED", getCivilizationAdjectiveKey());
					szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_DESTROYED", getCivilizationDescription());

					for (iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CIVDESTROYED", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
						}
					}
					GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
				}
			}
		}

		GC.getGameINLINE().setScoreDirty(true);
	}
}

/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// It appears that setAlive causes the new player's turn to fire out of turn (if it's not someone else's turn).
// This function is a copy of setAlive with that feature turned off.
void CvPlayer::setNewPlayerAlive(bool bNewValue)
{
	CvWString szBuffer;
	int iI;

	if (isAlive() != bNewValue)
	{
		m_bAlive = bNewValue;

		GET_TEAM(getTeam()).changeAliveCount((isAlive()) ? 1 : -1);

		// Report event to Python
		CvEventReporter::getInstance().setPlayerAlive(getID(), bNewValue);

		if (isAlive())
		{
			if (!isEverAlive())
			{
				m_bEverAlive = true;

				GET_TEAM(getTeam()).changeEverAliveCount(1);
			}

			if (getNumCities() == 0)
			{
				setFoundedFirstCity(false);
			}

			updatePlotGroups();

			// Turned off turn fire on next line
			/*
			if (GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS)) || (GC.getGameINLINE().getNumGameTurnActive() == 0) || (GC.getGameINLINE().isSimultaneousTeamTurns() && GET_TEAM(getTeam()).isTurnActive()))
			{
				setTurnActive(true);
			}
			*/
			gDLL->openSlot(getID());
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
			// From Sanguo Mod Performance, ie the CAR Mod
			// Attitude cache
			for( int iI = 0; iI < MAX_PLAYERS; iI++ )
			{
				GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
				GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		}
		else
		{
			clearResearchQueue();
			killUnits();
			killCities();
			killAllDeals();

			setTurnActive(false);

			gDLL->endMPDiplomacy();
			gDLL->endDiplomacy();

			if (!isHuman())
			{
				gDLL->closeSlot(getID());
			}

			if (GC.getGameINLINE().getElapsedGameTurns() > 0)
			{
				if (!isBarbarian())
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_DESTROYED", getCivilizationAdjectiveKey());

					for (iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CIVDESTROYED", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
						}
					}

					GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
				}
			}
		}

		GC.getGameINLINE().setScoreDirty(true);
	}
}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

void CvPlayer::verifyAlive()
{
	bool bKill;

	if (isAlive())
	{
		bKill = false;

		if (!bKill)
		{
			if (!isBarbarian())
			{
				if (getNumCities() == 0 && getAdvancedStartPoints() < 0)
				{
/************************************************************************************************/
/* REVOLUTION_MOD                         02/07/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/* original code
					if ((getNumUnits() == 0) || (!(GC.getGameINLINE().isOption(GAMEOPTION_COMPLETE_KILLS)) && isFoundedFirstCity()))
*/
					// Keep a rebel player alive until they lose all units
					if ((getNumUnits() == 0) || (!(GC.getGameINLINE().isOption(GAMEOPTION_COMPLETE_KILLS)) && isFoundedFirstCity() && !(isRebel())))
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
					{
						bKill = true;
					}
				}
			}
		}

		if (!bKill)
		{
			if (!isBarbarian())
			{
				if (GC.getGameINLINE().getMaxCityElimination() > 0)
				{
					if (getCitiesLost() >= GC.getGameINLINE().getMaxCityElimination())
					{
						bKill = true;
					}
				}
			}
		}

		if (bKill)
		{
			setAlive(false);
/************************************************************************************************/
/* REVOLUTION_MOD                                                                 lemmy101      */
/*                                                                                jdog5000      */
/*                                                                                              */
/************************************************************************************************/
// Choose a random AI to take over if we die when on autoplay. (Testing)
			if(isHumanDisabled())
			{
				std::vector<int> Potentials;
				for(int x=0;x<MAX_PLAYERS;x++)
				{
					if(GET_PLAYER((PlayerTypes)x).isAlive() && 
						!GET_PLAYER((PlayerTypes)x).isHumanDisabled() && 
						!GET_PLAYER((PlayerTypes)x).isHuman() &&
						GET_PLAYER((PlayerTypes)x).getNumCities() > 0)
					{
						Potentials.push_back(x);
					}
				}

				if(Potentials.size()==0)
				{
					if(GET_PLAYER((PlayerTypes)x).isAlive() && 
						!GET_PLAYER((PlayerTypes)x).isHumanDisabled() && 
						!GET_PLAYER((PlayerTypes)x).isHuman())
					{
						Potentials.push_back(x);
					}

				}

				int choose = GC.getGame().getSorenRand().get(Potentials.size(), "Picking new player for dead player...");

				GC.getGame().changeHumanPlayer((PlayerTypes)getID(), (PlayerTypes)choose);
			}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
		}
	}
	else
	{
		if ((getNumCities() > 0) || (getNumUnits() > 0))
		{
			setAlive(true);
		}
	}
}


bool CvPlayer::isTurnActive() const
{
	return m_bTurnActive;
}

void CvPlayer::setTurnActiveForPbem(bool bActive)
{
	FAssertMsg(GC.getGameINLINE().isPbem(), "You are using setTurnActiveForPbem. Are you sure you know what you're doing?");

	// does nothing more than to set the member variable before saving the game
	// the rest of the turn will be performed upon loading the game
	// This allows the player to browse the game in paused mode after he has generated the save
	if (isTurnActive() != bActive)
	{
		m_bTurnActive = bActive;
		GC.getGameINLINE().changeNumGameTurnActive(isTurnActive() ? 1 : -1);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
		// Plot danger cache
		//if( GC.getGameINLINE().getNumGameTurnActive() != 1 )
		{
			GC.getMapINLINE().invalidateIsActivePlayerNoDangerCache();
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	}
}


void CvPlayer::setTurnActive(bool bNewValue, bool bDoTurn)
{// LOL: consume long-time
	PROFILE_FUNC()
	int iI;
	if (isTurnActive() != bNewValue)
	{
		m_bTurnActive = bNewValue;

		if (isTurnActive())
		{
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/26/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
			if( gPlayerLogLevel > 0 ) 
			{
				logBBAI("\n\n Player %d (%S) setTurnActive for turn %d", getID(), getCivilizationDescription(0), GC.getGameINLINE().getGameTurn() );
			
				if( GC.getGameINLINE().getGameTurn() > 0 && (GC.getGameINLINE().getGameTurn() % 25) == 0 && !isBarbarian() )
				{
					CvWStringBuffer szBuffer;
					GAMETEXT.setScoreHelp(szBuffer, getID());
					logBBAI("%S", szBuffer);

					int iGameTurn = GC.getGameINLINE().getGameTurn();
					logBBAI("  Total Score: %d, Population Score: %d (%d total pop), Land Score: %d, Tech Score: %d, Wonder Score: %d", calculateScore(), getPopScore(false), getTotalPopulation(), getLandScore(false), getTechScore(), getWondersScore());
					
					int iEconomy = 0;
					int iProduction = 0;
					int iAgri = 0;
					int iCount = 0;
					for( int iI = 1; iI <= 5; iI++ )
					{
						if( iGameTurn - iI >= 0 )
						{
							iEconomy += getEconomyHistory(iGameTurn - iI);
							iProduction += getIndustryHistory(iGameTurn - iI);
							iAgri += getAgricultureHistory(iGameTurn - iI);
							iCount++;
						}
					}
					iEconomy /= std::max(1, iCount);
					iProduction /= std::max(1, iCount);
					iAgri /= std::max(1, iCount);

					logBBAI("  Economy avg: %d,  Industry avg: %d,  Agriculture avg: %d", iEconomy, iProduction, iAgri);
				}
			}
				
			if( gPlayerLogLevel >= 2 )
			{
				CvWStringBuffer szBuffer;

				logBBAI("  Player %d (%S) has %d cities, %d pop, %d power, %d tech percent", getID(), getCivilizationDescription(0), getNumCities(), getTotalPopulation(), getPower(), GET_TEAM(getTeam()).getBestKnownTechScorePercent());

				if( GET_PLAYER(getID()).AI_isFinancialTrouble() )
				{
					logBBAI("    Financial trouble!");
				}

				szBuffer.append(CvWString::format(L"    Team %d has met: ", getTeam()));

				for( int iI = 0; iI < MAX_CIV_TEAMS; iI++ )
				{
					if( iI != getTeam() && GET_TEAM(getTeam()).isHasMet((TeamTypes)iI) )
					{
						if( GET_TEAM((TeamTypes)iI).isAlive() )
						{
							szBuffer.append(CvWString::format(L"%d,", iI));
						}
					}
				}

				if( GET_TEAM(getTeam()).getVassalCount() > 0 )
				{
					szBuffer.append(L";  vassals: ");

					for( int iI = 0; iI < MAX_CIV_TEAMS; iI++ )
					{
						if( iI != getTeam() && GET_TEAM((TeamTypes)iI).isVassal(getTeam()) )
						{
							if( GET_TEAM((TeamTypes)iI).isAlive() )
							{
								szBuffer.append(CvWString::format(L"%d,", iI));
							}
						}
					}
				}

				if( GET_TEAM(getTeam()).getAtWarCount(false) > 0 )
				{
					szBuffer.append(L";  at war with: ");

					for( int iI = 0; iI < MAX_CIV_TEAMS; iI++ )
					{
						if( iI != getTeam() && GET_TEAM(getTeam()).isAtWar((TeamTypes)iI) )
						{
							if( GET_TEAM((TeamTypes)iI).isAlive() )
							{
								szBuffer.append(CvWString::format(L"%d,", iI));
							}
						}
					}
				}

				if( GET_TEAM(getTeam()).getAnyWarPlanCount(true) > 0 )
				{
					szBuffer.append(L";  planning war with: ");

					for( int iI = 0; iI < MAX_CIV_TEAMS; iI++ )
					{
						if( iI != getTeam() && !GET_TEAM(getTeam()).isAtWar((TeamTypes)iI) && GET_TEAM(getTeam()).AI_getWarPlan((TeamTypes)iI) != NO_WARPLAN )
						{
							if( GET_TEAM((TeamTypes)iI).isAlive() )
							{
								szBuffer.append(CvWString::format(L"%d,", iI));
							}
						}
					}
				}
				
				logBBAI("%S", szBuffer.getCString());

				szBuffer.clear();

				if( GET_TEAM(getTeam()).getAnyWarPlanCount(true) > 0 ) logBBAI("    Enemy power perc: %d (%d with others reduction)", GET_TEAM(getTeam()).AI_getEnemyPowerPercent(), GET_TEAM(getTeam()).AI_getEnemyPowerPercent(true));
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

			FAssertMsg(isAlive(), "isAlive is expected to be true");

			setEndTurn(false);
			GC.getGameINLINE().resetTurnTimer();

			// If we are the Pitboss, send this player an email
			if ( gDLL->IsPitbossHost() )
			{
				// If this guy is not currently connected, try sending him an email
				if ( isHuman() && !isConnected() )
				{
					sendReminder();
				}
			}

			if ((GC.getGameINLINE().isHotSeat() || GC.getGameINLINE().isPbem()) && isHuman() && bDoTurn)
			{
				gDLL->getInterfaceIFace()->clearEventMessages();
				gDLL->getEngineIFace()->setResourceLayer(false);

				GC.getGameINLINE().setActivePlayer(getID());
			}

			GC.getGameINLINE().changeNumGameTurnActive(1);

			if (bDoTurn)
			{
				if (isAlive() && !isHuman() && !isBarbarian() && (getAdvancedStartPoints() >= 0))
				{
					AI_doAdvancedStart();
				}

				if (GC.getGameINLINE().getElapsedGameTurns() > 0)
				{
					if (isAlive())
					{
						if (GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
						{
							doTurn();
						}

						doTurnUnits();
					}
				}

				if ((getID() == GC.getGameINLINE().getActivePlayer()) && (GC.getGameINLINE().getElapsedGameTurns() > 0))
				{
					if (GC.getGameINLINE().isNetworkMultiPlayer())
					{
						gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_TURN_BEGINS").GetCString(), "AS2D_NEWTURN", MESSAGE_TYPE_DISPLAY_ONLY);
					}
					else
					{
						gDLL->getInterfaceIFace()->playGeneralSound("AS2D_NEWTURN");
					}
				}

				doWarnings();
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				if (gDLL->getInterfaceIFace()->getLengthSelectionList() == 0)
				{
					gDLL->getInterfaceIFace()->setCycleSelectionCounter(1);
				}

				gDLL->getInterfaceIFace()->setDirty(SelectionCamera_DIRTY_BIT, true);
			}
		}
		else
		{
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setForcePopup(false);
				gDLL->getInterfaceIFace()->clearQueuedPopups();
				gDLL->getInterfaceIFace()->flushTalkingHeadMessages();
			}

			// start profiling DLL if desired
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				startProfilingDLL();
			}

			GC.getGameINLINE().changeNumGameTurnActive(-1);

			if (bDoTurn)
			{
				if (!GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
				{
					if (isAlive())
					{
						doTurn();
					}

					if ((GC.getGameINLINE().isPbem() || GC.getGameINLINE().isHotSeat()) && isHuman() && GC.getGameINLINE().countHumanPlayersAlive() > 1)
					{
						GC.getGameINLINE().setHotPbemBetweenTurns(true);
					}

					if (GC.getGameINLINE().isSimultaneousTeamTurns())
					{
						if (!GET_TEAM(getTeam()).isTurnActive())
						{
							for (iI = (getTeam() + 1); iI < MAX_TEAMS; iI++)
							{
								if (GET_TEAM((TeamTypes)iI).isAlive())
								{
									GET_TEAM((TeamTypes)iI).setTurnActive(true);
									break;
								}
							}
						}
					}
					else
					{
						for (iI = (getID() + 1); iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (GC.getGameINLINE().isPbem() && GET_PLAYER((PlayerTypes)iI).isHuman())
								{
									if (!GC.getGameINLINE().getPbemTurnSent())
									{
										gDLL->sendPbemTurn((PlayerTypes)iI);
									}
								}
								else
								{
									GET_PLAYER((PlayerTypes)iI).setTurnActive(true);
								}
								break;
							}
						}
					}
				}
			}
		}

		gDLL->getInterfaceIFace()->updateCursorType();

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
		// Plot danger cache
		//if( GC.getGameINLINE().getNumGameTurnActive() != 1 )
		{
			GC.getMapINLINE().invalidateIsActivePlayerNoDangerCache();
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	}
}


bool CvPlayer::isAutoMoves() const																			
{
	return m_bAutoMoves;
}


void CvPlayer::setAutoMoves(bool bNewValue)
{
	if (isAutoMoves() != bNewValue)
	{
		m_bAutoMoves = bNewValue;

		if (!isAutoMoves())
		{
			if (isEndTurn() || !isHuman())
			{
				setTurnActive(false);
			}
			else
			{
				if (getID() == GC.getGameINLINE().getActivePlayer())
				{
					gDLL->getInterfaceIFace()->setCycleSelectionCounter(1);
				}
			}
		}
	}
}


bool CvPlayer::isEndTurn() const
{
	return m_bEndTurn;
}


void CvPlayer::setEndTurn(bool bNewValue)
{
	if (isEndTurn() != bNewValue)
	{
		FAssertMsg(isTurnActive(), "isTurnActive is expected to be true");

		m_bEndTurn = bNewValue;

		if (isEndTurn())
		{
			setAutoMoves(true);
		}
	}
}

bool CvPlayer::isTurnDone() const
{
	// if this returns true, popups and diplomacy will wait to appear until next turn
	if (!GC.getGameINLINE().isPbem() && !GC.getGameINLINE().isHotSeat())
	{
		return false;
	}
	if (!isHuman() )
	{
		return true;
	}
	if (!isEndTurn())
	{
		return false;
	}
	return (!isAutoMoves());
}

bool CvPlayer::isExtendedGame() const
{
	return m_bExtendedGame;
}


void CvPlayer::makeExtendedGame()
{
	m_bExtendedGame = true;
}


bool CvPlayer::isFoundedFirstCity() const
{
	return m_bFoundedFirstCity;
}


void CvPlayer::setFoundedFirstCity(bool bNewValue)
{
	if (isFoundedFirstCity() != bNewValue)
	{
		m_bFoundedFirstCity = bNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(PercentButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		}
	}
}


bool CvPlayer::isStrike() const
{
	return m_bStrike;
}


void CvPlayer::setStrike(bool bNewValue)
{
	if (isStrike() != bNewValue)
	{
		m_bStrike = bNewValue;

		if (isStrike())
		{
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_UNITS_ON_STRIKE").GetCString(), "AS2D_STRIKE", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));

				gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
			}
		}
	}
}

PlayerTypes CvPlayer::getID() const
{
	return m_eID;
}


HandicapTypes CvPlayer::getHandicapType() const
{
	return GC.getInitCore().getHandicap(getID());
}


CivilizationTypes CvPlayer::getCivilizationType() const
{
	return GC.getInitCore().getCiv(getID());
}


LeaderHeadTypes CvPlayer::getLeaderType() const
{
	return GC.getInitCore().getLeader(getID());
}


LeaderHeadTypes CvPlayer::getPersonalityType() const
{
	return m_ePersonalityType;
}


void CvPlayer::setPersonalityType(LeaderHeadTypes eNewValue)
{
	m_ePersonalityType = eNewValue;
}


EraTypes CvPlayer::getCurrentEra() const
{
	return m_eCurrentEra;
}


// ERA_FIX 09/2017 lfgr
EraTypes CvPlayer::getCurrentRealEra() const
{
	return m_eCurrentRealEra;
}
// ERA_FIX end



void CvPlayer::setCurrentEra(EraTypes eNewValue)
{
	CvCity* pLoopCity;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	int iLoop;
	int iI;

	if (getCurrentEra() != eNewValue)
	{
		EraTypes eOldEra = m_eCurrentEra;
		m_eCurrentEra = eNewValue;

		if (GC.getGameINLINE().getActiveTeam() != NO_TEAM)
		{
			for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
			{
				pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
				pLoopPlot->updateGraphicEra();

				if (pLoopPlot->getRevealedImprovementType(GC.getGameINLINE().getActiveTeam(), true) != NO_IMPROVEMENT)
				{
					if ((pLoopPlot->getOwnerINLINE() == getID()) || (!(pLoopPlot->isOwned()) && (getID() == GC.getGameINLINE().getActivePlayer())))
					{
						pLoopPlot->setLayoutDirty(true);
					}
				}
			}
		}

		// dirty all of this player's cities...
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getOwnerINLINE() == getID())
			{
				pLoopCity->setLayoutDirty(true);
			}
		}

		//update unit eras
		for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			gDLL->getEntityIFace()->updateGraphicEra(pLoopUnit->getUnitEntity(), eOldEra);
		}

		//update flag eras
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Soundtrack_DIRTY_BIT, true);
		}

		if (isHuman() && (getCurrentRealEra() != GC.getGameINLINE().getStartEra()) && !GC.getGameINLINE().isNetworkMultiPlayer())
		{
			if (GC.getGameINLINE().isFinalInitialized() && !(gDLL->GetWorldBuilderMode()))
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
				if (NULL != pInfo)
				{
					pInfo->setData1(eNewValue);
					pInfo->setText(L"showEraMovie");
					addPopup(pInfo);
				}
			}
		}
	}
}

// ERA_FIX 09/2017 lfgr
void CvPlayer::setCurrentRealEra( EraTypes eNewValue )
{
	FAssertMsg( eNewValue == NO_ERA || GC.getEraInfo( eNewValue ).isRealEra(),
		"Can't set current real era to a non-real era! These have to declared as \
		PseudoEra of a religion to work properly." );

	m_eCurrentRealEra = eNewValue;
	updateCurrentEra();
}

void CvPlayer::updateCurrentEra()
{
	EraTypes eNewEra = NO_ERA;
	
	// Pseudo era takes precendence
	if( getStateReligion() != NO_RELIGION )
	{
		// Note: eNewEra remains NO_ERA if religion has no pseudo era.
		eNewEra = GC.getReligionInfo( getStateReligion() ).getPseudoEra();
	}

	// If no pseudo era was found, use the real era
	if( eNewEra == NO_ERA )
		eNewEra = getCurrentRealEra();

	setCurrentEra( eNewEra );
}
// ERA_FIX end


ReligionTypes CvPlayer::getLastStateReligion() const
{
	return m_eLastStateReligion;
}


ReligionTypes CvPlayer::getStateReligion() const
{
	return ((isStateReligion()) ? getLastStateReligion() : NO_RELIGION);
}


void CvPlayer::setLastStateReligion(ReligionTypes eNewValue)
{
	ReligionTypes eOldReligion;
	CvWString szBuffer;
	int iI;

	if (getLastStateReligion() != eNewValue)
	{
		// religion visibility now part of espionage
		//GC.getGameINLINE().updateCitySight(false, true);

//FfH: Added by Kael 11/03/2007
		GC.getGameINLINE().updateCitySight(false);
//FfH: End Add

		eOldReligion = getLastStateReligion();
		m_eLastStateReligion = eNewValue;

		// religion visibility now part of espionage
		//GC.getGameINLINE().updateCitySight(true, true);

//FfH: Added by Kael 11/03/2007
		GC.getGameINLINE().updateCitySight(true);
//FfH: End Add

		updateMaintenance();
		updateReligionHappiness();
		updateReligionCommerce();

		GC.getGameINLINE().updateSecretaryGeneral();

		GC.getGameINLINE().AI_makeAssignWorkDirty();

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

	// ERA_FIX 09/2017 lfgr
	// In case the previous or new religion triggers an era change
		updateCurrentEra();
	// ERA_FIX end

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if (gDLL->isDiplomacy() && (gDLL->getDiplomacyPlayer() == getID()))
			{
				gDLL->updateDiplomacyAttitude(true);
			}

/************************************************************************************************/
/* REVOLUTION_MOD                         01/01/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/* original code
			if (!isBarbarian())
*/
			// Silence announcement for civs who are not alive, ie rebels who may not be born
			if (!isBarbarian() && isAlive())
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
			{
				if (getLastStateReligion() != NO_RELIGION)
				{
					if (!GC.getReligionInfo((ReligionTypes)getLastStateReligion()).isHidden()) // suppress messages to other players for hidden religions
					{
						for (iI = 0; iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()))
								{
									szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_CONVERT_RELIGION", getNameKey(), GC.getReligionInfo(getLastStateReligion()).getTextKeyWide());
									gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_RELIGION_CONVERT", MESSAGE_TYPE_MAJOR_EVENT);
								}
							}
						}
					}

					szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_CONVERT_RELIGION", getNameKey(), GC.getReligionInfo(getLastStateReligion()).getTextKeyWide());
					GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer);
				}
			}

			// Python Event
			CvEventReporter::getInstance().playerChangeStateReligion(getID(), eNewValue, eOldReligion);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
			// From Sanguo Mod Performance, ie the CAR Mod
			// Attitude cache
			for (int iI = 0; iI < GC.getMAX_PLAYERS(); iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getStateReligion() != NO_RELIGION)
				{
					GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
					GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
				}
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		}
	}
}

PlayerTypes CvPlayer::getParent() const
{
	return m_eParent;
}

void CvPlayer::setParent(PlayerTypes eParent)
{
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// From Sanguo Mod Performance, ie the CAR Mod
	// Attitude cache
	if (m_eParent != eParent)
	{
		GET_PLAYER(getID()).AI_invalidateAttitudeCache(eParent);
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	m_eParent = eParent;
}

TeamTypes CvPlayer::getTeam() const
{
	return m_eTeamType;
}

void CvPlayer::updateTeamType()
{
	if(getID() == NO_PLAYER)
	{
		m_eTeamType = NO_TEAM;
	}
	else
	{
		m_eTeamType = GC.getInitCore().getTeam(getID());
	}
}

void CvPlayer::setTeam(TeamTypes eTeam)
{
	FAssert(eTeam != NO_TEAM);
	FAssert(getTeam() != NO_TEAM);

	GET_TEAM(getTeam()).changeNumMembers(-1);
	if (isAlive())
	{
		GET_TEAM(getTeam()).changeAliveCount(-1);
	}
	if (isEverAlive())
	{
		GET_TEAM(getTeam()).changeEverAliveCount(-1);
	}
	GET_TEAM(getTeam()).changeNumCities(-(getNumCities()));
	GET_TEAM(getTeam()).changeTotalPopulation(-(getTotalPopulation()));
	GET_TEAM(getTeam()).changeTotalLand(-(getTotalLand()));

	GC.getInitCore().setTeam(getID(), eTeam);

	GET_TEAM(getTeam()).changeNumMembers(1);
	if (isAlive())
	{
		GET_TEAM(getTeam()).changeAliveCount(1);
	}
	if (isEverAlive())
	{
		GET_TEAM(getTeam()).changeEverAliveCount(1);
	}
	GET_TEAM(getTeam()).changeNumCities(getNumCities());
	GET_TEAM(getTeam()).changeTotalPopulation(getTotalPopulation());
	GET_TEAM(getTeam()).changeTotalLand(getTotalLand());

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// From Sanguo Mod Performance, ie the CAR Mod
	// Attitude cache
	if (GC.getGameINLINE().isFinalInitialized())
	{
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if( GET_PLAYER((PlayerTypes)iI).isAlive() )
			{
				GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
				GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
			}
		}
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
}


/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  Glider1      */
/*************************************************************************************************/
// RevolutionDCM start - new diplomacy option
void CvPlayer::setDoNotBotherStatus(PlayerTypes playerID)
{
	m_bDoNotBotherStatus = playerID;
}


bool CvPlayer::isDoNotBotherStatus(PlayerTypes playerID) const
{
	if (m_bDoNotBotherStatus != NO_PLAYER && m_bDoNotBotherStatus == playerID)
	{
		return true;
	}
	return false;
}
// RevolutionDCM end
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/


PlayerColorTypes CvPlayer::getPlayerColor() const
{
	return GC.getInitCore().getColor(getID());
}


int CvPlayer::getPlayerTextColorR() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().r * 255));
}


int CvPlayer::getPlayerTextColorG() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().g * 255));
}


int CvPlayer::getPlayerTextColorB() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().b * 255));
}


int CvPlayer::getPlayerTextColorA() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().a * 255));
}


int CvPlayer::getSeaPlotYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiSeaPlotYield[eIndex];
}


void CvPlayer::changeSeaPlotYield(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiSeaPlotYield[eIndex] = (m_aiSeaPlotYield[eIndex] + iChange);

		updateYield();
	}
}


int CvPlayer::getYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiYieldRateModifier[eIndex];
}


void CvPlayer::changeYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiYieldRateModifier[eIndex] = (m_aiYieldRateModifier[eIndex] + iChange);

		invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_makeAssignWorkDirty();

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getCapitalYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCapitalYieldRateModifier[eIndex];
}


void CvPlayer::changeCapitalYieldRateModifier(YieldTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCapitalYieldRateModifier[eIndex] = (m_aiCapitalYieldRateModifier[eIndex] + iChange);

		invalidateYieldRankCache(eIndex);

		pCapitalCity = getCapitalCity();

		if (pCapitalCity != NULL)
		{
			if (eIndex == YIELD_COMMERCE)
			{
				pCapitalCity->updateCommerce();
			}

			pCapitalCity->AI_setAssignWorkDirty(true);

			if (pCapitalCity->getTeam() == GC.getGameINLINE().getActiveTeam())
			{
				pCapitalCity->setInfoDirty(true);
			}
		}
	}
}


int CvPlayer::getExtraYieldThreshold(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiExtraYieldThreshold[eIndex];
}


void CvPlayer::updateExtraYieldThreshold(YieldTypes eIndex)
{
	int iBestValue;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	iBestValue = 0;

	FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::updateExtraYieldThreshold");
	for (iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			if (GC.getTraitInfo((TraitTypes) iI).getExtraYieldThreshold(eIndex) > 0)
			{
				if ((iBestValue == 0) || (GC.getTraitInfo((TraitTypes) iI).getExtraYieldThreshold(eIndex) < iBestValue))
				{
					iBestValue = GC.getTraitInfo((TraitTypes) iI).getExtraYieldThreshold(eIndex);
				}
			}
		}
	}

	if (getExtraYieldThreshold(eIndex) != iBestValue)
	{
		m_aiExtraYieldThreshold[eIndex] = iBestValue;
		FAssert(getExtraYieldThreshold(eIndex) >= 0);

		updateYield();
	}
}


int CvPlayer::getTradeYieldModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiTradeYieldModifier[eIndex];
}


void CvPlayer::changeTradeYieldModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiTradeYieldModifier[eIndex] = (m_aiTradeYieldModifier[eIndex] + iChange);

		updateTradeRoutes();
	}
}


int CvPlayer::getFreeCityCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiFreeCityCommerce[eIndex];
}


void CvPlayer::changeFreeCityCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiFreeCityCommerce[eIndex] = (m_aiFreeCityCommerce[eIndex] + iChange);
		FAssert(getFreeCityCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}


int CvPlayer::getCommercePercent(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCommercePercent[eIndex];
}


void CvPlayer::setCommercePercent(CommerceTypes eIndex, int iNewValue)
{
	int iTotalCommercePercent;
	int iOldValue;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	iOldValue = getCommercePercent(eIndex);

	m_aiCommercePercent[eIndex] = range(iNewValue, 0, 100);

	if (iOldValue != getCommercePercent(eIndex))
	{
		iTotalCommercePercent = 0;

		for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			iTotalCommercePercent += getCommercePercent((CommerceTypes)iI);
		}

		for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			if (iI != eIndex)
			{
				if (100 != iTotalCommercePercent)
				{
					int iAdjustment = std::min(m_aiCommercePercent[iI], iTotalCommercePercent - 100);
					m_aiCommercePercent[iI] -= iAdjustment;
					iTotalCommercePercent -= iAdjustment;
				}
				else
				{
					break;
				}
			}
		}

		FAssert(100 == iTotalCommercePercent);

		updateCommerce();

		AI_makeAssignWorkDirty();

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Financial_Screen_DIRTY_BIT, true);
		}
	}
}


void CvPlayer::changeCommercePercent(CommerceTypes eIndex, int iChange)
{
	setCommercePercent(eIndex, (getCommercePercent(eIndex) + iChange));
}


int CvPlayer::getCommerceRate(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	int iRate = m_aiCommerceRate[eIndex];
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		if (eIndex == COMMERCE_CULTURE)
		{
			iRate += m_aiCommerceRate[COMMERCE_ESPIONAGE];
		}
		else if (eIndex == COMMERCE_ESPIONAGE)
		{
			iRate = 0;
		}
	}

//FfH: Added by Kael 08/28/2008
    if (getDisableResearch() > 0)
    {
        return 0;
    }
//FfH: End Add

	return iRate / 100;
}


void CvPlayer::changeCommerceRate(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCommerceRate[eIndex] += iChange;
//		FAssert(getCommerceRate(eIndex) >= 0);  some buildings give negative commerce Sephi

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

int CvPlayer::getCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCommerceRateModifier[eIndex];
}


void CvPlayer::changeCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCommerceRateModifier[eIndex] = (m_aiCommerceRateModifier[eIndex] + iChange);

		updateCommerce(eIndex);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getCapitalCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCapitalCommerceRateModifier[eIndex];
}


void CvPlayer::changeCapitalCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCapitalCommerceRateModifier[eIndex] = (m_aiCapitalCommerceRateModifier[eIndex] + iChange);

		pCapitalCity = getCapitalCity();

		if (pCapitalCity != NULL)
		{
			pCapitalCity->updateCommerce();

			pCapitalCity->AI_setAssignWorkDirty(true);
		}
	}
}


int CvPlayer::getStateReligionBuildingCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiStateReligionBuildingCommerce[eIndex];
}


void CvPlayer::changeStateReligionBuildingCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiStateReligionBuildingCommerce[eIndex] = (m_aiStateReligionBuildingCommerce[eIndex] + iChange);
		FAssert(getStateReligionBuildingCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}


int CvPlayer::getSpecialistExtraCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiSpecialistExtraCommerce[eIndex];
}


void CvPlayer::changeSpecialistExtraCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiSpecialistExtraCommerce[eIndex] = (m_aiSpecialistExtraCommerce[eIndex] + iChange);
		FAssert(getSpecialistExtraCommerce(eIndex) >= 0);

		updateCommerce(eIndex);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getCommerceFlexibleCount(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCommerceFlexibleCount[eIndex];
}


bool CvPlayer::isCommerceFlexible(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isFoundedFirstCity())
	{
		return false;
	}

	if (eIndex == COMMERCE_ESPIONAGE)
	{
		if (0 == GET_TEAM(getTeam()).getHasMetCivCount(true) || GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
		{
			return false;
		}
	}

	return (GC.getCommerceInfo(eIndex).isFlexiblePercent() || (getCommerceFlexibleCount(eIndex) > 0) || GET_TEAM(getTeam()).isCommerceFlexible(eIndex));
}


void CvPlayer::changeCommerceFlexibleCount(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCommerceFlexibleCount[eIndex] = (m_aiCommerceFlexibleCount[eIndex] + iChange);
		FAssert(getCommerceFlexibleCount(eIndex) >= 0);

		if (!isCommerceFlexible(eIndex))
		{
			setCommercePercent(eIndex, 0);
		}

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(PercentButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getGoldPerTurnByPlayer(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiGoldPerTurnByPlayer[eIndex];
}


void CvPlayer::changeGoldPerTurnByPlayer(PlayerTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_iGoldPerTurn = (m_iGoldPerTurn + iChange);
		m_aiGoldPerTurnByPlayer[eIndex] = (m_aiGoldPerTurnByPlayer[eIndex] + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}

		if (!isHuman())
		{
			AI_doCommerce();
		}
	}
}


bool CvPlayer::isFeatAccomplished(FeatTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_FEAT_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_abFeatAccomplished[eIndex];
}


void CvPlayer::setFeatAccomplished(FeatTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_FEAT_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	m_abFeatAccomplished[eIndex] = bNewValue;
}


bool CvPlayer::isOption(PlayerOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_PLAYEROPTION_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_abOptions[eIndex];
}


void CvPlayer::setOption(PlayerOptionTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_PLAYEROPTION_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	m_abOptions[eIndex] = bNewValue;
}

bool CvPlayer::isPlayable() const
{
	return GC.getInitCore().getPlayableCiv(getID());
}

void CvPlayer::setPlayable(bool bNewValue)
{
	GC.getInitCore().setPlayableCiv(getID(), bNewValue);
}


int CvPlayer::getBonusExport(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBonusExport[eIndex];
}


void CvPlayer::changeBonusExport(BonusTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		pCapitalCity = getCapitalCity();
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(false);
		}
		m_paiBonusExport[eIndex] = (m_paiBonusExport[eIndex] + iChange);
		FAssert(getBonusExport(eIndex) >= 0);
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(true);
		}
	}
}


int CvPlayer::getBonusImport(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBonusImport[eIndex];
}


void CvPlayer::changeBonusImport(BonusTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		pCapitalCity = getCapitalCity();
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(false);
		}
		m_paiBonusImport[eIndex] = (m_paiBonusImport[eIndex] + iChange);
		FAssert(getBonusImport(eIndex) >= 0);
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(true);
		}
	}
}


int CvPlayer::getImprovementCount(ImprovementTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiImprovementCount[eIndex];
}


void CvPlayer::changeImprovementCount(ImprovementTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiImprovementCount[eIndex] = (m_paiImprovementCount[eIndex] + iChange);
	FAssert(getImprovementCount(eIndex) >= 0);
}


int CvPlayer::getFreeBuildingCount(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiFreeBuildingCount[eIndex];
}


bool CvPlayer::isBuildingFree(BuildingTypes eIndex)	const
{
	return (getFreeBuildingCount(eIndex) > 0);
}


void CvPlayer::changeFreeBuildingCount(BuildingTypes eIndex, int iChange)
{
	CvCity* pLoopCity;
	int iOldFreeBuildingCount;
	int iLoop;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

/*************************************************************************************************/
/**	BUGFIX (CvBuildinginfo::getFreeBuilding works correct for tolerant cities) Sephi			**/
/*************************************************************************************************/
	BuildingClassTypes eBuildingClass=(BuildingClassTypes)GC.getBuildingInfo(eIndex).getBuildingClassType();
/*************************************************************************************************/
/**	BUGFIX									END													**/
/*************************************************************************************************/

	if (iChange != 0)
	{
		iOldFreeBuildingCount = getFreeBuildingCount(eIndex);

		m_paiFreeBuildingCount[eIndex] = (m_paiFreeBuildingCount[eIndex] + iChange);
		FAssert(getFreeBuildingCount(eIndex) >= 0);

		if (iOldFreeBuildingCount == 0)
		{
			FAssertMsg(getFreeBuildingCount(eIndex) > 0, "getFreeBuildingCount(eIndex) is expected to be greater than 0");

			for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
/*************************************************************************************************/
/**	BUGFIX (CvBuildinginfo::getFreeBuilding works correct for tolerant cities) Sephi			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				pLoopCity->setNumFreeBuilding(eIndex, 1);
/**								----  End Original Code  ----									**/
				BuildingTypes eTrueIndex=(BuildingTypes)GC.getCivilizationInfo(pLoopCity->getCivilizationType()).getCivilizationBuildings(eBuildingClass);
				if (eTrueIndex!=NO_BUILDING)
				{
					pLoopCity->setNumFreeBuilding(eIndex, 1);
				}
/*************************************************************************************************/
/**	BUGFIX									END													**/
/*************************************************************************************************/

				pLoopCity->setNumFreeBuilding(eIndex, 1);
			}
		}
		else if (getFreeBuildingCount(eIndex) == 0)
		{
			FAssertMsg(iOldFreeBuildingCount > 0, "iOldFreeBuildingCount is expected to be greater than 0");

			for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
/*************************************************************************************************/
/**	BUGFIX (CvBuildinginfo::getFreeBuilding works correct for tolerant cities) Sephi			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				pLoopCity->setNumFreeBuilding(eIndex, 0);
/**								----  End Original Code  ----									**/
				BuildingTypes eTrueIndex=(BuildingTypes)GC.getCivilizationInfo(pLoopCity->getCivilizationType()).getCivilizationBuildings(eBuildingClass);
				if (eTrueIndex!=NO_BUILDING)
				{
					pLoopCity->setNumFreeBuilding(eIndex, 0);
				}
/*************************************************************************************************/
/**	BUGFIX									END													**/
/*************************************************************************************************/

			}
		}
	}
}


int CvPlayer::getExtraBuildingHappiness(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiExtraBuildingHappiness[eIndex];
}


void CvPlayer::changeExtraBuildingHappiness(BuildingTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiExtraBuildingHappiness[eIndex] += iChange;

		updateExtraBuildingHappiness();
	}
}

int CvPlayer::getExtraBuildingHealth(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiExtraBuildingHealth[eIndex];
}


void CvPlayer::changeExtraBuildingHealth(BuildingTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiExtraBuildingHealth[eIndex] += iChange;

		updateExtraBuildingHealth();
	}
}


int CvPlayer::getFeatureHappiness(FeatureTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumFeatureInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiFeatureHappiness[eIndex];
}


void CvPlayer::changeFeatureHappiness(FeatureTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumFeatureInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiFeatureHappiness[eIndex] = (m_paiFeatureHappiness[eIndex] + iChange);

		updateFeatureHappiness();
	}
}


int CvPlayer::getUnitClassCount(UnitClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiUnitClassCount[eIndex];
}


bool CvPlayer::isUnitClassMaxedOut(UnitClassTypes eIndex, int iExtra) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isNationalUnitClass(eIndex))
	{
		return false;
	}

	// lfgr fix: In FfH, MaxPlayerInstances aren't that strict, but only apply when trying to build new units.
	//FAssertMsg(getUnitClassCount(eIndex) <= GC.getUnitClassInfo(eIndex).getMaxPlayerInstances(), "getUnitClassCount is expected to be less than maximum bound of MaxPlayerInstances (invalid index)");

	return ((getUnitClassCount(eIndex) + iExtra) >= GC.getUnitClassInfo(eIndex).getMaxPlayerInstances());
}


void CvPlayer::changeUnitClassCount(UnitClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiUnitClassCount[eIndex] = (m_paiUnitClassCount[eIndex] + iChange);
	FAssert(getUnitClassCount(eIndex) >= 0);
}


int CvPlayer::getUnitClassMaking(UnitClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiUnitClassMaking[eIndex];
}


void CvPlayer::changeUnitClassMaking(UnitClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiUnitClassMaking[eIndex] = (m_paiUnitClassMaking[eIndex] + iChange);
		FAssert(getUnitClassMaking(eIndex) >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Help_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getUnitClassCountPlusMaking(UnitClassTypes eIndex) const
{
	return (getUnitClassCount(eIndex) + getUnitClassMaking(eIndex));
}

// lfgr 11/2021
int CvPlayer::getCasterCount( SpellTypes eSpell ) const
{
	int iCount = 0;
	int iLoop = 0;
	CvUnit* pLoopUnit;
	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		// lfgr 11/2021: More accurate counting of eligible units.
		if( pLoopUnit->canCastWithCurrentPromotions( eSpell ) )
		{
			iCount += 1;
		}
	}
	return iCount;
}


int CvPlayer::getBuildingClassCount(BuildingClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBuildingClassCount[eIndex];
}


bool CvPlayer::isBuildingClassMaxedOut(BuildingClassTypes eIndex, int iExtra) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isNationalWonderClass(eIndex))
	{
		return false;
	}

	FAssertMsg(getBuildingClassCount(eIndex) <= (GC.getBuildingClassInfo(eIndex).getMaxPlayerInstances() + GC.getBuildingClassInfo(eIndex).getExtraPlayerInstances()), "BuildingClassCount is expected to be less than or match the number of max player instances plus extra player instances");

	return ((getBuildingClassCount(eIndex) + iExtra) >= (GC.getBuildingClassInfo(eIndex).getMaxPlayerInstances() + GC.getBuildingClassInfo(eIndex).getExtraPlayerInstances()));
}


void CvPlayer::changeBuildingClassCount(BuildingClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiBuildingClassCount[eIndex] = (m_paiBuildingClassCount[eIndex] + iChange);
	FAssert(getBuildingClassCount(eIndex) >= 0);
}


int CvPlayer::getBuildingClassMaking(BuildingClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBuildingClassMaking[eIndex];
}


void CvPlayer::changeBuildingClassMaking(BuildingClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiBuildingClassMaking[eIndex] = (m_paiBuildingClassMaking[eIndex] + iChange);
		FAssert(getBuildingClassMaking(eIndex) >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Help_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getBuildingClassCountPlusMaking(BuildingClassTypes eIndex) const
{
	return (getBuildingClassCount(eIndex) + getBuildingClassMaking(eIndex));
}


int CvPlayer::getHurryCount(HurryTypes eIndex) const
{
	FAssert(eIndex >= 0);
	FAssert(eIndex < GC.getNumHurryInfos());
	return m_paiHurryCount[eIndex];
}


bool CvPlayer::canHurry(HurryTypes eIndex) const
{
	return (getHurryCount(eIndex) > 0);
}


bool CvPlayer::canPopRush()
{
	return (m_iPopRushHurryCount > 0);
}

void CvPlayer::changeHurryCount(HurryTypes eIndex, int iChange)
{
	FAssert(eIndex >= 0);
	FAssert(eIndex < GC.getNumHurryInfos());

	int oldHurryCount = m_paiHurryCount[eIndex];
	m_paiHurryCount[eIndex] = (m_paiHurryCount[eIndex] + iChange);
	FAssert(getHurryCount(eIndex) >= 0);

	// if we just went from 0 to 1 (or the reverse)
	if ((oldHurryCount > 0) != (m_paiHurryCount[eIndex] > 0))
	{
		// does this hurry reduce population?
		if (GC.getHurryInfo(eIndex).getProductionPerPopulation() > 0)
		{
			m_iPopRushHurryCount += iChange;
			FAssert(m_iPopRushHurryCount >= 0);
		}
	}
}

// lfgr 05/2022: Expose inflation
int CvPlayer::getInflationModifier() const
{
	return m_iInflationModifier;
}

// lfgr 05/2022: Expose inflation
void CvPlayer::changeInflationModifier( int iChange )
{
	m_iInflationModifier += iChange;
}

int CvPlayer::getSpecialBuildingNotRequiredCount(SpecialBuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiSpecialBuildingNotRequiredCount[eIndex];
}


bool CvPlayer::isSpecialBuildingNotRequired(SpecialBuildingTypes eIndex) const
{
	return (getSpecialBuildingNotRequiredCount(eIndex) > 0);
}


void CvPlayer::changeSpecialBuildingNotRequiredCount(SpecialBuildingTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiSpecialBuildingNotRequiredCount[eIndex] = (m_paiSpecialBuildingNotRequiredCount[eIndex] + iChange);
	FAssert(getSpecialBuildingNotRequiredCount(eIndex) >= 0);
}


int CvPlayer::getHasCivicOptionCount(CivicOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiHasCivicOptionCount[eIndex];
}


bool CvPlayer::isHasCivicOption(CivicOptionTypes eIndex) const
{
	return (getHasCivicOptionCount(eIndex) > 0);
}


void CvPlayer::changeHasCivicOptionCount(CivicOptionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiHasCivicOptionCount[eIndex] = (m_paiHasCivicOptionCount[eIndex] + iChange);
	FAssert(getHasCivicOptionCount(eIndex) >= 0);
}


int CvPlayer::getNoCivicUpkeepCount(CivicOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiNoCivicUpkeepCount[eIndex];
}


bool CvPlayer::isNoCivicUpkeep(CivicOptionTypes eIndex) const
{
	return (getNoCivicUpkeepCount(eIndex) > 0);
}


void CvPlayer::changeNoCivicUpkeepCount(CivicOptionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiNoCivicUpkeepCount[eIndex] = (m_paiNoCivicUpkeepCount[eIndex] + iChange);
		FAssert(getNoCivicUpkeepCount(eIndex) >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getHasReligionCount(ReligionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiHasReligionCount[eIndex];
}


int CvPlayer::countTotalHasReligion() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iCount += getHasReligionCount((ReligionTypes)iI);
	}

	return iCount;
}

int CvPlayer::getHasCorporationCount(CorporationTypes eIndex) const
{
	if (!isActiveCorporation(eIndex))
	{
		return 0;
	}

	return m_paiHasCorporationCount[eIndex];
}


int CvPlayer::countTotalHasCorporation() const
{
	int iCount = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		iCount += getHasCorporationCount((CorporationTypes)iI);
	}

	return iCount;
}

bool CvPlayer::isActiveCorporation(CorporationTypes eIndex) const
{
	if (isNoCorporations())
	{
		return false;
	}

	if (isNoForeignCorporations() && !hasHeadquarters(eIndex))
	{
		return false;
	}

	return true;
}


int CvPlayer::findHighestHasReligionCount() const
{
	int iValue;
	int iBestValue;
	int iI;

	iBestValue = 0;

	for (iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iValue = getHasReligionCount((ReligionTypes)iI);

		if (iValue > iBestValue)
		{
			iBestValue = iValue;
		}
	}

	return iBestValue;
}


void CvPlayer::changeHasReligionCount(ReligionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiHasReligionCount[eIndex] = (m_paiHasReligionCount[eIndex] + iChange);
		FAssert(getHasReligionCount(eIndex) >= 0);

		GC.getGameINLINE().updateBuildingCommerce();

		GC.getGameINLINE().AI_makeAssignWorkDirty();
	}
}


void CvPlayer::changeHasCorporationCount(CorporationTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiHasCorporationCount[eIndex] += iChange;
		FAssert(getHasCorporationCount(eIndex) >= 0);

		GC.getGameINLINE().updateBuildingCommerce();

		GC.getGameINLINE().AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getUpkeepCount(UpkeepTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUpkeepInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(m_paiUpkeepCount != NULL, "m_paiUpkeepCount is not expected to be equal with NULL");
	return m_paiUpkeepCount[eIndex];
}


void CvPlayer::changeUpkeepCount(UpkeepTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUpkeepInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		FAssertMsg(m_paiUpkeepCount != NULL, "m_paiUpkeepCount is not expected to be equal with NULL");
		m_paiUpkeepCount[eIndex] = (m_paiUpkeepCount[eIndex] + iChange);
		FAssertMsg(getUpkeepCount(eIndex) >= 0, "getUpkeepCount(eIndex) is expected to be non-negative (invalid Index)");

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getSpecialistValidCount(SpecialistTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(m_paiSpecialistValidCount != NULL, "m_paiSpecialistValidCount is not expected to be equal with NULL");
	return m_paiSpecialistValidCount[eIndex];
}


bool CvPlayer::isSpecialistValid(SpecialistTypes eIndex) const
{
	return (getSpecialistValidCount(eIndex) > 0);
}


void CvPlayer::changeSpecialistValidCount(SpecialistTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		FAssertMsg(m_paiSpecialistValidCount != NULL, "m_paiSpecialistValidCount is not expected to be equal with NULL");
		m_paiSpecialistValidCount[eIndex] = (m_paiSpecialistValidCount[eIndex] + iChange);
		FAssertMsg(getSpecialistValidCount(eIndex) >= 0, "getSpecialistValidCount(eIndex) is expected to be non-negative (invalid Index)");

		AI_makeAssignWorkDirty();
	}
}


bool CvPlayer::isResearchingTech(TechTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumTechInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_pabResearchingTech[eIndex];
}


void CvPlayer::setResearchingTech(TechTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumTechInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (isResearchingTech(eIndex) != bNewValue)
	{
		m_pabResearchingTech[eIndex] = bNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Popup_DIRTY_BIT, true); // to check whether we still need the tech chooser popup
		}
	}
}

bool CvPlayer::isLoyalMember(VoteSourceTypes eVoteSource) const
{
	FAssertMsg(eVoteSource >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eVoteSource < GC.getNumVoteSourceInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_pabLoyalMember[eVoteSource];
}

void CvPlayer::setLoyalMember(VoteSourceTypes eVoteSource, bool bNewValue)
{
	FAssertMsg(eVoteSource >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eVoteSource < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (isLoyalMember(eVoteSource) != bNewValue)
	{
		processVoteSourceBonus(eVoteSource, false);
		m_pabLoyalMember[eVoteSource] = bNewValue;
		processVoteSourceBonus(eVoteSource, true);

		GC.getGameINLINE().updateSecretaryGeneral();
	}
}

CivicTypes CvPlayer::getCivics(CivicOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paeCivics[eIndex];
}


int CvPlayer::getSingleCivicUpkeep(CivicTypes eCivic, bool bIgnoreAnarchy) const
{
	int iUpkeep;

	if (eCivic == NO_CIVIC)
	{
		return 0;
	}

	if (isNoCivicUpkeep((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())))
	{
		return 0;
	}

	if (GC.getCivicInfo(eCivic).getUpkeep() == NO_UPKEEP)
	{
		return 0;
	}

	if (!bIgnoreAnarchy)
	{
		if (isAnarchy())
		{
			return 0;
		}

//FfH: Added by Kael 10/03/2008
        if (getDisableProduction() > 0)
        {
            return 0;
        }
//FfH: End Add

	}

	iUpkeep = 0;

	iUpkeep += ((std::max(0, (getTotalPopulation() + GC.getDefineINT("UPKEEP_POPULATION_OFFSET") - GC.getCivicInfo(eCivic).getCivicOptionType())) * GC.getUpkeepInfo((UpkeepTypes)(GC.getCivicInfo(eCivic).getUpkeep())).getPopulationPercent()) / 100);

//FfH: Modified by Kael 11/18/2007
//	iUpkeep += ((std::max(0, (getNumCities() + GC.getDefineINT("UPKEEP_CITY_OFFSET") + GC.getCivicInfo(eCivic).getCivicOptionType() - (GC.getNumCivicOptionInfos() / 2))) * GC.getUpkeepInfo((UpkeepTypes)(GC.getCivicInfo(eCivic).getUpkeep())).getCityPercent()) / 100);
	iUpkeep += ((std::max(0, ((getNumCities() - getNumSettlements()) + GC.getDefineINT("UPKEEP_CITY_OFFSET") + GC.getCivicInfo(eCivic).getCivicOptionType() - (GC.getNumCivicOptionInfos() / 2))) * GC.getUpkeepInfo((UpkeepTypes)(GC.getCivicInfo(eCivic).getUpkeep())).getCityPercent()) / 100);
//FfH: End Modify

	iUpkeep *= std::max(0, (getUpkeepModifier() + 100));
	iUpkeep /= 100;

	iUpkeep *= GC.getHandicapInfo(getHandicapType()).getCivicUpkeepPercent();
	iUpkeep /= 100;

	if (!isHuman() && !isBarbarian())
	{
		iUpkeep *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAICivicUpkeepPercent();
		iUpkeep /= 100;

		iUpkeep *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentRealEra()) + 100));
		iUpkeep /= 100;
	}

	return std::max(0, iUpkeep);
}


int CvPlayer::getCivicUpkeep(CivicTypes* paeCivics, bool bIgnoreAnarchy) const
{
	int iTotalUpkeep;
	int iI;

	if (paeCivics == NULL)
	{
		paeCivics = m_paeCivics;
	}

	iTotalUpkeep = 0;

	for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		iTotalUpkeep += getSingleCivicUpkeep(paeCivics[iI], bIgnoreAnarchy);
	}

/************************************************************************************************/
/* REVOLUTION_MOD                         02/01/08                                jdog5000      */
/*                                                                                              */
/* Rebels pay less civic upkeep                                                                 */
/************************************************************************************************/
	if( isRebel() )
		iTotalUpkeep /= 2;
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	return iTotalUpkeep;
}


void CvPlayer::setCivics(CivicOptionTypes eIndex, CivicTypes eNewValue)
{
	CvWString szBuffer;
	CivicTypes eOldCivic;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eNewValue >= 0, "eNewValue is expected to be non-negative (invalid Index)");
	FAssertMsg(eNewValue < GC.getNumCivicInfos(), "eNewValue is expected to be within maximum bounds (invalid Index)");

	eOldCivic = getCivics(eIndex);

	if (eOldCivic != eNewValue)
	{
		m_paeCivics[eIndex] = eNewValue;

		if (eOldCivic != NO_CIVIC)
		{
			processCivics(eOldCivic, -1);
		}
		if (getCivics(eIndex) != NO_CIVIC)
		{
			processCivics(getCivics(eIndex), 1);
		}

		GC.getGameINLINE().updateSecretaryGeneral();

		GC.getGameINLINE().AI_makeAssignWorkDirty();

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if (gDLL->isDiplomacy() && (gDLL->getDiplomacyPlayer() == getID()))
			{
				gDLL->updateDiplomacyAttitude(true);
			}

/************************************************************************************************/
/* REVOLUTION_MOD                         04/28/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/*
			if (!isBarbarian())
*/
			// Silence announcement for civs that are not alive, ie rebel civs who may not be born
			// and also for minor civs
			if (!isBarbarian() && !isMinorCiv() && isAlive())
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
			{
				if (getCivics(eIndex) != NO_CIVIC)
				{
					if (getCivics(eIndex) != GC.getCivilizationInfo(getCivilizationType()).getCivilizationInitialCivics(eIndex))
					{
						for (iI = 0; iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam())

//FfH: Added by Kael 11/15/2007
                                  && GET_PLAYER((PlayerTypes)iI).canSeeCivic(eIndex)
//FfH: End Add

                                  )

								{
									szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_ADOPTED_CIVIC", getNameKey(), GC.getCivicInfo(getCivics(eIndex)).getTextKeyWide());
									gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MAJOR_EVENT);
								}
							}
						}

						szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_ADOPTED_CIVIC", getNameKey(), GC.getCivicInfo(getCivics(eIndex)).getTextKeyWide());
						GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer);
					}
				}
			}
		}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
		// From Sanguo Mod Performance, ie the CAR Mod
		// Attitude cache
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
			GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	}
}


int CvPlayer::getSpecialistExtraYield(SpecialistTypes eIndex1, YieldTypes eIndex2) const
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 expected to be >= 0");
	FAssertMsg(eIndex1 < GC.getNumSpecialistInfos(), "eIndex1 expected to be < GC.getNumSpecialistInfos()");
	FAssertMsg(eIndex2 >= 0, "eIndex2 expected to be >= 0");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 expected to be < NUM_YIELD_TYPES");
	return m_ppaaiSpecialistExtraYield[eIndex1][eIndex2];
}


void CvPlayer::changeSpecialistExtraYield(SpecialistTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 expected to be >= 0");
	FAssertMsg(eIndex1 < GC.getNumSpecialistInfos(), "eIndex1 expected to be < GC.getNumSpecialistInfos()");
	FAssertMsg(eIndex2 >= 0, "eIndex2 expected to be >= 0");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_ppaaiSpecialistExtraYield[eIndex1][eIndex2] = (m_ppaaiSpecialistExtraYield[eIndex1][eIndex2] + iChange);
		FAssert(getSpecialistExtraYield(eIndex1, eIndex2) >= 0);

		updateExtraSpecialistYield();

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getImprovementYieldChange(ImprovementTypes eIndex1, YieldTypes eIndex2) const
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumImprovementInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");
	return m_ppaaiImprovementYieldChange[eIndex1][eIndex2];
}


void CvPlayer::changeImprovementYieldChange(ImprovementTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumImprovementInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_ppaaiImprovementYieldChange[eIndex1][eIndex2] = (m_ppaaiImprovementYieldChange[eIndex1][eIndex2] + iChange);
//		FAssert(getImprovementYieldChange(eIndex1, eIndex2) >= 0); //workshops give negative yields modified Sephi
		updateYield();
	}
}


// XXX should pUnit be a CvSelectionGroup???
void CvPlayer::updateGroupCycle(CvUnit* pUnit)
{
	CLLNode<IDInfo>* pUnitNode;
	CLLNode<int>* pSelectionGroupNode;
	CLLNode<int>* pBestSelectionGroupNode;
	CvSelectionGroup* pLoopSelectionGroup;
	CvUnit* pHeadUnit;
	CvUnit* pBeforeUnit;
	CvUnit* pAfterUnit;
	CvUnit* pLoopUnit;
	CvPlot* pPlot;
	int iValue;
	int iBestValue;

	if (!(pUnit->onMap()))
	{
		return;
	}

	FAssertMsg(pUnit->getGroup() != NULL, "Unit->getGroup() is not assigned a valid value");

	removeGroupCycle(pUnit->getGroupID());

	pPlot = pUnit->plot();

	pBeforeUnit = NULL;
	pAfterUnit = NULL;

	pUnitNode = pPlot->headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = pPlot->nextUnitNode(pUnitNode);

		if (pLoopUnit->isGroupHead())
		{
			if (pLoopUnit != pUnit)
			{
				if (!isBeforeUnitCycle(pLoopUnit, pUnit))
				{
					pBeforeUnit = pLoopUnit;
					break;
				}
				else
				{
					pAfterUnit = pLoopUnit;
				}
			}
		}
	}

	pSelectionGroupNode = headGroupCycleNode();

	iBestValue = MAX_INT;
	pBestSelectionGroupNode = NULL;

	while (pSelectionGroupNode != NULL)
	{
		pLoopSelectionGroup = getSelectionGroup(pSelectionGroupNode->m_data);
		FAssertMsg(pLoopSelectionGroup != NULL, "LoopSelectionGroup is not assigned a valid value");

		pHeadUnit = pLoopSelectionGroup->getHeadUnit();

		if (pHeadUnit != NULL)
		{
			if (pBeforeUnit != NULL)
			{
				if (pBeforeUnit == pHeadUnit)
				{
					pBestSelectionGroupNode = pSelectionGroupNode;
					break;
				}
			}
			else if (pAfterUnit != NULL)
			{
				if (pAfterUnit == pHeadUnit)
				{
					pBestSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
					break;
				}
			}
			else
			{
				iValue = plotDistance(pUnit->getX_INLINE(), pUnit->getY_INLINE(), pHeadUnit->getX_INLINE(), pHeadUnit->getY_INLINE());

				if (iValue < iBestValue)
				{
					iBestValue = iValue;
					pBestSelectionGroupNode = pSelectionGroupNode;
				}
			}
		}

		pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
	}

	if (pBestSelectionGroupNode != NULL)
	{
		m_groupCycle.insertBefore(pUnit->getGroupID(), pBestSelectionGroupNode);
	}
	else
	{
		m_groupCycle.insertAtEnd(pUnit->getGroupID());
	}
}


void CvPlayer::removeGroupCycle(int iID)
{
	CLLNode<int>* pSelectionGroupNode;

	pSelectionGroupNode = headGroupCycleNode();

	while (pSelectionGroupNode != NULL)
	{
		if (pSelectionGroupNode->m_data == iID)
		{
			pSelectionGroupNode = deleteGroupCycleNode(pSelectionGroupNode);
			break;
		}
		else
		{
			pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
		}
	}
}


CLLNode<int>* CvPlayer::deleteGroupCycleNode(CLLNode<int>* pNode)
{
	return m_groupCycle.deleteNode(pNode);
}


CLLNode<int>* CvPlayer::nextGroupCycleNode(CLLNode<int>* pNode) const
{
	return m_groupCycle.next(pNode);
}


CLLNode<int>* CvPlayer::previousGroupCycleNode(CLLNode<int>* pNode) const
{
	return m_groupCycle.prev(pNode);
}


CLLNode<int>* CvPlayer::headGroupCycleNode() const
{
	return m_groupCycle.head();
}


CLLNode<int>* CvPlayer::tailGroupCycleNode() const
{
	return m_groupCycle.tail();
}


//	Finds the path length from this tech type to one you already know
int CvPlayer::findPathLength(TechTypes eTech, bool bCost) const
{
	int i;
	int iNumSteps = 0;
	int iShortestPath = 0;
	int iPathLength = 0;
	TechTypes ePreReq;
	TechTypes eShortestOr;

	if (GET_TEAM(getTeam()).isHasTech(eTech) || isResearchingTech(eTech))
	{
		//	We have this tech, no reason to add this to the pre-reqs
		//	Base case return 0, we know it...
		return 0;
	}

	//	Cycle through the and paths and add up their tech lengths
	for (i = 0; i < GC.getNUM_AND_TECH_PREREQS(); i++)
	{
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqAndTechs(i);

		if (ePreReq != NO_TECH)
		{
			iPathLength += findPathLength(ePreReq, bCost);
		}
	}

	eShortestOr = NO_TECH;
	iShortestPath = MAX_INT;
	//	Find the shortest OR tech
	for (i = 0; i < GC.getNUM_OR_TECH_PREREQS(); i++)
	{
		//	Grab the tech
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqOrTechs(i);

		//	If this is a valid tech
		if (ePreReq != NO_TECH)
		{
			//	Recursively find the path length (takes into account all ANDs)
			iNumSteps = findPathLength(ePreReq, bCost);

			//	If the prereq is a valid tech and its the current shortest, mark it as such
			if (iNumSteps < iShortestPath)
			{
				eShortestOr = ePreReq;
				iShortestPath = iNumSteps;
			}
		}
	}

	//	If the shortest OR is a valid tech, add the steps to it...
	if (eShortestOr != NO_TECH)
	{
		iPathLength += iShortestPath;
	}

	return (iPathLength + ((bCost) ? GET_TEAM(getTeam()).getResearchCost(eTech) : 1));
}


//	Function specifically for python/tech chooser screen
int CvPlayer::getQueuePosition(TechTypes eTech) const
{
	int i = 1;
	CLLNode<TechTypes>* pResearchNode;

	for (pResearchNode = headResearchQueueNode(); pResearchNode; pResearchNode = nextResearchQueueNode(pResearchNode))
	{
		if (pResearchNode->m_data == eTech)
		{
			return i;
		}
		i++;
	}

	return -1;
}


void CvPlayer::clearResearchQueue()
{
	int iI;

	m_researchQueue.clear();

	for (iI = 0; iI < GC.getNumTechInfos(); iI++)
	{
		setResearchingTech(((TechTypes)iI), false);
	}

	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


//	Pushes research onto the queue.  If it is an append if will put it
//	and its pre-reqs into the queue.  If it is not an append it will change
//	research immediately and should be used with clear.  Clear will clear the entire queue.
bool CvPlayer::pushResearch(TechTypes eTech, bool bClear)
{
	int i;
	int iNumSteps;
	int iShortestPath;
	bool bOrPrereqFound;
	TechTypes ePreReq;
  TechTypes eShortestOr;

	FAssertMsg(eTech != NO_TECH, "Tech is not assigned a valid value");

	if (GET_TEAM(getTeam()).isHasTech(eTech) || isResearchingTech(eTech))
	{
		//	We have this tech, no reason to add this to the pre-reqs
		return true;
	}

	if (!canEverResearch(eTech))
	{
		return false;
	}

	//	Pop the entire queue...
	if (bClear)
	{
		clearResearchQueue();
	}

	//	Add in all the pre-reqs for the and techs...
	for (i = 0; i < GC.getNUM_AND_TECH_PREREQS(); i++)
	{
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqAndTechs(i);

		if (ePreReq != NO_TECH)
		{
			if (!pushResearch(ePreReq))
			{
				return false;
			}
		}
	}

	// Will return the shortest path of all the or techs.  Tie breaker goes to the first one...
	eShortestOr = NO_TECH;
	iShortestPath = MAX_INT;
	bOrPrereqFound = false;
	//	Cycle through all the OR techs
	for (i = 0; i < GC.getNUM_OR_TECH_PREREQS(); i++)
	{
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqOrTechs(i);

		if (ePreReq != NO_TECH)
		{
			bOrPrereqFound = true;

			//	If the pre-req exists, and we have it, it is the shortest path, get out, we're done
			if (GET_TEAM(getTeam()).isHasTech(ePreReq))
			{
				eShortestOr = ePreReq;
				break;
			}

			if (canEverResearch(ePreReq))
			{
				//	Find the length of the path to this pre-req
				iNumSteps = findPathLength(ePreReq);

				//	If this pre-req is a valid tech, and its the shortest current path, set it as such
				if (iNumSteps < iShortestPath)
				{
					eShortestOr = ePreReq;
					iShortestPath = iNumSteps;
				}
			}
		}
	}

	//	If the shortest path tech is valid, push it (and its children) on to the research queue recursively
	if (eShortestOr != NO_TECH)
	{
		if (!pushResearch(eShortestOr))
		{
			return false;
		}
	}
	else if (bOrPrereqFound)
	{
		return false;
	}

	//	Insert this tech at the end of the queue
	m_researchQueue.insertAtEnd(eTech);

	setResearchingTech(eTech, true);

	//	Set the dirty bits
	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}

	// ONEVENT - Tech selected (any)
	CvEventReporter::getInstance().techSelected(eTech, getID());

	return true;
}


//	If bHead is true we delete the entire queue...
void CvPlayer::popResearch(TechTypes eTech)
{
	CLLNode<TechTypes>* pResearchNode;

	for (pResearchNode = headResearchQueueNode(); pResearchNode; pResearchNode = nextResearchQueueNode(pResearchNode))
	{
		if (pResearchNode->m_data == eTech)
		{
			m_researchQueue.deleteNode(pResearchNode);
			break;
		}
	}

	setResearchingTech(eTech, false);

	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


int CvPlayer::getLengthResearchQueue() const
{
	return m_researchQueue.getLength();
}


CLLNode<TechTypes>* CvPlayer::nextResearchQueueNode(CLLNode<TechTypes>* pNode) const
{
	return m_researchQueue.next(pNode);
}


CLLNode<TechTypes>* CvPlayer::headResearchQueueNode() const
{
	return m_researchQueue.head();
}


CLLNode<TechTypes>* CvPlayer::tailResearchQueueNode() const
{
	return m_researchQueue.tail();
}


void CvPlayer::addCityName(const CvWString& szName)
{
	m_cityNames.insertAtEnd(szName);
}


int CvPlayer::getNumCityNames() const
{
	return m_cityNames.getLength();
}


CvWString CvPlayer::getCityName(int iIndex) const
{
	CLLNode<CvWString>* pCityNameNode;

	pCityNameNode = m_cityNames.nodeNum(iIndex);

	if (pCityNameNode != NULL)
	{
		return pCityNameNode->m_data;
	}
	else
	{
		return L"";
	}
}


CLLNode<CvWString>* CvPlayer::nextCityNameNode(CLLNode<CvWString>* pNode) const
{
	return m_cityNames.next(pNode);
}


CLLNode<CvWString>* CvPlayer::headCityNameNode() const
{
	return m_cityNames.head();
}


CvPlotGroup* CvPlayer::firstPlotGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_plotGroups.beginIter(pIterIdx) : m_plotGroups.endIter(pIterIdx);
}


CvPlotGroup* CvPlayer::nextPlotGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_plotGroups.nextIter(pIterIdx) : m_plotGroups.prevIter(pIterIdx);
}


int CvPlayer::getNumPlotGroups() const
{
	return m_plotGroups.getCount();
}


CvPlotGroup* CvPlayer::getPlotGroup(int iID) const
{
	return((CvPlotGroup *)(m_plotGroups.getAt(iID)));
}


CvPlotGroup* CvPlayer::addPlotGroup()
{
	return((CvPlotGroup *)(m_plotGroups.add()));
}


void CvPlayer::deletePlotGroup(int iID)
{
	m_plotGroups.removeAt(iID);
}


CvCity* CvPlayer::firstCity(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_cities.beginIter(pIterIdx) : m_cities.endIter(pIterIdx);
}


CvCity* CvPlayer::nextCity(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_cities.nextIter(pIterIdx) : m_cities.prevIter(pIterIdx);
}


int CvPlayer::getNumCities() const
{
	return m_cities.getCount();
}


CvCity* CvPlayer::getCity(int iID) const
{
	return(m_cities.getAt(iID));
}


CvCity* CvPlayer::addCity()
{
	return(m_cities.add());
}


void CvPlayer::deleteCity(int iID)
{
	m_cities.removeAt(iID);
}


CvUnit* CvPlayer::firstUnit(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_units.beginIter(pIterIdx) : m_units.endIter(pIterIdx);
}


CvUnit* CvPlayer::nextUnit(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_units.nextIter(pIterIdx) : m_units.prevIter(pIterIdx);
}


int CvPlayer::getNumUnits() const
{
	return m_units.getCount();
}


CvUnit* CvPlayer::getUnit(int iID) const
{
	return (m_units.getAt(iID));
}


CvUnit* CvPlayer::addUnit()
{
	return (m_units.add());
}


void CvPlayer::deleteUnit(int iID)
{
	m_units.removeAt(iID);
}


CvSelectionGroup* CvPlayer::firstSelectionGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_selectionGroups.beginIter(pIterIdx) : m_selectionGroups.endIter(pIterIdx);
}


CvSelectionGroup* CvPlayer::nextSelectionGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_selectionGroups.nextIter(pIterIdx) : m_selectionGroups.prevIter(pIterIdx);
}


int CvPlayer::getNumSelectionGroups() const
{
	return m_selectionGroups.getCount();
}


CvSelectionGroup* CvPlayer::getSelectionGroup(int iID) const
{
	return ((CvSelectionGroup *)(m_selectionGroups.getAt(iID)));
}


CvSelectionGroup* CvPlayer::addSelectionGroup()
{
	return ((CvSelectionGroup *)(m_selectionGroups.add()));
}


void CvPlayer::deleteSelectionGroup(int iID)
{
	bool bRemoved = m_selectionGroups.removeAt(iID);

	FAssertMsg(bRemoved, "could not find group, delete failed");
}

EventTriggeredData* CvPlayer::firstEventTriggered(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_eventsTriggered.beginIter(pIterIdx) : m_eventsTriggered.endIter(pIterIdx);
}

EventTriggeredData* CvPlayer::nextEventTriggered(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_eventsTriggered.nextIter(pIterIdx) : m_eventsTriggered.prevIter(pIterIdx);
}

int CvPlayer::getNumEventsTriggered() const
{
	return m_eventsTriggered.getCount();
}

EventTriggeredData* CvPlayer::getEventTriggered(int iID) const
{
	return ((EventTriggeredData*)(m_eventsTriggered.getAt(iID)));
}

EventTriggeredData* CvPlayer::addEventTriggered()
{
	return ((EventTriggeredData*)(m_eventsTriggered.add()));
}

void CvPlayer::deleteEventTriggered(int iID)
{
	m_eventsTriggered.removeAt(iID);
}


void CvPlayer::addMessage(const CvTalkingHeadMessage& message)
{
	m_listGameMessages.push_back(message);
}


void CvPlayer::clearMessages()
{
	m_listGameMessages.clear();
}


const CvMessageQueue& CvPlayer::getGameMessages() const
{
	return (m_listGameMessages);
}


void CvPlayer::expireMessages()
{
	CvMessageQueue::iterator it = m_listGameMessages.begin();
	bool bFoundExpired = false;
	while(it != m_listGameMessages.end())
	{
		CvTalkingHeadMessage& message = *it;
		if (GC.getGameINLINE().getGameTurn() >= message.getExpireTurn())
		{
			it = m_listGameMessages.erase(it);
			bFoundExpired = true;
		}
		else
		{
			++it;
		}
	}
	if (bFoundExpired)
	{
		gDLL->getInterfaceIFace()->dirtyTurnLog(getID());
	}
}


void CvPlayer::addPopup(CvPopupInfo* pInfo, bool bFront)
{
	if (isHuman())
	{
		if (bFront)
		{
			m_listPopups.push_front(pInfo);
		}
		else
		{
			m_listPopups.push_back(pInfo);
		}
	}
	else
	{
		SAFE_DELETE(pInfo);
	}
}


void CvPlayer::clearPopups()
{
	CvPopupQueue::iterator it;
	for (it = m_listPopups.begin(); it != m_listPopups.end(); ++it)
	{
		CvPopupInfo* pInfo = *it;
		if (NULL != pInfo)
		{
			delete pInfo;
		}
	}
	m_listPopups.clear();
}


CvPopupInfo* CvPlayer::popFrontPopup()
{
	CvPopupInfo* pInfo = NULL;
	if (!m_listPopups.empty())
	{
		pInfo = m_listPopups.front();
		m_listPopups.pop_front();
	}
	return pInfo;
}


const CvPopupQueue& CvPlayer::getPopups() const
{
	return (m_listPopups);
}


void CvPlayer::addDiplomacy(CvDiploParameters* pDiplo)
{
	if (NULL != pDiplo)
	{
		m_listDiplomacy.push_back(pDiplo);
	}
}


void CvPlayer::clearDiplomacy()
{
	CvDiploQueue::iterator it;
	for (it = m_listDiplomacy.begin(); it != m_listDiplomacy.end(); ++it)
	{
		CvDiploParameters* pDiplo = *it;
		if (NULL != pDiplo)
		{
			delete pDiplo;
		}
	}
	m_listDiplomacy.clear();
}


const CvDiploQueue& CvPlayer::getDiplomacy() const
{
	return (m_listDiplomacy);
}


CvDiploParameters* CvPlayer::popFrontDiplomacy()
{
	CvDiploParameters* pDiplo = NULL;
	if (!m_listDiplomacy.empty())
	{
		pDiplo = m_listDiplomacy.front();
		m_listDiplomacy.pop_front();
	}
	return pDiplo;
}


void CvPlayer::showSpaceShip()
{
	CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
	pInfo->setData1(-1);
	pInfo->setText(L"showSpaceShip");
	addPopup(pInfo);
}

void CvPlayer::clearSpaceShipPopups()
{
	//clear all spaceship popups
	CvPopupQueue::iterator it;
	for (it = m_listPopups.begin(); it != m_listPopups.end(); )
	{
		CvPopupInfo* pInfo = *it;
		if (NULL != pInfo)
		{
			if(pInfo->getText().compare(L"showSpaceShip") == 0)
			{
				it = m_listPopups.erase(it);
				SAFE_DELETE(pInfo);
			}
			else
			{
				it++;
			}
		}
		else
		{
			it++;
		}
	}
}

int CvPlayer::getScoreHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapScoreHistory.find(iTurn);
	if (it != m_mapScoreHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateScoreHistory(int iTurn, int iBestScore)
{
	m_mapScoreHistory[iTurn] = iBestScore;
}

int CvPlayer::getEconomyHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapEconomyHistory.find(iTurn);
	if (it != m_mapEconomyHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateEconomyHistory(int iTurn, int iBestEconomy)
{
	m_mapEconomyHistory[iTurn] = iBestEconomy;
}

int CvPlayer::getIndustryHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapIndustryHistory.find(iTurn);
	if (it != m_mapIndustryHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateIndustryHistory(int iTurn, int iBestIndustry)
{
	m_mapIndustryHistory[iTurn] = iBestIndustry;
}

int CvPlayer::getAgricultureHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapAgricultureHistory.find(iTurn);
	if (it != m_mapAgricultureHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateAgricultureHistory(int iTurn, int iBestAgriculture)
{
	m_mapAgricultureHistory[iTurn] = iBestAgriculture;
}

int CvPlayer::getPowerHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapPowerHistory.find(iTurn);
	if (it != m_mapPowerHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updatePowerHistory(int iTurn, int iBestPower)
{
	m_mapPowerHistory[iTurn] = iBestPower;
}

int CvPlayer::getCultureHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapCultureHistory.find(iTurn);
	if (it != m_mapCultureHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateCultureHistory(int iTurn, int iBestCulture)
{
	m_mapCultureHistory[iTurn] = iBestCulture;
}

int CvPlayer::getEspionageHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapEspionageHistory.find(iTurn);
	if (it != m_mapEspionageHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateEspionageHistory(int iTurn, int iBestEspionage)
{
	m_mapEspionageHistory[iTurn] = iBestEspionage;
}


/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         02/04/08                            Glider1        */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
// RevolutionDCM - record revolution stability history start
// Data is used for the CvInfo graphs
int CvPlayer::getRevolutionStabilityHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapRevolutionStabilityHistory.find(iTurn);
	if (it != m_mapRevolutionStabilityHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateRevolutionStabilityHistory(int iTurn, int iRevolutionStability)
{
	m_mapRevolutionStabilityHistory[iTurn] = iRevolutionStability;
}
// RevolutionDCM end
/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         END                                 Glider1        */
/************************************************************************************************/


std::string CvPlayer::getScriptData() const
{
	return m_szScriptData;
}

void CvPlayer::setScriptData(std::string szNewValue)
{
	m_szScriptData = szNewValue;
}

const CvString CvPlayer::getPbemEmailAddress() const
{
	return GC.getInitCore().getEmail(getID());
}

void CvPlayer::setPbemEmailAddress(const char* szAddress)
{
	GC.getInitCore().setEmail(getID(), szAddress);
}

const CvString CvPlayer::getSmtpHost() const
{
	return GC.getInitCore().getSmtpHost(getID());
}

void CvPlayer::setSmtpHost(const char* szHost)
{
	GC.getInitCore().setSmtpHost(getID(), szHost);
}

// Protected Functions...

void CvPlayer::doGold()
{
	bool bStrike;
	int iGoldChange;
	int iDisbandUnit;
	int iI;

	CyArgsList argsList;
	argsList.add(getID());
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doGold", argsList.makeFunctionArgs(), &lResult);
	if (lResult == 1)
	{
		return;
	}

	iGoldChange = calculateGoldRate();

	//FAssert(isHuman() || isBarbarian() || ((getGold() + iGoldChange) >= 0) || isAnarchy());

	changeGold(iGoldChange);

	bStrike = false;

	if (getGold() < 0)
	{
		setGold(0);

		if (!isBarbarian() && (getNumCities() > 0))
		{
			bStrike = true;
		}
	}

	if (bStrike)
	{
		setStrike(true);
		changeStrikeTurns(1);

		if (getStrikeTurns() > 1)
		{
			iDisbandUnit = (getStrikeTurns() / 2); // XXX mod?

			for (iI = 0; iI < iDisbandUnit; iI++)
			{
				disbandUnit(true);

				if (calculateGoldRate() >= 0)
				{
					break;
				}
			}
		}
	}
	else
	{
		setStrike(false);
	}
}


void CvPlayer::doResearch()
{
	bool bForceResearchChoice;
	int iOverflowResearch;

	CyArgsList argsList;
	argsList.add(getID());
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doResearch", argsList.makeFunctionArgs(), &lResult);
	if (lResult == 1)
	{
		return;
	}

	if (isResearch())
	{
		bForceResearchChoice = false;

		if (getCurrentResearch() == NO_TECH)
		{
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				chooseTech();
			}

			if (GC.getGameINLINE().getElapsedGameTurns() > 4)
			{
				AI_chooseResearch();

				bForceResearchChoice = true;
			}
		}

		TechTypes eCurrentTech = getCurrentResearch();
		if (eCurrentTech == NO_TECH)
		{
			int iOverflow = (100 * calculateResearchRate()) / std::max(1, calculateResearchModifier(eCurrentTech));
			changeOverflowResearch(iOverflow);
		}
		else
		{
			iOverflowResearch = (getOverflowResearch() * calculateResearchModifier(eCurrentTech)) / 100;
			setOverflowResearch(0);
			GET_TEAM(getTeam()).changeResearchProgress(eCurrentTech, (calculateResearchRate() + iOverflowResearch), getID());
		}

		if (bForceResearchChoice)
		{
			clearResearchQueue();
		}
	}
}

void CvPlayer::doEspionagePoints()
{
	if (getCommerceRate(COMMERCE_ESPIONAGE) > 0)
	{
		GET_TEAM(getTeam()).changeEspionagePointsEver(getCommerceRate(COMMERCE_ESPIONAGE));

		int iSpending = 0;

		// Divide up Espionage between Teams
		for (int iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
		{
			if (getTeam() != iLoop)
			{
				if (GET_TEAM((TeamTypes)iLoop).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
					{
						iSpending = getEspionageSpending((TeamTypes)iLoop);

						if (iSpending > 0)
						{
							GET_TEAM(getTeam()).changeEspionagePointsAgainstTeam((TeamTypes)iLoop, iSpending);
						}
					}
				}
			}
		}
	}
}

int CvPlayer::getEspionageSpending(TeamTypes eAgainstTeam) const
{
	int iSpendingValue = 0;

	int iTotalPoints = getCommerceRate(COMMERCE_ESPIONAGE);
	int iAvailablePoints = iTotalPoints;

	int iTotalWeight = 0;
	int iBestWeight = 0;

	bool bFoundTeam = false;

	int iLoop;

	// Get sum of all weights to be used later on
	for (iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
	{
		if (getTeam() != iLoop)
		{
			if (GET_TEAM((TeamTypes)iLoop).isAlive())
			{
				if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
				{
					if (iLoop == int(eAgainstTeam))
					{
						bFoundTeam = true;
					}

					int iWeight = getEspionageSpendingWeightAgainstTeam((TeamTypes)iLoop);

					if (iWeight > iBestWeight)
					{
						iBestWeight = iWeight;
					}

					iTotalWeight += iWeight;
				}
			}
		}
	}

	// The player requested is not valid
	if (!bFoundTeam)
	{
		return -1;
	}

	// Split up Espionage Point budget based on weights (if any weights have been assigned)
	if (iTotalWeight > 0)
	{
		for (iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
		{
			if (getTeam() != iLoop)
			{
				if (GET_TEAM((TeamTypes)iLoop).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
					{
						int iChange = (iTotalPoints * getEspionageSpendingWeightAgainstTeam((TeamTypes)iLoop) / iTotalWeight);
						iAvailablePoints -= iChange;

						if (iLoop == int(eAgainstTeam))
						{
							iSpendingValue += iChange;
						}
					}
				}
			}
		}
	}

	// Divide remainder evenly among top Teams
	while (iAvailablePoints > 0)
	{
		for (iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
		{
			if (getTeam() != iLoop)
			{
				if (GET_TEAM((TeamTypes)iLoop).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
					{
						if (getEspionageSpendingWeightAgainstTeam((TeamTypes)iLoop) == iBestWeight)
						{
							if (iLoop == int(eAgainstTeam))
							{
								++iSpendingValue;
							}
							--iAvailablePoints;

							if (iAvailablePoints <= 0)
							{
								break;
							}
						}
					}
				}
			}
		}
	}

	return iSpendingValue;
}

bool CvPlayer::canDoEspionageMission(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pUnit) const
{
	if (getID() == eTargetPlayer || NO_PLAYER == eTargetPlayer)
	{
		return false;
	}

	if (!GET_PLAYER(eTargetPlayer).isAlive() || !GET_TEAM(getTeam()).isHasMet(GET_PLAYER(eTargetPlayer).getTeam()))
	{
		return false;
	}

	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);

	// Need Tech Prereq, if applicable
	if (kMission.getTechPrereq() != NO_TECH)
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)kMission.getTechPrereq()))
		{
			return false;
		}
	}

	int iCost = getEspionageMissionCost(eMission, eTargetPlayer, pPlot, iExtraData, pUnit);
	if (iCost < 0)
	{
		return false;
	}

	if (NO_PLAYER != eTargetPlayer)
	{
		int iEspionagePoints = GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(GET_PLAYER(eTargetPlayer).getTeam());

		if (iEspionagePoints < iCost)
		{
			return false;
		}

		if (iEspionagePoints <= 0)
		{
			return false;
		}
	}

	return true;
}

int CvPlayer::getEspionageMissionCost(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit) const
{
	int iMissionCost = getEspionageMissionBaseCost(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit);

	if (-1 == iMissionCost)
	{
		return -1;
	}

	iMissionCost *= getEspionageMissionCostModifier(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit);
	iMissionCost /= 100;

	// Multiply cost of mission * number of team members
	iMissionCost *= GET_TEAM(getTeam()).getNumMembers();

	return std::max(0, iMissionCost);
}

int CvPlayer::getEspionageMissionBaseCost(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit) const
{
	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);
	int iBaseMissionCost = kMission.getCost();

	// -1 means this mission is disabled
	if (iBaseMissionCost == -1)
	{
		return -1;
	}

	CvCity* pCity = NULL;
	if (NULL != pPlot)
	{
		pCity = pPlot->getPlotCity();
	}

	if (kMission.isSelectPlot())
	{
		if (NULL == pPlot)
		{
			return -1;
		}

		if (!pPlot->isRevealed(getTeam(), false))
		{
			return -1;
		}
	}

	if (NULL == pCity && kMission.isTargetsCity())
	{
		return -1;
	}

	int iMissionCost = -1;

	if (kMission.getStealTreasuryTypes() > 0)
	{
		// Steal Treasury
		int iNumTotalGold = (GET_PLAYER(eTargetPlayer).getGold() * kMission.getStealTreasuryTypes()) / 100;

		if (NULL != pCity)
		{
			iNumTotalGold *= pCity->getPopulation();
			iNumTotalGold /= std::max(1, GET_PLAYER(eTargetPlayer).getTotalPopulation());
		}

		if (iNumTotalGold > 0)
		{
			iMissionCost = (iBaseMissionCost * iNumTotalGold) / 100;
		}
	}
	else if (kMission.getBuyTechCostFactor() > 0)
	{
		// Buy (Steal) Tech
		TechTypes eTech = (TechTypes)iExtraData;
		int iProdCost = MAX_INT;

		if (NO_TECH == eTech)
		{
			for (int iTech = 0; iTech < GC.getNumTechInfos(); ++iTech)
			{
				if (canStealTech(eTargetPlayer, (TechTypes)iTech))
				{
					int iCost = GET_TEAM(getTeam()).getResearchCost((TechTypes)iTech);
					if (iCost < iProdCost)
					{
						iProdCost = iCost;
						eTech = (TechTypes)iTech;
					}
				}
			}
		}
		else
		{
			iProdCost = GET_TEAM(getTeam()).getResearchCost(eTech);
		}

		if (NO_TECH != eTech)
		{
			if (canStealTech(eTargetPlayer, eTech))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getBuyTechCostFactor()) * iProdCost) / 100;
			}
		}
	}
	else if (kMission.getSwitchCivicCostFactor() > 0)
	{
		// Switch Civics
		CivicTypes eCivic = (CivicTypes)iExtraData;

		if (NO_CIVIC == eCivic)
		{
			for (int iCivic = 0; iCivic < GC.getNumCivicInfos(); ++iCivic)
			{
				if (canForceCivics(eTargetPlayer, (CivicTypes)iCivic))
				{
					eCivic = (CivicTypes)iCivic;
					break;
				}
			}
		}

		if (NO_CIVIC != eCivic)
		{
			if (canForceCivics(eTargetPlayer, eCivic))
			{
				iMissionCost = iBaseMissionCost + (kMission.getSwitchCivicCostFactor() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 10000;
			}
		}
	}
	else if (kMission.getSwitchReligionCostFactor() > 0)
	{
		// Switch Religions
		ReligionTypes eReligion = (ReligionTypes)iExtraData;

		if (NO_RELIGION == eReligion)
		{
			for (int iReligion = 0; iReligion < GC.getNumReligionInfos(); ++iReligion)
			{
				if (canForceReligion(eTargetPlayer, (ReligionTypes)iReligion))
				{
					eReligion = (ReligionTypes)iReligion;
					break;
				}
			}
		}

		if (NO_RELIGION != eReligion)
		{
			if (canForceReligion(eTargetPlayer, eReligion))
			{
				iMissionCost = iBaseMissionCost + (kMission.getSwitchReligionCostFactor() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 10000;
			}
		}
	}
	else if (kMission.getDestroyUnitCostFactor() > 0)
	{
		// Destroys Unit
		CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iExtraData);
		int iCost = MAX_INT;

		if (NULL == pUnit)
		{
			if (NULL != pPlot)
			{
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();

				while (pUnitNode != NULL)
				{
					CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);

					if (canSpyDestroyUnit(eTargetPlayer, *pLoopUnit))
					{
						int iValue = getProductionNeeded(pLoopUnit->getUnitType());
						if (iValue < iCost)
						{
							iCost = iValue;
							pUnit = pLoopUnit;
						}
					}
				}

			}
		}
		else
		{
			iCost = getProductionNeeded(pUnit->getUnitType());
		}

		if (NULL != pUnit)
		{
			if (canSpyDestroyUnit(eTargetPlayer, *pUnit))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyUnitCostFactor()) * iCost) / 100;
			}
		}
	}
	else if (kMission.getDestroyProjectCostFactor() > 0)
	{
		ProjectTypes eProject = (ProjectTypes) iExtraData;
		int iCost = MAX_INT;

		if (NO_PROJECT == eProject)
		{
			for (int iProject = 0; iProject < GC.getNumProjectInfos(); ++iProject)
			{
				if (canSpyDestroyProject(eTargetPlayer, (ProjectTypes)iProject))
				{
					int iValue = getProductionNeeded((ProjectTypes)iProject);

					if (iValue < iCost)
					{
						iCost = iValue;
						eProject = (ProjectTypes)iProject;
					}
				}
			}
		}
		else
		{
			iCost = getProductionNeeded(eProject);
		}

		if (NO_PROJECT != eProject)
		{
			if (canSpyDestroyProject(eTargetPlayer, eProject))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyProjectCostFactor()) * iCost) / 100;
			}
		}
	}
	else if (kMission.getDestroyProductionCostFactor() > 0)
	{
		FAssert(NULL != pCity);
		if (NULL != pCity)
		{
			iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyProductionCostFactor()) * pCity->getProduction()) / 100;
		}
	}
	else if (kMission.getBuyUnitCostFactor() > 0)
	{
		// Buy Unit
		CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iExtraData);
		int iCost = MAX_INT;

		if (NULL == pUnit)
		{
			if (NULL != pPlot)
			{
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();

				while (pUnitNode != NULL)
				{
					CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);

					if (canSpyBribeUnit(eTargetPlayer, *pLoopUnit))
					{
						int iValue = getProductionNeeded(pLoopUnit->getUnitType());
						if (iValue < iCost)
						{
							iCost = iValue;
							pUnit = pLoopUnit;
						}
					}
				}

			}
		}
		else
		{
			iCost = getProductionNeeded(pUnit->getUnitType());
		}


		if (NULL != pUnit)
		{
			if (canSpyBribeUnit(eTargetPlayer, *pUnit))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getBuyUnitCostFactor()) * iCost) / 100;
			}
		}
	}
	else if (kMission.getDestroyBuildingCostFactor() > 0)
	{
		BuildingTypes eBuilding = (BuildingTypes) iExtraData;
		int iCost = MAX_INT;

		if (NO_BUILDING == eBuilding)
		{
			for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); ++iBuilding)
			{
				if (NULL != pCity && pCity->getNumRealBuilding((BuildingTypes)iBuilding) > 0)
				{
					if (canSpyDestroyBuilding(eTargetPlayer, (BuildingTypes)iBuilding))
					{
						int iValue = getProductionNeeded((BuildingTypes)iBuilding);

						if (iValue < iCost)
						{
							iCost = iValue;
							eBuilding = (BuildingTypes)iBuilding;
						}
					}
				}
			}
		}
		else
		{
			iCost = getProductionNeeded(eBuilding);
		}

		if (NO_BUILDING != eBuilding)
		{
			if (NULL != pCity && pCity->getNumRealBuilding(eBuilding) > 0)
			{
				if (canSpyDestroyBuilding(eTargetPlayer, eBuilding))
				{
					iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyBuildingCostFactor()) * iCost) / 100;
				}
			}
		}
	}
	else if (kMission.getBuyCityCostFactor() > 0)
	{
		// Buy City
		if (NULL != pCity)
		{
			iMissionCost = iBaseMissionCost + (kMission.getBuyCityCostFactor() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent()) / 10000;
		}
	}
	else if (kMission.getCityInsertCultureCostFactor() > 0)
	{
		// Insert Culture into City
		if (NULL != pPlot && pPlot->getCulture(getID()) > 0)
		{
			int iCultureAmount = kMission.getCityInsertCultureAmountFactor() *  pCity->countTotalCultureTimes100();
			iCultureAmount /= 10000;
			iCultureAmount = std::max(1, iCultureAmount);
			iMissionCost = iBaseMissionCost + (kMission.getCityInsertCultureCostFactor() * iCultureAmount) / 100;
		}
	}
	else if (kMission.isDestroyImprovement())
	{
		if (NULL != pPlot && !pPlot->isCity())
		{
			if (pPlot->getImprovementType() != NO_IMPROVEMENT || pPlot->getRouteType() != NO_ROUTE)
			{
				iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent()) / 100;
			}
		}
	}
	else if (kMission.getCityPoisonWaterCounter() > 0)
	{
		FAssert(NULL != pCity);
		// Cannot poison a city's water supply if it's already poisoned (value is negative when active)
		if (NULL != pCity && pCity->getEspionageHealthCounter() <= 0)
		{
			iMissionCost = iBaseMissionCost;
		}
	}

	// Make city unhappy
	else if (kMission.getCityUnhappinessCounter() > 0)
	{
		FAssert(NULL != pCity);
		// Cannot make a city unhappy if you've already done it (value is negative when active)
		if (NULL != pCity && pCity->getEspionageHappinessCounter() <= 0)
		{
			iMissionCost = iBaseMissionCost;
		}
	}

	// Make city Revolt
	else if (kMission.getCityRevoltCounter() > 0)
	{
		FAssert(NULL != pCity);
		// Cannot make a city revolt if it's already revolting
		if (NULL != pCity && pCity->getOccupationTimer() == 0)
		{
			iMissionCost = iBaseMissionCost;
		}
	}
	else if (kMission.getCounterespionageMod() > 0)
	{
		if (GET_TEAM(getTeam()).getCounterespionageTurnsLeftAgainstTeam(GET_PLAYER(eTargetPlayer).getTeam()) <= 0)
		{
			iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getResearchPercent()) / 100;
		}
	}
	else if (kMission.getPlayerAnarchyCounter() > 0)
	{
		// Player anarchy timer: can't add more turns of anarchy to player already in the midst of it
		if (!GET_PLAYER(eTargetPlayer).isAnarchy())
		{
			iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 100;
		}
	}
	else if (kMission.isPassive())
	{
		iMissionCost = (iBaseMissionCost * (100 + GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam()).getEspionagePointsAgainstTeam(getTeam()))) / 100;
	}
	else
	{
		iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getResearchPercent()) / 100;
	}

	if (iMissionCost < 0)
	{
		return -1;
	}

	return iMissionCost;
}


int CvPlayer::getEspionageMissionCostModifier(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit) const
{
	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);
	int iModifier = 100;

	CvCity* pCity = NULL;
	if (NULL != pPlot)
	{
		pCity = pPlot->getPlotCity();
	}

	if (NO_PLAYER == eTargetPlayer)
	{
		eTargetPlayer = getID();
	}

	if (pCity != NULL && kMission.isTargetsCity())
	{
		// City Population
		iModifier *= 100 + (GC.getDefineINT("ESPIONAGE_CITY_POP_EACH_MOD") * (pCity->getPopulation() - 1));
		iModifier /= 100;

		// Trade Route
		if (pCity->isTradeRoute(getID()))
		{
			iModifier *= 100 + GC.getDefineINT("ESPIONAGE_CITY_TRADE_ROUTE_MOD");
			iModifier /= 100;
		}

		ReligionTypes eReligion = getStateReligion();
		if (NO_RELIGION != eReligion)
		{
			int iReligionModifier = 0;

			// City has Your State Religion
			if (pCity->isHasReligion(eReligion))
			{
				if (GET_PLAYER(eTargetPlayer).getStateReligion() != eReligion)
				{
					iReligionModifier += GC.getDefineINT("ESPIONAGE_CITY_RELIGION_STATE_MOD");
				}

				if (hasHolyCity(eReligion))
				{
					iReligionModifier += GC.getDefineINT("ESPIONAGE_CITY_HOLY_CITY_MOD");
				}
			}

			iModifier *= 100 + iReligionModifier;
			iModifier /= 100;

		}

		// City's culture affects cost
		iModifier *= 100 - (pCity->getCultureTimes100(getID()) * GC.getDefineINT("ESPIONAGE_CULTURE_MULTIPLIER_MOD")) / std::max(1, pCity->getCultureTimes100(eTargetPlayer) + pCity->getCultureTimes100(getID()));
		iModifier /= 100;

		iModifier *= 100 + pCity->getEspionageDefenseModifier();
		iModifier /= 100;
	}

	// Distance mod
	if (pPlot != NULL)
	{
		int iDistance = GC.getMap().maxPlotDistance();

		CvCity* pOurCapital = getCapitalCity();
		if (NULL != pOurCapital)
		{
			if (kMission.isSelectPlot() || kMission.isTargetsCity())
			{
				iDistance = plotDistance(pOurCapital->getX_INLINE(), pOurCapital->getY_INLINE(), pPlot->getX_INLINE(), pPlot->getY_INLINE());
			}
			else
			{
				CvCity* pTheirCapital = GET_PLAYER(eTargetPlayer).getCapitalCity();
				if (NULL != pTheirCapital)
				{
					iDistance = plotDistance(pOurCapital->getX_INLINE(), pOurCapital->getY_INLINE(), pTheirCapital->getX_INLINE(), pTheirCapital->getY_INLINE());
				}
			}
		}

		iModifier *= (iDistance + GC.getMapINLINE().maxPlotDistance()) * GC.getDefineINT("ESPIONAGE_DISTANCE_MULTIPLIER_MOD") / GC.getMapINLINE().maxPlotDistance();
		iModifier /= 100;
	}

	// Spy presence mission cost alteration
	if (NULL != pSpyUnit)
	{
		iModifier *= 100 - (pSpyUnit->getFortifyTurns() * GC.getDefineINT("ESPIONAGE_EACH_TURN_UNIT_COST_DECREASE"));
		iModifier /= 100;
	}

	// My points VS. Your points to mod cost
	int iTargetPoints = GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam()).getEspionagePointsEver();
	int iOurPoints = GET_TEAM(getTeam()).getEspionagePointsEver();
	iModifier *= (GC.getDefineINT("ESPIONAGE_SPENDING_MULTIPLIER") * (2 * iTargetPoints + iOurPoints)) / std::max(1, iTargetPoints + 2 * iOurPoints);
	iModifier /= 100;

	// Counterespionage Mission Mod
	CvTeam& kTargetTeam = GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam());
	if (kTargetTeam.getCounterespionageModAgainstTeam(getTeam()) > 0)
	{
		iModifier *= kTargetTeam.getCounterespionageModAgainstTeam(getTeam());
		iModifier /= 100;
	}
	
/************************************************************************************************/
/* Afforess	                  Start		 07/29/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
    if (pCity != NULL)
	{
		if (pCity == GET_PLAYER(eTargetPlayer).getCapitalCity() && GET_TEAM(getTeam()).isHasEmbassy(GET_PLAYER(eTargetPlayer).getTeam()))
		{
			iModifier *= 100 - GC.getDefineINT("EMBASSY_ESPIONAGE_MISSION_COST_MODIFIER");
			iModifier /= 100;
		}
		
		if (GET_TEAM(getTeam()).isFreeTradeAgreement(GET_PLAYER(eTargetPlayer).getTeam()))
		{
			iModifier *= 100 - GC.getDefineINT("FREE_TRADE_AGREEMENT_ESPIONAGE_MISSION_COST_MODIFIER");
			iModifier /= 100;
		}
	}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

	return iModifier;
}


bool CvPlayer::doEspionageMission(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, CvPlot* pPlot, int iExtraData, CvUnit* pSpyUnit)
{
	if (!canDoEspionageMission(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit))
	{
		return false;
	}

	TeamTypes eTargetTeam = NO_TEAM;
	if (NO_PLAYER != eTargetPlayer)
	{
		eTargetTeam = GET_PLAYER(eTargetPlayer).getTeam();
	}

	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);

	bool bSomethingHappened = false;
	bool bShowExplosion = false;
	CvWString szBuffer;
	int iMissionCost = getEspionageMissionCost(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit);


	//////////////////////////////
	// Destroy Improvement

	if (kMission.isDestroyImprovement())
	{
		if (NULL != pPlot)
		{
			// Blow it up
			if (pPlot->getImprovementType() != NO_IMPROVEMENT)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED", GC.getImprovementInfo(pPlot->getImprovementType()).getDescription()).GetCString();
				pPlot->setImprovementType((ImprovementTypes)(GC.getImprovementInfo(pPlot->getImprovementType()).getImprovementPillage()));
				bSomethingHappened = true;
			}
			else if (pPlot->getRouteType() != NO_ROUTE)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED", GC.getRouteInfo(pPlot->getRouteType()).getDescription()).GetCString();
				pPlot->setRouteType(NO_ROUTE, true);
				bSomethingHappened = true;
			}

			if (bSomethingHappened)
			{
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Building

	if (kMission.getDestroyBuildingCostFactor() > 0)
	{
		BuildingTypes eTargetBuilding = (BuildingTypes)iExtraData;

		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED_IN", GC.getBuildingInfo(eTargetBuilding).getDescription(), pCity->getNameKey()).GetCString();
				pCity->setNumRealBuilding(eTargetBuilding, pCity->getNumRealBuilding(eTargetBuilding) - 1);

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Project

	if (kMission.getDestroyProjectCostFactor() > 0)
	{
		ProjectTypes eTargetProject = (ProjectTypes)iExtraData;

		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED_IN", GC.getProjectInfo(eTargetProject).getDescription(), pCity->getNameKey()).GetCString();
				GET_TEAM(eTargetTeam).changeProjectCount(eTargetProject, -1);

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Production

	if (kMission.getDestroyProductionCostFactor() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_PRODUCTION_DESTROYED_IN", pCity->getProductionName(), pCity->getNameKey());
				pCity->setProduction(0);

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Unit

	if (kMission.getDestroyUnitCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iTargetUnitID = iExtraData;

			CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iTargetUnitID);

			if (NULL != pUnit)
			{
				FAssert(pUnit->plot() == pPlot);
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED", pUnit->getNameKey()).GetCString();
				logBBAI("    Killing %S -- destroyed unit by espionage (Unit %d - plot: %d, %d)",
						pUnit->getName().GetCString(), pUnit->getID(), pUnit->getX(), pUnit->getY());
				pUnit->kill(false, getID());

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Buy Unit

	if (kMission.getBuyUnitCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iTargetUnitID = iExtraData;

			CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iTargetUnitID);

			if (NULL != pUnit)
			{
				FAssert(pUnit->plot() == pPlot);

				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_UNIT_BOUGHT", pUnit->getNameKey()).GetCString();

				UnitTypes eUnitType = pUnit->getUnitType();
				int iX = pUnit->getX_INLINE();
				int iY = pUnit->getY_INLINE();
				logBBAI("    Killing %S -- Bought unit by espionage (Unit %d - plot: %d, %d)",
						pUnit->getName().GetCString(), pUnit->getID(), pUnit->getX(), pUnit->getY());
				pUnit->kill(false, getID());
				initUnit(eUnitType, iX, iY, NO_UNITAI);

				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Buy City

	if (kMission.getBuyCityCostFactor() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_BOUGHT", pCity->getNameKey()).GetCString();
				acquireCity(pCity, false, true, true);

				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Insert Culture into City

	if (kMission.getCityInsertCultureCostFactor() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_CULTURE_INSERTED", pCity->getNameKey()).GetCString();

				int iCultureAmount = kMission.getCityInsertCultureAmountFactor() * pCity->countTotalCultureTimes100();
				iCultureAmount /= 10000;
				iCultureAmount = std::max(1, iCultureAmount);

				int iNumTurnsApplied = (GC.getDefineINT("GREAT_WORKS_CULTURE_TURNS") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getUnitGreatWorkPercent()) / 100;

				for (int i = 0; i < iNumTurnsApplied; ++i)
				{
					pCity->changeCulture(getID(), iCultureAmount / iNumTurnsApplied, true, true);
				}

				if (iNumTurnsApplied > 0)
				{
					pCity->changeCulture(getID(), iCultureAmount % iNumTurnsApplied, false, true);
				}

				bSomethingHappened = true;
			}

		}
	}

	//////////////////////////////
	// Poison City's Water Supply

	if (kMission.getCityPoisonWaterCounter() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_POISONED", pCity->getNameKey()).GetCString();
				pCity->changeEspionageHealthCounter(kMission.getCityPoisonWaterCounter());

				bShowExplosion = true;
				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Make city Unhappy

	if (kMission.getCityUnhappinessCounter() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_UNHAPPY", pCity->getNameKey()).GetCString();
				pCity->changeEspionageHappinessCounter(kMission.getCityUnhappinessCounter());

				bShowExplosion = true;
				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Make city Revolt

	if (kMission.getCityRevoltCounter() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_REVOLT", pCity->getNameKey()).GetCString();
				pCity->changeCultureUpdateTimer(kMission.getCityRevoltCounter());
				pCity->changeOccupationTimer(kMission.getCityRevoltCounter());

				bSomethingHappened = true;
				bShowExplosion = true;

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/12/10                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
				if( gUnitLogLevel >= 2 )
				{
					logBBAI("      Spy for player %d (%S) causes revolt in %S, owned by %S (%d)", getID(), getCivilizationDescription(0), pCity->getName().GetCString(), GET_PLAYER(pCity->getOwner()).getCivilizationDescription(0), pCity->getOwner() );
				}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
			}
		}
	}

	//////////////////////////////
	// Steal Treasury

	if (kMission.getStealTreasuryTypes() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iNumTotalGold = (GET_PLAYER(eTargetPlayer).getGold() * kMission.getStealTreasuryTypes()) / 100;

			if (NULL != pPlot)
			{
				CvCity* pCity = pPlot->getPlotCity();

				if (NULL != pCity)
				{
					iNumTotalGold *= pCity->getPopulation();
					iNumTotalGold /= std::max(1, GET_PLAYER(eTargetPlayer).getTotalPopulation());
				}
			}

			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_STEAL_TREASURY").GetCString();
			changeGold(iNumTotalGold);
			if (NO_PLAYER != eTargetPlayer)
			{
				GET_PLAYER(eTargetPlayer).changeGold(-iNumTotalGold);
			}

			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Buy (Steal) Tech

	if (kMission.getBuyTechCostFactor() > 0)
	{
		int iTech = iExtraData;

		szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_TECH_BOUGHT", GC.getTechInfo((TechTypes) iTech).getDescription()).GetCString();
		GET_TEAM(getTeam()).setHasTech((TechTypes) iTech, true, getID(), false, true);
		GET_TEAM(getTeam()).setNoTradeTech((TechTypes)iTech, true);

		bSomethingHappened = true;
	}

	//////////////////////////////
	// Switch Civic

	if (kMission.getSwitchCivicCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iCivic = iExtraData;

			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SWITCH_CIVIC", GC.getCivicInfo((CivicTypes) iCivic).getDescription()).GetCString();
			GET_PLAYER(eTargetPlayer).setCivics((CivicOptionTypes) GC.getCivicInfo((CivicTypes) iCivic).getCivicOptionType(), (CivicTypes) iCivic);
			GET_PLAYER(eTargetPlayer).setRevolutionTimer(std::max(1, ((100 + GET_PLAYER(eTargetPlayer).getAnarchyModifier()) * GC.getDefineINT("MIN_REVOLUTION_TURNS")) / 100));
			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Switch Religion

	if (kMission.getSwitchReligionCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iReligion = iExtraData;

			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SWITCH_RELIGION", GC.getReligionInfo((ReligionTypes) iReligion).getDescription()).GetCString();
			GET_PLAYER(eTargetPlayer).setLastStateReligion((ReligionTypes) iReligion);
			GET_PLAYER(eTargetPlayer).setConversionTimer(std::max(1, ((100 + GET_PLAYER(eTargetPlayer).getAnarchyModifier()) * GC.getDefineINT("MIN_CONVERSION_TURNS")) / 100));
			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Player Anarchy

	if (kMission.getPlayerAnarchyCounter() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iTurns = (kMission.getPlayerAnarchyCounter() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 100;
			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_PLAYER_ANARCHY").GetCString();
			GET_PLAYER(eTargetPlayer).changeAnarchyTurns(iTurns);

			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Counterespionage

	if (kMission.getCounterespionageNumTurns() > 0 && kMission.getCounterespionageMod() > 0)
	{
		szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_COUNTERESPIONAGE").GetCString();

		if (NO_TEAM != eTargetTeam)
		{
			int iTurns = (kMission.getCounterespionageNumTurns() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getResearchPercent()) / 100;
			GET_TEAM(getTeam()).changeCounterespionageTurnsLeftAgainstTeam(eTargetTeam, iTurns);
			GET_TEAM(getTeam()).changeCounterespionageModAgainstTeam(eTargetTeam, kMission.getCounterespionageMod());

			bSomethingHappened = true;

		}
	}

	int iHave = 0;
	if (NO_TEAM != eTargetTeam)
	{
		iHave = GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(eTargetTeam);

		if (bSomethingHappened)
		{
			GET_TEAM(getTeam()).changeEspionagePointsAgainstTeam(eTargetTeam, -iMissionCost);
		}
	}

	if (bShowExplosion)
	{
		if (pPlot)
		{
			if (pPlot->isVisible(GC.getGame().getActiveTeam(), false))
			{
				EffectTypes eEffect = GC.getEntityEventInfo(GC.getMissionInfo(MISSION_BOMBARD).getEntityEvent()).getEffectType();
				gDLL->getEngineIFace()->TriggerEffect(eEffect, pPlot->getPoint(), (float)(GC.getASyncRand().get(360)));
				gDLL->getInterfaceIFace()->playGeneralSound("AS3D_UN_CITY_EXPLOSION", pPlot->getPoint());
			}
		}
	}

	if (bSomethingHappened)
	{
		int iX = -1;
		int iY = -1;
		if (NULL != pPlot)
		{
			iX = pPlot->getX_INLINE();
			iY = pPlot->getY_INLINE();
		}

		gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_ESPIONAGE_MISSION_PERFORMED"), "AS2D_POSITIVE_DINK", MESSAGE_TYPE_INFO, ARTFILEMGR.getInterfaceArtInfo("ESPIONAGE_BUTTON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_GREEN"), iX, iY, true, true);
	}
	else if (getID() == GC.getGameINLINE().getActivePlayer())
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
		if (iHave < iMissionCost)
		{
			pInfo->setText(gDLL->getText("TXT_KEY_ESPIONAGE_TOO_EXPENSIVE", iMissionCost, iHave));
		}
		else
		{
			pInfo->setText(gDLL->getText("TXT_KEY_ESPIONAGE_CANNOT_DO_MISSION"));
		}

		addPopup(pInfo);
	}

	if (bSomethingHappened && !szBuffer.empty())
	{
		int iX = -1;
		int iY = -1;
		if (NULL != pPlot)
		{
			iX = pPlot->getX_INLINE();
			iY = pPlot->getY_INLINE();
		}

		if (NO_PLAYER != eTargetPlayer)
		{
			gDLL->getInterfaceIFace()->addMessage(eTargetPlayer, true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DEAL_CANCELLED", MESSAGE_TYPE_INFO, ARTFILEMGR.getInterfaceArtInfo("ESPIONAGE_BUTTON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), iX, iY, true, true);
		}
	}

	return bSomethingHappened;
}

int CvPlayer::getEspionageSpendingWeightAgainstTeam(TeamTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiEspionageSpendingWeightAgainstTeam[eIndex];
}

void CvPlayer::setEspionageSpendingWeightAgainstTeam(TeamTypes eIndex, int iValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssert(iValue >= 0);

	iValue = std::min(std::max(0, iValue), 99);

	if (iValue != getEspionageSpendingWeightAgainstTeam(eIndex))
	{
		m_aiEspionageSpendingWeightAgainstTeam[eIndex] = iValue;

		gDLL->getInterfaceIFace()->setDirty(Espionage_Advisor_DIRTY_BIT, true);
	}
}

void CvPlayer::changeEspionageSpendingWeightAgainstTeam(TeamTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");

	setEspionageSpendingWeightAgainstTeam(eIndex, getEspionageSpendingWeightAgainstTeam(eIndex) + iChange);
}

void CvPlayer::doAdvancedStartAction(AdvancedStartActionTypes eAction, int iX, int iY, int iData, bool bAdd)
{
	if (getAdvancedStartPoints() < 0)
	{
		return;
	}

	CvPlot* pPlot = GC.getMap().plot(iX, iY);

	if (0 == getNumCities())
	{
		switch (eAction)
		{
		case ADVANCEDSTARTACTION_EXIT:
			//Try to build this player's empire
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setBusy(true);
			}
			AI_doAdvancedStart(true);
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setBusy(false);
			}
			break;
		case ADVANCEDSTARTACTION_AUTOMATE:
		case ADVANCEDSTARTACTION_CITY:
			break;
		default:
			// The first action must be to place a city
			// so players can lose by spending everything
			return;
		}
	}

	switch (eAction)
	{
	case ADVANCEDSTARTACTION_EXIT:
		changeGold(getAdvancedStartPoints());
		setAdvancedStartPoints(-1);
		if (GC.getGameINLINE().getActivePlayer() == getID())
		{
			gDLL->getInterfaceIFace()->setInAdvancedStart(false);
		}

		if (isHuman())
		{
			int iLoop;
			for (CvCity* pCity = firstCity(&iLoop); NULL != pCity; pCity = nextCity(&iLoop))
			{
				pCity->chooseProduction();
			}

			chooseTech();

			if (canRevolution(NULL))
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHANGECIVIC);
				if (NULL != pInfo)
				{
					gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
				}
			}
		}
		break;
	case ADVANCEDSTARTACTION_AUTOMATE:
		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setBusy(true);
		}
		AI_doAdvancedStart(true);
		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setBusy(false);
		}
		break;
	case ADVANCEDSTARTACTION_UNIT:
		{
			if(pPlot == NULL)
				return;

			UnitTypes eUnit = (UnitTypes) iData;
			int iCost = getAdvancedStartUnitCost(eUnit, bAdd, pPlot);

			if (bAdd && iCost < 0)
			{
				return;
			}

			// Add unit to the map
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					// lfgr 01/2022: Try to add at least one defender per city
					UnitAITypes eUnitAI = NO_UNITAI;
					if( GC.getUnitInfo( eUnit ).getUnitAIType( UNITAI_CITY_DEFENSE )
							&& pPlot->plotCount( PUF_isUnitAIType, UNITAI_CITY_DEFENSE, -1, getIDINLINE() ) == 0 )
					{
						eUnitAI = UNITAI_CITY_DEFENSE;
					}

					CvUnit* pUnit = initUnit(eUnit, iX, iY, eUnitAI);
					if (NULL != pUnit)
					{
						pUnit->finishMoves();
						changeAdvancedStartPoints(-iCost);
					}
				}
			}

			// Remove unit from the map
			else
			{
				// If cost is -1 we already know this unit isn't present
				if (iCost != -1)
				{
					CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
					while (pUnitNode != NULL)
					{
						CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
						pUnitNode = pPlot->nextUnitNode(pUnitNode);

						if (pLoopUnit->getUnitType() == eUnit)
						{
							logBBAI("    Killing %S -- Removed advanced start unit (Unit %d - plot: %d, %d)",
									pLoopUnit->getName().GetCString(), pLoopUnit->getID(), pLoopUnit->getX(), pLoopUnit->getY());
							pLoopUnit->kill(false);
							changeAdvancedStartPoints(iCost);
							return;
						}
					}
				}

				// Proper unit not found above, delete first found
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
				if (pUnitNode != NULL)
				{
					CvUnit* pUnit = ::getUnit(pUnitNode->m_data);

					iCost = getAdvancedStartUnitCost(pUnit->getUnitType(), false);
					FAssertMsg(iCost != -1, "If this is -1 then that means it's going to try to delete a unit which shouldn't exist");
					logBBAI("    Killing %S -- Removed advanced start unit (Unit %d - plot: %d, %d)",
							pUnit->getName().GetCString(), pUnit->getID(), pUnit->getX(), pUnit->getY());
					pUnit->kill(false);
					changeAdvancedStartPoints(iCost);
				}
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_CITY:
		{
			if(pPlot == NULL)
				return;

			int iCost = getAdvancedStartCityCost(bAdd, pPlot);

			if (iCost < 0)
			{
				return;
			}

			// Add City to the map
			if (bAdd)
			{
				if (0 == getNumCities())
				{
					PlayerTypes eClosestPlayer = NO_PLAYER;
					int iMinDistance = MAX_INT;
					for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
					{
						CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);
						if (kPlayer.isAlive())
						{
							if (kPlayer.getTeam() == getTeam())
							{
								if (0 == kPlayer.getNumCities())
								{
									FAssert(kPlayer.getStartingPlot() != NULL);
									int iDistance = plotDistance(iX, iY, kPlayer.getStartingPlot()->getX_INLINE(), kPlayer.getStartingPlot()->getY_INLINE());
									if (iDistance < iMinDistance)
									{
										eClosestPlayer = kPlayer.getID();
										iMinDistance = iDistance;
									}
								}
							}
						}
					}
					FAssertMsg(eClosestPlayer != NO_PLAYER, "Self at a minimum should always be valid");
					if (eClosestPlayer != getID())
					{
						CvPlot* pTempPlot = GET_PLAYER(eClosestPlayer).getStartingPlot();
						GET_PLAYER(eClosestPlayer).setStartingPlot(getStartingPlot(), false);
						setStartingPlot(pTempPlot, false);
					}
				}
				if (getAdvancedStartPoints() >= iCost || 0 == getNumCities())
				{
					found(iX, iY);
					changeAdvancedStartPoints(-std::min(iCost, getAdvancedStartPoints()));
					GC.getGameINLINE().updateColoredPlots();
					CvCity* pCity = pPlot->getPlotCity();
					if (pCity != NULL)
					{
						if (pCity->getPopulation() > 1)
						{
							pCity->setFood(pCity->growthThreshold() / 2);
						}
					}
				}
			}

			// Remove City from the map
			else
			{
				pPlot->setRouteType(NO_ROUTE, true);
				pPlot->getPlotCity()->kill(true);
				pPlot->setImprovementType(NO_IMPROVEMENT);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_POP:
		{
			if(pPlot == NULL)
				return;

			CvCity* pCity = pPlot->getPlotCity();

			if (pCity != NULL)
			{
				int iCost = getAdvancedStartPopCost(bAdd, pCity);

				if (iCost < 0)
				{
					return;
				}

				bool bPopChanged = false;
				if (bAdd)
				{
					if (getAdvancedStartPoints() >= iCost)
					{
						pCity->changePopulation(1);
						changeAdvancedStartPoints(-iCost);
						bPopChanged = true;
					}
				}
				else
				{
					pCity->changePopulation(-1);
					changeAdvancedStartPoints(iCost);
					bPopChanged = true;
				}

				if (bPopChanged)
				{
					pCity->setHighestPopulation(pCity->getPopulation());
					if (pCity->getPopulation() == 1)
					{
						pCity->setFood(0);
						pCity->setFoodKept(0);
					}
					else if (pCity->getPopulation() > 1)
					{
						pCity->setFood(pCity->growthThreshold() / 2);
						pCity->setFoodKept((pCity->getFood() * pCity->getMaxFoodKeptPercent()) / 100);
					}
				}
			}
		}
		break;
	case ADVANCEDSTARTACTION_CULTURE:
		{
			if(pPlot == NULL)
				return;

			CvCity* pCity = pPlot->getPlotCity();

			if (pCity != NULL)
			{
				int iCost = getAdvancedStartCultureCost(bAdd, pCity);

				if (iCost < 0)
				{
					return;
				}

				// Add Culture to the City
				if (bAdd)
				{
					if (getAdvancedStartPoints() >= iCost)
					{
						pCity->setCulture(getID(), pCity->getCultureThreshold(), true, true);
						changeAdvancedStartPoints(-iCost);
					}
				}

				// Remove Culture from the city
				else
				{
					CultureLevelTypes eLevel = (CultureLevelTypes)std::max(0, pCity->getCultureLevel() - 1);
					pCity->setCulture(getID(), CvCity::getCultureThreshold(eLevel), true, true);
					changeAdvancedStartPoints(iCost);
				}
			}
		}
		break;
	case ADVANCEDSTARTACTION_BUILDING:
		{
			if(pPlot == NULL)
				return;

			CvCity* pCity = pPlot->getPlotCity();

			if (pCity != NULL)
			{
				BuildingTypes eBuilding = (BuildingTypes) iData;
				int iCost = getAdvancedStartBuildingCost(eBuilding, bAdd, pCity);

				if (iCost < 0)
				{
					return;
				}

				// Add Building to the City
				if (bAdd)
				{
					if (getAdvancedStartPoints() >= iCost)
					{
						pCity->setNumRealBuilding(eBuilding, pCity->getNumRealBuilding(eBuilding)+1);
						changeAdvancedStartPoints(-iCost);
						if (GC.getBuildingInfo(eBuilding).getFoodKept() != 0)
						{
							pCity->setFoodKept((pCity->getFood() * pCity->getMaxFoodKeptPercent()) / 100);
						}
					}
				}

				// Remove Building from the map
				else
				{
					pCity->setNumRealBuilding(eBuilding, pCity->getNumRealBuilding(eBuilding)-1);
					changeAdvancedStartPoints(iCost);
					if (GC.getBuildingInfo(eBuilding).getFoodKept() != 0)
					{
						pCity->setFoodKept((pCity->getFood() * pCity->getMaxFoodKeptPercent()) / 100);
					}
				}
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_ROUTE:
		{
			if(pPlot == NULL)
				return;

			RouteTypes eRoute = (RouteTypes) iData;
			int iCost = getAdvancedStartRouteCost(eRoute, bAdd, pPlot);

			if (bAdd && iCost < 0)
			{
				return;
			}

			// Add Route to the plot
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					pPlot->setRouteType(eRoute, true);
					changeAdvancedStartPoints(-iCost);
				}
			}

			// Remove Route from the Plot
			else
			{
				if (pPlot->getRouteType() != eRoute)
				{
					eRoute = pPlot->getRouteType();
					iCost = getAdvancedStartRouteCost(eRoute, bAdd);
				}

				if (iCost < 0)
				{
					return;
				}

				pPlot->setRouteType(NO_ROUTE, true);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_IMPROVEMENT:
		{
			if(pPlot == NULL)
				return;

			ImprovementTypes eImprovement = (ImprovementTypes) iData;
			int iCost = getAdvancedStartImprovementCost(eImprovement, bAdd, pPlot);

			if (bAdd && iCost < 0)
			{
				return;
			}

			// Add Improvement to the plot
			if (bAdd)
			{
				// lfgr 11/2021: Refund overwritten improvement
				int iOldCost = getAdvancedStartImprovementCost(pPlot->getImprovementType(), false, pPlot);
				iOldCost = std::max( 0, iOldCost ); // Could be -1 if 

				if (getAdvancedStartPoints() + iOldCost >= iCost) // lfgr 11/2021: Refund overwritten improvement
				{
					if (pPlot->getFeatureType() != NO_FEATURE)
					{
						for (int iI = 0; iI < GC.getNumBuildInfos(); ++iI)
						{
							ImprovementTypes eLoopImprovement = ((ImprovementTypes)(GC.getBuildInfo((BuildTypes)iI).getImprovement()));

							if (eImprovement == eLoopImprovement)
							{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/02/21
//*** Elvish civilization can see the amount of production from forest chopping.
/*
								if (GC.getBuildInfo((BuildTypes)iI).isFeatureRemove(pPlot->getFeatureType()) && canBuild(pPlot, (BuildTypes)iI)

//FfH: Added by Kael 11/11/2007
								  && (!GC.getCivilizationInfo(getCivilizationType()).isMaintainFeatures(pPlot->getFeatureType()) || GC.getBuildInfo((BuildTypes)iI).getImprovement() == NO_IMPROVEMENT)
//FfH: End Add

								  )
*/
								if (pPlot->isFeatureRemove((BuildTypes)iI) && canBuild(pPlot, (BuildTypes)iI))
//<<<<Unofficial Bug Fix: End Modify
								{
									pPlot->setFeatureType(NO_FEATURE);
									break;
								}
							}
						}
					}

					pPlot->setImprovementType(eImprovement);

					changeAdvancedStartPoints(iOldCost-iCost); // lfgr 11/2021: Refund overwritten improvement
				}
			}

			// Remove Improvement from the Plot
			else
			{
				if (pPlot->getImprovementType() != eImprovement)
				{
					eImprovement = pPlot->getImprovementType();
					iCost = getAdvancedStartImprovementCost(eImprovement, bAdd, pPlot);
				}

				if (iCost < 0)
				{
					return;
				}

				pPlot->setImprovementType(NO_IMPROVEMENT);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_TECH:
		{
			TechTypes eTech = (TechTypes) iData;
			int iCost = getAdvancedStartTechCost(eTech, bAdd);

			if (iCost < 0)
			{
				return;
			}

			// Add Tech to team
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					GET_TEAM(getTeam()).setHasTech(eTech, true, getID(), false, false);
					changeAdvancedStartPoints(-iCost);
				}
			}

			// Remove Tech from the Team
			else
			{
				GET_TEAM(getTeam()).setHasTech(eTech, false, getID(), false, false);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_VISIBILITY:
		{
			if(pPlot == NULL)
				return;

			int iCost = getAdvancedStartVisibilityCost(bAdd, pPlot);

			if (iCost < 0)
			{
				return;
			}

			// Add Visibility to the plot
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					pPlot->setRevealed(getTeam(), true, true, NO_TEAM, true);
					changeAdvancedStartPoints(-iCost);
				}
			}

			// Remove Visibility from the Plot
			else
			{
				pPlot->setRevealed(getTeam(), false, true, NO_TEAM, true);
				changeAdvancedStartPoints(iCost);
			}

			// lfgr fix 11/2021
			GC.getGameINLINE().updateColoredPlots();
		}
		break;
	default:
		FAssert(false);
		break;
	}
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing a unit
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartUnitCost(UnitTypes eUnit, bool bAdd, CvPlot* pPlot) const
{
	int iLoop;
	int iNumUnitType = 0;

	if (0 == getNumCities())
	{
		return -1;
	}

	CvUnitInfo& kUnitInfo = GC.getUnitInfo(eUnit);

	// lfgr fix 05/2020: If we remove the unit tell this getProductionNeeded to make sure we don't refund too much
	int iCost = (getProductionNeeded(eUnit, !bAdd ) * kUnitInfo.getAdvancedStartCost()) / 100;
	if (iCost < 0)
	{
		return -1;
	}

	if (NULL == pPlot)
	{
		if (bAdd)
		{
			bool bValid = false;
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->canTrain(eUnit))
				{
					bValid = true;
					break;
				}
			}

			if (!bValid)
			{
				return -1;
			}
		}
	}
	else
	{
		CvCity* pCity = NULL;

		if (0 == GC.getDefineINT("ADVANCED_START_ALLOW_UNITS_OUTSIDE_CITIES"))
		{
			pCity = pPlot->getPlotCity();

			if (NULL == pCity || pCity->getOwnerINLINE() != getID())
			{
				return -1;
			}

			iCost *= 100;
			iCost /= std::max(1, 100 + pCity->getProductionModifier(eUnit));
		}
		else
		{
			if (pPlot->getOwnerINLINE() != getID())
			{
				return -1;
			}

			iCost *= 100;
			iCost /= std::max(1, 100 + getProductionModifier(eUnit));
		}


		if (bAdd)
		{
			int iMaxUnitsPerCity = GC.getDefineINT("ADVANCED_START_MAX_UNITS_PER_CITY");
			if (iMaxUnitsPerCity >= 0)
			{
				if (kUnitInfo.isMilitarySupport() && getNumMilitaryUnits() >= iMaxUnitsPerCity * getNumCities())
				{
					return -1;
				}
			}

			if (NULL != pCity)
			{
				if (!pCity->canTrain(eUnit))
				{
					return -1;
				}
			}
			else
			{
				if (!pPlot->canTrain(eUnit, false, false))
				{
					return -1;
				}

				if (pPlot->isImpassable() && !kUnitInfo.isCanMoveImpassable())
				{
					return -1;
				}

				if (pPlot->getFeatureType() != NO_FEATURE)
				{
					if (kUnitInfo.getFeatureImpassable(pPlot->getFeatureType()))
					{
						TechTypes eTech = (TechTypes)kUnitInfo.getFeaturePassableTech(pPlot->getFeatureType());
						if (NO_TECH == eTech || !GET_TEAM(getTeam()).isHasTech(eTech))
						{
							return -1;
						}
					}
				}
				else
				{
					if (kUnitInfo.getTerrainImpassable(pPlot->getTerrainType()))
					{
						TechTypes eTech = (TechTypes)kUnitInfo.getTerrainPassableTech(pPlot->getTerrainType());
						if (NO_TECH == eTech || !GET_TEAM(getTeam()).isHasTech(eTech))
						{
							return -1;
						}
					}
				}
			}
		}
		// Must be this unit at plot in order to remove
		else
		{
			bool bUnitFound = false;

			CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
			while (pUnitNode != NULL)
			{
				CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
				pUnitNode = pPlot->nextUnitNode(pUnitNode);

				if (pLoopUnit->getUnitType() == eUnit)
				{
					bUnitFound = true;
				}
			}

			if (!bUnitFound)
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != kUnitInfo.getAdvancedStartCostIncrease())
	{
		for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (pLoopUnit->getUnitType() == eUnit)
			{
				++iNumUnitType;
			}
		}

		if (!bAdd)
		{
			--iNumUnitType;
		}

		if (iNumUnitType > 0)
		{
			iCost *= 100 + kUnitInfo.getAdvancedStartCostIncrease() * iNumUnitType;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing a City
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartCityCost(bool bAdd, CvPlot* pPlot) const
{
	int iNumCities = getNumCities();

	int iCost = getNewCityProductionValue();

	if (iCost < 0)
	{
		return -1;
	}

	// Valid plot?
	if (pPlot != NULL)
	{
		// Need valid plot to found on if adding
		if (bAdd)
		{
			if (!canFound(pPlot->getX(), pPlot->getY(), false))
			{
				return -1;
			}
		}
		// Need your own city present to remove
		else
		{
			if (pPlot->isCity())
			{
				if (pPlot->getPlotCity()->getOwnerINLINE() != getID())
				{
					return -1;
				}
			}
			else
			{
				return -1;
			}
		}

		// Is there a distance limit on how far a city can be placed from a player's start/another city?
		if (GC.getDefineINT("ADVANCED_START_CITY_PLACEMENT_MAX_RANGE") > 0)
		{
			PlayerTypes eClosestPlayer = NO_PLAYER;
			int iClosestDistance = MAX_INT;

			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);

				if (kPlayer.isAlive())
				{
					CvPlot* pStartingPlot = kPlayer.getStartingPlot();

					if (NULL != pStartingPlot)
					{
						int iDistance = ::plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE());
						if (iDistance <= GC.getDefineINT("ADVANCED_START_CITY_PLACEMENT_MAX_RANGE"))
						{
							if (iDistance < iClosestDistance || (iDistance == iClosestDistance && getTeam() != kPlayer.getTeam()))
							{
								iClosestDistance = iDistance;
								eClosestPlayer = kPlayer.getID();
							}
						}
					}
				}
			}

			if (NO_PLAYER == eClosestPlayer || GET_PLAYER(eClosestPlayer).getTeam() != getTeam())
			{
				return -1;
			}
			//Only allow founding a city at someone elses start point if
			//We have no cities and they have no cities.
			if ((getID() != eClosestPlayer) && ((getNumCities() > 0) || (GET_PLAYER(eClosestPlayer).getNumCities() > 0)))
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getDefineINT("ADVANCED_START_CITY_COST_INCREASE"))
	{
		if (!bAdd)
		{
			--iNumCities;
		}

		if (iNumCities > 0)
		{
			iCost *= 100 + GC.getDefineINT("ADVANCED_START_CITY_COST_INCREASE") * iNumCities;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Population
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartPopCost(bool bAdd, CvCity* pCity) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iCost = (getGrowthThreshold(1) * GC.getDefineINT("ADVANCED_START_POPULATION_COST")) / 100;

	if (NULL != pCity)
	{
		if (pCity->getOwnerINLINE() != getID())
		{
			return -1;
		}

		int iPopulation = pCity->getPopulation();

		// Need to have Population to remove it
		if (!bAdd)
		{
			--iPopulation;

			if (iPopulation < GC.getDefineINT("INITIAL_CITY_POPULATION") + GC.getEraInfo(GC.getGameINLINE().getStartEra()).getFreePopulation())
			{
				return -1;
			}
		}

		iCost = (getGrowthThreshold(iPopulation) * GC.getDefineINT("ADVANCED_START_POPULATION_COST")) / 100;

		// Increase cost if the XML defines that additional Pop will cost more
		if (0 != GC.getDefineINT("ADVANCED_START_POPULATION_COST_INCREASE"))
		{
			--iPopulation;

			if (iPopulation > 0)
			{
				iCost *= 100 + GC.getDefineINT("ADVANCED_START_POPULATION_COST_INCREASE") * iPopulation;
				iCost /= 100;
			}
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Culture
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartCultureCost(bool bAdd, CvCity* pCity) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iCost = GC.getDefineINT("ADVANCED_START_CULTURE_COST");
	if (iCost < 0)
	{
		return -1;
	}

	if (NULL != pCity)
	{
		if (pCity->getOwnerINLINE() != getID())
		{
			return -1;
		}

		// Need to have enough culture to remove it
		if (!bAdd)
		{
			if (pCity->getCultureLevel() <= 0)
			{
				return -1;
			}
		}

		int iCulture;
		if (bAdd)
		{
			iCulture = CvCity::getCultureThreshold((CultureLevelTypes)(pCity->getCultureLevel() + 1)) - pCity->getCulture(getID());
		}
		else
		{
			iCulture = pCity->getCulture(getID()) - CvCity::getCultureThreshold((CultureLevelTypes)(pCity->getCultureLevel() - 1));
		}

		iCost *= iCulture;
		iCost /= std::max(1, GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryPercent());
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing a Building from a city
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartBuildingCost(BuildingTypes eBuilding, bool bAdd, CvCity* pCity) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumBuildingType = 0;

	int iCost = (getProductionNeeded(eBuilding) * GC.getBuildingInfo(eBuilding).getAdvancedStartCost()) / 100;

	if (iCost < 0)
	{
		return -1;
	}

	if (GC.getBuildingInfo(eBuilding).getFreeStartEra() != NO_ERA && GC.getGameINLINE().getStartEra() >=  GC.getBuildingInfo(eBuilding).getFreeStartEra())
	{
		// you get this building for free
		return -1;
	}

	if (NULL == pCity)
	{
		if (bAdd)
		{
			bool bValid = false;
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->canConstruct(eBuilding))
				{
					bValid = true;
					break;
				}
			}

			if (!bValid)
			{
				return -1;
			}
		}
	}
	if (NULL != pCity)
	{
		if (pCity->getOwnerINLINE() != getID())
		{
			return -1;
		}

		iCost *= 100;
		iCost /= std::max(1, 100 + pCity->getProductionModifier(eBuilding));

		if (bAdd)
		{
			if (!pCity->canConstruct(eBuilding, true, false, false))
			{
				return -1;
			}
		}
		else
		{
			if (pCity->getNumRealBuilding(eBuilding) <= 0)
			{
				return -1;
			}

			// Check other buildings in this city and make sure none of them require this one

			// Loop through Buildings to see which are present
			for (int iBuildingLoop = 0; iBuildingLoop < GC.getNumBuildingInfos(); iBuildingLoop++)
			{
				BuildingTypes eBuildingLoop = (BuildingTypes) iBuildingLoop;

				if (pCity->getNumBuilding(eBuildingLoop) > 0)
				{
					// Loop through present Building's requirements
					for (int iBuildingClassPrereqLoop = 0; iBuildingClassPrereqLoop < GC.getNumBuildingClassInfos(); iBuildingClassPrereqLoop++)
					{
						if (GC.getBuildingInfo(eBuildingLoop).isBuildingClassNeededInCity(iBuildingClassPrereqLoop))
						{
							if ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iBuildingClassPrereqLoop)) == eBuilding)
							{
								return -1;
							}
						}
					}
				}
			}
		}
	}

	// Increase cost if the XML defines that additional Buildings will cost more
	if (0 != GC.getBuildingInfo(eBuilding).getAdvancedStartCostIncrease())
	{
		iNumBuildingType = countNumBuildings(eBuilding);

		if (!bAdd)
		{
			--iNumBuildingType;
		}

		if (iNumBuildingType > 0)
		{
			iCost *= 100 + GC.getBuildingInfo(eBuilding).getAdvancedStartCostIncrease() * std::max(0, iNumBuildingType - getNumCities());
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Route
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartRouteCost(RouteTypes eRoute, bool bAdd, CvPlot* pPlot) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	if (eRoute == NO_ROUTE)
	{
		return -1;
	}

	int iNumRoutes = 0;

	int iCost = GC.getRouteInfo(eRoute).getAdvancedStartCost();

	// This denotes cities may not be purchased through Advanced Start
	if (iCost < 0)
	{
		return -1;
	}

	iCost *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent();
	iCost /= 100;

	// No invalid plots!
	if (pPlot != NULL)
	{
		if (pPlot->isCity())
		{
			return -1;
		}

		if (bAdd)
		{
			if (pPlot->isImpassable() || pPlot->isWater())
			{
				return -1;
			}
			// Can't place twice
			if (pPlot->getRouteType() == eRoute)
			{
				return -1;
			}
		}
		else
		{
			// Need Route to remove it
			if (pPlot->getRouteType() != eRoute)
			{
				return -1;
			}
		}

		// Must be owned by me
		if (pPlot->getOwnerINLINE() != getID())
		{
			return -1;
		}
	}

	// Tech requirement
	for (int iBuildLoop = 0; iBuildLoop < GC.getNumBuildInfos(); iBuildLoop++)
	{
		if (GC.getBuildInfo((BuildTypes) iBuildLoop).getRoute() == eRoute)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo((BuildTypes) iBuildLoop).getTechPrereq())))
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getRouteInfo(eRoute).getAdvancedStartCostIncrease())
	{
		int iPlotLoop = 0;
		CvPlot* pPlot;

		for (iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); iPlotLoop++)
		{
			pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

			if (pPlot->getRouteType() == eRoute)
			{
				++iNumRoutes;
			}
		}

		if (!bAdd)
		{
			--iNumRoutes;
		}

		if (iNumRoutes > 0)
		{
			iCost *= 100 + GC.getRouteInfo(eRoute).getAdvancedStartCostIncrease() * iNumRoutes;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Improvement
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartImprovementCost(ImprovementTypes eImprovement, bool bAdd, CvPlot* pPlot) const
{
	if (eImprovement == NO_IMPROVEMENT)
	{
		return -1;
	}

	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumImprovements = 0;
	int iCost = GC.getImprovementInfo(eImprovement).getAdvancedStartCost();

		// This denotes cities may not be purchased through Advanced Start
	if (iCost < 0)
	{
		return -1;
	}

	iCost *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent();
	iCost /= 100;

	// Can this Improvement be on our plot?
	if (pPlot != NULL)
	{
		if (bAdd)
		{
			// Valid Plot
//>>>>Unofficial Bug Fix: Modified by Denev 2010/05/04
//			if (!pPlot->canHaveImprovement(eImprovement, getTeam(), false))
			if (!pPlot->canHaveImprovement(eImprovement, getID(), false))
//<<<<Unofficial Bug Fix: End Modify
			{
				return -1;
			}

			bool bValid = false;

			for (int iI = 0; iI < GC.getNumBuildInfos(); ++iI)
			{
				CvBuildInfo& kBuild = GC.getBuildInfo((BuildTypes)iI);
				ImprovementTypes eLoopImprovement = ((ImprovementTypes)(kBuild.getImprovement()));

				if (eImprovement == eLoopImprovement && canBuild(pPlot, (BuildTypes)iI))
				{
					bValid = true;

					FeatureTypes eFeature = pPlot->getFeatureType();
//>>>>Unofficial Bug Fix: Modified by Denev 2010/02/21
//*** Elvish civilization can see the amount of production from forest chopping.
/*
					if (NO_FEATURE != eFeature && kBuild.isFeatureRemove(eFeature)

//FfH: Added by Kael 11/11/2007
					  && !GC.getCivilizationInfo(getCivilizationType()).isMaintainFeatures(pPlot->getFeatureType())
//FfH: End Add

					  )
*/
					if (pPlot->isFeatureRemove((BuildTypes)iI))
//<<<<Unofficial Bug Fix: End Modify
					{
						iCost += GC.getFeatureInfo(eFeature).getAdvancedStartRemoveCost();
					}

					break;
				}
			}

			if (!bValid)
			{
				return -1;
			}

			// Can't place twice
			if (pPlot->getImprovementType() == eImprovement)
			{
				return -1;
			}
		}
		else
		{
			// Need this improvement in order to remove it
			if (pPlot->getImprovementType() != eImprovement)
			{
				return -1;
			}
		}

		// Must be owned by me
		if (pPlot->getOwnerINLINE() != getID())
		{
			return -1;
		}
	}

	// Tech requirement
	for (int iBuildLoop = 0; iBuildLoop < GC.getNumBuildInfos(); iBuildLoop++)
	{
		if (GC.getBuildInfo((BuildTypes) iBuildLoop).getImprovement() == eImprovement)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo((BuildTypes) iBuildLoop).getTechPrereq())))
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getImprovementInfo(eImprovement).getAdvancedStartCostIncrease())
	{
		int iPlotLoop = 0;
		CvPlot* pPlot;

		for (iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); iPlotLoop++)
		{
			pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

			if (pPlot->getImprovementType() == eImprovement)
			{
				++iNumImprovements;
			}
		}

		if (!bAdd)
		{
			--iNumImprovements;
		}

		if (iNumImprovements > 0)
		{
			iCost *= 100 + GC.getImprovementInfo(eImprovement).getAdvancedStartCostIncrease() * iNumImprovements;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Tech
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartTechCost(TechTypes eTech, bool bAdd) const
{
	if (eTech == NO_TECH)
	{
		return -1;
	}

	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumTechs = 0;

	int iCost = (GET_TEAM(getTeam()).getResearchCost(eTech) * GC.getTechInfo(eTech).getAdvancedStartCost()) / 100;
	if (iCost < 0)
	{
		return -1;
	}

	if (bAdd)
	{
		if (!canResearch(eTech, false))
		{
			return -1;
		}
	}
	else if (!bAdd)
	{
		if (!GET_TEAM(getTeam()).isHasTech(eTech))
		{
			return -1;
		}

		// Search through all techs to see if any of the currently owned ones requires this tech
		for (int iTechLoop = 0; iTechLoop < GC.getNumTechInfos(); iTechLoop++)
		{
			TechTypes eTechLoop = (TechTypes) iTechLoop;

			if (GET_TEAM(getTeam()).isHasTech(eTechLoop))
			{
				int iPrereqLoop;

				// Or Prereqs
				for (iPrereqLoop = 0; iPrereqLoop < GC.getNUM_OR_TECH_PREREQS(); iPrereqLoop++)
				{
					if (GC.getTechInfo(eTechLoop).getPrereqOrTechs(iPrereqLoop) == eTech)
					{
						return -1;
					}
				}

				// And Prereqs
				for (iPrereqLoop = 0; iPrereqLoop < GC.getNUM_AND_TECH_PREREQS(); iPrereqLoop++)
				{
					if (GC.getTechInfo(eTechLoop).getPrereqAndTechs(iPrereqLoop) == eTech)
					{
						return -1;
					}
				}
			}
		}

		// If player has placed anything on the map which uses this tech then you cannot remove it
		int iLoop;

		// Units
		CvUnit* pLoopUnit;
		for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (pLoopUnit->getUnitInfo().getPrereqAndTech() == eTech)
			{
				return -1;
			}

			for (int iI = 0; iI < GC.getNUM_UNIT_AND_TECH_PREREQS(); iI++)
			{
				if (pLoopUnit->getUnitInfo().getPrereqAndTechs(iI) == eTech)
				{
					return -1;
				}
			}
		}

		// Cities
		CvCity* pLoopCity;
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			// All Buildings
			for (int iBuildingLoop = 0; iBuildingLoop < GC.getNumBuildingInfos(); iBuildingLoop++)
			{
				BuildingTypes eBuilding = (BuildingTypes) iBuildingLoop;

				if (pLoopCity->getNumRealBuilding(eBuilding) > 0)
				{
					if (GC.getBuildingInfo(eBuilding).getPrereqAndTech() == eTech)
					{
						return -1;
					}

					for (int iI = 0; iI < GC.getNUM_BUILDING_AND_TECH_PREREQS(); iI++)
					{
						if (GC.getBuildingInfo(eBuilding).getPrereqAndTechs(iI) == eTech)
						{
							return -1;
						}
					}
				}
			}
		}

	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getTechInfo(eTech).getAdvancedStartCostIncrease())
	{
		for (int iTechLoop = 0; iTechLoop < GC.getNumTechInfos(); iTechLoop++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes) iTechLoop))
			{
				++iNumTechs;
			}
		}

		if (!bAdd)
		{
			--iNumTechs;
		}

		if (iNumTechs > 0)
		{
			iCost *= 100 + GC.getTechInfo(eTech).getAdvancedStartCostIncrease() * iNumTechs;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Visibility
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartVisibilityCost(bool bAdd, CvPlot* pPlot) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumVisiblePlots = 0;
	int iCost = GC.getDefineINT("ADVANCED_START_VISIBILITY_COST");

	// This denotes Visibility may not be purchased through Advanced Start
	if (iCost == -1)
	{
		return -1;
	}

	// Valid Plot?
	if (pPlot != NULL)
	{
		if (bAdd)
		{
			if (pPlot->isRevealed(getTeam(), false))
			{
				return -1;
			}
			if (!pPlot->isAdjacentRevealed(getTeam()))
			{
				return -1;
			}
		}
		else
		{
			if (!pPlot->isRevealed(getTeam(), false))
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getDefineINT("ADVANCED_START_VISIBILITY_COST_INCREASE"))
	{
		int iPlotLoop = 0;
		CvPlot* pPlot;

		for (iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); iPlotLoop++)
		{
			pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

			if (pPlot->isRevealed(getTeam(), false))
			{
				++iNumVisiblePlots;
			}
		}

		if (!bAdd)
		{
			--iNumVisiblePlots;
		}

		if (iNumVisiblePlots > 0)
		{
			iCost *= 100 + GC.getDefineINT("ADVANCED_START_VISIBILITY_COST_INCREASE") * iNumVisiblePlots;
			iCost /= 100;
		}
	}

	return iCost;
}

void CvPlayer::doWarnings()
{
	CvCity* pNearestCity;
	CvPlot* pLoopPlot;
	CvUnit* pLoopUnit;
	wchar szBuffer[1024];
	int iMaxCount;
	int iI;

	//update enemy unit in your territory glow
	int iLoop;
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		//update glow
		gDLL->getEntityIFace()->updateEnemyGlow(pLoopUnit->getUnitEntity());
	}

// BUG - Ignore Harmless Barbarians - start
	bool bCheckBarbarians = false;
	bool bCheckBarbariansInitialized = !isHuman();
// BUG - Ignore Harmless Barbarians - end

	//update enemy units close to your territory
	iMaxCount = range(((getNumCities() + 4) / 7), 2, 5);
	for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		if (iMaxCount == 0)
		{
			break;
		}

		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->isAdjacentPlayer(getID()))
		{
			if (!(pLoopPlot->isCity()))
			{
				if (pLoopPlot->isVisible(getTeam(), false))
				{
					CvUnit *pUnit = pLoopPlot->getVisibleEnemyDefender(getID());
					if (pUnit != NULL)
					{
						if (!pUnit->isAnimal())
						{
// BUG - Ignore Harmless Barbarians - start
							if (!bCheckBarbariansInitialized && GC.getGameINLINE().getElapsedGameTurns() > 0)
							{
								bCheckBarbarians = getBugOptionBOOL("Actions__IgnoreHarmlessBarbarians", true, "BUG_IGNORE_HARMLESS_BARBARIANS");
								bCheckBarbariansInitialized = true;
							}
							if (bCheckBarbarians && pUnit->isBarbarian() && pUnit->getDomainType() == DOMAIN_LAND)
							{
								CvArea* pArea = pUnit->area();
								if (pArea && pArea->isBorderObstacle(getTeam()))
								{
									// don't show warning for land-based barbarians when player has Great Wall
									continue;
								}

								// lfgr 01/2022: Don't show warning for lairguardians
								if( pUnit->AI_getUnitAIType() == UNITAI_LAIRGUARDIAN )
								{
									continue;
								}
								if (pUnit->isHeld())
								{
									// Ignore held units.
									continue;
								}
							}
// BUG - Ignore Harmless Barbarians - end

							pNearestCity = GC.getMapINLINE().findCity(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), getID(), NO_TEAM, !(pLoopPlot->isWater()));

							if (pNearestCity != NULL)
							{
/*************************************************************************************************/
/**	ADDON (display tweak) merged Sephi 							01/04/09	Xienwolf Tweak		**/
/**																								**/
/**							Displays WHICH enemy is near your territory							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
								swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_ENEMY_TROOPS_SPOTTED", pNearestCity->getNameKey()).GetCString());
/**								----  End Original Code  ----									**/
								swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_ENEMY_TROOPS_SPOTTED", pNearestCity->getNameKey(), GET_PLAYER(pUnit->getVisualOwner(getTeam())).getCivilizationDescriptionKey()));
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
								
							// lfgr: ignore when in autoplay
							/* old code
								gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_ENEMY_TROOPS", MESSAGE_TYPE_INFO, pUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), true, true);
							*/
								if( GC.getGameINLINE().getAIAutoPlay( GC.getGameINLINE().getActivePlayer() ) <= 0 )
									gDLL->getInterfaceIFace()->addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_ENEMY_TROOPS", MESSAGE_TYPE_INFO, pUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), true, true);
							// lfgr end

								iMaxCount--;
							}
						}
					}
				}
			}
		}
	}
}


void CvPlayer::verifyGoldCommercePercent()
{
	while ((getGold() + calculateGoldRate()) < 0)
	{
		changeCommercePercent(COMMERCE_GOLD, GC.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"));

		if (getCommercePercent(COMMERCE_GOLD) == 100)
		{
			break;
		}
	}
}


void CvPlayer::processCivics(CivicTypes eCivic, int iChange)
{
	int iI, iJ;
	CvCivicInfo& kCivic = GC.getCivicInfo(eCivic);

	changeGreatPeopleRateModifier(kCivic.getGreatPeopleRateModifier() * iChange);
	changeGreatGeneralRateModifier(kCivic.getGreatGeneralRateModifier() * iChange);
	changeDomesticGreatGeneralRateModifier(kCivic.getDomesticGreatGeneralRateModifier() * iChange);
	changeStateReligionGreatPeopleRateModifier(kCivic.getStateReligionGreatPeopleRateModifier() * iChange);
	changeDistanceMaintenanceModifier(kCivic.getDistanceMaintenanceModifier() * iChange);
	changeNumCitiesMaintenanceModifier(kCivic.getNumCitiesMaintenanceModifier() * iChange);
	changeCorporationMaintenanceModifier(kCivic.getCorporationMaintenanceModifier() * iChange);
	changeExtraHealth(kCivic.getExtraHealth() * iChange);
	changeFreeExperience(kCivic.getFreeExperience() * iChange);
	changeWorkerSpeedModifier(kCivic.getWorkerSpeedModifier() * iChange);
	changeImprovementUpgradeRateModifier(kCivic.getImprovementUpgradeRateModifier() * iChange);
	changeMilitaryProductionModifier(kCivic.getMilitaryProductionModifier() * iChange);
	changeBaseFreeUnits(kCivic.getBaseFreeUnits() * iChange);
	changeBaseFreeMilitaryUnits(kCivic.getBaseFreeMilitaryUnits() * iChange);
	changeFreeUnitsPopulationPercent(kCivic.getFreeUnitsPopulationPercent() * iChange);
	changeFreeMilitaryUnitsPopulationPercent(kCivic.getFreeMilitaryUnitsPopulationPercent() * iChange);
	changeGoldPerUnit(kCivic.getGoldPerUnit() * iChange);
	changeGoldPerMilitaryUnit(kCivic.getGoldPerMilitaryUnit() * iChange);
	changeHappyPerMilitaryUnit(kCivic.getHappyPerMilitaryUnit() * iChange);
	changeMilitaryFoodProductionCount((kCivic.isMilitaryFoodProduction()) ? iChange : 0);
	changeMaxConscript(getWorldSizeMaxConscript(eCivic) * iChange);
	changeNoUnhealthyPopulationCount((kCivic.isNoUnhealthyPopulation()) ? iChange : 0);
	changeBuildingOnlyHealthyCount((kCivic.isBuildingOnlyHealthy()) ? iChange : 0);
	changeLargestCityHappiness(kCivic.getLargestCityHappiness() * iChange);
	changeWarWearinessModifier(kCivic.getWarWearinessModifier() * iChange);
	changeFreeSpecialist(kCivic.getFreeSpecialist() * iChange);
	changeTradeRoutes(kCivic.getTradeRoutes() * iChange);
	changeNoForeignTradeCount(kCivic.isNoForeignTrade() * iChange);
	changeNoCorporationsCount(kCivic.isNoCorporations() * iChange);
	changeNoForeignCorporationsCount(kCivic.isNoForeignCorporations() * iChange);
	changeStateReligionCount((kCivic.isStateReligion()) ? iChange : 0);
	changeNoNonStateReligionSpreadCount((kCivic.isNoNonStateReligionSpread()) ? iChange : 0);
	changeStateReligionHappiness(kCivic.getStateReligionHappiness() * iChange);
	changeNonStateReligionHappiness(kCivic.getNonStateReligionHappiness() * iChange);
	changeStateReligionUnitProductionModifier(kCivic.getStateReligionUnitProductionModifier() * iChange);
	changeStateReligionBuildingProductionModifier(kCivic.getStateReligionBuildingProductionModifier() * iChange);
	changeStateReligionFreeExperience(kCivic.getStateReligionFreeExperience() * iChange);
	changeExpInBorderModifier(kCivic.getExpInBorderModifier() * iChange);

/*************************************************************************************************/
/* Advanced Diplomacy         START                                                               */
/*************************************************************************************************/
	changeActiveSenateCount((GC.getCivicInfo(eCivic).isActiveSenate()) ? iChange : 0);
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/**
	
/************************************************************************************************/
/* REVDCM                                 09/02/10                                phungus420    */
/*                                                                                              */
/* RevCivic Effects                                                                             */
/************************************************************************************************/
	setCanInquisition(kCivic.isDisallowInquisitions() ? false : true);
/************************************************************************************************/
/* REVDCM                                  END                                                  */
/************************************************************************************************/

//FfH Civics: Added by Kael 08/11/2007
    changeCoastalTradeRoutes(kCivic.getCoastalTradeRoutes() * iChange);
    changeEnslavementChance(kCivic.getEnslavementChance() * iChange);
    changeNoDiplomacyWithEnemies(kCivic.isNoDiplomacyWithEnemies() * iChange);
    if (iChange == -1)
    {
        for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
        {
            if (GC.getVoteSourceInfo((VoteSourceTypes)iI).getCivic() == eCivic)
            {
                if (GC.getGameINLINE().getSecretaryGeneral((VoteSourceTypes)iI) == getTeam())
                {
                    GC.getGameINLINE().clearSecretaryGeneral((VoteSourceTypes)iI);
                }
            }
        }
    }
//FfH: End Add

	for (iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeYieldRateModifier(((YieldTypes)iI), (kCivic.getYieldModifier(iI) * iChange));
		changeCapitalYieldRateModifier(((YieldTypes)iI), (kCivic.getCapitalYieldModifier(iI) * iChange));
		changeTradeYieldModifier(((YieldTypes)iI), (kCivic.getTradeYieldModifier(iI) * iChange));
	}

	for (iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeCommerceRateModifier(((CommerceTypes)iI), (kCivic.getCommerceModifier(iI) * iChange));
		changeCapitalCommerceRateModifier(((CommerceTypes)iI), (kCivic.getCapitalCommerceModifier(iI) * iChange));
		changeSpecialistExtraCommerce(((CommerceTypes)iI), (kCivic.getSpecialistExtraCommerce(iI) * iChange));
	}

	for (iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		BuildingTypes eOurBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI);
		if (NO_BUILDING != eOurBuilding)
		{
			changeExtraBuildingHappiness(eOurBuilding, (kCivic.getBuildingHappinessChanges(iI) * iChange));
			changeExtraBuildingHealth(eOurBuilding, (kCivic.getBuildingHealthChanges(iI) * iChange));
		}
	}

	for (iI = 0; iI < GC.getNumFeatureInfos(); iI++)
	{
		changeFeatureHappiness(((FeatureTypes)iI), (kCivic.getFeatureHappinessChanges(iI) * iChange));
	}

	for (iI = 0; iI < GC.getNumHurryInfos(); iI++)
	{
		changeHurryCount(((HurryTypes)iI), ((kCivic.isHurry(iI)) ? iChange : 0));
	}

	for (iI = 0; iI < GC.getNumSpecialBuildingInfos(); iI++)
	{
		changeSpecialBuildingNotRequiredCount(((SpecialBuildingTypes)iI), ((kCivic.isSpecialBuildingNotRequired(iI)) ? iChange : 0));
	}

	for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		changeSpecialistValidCount(((SpecialistTypes)iI), ((kCivic.isSpecialistValid(iI)) ? iChange : 0));
	}

	for (iI = 0; iI < GC.getNumImprovementInfos(); iI++)
	{
		for (iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeImprovementYieldChange(((ImprovementTypes)iI), ((YieldTypes)iJ), (GC.getCivicInfo(eCivic).getImprovementYieldChanges(iI, iJ) * iChange));
		}
	}
}

void CvPlayer::showMissedMessages()
{
	CvMessageQueue::iterator it = m_listGameMessages.begin();
	while (it != m_listGameMessages.end())
	{
		CvTalkingHeadMessage& msg = *it;
		if (!msg.getShown())
		{
			msg.setShown(true);
			gDLL->getInterfaceIFace()->showMessage(msg);
		}
		++it;
	}
}

bool CvPlayer::isPbemNewTurn() const
{
	return m_bPbemNewTurn;
}

void CvPlayer::setPbemNewTurn(bool bNew)
{
	m_bPbemNewTurn = bNew;
}



//
// read object from a stream
// used during load
//
void CvPlayer::read(FDataStreamBase* pStream)
{
	int iI;

	// Init data before load
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iStartingX);
	pStream->Read(&m_iStartingY);
	pStream->Read(&m_iTotalPopulation);
	pStream->Read(&m_iTotalLand);
	pStream->Read(&m_iTotalLandScored);
	pStream->Read(&m_iGold);
	pStream->Read(&m_iGoldPerTurn);
	pStream->Read(&m_iAdvancedStartPoints);
	pStream->Read(&m_iGoldenAgeTurns);
	pStream->Read(&m_iNumUnitGoldenAges);
	pStream->Read(&m_iStrikeTurns);
	pStream->Read(&m_iAnarchyTurns);
	pStream->Read(&m_iMaxAnarchyTurns);
	pStream->Read(&m_iAnarchyModifier);
	pStream->Read(&m_iGoldenAgeModifier);
	pStream->Read(&m_iGlobalHurryModifier);
	pStream->Read(&m_iGreatPeopleCreated);
	pStream->Read(&m_iGreatGeneralsCreated);
	pStream->Read(&m_iGreatPeopleThresholdModifier);
	pStream->Read(&m_iGreatGeneralsThresholdModifier);
	pStream->Read(&m_iGreatPeopleRateModifier);
	pStream->Read(&m_iGreatGeneralRateModifier);
	pStream->Read(&m_iDomesticGreatGeneralRateModifier);
	pStream->Read(&m_iStateReligionGreatPeopleRateModifier);
	pStream->Read(&m_iMaxGlobalBuildingProductionModifier);
	pStream->Read(&m_iMaxTeamBuildingProductionModifier);
	pStream->Read(&m_iMaxPlayerBuildingProductionModifier);
	pStream->Read(&m_iFreeExperience);
	pStream->Read(&m_iFeatureProductionModifier);
	pStream->Read(&m_iWorkerSpeedModifier);
	pStream->Read(&m_iImprovementUpgradeRateModifier);
	pStream->Read(&m_iMilitaryProductionModifier);
	pStream->Read(&m_iSpaceProductionModifier);
	pStream->Read(&m_iCityDefenseModifier);
/************************************************************************************************/
/* REVDCM                                 09/02/10                                phungus420    */
/*                                                                                              */
/* Player Functions                                                                             */
/************************************************************************************************/
	pStream->Read(&m_iNonStateReligionCommerceCount);

	// LFGR_TODO: Compatability
	int iTmp;
	float fTmp;
	for( int i = 0; i < 5; i++ ) pStream->Read( &iTmp );
	for( int i = 0; i < 3; i++ ) pStream->Read( &fTmp );

	pStream->Read(&m_bCanInquisition);
/************************************************************************************************/
/* REVDCM                                  END                                                  */
/************************************************************************************************/
	pStream->Read(&m_iNumNukeUnits);
	pStream->Read(&m_iNumOutsideUnits);
	pStream->Read(&m_iBaseFreeUnits);
	pStream->Read(&m_iBaseFreeMilitaryUnits);
	pStream->Read(&m_iFreeUnitsPopulationPercent);
	pStream->Read(&m_iFreeMilitaryUnitsPopulationPercent);
	pStream->Read(&m_iGoldPerUnit);
	pStream->Read(&m_iGoldPerMilitaryUnit);
	pStream->Read(&m_iExtraUnitCost);
	pStream->Read(&m_iNumMilitaryUnits);
	pStream->Read(&m_iHappyPerMilitaryUnit);
	pStream->Read(&m_iMilitaryFoodProductionCount);
	pStream->Read(&m_iConscriptCount);
	pStream->Read(&m_iMaxConscript);
	pStream->Read(&m_iHighestUnitLevel);
	pStream->Read(&m_iOverflowResearch);
	pStream->Read(&m_iNoUnhealthyPopulationCount);
	pStream->Read(&m_iExpInBorderModifier);
	pStream->Read(&m_iBuildingOnlyHealthyCount);
	pStream->Read(&m_iDistanceMaintenanceModifier);
	pStream->Read(&m_iNumCitiesMaintenanceModifier);
	pStream->Read(&m_iCorporationMaintenanceModifier);
	pStream->Read(&m_iTotalMaintenance);
	pStream->Read(&m_iUpkeepModifier);
	pStream->Read(&m_iLevelExperienceModifier);
	pStream->Read(&m_iExtraHealth);
	pStream->Read(&m_iBuildingGoodHealth);
	pStream->Read(&m_iBuildingBadHealth);
	pStream->Read(&m_iExtraHappiness);
	pStream->Read(&m_iBuildingHappiness);
	pStream->Read(&m_iLargestCityHappiness);
	pStream->Read(&m_iWarWearinessPercentAnger);
	pStream->Read(&m_iWarWearinessModifier);
	pStream->Read(&m_iFreeSpecialist);
	pStream->Read(&m_iNoForeignTradeCount);
	pStream->Read(&m_iNoCorporationsCount);
	pStream->Read(&m_iNoForeignCorporationsCount);
	pStream->Read(&m_iCoastalTradeRoutes);
	pStream->Read(&m_iTradeRoutes);
	pStream->Read(&m_iRevolutionTimer);
	pStream->Read(&m_iConversionTimer);
	pStream->Read(&m_iStateReligionCount);
	pStream->Read(&m_iNoNonStateReligionSpreadCount);
/*************************************************************************************************/
/* Advanced Diplomacy         START                                                               */
/*************************************************************************************************/
	pStream->Read(&m_iActiveSenateCount);
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/
	pStream->Read(&m_iStateReligionHappiness);
	pStream->Read(&m_iNonStateReligionHappiness);
	pStream->Read(&m_iStateReligionUnitProductionModifier);
	pStream->Read(&m_iStateReligionBuildingProductionModifier);
	pStream->Read(&m_iStateReligionFreeExperience);
	pStream->Read(&m_iCapitalCityID);
	pStream->Read(&m_iCitiesLost);
	pStream->Read(&m_iWinsVsBarbs);
	pStream->Read(&m_iAssets);
	pStream->Read(&m_iPower);
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	pStream->Read(&m_iTechPower);
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	pStream->Read(&m_iPopulationScore);
	pStream->Read(&m_iLandScore);
	pStream->Read(&m_iWondersScore);
	pStream->Read(&m_iTechScore);
	pStream->Read(&m_iCombatExperience);

	pStream->Read(&m_bAlive);
	pStream->Read(&m_bEverAlive);
	pStream->Read(&m_bTurnActive);
	pStream->Read(&m_bAutoMoves);
	pStream->Read(&m_bEndTurn);
	pStream->Read(&m_bPbemNewTurn);
	pStream->Read(&m_bExtendedGame);
	pStream->Read(&m_bFoundedFirstCity);
	pStream->Read(&m_bStrike);

/************************************************************************************************/
/* AI_AUTO_PLAY                           07/09/08                                jdog5000      */
/************************************************************************************************/
	pStream->Read(&m_bDisableHuman);
/************************************************************************************************/
/* AI_AUTO_PLAY                            END                                                  */
/************************************************************************************************/

	// tech bug fix
	pStream->Read(&m_bChoosingFreeTech);
	pStream->Read(&m_bPuppetState); // MNAI - Puppet States

/*************************************************************************************************/
/**	CivCounter			               		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
    pStream->Read(&m_iCivCounter);
    pStream->Read(&m_iCivCounterMod);
/*************************************************************************************************/
/**	CivCounter								END													**/
/*************************************************************************************************/

	// Sephi AI (New Functions Definition)
    pStream->Read((int*)&m_eFavoriteReligion);
    pStream->Read(&m_iTowerVicFlag);
	pStream->Read(&m_bSumSuiMode);
	// End Sephi AI

	//FfH Traits: Added by Kael 08/02/2007
	pStream->Read(&m_bAdaptive);
	pStream->Read(&m_bAgnostic);
	pStream->Read(&m_bAssimilation);
	pStream->Read(&m_bDeclaringWar);
	//pStream->Read(&m_bDisableHuman); // AI Auto-Play
	pStream->Read(&m_bHideUnits);
	pStream->Read(&m_bIgnoreFood);
	pStream->Read(&m_bInsane);
	pStream->Read(&m_bSeeInvisible);
	pStream->Read(&m_bSprawling);
	pStream->Read((int*)&m_eAlignment);
	pStream->Read(&m_iDisableProduction);
	pStream->Read(&m_iDisableResearch);
	pStream->Read(&m_iDisableSpellcasting);
	pStream->Read(&m_iDiscoverRandModifier);
	pStream->Read(&m_iEnslavementChance);
	pStream->Read(&m_iFreeXPFromCombat);
	pStream->Read(&m_iHealChange);
	pStream->Read(&m_iHealChangeEnemy);
	pStream->Read(&m_iMaxCities);
	pStream->Read(&m_iNoDiplomacyWithEnemies);
	pStream->Read(&m_iPillagingGold);
	pStream->Read(&m_iPlayersKilled);
	pStream->Read(&m_iRealPlayer);
	pStream->Read(&m_iResistEnemyModify);
	pStream->Read(&m_iResistModify);
	pStream->Read(&m_iSanctuaryTimer);
	pStream->Read(&m_iStartingGold);
	pStream->Read(&m_iSummonDuration);
	pStream->Read(&m_iTempPlayerTimer);
	pStream->Read(&m_iUpgradeCostModifier);
	pStream->Read(GC.getNumTraitInfos(), m_pbTraits);
	for (iI=0;iI<GC.getNumSpecialistInfos();iI++)
	{
		pStream->Read(NUM_COMMERCE_TYPES, m_ppaaiSpecialistTypeExtraCommerce[iI]);
	}
	//FfH: End Add

/************************************************************************************************/
/* REVOLUTION_MOD                         02/04/09                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	pStream->Read(&m_iFreeUnitCountdown);

	pStream->Read(&m_iStabilityIndex);
	pStream->Read(&m_iStabilityIndexAverage);
	
	pStream->Read(&m_bRebel);
	pStream->Read(&m_iMotherPlayer);

	// Used for DynamicCivNames
	pStream->ReadString(m_szName);
	pStream->ReadString(m_szCivDesc);
	pStream->ReadString(m_szCivShort);
	pStream->ReadString(m_szCivAdj);
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

	pStream->Read((int*)&m_eID);
	pStream->Read((int*)&m_ePersonalityType);
	pStream->Read((int*)&m_eCurrentEra);
// ERA_FIX 09/2017 lfgr
	pStream->Read((int*)&m_eCurrentRealEra);
// ERA_FIX end
	pStream->Read((int*)&m_eLastStateReligion);
	pStream->Read((int*)&m_eParent);
	updateTeamType(); //m_eTeamType not saved
	updateHuman();

	pStream->Read(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiCapitalYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiExtraYieldThreshold);
	pStream->Read(NUM_YIELD_TYPES, m_aiTradeYieldModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiFreeCityCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommercePercent);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCapitalCommerceRateModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiStateReligionBuildingCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiSpecialistExtraCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceFlexibleCount);
	pStream->Read(MAX_PLAYERS, m_aiGoldPerTurnByPlayer);
	pStream->Read(MAX_TEAMS, m_aiEspionageSpendingWeightAgainstTeam);

	pStream->Read(NUM_FEAT_TYPES, m_abFeatAccomplished);
	pStream->Read(NUM_PLAYEROPTION_TYPES, m_abOptions);

	pStream->ReadString(m_szScriptData);
	
/*************************************************************************************************/
/* Advanced Diplomacy         START                                                              */
/*************************************************************************************************/
	{
		m_aiSenateVeto.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iValue;
			pStream->Read(&iValue);
			m_aiSenateVeto.push_back(iValue);
		}
	}
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but it is expected to be in CvPlayer::read");
	pStream->Read(GC.getNumBonusInfos(), m_paiBonusExport);
	pStream->Read(GC.getNumBonusInfos(), m_paiBonusImport);
	pStream->Read(GC.getNumImprovementInfos(), m_paiImprovementCount);
	pStream->Read(GC.getNumBuildingInfos(), m_paiFreeBuildingCount);
	pStream->Read(GC.getNumBuildingInfos(), m_paiExtraBuildingHappiness);
	pStream->Read(GC.getNumBuildingInfos(), m_paiExtraBuildingHealth);
	pStream->Read(GC.getNumFeatureInfos(), m_paiFeatureHappiness);
	pStream->Read(GC.getNumUnitClassInfos(), m_paiUnitClassCount);
	pStream->Read(GC.getNumUnitClassInfos(), m_paiUnitClassMaking);
	pStream->Read(GC.getNumBuildingClassInfos(), m_paiBuildingClassCount);
	pStream->Read(GC.getNumBuildingClassInfos(), m_paiBuildingClassMaking);
	pStream->Read(GC.getNumHurryInfos(), m_paiHurryCount);
	pStream->Read(GC.getNumSpecialBuildingInfos(), m_paiSpecialBuildingNotRequiredCount);
	pStream->Read(GC.getNumCivicOptionInfos(), m_paiHasCivicOptionCount);
	pStream->Read(GC.getNumCivicOptionInfos(), m_paiNoCivicUpkeepCount);
	pStream->Read(GC.getNumReligionInfos(), m_paiHasReligionCount);
	pStream->Read(GC.getNumCorporationInfos(), m_paiHasCorporationCount);
	pStream->Read(GC.getNumUpkeepInfos(), m_paiUpkeepCount);
	pStream->Read(GC.getNumSpecialistInfos(), m_paiSpecialistValidCount);
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	pStream->Read((int*)&m_eSecretaryGeneralVote);
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

/************************************************************************************************/
/* EVENT_NEW_TAGS                           12/2015                                 lfgr        */
/************************************************************************************************/
	pStream->Read( GC.getNumEventTriggerInfos(), m_paiEventTriggerDelayCounters );
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/


	FAssertMsg((0 < GC.getNumTechInfos()), "GC.getNumTechInfos() is not greater than zero but it is expected to be in CvPlayer::read");
	pStream->Read(GC.getNumTechInfos(), m_pabResearchingTech);

	pStream->Read(GC.getNumVoteSourceInfos(), m_pabLoyalMember);

	for (iI=0;iI<GC.getNumCivicOptionInfos();iI++)
	{
		pStream->Read((int*)&m_paeCivics[iI]);
	}

	for (iI=0;iI<GC.getNumSpecialistInfos();iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaaiSpecialistExtraYield[iI]);
	}

	for (iI=0;iI<GC.getNumImprovementInfos();iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaaiImprovementYieldChange[iI]);
	}

	m_groupCycle.Read(pStream);
	m_researchQueue.Read(pStream);

	{
		m_cityNames.clear();
		CvWString szBuffer;
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			pStream->ReadString(szBuffer);
			m_cityNames.insertAtEnd(szBuffer);
		}
	}

	ReadStreamableFFreeListTrashArray(m_plotGroups, pStream);
	ReadStreamableFFreeListTrashArray(m_cities, pStream);
	ReadStreamableFFreeListTrashArray(m_units, pStream);
	ReadStreamableFFreeListTrashArray(m_selectionGroups, pStream);
	ReadStreamableFFreeListTrashArray(m_eventsTriggered, pStream);

	{
		CvMessageQueue::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (CvMessageQueue::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvTalkingHeadMessage message;
			message.read(*pStream);
			m_listGameMessages.push_back(message);
		}
	}

	{
		clearPopups();
		CvPopupQueue::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (CvPopupQueue::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvPopupInfo* pInfo = new CvPopupInfo();
			if (NULL != pInfo)
			{
				pInfo->read(*pStream);
				m_listPopups.push_back(pInfo);
			}
		}
	}

	{
		clearDiplomacy();
		CvDiploQueue::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (CvDiploQueue::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvDiploParameters* pDiplo = new CvDiploParameters(NO_PLAYER);
			if (NULL != pDiplo)
			{
				pDiplo->read(*pStream);
				m_listDiplomacy.push_back(pDiplo);
			}
		}
	}

	{
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapScoreHistory[iTurn] = iScore;
		}
	}

	{
		m_mapEconomyHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapEconomyHistory[iTurn] = iScore;
		}
	}

	{
		m_mapIndustryHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapIndustryHistory[iTurn] = iScore;
		}
	}

	{
		m_mapAgricultureHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapAgricultureHistory[iTurn] = iScore;
		}
	}

	{
		m_mapPowerHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapPowerHistory[iTurn] = iScore;
		}
	}

	{
		m_mapCultureHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapCultureHistory[iTurn] = iScore;
		}
	}

	{
		m_mapEspionageHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapEspionageHistory[iTurn] = iScore;
		}
	}


/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         02/04/08                            Glider1        */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	// RevolutionDCM - read revolution stability history data from disk
	{
		m_mapRevolutionStabilityHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapRevolutionStabilityHistory[iTurn] = iScore;
		}
	}
	// RevolutionDCM end
/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         END                                 Glider1        */
/************************************************************************************************/

	{
		m_mapEventsOccured.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			EventTriggeredData kData;
			EventTypes eEvent;
			pStream->Read((int*)&eEvent);
			kData.read(pStream);
			m_mapEventsOccured[eEvent] = kData;
		}
	}

	{
		m_mapEventCountdown.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			EventTriggeredData kData;
			EventTypes eEvent;
			pStream->Read((int*)&eEvent);
			kData.read(pStream);
			m_mapEventCountdown[eEvent] = kData;
		}
	}

	{
		m_aFreeUnitCombatPromotions.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iUnitCombat;
			int iPromotion;
			pStream->Read(&iUnitCombat);
			pStream->Read(&iPromotion);
			m_aFreeUnitCombatPromotions.push_back(std::make_pair((UnitCombatTypes)iUnitCombat, (PromotionTypes)iPromotion));
		}
	}

	{
		m_aFreeUnitClassPromotions.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iUnitClass;
			int iPromotion;
			pStream->Read(&iUnitClass);
			pStream->Read(&iPromotion);
			m_aFreeUnitClassPromotions.push_back(std::make_pair((UnitClassTypes)iUnitClass, (PromotionTypes)iPromotion));
		}
	}

	{
		m_aVote.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iId;
			PlayerVoteTypes eVote;
			pStream->Read(&iId);
			pStream->Read((int*)&eVote);
			m_aVote.push_back(std::make_pair(iId, eVote));
		}
	}

	{
		m_aUnitExtraCosts.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iCost;
			UnitClassTypes eUnit;
			pStream->Read((int*)&eUnit);
			pStream->Read(&iCost);
			m_aUnitExtraCosts.push_back(std::make_pair(eUnit, iCost));
		}
	}

	if (uiFlag > 0)
	{
		m_triggersFired.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTrigger;
			pStream->Read(&iTrigger);
			m_triggersFired.push_back((EventTriggerTypes)iTrigger);
		}
	}
	else
	{

//FfH: Modified by Kael 09/18/2008
//		int iNumEventTriggers = std::min(176, GC.getNumEventTriggerInfos()); // yuck, hardcoded number of eventTriggers in the epic game in initial release
//		for (iI=0; iI < iNumEventTriggers; iI++)
		for (iI=0; iI < GC.getNumEventTriggerInfos(); iI++)
//FfH: End Modify

		{
			bool bTriggered;
			pStream->Read(&bTriggered);
			if (bTriggered)
			{
				m_triggersFired.push_back((EventTriggerTypes)iI);
			}
		}
	}

	if (!isBarbarian())
	{
		// Get the NetID from the initialization structure
		setNetID(gDLL->getAssignedNetworkID(getID()));
	}

	pStream->Read(&m_iPopRushHurryCount);
	pStream->Read(&m_iInflationModifier);
}

//
// save object to a stream
// used during save
//
void CvPlayer::write(FDataStreamBase* pStream)
{
	int iI;

	uint uiFlag = 1;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iStartingX);
	pStream->Write(m_iStartingY);
	pStream->Write(m_iTotalPopulation);
	pStream->Write(m_iTotalLand);
	pStream->Write(m_iTotalLandScored);
	pStream->Write(m_iGold);
	pStream->Write(m_iGoldPerTurn);
	pStream->Write(m_iAdvancedStartPoints);
	pStream->Write(m_iGoldenAgeTurns);
	pStream->Write(m_iNumUnitGoldenAges);
	pStream->Write(m_iStrikeTurns);
	pStream->Write(m_iAnarchyTurns);
	pStream->Write(m_iMaxAnarchyTurns);
	pStream->Write(m_iAnarchyModifier);
	pStream->Write(m_iGoldenAgeModifier);
	pStream->Write(m_iGlobalHurryModifier);
	pStream->Write(m_iGreatPeopleCreated);
	pStream->Write(m_iGreatGeneralsCreated);
	pStream->Write(m_iGreatPeopleThresholdModifier);
	pStream->Write(m_iGreatGeneralsThresholdModifier);
	pStream->Write(m_iGreatPeopleRateModifier);
	pStream->Write(m_iGreatGeneralRateModifier);
	pStream->Write(m_iDomesticGreatGeneralRateModifier);
	pStream->Write(m_iStateReligionGreatPeopleRateModifier);
	pStream->Write(m_iMaxGlobalBuildingProductionModifier);
	pStream->Write(m_iMaxTeamBuildingProductionModifier);
	pStream->Write(m_iMaxPlayerBuildingProductionModifier);
	pStream->Write(m_iFreeExperience);
	pStream->Write(m_iFeatureProductionModifier);
	pStream->Write(m_iWorkerSpeedModifier);
	pStream->Write(m_iImprovementUpgradeRateModifier);
	pStream->Write(m_iMilitaryProductionModifier);
	pStream->Write(m_iSpaceProductionModifier);
	pStream->Write(m_iCityDefenseModifier);
/************************************************************************************************/
/* REVDCM                                 09/02/10                                phungus420    */
/*                                                                                              */
/* Player Functions                                                                             */
/************************************************************************************************/
	pStream->Write(m_iNonStateReligionCommerceCount);

	// LFGR_TODO: Compatability
	for( int i = 0; i < 5; i++ ) pStream->Write( 0 );
	for( int i = 0; i < 3; i++ ) pStream->Write( 0.f );

	pStream->Write(m_bCanInquisition);
/************************************************************************************************/
/* REVDCM                                  END                                                  */
/************************************************************************************************/
	pStream->Write(m_iNumNukeUnits);
	pStream->Write(m_iNumOutsideUnits);
	pStream->Write(m_iBaseFreeUnits);
	pStream->Write(m_iBaseFreeMilitaryUnits);
	pStream->Write(m_iFreeUnitsPopulationPercent);
	pStream->Write(m_iFreeMilitaryUnitsPopulationPercent);
	pStream->Write(m_iGoldPerUnit);
	pStream->Write(m_iGoldPerMilitaryUnit);
	pStream->Write(m_iExtraUnitCost);
	pStream->Write(m_iNumMilitaryUnits);
	pStream->Write(m_iHappyPerMilitaryUnit);
	pStream->Write(m_iMilitaryFoodProductionCount);
	pStream->Write(m_iConscriptCount);
	pStream->Write(m_iMaxConscript);
	pStream->Write(m_iHighestUnitLevel);
	pStream->Write(m_iOverflowResearch);
	pStream->Write(m_iNoUnhealthyPopulationCount);
	pStream->Write(m_iExpInBorderModifier);
	pStream->Write(m_iBuildingOnlyHealthyCount);
	pStream->Write(m_iDistanceMaintenanceModifier);
	pStream->Write(m_iNumCitiesMaintenanceModifier);
	pStream->Write(m_iCorporationMaintenanceModifier);
	pStream->Write(m_iTotalMaintenance);
	pStream->Write(m_iUpkeepModifier);
	pStream->Write(m_iLevelExperienceModifier);
	pStream->Write(m_iExtraHealth);
	pStream->Write(m_iBuildingGoodHealth);
	pStream->Write(m_iBuildingBadHealth);
	pStream->Write(m_iExtraHappiness);
	pStream->Write(m_iBuildingHappiness);
	pStream->Write(m_iLargestCityHappiness);
	pStream->Write(m_iWarWearinessPercentAnger);
	pStream->Write(m_iWarWearinessModifier);
	pStream->Write(m_iFreeSpecialist);
	pStream->Write(m_iNoForeignTradeCount);
	pStream->Write(m_iNoCorporationsCount);
	pStream->Write(m_iNoForeignCorporationsCount);
	pStream->Write(m_iCoastalTradeRoutes);
	pStream->Write(m_iTradeRoutes);
	pStream->Write(m_iRevolutionTimer);
	pStream->Write(m_iConversionTimer);
	pStream->Write(m_iStateReligionCount);
	pStream->Write(m_iNoNonStateReligionSpreadCount);
/*************************************************************************************************/
/* Advanced Diplomacy         START                                                               */
/*************************************************************************************************/
	pStream->Write(m_iActiveSenateCount);
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/
	pStream->Write(m_iStateReligionHappiness);
	pStream->Write(m_iNonStateReligionHappiness);
	pStream->Write(m_iStateReligionUnitProductionModifier);
	pStream->Write(m_iStateReligionBuildingProductionModifier);
	pStream->Write(m_iStateReligionFreeExperience);
	pStream->Write(m_iCapitalCityID);
	pStream->Write(m_iCitiesLost);
	pStream->Write(m_iWinsVsBarbs);
	pStream->Write(m_iAssets);
	pStream->Write(m_iPower);
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	pStream->Write(m_iTechPower);//Aforesss
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	pStream->Write(m_iPopulationScore);
	pStream->Write(m_iLandScore);
	pStream->Write(m_iWondersScore);
	pStream->Write(m_iTechScore);
	pStream->Write(m_iCombatExperience);

	pStream->Write(m_bAlive);
	pStream->Write(m_bEverAlive);
	pStream->Write(m_bTurnActive);
	pStream->Write(m_bAutoMoves);
	pStream->Write(m_bEndTurn);
	pStream->Write(m_bPbemNewTurn && GC.getGameINLINE().isPbem());
	pStream->Write(m_bExtendedGame);
	pStream->Write(m_bFoundedFirstCity);
	pStream->Write(m_bStrike);

/************************************************************************************************/
/* AI_AUTO_PLAY                           07/09/08                                jdog5000      */
/************************************************************************************************/
	pStream->Write(m_bDisableHuman);
/************************************************************************************************/
/* AI_AUTO_PLAY                            END                                                  */
/************************************************************************************************/

	// Tech bug fix
	pStream->Write(m_bChoosingFreeTech);

	pStream->Write(m_bPuppetState); // MNAI - Puppet States
/*************************************************************************************************/
/**	CivCounter			               		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
    pStream->Write(m_iCivCounter);
    pStream->Write(m_iCivCounterMod);
/*************************************************************************************************/
/**	CivCounter								END													**/
/*************************************************************************************************/


	// Sephi AI (New Functions Definition) Sephi
    pStream->Write(m_eFavoriteReligion);
    pStream->Write(m_iTowerVicFlag);
	pStream->Write(m_bSumSuiMode);
	// End Sephi AI

	//FfH Traits: Added by Kael 08/02/2007
	pStream->Write(m_bAdaptive);
	pStream->Write(m_bAgnostic);
	pStream->Write(m_bAssimilation);
	pStream->Write(m_bDeclaringWar);
	//pStream->Write(m_bDisableHuman); // AI_AUTO_PLAY
	pStream->Write(m_bHideUnits);
	pStream->Write(m_bIgnoreFood);
	pStream->Write(m_bInsane);
	pStream->Write(m_bSeeInvisible);
	pStream->Write(m_bSprawling);
	pStream->Write(m_eAlignment);
	pStream->Write(m_iDisableProduction);
	pStream->Write(m_iDisableResearch);
	pStream->Write(m_iDisableSpellcasting);
	pStream->Write(m_iDiscoverRandModifier);
	pStream->Write(m_iEnslavementChance);
	pStream->Write(m_iFreeXPFromCombat);
	pStream->Write(m_iHealChange);
	pStream->Write(m_iHealChangeEnemy);
	pStream->Write(m_iMaxCities);
	pStream->Write(m_iNoDiplomacyWithEnemies);
	pStream->Write(m_iPillagingGold);
	pStream->Write(m_iPlayersKilled);
	pStream->Write(m_iRealPlayer);
	pStream->Write(m_iResistEnemyModify);
	pStream->Write(m_iResistModify);
	pStream->Write(m_iSanctuaryTimer);
	pStream->Write(m_iStartingGold);
	pStream->Write(m_iSummonDuration);
	pStream->Write(m_iTempPlayerTimer);
	pStream->Write(m_iUpgradeCostModifier);

	pStream->Write(GC.getNumTraitInfos(), m_pbTraits);
	for (iI=0;iI<GC.getNumSpecialistInfos();iI++)
	{
		pStream->Write(NUM_COMMERCE_TYPES, m_ppaaiSpecialistTypeExtraCommerce[iI]);
	}
	//FfH: End Add

/************************************************************************************************/
/* REVOLUTION_MOD                         06/11/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	pStream->Write(m_iFreeUnitCountdown);
	
	pStream->Write(m_iStabilityIndex);
	pStream->Write(m_iStabilityIndexAverage);
	
	pStream->Write(m_bRebel);
	pStream->Write(m_iMotherPlayer);

	// Used for DynamicCivNames
	pStream->WriteString(m_szName);
	pStream->WriteString(m_szCivDesc);
	pStream->WriteString(m_szCivShort);
	pStream->WriteString(m_szCivAdj);
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

	pStream->Write(m_eID);
	pStream->Write(m_ePersonalityType);
	pStream->Write(m_eCurrentEra);
// ERA_FIX 09/2017 lfgr
	pStream->Write(m_eCurrentRealEra);
// ERA_FIX end
	pStream->Write(m_eLastStateReligion);
	pStream->Write(m_eParent);
	//m_eTeamType not saved

	pStream->Write(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiCapitalYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiExtraYieldThreshold);
	pStream->Write(NUM_YIELD_TYPES, m_aiTradeYieldModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiFreeCityCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommercePercent);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCapitalCommerceRateModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiStateReligionBuildingCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiSpecialistExtraCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceFlexibleCount);
	pStream->Write(MAX_PLAYERS, m_aiGoldPerTurnByPlayer);
	pStream->Write(MAX_TEAMS, m_aiEspionageSpendingWeightAgainstTeam);

	pStream->Write(NUM_FEAT_TYPES, m_abFeatAccomplished);
	pStream->Write(NUM_PLAYEROPTION_TYPES, m_abOptions);

	pStream->WriteString(m_szScriptData);
	
/*************************************************************************************************/
/* Advanced Diplomacy         START                                                               */
/*************************************************************************************************/
	{
		uint iSize = m_aiSenateVeto.size();
		pStream->Write(iSize);
		std::vector<int>::iterator it;
		for (it = m_aiSenateVeto.begin(); it != m_aiSenateVeto.end(); ++it)
		{
			pStream->Write((*it));
		}
	}
/*************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/*************************************************************************************************/

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlayer::write");
	pStream->Write(GC.getNumBonusInfos(), m_paiBonusExport);
	pStream->Write(GC.getNumBonusInfos(), m_paiBonusImport);
	pStream->Write(GC.getNumImprovementInfos(), m_paiImprovementCount);
	pStream->Write(GC.getNumBuildingInfos(), m_paiFreeBuildingCount);
	pStream->Write(GC.getNumBuildingInfos(), m_paiExtraBuildingHappiness);
	pStream->Write(GC.getNumBuildingInfos(), m_paiExtraBuildingHealth);
	pStream->Write(GC.getNumFeatureInfos(), m_paiFeatureHappiness);
	pStream->Write(GC.getNumUnitClassInfos(), m_paiUnitClassCount);
	pStream->Write(GC.getNumUnitClassInfos(), m_paiUnitClassMaking);
	pStream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingClassCount);
	pStream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingClassMaking);
	pStream->Write(GC.getNumHurryInfos(), m_paiHurryCount);
	pStream->Write(GC.getNumSpecialBuildingInfos(), m_paiSpecialBuildingNotRequiredCount);
	pStream->Write(GC.getNumCivicOptionInfos(), m_paiHasCivicOptionCount);
	pStream->Write(GC.getNumCivicOptionInfos(), m_paiNoCivicUpkeepCount);
	pStream->Write(GC.getNumReligionInfos(), m_paiHasReligionCount);
	pStream->Write(GC.getNumCorporationInfos(), m_paiHasCorporationCount);
	pStream->Write(GC.getNumUpkeepInfos(), m_paiUpkeepCount);
	pStream->Write(GC.getNumSpecialistInfos(), m_paiSpecialistValidCount);
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	pStream->Write(m_eSecretaryGeneralVote);
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

/************************************************************************************************/
/* EVENT_NEW_TAGS                           12/2015                                 lfgr        */
/************************************************************************************************/
	pStream->Write(GC.getNumEventTriggerInfos(), m_paiEventTriggerDelayCounters);
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/


	FAssertMsg((0 < GC.getNumTechInfos()), "GC.getNumTechInfos() is not greater than zero but it is expected to be in CvPlayer::write");
	pStream->Write(GC.getNumTechInfos(), m_pabResearchingTech);

	pStream->Write(GC.getNumVoteSourceInfos(), m_pabLoyalMember);

	for (iI=0;iI<GC.getNumCivicOptionInfos();iI++)
	{
		pStream->Write(m_paeCivics[iI]);
	}

	for (iI=0;iI<GC.getNumSpecialistInfos();iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaaiSpecialistExtraYield[iI]);
	}

	for (iI=0;iI<GC.getNumImprovementInfos();iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaaiImprovementYieldChange[iI]);
	}

	m_groupCycle.Write(pStream);
	m_researchQueue.Write(pStream);

	{
		CLLNode<CvWString>* pNode;
		uint iSize = m_cityNames.getLength();
		pStream->Write(iSize);
		pNode = m_cityNames.head();
		while (pNode != NULL)
		{
			pStream->WriteString(pNode->m_data);
			pNode = m_cityNames.next(pNode);
		}
	}

	WriteStreamableFFreeListTrashArray(m_plotGroups, pStream);
	WriteStreamableFFreeListTrashArray(m_cities, pStream);
	WriteStreamableFFreeListTrashArray(m_units, pStream);
	WriteStreamableFFreeListTrashArray(m_selectionGroups, pStream);
	WriteStreamableFFreeListTrashArray(m_eventsTriggered, pStream);

	{
		CvMessageQueue::_Alloc::size_type iSize = m_listGameMessages.size();
		pStream->Write(iSize);
		CvMessageQueue::iterator it;
		for (it = m_listGameMessages.begin(); it != m_listGameMessages.end(); ++it)
		{
			CvTalkingHeadMessage& message = *it;
			message.write(*pStream);
		}
	}

	{
		CvPopupQueue currentPopups;
		if (GC.getGameINLINE().isNetworkMultiPlayer())
		{
			// don't save open popups in MP to avoid having different state on different machines
			currentPopups.clear();
		}
		else
		{
			gDLL->getInterfaceIFace()->getDisplayedButtonPopups(currentPopups);
		}
		CvPopupQueue::_Alloc::size_type iSize = m_listPopups.size() + currentPopups.size();
		pStream->Write(iSize);
		CvPopupQueue::iterator it;
		for (it = currentPopups.begin(); it != currentPopups.end(); ++it)
		{
			CvPopupInfo* pInfo = *it;
			if (NULL != pInfo)
			{
				pInfo->write(*pStream);
			}
		}
		for (it = m_listPopups.begin(); it != m_listPopups.end(); ++it)
		{
			CvPopupInfo* pInfo = *it;
			if (NULL != pInfo)
			{
				pInfo->write(*pStream);
			}
		}
	}

	{
		CvDiploQueue::_Alloc::size_type iSize = m_listDiplomacy.size();
		pStream->Write(iSize);
		CvDiploQueue::iterator it;
		for (it = m_listDiplomacy.begin(); it != m_listDiplomacy.end(); ++it)
		{
			CvDiploParameters* pDiplo = *it;
			if (NULL != pDiplo)
			{
				pDiplo->write(*pStream);
			}
		}
	}

	{
		uint iSize = m_mapScoreHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapScoreHistory.begin(); it != m_mapScoreHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapEconomyHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapEconomyHistory.begin(); it != m_mapEconomyHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapIndustryHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapIndustryHistory.begin(); it != m_mapIndustryHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapAgricultureHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapAgricultureHistory.begin(); it != m_mapAgricultureHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapPowerHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapPowerHistory.begin(); it != m_mapPowerHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapCultureHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapCultureHistory.begin(); it != m_mapCultureHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapEspionageHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapEspionageHistory.begin(); it != m_mapEspionageHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         02/04/08                            Glider1        */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	// RevolutionDCM - save revolution stability history to disk
	{
		uint iSize = m_mapRevolutionStabilityHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapRevolutionStabilityHistory.begin(); it != m_mapRevolutionStabilityHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}
	// RevolutionDCM - end
/************************************************************************************************/
/* REVOLUTIONDCM_MOD                         END                                 Glider1        */
/************************************************************************************************/

	{
		uint iSize = m_mapEventsOccured.size();
		pStream->Write(iSize);
		CvEventMap::iterator it;
		for (it = m_mapEventsOccured.begin(); it != m_mapEventsOccured.end(); ++it)
		{
			pStream->Write(it->first);
			it->second.write(pStream);
		}
	}

	{
		uint iSize = m_mapEventCountdown.size();
		pStream->Write(iSize);
		CvEventMap::iterator it;
		for (it = m_mapEventCountdown.begin(); it != m_mapEventCountdown.end(); ++it)
		{
			pStream->Write(it->first);
			it->second.write(pStream);
		}
	}

	{
		uint iSize = m_aFreeUnitCombatPromotions.size();
		pStream->Write(iSize);
		UnitCombatPromotionArray::iterator it;
		for (it = m_aFreeUnitCombatPromotions.begin(); it != m_aFreeUnitCombatPromotions.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_aFreeUnitClassPromotions.size();
		pStream->Write(iSize);
		UnitClassPromotionArray::iterator it;
		for (it = m_aFreeUnitClassPromotions.begin(); it != m_aFreeUnitClassPromotions.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_aVote.size();
		pStream->Write(iSize);
		std::vector< std::pair<int, PlayerVoteTypes> >::iterator it;
		for (it = m_aVote.begin(); it != m_aVote.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_aUnitExtraCosts.size();
		pStream->Write(iSize);
		std::vector< std::pair<UnitClassTypes, int> >::iterator it;
		for (it = m_aUnitExtraCosts.begin(); it != m_aUnitExtraCosts.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_triggersFired.size();
		pStream->Write(iSize);
		std::vector<EventTriggerTypes>::iterator it;
		for (it = m_triggersFired.begin(); it != m_triggersFired.end(); ++it)
		{
			pStream->Write((*it));
		}
	}

	pStream->Write(m_iPopRushHurryCount);
	pStream->Write(m_iInflationModifier);
}

void CvPlayer::createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience, int iX, int iY)
{
/************************************************************************************************/
/* GP_NAMES                                 07/2013                                 lfgr        */
/* Only GPs created here get a name (or if explicitly stated elsewhere)                         */
/************************************************************************************************/
/*
	CvUnit* pGreatPeopleUnit = initUnit(eGreatPersonUnit, iX, iY);
*/
	// If no names left, name is simply ""
	int eName = getNewGreatPersonBornName( eGreatPersonUnit );
	CvUnit* pGreatPeopleUnit = initUnit( eGreatPersonUnit, iX, iY, NO_UNITAI, NO_DIRECTION, true, false, eName );
/************************************************************************************************/
/* GP_NAMES                                END                                                  */
/************************************************************************************************/
	if (NULL == pGreatPeopleUnit)
	{
		FAssert(false);
		return;
	}

	if (bIncrementThreshold)
	{
		incrementGreatPeopleCreated();

		changeGreatPeopleThresholdModifier(GC.getDefineINT("GREAT_PEOPLE_THRESHOLD_INCREASE") * ((getGreatPeopleCreated() / 10) + 1));

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				GET_PLAYER((PlayerTypes)iI).changeGreatPeopleThresholdModifier(GC.getDefineINT("GREAT_PEOPLE_THRESHOLD_INCREASE_TEAM") * ((getGreatPeopleCreated() / 10) + 1));
			}
		}
	}

	if (bIncrementExperience)
	{
		incrementGreatGeneralsCreated();

		changeGreatGeneralsThresholdModifier(GC.getDefineINT("GREAT_GENERALS_THRESHOLD_INCREASE") * ((getGreatGeneralsCreated() / 10) + 1));

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				GET_PLAYER((PlayerTypes)iI).changeGreatGeneralsThresholdModifier(GC.getDefineINT("GREAT_GENERALS_THRESHOLD_INCREASE_TEAM") * ((getGreatGeneralsCreated() / 10) + 1));
			}
		}
	}


	CvPlot* pPlot = GC.getMapINLINE().plot(iX, iY);
	CvCity* pCity = pPlot->getPlotCity();
	CvWString szReplayMessage;

	if (pPlot)
	{
		if (pCity)
		{
			CvWString szCity;
			szCity.Format(L"%s (%s)", pCity->getName().GetCString(), GET_PLAYER(pCity->getOwnerINLINE()).getName());
			szReplayMessage = gDLL->getText("TXT_KEY_MISC_GP_BORN", pGreatPeopleUnit->getName().GetCString(), szCity.GetCString());
		}
		else
		{
			szReplayMessage = gDLL->getText("TXT_KEY_MISC_GP_BORN_FIELD", pGreatPeopleUnit->getName().GetCString());
		}
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szReplayMessage, iX, iY, (ColorTypes)GC.getInfoTypeForString("COLOR_UNIT_TEXT"));
	}

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (pPlot->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
			{
				gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szReplayMessage, "AS2D_UNIT_GREATPEOPLE", MESSAGE_TYPE_MAJOR_EVENT, pGreatPeopleUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_UNIT_TEXT"), iX, iY, true, true);
			}
			else
			{
				CvWString szMessage = gDLL->getText("TXT_KEY_MISC_GP_BORN_SOMEWHERE", pGreatPeopleUnit->getName().GetCString());
				gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szMessage, "AS2D_UNIT_GREATPEOPLE", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_UNIT_TEXT"));
			}
		}
	}

	// Python Event
	if (pCity)
	{
		CvEventReporter::getInstance().greatPersonBorn(pGreatPeopleUnit, getID(), pCity);
	}

}


const EventTriggeredData* CvPlayer::getEventOccured(EventTypes eEvent) const
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::const_iterator it = m_mapEventsOccured.find(eEvent);

	if (it == m_mapEventsOccured.end())
	{
		return NULL;
	}

	return &(it->second);
}

bool CvPlayer::isTriggerFired(EventTriggerTypes eEventTrigger) const
{
	return (std::find(m_triggersFired.begin(), m_triggersFired.end(), eEventTrigger) != m_triggersFired.end());
}

void CvPlayer::resetEventOccured(EventTypes eEvent, bool bAnnounce)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::iterator it = m_mapEventsOccured.find(eEvent);

	if (it != m_mapEventsOccured.end())
	{
		expireEvent(it->first, it->second, bAnnounce);
		m_mapEventsOccured.erase(it);
	}
}

void CvPlayer::setEventOccured(EventTypes eEvent, const EventTriggeredData& kEventTriggered, bool bOthers)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	m_mapEventsOccured[eEvent] = kEventTriggered;

	if (GC.getEventInfo(eEvent).isQuest())
	{
		CvWStringBuffer szMessageBuffer;
		szMessageBuffer.append(GC.getEventInfo(eEvent).getDescription());
		GAMETEXT.setEventHelp(szMessageBuffer, eEvent, kEventTriggered.getID(), getID());
		gDLL->getInterfaceIFace()->addQuestMessage(getID(), szMessageBuffer.getCString(), kEventTriggered.getID());
	}

	if (bOthers)
	{
		if (GC.getEventInfo(eEvent).isGlobal())
		{
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				if (i != getID())
				{
					GET_PLAYER((PlayerTypes)i).setEventOccured(eEvent, kEventTriggered, false);
				}
			}
		}
		else if (GC.getEventInfo(eEvent).isTeam())
		{
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				if (i != getID() && getTeam() == GET_PLAYER((PlayerTypes)i).getTeam())
				{
					GET_PLAYER((PlayerTypes)i).setEventOccured(eEvent, kEventTriggered, false);
				}
			}
		}
	}
}


const EventTriggeredData* CvPlayer::getEventCountdown(EventTypes eEvent) const
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::const_iterator it = m_mapEventCountdown.find(eEvent);

	if (it == m_mapEventCountdown.end())
	{
		return NULL;
	}

	return &(it->second);
}

void CvPlayer::setEventCountdown(EventTypes eEvent, const EventTriggeredData& kEventTriggered)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	m_mapEventCountdown[eEvent] = kEventTriggered;
}

void CvPlayer::resetEventCountdown(EventTypes eEvent)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::iterator it = m_mapEventCountdown.find(eEvent);

	if (it != m_mapEventCountdown.end())
	{
		m_mapEventCountdown.erase(it);
	}
}


void CvPlayer::resetTriggerFired(EventTriggerTypes eTrigger)
{
	std::vector<EventTriggerTypes>::iterator it = std::find(m_triggersFired.begin(), m_triggersFired.end(), eTrigger);

	if (it != m_triggersFired.end())
	{
		m_triggersFired.erase(it);
	}
}

void CvPlayer::setTriggerFired(const EventTriggeredData& kTriggeredData, bool bOthers, bool bAnnounce, bool bDoEffects)
{
	FAssert(kTriggeredData.m_eTrigger >= 0 && kTriggeredData.m_eTrigger < GC.getNumEventTriggerInfos());

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(kTriggeredData.m_eTrigger);

	if (!isTriggerFired(kTriggeredData.m_eTrigger))
	{
		m_triggersFired.push_back(kTriggeredData.m_eTrigger);

		if (bOthers)
		{
			if (kTrigger.isGlobal())
			{
				for (int i = 0; i < MAX_CIV_PLAYERS; i++)
				{
					if (i != getID())
					{

//						GET_PLAYER((PlayerTypes)i).setTriggerFired(kTriggeredData, false, false);
                        if (GET_PLAYER((PlayerTypes)i).isAlive())
                        {
                            GET_PLAYER((PlayerTypes)i).setTriggerFired(kTriggeredData, false, false, bDoEffects);
                        }

					}
				}
			}
			else if (kTrigger.isTeam())
			{
				for (int i = 0; i < MAX_CIV_PLAYERS; i++)
				{
					if (i != getID() && getTeam() == GET_PLAYER((PlayerTypes)i).getTeam())
					{
						GET_PLAYER((PlayerTypes)i).setTriggerFired(kTriggeredData, false, false, bDoEffects);
					}
				}
			}
		}
		//}

	//FfH: Modified by Kael 09/25/2008
		// lfgr 06/2019: Moved callback
		GC.getGameINLINE().setEventTriggered((EventTriggerTypes)kTriggeredData.m_eTrigger, true);
	//FfH: End Modify
	}
	
	// lfgr 06/2019: Apply python effects if and only if bDoEffects
	if( bDoEffects && isAlive() && !CvString(kTrigger.getPythonCallback()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(&kTriggeredData));
		argsList.add(getID());	// Player ID
		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kTrigger.getPythonCallback(), argsList.makeFunctionArgs(), &lResult);
	}
	// lfgr END

	if (bAnnounce)
	{
		CvPlot* pPlot = GC.getMapINLINE().plot(kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY);

		if (!kTriggeredData.m_szGlobalText.empty())
		{
			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

				if (kLoopPlayer.isAlive())
				{
					if (GET_TEAM(kLoopPlayer.getTeam()).isHasMet(getTeam()) && (NO_PLAYER == kTriggeredData.m_eOtherPlayer || GET_TEAM(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()).isHasMet(getTeam())))
					{
						bool bShowPlot = kTrigger.isShowPlot();

						if (bShowPlot)
						{
							if (kLoopPlayer.getTeam() != getTeam())
							{
								if (NULL == pPlot || !pPlot->isRevealed(kLoopPlayer.getTeam(), false))
								{
									bShowPlot = false;
								}
							}
						}

						if (bShowPlot)
						{
							gDLL->getInterfaceIFace()->addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY, true, true);
						}
						else
						{
							gDLL->getInterfaceIFace()->addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT);
						}
					}
				}
			}

			GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), kTriggeredData.m_szGlobalText, kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
		}
		else if (!kTriggeredData.m_szText.empty())
		{
			if (kTrigger.isShowPlot() && NULL != pPlot && pPlot->isRevealed(getTeam(), false))
			{
				gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY, true, true);
			}
			else
			{
				gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"));
			}
		}
	}
}

// lfgr cmt: here affected units, cities etc. are chosen
EventTriggeredData* CvPlayer::initTriggeredData(EventTriggerTypes eEventTrigger, bool bFire, int iCityId, int iPlotX, int iPlotY, PlayerTypes eOtherPlayer, int iOtherPlayerCityId, ReligionTypes eReligion, CorporationTypes eCorporation, int iUnitId, BuildingTypes eBuilding)
{
	// lfgr EVENT_DEBUG
//	logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\"", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType() );
	// lfgr end

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eEventTrigger);

	CvCity* pCity = getCity(iCityId);
	CvCity* pOtherPlayerCity = NULL;
	if (NO_PLAYER != eOtherPlayer)
	{
		pOtherPlayerCity = GET_PLAYER(eOtherPlayer).getCity(iOtherPlayerCityId);
	}
	CvPlot* pPlot = GC.getMapINLINE().plot(iPlotX, iPlotY);
	CvUnit* pUnit = getUnit(iUnitId);

	std::vector<CvPlot*> apPlots;
	bool bPickPlot = ::isPlotEventTrigger(eEventTrigger);

	if (kTrigger.isPickCity())
	{
		if (NULL == pCity)
		{
			pCity = pickTriggerCity(eEventTrigger); // LFGR_TODO: Pick plot at the same time, otherwise we might miss a valid combination.
		}

		if (NULL != pCity)
		{
			if (bPickPlot)
			{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//				for (int iPlot = 0; iPlot < NUM_CITY_PLOTS; ++iPlot)
				for (int iPlot = 0; iPlot < ::calculateNumCityPlots(getNextCityRadius()); ++iPlot)
//<<<<Unofficial Bug Fix: End Modify
				{
					if (CITY_HOME_PLOT != iPlot)
					{
						CvPlot* pLoopPlot = pCity->getCityIndexPlot(iPlot);

						if (NULL != pLoopPlot)
						{
							if (pLoopPlot->canTrigger(eEventTrigger, getID()))
							{
								apPlots.push_back(pLoopPlot);
							}
						}
					}
				}
			}
		}
		else
		{
			return NULL;
		}
	}
	else
	{
		if (kTrigger.getNumBuildings() > 0 && kTrigger.getNumBuildingsRequired() > 0)
		{
			int iFoundValid = 0;

			for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
			{
				if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
				{
					iFoundValid += getBuildingClassCount((BuildingClassTypes)kTrigger.getBuildingRequired(i));
				}
			}

			if (iFoundValid < kTrigger.getNumBuildings())
			{
				return NULL;
			}
		}

		if (kTrigger.getNumReligions() > 0)
		{
			int iFoundValid = 0;

			if (kTrigger.getNumReligionsRequired() > 0)
			{
				for (int i = 0; i < kTrigger.getNumReligionsRequired(); ++i)
				{
					if (kTrigger.getReligionRequired(i) != NO_RELIGION)
					{
						if (getHasReligionCount((ReligionTypes)kTrigger.getReligionRequired(i)) > 0)
						{
							++iFoundValid;
						}
					}
				}
			}
			else
			{
				for (int i = 0; i < GC.getNumReligionInfos(); ++i)
				{
					if (getHasReligionCount((ReligionTypes)i) > 0)
					{
						++iFoundValid;
					}
				}
			}

			if (iFoundValid < kTrigger.getNumReligions())
			{
				return NULL;
			}
		}

		if (kTrigger.getNumCorporations() > 0)
		{
			int iFoundValid = 0;

			if (kTrigger.getNumCorporationsRequired() > 0)
			{
				for (int i = 0; i < kTrigger.getNumCorporationsRequired(); ++i)
				{
					if (kTrigger.getCorporationRequired(i) != NO_CORPORATION)
					{
						if (getHasCorporationCount((CorporationTypes)kTrigger.getCorporationRequired(i)) > 0)
						{
							++iFoundValid;
						}
					}
				}
			}
			else
			{
				for (int i = 0; i < GC.getNumCorporationInfos(); ++i)
				{
					if (getHasCorporationCount((CorporationTypes)i) > 0)
					{
						++iFoundValid;
					}
				}
			}

			if (iFoundValid < kTrigger.getNumCorporations())
			{
				return NULL;
			}
		}

		if (kTrigger.getMinPopulation() > 0)
		{
			if (getTotalPopulation() < kTrigger.getMinPopulation())
			{
				return NULL;
			}
		}

		if (kTrigger.getMaxPopulation() > 0)
		{
			if (getTotalPopulation() > kTrigger.getMaxPopulation())
			{
				return NULL;
			}
		}

		if (bPickPlot)
		{
			for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
			{
				CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

				if (pLoopPlot->canTrigger(eEventTrigger, getID()))
				{
					apPlots.push_back(pLoopPlot);
				}
			}
		}
	}

	if (kTrigger.isPickReligion())
	{
		if (NO_RELIGION == eReligion)
		{
			if (kTrigger.isStateReligion())
			{
				ReligionTypes eStateReligion = getStateReligion();
				if (NO_RELIGION != eStateReligion && isValidTriggerReligion(kTrigger, pCity, eStateReligion))
				{
					eReligion = getStateReligion();
				}
			}
			else
			{
				int iOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumReligionInfos(), "Event pick religion");
				logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\": Picking random religion with offset: %i", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType(), iOffset);

				for (int i = 0; i < GC.getNumReligionInfos(); ++i)
				{
					int iReligion = (i + iOffset) % GC.getNumReligionInfos();

					if (isValidTriggerReligion(kTrigger, pCity, (ReligionTypes)iReligion))
					{
						eReligion = (ReligionTypes)iReligion;
						break;
					}
				}
			}
		}

		if (NO_RELIGION == eReligion)
		{
			return NULL;
		}
	}

	if (kTrigger.isPickCorporation())
	{
		if (NO_CORPORATION == eCorporation)
		{
			int iOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumCorporationInfos(), "Event pick corporation");
			logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\": Picking random corporation with offset: %i", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType(), iOffset);

			for (int i = 0; i < GC.getNumCorporationInfos(); ++i)
			{
				int iCorporation = (i + iOffset) % GC.getNumCorporationInfos();

				if (isValidTriggerCorporation(kTrigger, pCity, (CorporationTypes)iCorporation))
				{
					eCorporation = (CorporationTypes)iCorporation;
					break;
				}
			}
		}

		if (NO_CORPORATION == eCorporation)
		{
			return NULL;
		}
	}

	if (NULL == pPlot)
	{
		if (apPlots.size() > 0)
		{
			int iChosen = GC.getGameINLINE().getSorenRandNum(apPlots.size(), "Event pick plot");
			logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\": Picking random plot: %i", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType(), iChosen);
			pPlot = apPlots[iChosen];

			if (NULL == pCity)
			{
				pCity = GC.getMapINLINE().findCity(pPlot->getX_INLINE(), pPlot->getY_INLINE(), getID(), NO_TEAM, false);
			}
		}
		else
		{
			if (bPickPlot)
			{
				return NULL;
			}

			if (NULL != pCity)
			{
				pPlot = pCity->plot();
			}
		}
	}

	if (kTrigger.getNumBuildings() > 0)
	{
		if (NULL != pCity && NO_BUILDING == eBuilding)
		{
			std::vector<BuildingTypes> aeBuildings;
			for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
			{
				if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
				{
					BuildingTypes eTestBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(kTrigger.getBuildingRequired(i));
					if (NO_BUILDING != eTestBuilding && pCity->getNumRealBuilding(eTestBuilding) > 0)
					{
						aeBuildings.push_back(eTestBuilding);
					}
				}
			}

			if (aeBuildings.size() > 0)
			{
				int iChosen = GC.getGameINLINE().getSorenRandNum(aeBuildings.size(), "Event pick building");
				logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\": Picking random building: %i", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType(), iChosen);
				eBuilding = aeBuildings[iChosen];
			}
			else
			{
				return NULL;
			}
		}
	}

	if (NULL == pUnit)
	{
		pUnit = pickTriggerUnit(eEventTrigger, pPlot, bPickPlot);
	}

	if (NULL == pUnit && kTrigger.getNumUnits() > 0)
	{
		return NULL;
	}

	if (NULL == pPlot && NULL != pUnit)
	{
		pPlot = pUnit->plot();
	}

	if (NULL == pPlot && bPickPlot)
	{
		return NULL;
	}

	// LFGR_TODO: kTrigger.getNumUnits() > 0 ? (kTrigger.getNumUnits() <= 0 -> pLoopUnit->getTriggerValue() == MIN_INT)
	if (kTrigger.getNumUnitsGlobal() > 0)
	{
		int iNumUnits = 0;
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

			if (kLoopPlayer.isAlive())
			{
				int iLoop;
				for (CvUnit* pLoopUnit = kLoopPlayer.firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = kLoopPlayer.nextUnit(&iLoop))
				{
					if (MIN_INT != pLoopUnit->getTriggerValue(eEventTrigger, pPlot, true))
					{
						++iNumUnits;
					}
				}
			}
		}

		if (iNumUnits < kTrigger.getNumUnitsGlobal())
		{
			return NULL;
		}
	}

	if (kTrigger.getNumBuildingsGlobal() > 0)
	{
		int iNumBuildings = 0;
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

			if (kLoopPlayer.isAlive())
			{
				for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
				{
					if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
					{
						iNumBuildings += getBuildingClassCount((BuildingClassTypes)kTrigger.getBuildingRequired(i));
					}
				}
			}
		}

		if (iNumBuildings < kTrigger.getNumBuildingsGlobal())
		{
			return NULL;
		}
	}

	if (kTrigger.isPickPlayer())
	{
		std::vector<PlayerTypes> aePlayers;
		std::vector<CvCity*> apCities;

		if (NO_PLAYER == eOtherPlayer)
		{
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				if (GET_PLAYER((PlayerTypes)i).canTrigger(eEventTrigger, getID(), eReligion))
				{
					if (kTrigger.isPickOtherPlayerCity())
					{
						CvCity* pBestCity = NULL;

						if (NULL != pCity)
						{
							pBestCity = GC.getMapINLINE().findCity(pCity->getX_INLINE(), pCity->getY_INLINE(), (PlayerTypes)i);
						}
						else
						{
							pBestCity = GET_PLAYER((PlayerTypes)i).pickTriggerCity(eEventTrigger);
						}

						if (NULL != pBestCity)
						{
							apCities.push_back(pBestCity);
							aePlayers.push_back((PlayerTypes)i);
						}
					}
					else
					{
						apCities.push_back(NULL);
						aePlayers.push_back((PlayerTypes)i);
					}
				}
			}

			if (aePlayers.size() > 0)
			{
				int iChosen = GC.getGameINLINE().getSorenRandNum(aePlayers.size(), "Event pick player");
				logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\": Picking random player: %i", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType(), iChosen);
				eOtherPlayer = aePlayers[iChosen];
				pOtherPlayerCity = apCities[iChosen];
			}
			else
			{
				return NULL;
			}
		}
	}

	EventTriggeredData* pTriggerData = addEventTriggered();

	if (NULL != pTriggerData)
	{
		pTriggerData->m_eTrigger = eEventTrigger;
		pTriggerData->m_ePlayer = getID();
		pTriggerData->m_iTurn = GC.getGameINLINE().getGameTurn();
		pTriggerData->m_iCityId = (NULL != pCity) ? pCity->getID() : -1;
		pTriggerData->m_iPlotX = (NULL != pPlot) ? pPlot->getX_INLINE() : INVALID_PLOT_COORD;
		pTriggerData->m_iPlotY = (NULL != pPlot) ? pPlot->getY_INLINE() : INVALID_PLOT_COORD;
		pTriggerData->m_eOtherPlayer = eOtherPlayer;
		pTriggerData->m_iOtherPlayerCityId = (NULL != pOtherPlayerCity) ? pOtherPlayerCity->getID() : -1;
		pTriggerData->m_eReligion = eReligion;
		pTriggerData->m_eCorporation = eCorporation;
		pTriggerData->m_iUnitId = (NULL != pUnit) ? pUnit->getID() : -1;
		pTriggerData->m_eBuilding = eBuilding;
	}
	else
	{
		return NULL;
	}
	
/************************************************************************************************/
/* EVENT_NEW_TAGS                          01/2014                                  lfgr        */
/************************************************************************************************/
	if( kTrigger.isRequiresValidEvent() )
	{
		bool bValidEvent = false;
		for( int i = 0; i < kTrigger.getNumEvents(); i++ )
		{
			if( canDoEvent( (EventTypes) kTrigger.getEvent( i ), *pTriggerData ) )
			{
				bValidEvent = true;
				break;
			}
		}
		if( !bValidEvent )
		{
			deleteEventTriggered(pTriggerData->getID());
			return NULL;
		}
	}
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/
	
	if (!CvString(kTrigger.getPythonCanDo()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pTriggerData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kTrigger.getPythonCanDo(), argsList.makeFunctionArgs(), &lResult);

		if (0 == lResult)
		{
			deleteEventTriggered(pTriggerData->getID());
			return NULL;
		}

		// python may change pTriggerData
		pCity = getCity(pTriggerData->m_iCityId);
		pPlot = GC.getMapINLINE().plot(pTriggerData->m_iPlotX, pTriggerData->m_iPlotY);
		pUnit = getUnit(pTriggerData->m_iUnitId);
		eOtherPlayer = pTriggerData->m_eOtherPlayer;
		if (NO_PLAYER != eOtherPlayer)
		{
			pOtherPlayerCity = GET_PLAYER(eOtherPlayer).getCity(pTriggerData->m_iOtherPlayerCityId);
		}
		eReligion = pTriggerData->m_eReligion;
		eCorporation = pTriggerData->m_eCorporation;
		eBuilding = pTriggerData->m_eBuilding;
	}

	std::vector<CvWString> aszTexts;
	for (int i = 0; i < kTrigger.getNumTexts(); ++i)
	{
		if (NO_ERA == kTrigger.getTextEra(i) || kTrigger.getTextEra(i) == getCurrentRealEra())
		{
			aszTexts.push_back(kTrigger.getText(i));
		}
	}

	if (aszTexts.size() > 0)
	{
		int iText = GC.getGameINLINE().getSorenRandNum(aszTexts.size(), "Event Text choice");
		logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\": Picking event text choice: %i", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType(), iText);

		pTriggerData->m_szText = gDLL->getText(aszTexts[iText].GetCString(),
			eOtherPlayer != NO_PLAYER ? GET_PLAYER(eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pCity ? pCity->getNameKey() : L"",
			NULL != pUnit ? pUnit->getNameKey() : L"",
			NO_RELIGION != eReligion ? GC.getReligionInfo(eReligion).getAdjectiveKey() : L"",
			NO_BUILDING != eBuilding ? GC.getBuildingInfo(eBuilding).getTextKeyWide() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			NULL != pPlot && NO_TERRAIN != pPlot->getTerrainType() ? GC.getTerrainInfo(pPlot->getTerrainType()).getTextKeyWide() : L"",
			NULL != pPlot && NO_IMPROVEMENT != pPlot->getImprovementType() ? GC.getImprovementInfo(pPlot->getImprovementType()).getTextKeyWide() : L"",
			NULL != pPlot && NO_BONUS != pPlot->getBonusType() ? GC.getBonusInfo(pPlot->getBonusType()).getTextKeyWide() : L"",
			NULL != pPlot && NO_ROUTE != pPlot->getRouteType() ? GC.getRouteInfo(pPlot->getRouteType()).getTextKeyWide() : L"",
			NO_CORPORATION != eCorporation ? GC.getCorporationInfo(eCorporation).getTextKeyWide() : L""
			);

	}
	else
	{
		pTriggerData->m_szText = L"";
	}

	if (kTrigger.getNumWorldNews() > 0)
	{
		int iText = GC.getGameINLINE().getSorenRandNum(kTrigger.getNumWorldNews(), "Trigger World News choice");
		logBBAI( "EVENT_DEBUG - initTriggeredData #%d \"%s\": Picking world news text choice: %i", eEventTrigger, GC.getEventTriggerInfo( eEventTrigger ).getType(), iText);

		pTriggerData->m_szGlobalText = gDLL->getText(kTrigger.getWorldNews(iText).GetCString(),
			getCivilizationAdjectiveKey(),
			NULL != pCity ? pCity->getNameKey() : L"",
			pTriggerData->m_eReligion != NO_RELIGION ? GC.getReligionInfo(pTriggerData->m_eReligion).getAdjectiveKey() : L"",
			eOtherPlayer != NO_PLAYER ? GET_PLAYER(eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			pTriggerData->m_eCorporation != NO_CORPORATION ? GC.getCorporationInfo(pTriggerData->m_eCorporation).getTextKeyWide() : L""
			);
	}
	else
	{
		pTriggerData->m_szGlobalText.clear();
	}

	if (bFire)
	{
		trigger(*pTriggerData);
	}

	return pTriggerData;
}


bool CvPlayer::canDoEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const
{
	if (eEvent == NO_EVENT)
	{
		FAssert(false);
		return false;
	}

	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	int iGold = std::min(getEventCost(eEvent, kTriggeredData.m_eOtherPlayer, false), getEventCost(eEvent, kTriggeredData.m_eOtherPlayer, true));

	if (iGold != 0)
	{
		if (iGold > 0 && NO_PLAYER != kTriggeredData.m_eOtherPlayer && kEvent.isGoldToPlayer())
		{
			if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).getGold() < iGold)
			{
				return false;
			}
		}
		else if (iGold < 0)
		{
			if (getGold() < -iGold)
			{
				return false;
			}
		}
	}

	if (0 != kEvent.getSpaceProductionModifier())
	{
		bool bValid = false;
		for (int iProject = 0; iProject < GC.getNumProjectInfos(); ++iProject)
		{
			CvProjectInfo& kProject = GC.getProjectInfo((ProjectTypes)iProject);
			if (kProject.isSpaceship())
			{
				if (kProject.getVictoryPrereq() != NO_VICTORY)
				{
					if (GC.getGameINLINE().isVictoryValid((VictoryTypes)(kProject.getVictoryPrereq())))
					{
						bValid = true;
						break;
					}
				}
			}
		}

		if (!bValid)
		{
			return false;
		}
	}

	if (kEvent.getEspionagePoints() > 0 && GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		return false;
	}

	if (NO_PLAYER != kTriggeredData.m_eOtherPlayer)
	{
		if (kEvent.getEspionagePoints() + GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()) < 0)
		{
			return false;
		}
	}

	if (0 != kEvent.getTechPercent() || 0 != kEvent.getTechCostPercent())
	{
		if (NO_TECH == getBestEventTech(eEvent, kTriggeredData.m_eOtherPlayer))
		{
			return false;
		}
	}

	if (NO_TECH != kEvent.getPrereqTech())
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)kEvent.getPrereqTech()))
		{
			return false;
		}
	}

	if (NO_BONUS != kEvent.getBonusGift())
	{
		BonusTypes eBonus = (BonusTypes)kEvent.getBonusGift();
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		if (!canTradeNetworkWith(kTriggeredData.m_eOtherPlayer))
		{
			return false;
		}

		if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).getNumAvailableBonuses(eBonus) > 0)
		{
			return false;
		}

		if (getNumTradeableBonuses(eBonus) <= 1)
		{
			return false;
		}
	}

	if (kEvent.getUnitClass() != NO_UNITCLASS)
	{
		UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(kEvent.getUnitClass());
		if (eUnit == NO_UNIT)
		{
			return false;
		}
	}

// UNIVERSAL_PREREQS 07/2019 lfgr
	if( kEvent.getGamePrereq() != NULL ) {
		if( ! kEvent.getGamePrereq()->isValid( &( GC.getGameINLINE() ) ) ) {
			return false;
		}
	}

	if( kEvent.getPlayerPrereq() != NULL ) {
		if( ! kEvent.getPlayerPrereq()->isValid( this ) ) {
			return false;
		}
	}
// UNIVERSAL_PREREQS end

	if (kEvent.isCityEffect())
	{
		CvCity* pCity =	getCity(kTriggeredData.m_iCityId);
		if (NULL == pCity || !pCity->canApplyEvent(eEvent, kTriggeredData))
		{
			return false;
		}
	}
	else if (kEvent.isOtherPlayerCityEffect())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		CvCity* pCity = GET_PLAYER(kTriggeredData.m_eOtherPlayer).getCity(kTriggeredData.m_iOtherPlayerCityId);
		if (NULL == pCity || !pCity->canApplyEvent(eEvent, kTriggeredData))
		{
			return false;
		}
	}

	if (::isPlotEventTrigger(kTriggeredData.m_eTrigger))
	{
		CvPlot* pPlot = GC.getMapINLINE().plotINLINE(kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY);
		if (NULL != pPlot)
		{
			if (!pPlot->canApplyEvent(eEvent))
			{
				return false;
			}
		}
	}

	CvUnit* pUnit = getUnit(kTriggeredData.m_iUnitId);
	if (NULL != pUnit)
	{
		if (!pUnit->canApplyEvent(eEvent))
		{
			return false;
		}
	}

	if (NO_BONUS != kEvent.getBonusRevealed())
	{
		if (GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBonusInfo((BonusTypes)kEvent.getBonusRevealed()).getTechReveal()))
		{
			return false;
		}

		if (GET_TEAM(getTeam()).isForceRevealedBonus((BonusTypes)kEvent.getBonusRevealed()))
		{
			return false;
		}
	}

	if (kEvent.getConvertOwnCities() > 0)
	{
		bool bFoundValid = false;

		if (NO_RELIGION != kTriggeredData.m_eReligion)
		{
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				if (!pLoopCity->isHasReligion(kTriggeredData.m_eReligion))
				{
					if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
					{
						bFoundValid = true;
						break;
					}
				}
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (kEvent.getConvertOtherCities() > 0)
	{
		bool bFoundValid = false;

		if (NO_RELIGION != kTriggeredData.m_eReligion)
		{
			if (NO_PLAYER != kTriggeredData.m_eOtherPlayer)
			{
				int iLoop;
				for (CvCity* pLoopCity = GET_PLAYER(kTriggeredData.m_eOtherPlayer).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(kTriggeredData.m_eOtherPlayer).nextCity(&iLoop))
				{
					if (!pLoopCity->isHasReligion(kTriggeredData.m_eReligion))
					{
						if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
						{
							bFoundValid = true;
							break;
						}
					}
				}
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (0 != kEvent.getAttitudeModifier())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam() == getTeam())
		{
			return false;
		}

		if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).isHuman())
		{
			if (0 == kEvent.getOurAttitudeModifier())
			{
				return false;
			}
		}
	}

	if (0 != kEvent.getTheirEnemyAttitudeModifier())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		TeamTypes eWorstEnemy = GET_TEAM(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
		if (NO_TEAM == eWorstEnemy || eWorstEnemy == getTeam())
		{
			return false;
		}

		if (!GET_TEAM(eWorstEnemy).isAlive())
		{
			return false;
		}

		if (eWorstEnemy == getTeam())
		{
			return false;
		}
	}

	if (kEvent.isDeclareWar())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		if (!GET_TEAM(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()).canDeclareWar(getTeam()) || !GET_TEAM(getTeam()).canDeclareWar(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()))
		{
			return false;
		}
	}

	if (kEvent.isQuest())
	{
		for (int iTrigger = 0; iTrigger < GC.getNumEventTriggerInfos(); ++iTrigger)
		{
			CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo((EventTriggerTypes)iTrigger);
			if (!kTrigger.isRecurring())
			{
				for (int i = 0; i < kTrigger.getNumPrereqEvents(); ++i)
				{
					if (kTrigger.getPrereqEvent(i) == eEvent)
					{
						if (isTriggerFired((EventTriggerTypes)iTrigger))
						{
							return false;
						}
					}
				}
			}
		}
	}

//FfH: Added by Kael 01/21/2008
	if (kEvent.getPrereqAlignment() != NO_ALIGNMENT)
	{
        if (getAlignment() != kEvent.getPrereqAlignment())
        {
            return false;
		}
	}
	if (kEvent.getPrereqBonus() != NO_BONUS)
	{
        if (!hasBonus((BonusTypes)kEvent.getPrereqBonus()))
        {
            return false;
		}
	}
	if (kEvent.getPrereqCivilization() != NO_CIVILIZATION)
	{
        if (getCivilizationType() != kEvent.getPrereqCivilization())
        {
            return false;
		}
	}
	if (kEvent.getPrereqCorporation() != NO_CORPORATION)
	{
		CvCity* pCity =	getCity(kTriggeredData.m_iCityId);
		if (pCity != NULL)
		{
            if (!pCity->isHasCorporation((CorporationTypes)kEvent.getPrereqCorporation()))
           {
                return false;
            }
		}
	}
	if (kEvent.getPrereqReligion() != NO_RELIGION)
	{
		CvCity* pCity =	getCity(kTriggeredData.m_iCityId);
		if (pCity != NULL)
		{
            if (!pCity->isHasReligion((ReligionTypes)kEvent.getPrereqReligion()))
            {
                return false;
            }
		}
	}
	if (kEvent.getPrereqStateReligion() != NO_RELIGION)
	{
        if (getStateReligion() != kEvent.getPrereqStateReligion())
        {
            return false;
		}
	}
//FfH: End Add

	if (!CvString(kEvent.getPythonCanDo()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eEvent);
		argsList.add(gDLL->getPythonIFace()->makePythonObject(&kTriggeredData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kEvent.getPythonCanDo(), argsList.makeFunctionArgs(), &lResult);

		if (0 == lResult)
		{
			return false;
		}
	}

	return true;
}


void CvPlayer::applyEvent(EventTypes eEvent, int iEventTriggeredId, bool bUpdateTrigger)
{
	FAssert(eEvent != NO_EVENT);

	EventTriggeredData* pTriggeredData = getEventTriggered(iEventTriggeredId);

	if (NULL == pTriggeredData)
	{
		deleteEventTriggered(iEventTriggeredId);
		return;
	}
	else
	{
		//logBBAI("    Event Trigger - %S", GC.getEventInfo((EventTypes)iEventTriggeredId).getDescription());
	}

	logBBAI("    Event result - %S", GC.getEventInfo((EventTypes)eEvent).getDescription() );

	if (bUpdateTrigger)
	{
		setTriggerFired(*pTriggeredData, true);
	}

	if (!canDoEvent(eEvent, *pTriggeredData))
	{
		if (bUpdateTrigger)
		{
			deleteEventTriggered(iEventTriggeredId);
		}
		return;
	}

	setEventOccured(eEvent, *pTriggeredData);

	CvEventInfo& kEvent = GC.getEventInfo(eEvent);
	CvCity* pCity =	getCity(pTriggeredData->m_iCityId);
	CvCity* pOtherPlayerCity = NULL;

	if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
	{
		pOtherPlayerCity = GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCity(pTriggeredData->m_iOtherPlayerCityId);
	}

	int iGold = getEventCost(eEvent, pTriggeredData->m_eOtherPlayer, false);
	int iRandomGold = getEventCost(eEvent, pTriggeredData->m_eOtherPlayer, true);

	iGold += GC.getGameINLINE().getSorenRandNum(iRandomGold - iGold + 1, "Event random gold");

	if (iGold != 0)
	{
		changeGold(iGold);

		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer && kEvent.isGoldToPlayer())
		{
			GET_PLAYER(pTriggeredData->m_eOtherPlayer).changeGold(-iGold);
		}
	}

	if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
	{
		if (kEvent.getEspionagePoints() != 0)
		{
			GET_TEAM(getTeam()).changeEspionagePointsAgainstTeam(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam(), kEvent.getEspionagePoints());
		}
	}

	if (0 != kEvent.getTechPercent())
	{
		TechTypes eBestTech = getBestEventTech(eEvent, pTriggeredData->m_eOtherPlayer);

		if (eBestTech != NO_TECH)
		{
			int iBeakers  = GET_TEAM(getTeam()).changeResearchProgressPercent(eBestTech, kEvent.getTechPercent(), getID());

			if (iBeakers > 0)
			{
				for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						if (GET_PLAYER((PlayerTypes)iI).getTeam() == getID())
						{
							CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_PROGRESS_TOWARDS_TECH", iBeakers, GC.getTechInfo(eBestTech).getTextKeyWide());

							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, NULL, MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_TECH_TEXT"));
						}
					}
				}
			}
		}
	}

	if (kEvent.isGoldenAge())
	{
		changeGoldenAgeTurns(getGoldenAgeLength());
	}

	if (0 != kEvent.getInflationModifier())
	{
		changeInflationModifier( kEvent.getInflationModifier() ); // lfgr 05/2022
	}

	if (0 != kEvent.getSpaceProductionModifier())
	{
		changeSpaceProductionModifier(kEvent.getSpaceProductionModifier());
	}

	if (0 != kEvent.getFreeUnitSupport())
	{
		changeBaseFreeUnits(kEvent.getFreeUnitSupport());
	}

	if (kEvent.isDeclareWar())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/02/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("    Team %d (%S) declares war on team %d due to event", GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam(), GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationDescription(0), getTeam() );
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
			GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).declareWar(getTeam(), false, WARPLAN_LIMITED);
		}
	}

	if (NO_BONUS != kEvent.getBonusGift())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			CLinkList<TradeData> ourList;
			CLinkList<TradeData> theirList;
			TradeData kTradeData;
			setTradeItem(&kTradeData, TRADE_RESOURCES, kEvent.getBonusGift());
			ourList.insertAtEnd(kTradeData);
			GC.getGameINLINE().implementDeal(getID(), pTriggeredData->m_eOtherPlayer, &ourList, &theirList);
		}
	}

	bool bClear = false;
	for (int iEvent = 0; iEvent < GC.getNumEventInfos(); ++iEvent)
	{
		if (kEvent.getClearEventChance(iEvent) > 0)
		{
			bClear = GC.getGameINLINE().getSorenRandNum(100, "Event Clear") < kEvent.getClearEventChance(iEvent);
			if (bClear)
			{
				if (kEvent.isGlobal())
				{
					for (int j = 0; j < MAX_CIV_PLAYERS; j++)
					{
						GET_PLAYER((PlayerTypes)j).resetEventOccured((EventTypes)iEvent, j != getID());
					}
				}
				else if (kEvent.isTeam())
				{
					for (int j = 0; j < MAX_CIV_PLAYERS; j++)
					{
						if (getTeam() == GET_PLAYER((PlayerTypes)j).getTeam())
						{
							GET_PLAYER((PlayerTypes)j).resetEventOccured((EventTypes)iEvent, j != getID());
						}
					}
				}
				else
				{
					resetEventOccured((EventTypes)iEvent, false);
				}
			}
		}
	}

	if (NULL != pCity && kEvent.isCityEffect())
	{
		pCity->applyEvent(eEvent, *pTriggeredData, bClear);
	}
	else if (NULL != pOtherPlayerCity && kEvent.isOtherPlayerCityEffect())
	{
		pOtherPlayerCity->applyEvent(eEvent, *pTriggeredData, bClear);
	}

	if (!kEvent.isCityEffect() && !kEvent.isOtherPlayerCityEffect())
	{
		if (kEvent.getHappy() != 0)
		{
			changeExtraHappiness(kEvent.getHappy());
		}

		if (kEvent.getHealth() != 0)
		{
			changeExtraHealth(kEvent.getHealth());
		}

		if (kEvent.getNumBuildingYieldChanges() > 0)
		{
			int iLoop;
			for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
			{
				for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
				{
					for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
					{
						pLoopCity->changeBuildingYieldChange((BuildingClassTypes)iBuildingClass, (YieldTypes)iYield, kEvent.getBuildingYieldChange(iBuildingClass, iYield));
					}
				}
			}
		}

		if (kEvent.getNumBuildingCommerceChanges() > 0)
		{
			int iLoop;
			for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
			{
				for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
				{
					for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
					{
						pLoopCity->changeBuildingCommerceChange((BuildingClassTypes)iBuildingClass, (CommerceTypes)iCommerce, kEvent.getBuildingCommerceChange(iBuildingClass, iCommerce));
					}
				}
			}
		}

		if (kEvent.getNumBuildingHappyChanges() > 0)
		{
			for (int i = 0; i < GC.getNumBuildingClassInfos(); ++i)
			{
				if (0 != kEvent.getBuildingHappyChange(i))
				{
					BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(i);
					if (NO_BUILDING != eBuilding)
					{
						changeExtraBuildingHappiness(eBuilding, kEvent.getBuildingHappyChange(i));
					}
				}
			}
		}

		if (kEvent.getNumBuildingHealthChanges() > 0)
		{
			for (int i = 0; i < GC.getNumBuildingClassInfos(); ++i)
			{
				if (0 != kEvent.getBuildingHealthChange(i))
				{
					BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(i);
					if (NO_BUILDING != eBuilding)
					{
						changeExtraBuildingHealth(eBuilding, kEvent.getBuildingHealthChange(i));
					}
				}
			}
		}

		if (kEvent.getHurryAnger() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeHurryAngerTimer(kEvent.getHurryAnger() * pLoopCity->flatHurryAngerLength());
			}
		}

		if (kEvent.getHappyTurns() > 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeHappinessTimer(kEvent.getHappyTurns());
			}
		}

		if (kEvent.getMaxPillage() > 0)
		{
			FAssert(kEvent.getMaxPillage() >= kEvent.getMinPillage());
			int iNumPillage = kEvent.getMinPillage() + GC.getGameINLINE().getSorenRandNum(kEvent.getMaxPillage() - kEvent.getMinPillage(), "Pick number of event pillaged plots");

			int iNumPillaged = 0;
			for (int i = 0; i < iNumPillage; ++i)
			{
				int iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getMapINLINE().numPlotsINLINE(), "Pick event pillage plot (any city)");
				for (int j = 0; j < GC.getMapINLINE().numPlotsINLINE(); ++j)
				{
					int iPlot = (j + iRandOffset) % GC.getMapINLINE().numPlotsINLINE();
					CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);
					if (NULL != pPlot && pPlot->getOwnerINLINE() == getID() && pPlot->isCity())
					{
						if (NO_IMPROVEMENT != pPlot->getImprovementType() && !GC.getImprovementInfo(pPlot->getImprovementType()).isPermanent())
						{
							CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", GC.getImprovementInfo(pPlot->getImprovementType()).getTextKeyWide());
							gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO, GC.getImprovementInfo(pPlot->getImprovementType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), pPlot->getX_INLINE(), pPlot->getY_INLINE(), true, true);
							pPlot->setImprovementType(NO_IMPROVEMENT);
							++iNumPillaged;
							break;
						}
					}
				}
			}

			if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
			{
				CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_NUM_CITY_IMPROVEMENTS_DESTROYED", iNumPillaged, getCivilizationAdjectiveKey());
				gDLL->getInterfaceIFace()->addMessage(pTriggeredData->m_eOtherPlayer, false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO);
			}
		}

		if (kEvent.getFood() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeFood(kEvent.getFood());
			}
		}

		if (kEvent.getFoodPercent() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeFood((pLoopCity->getFood() * kEvent.getFoodPercent()) / 100);
			}
		}

		if (kEvent.getPopulationChange() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->getPopulation() + kEvent.getPopulationChange() > 0)
				{
					pLoopCity->changePopulation(kEvent.getPopulationChange());
				}
			}
		}

		if (kEvent.getCulture() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->getCultureTimes100(pLoopCity->getOwnerINLINE()) + 100 * kEvent.getCulture() > 0)
				{
					pLoopCity->changeCulture(pLoopCity->getOwnerINLINE(), kEvent.getCulture(), true, true);
				}
			}
		}

		if (kEvent.getUnitClass() != NO_UNITCLASS)
		{
			UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(kEvent.getUnitClass());
			if (eUnit != NO_UNIT)
			{
				CvCity* pUnitCity = pCity;

				if (NULL == pUnitCity)
				{
					pUnitCity = getCapitalCity();
				}

				if (NULL != pUnitCity)
				{
					for (int i = 0; i < kEvent.getNumUnits(); ++i)
					{

//FfH: Modified by Kael 10/29/2007
//						initUnit(eUnit, pUnitCity->getX_INLINE(), pUnitCity->getY_INLINE());
                        CvUnit* pUnit = initUnit(eUnit, pUnitCity->getX_INLINE(), pUnitCity->getY_INLINE());
                        if (kEvent.getUnitPromotion() != NO_PROMOTION)
                        {
                            pUnit->setHasPromotion((PromotionTypes)kEvent.getUnitPromotion(), true);
                        }
/************************************************************************************************/
/* EVENT_NEW_TAGS                           01/21/13                                lfgr        */
/************************************************************************************************/
						for( int i = 0; i < GC.getNumPromotionInfos(); i++ )
							if( kEvent.isUnitPromotion( i ) )
							{
								pUnit->setHasPromotion((PromotionTypes)i, true);
							}
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/
                        if (kEvent.getUnitExperience() != 0)
                        {
                            pUnit->changeExperience(kEvent.getUnitExperience());
                        }
//FfH: End Modify
						// EVENTS_ENHANCED 02/2021 lfgr: Apply UnitName also to new units
						CvWString szNameKey(kEvent.getUnitNameKey());
						if (!szNameKey.empty())
						{
							pUnit->setName(gDLL->getText(szNameKey));
						}
					}
				}
			}
		}
	}

	CvPlot* pPlot = GC.getMapINLINE().plotINLINE(pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY);
	if (NULL != pPlot)
	{
		if (::isPlotEventTrigger(pTriggeredData->m_eTrigger))
		{
			FAssert(pPlot->canApplyEvent(eEvent));
			pPlot->applyEvent(eEvent);
		}
	}

	CvUnit* pUnit = getUnit(pTriggeredData->m_iUnitId);
	if (NULL != pUnit)
	{
		FAssert(pUnit->canApplyEvent(eEvent));
		pUnit->applyEvent(eEvent);   // might kill the unit
	}

	for (int i = 0; i < GC.getNumUnitCombatInfos(); ++i)
	{
		if (NO_PROMOTION != kEvent.getUnitCombatPromotion(i))
		{
			int iLoop;
			for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
			{
				if (pLoopUnit->getUnitCombatType() == i)
				{
					pLoopUnit->setHasPromotion((PromotionTypes)kEvent.getUnitCombatPromotion(i), true);
				}
			}

			setFreePromotion((UnitCombatTypes)i, (PromotionTypes)kEvent.getUnitCombatPromotion(i), true);
		}
	}

	for (int i = 0; i < GC.getNumUnitClassInfos(); ++i)
	{
		if (NO_PROMOTION != kEvent.getUnitClassPromotion(i))
		{
			int iLoop;
			for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
			{
				if (pLoopUnit->getUnitClassType() == i)
				{
					pLoopUnit->setHasPromotion((PromotionTypes)kEvent.getUnitClassPromotion(i), true);
				}
			}

			setFreePromotion((UnitClassTypes)i, (PromotionTypes)kEvent.getUnitClassPromotion(i), true);
		}
	}

	if (NO_BONUS != kEvent.getBonusRevealed())
	{
		GET_TEAM(getTeam()).setForceRevealedBonus((BonusTypes)kEvent.getBonusRevealed(), true);
	}

	std::vector<CvCity*> apSpreadReligionCities;

	if (kEvent.getConvertOwnCities() > 0)
	{
		if (NO_RELIGION != pTriggeredData->m_eReligion)
		{
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				if (!pLoopCity->isHasReligion(pTriggeredData->m_eReligion))
				{
					if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
					{
						apSpreadReligionCities.push_back(pLoopCity);
					}
				}
			}
		}
	}

	while ((int)apSpreadReligionCities.size() > kEvent.getConvertOwnCities())
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apSpreadReligionCities.size(), "Even Spread Religion (own)");

		int i = 0;
		for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
		{
			if (i == iChosen)
			{
				apSpreadReligionCities.erase(it);
				break;
			}
			++i;
		}
	}

	for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
	{
		(*it)->setHasReligion(pTriggeredData->m_eReligion, true, true, false);
	}

	apSpreadReligionCities.clear();

	if (kEvent.getConvertOtherCities() > 0)
	{
		if (NO_RELIGION != pTriggeredData->m_eReligion)
		{
			if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
			{
				std::vector<CvCity*> apCities;
				int iLoop;
				for (CvCity* pLoopCity = GET_PLAYER(pTriggeredData->m_eOtherPlayer).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(pTriggeredData->m_eOtherPlayer).nextCity(&iLoop))
				{
					if (!pLoopCity->isHasReligion(pTriggeredData->m_eReligion))
					{
						if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
						{
							apSpreadReligionCities.push_back(pLoopCity);
						}
					}
				}
			}
		}
	}

	while ((int)apSpreadReligionCities.size() > kEvent.getConvertOtherCities())
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apSpreadReligionCities.size(), "Even Spread Religion (other)");

		int i = 0;
		for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
		{
			if (i == iChosen)
			{
				apSpreadReligionCities.erase(it);
				break;
			}
			++i;
		}
	}

	for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
	{
		(*it)->setHasReligion(pTriggeredData->m_eReligion, true, true, false);
	}

	if (0 != kEvent.getOurAttitudeModifier())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			if (kEvent.getOurAttitudeModifier() > 0)
			{
				AI_changeMemoryCount(pTriggeredData->m_eOtherPlayer, MEMORY_EVENT_GOOD_TO_US, kEvent.getOurAttitudeModifier());
			}
			else
			{
				AI_changeMemoryCount(pTriggeredData->m_eOtherPlayer, MEMORY_EVENT_BAD_TO_US, -kEvent.getOurAttitudeModifier());
			}
		}
	}

	if (0 != kEvent.getAttitudeModifier())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			if (kEvent.getAttitudeModifier() > 0)
			{
				GET_PLAYER(pTriggeredData->m_eOtherPlayer).AI_changeMemoryCount(getID(), MEMORY_EVENT_GOOD_TO_US, kEvent.getAttitudeModifier());
			}
			else
			{
				GET_PLAYER(pTriggeredData->m_eOtherPlayer).AI_changeMemoryCount(getID(), MEMORY_EVENT_BAD_TO_US, -kEvent.getAttitudeModifier());
			}
		}
	}

	if (0 != kEvent.getTheirEnemyAttitudeModifier())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			TeamTypes eWorstEnemy = GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
			if (NO_TEAM != eWorstEnemy)
			{
				for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
				{
					CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
					if (kLoopPlayer.isAlive() && kLoopPlayer.getTeam() == eWorstEnemy)
					{
						if (kEvent.getTheirEnemyAttitudeModifier() > 0)
						{
							kLoopPlayer.AI_changeMemoryCount(getID(), MEMORY_EVENT_GOOD_TO_US, kEvent.getTheirEnemyAttitudeModifier());
							AI_changeMemoryCount((PlayerTypes)iPlayer, MEMORY_EVENT_GOOD_TO_US, kEvent.getTheirEnemyAttitudeModifier());
						}
						else
						{
							kLoopPlayer.AI_changeMemoryCount(getID(), MEMORY_EVENT_BAD_TO_US, -kEvent.getTheirEnemyAttitudeModifier());
							AI_changeMemoryCount((PlayerTypes)iPlayer, MEMORY_EVENT_BAD_TO_US, -kEvent.getTheirEnemyAttitudeModifier());
						}
					}
				}
			}
		}
	}

//FfH: Added by Kael 02/23/2008
	if (kEvent.getGlobalCounter() != 0)
	{
        GC.getGameINLINE().changeGlobalCounter(kEvent.getGlobalCounter());
	}
//FfH: End Add

	if (!CvString(kEvent.getPythonCallback()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eEvent);
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pTriggeredData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kEvent.getPythonCallback(), argsList.makeFunctionArgs(), &lResult);
	}

	if (kEvent.getNumWorldNews() > 0)
	{
		int iText = GC.getGameINLINE().getSorenRandNum(kEvent.getNumWorldNews(), "Event World News choice");

		CvWString szGlobalText;

		TeamTypes eTheirWorstEnemy = NO_TEAM;
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			eTheirWorstEnemy = GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
		}

		szGlobalText = gDLL->getText(kEvent.getWorldNews(iText).GetCString(),
			getCivilizationAdjectiveKey(),
			NULL != pCity ? pCity->getNameKey() : L"",
			pTriggeredData->m_eOtherPlayer != NO_PLAYER ? GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			NO_RELIGION != pTriggeredData->m_eReligion ? GC.getReligionInfo(pTriggeredData->m_eReligion).getAdjectiveKey() : L"",
			NO_TEAM != eTheirWorstEnemy ? GET_TEAM(eTheirWorstEnemy).getName().GetCString() : L"",
			NO_CORPORATION != pTriggeredData->m_eCorporation ? GC.getCorporationInfo(pTriggeredData->m_eCorporation).getTextKeyWide() : L""
			);

		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

			if (kLoopPlayer.isAlive())
			{
				if (GET_TEAM(kLoopPlayer.getTeam()).isHasMet(getTeam()) && (NO_PLAYER == pTriggeredData->m_eOtherPlayer || GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).isHasMet(getTeam())))
				{
					bool bShowPlot = GC.getEventTriggerInfo(pTriggeredData->m_eTrigger).isShowPlot();

					if (bShowPlot)
					{
						if (kLoopPlayer.getTeam() != getTeam())
						{
							if (NULL == pPlot || !pPlot->isRevealed(kLoopPlayer.getTeam(), false))
							{
								bShowPlot = false;
							}
						}
					}

					if (bShowPlot)
					{
						gDLL->getInterfaceIFace()->addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY, true, true);
					}
					else
					{
						gDLL->getInterfaceIFace()->addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT);
					}
				}
			}
		}

/************************************************************************************************/
/* REVOLUTION_MOD                         02/01/08                                jdog5000      */
/*                                                                                              */
/* Silence replay messages for events ... too crowded by late game                              */
/************************************************************************************************/
/*
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szGlobalText, pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
*/
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	}

	if (!CvWString(kEvent.getLocalInfoTextKey()).empty())
	{
		CvWString szLocalText;

		TeamTypes eTheirWorstEnemy = NO_TEAM;
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			eTheirWorstEnemy = GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
		}

		szLocalText = gDLL->getText(kEvent.getLocalInfoTextKey(),
			getCivilizationAdjectiveKey(),
			NULL != pCity ? pCity->getNameKey() : L"",
			pTriggeredData->m_eOtherPlayer != NO_PLAYER ? GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			NO_RELIGION != pTriggeredData->m_eReligion ? GC.getReligionInfo(pTriggeredData->m_eReligion).getAdjectiveKey() : L"",
			NO_TEAM != eTheirWorstEnemy ? GET_TEAM(eTheirWorstEnemy).getName().GetCString() : L"",
			NO_CORPORATION != pTriggeredData->m_eCorporation ? GC.getCorporationInfo(pTriggeredData->m_eCorporation).getTextKeyWide() : L""
			);

			if (GC.getEventTriggerInfo(pTriggeredData->m_eTrigger).isShowPlot())
			{
				gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szLocalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY, true, true);
			}
			else
			{
				gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szLocalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"));
			}

	}

	if (!CvWString(kEvent.getOtherPlayerPopup()).empty())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			CvWString szText = gDLL->getText(kEvent.getOtherPlayerPopup(),
				getCivilizationAdjectiveKey(),
				NULL != pCity ? pCity->getNameKey() : L"",
				pTriggeredData->m_eOtherPlayer != NO_PLAYER ? GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationAdjectiveKey() : L"",
				NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
				NO_RELIGION != pTriggeredData->m_eReligion ? GC.getReligionInfo(pTriggeredData->m_eReligion).getAdjectiveKey() : L"",
				NO_CORPORATION != pTriggeredData->m_eCorporation ? GC.getCorporationInfo(pTriggeredData->m_eCorporation).getTextKeyWide() : L""
				);

			CvPopupInfo* pInfo = new CvPopupInfo();

			if (NULL != pInfo)
			{
				pInfo->setText(szText);

				GET_PLAYER(pTriggeredData->m_eOtherPlayer).addPopup(pInfo);
			}
		}
	}

	bool bDeleteTrigger = bUpdateTrigger;

	for (int iEvent = 0; iEvent < GC.getNumEventInfos(); ++iEvent)
	{
		if (0 == kEvent.getAdditionalEventTime(iEvent))
		{
			if (kEvent.getAdditionalEventChance(iEvent) > 0)
			{
				if (canDoEvent((EventTypes)iEvent, *pTriggeredData))
				{
					if (GC.getGameINLINE().getSorenRandNum(100, "Additional Event") < kEvent.getAdditionalEventChance(iEvent))
					{
						applyEvent((EventTypes)iEvent, iEventTriggeredId, false);
					}
				}
			}
		}
		else
		{
			bool bSetTimer = true;
			if (kEvent.getAdditionalEventChance(iEvent) > 0)
			{
				if (GC.getGameINLINE().getSorenRandNum(100, "Additional Event 2") >= kEvent.getAdditionalEventChance(iEvent))
				{
					bSetTimer = false;
				}
			}

			if (bSetTimer)
			{
				EventTriggeredData kTriggered = *pTriggeredData;
				kTriggered.m_iTurn = (GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent() * kEvent.getAdditionalEventTime((EventTypes)iEvent)) / 100 + GC.getGameINLINE().getGameTurn();

				const EventTriggeredData* pExistingTriggered = getEventCountdown((EventTypes)iEvent);

				if (NULL != pExistingTriggered)
				{
					kTriggered.m_iTurn = std::min(kTriggered.m_iTurn, pExistingTriggered->m_iTurn);
				}

				setEventCountdown((EventTypes)iEvent, kTriggered);
				bDeleteTrigger = false;
			}
		}
	}

	if (bDeleteTrigger)
	{
		deleteEventTriggered(iEventTriggeredId);
	}
}

bool CvPlayer::isValidEventTech(TechTypes eTech, EventTypes eEvent, PlayerTypes eOtherPlayer) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (0 == kEvent.getTechPercent() && 0 == kEvent.getTechCostPercent())
	{
		return false;
	}

	if (kEvent.getTechPercent() < 0 && GET_TEAM(getTeam()).getResearchProgress(eTech) <= 0)
	{
		return false;
	}

	if (!canResearch(eTech))
	{
		return false;
	}

	if (getResearchTurnsLeft(eTech, true) < kEvent.getTechMinTurnsLeft())
	{
		return false;
	}

	if (NO_PLAYER != eOtherPlayer && !GET_TEAM(GET_PLAYER(eOtherPlayer).getTeam()).isHasTech(eTech))
	{
		return false;
	}

	return true;
}


TechTypes CvPlayer::getBestEventTech(EventTypes eEvent, PlayerTypes eOtherPlayer) const
{
	TechTypes eBestTech = NO_TECH;
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (0 == kEvent.getTechPercent() && 0 == kEvent.getTechCostPercent())
	{
		return NO_TECH;
	}

	if (NO_TECH != kEvent.getTech())
	{
		eBestTech = (TechTypes)kEvent.getTech();
	}
	else
	{
		bool bFoundFlavor = false;
		for (int i = 0; i < GC.getNumFlavorTypes(); ++i)
		{
			if (0 != kEvent.getTechFlavorValue(i))
			{
				bFoundFlavor = true;
				break;
			}
		}

		if (!bFoundFlavor)
		{
			eBestTech = getCurrentResearch();
		}
	}

	if (NO_TECH != eBestTech)
	{
		if (!isValidEventTech(eBestTech, eEvent, eOtherPlayer))
		{
			eBestTech = NO_TECH;
		}
	}
	else
	{
		int iBestValue = 0;
		for (int iTech = 0; iTech < GC.getNumTechInfos(); ++iTech)
		{
			if (isValidEventTech((TechTypes)iTech, eEvent, eOtherPlayer))
			{
				int iValue = 0;
				for (int i = 0; i < GC.getNumFlavorTypes(); ++i)
				{
					iValue += kEvent.getTechFlavorValue(i) * GC.getTechInfo((TechTypes)iTech).getFlavorValue(i);
				}

				if (iValue > iBestValue)
				{
					eBestTech = (TechTypes)iTech;
					iBestValue = iValue;
				}
			}
		}
	}

	return eBestTech;
}

int CvPlayer::getEventCost(EventTypes eEvent, PlayerTypes eOtherPlayer, bool bRandom) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	int iGold = kEvent.getGold();
	if (bRandom)
	{
		iGold += kEvent.getRandomGold();
	}

	iGold *= std::max(0, calculateInflationRate() + 100);
	iGold /= 100;

	TechTypes eBestTech = getBestEventTech(eEvent, eOtherPlayer);

	if (NO_TECH != eBestTech)
	{
		iGold -= (kEvent.getTechCostPercent() * GET_TEAM(getTeam()).getResearchCost(eBestTech)) / 100;
	}

	return iGold;
}


void CvPlayer::doEvents()
{
	// lfgr EVENT_DEBUG
	logBBAI( "EVENT_DEBUG - doEvents on player #%d", getID() );
	// lfgr end

	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_EVENTS))
	{
		return;
	}

/************************************************************************************************/
/* REVOLUTION_MOD                         03/02/08                                jdog5000      */
/*                                                                                              */
/* For minor civs                                                                               */
/************************************************************************************************/
/* original code
	if (isBarbarian() || isMinorCiv())
*/
	// Allow events for minor civs
	if (isBarbarian())
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/
	{
		return;
	}

	// Expire old events (not triggers!) and their triggerdata
	CvEventMap::iterator it = m_mapEventsOccured.begin();
	while (it != m_mapEventsOccured.end())
	{
		if (checkExpireEvent(it->first, it->second))
		{
			expireEvent(it->first, it->second, true);
			it = m_mapEventsOccured.erase(it);
		}
		else
		{
			++it;
		}
	}

	// lfgr cmt: check whether any event can trigger (weight==-1 triggers anyway)

	bool bNewEventEligible = true;
	if (GC.getGameINLINE().getElapsedGameTurns() < GC.getDefineINT("FIRST_EVENT_DELAY_TURNS"))
	{
		bNewEventEligible = false;
	}

	if (bNewEventEligible)
	{

//FfH: Modifed by Kael 09/26/2007
//		if (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("EVENT_PROBABILITY_ROLL_SIDES"), "Global event check") >= GC.getEraInfo(getCurrentEra()).getEventChancePerTurn())
        int iChance = GC.getEraInfo(getCurrentRealEra()).getEventChancePerTurn();
        if (GC.getGameINLINE().isOption(GAMEOPTION_DOUBLE_EVENTS))
        {
            iChance *= 2;
        }
		if (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("EVENT_PROBABILITY_ROLL_SIDES"), "Global event check") >= iChance)
//FfH: End Modify

		{
			bNewEventEligible = false;
		}
	}

	// lfgr cmt: get all event weights, trigger all with weight == -1, create triggeredData for all weight > 0
	//  (the latter only if global event check succeeds.

	std::vector< std::pair<EventTriggeredData*, int> > aePossibleEventTriggerWeights;
	int iTotalWeight = 0;
	for (int i = 0; i < GC.getNumEventTriggerInfos(); ++i)
	{
		int iWeight = getEventTriggerWeight((EventTriggerTypes)i);
		if (iWeight == -1)
		{
/************************************************************************************************/
/* EVENT_NEW_TAGS                           12/2015                                 lfgr        */
/************************************************************************************************/
/* old
			trigger((EventTriggerTypes)i);
*/
			int iDelay = GC.getEventTriggerInfo( (EventTriggerTypes) i ).getDelay();
			if( iDelay <= m_paiEventTriggerDelayCounters[i] ) // always if iDelay == 0
				trigger( (EventTriggerTypes) i );
			else
				m_paiEventTriggerDelayCounters[i]++;
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/
		}
		else if (iWeight > 0 && bNewEventEligible)
		{
			EventTriggeredData* pTriggerData = initTriggeredData((EventTriggerTypes)i);
			if (NULL != pTriggerData)
			{
				logBBAI( "EVENT_DEBUG - Assigning a total weight of %i to EventTrigger \"%s\" in the list of possible EventTriggers", iTotalWeight, GC.getEventTriggerInfo( pTriggerData->m_eTrigger ).getType() );
				iTotalWeight += iWeight;
				aePossibleEventTriggerWeights.push_back(std::make_pair(pTriggerData, iTotalWeight));
			}
		}
	}

	// lfgr cmt: fire one semi-random event, clean up the others

	if (iTotalWeight > 0)
	{
		bool bFired = false;
		int iValue = GC.getGameINLINE().getSorenRandNum(iTotalWeight, "Event trigger");
		logBBAI( "EVENT_DEBUG - Chosen random value: %i (total: %i)", iValue, iTotalWeight );
		for (std::vector< std::pair<EventTriggeredData*, int> >::iterator it = aePossibleEventTriggerWeights.begin(); it != aePossibleEventTriggerWeights.end(); ++it)
		{
			EventTriggeredData* pTriggerData = (*it).first;
			if (NULL != pTriggerData)
			{
				logBBAI( "EVENT_DEBUG - Checking EventTrigger \"%s\"", GC.getEventTriggerInfo( pTriggerData->m_eTrigger ).getType() );
				if (iValue < (*it).second && !bFired)
				{
					trigger(*pTriggerData);
					bFired = true;
				}
				else
				{
					logBBAI( "EVENT_DEBUG - EventTrigger \"%s\" not triggered", GC.getEventTriggerInfo( pTriggerData->m_eTrigger ).getType() );
					deleteEventTriggered(pTriggerData->getID());
				}
			}
		}
	}

	// lfgr cmt: apply countdown events and clean them up

	std::vector<int> aCleanup;
	for (int i = 0; i < GC.getNumEventInfos(); ++i)
	{
		const EventTriggeredData* pTriggeredData = getEventCountdown((EventTypes)i);
		if (NULL != pTriggeredData)
		{
			if (GC.getGameINLINE().getGameTurn() >= pTriggeredData->m_iTurn)
			{
				applyEvent((EventTypes)i, pTriggeredData->m_iId);
				resetEventCountdown((EventTypes)i);
				aCleanup.push_back(pTriggeredData->m_iId);
			}
		}
	}

	for (std::vector<int>::iterator it = aCleanup.begin(); it != aCleanup.end(); ++it)
	{
		bool bDelete = true;

		for (int i = 0; i < GC.getNumEventInfos(); ++i)
		{
			const EventTriggeredData* pTriggeredData = getEventCountdown((EventTypes)i);
			if (NULL != pTriggeredData)
			{
				if (pTriggeredData->m_iId == *it)
				{
					bDelete = false;
					break;
				}
			}
		}

		if (bDelete)
		{
			deleteEventTriggered(*it);
		}
	}
}


void CvPlayer::expireEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData, bool bFail)
{
	FAssert(getEventOccured(eEvent) == &kTriggeredData);
	FAssert(GC.getEventInfo(eEvent).isQuest() || GC.getGameINLINE().getGameTurn() - kTriggeredData.m_iTurn <= 4);

	if (GC.getEventInfo(eEvent).isQuest())
	{
		CvMessageQueue::iterator it;
		for (it = m_listGameMessages.begin(); it != m_listGameMessages.end(); ++it)
		{
			CvTalkingHeadMessage& message = *it;

			// the trigger ID is stored in the otherwise unused length field
			if (message.getLength() == kTriggeredData.getID())
			{
				m_listGameMessages.erase(it);
				gDLL->getInterfaceIFace()->dirtyTurnLog(getID());
				break;
			}
		}

		if (bFail)
		{
			gDLL->getInterfaceIFace()->addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText(GC.getEventInfo(eEvent).getQuestFailTextKey()), "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_RED"));
		}
	}
}

bool CvPlayer::checkExpireEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (!CvString(kEvent.getPythonExpireCheck()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eEvent);
		argsList.add(gDLL->getPythonIFace()->makePythonObject(&kTriggeredData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kEvent.getPythonExpireCheck(), argsList.makeFunctionArgs(), &lResult);

		if (0 != lResult)
		{
			return true;
		}
	}

	if (!kEvent.isQuest())
	{
/************************************************************************************************/
/* EVENT_NEW_TAGS                           12/2015                                 lfgr        */
/* Non-quest events with bNoExpire = 1 no longer expire automatically after 2 turns             */
/************************************************************************************************/
/* old
		if (GC.getGameINLINE().getGameTurn() - kTriggeredData.m_iTurn > 2)
*/
		if( !kEvent.isNoExpire() && GC.getGameINLINE().getGameTurn() - kTriggeredData.m_iTurn > 2 )
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/
		{
			return true;
		}

		return false;
	}

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(kTriggeredData.m_eTrigger);

	FAssert(kTriggeredData.m_ePlayer != NO_PLAYER);

	CvPlayer& kPlayer = GET_PLAYER(kTriggeredData.m_ePlayer);

	if (kTrigger.isStateReligion() & kTrigger.isPickReligion())
	{
		if (kPlayer.getStateReligion() != kTriggeredData.m_eReligion)
		{
			return true;
		}
	}

	if (NO_CIVIC != kTrigger.getCivic())
	{
		if (!kPlayer.isCivic((CivicTypes)kTrigger.getCivic()))
		{
			return true;
		}
	}

	if (kTriggeredData.m_iCityId != -1)
	{
		if (NULL == kPlayer.getCity(kTriggeredData.m_iCityId))
		{
			return true;
		}
	}

	if (kTriggeredData.m_iUnitId != -1)
	{
		if (NULL == kPlayer.getUnit(kTriggeredData.m_iUnitId))
		{
			return true;
		}
	}

	if (NO_PLAYER != kTriggeredData.m_eOtherPlayer)
	{
		if (!GET_PLAYER(kTriggeredData.m_eOtherPlayer).isAlive())
		{
			return true;
		}

		if (kTriggeredData.m_iOtherPlayerCityId != -1)
		{
			if (NULL == GET_PLAYER(kTriggeredData.m_eOtherPlayer).getCity(kTriggeredData.m_iOtherPlayerCityId))
			{
				return true;
			}
		}
	}

	if (kTrigger.getNumObsoleteTechs() > 0)
	{
		for (int iI = 0; iI < kTrigger.getNumObsoleteTechs(); iI++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getObsoleteTech(iI))))
			{
				return true;
			}
		}
	}

	return false;
}


void CvPlayer::trigger(EventTriggerTypes eTrigger)
{
	initTriggeredData(eTrigger, true);
}

void CvPlayer::trigger(const EventTriggeredData& kData)
{
	// lfgr EVENT_DEBUG
	logBBAI( "EVENT_DEBUG - Triggered EventTrigger \"%s\" for Player #%d, \"%S\"",
			GC.getEventTriggerInfo( kData.m_eTrigger ).getType(), getID(), getName() );
	// lfgr end

	if (isHuman())
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_EVENT, kData.getID());
		addPopup(pInfo);
	}
	else
	{
		EventTypes eEvent = AI_chooseEvent(kData.getID());
		if (NO_EVENT != eEvent)
		{
			applyEvent(eEvent, kData.getID());
		}
	}
}

// lfgr cmt: this is the OTHER player
bool CvPlayer::canTrigger(EventTriggerTypes eTrigger, PlayerTypes ePlayer, ReligionTypes eReligion) const
{
	if (!isAlive())
	{
		return false;
	}

	if (getID() == ePlayer)
	{
		return false;
	}

	CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);

	if (getTeam() == kPlayer.getTeam())
	{
		return false;
	}

	if (!kTrigger.isPickPlayer())
	{
		return false;
	}

	if (!GET_TEAM(getTeam()).isHasMet(kPlayer.getTeam()))
	{
		return false;
	}

	if (isHuman() && kTrigger.isOtherPlayerAI())
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isAtWar(kPlayer.getTeam()) != kTrigger.isOtherPlayerWar())
	{
		return false;
	}

	if (NO_TECH != kTrigger.getOtherPlayerHasTech())
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)kTrigger.getOtherPlayerHasTech()))
		{
			return false;
		}
	}

	if (kTrigger.getOtherPlayerShareBorders() > 0)
	{
		int iCount = 0;

		for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); ++iI)
		{
			CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

			if (!pLoopPlot->isWater())
			{
				if ((pLoopPlot->getOwnerINLINE() == getID()) && pLoopPlot->isAdjacentPlayer(ePlayer, true))
				{
					++iCount;
				}
			}
		}

		if (iCount < kTrigger.getOtherPlayerShareBorders())
		{
			return false;
		}
	}

	if (NO_RELIGION != eReligion)
	{
		bool bHasReligion = kTrigger.isStateReligion() ? (getStateReligion() == eReligion) : (getHasReligionCount(eReligion) > 0);

		if (kTrigger.isOtherPlayerHasReligion())
		{
			if (!bHasReligion)
			{
				return false;
			}
		}

		if (kTrigger.isOtherPlayerHasOtherReligion())
		{
			if (bHasReligion)
			{
				return false;
			}

			if (kTrigger.isStateReligion() && getStateReligion() == NO_RELIGION)
			{
				return false;
			}

		}
	}
	
/************************************************************************************************/
/* EVENT_NEW_TAGS                           08/21/13                                lfgr        */
/************************************************************************************************/
	if ( kTrigger.getPrereqCivilizationPleased() != NO_CIVILIZATION )
		if( getCivilizationType() != kTrigger.getPrereqCivilizationPleased() )
			return false;
/************************************************************************************************/
/* EVENT_NEW_TAGS                          END                                                  */
/************************************************************************************************/

	return true;
}

CvCity* CvPlayer::pickTriggerCity(EventTriggerTypes eTrigger) const
{
	CvCity* pCity = NULL;
	std::vector<CvCity*> apCities;
	int iLoop;
	int iBestValue = MIN_INT;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		int iValue = pLoopCity->getTriggerValue(eTrigger);

		if (iValue >= iBestValue && iValue != MIN_INT)
		{
			if (iValue > iBestValue)
			{
				apCities.clear();
				iBestValue = iValue;
			}
			apCities.push_back(pLoopCity);
		}
	}

	if (apCities.size() > 0)
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apCities.size(), "Event pick city");
		pCity = apCities[iChosen];
	}

	return pCity;
}

CvUnit* CvPlayer::pickTriggerUnit(EventTriggerTypes eTrigger, CvPlot* pPlot, bool bPickPlot) const
{
	CvUnit* pUnit = NULL;
	std::vector<CvUnit*> apUnits;
	int iLoop;
	int iBestValue = MIN_INT;
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		int iValue = pLoopUnit->getTriggerValue(eTrigger, pPlot, bPickPlot);

		if (iValue >= iBestValue && iValue != MIN_INT)
		{
			if (iValue > iBestValue)
			{
				apUnits.clear();
				iBestValue = iValue;
			}
			apUnits.push_back(pLoopUnit);
		}
	}

	if (apUnits.size() > 0)
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apUnits.size(), "Event pick unit");
		pUnit = apUnits[iChosen];
	}

	return pUnit;
}

// lfgr cmt: Most important function for event triggering. 0 means don't trigger, -1 means always trigger
int CvPlayer::getEventTriggerWeight(EventTriggerTypes eTrigger) const
{
	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);
//	logBBAI( "EVENT_DEBUG - Getting EventTrigger weight \"%s\"", kTrigger.getType() );
	// lfgr cmt: check simple requirements

	if (NO_HANDICAP != kTrigger.getMinDifficulty())
	{
		if (GC.getGameINLINE().getHandicapType() < kTrigger.getMinDifficulty())
		{
			return 0;
		}
	}

	if (kTrigger.isSinglePlayer() && GC.getGameINLINE().isGameMultiPlayer())
	{
		return 0;
	}

	if (!GC.getGameINLINE().isEventActive(eTrigger))
	{
		return 0;
	}

	if (kTrigger.getNumObsoleteTechs() > 0)
	{
		for (int iI = 0; iI < kTrigger.getNumObsoleteTechs(); iI++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getObsoleteTech(iI))))
			{
				return 0;
			}
		}
	}

	if (!kTrigger.isRecurring())
	{
		if (isTriggerFired(eTrigger))
		{
			return 0;
		}

//FfH: Added by Kael 09/19/2008
        if (kTrigger.isGlobal())
        {
            if (GC.getGameINLINE().isEventTriggered(eTrigger))
            {
                return 0;
            }
        }
//FfH: End Add

	}

	if (kTrigger.getNumPrereqOrTechs() > 0)
	{
		bool bFoundValid = false;

		for (int iI = 0; iI < kTrigger.getNumPrereqOrTechs(); iI++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getPrereqOrTechs(iI))))
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}


	if (kTrigger.getNumPrereqAndTechs() > 0)
	{
		bool bFoundValid = true;

		for (int iI = 0; iI < kTrigger.getNumPrereqAndTechs(); iI++)
		{
			if (!GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getPrereqAndTechs(iI))))
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}

	if (kTrigger.getNumPrereqEvents() > 0)
	{
		bool bFoundValid = true;
		for (int iI = 0; iI < kTrigger.getNumPrereqEvents(); iI++)
		{
			if (NULL == getEventOccured((EventTypes)kTrigger.getPrereqEvent(iI)))
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}

	if (NO_CIVIC != kTrigger.getCivic())
	{
		bool bFoundValid = false;

		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); ++iI)
		{
			if (getCivics((CivicOptionTypes)iI) == kTrigger.getCivic())
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}

//FfH Events: Added by Kael 08/08/2007
	if (kTrigger.getPrereqGlobalCounter() != 0)
	{
	    if (GC.getGameINLINE().getGlobalCounter() < kTrigger.getPrereqGlobalCounter())
	    {
	        return 0;
	    }
	}
	if (kTrigger.getPrereqAlignment() != NO_ALIGNMENT)
	{
	    if (getAlignment() != kTrigger.getPrereqAlignment())
	    {
	        return 0;
	    }
	}
	if (kTrigger.getPrereqTrait() != NO_TRAIT)
	{
	    if (!hasTrait((TraitTypes)kTrigger.getPrereqTrait()))
	    {
	        return 0;
	    }
	}
	if (kTrigger.getPrereqCivilizationPleased() != NO_CIVILIZATION)
	{
	    if (kTrigger.getPrereqCivilizationPleased() == getCivilizationType())
	    {
	        return 0;
	    }
	    bool bValid = false;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
        {
            if (GET_PLAYER((PlayerTypes)iI).isAlive())
            {
                if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == kTrigger.getPrereqCivilizationPleased())
                {
                    if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()))
                    {
                        if (GET_PLAYER((PlayerTypes)iI).AI_getAttitude(getID()) >= ATTITUDE_PLEASED)
                        {
                            bValid = true;
                        }
                    }
                }
            }
        }
        if (bValid == false)
        {
            return 0;
        }
	}
	if (kTrigger.getPrereqLeader() != NO_LEADER)
	{
	    if (getLeaderType() != kTrigger.getPrereqLeader())
	    {
	        return 0;
	    }
	}
//FfH: End Add

	if (kTrigger.getMinTreasury() > 0)
	{
		if (getGold() < kTrigger.getMinTreasury())
		{
			return 0;
		}
	}

	if (GC.getMapINLINE().getNumLandAreas() < kTrigger.getMinMapLandmass())
	{
		return 0;
	}

	if (kTrigger.getMinOurLandmass() > 0 || kTrigger.getMaxOurLandmass() != -1)
	{
		int iNumLandmass = 0;

		int iLoop;
		for (CvArea* pArea = GC.getMapINLINE().firstArea(&iLoop); NULL != pArea; pArea = GC.getMapINLINE().nextArea(&iLoop))
		{
			if (!pArea->isWater())
			{
				if (pArea->getCitiesPerPlayer(getID()) > 0)
				{
					++iNumLandmass;
				}
			}
		}

		if (iNumLandmass < kTrigger.getMinOurLandmass())
		{
			return 0;
		}

		if (kTrigger.getMaxOurLandmass() != -1 && iNumLandmass > kTrigger.getMaxOurLandmass())
		{
			return 0;
		}
	}

// UNIVERSAL_PREREQS 09/2017 lfgr
	if( kTrigger.getGamePrereq() != NULL 
			&& ! kTrigger.getGamePrereq()->isValid( &( GC.getGameINLINE() ) ) )
		return 0;
	if( kTrigger.getPlayerPrereq() != NULL 
			&& ! kTrigger.getPlayerPrereq()->isValid( this ) )
		return 0;
// UNIVERSAL_PREREQS end

	// lfgr cmt: calc weight (probability)

	// lfgr cmt: calc weight (probability)

	if (kTrigger.getProbability() < 0)
	{
		return kTrigger.getProbability();
	}

	int iProbability = kTrigger.getProbability();

	if (kTrigger.isProbabilityUnitMultiply() && kTrigger.getNumUnits() > 0)
	{
		int iNumUnits = 0;
		int iLoop;
		for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (MIN_INT != pLoopUnit->getTriggerValue(eTrigger, NULL, true))
			{
				++iNumUnits;
			}
		}

		iProbability *= iNumUnits;
	}

	if (kTrigger.isProbabilityBuildingMultiply() && kTrigger.getNumBuildings() > 0)
	{
		int iNumBuildings = 0;
		for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
		{
			if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
			{
				iNumBuildings += getBuildingClassCount((BuildingClassTypes)kTrigger.getBuildingRequired(i));
			}
		}

		iProbability *= iNumBuildings;
	}

	return iProbability;
}


PlayerTypes CvPlayer::getSplitEmpirePlayer(int iAreaId) const
{
	// can't create different derivative civs on the same continent
	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.isAlive() && kLoopPlayer.getParent() == getID())
		{
			CvCity* pLoopCapital = kLoopPlayer.getCapitalCity();
			if (NULL != pLoopCapital)
			{
				if (pLoopCapital->area()->getID() == iAreaId)
				{
					return NO_PLAYER;
				}
			}
		}
	}
//>>>>Unofficial Bug Fix: Added by Denev 2010/02/20
//*** Separate function of opening new player from ::getSplitEmpirePlayer().
	return getOpenPlayer();
}

PlayerTypes CvPlayer::getOpenPlayer() const
{
//<<<<Unofficial Bug Fix: End Add
	PlayerTypes eNewPlayer = NO_PLAYER;

	// Try to find a player who's never been in the game before
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		if (!GET_PLAYER((PlayerTypes)i).isEverAlive())
		{
			eNewPlayer = (PlayerTypes)i;
			break;
		}
	}

	if (eNewPlayer == NO_PLAYER)
	{
		// Try to recycle a dead player
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			if (!GET_PLAYER((PlayerTypes)i).isAlive())
			{
				eNewPlayer = (PlayerTypes)i;
				break;
			}
		}
	}

	return eNewPlayer;
}

bool CvPlayer::canSplitEmpire() const
{
	int iLoopArea;

	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_VASSAL_STATES))
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isAVassal())
	{
		return false;
	}

	CivLeaderArray aLeaders;
	if (!getSplitEmpireLeaders(aLeaders))
	{
		return false;
	}

	bool bFoundArea = false;

	for (CvArea* pLoopArea = GC.getMapINLINE().firstArea(&iLoopArea); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoopArea))
	{
		if (canSplitArea(pLoopArea->getID()))
		{
			bFoundArea = true;
			break;
		}
	}

	if (!bFoundArea)
	{
		return false;
	}

	return true;
}

bool CvPlayer::canSplitArea(int iAreaId) const
{
	CvArea* pArea = GC.getMapINLINE().getArea(iAreaId);
	CvCity* pCapital = getCapitalCity();

	if (NULL == pCapital)
	{
		return false;
	}

	if (NULL == pArea || pArea == pCapital->area())
	{
		return false;
	}

	if (0 == pArea->getCitiesPerPlayer(getID()))
	{
		return false;
	}

	PlayerTypes ePlayer = getSplitEmpirePlayer(pArea->getID());
	if (NO_PLAYER == ePlayer)
	{
		return false;
	}

	if (!GET_PLAYER(ePlayer).isAlive())
	{
		if (pArea->getCitiesPerPlayer(getID()) <= 1)
		{
			return false;
		}
	}

	return true;
}

bool CvPlayer::getSplitEmpireLeaders(CivLeaderArray& aLeaders) const
{
	aLeaders.clear();

	for (int i = 0; i < GC.getNumCivilizationInfos(); ++i)
	{
		bool bValid = true;

//FfH: Modified by Kael 01/16/2009
//		if (getCivilizationType() == i)
//		{
//			bValid = false;
//		}
//FfH: End Modify

		if (bValid)
		{
			if (!GC.getCivilizationInfo((CivilizationTypes)i).isPlayable() || !GC.getCivilizationInfo((CivilizationTypes)i).isAIPlayable())
			{
				bValid = false;
			}
		}

		if (bValid)
		{
			for (int j = 0; j < MAX_CIV_PLAYERS; ++j)
			{
				if (getID() != j && GET_PLAYER((PlayerTypes)j).isEverAlive() && GET_PLAYER((PlayerTypes)j).getCivilizationType() == i)
				{
					bValid = false;
					break;
				}
			}
		}

		if (bValid)
		{
			for (int j = 0; j < GC.getNumLeaderHeadInfos(); ++j)
			{
				bool bLeaderValid = true;
				if (!GC.getCivilizationInfo((CivilizationTypes)i).isLeaders(j) && !GC.getGameINLINE().isOption(GAMEOPTION_LEAD_ANY_CIV))
				{
					bLeaderValid = false;
				}

//FfH: Added by Kael 01/16/2008
                if (getCivilizationType() == i)
                {
                    if (GC.getLeaderHeadInfo((LeaderHeadTypes)j).isGraphicalOnly())
                    {
                        if (GC.getLeaderHeadInfo((LeaderHeadTypes)j).getAlignment() == getAlignment())
                        {
                            bLeaderValid = true;
                        }
                    }
                }
                if (GC.getLeaderHeadInfo((LeaderHeadTypes)j).getFavoriteWonder() == NO_BUILDING)
                {
                    bLeaderValid = false;
                }
//FfH: End Add

// Leader categories START
				CvLeaderHeadInfo& currentLeader = GC.getLeaderHeadInfo((LeaderHeadTypes)j);

				if (currentLeader.getLeaderCategory() == LEADERCATEGORY_SCENEXTRA && !GC.getGameINLINE().isOption(GAMEOPTION_LEADER_SCENEXTRA)) {
					// If extra scenario leaders have not been selected, avoid using them.
					bLeaderValid = false;
					continue;
				}

				if (currentLeader.getLeaderCategory() == LEADERCATEGORY_EXTRA && !GC.getGameINLINE().isOption(GAMEOPTION_LEADER_EXTRA)) {
					// If extra leaders have not been selected, avoid using them.
					bLeaderValid = false;
					continue;
				}
// Leader categories END

				if (bLeaderValid)
				{
					for (int k = 0; k < MAX_CIV_PLAYERS; ++k)
					{
						if (GET_PLAYER((PlayerTypes)k).isEverAlive() && GET_PLAYER((PlayerTypes)k).getPersonalityType() == j)
						{
							bLeaderValid = false;
						}
					}
				}

				if (bLeaderValid)
				{
					aLeaders.push_back(std::make_pair((CivilizationTypes)i, (LeaderHeadTypes)j));
				}
			}
		}
	}

	return (aLeaders.size() > 0);
}

bool CvPlayer::splitEmpire(int iAreaId)
{
	PROFILE_FUNC();

	if (!canSplitEmpire())
	{
		return false;
	}

	if (!canSplitArea(iAreaId))
	{
		return false;
	}

	CvArea* pArea = GC.getMapINLINE().getArea(iAreaId);
	if (NULL == pArea)
	{
		return false;
	}

//>>>>Unofficial Bug Fix: Deleted by Denev 2010/03/18
/*
	PlayerTypes eNewPlayer = getSplitEmpirePlayer(iAreaId);
	if (eNewPlayer == NO_PLAYER)
	{
		return false;
	}

	bool bPlayerExists = GET_TEAM(GET_PLAYER(eNewPlayer).getTeam()).isAlive();
	FAssert(!bPlayerExists);
	if (!bPlayerExists)
	{
*/
//<<<<Unofficial Bug Fix: End Delete
		int iBestValue = -1;
		LeaderHeadTypes eBestLeader = NO_LEADER;
		CivilizationTypes eBestCiv = NO_CIVILIZATION;

		CivLeaderArray aLeaders;
		if (getSplitEmpireLeaders(aLeaders))
		{
			CivLeaderArray::iterator it;
			for (it = aLeaders.begin(); it != aLeaders.end(); ++it)
			{
				int iValue = (1 + GC.getGameINLINE().getSorenRandNum(100, "Choosing Split Personality"));

//FfH: Added by Kael 01/16/2008
				if (getCivilizationType() == it->first)
				{
                    iValue += 1000;
                }
                if (GC.getLeaderHeadInfo(it->second).isGraphicalOnly())
                {
                    iValue += 1000;
                }
//FfH: End Add

				if (GC.getCivilizationInfo(getCivilizationType()).getDerivativeCiv() == it->first)
				{
					iValue += 1000;
				}

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestLeader = it->second;
					eBestCiv = it->first;
				}
			}
		}

		if (eBestLeader == NO_LEADER || eBestCiv == NO_CIVILIZATION)
		{
			return false;
		}

//>>>>Unofficial Bug Fix: Added by Denev 2010/03/18
		PlayerTypes eNewPlayer = initNewEmpire(eBestLeader, eBestCiv);
//<<<<Unofficial Bug Fix: End Add

		CvWString szMessage = gDLL->getText("TXT_KEY_MISC_EMPIRE_SPLIT", getNameKey(), GC.getCivilizationInfo(eBestCiv).getShortDescriptionKey(), GC.getLeaderHeadInfo(eBestLeader).getTextKeyWide());
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			if (GET_PLAYER((PlayerTypes)i).isAlive())
			{
				if (i == getID() || i == eNewPlayer || GET_TEAM(GET_PLAYER((PlayerTypes)i).getTeam()).isHasMet(getTeam()))
				{
					gDLL->getInterfaceIFace()->addMessage((PlayerTypes)i, false, GC.getEVENT_MESSAGE_TIME(), szMessage, "AS2D_REVOLTEND", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_CITY_BAR_CAPITAL_TEXTURE")->getPath());
				}
			}
		}
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szMessage, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      12/30/08                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/*
		// remove leftover culture from old recycled player
		for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
		{
			CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

			pLoopPlot->setCulture(eNewPlayer, 0, false, false);
		}
*/
		// Clearing plot culture along with many other bits of data now handled by CvGame::addPlayer
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

//>>>>Unofficial Bug Fix: Modified by Denev 2010/02/20
/*
		GC.getGameINLINE().addPlayer(eNewPlayer, eBestLeader, eBestCiv);
		GET_PLAYER(eNewPlayer).setParent(getID());
		GC.getInitCore().setLeaderName(eNewPlayer, GC.getLeaderHeadInfo(eBestLeader).getTextKeyWide());

		CvTeam& kNewTeam = GET_TEAM(GET_PLAYER(eNewPlayer).getTeam());
		for (int i = 0; i < GC.getNumTechInfos(); ++i)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)i))
			{
				kNewTeam.setHasTech((TechTypes)i, true, eNewPlayer, false, false);
				if (GET_TEAM(getTeam()).isNoTradeTech((TechTypes)i) || GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING))
				{
					kNewTeam.setNoTradeTech((TechTypes)i, true);
				}
			}
		}

		for (int iTeam = 0; iTeam < MAX_TEAMS; ++iTeam)
		{
			CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iTeam);

			if (kLoopTeam.isAlive())
			{
				kNewTeam.setEspionagePointsAgainstTeam((TeamTypes)iTeam, GET_TEAM(getTeam()).getEspionagePointsAgainstTeam((TeamTypes)iTeam));
				kLoopTeam.setEspionagePointsAgainstTeam(GET_PLAYER(eNewPlayer).getTeam(), kLoopTeam.getEspionagePointsAgainstTeam(getTeam()));
			}
		}
		kNewTeam.setEspionagePointsEver(GET_TEAM(getTeam()).getEspionagePointsEver());

		GET_TEAM(getTeam()).assignVassal(GET_PLAYER(eNewPlayer).getTeam(), false);

		AI_updateBonusValue();
	}
*/
	GET_PLAYER(eNewPlayer).setParent(getID());
	GET_TEAM(getTeam()).assignVassal(GET_PLAYER(eNewPlayer).getTeam(), false);
//<<<<Unofficial Bug Fix: End Modify

	std::vector< std::pair<int, int> > aCultures;
	for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

		bool bTranferPlot = false;

		if (!bTranferPlot && pLoopPlot->area() == pArea)
		{
			bTranferPlot = true;
		}

		if (!bTranferPlot)
		{
			CvCity* pWorkingCity = pLoopPlot->getWorkingCity();
			if (NULL != pWorkingCity && pWorkingCity->getOwnerINLINE() == getID() && pWorkingCity->area() == pArea)
			{
				bTranferPlot = true;
			}
		}

		if (!bTranferPlot && pLoopPlot->isWater() && pLoopPlot->isAdjacentToArea(pArea))
		{
			bTranferPlot = true;
		}

		if (bTranferPlot)
		{
			int iCulture = pLoopPlot->getCulture(getID());

//>>>>Unofficial Bug Fix: Deleted by Denev 2010/03/18
//			if (bPlayerExists)
//<<<<Unofficial Bug Fix: End Modify
			{
				iCulture = std::max(iCulture, pLoopPlot->getCulture(eNewPlayer));
			}

			aCultures.push_back(std::make_pair(iPlot, iCulture));
		}

		if (pLoopPlot->isRevealed(getTeam(), false))
		{
			pLoopPlot->setRevealed(GET_PLAYER(eNewPlayer).getTeam(), true, false, getTeam(), false);
		}
	}

	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->area() == pArea)
		{
			int iCulture = pLoopCity->getCultureTimes100(getID());
			CvPlot* pPlot = pLoopCity->plot();

			GET_PLAYER(eNewPlayer).acquireCity(pLoopCity, false, true, false);

			if (NULL != pPlot)
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (NULL != pCity)
				{
					pCity->setCultureTimes100(eNewPlayer, iCulture, false, false);
				}
//>>>>Unofficial Bug Fix: Deleted by Denev 2010/02/22
/*
//FfH: Added by Kael 01/16/2009 (to prevent CtD's when colony free units are dropped on top of hidden nationaliy units)
				CvUnit* pLoopUnit;
				CLLNode<IDInfo>* pUnitNode;
				pUnitNode = pPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);
					if (pLoopUnit->isHiddenNationality())
					{
						pLoopUnit->jumpToNearestValidPlot();
					}
				}
//FfH: End Add
*/
//<<<<Unofficial Bug Fix: End Delete
				for (int i = 0; i < GC.getDefineINT("COLONY_NUM_FREE_DEFENDERS"); ++i)
				{
					pCity->initConscriptedUnit();
				}
			}
		}
	}

	for (uint i = 0; i < aCultures.size(); ++i)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(aCultures[i].first);
		pPlot->setCulture(eNewPlayer, aCultures[i].second, true, false);
		pPlot->setCulture(getID(), 0, true, false);

		for (int iTeam = 0; iTeam < MAX_TEAMS; ++iTeam)
		{
			if (pPlot->getRevealedOwner((TeamTypes)iTeam, false) == getID())
			{
				pPlot->setRevealedOwner((TeamTypes)iTeam, eNewPlayer);
			}
		}
	}

	GC.getGameINLINE().updatePlotGroups();

	return true;
}

//>>>>Unofficial Bug Fix: Added by Denev 2010/02/20
PlayerTypes CvPlayer::initNewEmpire(LeaderHeadTypes eNewLeader, CivilizationTypes eNewCiv)
{
	FAssert(eNewLeader != NO_LEADER);
	FAssert(eNewCiv != NO_CIVILIZATION);

	PlayerTypes eNewPlayer = getOpenPlayer();
	FAssert(eNewPlayer != NO_PLAYER);
	FAssert(!GET_TEAM(GET_PLAYER(eNewPlayer).getTeam()).isAlive());

	if (eNewPlayer != NO_PLAYER)
	{
		// remove leftover culture from old recycled player
		for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
		{
			CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

			pLoopPlot->setCulture(eNewPlayer, 0, false, false);
		}

		GC.getGameINLINE().addPlayer(eNewPlayer, eNewLeader, eNewCiv);
		GC.getInitCore().setLeaderName(eNewPlayer, GC.getLeaderHeadInfo(eNewLeader).getTextKeyWide());

		CvTeam& kNewTeam = GET_TEAM(GET_PLAYER(eNewPlayer).getTeam());
		for (int i = 0; i < GC.getNumTechInfos(); ++i)
		{
			if ((GC.getCivilizationInfo(eNewCiv).isCivilizationFreeTechs((TechTypes)i)))
			{
				kNewTeam.setHasTech((TechTypes)i, true, eNewPlayer, false, false);
			}
			else if (GET_TEAM(getTeam()).isHasTech((TechTypes)i) && GET_PLAYER(eNewPlayer).canEverResearch((TechTypes)i))
			{
				kNewTeam.setHasTech((TechTypes)i, true, eNewPlayer, false, false);
				if (GET_TEAM(getTeam()).isNoTradeTech((TechTypes)i) || GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING))
				{
					kNewTeam.setNoTradeTech((TechTypes)i, true);
				}
			}
		}

		ReligionTypes eFavorite = getFavoriteReligion();
		ReligionTypes eNewFavorite = GET_PLAYER(eNewPlayer).getFavoriteReligion();

		if (eFavorite != NO_RELIGION)
		{
			if (eNewFavorite == NO_RELIGION)
			{
				GET_PLAYER(eNewPlayer).setFavoriteReligion(eFavorite);
			}
		}

		for (int iTeam = 0; iTeam < GC.getMAX_TEAMS(); iTeam++)
		{
			CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iTeam);

			if (kLoopTeam.isAlive())
			{
				kNewTeam.setEspionagePointsAgainstTeam((TeamTypes)iTeam, GET_TEAM(getTeam()).getEspionagePointsAgainstTeam((TeamTypes)iTeam));
				kLoopTeam.setEspionagePointsAgainstTeam(GET_PLAYER(eNewPlayer).getTeam(), kLoopTeam.getEspionagePointsAgainstTeam(getTeam()));
			}
		}
		kNewTeam.setEspionagePointsEver(GET_TEAM(getTeam()).getEspionagePointsEver());

		AI_updateBonusValue();

		kNewTeam.AI_updateAreaStragies(); // fix 05/2020 lfgr
	}

	return eNewPlayer;
}
//<<<<Unofficial Bug Fix: End Add

// MNAI - Puppet States
//returns a player number for the new player
PlayerTypes CvPlayer::getPuppetPlayer() const
{
    PlayerTypes eNewPlayer = NO_PLAYER;
    for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
    {
        if (!GET_PLAYER((PlayerTypes)i).isEverAlive())
        {
            eNewPlayer = (PlayerTypes)i;
            break;
        }
    }

    return eNewPlayer;
}

/********************************************************************************/
/* MinorPuppetLeaders	03/2015											lfgr	*/
/********************************************************************************/
/* old
bool CvPlayer::canMakePuppet(PlayerTypes eFromPlayer) const
{
*/
bool CvPlayer::canMakePuppet( CvCity* pVassalCapital ) const
{
	//PlayerTypes eFromPlayer = pVassalCapital->getOwnerINLINE();
	PlayerTypes eFromPlayer = pVassalCapital->getPreviousOwner();
/********************************************************************************/
/* MinorPuppetLeaders	End												lfgr	*/
/********************************************************************************/
	// Puppet States are a type of Vassal
    if (GC.getGameINLINE().isOption(GAMEOPTION_NO_VASSAL_STATES))
    {
        return false;
    }

    if (!GC.getGameINLINE().isOption(GAMEOPTION_PUPPET_STATES))
    {
        return false;
    }

	if (isBarbarian() || GET_PLAYER((PlayerTypes)eFromPlayer).isBarbarian())
	{
		return false;
	}

    if (GET_TEAM(getTeam()).isAVassal())
    {
        return false;
    }

	if (!GET_TEAM(getTeam()).isPuppetStateTrading())
	{
		return false;
	}

	/*
	if (!GET_TEAM(getTeam()).isVassalStateTrading())
	{
		return false;
	}
	*/

    PlayerTypes ePlayer = getPuppetPlayer();
    if (ePlayer == NO_PLAYER)
    {
        return false;
    }
    else if (GET_PLAYER(ePlayer).isAlive())
    {
        return false;
    }
	
/********************************************************************************/
/* MinorPuppetLeaders	03/2015											lfgr	*/
/********************************************************************************/
/* old
    CivLeaderArray aLeaders;
    if (!getPuppetLeaders(aLeaders))
    {
        return false;
    }
*/

	CyArgsList argsList;
	argsList.add( this->getID() );
	argsList.add( pVassalCapital->getOriginalOwner() );
	argsList.add( pVassalCapital->getID() );
	long lResult = 0;
	// Use canHavePuppetCivLeader, which does not perform random number calls.
	gDLL->getPythonIFace()->callFunction( PYRevModule, "canHavePuppetCivLeader", argsList.makeFunctionArgs(), &lResult );

	if (lResult == 0)
		return false;

/********************************************************************************/
/* MinorPuppetLeaders	End												lfgr	*/
/********************************************************************************/

    if (findPuppetPlayer(eFromPlayer) != NO_PLAYER)
    {
        return false;
    }

	bool bMatchingPuppetCiv = false;
	// only one puppet per player per civ-type
	// loop through all players
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
    {
		//if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam())
		// find those that are Puppets
		if (GET_PLAYER((PlayerTypes)iI).isPuppetState())
		{
			// see if they are our Puppets
			if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isVassal(getTeam()))
			{
				// see if they match the civ-type of the current civ we're trying to Puppet
				if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == GET_PLAYER((PlayerTypes)eFromPlayer).getCivilizationType())
				{
					bMatchingPuppetCiv = true;
					break;
				}
			}
		}
	}

	if (bMatchingPuppetCiv)
	{
		return false;
	}

    return true;
}

// lfgr MinorPuppetLeaders 03/2015: removed getPuppetLeaders(). Now handled in python.

bool CvPlayer::makePuppet(PlayerTypes eSplitPlayer, CvCity* pVassalCapital)
{
    PROFILE_FUNC();

    int iI;

    if ( !canMakePuppet( pVassalCapital ) )
    {
        return false;
    }

    PlayerTypes eNewPlayer = getPuppetPlayer();
    if (eNewPlayer == NO_PLAYER)
    {
        return false;
    }

	CvPlayerAI &kNewPlayer = GET_PLAYER(eNewPlayer);

    bool bPlayerExists = kNewPlayer.isAlive();
    FAssert(!bPlayerExists);
    if (!bPlayerExists)
    {
		int iValue = 0;
        int iBestValue = -1;
		int iBestLeader = -1;
        LeaderHeadTypes eBestLeader = NO_LEADER;
        CivilizationTypes eBestCiv = NO_CIVILIZATION;

		CyArgsList argsList;
		argsList.add( this->getID() );
		argsList.add( pVassalCapital->getOriginalOwner() );
		argsList.add( pVassalCapital->getID() );
		long lResult = 0;
		gDLL->getPythonIFace()->callFunction( PYRevModule, "getPuppetCivLeader", argsList.makeFunctionArgs(), &lResult );

		eBestLeader = (LeaderHeadTypes) (lResult % GC.getNumLeaderHeadInfos());
		eBestCiv = (CivilizationTypes) (lResult / GC.getNumLeaderHeadInfos());

		if (eBestLeader == NO_LEADER || eBestCiv == NO_CIVILIZATION)
		{
			return false;
		}

		CvWString szMessage = gDLL->getText("TXT_KEY_MISC_MAKE_PUPPET", getCivilizationAdjectiveKey(), pVassalCapital->getNameKey(), GC.getLeaderHeadInfo(eBestLeader).getTextKeyWide(), GC.getCivilizationInfo(eBestCiv).getShortDescriptionKey());
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			if (GET_PLAYER((PlayerTypes)i).isAlive())
			{
				if (i == getID() || i == eNewPlayer || GET_TEAM(GET_PLAYER((PlayerTypes)i).getTeam()).isHasMet(GET_PLAYER((PlayerTypes)getID()).getTeam()))
				{
					gDLL->getInterfaceIFace()->addMessage((PlayerTypes)i, false, GC.getEVENT_MESSAGE_TIME(), szMessage, "AS2D_REVOLTEND", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_CITY_BAR_CAPITAL_TEXTURE")->getPath());
				}
			}
		}
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szMessage, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

		GC.getGameINLINE().addPlayer(eNewPlayer, eBestLeader, eBestCiv);

		kNewPlayer = GET_PLAYER(eNewPlayer); //reset this variable
		kNewPlayer.setParent(GET_PLAYER(eSplitPlayer).getID());

        if (getStateReligion() != NO_RELIGION)
        {
            if (kNewPlayer.getStateReligion() != getStateReligion())
            {
                if (kNewPlayer.canConvert(getStateReligion()))
                {
                    kNewPlayer.convert(getStateReligion());
                }
            }
        }

        for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
        {
            if (getCivics((CivicOptionTypes)iI) != kNewPlayer.getCivics((CivicOptionTypes)iI))
            {
                kNewPlayer.setCivics((CivicOptionTypes)iI, getCivics((CivicOptionTypes)iI));
            }
        }

		CvTeam& kNewTeam = GET_TEAM(kNewPlayer.getTeam());
		for (int i = 0; i < GC.getNumTechInfos(); ++i)
		{
			// only give free techs that both civs already have
			if (GET_TEAM(GET_PLAYER(eSplitPlayer).getTeam()).isHasTech((TechTypes)i) && GET_TEAM(getTeam()).isHasTech((TechTypes)i))
			{
				kNewTeam.setHasTech((TechTypes)i, true, eNewPlayer, false, false);
			}
		}

		if (!GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
		{
			for (int iTeam = 0; iTeam < MAX_TEAMS; ++iTeam)
			{
				CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iTeam);

				if (kLoopTeam.isAlive())
				{
					kNewTeam.setEspionagePointsAgainstTeam((TeamTypes)iTeam, GET_TEAM(GET_PLAYER(eSplitPlayer).getTeam()).getEspionagePointsAgainstTeam((TeamTypes)iTeam));
					kLoopTeam.setEspionagePointsAgainstTeam(kNewPlayer.getTeam(), kLoopTeam.getEspionagePointsAgainstTeam(GET_PLAYER(eSplitPlayer).getTeam()));
				}
			}
			kNewTeam.setEspionagePointsEver(GET_TEAM(GET_PLAYER(eSplitPlayer).getTeam()).getEspionagePointsEver());
		}

		GET_TEAM(getTeam()).assignVassal(kNewPlayer.getTeam(), true);
		kNewPlayer.setPuppetState(true);

		GET_TEAM(getTeam()).signOpenBorders(kNewPlayer.getTeam());
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			GET_TEAM(getTeam()).setHasEmbassy(kNewPlayer.getTeam(), true);
		}

		AI_updateBonusValue();
	}

	if (pVassalCapital != NULL)
	{
	    CvPlot* pPlot = pVassalCapital->plot();
		int iMultiplier = GC.getDefineINT("PUPPET_CULTURE_MULTIPLIER");
        int iCulture = ((100 + pVassalCapital->getCultureTimes100(eSplitPlayer)) * GC.getDefineINT("PUPPET_CULTURE_MULTIPLIER")) / 100;

        kNewPlayer.acquireCity(pVassalCapital, false, true, true);

		if (NULL != pPlot)
        {
            CvCity* pCity = pPlot->getPlotCity();
            if (NULL != pCity)
            {
            	pCity->setOccupationTimer(0);
		        pCity->setCultureTimes100(eNewPlayer, iCulture, true, true);

	            for (int i = 0; i < (GC.getDefineINT("COLONY_NUM_FREE_DEFENDERS") * 4); ++i)
	            {
	                pCity->initConscriptedUnit();
	            }

				int iFreeCount = GC.getHandicapInfo(getHandicapType()).getStartingWorkerUnits();
				iFreeCount += GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingWorkerUnits();
				iFreeCount += GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingWorkerUnits();
				iFreeCount += 2;
			
				if (iFreeCount > 0)
				{
					kNewPlayer.addFreeUnitAI(UNITAI_WORKER, iFreeCount);
				}
			}
        }
	}

	GC.getGameINLINE().updatePlotGroups();

	return true;
}

bool CvPlayer::annex(PlayerTypes eAnnexedPlayer) const
{
    int iI;
    bool bTransferPlot = false;
    CvPlayer& kPlayer = GET_PLAYER(eAnnexedPlayer);

    for (iI = 0; iI < GC.getNumTechInfos(); iI++)
    {
        if (GET_TEAM(kPlayer.getTeam()).isHasTech((TechTypes)iI))
        {
            GET_TEAM(getTeam()).setHasTech((TechTypes)iI, true, getID(), false, false);
        }
    }

	CvCity* pLoopCity;
	CvUnit* pLoopUnit;

	// Give cities
	int iLoop;
	for (pLoopCity = kPlayer.firstCity(&iLoop); pLoopCity != NULL; pLoopCity = kPlayer.nextCity(&iLoop))
	{
		GET_PLAYER(getID()).acquireCity(pLoopCity, false, true, true);
	}

	// Give units
	for(pLoopUnit = kPlayer.firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = kPlayer.nextUnit(&iLoop))
	{
		pLoopUnit->gift(getID());
	}

    // Change control of plots
	std::vector< std::pair<int, int> > aCultures;
	for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

		bool bTranferPlot = false;

        if (!bTransferPlot && pLoopPlot->getOwner() == eAnnexedPlayer)
        {
            bTransferPlot = true;
        }

		if (bTranferPlot)
		{
			int iCulture = pLoopPlot->getCulture(eAnnexedPlayer);

            iCulture = std::max(iCulture, pLoopPlot->getCulture(getID()));

			aCultures.push_back(std::make_pair(iPlot, iCulture));
		}
	}

	for (uint i = 0; i < aCultures.size(); ++i)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(aCultures[i].first);
		pPlot->setCulture(getID(), aCultures[i].second, true, false);
		pPlot->setCulture(eAnnexedPlayer, 0, true, false);

		for (int iTeam = 0; iTeam < MAX_TEAMS; ++iTeam)
		{
			if (pPlot->getRevealedOwner((TeamTypes)iTeam, false) == eAnnexedPlayer)
			{
				pPlot->setRevealedOwner((TeamTypes)iTeam, getID());
			}
		}
	}

	return true;

}

PlayerTypes CvPlayer::findPuppetPlayer(PlayerTypes eParent) const
{
    for (int iI = 0; iI < MAX_PLAYERS; iI++)
    {
        if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isVassal(getTeam()) && (GET_PLAYER((PlayerTypes)iI).getParent() == eParent))
        {
            return ((PlayerTypes)iI);
        }
    }
    return NO_PLAYER;
}
// MNAI - End Puppet States

/************************************************************************************************/
/* REVOLUTION_MOD                         11/15/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
// Add ePlayer's cities, units, techs, etc to this player
bool CvPlayer::assimilatePlayer( PlayerTypes ePlayer )
{
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	if( !kPlayer.isAlive() )
	{
		return false;
	}
	CvTeam& kTeam = GET_TEAM(kPlayer.getTeam());

	CvCity* pCapital = getCapitalCity();
	if( pCapital == NULL )
	{
		return false;
	}

	CvCity* pLoopCity = NULL;
	CvUnit* pLoopUnit = NULL;

	if( kTeam.isAtWar(getTeam()) )
	{
		kTeam.makePeace(getTeam(),false);
	}
	
	for(int iI = 0; iI < MAX_CIV_PLAYERS; iI++ )
	{
		if( kPlayer.canContact((PlayerTypes)iI) )
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_REV_MESS_ASSIMILATE", kPlayer.getCivilizationDescription(), getCivilizationDescription());
			gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, NULL, MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
		}
	}

	// Convert units
	int iLoop;
	for (pLoopUnit = kPlayer.firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = kPlayer.nextUnit(&iLoop))
	{
		CvUnit* pNewUnit = initUnit(pLoopUnit->getUnitType(), pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE());
		pNewUnit->convert(pLoopUnit);
	}

	// Convert cities
	for (pLoopCity = kPlayer.firstCity(&iLoop); pLoopCity != NULL; pLoopCity = kPlayer.nextCity(&iLoop))
	{
		CvPlot* pPlot = pLoopCity->plot();
		pPlot->setOwner(getID(), false, false);
		pLoopCity = pPlot->getPlotCity();

		pLoopCity->changeCultureTimes100(getID(), pLoopCity->getCultureTimes100(kPlayer.getID())/2, true, false);
		pPlot->changeCulture(getID(), pPlot->getCulture(kPlayer.getID())/2, false);
	}	

	// Add Techs
	for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
	{
		if( kTeam.isHasTech((TechTypes)iI) && !(GET_TEAM(getTeam()).isHasTech((TechTypes)iI)) )
		{
			GET_TEAM(getTeam()).setHasTech((TechTypes)iI, true, getID(), false, false);
		}
	}

	// Share map
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->isRevealed(kTeam.getID(), false))
		{
			pLoopPlot->setRevealed(getTeam(), true, false, kTeam.getID(), false);
		}
	}

	// Diplomacy
	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		if ((iI != getTeam()) && (iI != kTeam.getID()))
		{
			if (GET_TEAM((TeamTypes)iI).isAlive())
			{
				if (kTeam.isHasMet((TeamTypes)iI))
				{
					GET_TEAM(getTeam()).meet(((TeamTypes)iI), false);
				}
			}
		}
	}

	// Make sure assimilated player is dead
	kPlayer.killUnits();
	kPlayer.killCities();

	for (int i = 0; i < GC.getMapINLINE().numPlotsINLINE(); ++i)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(i);
		if (pLoopPlot && (pLoopPlot->getTeam() == getTeam() || pLoopPlot->getTeam() == kTeam.getID()))
		{
			pLoopPlot->updateCulture(true, false);
		}
	}

	GC.getGameINLINE().updatePlotGroups();
	GC.getMapINLINE().verifyUnitValidPlot();

	GET_TEAM(getTeam()).AI_updateWorstEnemy();
	GET_TEAM(getTeam()).AI_updateAreaStragies();

	GC.getGameINLINE().updateScore(true);

	return true;
}
/************************************************************************************************/
/* REVOLUTION_MOD                          END                                                  */
/************************************************************************************************/

bool CvPlayer::isValidTriggerReligion(const CvEventTriggerInfo& kTrigger, CvCity* pCity, ReligionTypes eReligion) const
{
	if (kTrigger.getNumReligionsRequired() > 0)
	{
		bool bFound = false;

		for (int i = 0; i < kTrigger.getNumReligionsRequired(); ++i)
		{
			if (eReligion == kTrigger.getReligionRequired(i))
			{
				bFound = true;
				break;
			}
		}

		if (!bFound)
		{
			return false;
		}
	}

	if (NULL != pCity)
	{
		if (!pCity->isHasReligion(eReligion))
		{
			return false;
		}

		if (kTrigger.isHolyCity())
		{
			if (!pCity->isHolyCity(eReligion))
			{
				return false;
			}
		}
	}
	else
	{
		if (0 == getHasReligionCount(eReligion))
		{
			return false;
		}

		if (kTrigger.isHolyCity())
		{
			CvCity* pHolyCity = GC.getGameINLINE().getHolyCity(eReligion);
			if (NULL == pHolyCity || pHolyCity->getOwnerINLINE() != getID())
			{
				return false;
			}
		}
	}

	return true;
}

bool CvPlayer::isValidTriggerCorporation(const CvEventTriggerInfo& kTrigger, CvCity* pCity, CorporationTypes eCorporation) const
{
	if (kTrigger.getNumCorporationsRequired() > 0)
	{
		bool bFound = false;

		for (int i = 0; i < kTrigger.getNumCorporationsRequired(); ++i)
		{
			if (eCorporation == kTrigger.getCorporationRequired(i))
			{
				bFound = true;
				break;
			}
		}

		if (!bFound)
		{
			return false;
		}
	}

	if (NULL != pCity)
	{
		if (!pCity->isHasCorporation(eCorporation))
		{
			return false;
		}

		if (kTrigger.isHeadquarters())
		{
			if (!pCity->isHeadquarters(eCorporation))
			{
				return false;
			}
		}
	}
	else
	{
		if (getHasCorporationCount(eCorporation) > 0)
		{
			return true;
		}

		if (kTrigger.isHeadquarters())
		{
			CvCity* pHeadquarters = GC.getGameINLINE().getHeadquarters(eCorporation);
			if (NULL == pHeadquarters || pHeadquarters->getOwnerINLINE() != getID())
			{
				return false;
			}
		}
	}

	return false;
}

void CvPlayer::launch(VictoryTypes eVictory)
{
	CvTeam& kTeam = GET_TEAM(getTeam());

	if (!kTeam.canLaunch(eVictory))
	{
		return;
	}

	kTeam.finalizeProjectArtTypes();
	kTeam.setVictoryCountdown(eVictory, kTeam.getVictoryDelay(eVictory));

	// K-Mod. The spaceship launch causes pitboss to crash
	if (!gDLL->IsPitbossHost())
		gDLL->getEngineIFace()->AddLaunch(getID());
	// K-Mod end.

	kTeam.setCanLaunch(eVictory, false);

	CvCity *capital = getCapitalCity();

	//message
	CvWString szBuffer;
	for(int i = 0; i < MAX_PLAYERS; ++i)
	{
		if (GET_PLAYER((PlayerTypes)i).isAlive())
		{
			int plotX = -1;
			int plotY = -1;
			if((capital != NULL) && capital->isRevealed(GET_PLAYER((PlayerTypes) i).getTeam(), false))
			{
				plotX = capital->getX();
				plotY = capital->getY();
			}

			if (GET_PLAYER((PlayerTypes)i).getTeam() == getTeam())
			{
				szBuffer = gDLL->getText("TXT_KEY_VICTORY_YOU_HAVE_LAUNCHED");
			}
			else
			{
				szBuffer = gDLL->getText("TXT_KEY_VICTORY_TEAM_HAS_LAUNCHED", GET_TEAM(getTeam()).getName().GetCString());
			}

			gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)i), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getMiscArtInfo("SPACE_SHIP_BUTTON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), plotX, plotY, true, true);
		}
	}
}

bool CvPlayer::isFreePromotion(UnitCombatTypes eUnitCombat, PromotionTypes ePromotion) const
{
	for (UnitCombatPromotionArray::const_iterator it = m_aFreeUnitCombatPromotions.begin(); it != m_aFreeUnitCombatPromotions.end(); ++it)
	{
		if ((*it).first == eUnitCombat && (*it).second == ePromotion)
		{
			return true;
		}
	}

	return false;
}

void CvPlayer::setFreePromotion(UnitCombatTypes eUnitCombat, PromotionTypes ePromotion, bool bFree)
{
	for (UnitCombatPromotionArray::iterator it = m_aFreeUnitCombatPromotions.begin(); it != m_aFreeUnitCombatPromotions.end(); ++it)
	{
		if ((*it).first == eUnitCombat && (*it).second == ePromotion)
		{
			if (!bFree)
			{
				m_aFreeUnitCombatPromotions.erase(it);
			}
			return;
		}
	}

	if (bFree)
	{
		m_aFreeUnitCombatPromotions.push_back(std::make_pair(eUnitCombat, ePromotion));
	}
}

bool CvPlayer::isFreePromotion(UnitClassTypes eUnitClass, PromotionTypes ePromotion) const
{
	for (UnitClassPromotionArray::const_iterator it = m_aFreeUnitClassPromotions.begin(); it != m_aFreeUnitClassPromotions.end(); ++it)
	{
		if ((*it).first == eUnitClass && (*it).second == ePromotion)
		{
			return true;
		}
	}

	return false;
}

void CvPlayer::setFreePromotion(UnitClassTypes eUnitClass, PromotionTypes ePromotion, bool bFree)
{
	for (UnitClassPromotionArray::iterator it = m_aFreeUnitClassPromotions.begin(); it != m_aFreeUnitClassPromotions.end(); ++it)
	{
		if ((*it).first == eUnitClass && (*it).second == ePromotion)
		{
			if (!bFree)
			{
				m_aFreeUnitClassPromotions.erase(it);
			}
			return;
		}
	}

	if (bFree)
	{
		m_aFreeUnitClassPromotions.push_back(std::make_pair(eUnitClass, ePromotion));
	}
}

PlayerVoteTypes CvPlayer::getVote(int iId) const
{
	for (std::vector< std::pair<int, PlayerVoteTypes> >::const_iterator it = m_aVote.begin(); it != m_aVote.end(); ++it)
	{
		if ((*it).first == iId)
		{
			return ((*it).second);
		}
	}

	return NO_PLAYER_VOTE;
}

void CvPlayer::setVote(int iId, PlayerVoteTypes ePlayerVote)
{
	for (std::vector< std::pair<int, PlayerVoteTypes> >::iterator it = m_aVote.begin(); it != m_aVote.end(); ++it)
	{
		if ((*it).first == iId)
		{
			if (ePlayerVote == NO_PLAYER_VOTE)
			{
				m_aVote.erase(it);
			}
			else
			{
				(*it).second = ePlayerVote;
			}
			return;
		}
	}

	if (ePlayerVote != NO_PLAYER_VOTE)
	{
		m_aVote.push_back(std::make_pair(iId, ePlayerVote));
	}
}

int CvPlayer::getUnitExtraCost(UnitClassTypes eUnitClass) const
{
	for (std::vector< std::pair<UnitClassTypes, int> >::const_iterator it = m_aUnitExtraCosts.begin(); it != m_aUnitExtraCosts.end(); ++it)
	{
		if ((*it).first == eUnitClass)
		{
			return ((*it).second);
		}
	}

	return 0;
}

void CvPlayer::setUnitExtraCost(UnitClassTypes eUnitClass, int iCost)
{
	for (std::vector< std::pair<UnitClassTypes, int> >::iterator it = m_aUnitExtraCosts.begin(); it != m_aUnitExtraCosts.end(); ++it)
	{
		if ((*it).first == eUnitClass)
		{
			if (0 == iCost)
			{
				m_aUnitExtraCosts.erase(it);
			}
			else
			{
				(*it).second = iCost;
			}
			return;
		}
	}

	if (0 != iCost)
	{
		m_aUnitExtraCosts.push_back(std::make_pair(eUnitClass, iCost));
	}
}

// CACHE: cache frequently used values
///////////////////////////////////////
bool CvPlayer::hasShrine(ReligionTypes eReligion)
{
	bool bHasShrine = false;

	if (eReligion != NO_RELIGION)
	{
		CvCity* pHolyCity = GC.getGameINLINE().getHolyCity(eReligion);

		// if the holy city exists, and we own it
		if (pHolyCity != NULL && pHolyCity->getOwnerINLINE() == getID())
			bHasShrine = pHolyCity->hasShrine(eReligion);
	}
	return bHasShrine;
}

void CvPlayer::invalidatePopulationRankCache()
{
	int iLoop;
	CvCity* pLoopCity;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->invalidatePopulationRankCache();
	}
}

void CvPlayer::invalidateYieldRankCache(YieldTypes eYield)
{
	int iLoop;
	CvCity* pLoopCity;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->invalidateYieldRankCache();
	}
}

void CvPlayer::invalidateCommerceRankCache(CommerceTypes eCommerce)
{
	int iLoop;
	CvCity* pLoopCity;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->invalidateCommerceRankCache();
	}
}


void CvPlayer::doUpdateCacheOnTurn()
{
	// add this back, after testing without it
	// invalidateYieldRankCache();
}

void CvPlayer::processVoteSourceBonus(VoteSourceTypes eVoteSource, bool bActive)
{
	int iLoop;
	for (CvCity* pCity = firstCity(&iLoop); NULL != pCity; pCity = nextCity(&iLoop))
	{
		pCity->processVoteSourceBonus(eVoteSource, bActive);
	}
}

#if !defined(USE_OLD_CODE)
bool CvPlayer::hasVotes(ReligionTypes eReligion) const
{
	if (NO_RELIGION != eReligion)
	{
		// iVotes = getReligionPopulation(eReligion);
		int iLoop;
		for (CvCity* pCity = firstCity(&iLoop); NULL != pCity; pCity = nextCity(&iLoop))
		{
			if (pCity->isHasReligion(eReligion) && pCity->getPopulation() > 0)
			{
				return true;
			}
		}
	}
	else
	{
		// iVotes = getTotalPopulation();
		if( m_iTotalPopulation > 0 )
			return true;
	}

//FfH: Added by Kael 11/14/2007
	int iLoop;
	for(CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (GC.getUnitInfo(pLoopUnit->getUnitTypeINLINE()).getDiploVoteType() != NO_VOTESOURCE)
		{
			if (pLoopUnit->getDuration() == 0)
			{
			    return true;
			}
		}
	}
//FfH: End Add

	return false;
}
#endif

int CvPlayer::getVotes(VoteTypes eVote, VoteSourceTypes eVoteSource) const
{
	int iVotes = 0;

	ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(eVoteSource);

//FfH: Added by Kael 11/15/2007
    if (GC.getVoteSourceInfo(eVoteSource).getCivic() != NO_CIVIC)
    {
        if (!isCivic((CivicTypes)GC.getVoteSourceInfo(eVoteSource).getCivic()))
        {
            return 0;
        }
    }
//FfH: End Add

	if (NO_VOTE == eVote)
	{
		if (NO_RELIGION != eReligion)
		{
			iVotes = getReligionPopulation(eReligion);
		}
		else
		{
			iVotes = getTotalPopulation();
		}
	}
	else
	{
		if (!GC.getVoteInfo(eVote).isVoteSourceType(eVoteSource))
		{
			return 0;
		}

		if (GC.getVoteInfo(eVote).isCivVoting())
		{
			if (NO_RELIGION == eReligion || getHasReligionCount(eReligion) > 0)
			{
				iVotes = 1;
			}
		}
		else if (GC.getVoteInfo(eVote).isCityVoting())
		{
			if (NO_RELIGION != eReligion)
			{
				iVotes = getHasReligionCount(eReligion);
			}
			else
			{
				iVotes = getNumCities();
			}
		}
		else
		{
			if (NO_RELIGION == eReligion)
			{
				iVotes = getTotalPopulation();
			}
			else
			{
				iVotes = getReligionPopulation(eReligion);
			}
		}

		if (NO_RELIGION != eReligion && getStateReligion() == eReligion)
		{
			iVotes *= (100 + GC.getVoteInfo(eVote).getStateReligionVotePercent());
			iVotes /= 100;
		}
	}

//FfH: Added by Kael 11/14/2007
	CvUnit* pLoopUnit;
	int iLoop;
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
#ifdef USE_OLD_CODE
		if (GC.getUnitInfo(pLoopUnit->getUnitType()).getDiploVoteType() != NO_VOTESOURCE)
#else
		if (GC.getUnitInfo(pLoopUnit->getUnitTypeINLINE()).getDiploVoteType() != NO_VOTESOURCE)
#endif
		{
			if (GC.getUnitInfo(pLoopUnit->getUnitTypeINLINE()).getDiploVoteType() == eVoteSource)
			{
				if (pLoopUnit->getDuration() == 0)
				{
				    iVotes += 1;
				}
			}
		}
	}
//FfH: End Add

	return iVotes;
}

/************************************************************************************************/
/* Advanced Diplomacy         START                                                             */
/************************************************************************************************/
/*
bool CvPlayer::isCivicCondemned() const
{
	//if (GC.getGameINLINE().isCondemnCivicCountArrayValid()) 
	{
		int numCivicOptionInfos = GC.getNumCivicOptionInfos();
		for (int iI = 0; iI < numCivicOptionInfos; iI++)
		{   
			if (GC.getGameINLINE().isCondemnCivic(getCivics((CivicOptionTypes)iI)))
			{
				return true;
			}
		}
	}

	return false;
}
*/
/************************************************************************************************/
/* Advanced Diplomacy         END                                                             */
/************************************************************************************************/

bool CvPlayer::canDoResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const
{
	CvTeam& kOurTeam = GET_TEAM(getTeam());

	if (NO_PLAYER != kData.ePlayer)
	{
		if (!kOurTeam.isHasMet(GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return false;
		}
	}

	if (GC.getVoteInfo(kData.eVote).isOpenBorders())
	{
		for (int iTeam2 = 0; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
		{
			if (GET_TEAM((TeamTypes)iTeam2).isVotingMember(eVoteSource))
			{
				if (!kOurTeam.isOpenBordersTrading() && !GET_TEAM((TeamTypes)iTeam2).isOpenBordersTrading())
				{
					return false;
				}

				if (kOurTeam.isAtWar((TeamTypes)iTeam2))
				{
					return false;
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isDefensivePact())
	{
		for (int iTeam2 = 0; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
		{
			if (GET_TEAM((TeamTypes)iTeam2).isVotingMember(eVoteSource))
			{
				if (!kOurTeam.isDefensivePactTrading() && !GET_TEAM((TeamTypes)iTeam2).isDefensivePactTrading())
				{
					return false;
				}

				if (kOurTeam.getAtWarCount(true) > 0 || GET_TEAM((TeamTypes)iTeam2).getAtWarCount(true) > 0)
				{
					return false;
				}

				if (!kOurTeam.canSignDefensivePact((TeamTypes)iTeam2))
				{
					return false;
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForcePeace())
	{
		FAssert(NO_PLAYER != kData.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (kPlayer.getTeam() != getTeam())
		{
			if (kOurTeam.isAtWar(kPlayer.getTeam()))
			{
				TeamTypes eMaster = getTeam();
				for (int iMaster = 0; iMaster < MAX_CIV_TEAMS; ++iMaster)
				{
					if (iMaster != getID() && kOurTeam.isVassal((TeamTypes)iMaster))
					{
						if (GET_TEAM((TeamTypes)iMaster).isVotingMember(eVoteSource))
						{
							eMaster = (TeamTypes)iMaster;
							break;
						}
					}
				}

				if (!GET_TEAM(eMaster).canContact(kPlayer.getTeam()))
				{
					return false;
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceWar())
	{
		FAssert(NO_PLAYER != kData.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (!kOurTeam.isAtWar(kPlayer.getTeam()))
		{
			TeamTypes eMaster = getTeam();
			for (int iMaster = 0; iMaster < MAX_CIV_TEAMS; ++iMaster)
			{
				if (iMaster != getID() && kOurTeam.isVassal((TeamTypes)iMaster))
				{
					if (GET_TEAM((TeamTypes)iMaster).isVotingMember(eVoteSource))
					{
						eMaster = (TeamTypes)iMaster;
						break;
					}
				}
			}

			if (!GET_TEAM(eMaster).canDeclareWar(kPlayer.getTeam()))
			{
				return false;
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceNoTrade())
	{
		FAssert(NO_PLAYER != kData.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (!canStopTradingWithTeam(kPlayer.getTeam(), true))
		{
			return false;
		}

	}
	else if (GC.getVoteInfo(kData.eVote).isAssignCity())
	{
		if (GET_TEAM(GET_PLAYER(kData.eOtherPlayer).getTeam()).isVassal(GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return false;
		}
	}

	return true;
}

bool CvPlayer::canDefyResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const
{
	if (GC.getGameINLINE().getSecretaryGeneral(eVoteSource) == getTeam())
	{
		return false;
	}

	if (GC.getVoteInfo(kData.eVote).isOpenBorders())
	{
		for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iTeam);
			if ((PlayerTypes)iTeam != getTeam())
			{
				if (kTeam.isVotingMember(eVoteSource))
				{
					if (!kTeam.isOpenBorders(getTeam()))
					{
						return true;
					}
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isDefensivePact())
	{
		for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iTeam);
			if ((PlayerTypes)iTeam != getTeam())
			{
				if (kTeam.isVotingMember(eVoteSource))
				{
					if (!kTeam.isDefensivePact(getTeam()))
					{
						return true;
					}
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceNoTrade())
	{
		return true;
	}
	else if (GC.getVoteInfo(kData.eVote).isForceWar())
	{
		if (!::atWar(getTeam(), GET_PLAYER(kData.ePlayer).getTeam()))
		{
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      12/31/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
			// Vassals can't defy declarations of war
			if( !GET_TEAM(getTeam()).isAVassal() )
			{
				return true;
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForcePeace())
	{
		if (GET_PLAYER(kData.ePlayer).getTeam() == getTeam())
		{
			return true;
		}

		if (::atWar(getTeam(), GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return true;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isAssignCity())
	{
		if (kData.ePlayer == getID())
		{
			return true;
		}
	}
	else if (!GC.getGameINLINE().isTeamVote(kData.eVote))
	{
		return true;
	}

	return false;
}


void CvPlayer::setDefiedResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData)
{
	FAssert(canDefyResolution(eVoteSource, kData));

	// cities get unhappiness
	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
	{
		ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(eVoteSource);

		if (NO_RELIGION == eReligion || pLoopCity->isHasReligion(eReligion))
		{
			int iAngerLength = pLoopCity->flatDefyResolutionAngerLength();
			if (NO_RELIGION != eReligion && pLoopCity->isHasReligion(eReligion))
			{
				iAngerLength /= std::max(1, pLoopCity->getReligionCount());
			}

			pLoopCity->changeDefyResolutionAngerTimer(iAngerLength);
		}
	}

	setLoyalMember(eVoteSource, false);
}


void CvPlayer::setEndorsedResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData)
{
	setLoyalMember(eVoteSource, true);
}

bool CvPlayer::isFullMember(VoteSourceTypes eVoteSource) const
{PROFILE_FUNC()
#if defined(USE_OLD_CODE)
	if (NO_RELIGION != GC.getGameINLINE().getVoteSourceReligion(eVoteSource))
	{
		if (getStateReligion() != GC.getGameINLINE().getVoteSourceReligion(eVoteSource))
		{
			return false;
		}
	}

	if (NO_CIVIC != GC.getVoteSourceInfo(eVoteSource).getCivic())
	{
		if (!isCivic((CivicTypes)GC.getVoteSourceInfo(eVoteSource).getCivic()))
		{
			return false;
		}
	}

	if (!isLoyalMember(eVoteSource))
	{
		return false;
	}

	return isVotingMember(eVoteSource);
#else
	ReligionTypes eReligionType = GC.getGameINLINE().getVoteSourceReligion(eVoteSource);
	if (NO_RELIGION != eReligionType)
	{
		if (getStateReligion() != eReligionType)
		{ 
			return false;
		}
	}
	// duplicate check
	const CvVoteSourceInfo &kVoteSourceInfo = GC.getVoteSourceInfo(eVoteSource);
	if (NO_CIVIC != kVoteSourceInfo.getCivicINLINE())
	{
		if (!isCivic((CivicTypes)kVoteSourceInfo.getCivicINLINE()))
		{
			return false;
		}
	}

	if (!isLoyalMember(eVoteSource))
	{
		return false;
	}

	return hasVotes(eReligionType);
#endif
}

bool CvPlayer::isVotingMember(VoteSourceTypes eVoteSource) const
{

//FfH: Added by Kael 11/15/2007
	if (GC.getVoteSourceInfo(eVoteSource).getCivic() != NO_CIVIC)
	{
		if (!isCivic((CivicTypes)GC.getVoteSourceInfo(eVoteSource).getCivic()))
		{
			return false;
		}
	}
//FfH: End Add

#if defined(USE_OLD_CODE)
	return (getVotes(NO_VOTE, eVoteSource) > 0);
#else
	return hasVotes(GC.getGameINLINE().getVoteSourceReligion(eVoteSource));
#endif
}

#if 0 // !defined(USE_OLD_CODE)
bool CvPlayer::isVotingMember(const CvVoteSourceInfo &kVoteSourceInfo, VoteSourceTypes eVoteSource) const
{
//FfH: Added by Kael 11/15/2007
	if (kVoteSourceInfo.getCivicINLINE() != NO_CIVIC)
	{
		if (!isCivic((CivicTypes)kVoteSourceInfo.getCivicINLINE()))
		{
			return false;
		}
	}
//FfH: End Add

	return hasVotes(GC.getGameINLINE().getVoteSourceReligion(eVoteSource));
}
#endif

PlayerTypes CvPlayer::pickConqueredCityOwner(const CvCity& kCity) const
{
	PlayerTypes eBestPlayer = kCity.getLiberationPlayer(true);

	if (NO_PLAYER != eBestPlayer)
	{
		if (GET_TEAM(getTeam()).isVassal(GET_PLAYER(eBestPlayer).getTeam()))
		{
			return eBestPlayer;
		}
	}

	return getID();
}

bool CvPlayer::canHaveTradeRoutesWith(PlayerTypes ePlayer) const
{
	CvPlayer& kOtherPlayer = GET_PLAYER(ePlayer);

	if (!kOtherPlayer.isAlive())
	{
		return false;
	}

	if (getTeam() == kOtherPlayer.getTeam())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isFreeTrade(kOtherPlayer.getTeam()))
	{
		if (GET_TEAM(getTeam()).isVassal(kOtherPlayer.getTeam()))
		{
			return true;
		}

		if (GET_TEAM(kOtherPlayer.getTeam()).isVassal(getTeam()))
		{
			return true;
		}

		if (!isNoForeignTrade() && !kOtherPlayer.isNoForeignTrade())
		{
			return true;
		}
	}

	return false;
}

bool CvPlayer::canStealTech(PlayerTypes eTarget, TechTypes eTech) const
{
	if (GET_TEAM(GET_PLAYER(eTarget).getTeam()).isHasTech(eTech))
	{
		if (canResearch(eTech))
		{
			return true;
		}
	}

	return false;
}

bool CvPlayer::canForceCivics(PlayerTypes eTarget, CivicTypes eCivic) const
{
	return (GET_PLAYER(eTarget).canDoCivics(eCivic) && !GET_PLAYER(eTarget).isCivic(eCivic) && isCivic(eCivic));
}

bool CvPlayer::canForceReligion(PlayerTypes eTarget, ReligionTypes eReligion) const
{
	return (GET_PLAYER(eTarget).canDoReligion(eReligion) && GET_PLAYER(eTarget).getStateReligion() != eReligion && getStateReligion() == eReligion);
}

bool CvPlayer::canSpyDestroyUnit(PlayerTypes eTarget, CvUnit& kUnit) const
{
	if (kUnit.getTeam() == getTeam())
	{
		return false;
	}

	if (kUnit.getUnitInfo().getProductionCost() <= 0)
	{
		return false;
	}

	if (!kUnit.plot()->isVisible(getTeam(), false))
	{
		return false;
	}

	return true;
}

bool CvPlayer::canSpyBribeUnit(PlayerTypes eTarget, CvUnit& kUnit) const
{
	if (!canSpyDestroyUnit(eTarget, kUnit))
	{
		return false;
	}

	// Can't buy units when at war
	if (kUnit.isEnemy(getTeam()))
	{
		return false;
	}

	// Can't buy units if they are not in a legal plot
	if (!GET_TEAM(getTeam()).isFriendlyTerritory(GET_PLAYER(eTarget).getTeam()) && !GET_TEAM(getTeam()).isOpenBorders(GET_PLAYER(eTarget).getTeam()))
	{
		return false;
	}

	CLLNode<IDInfo>* pUnitNode = kUnit.plot()->headUnitNode();

	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = kUnit.plot()->nextUnitNode(pUnitNode);

		if (NULL != pLoopUnit && pLoopUnit != &kUnit)
		{
			if (pLoopUnit->isEnemy(getTeam()))
			{
				// If we buy the unit, we will be on the same plot as an enemy unit! Not good.
				return false;
			}
		}
	}

	return true;
}

bool CvPlayer::canSpyDestroyBuilding(PlayerTypes eTarget, BuildingTypes eBuilding) const
{
	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	if (kBuilding.getProductionCost() <= 0)
	{
		return false;
	}

	if (::isLimitedWonderClass((BuildingClassTypes)kBuilding.getBuildingClassType()))
	{
		return false;
	}

	return true;
}

bool CvPlayer::canSpyDestroyProject(PlayerTypes eTarget, ProjectTypes eProject) const
{
	CvProjectInfo& kProject = GC.getProjectInfo(eProject);
	if (kProject.getProductionCost() <= 0)
	{
		return false;
	}

	if (GET_TEAM(GET_PLAYER(eTarget).getTeam()).getProjectCount(eProject) <= 0)
	{
		return false;
	}

	if (::isWorldProject(eProject))
	{
		return false;
	}

	if (!kProject.isSpaceship())
	{
		return false;
	}
	else
	{
		VictoryTypes eVicotry = (VictoryTypes)kProject.getVictoryPrereq();
		if (NO_VICTORY != eVicotry)
		{
			// Can't destroy spaceship components if we have already launched
			if (GET_TEAM(GET_PLAYER(eTarget).getTeam()).getVictoryCountdown(eVicotry) >= 0)
			{
				return false;
			}
		}
	}

	return true;
}

void CvPlayer::forcePeace(PlayerTypes ePlayer)
{
	if (!GET_TEAM(getTeam()).isAVassal())
	{
		FAssert(GET_TEAM(getTeam()).canChangeWarPeace(GET_PLAYER(ePlayer).getTeam()));

		CLinkList<TradeData> playerList;
		CLinkList<TradeData> loopPlayerList;
		TradeData kTradeData;
		setTradeItem(&kTradeData, TRADE_PEACE_TREATY);
		playerList.insertAtEnd(kTradeData);
		loopPlayerList.insertAtEnd(kTradeData);

		GC.getGameINLINE().implementDeal(getID(), ePlayer, &playerList, &loopPlayerList);
	}
}

bool CvPlayer::canSpiesEnterBorders(PlayerTypes ePlayer) const
{
	for (int iMission = 0; iMission < GC.getNumEspionageMissionInfos(); ++iMission)
	{
		if (GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).isNoActiveMissions() && GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).isPassive())
		{
			if (GET_PLAYER(ePlayer).canDoEspionageMission((EspionageMissionTypes)iMission, getID(), NULL, -1, NULL))
			{
				return false;
			}
		}
	}

	return true;
}

int CvPlayer::getReligionPopulation(ReligionTypes eReligion) const
{
	int iPopulation = 0;
	int iLoop;
	for (CvCity* pCity = firstCity(&iLoop); NULL != pCity; pCity = nextCity(&iLoop))
	{
		if (pCity->isHasReligion(eReligion))
		{
			iPopulation += pCity->getPopulation();
		}
	}

	return iPopulation;
}

int CvPlayer::getNewCityProductionValue() const
{
	int iValue = 0;
	for (int iJ = 0; iJ < GC.getNumBuildingClassInfos(); iJ++)
	{
		BuildingTypes eBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iJ)));

		if (NO_BUILDING != eBuilding)
		{
			if (GC.getBuildingInfo(eBuilding).getFreeStartEra() != NO_ERA)
			{
				if (GC.getGameINLINE().getStartEra() >= GC.getBuildingInfo(eBuilding).getFreeStartEra())
				{
					iValue += (100 * getProductionNeeded(eBuilding)) / std::max(1, 100 + getProductionModifier(eBuilding));
				}
			}
		}
	}

	iValue *= 100 + GC.getDefineINT("NEW_CITY_BUILDING_VALUE_MODIFIER");
	iValue /= 100;

	iValue += (GC.getDefineINT("ADVANCED_START_CITY_COST") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent()) / 100;

	int iPopulation = GC.getDefineINT("INITIAL_CITY_POPULATION") + GC.getEraInfo(GC.getGameINLINE().getStartEra()).getFreePopulation();
	for (int i = 1; i <= iPopulation; ++i)
	{
		iValue += (getGrowthThreshold(i) * GC.getDefineINT("ADVANCED_START_POPULATION_COST")) / 100;
	}

	return iValue;
}

int CvPlayer::getGrowthThreshold(int iPopulation) const
{
	int iThreshold;

	iThreshold = (GC.getDefineINT("BASE_CITY_GROWTH_THRESHOLD") + (iPopulation * GC.getDefineINT("CITY_GROWTH_MULTIPLIER")));

	iThreshold *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent();
	iThreshold /= 100;

	iThreshold *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getGrowthPercent();
	iThreshold /= 100;

	if (!isHuman() && !isBarbarian())
	{
		iThreshold *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIGrowthPercent();
		iThreshold /= 100;

		iThreshold *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentRealEra()) + 100));
		iThreshold /= 100;
	}

	return std::max(1, iThreshold);
}

void CvPlayer::verifyUnitStacksValid()
{
	int iLoop;
	for(CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		pLoopUnit->verifyStackValid();
	}
}

UnitTypes CvPlayer::getTechFreeUnit(TechTypes eTech) const
{
	UnitClassTypes eUnitClass = (UnitClassTypes) GC.getTechInfo(eTech).getFirstFreeUnitClass();
	if (eUnitClass == NO_UNITCLASS)
	{
		return NO_UNIT;
	}

	UnitTypes eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass)));
	if (eUnit == NO_UNIT)
	{
		return NO_UNIT;
	}

	if (GC.getUnitInfo(eUnit).getEspionagePoints() > 0 && GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		return NO_UNIT;
	}

	return eUnit;
}

// BUG - Trade Totals - start
/*
 * Adds the yield and count for each trade route with eWithPlayer.
 *
 * The yield and counts are not reset to zero.
 * If Fractional Trade Routes is enabled and bRound is false, the yield values are left times 100.
 */
void CvPlayer::calculateTradeTotals(YieldTypes eIndex, int& iDomesticYield, int& iDomesticRoutes, int& iForeignYield, int& iForeignRoutes, PlayerTypes eWithPlayer, bool bRound, bool bBase) const
{
	int iIter;

	for (CvCity* pCity = firstCity(&iIter); NULL != pCity; pCity = nextCity(&iIter))
	{
		pCity->calculateTradeTotals(eIndex, iDomesticYield, iDomesticRoutes, iForeignYield, iForeignRoutes, eWithPlayer, bRound, bBase);
	}
}

/*
 * Returns the total trade yield with eWithPlayer.
 *
 * If Fractional Trade Routes is enabled, the yield value is left times 100.
 * UNUSED
 */
int CvPlayer::calculateTotalTradeYield(YieldTypes eIndex, PlayerTypes eWithPlayer, bool bRound, bool bBase) const
{
	int iDomesticYield = 0;
	int iDomesticRoutes = 0;
	int iForeignYield = 0;
	int iForeignRoutes = 0;
	
	calculateTradeTotals(eIndex, iDomesticYield, iDomesticRoutes, iForeignYield, iForeignRoutes, eWithPlayer, bRound, bBase);
	return iDomesticYield + iForeignRoutes;
}
// BUG - Trade Totals - end


void CvPlayer::buildTradeTable(PlayerTypes eOtherPlayer, CLinkList<TradeData>& ourList) const
{
	TradeData item;
	int iLoop;

	//	Put the gold and maps into the table
	setTradeItem(&item, TRADE_GOLD);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Gold per turn
	setTradeItem(&item, TRADE_GOLD_PER_TURN);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Maps
	setTradeItem(&item, TRADE_MAPS, 0);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Vassal
	setTradeItem(&item, TRADE_VASSAL, 0);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}
/************************************************************************************************/
/* Afforess	                  Start		 06/16/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
  	//Right of Passage
	setTradeItem(&item, TRADE_RIGHT_OF_PASSAGE);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}  
	
	//Embassy
    setTradeItem(&item, TRADE_EMBASSY);
    if (canTradeItem(eOtherPlayer, item))
    {
        ourList.insertAtEnd(item);
    }
	
	//Free Trade
	setTradeItem(&item, TRADE_FREE_TRADE_ZONE);
    if (canTradeItem(eOtherPlayer, item))
    {
        ourList.insertAtEnd(item);
    }

	// NonAggression
	setTradeItem(&item, TRADE_NON_AGGRESSION);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	// POW
	setTradeItem(&item, TRADE_POW);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}
	
	//War Reparations
	setTradeItem(&item, TRADE_WAR_REPARATIONS);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

	//	Open Borders
	setTradeItem(&item, TRADE_OPEN_BORDERS);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Defensive Pact
	setTradeItem(&item, TRADE_DEFENSIVE_PACT);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Permanent Alliance
	setTradeItem(&item, TRADE_PERMANENT_ALLIANCE);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	if (::atWar(getTeam(), GET_PLAYER(eOtherPlayer).getTeam()))
	{
		//	We are at war, allow a peace treaty option
		setTradeItem(&item, TRADE_PEACE_TREATY);
		ourList.insertAtEnd(item);

		//	Capitulation
		setTradeItem(&item, TRADE_SURRENDER, 0);
		if (canTradeItem(eOtherPlayer, item))
		{
			ourList.insertAtEnd(item);
		}
	}

	//	Initial build of the inventory lists and buttons.
	//	Go through all the possible headings
	for (int i = NUM_BASIC_ITEMS; i < NUM_TRADEABLE_HEADINGS; i++)
	{
		bool bFoundItemUs = false;

		//	Build what we need to build for this item
		switch (i)
		{
		case TRADE_TECHNOLOGIES:
			for (int j = 0; j < GC.getNumTechInfos(); j++)
			{
				setTradeItem(&item, TRADE_TECHNOLOGIES, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_RESOURCES:
			for (int j = 0; j < GC.getNumBonusInfos(); j++)
			{
				setTradeItem(&item, TRADE_RESOURCES, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_CITIES:
			for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				setTradeItem(&item, TRADE_CITIES, pLoopCity->getID());
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_PEACE:
			if (!isHuman())
			{
				for (int j = 0; j < MAX_CIV_TEAMS; j++)
				{
					if (GET_TEAM((TeamTypes)j).isAlive())
					{
						if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
						{
							setTradeItem(&item, TRADE_PEACE, j);
							if (canTradeItem(eOtherPlayer, item))
							{
								ourList.insertAtEnd(item);
								bFoundItemUs = true;
							}
						}
					}
				}
			}
			break;

		case TRADE_WAR:
			// lfgr 08/2023
			if( GC.getDefineINT( "NO_WAR_TRADE", 0 ) ) {
				break;
			}
			if (!isHuman())
			{
				for (int j = 0; j < MAX_CIV_TEAMS; j++)
				{
					if (GET_TEAM((TeamTypes)j).isAlive())
					{
						if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
						{
							setTradeItem(&item, TRADE_WAR, j);
							if (canTradeItem(eOtherPlayer, item))
							{
								ourList.insertAtEnd(item);
								bFoundItemUs = true;
							}
						}
					}
				}
			}
			break;
/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
		case TRADE_WAR_PREPARE:
			// lfgr 08/2023
			if( GC.getDefineINT( "NO_WAR_TRADE", 0 ) ) {
				break;
			}
			if (!isHuman())
			{
				for (int j = 0; j < MAX_CIV_TEAMS; j++)
				{
					if (GET_TEAM((TeamTypes)j).isAlive())
					{
						if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
						{
							//setTradeItem(&item, TRADE_WAR, j); //byFra
							setTradeItem(&item, (TradeableItems)i, j);   //byFra
							if (canTradeItem(eOtherPlayer, item))
							{
								ourList.insertAtEnd(item);
								bFoundItemUs = true;
							}
						}
					}
				}
			}
			break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/
		case TRADE_EMBARGO:
			if (!isHuman())
			{
				for (int j = 0; j < MAX_CIV_TEAMS; j++)
				{
					if (GET_TEAM((TeamTypes)j).isAlive())
					{
						if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
						{
							setTradeItem(&item, TRADE_EMBARGO, j);
							if (canTradeItem(eOtherPlayer, item))
							{
								ourList.insertAtEnd(item);
								bFoundItemUs = true;
							}
						}
					}
				}
			}
			break;

		case TRADE_CIVIC:
			for (int j = 0; j < GC.getNumCivicInfos(); j++)
			{
				setTradeItem(&item, TRADE_CIVIC, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_RELIGION:
			for (int j = 0; j < GC.getNumReligionInfos(); j++)
			{
				setTradeItem(&item, TRADE_RELIGION, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;
/************************************************************************************************/
/* Afforess	                  Start		 06/16/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
        case TRADE_CORPORATION:
            for (int j = 0; j < GC.getNumCorporationInfos(); j++)
            {
                setTradeItem(&item, TRADE_CORPORATION, j);
                if (canTradeItem(eOtherPlayer, item))
                {
                    bFoundItemUs = true;
                    ourList.insertAtEnd(item);
                }
            }
            break;
		case TRADE_SECRETARY_GENERAL_VOTE:
			for (int j = 0; j < GC.getNumVoteSourceInfos(); j++)
			{
				setTradeItem(&item, TRADE_SECRETARY_GENERAL_VOTE, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;
			
		case TRADE_WORKER:
            for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
            {
                setTradeItem(&item, TRADE_WORKER, pLoopUnit->getID());
                if (canTradeItem(eOtherPlayer, item))
                {
                    bFoundItemUs = true;
                    ourList.insertAtEnd(item);
                }
            }
            break;

        case TRADE_MILITARY_UNIT:
            for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
            {
                setTradeItem(&item, TRADE_MILITARY_UNIT, pLoopUnit->getID());
                if (canTradeItem(eOtherPlayer, item))
                {
                    bFoundItemUs = true;
                    ourList.insertAtEnd(item);
                }
            }
            break;
        case TRADE_CONTACT:
            for (int j = 0; j < MAX_CIV_TEAMS; j++)
            {
                if (GET_TEAM((TeamTypes)j).isAlive())
                {
                    if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
                    {
                        setTradeItem(&item, TRADE_CONTACT, j);
                        if (canTradeItem(eOtherPlayer, item))
                        {
                            ourList.insertAtEnd(item);
                            bFoundItemUs = true;
                        }
                    }
                }
            }
            break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
		}
	}
}

bool CvPlayer::getHeadingTradeString(PlayerTypes eOtherPlayer, TradeableItems eItem, CvWString& szString, CvString& szIcon) const
{
	szIcon.clear();

	switch ( eItem )
	{
	case TRADE_TECHNOLOGIES:
		szString = gDLL->getText("TXT_KEY_CONCEPT_TECHNOLOGY");
		break;

	case TRADE_RESOURCES:
		szString = gDLL->getText("TXT_KEY_TRADE_RESOURCES");
		break;

	case TRADE_CITIES:
		szString = gDLL->getText("TXT_KEY_TRADE_CITIES");
		break;

/************************************************************************************************/
/* Afforess	                  Start		 07/29/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
    case TRADE_WORKER:
        szString = gDLL->getText("TXT_KEY_TRADE_WORKERS");
        break;

    case TRADE_MILITARY_UNIT:
        szString = gDLL->getText("TXT_KEY_TRADE_MILITARY_UNIT");
        break;
		
    case TRADE_CONTACT:
        szString = gDLL->getText("TXT_KEY_TRADE_MAKE_CONTACT_WITH");
        break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */	
/************************************************************************************************/

	case TRADE_PEACE:
		szString = gDLL->getText("TXT_KEY_TRADE_MAKE_PEACE_WITH");
		break;

	case TRADE_WAR:
		szString = gDLL->getText("TXT_KEY_TRADE_DECLARE_WAR_ON");
		break;

/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	// byFra
	case TRADE_WAR_PREPARE:
		szString = gDLL->getText("TXT_KEY_TRADE_PREPARE_WAR_ON");
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/

	case TRADE_EMBARGO:
		szString = gDLL->getText("TXT_KEY_TRADE_STOP_TRADING_WITH");
		break;

	case TRADE_CIVIC:
		szString = gDLL->getText("TXT_KEY_TRADE_ADOPT");
		break;

	case TRADE_RELIGION:
		szString = gDLL->getText("TXT_KEY_TRADE_CONVERT");
		break;

/************************************************************************************************/
/* Afforess	                  Start		 07/29/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
    case TRADE_CORPORATION:
        szString = gDLL->getText("TXT_KEY_TRADE_BUY_CORPORATION");
        break;
		
	case TRADE_SECRETARY_GENERAL_VOTE:
		szString = gDLL->getText("TXT_KEY_TRADE_SECRETARY_GENERAL_VOTE");
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */	
/************************************************************************************************/
	default:
		szString.clear();
		return false;
		break;
	}

	return true;
}


bool CvPlayer::getItemTradeString(PlayerTypes eOtherPlayer, bool bOffer, bool bShowingCurrent, const TradeData& zTradeData, CvWString& szString, CvString& szIcon) const
{
	szIcon.clear();

	switch (zTradeData.m_eItemType)
	{
	case TRADE_GOLD:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_NUM", zTradeData.m_iData);
		}
		else
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_NUM", AI_maxGoldTrade(eOtherPlayer));
		}
		break;
	case TRADE_GOLD_PER_TURN:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_PER_TURN_NUM", zTradeData.m_iData);
		}
		else
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_PER_TURN_NUM", AI_maxGoldPerTurnTrade(eOtherPlayer));
		}
		break;
	case TRADE_MAPS:
		szString = gDLL->getText("TXT_KEY_TRADE_WORLD_MAP_STRING");
		break;
	case TRADE_VASSAL:
		szString = gDLL->getText("TXT_KEY_TRADE_VASSAL_STRING");
		break;
	case TRADE_SURRENDER:
		szString = gDLL->getText("TXT_KEY_TRADE_CAPITULATE_STRING");
		break;
	case TRADE_OPEN_BORDERS:
		szString = gDLL->getText("TXT_KEY_TRADE_OPEN_BORDERS_STRING");
		break;
	case TRADE_DEFENSIVE_PACT:
		szString = gDLL->getText("TXT_KEY_TRADE_DEFENSIVE_PACT_STRING");
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       START                                                  			 */
/*************************************************************************************************/
	case TRADE_NON_AGGRESSION:
		szString = gDLL->getText("TXT_KEY_TRADE_NON_AGGRESSION_STRING");
		break;
	case TRADE_POW:
		szString = gDLL->getText("TXT_KEY_TRADE_POW_STRING");
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END	                                                  			 */
/*************************************************************************************************/
	case TRADE_PERMANENT_ALLIANCE:
		szString = gDLL->getText("TXT_KEY_TRADE_PERMANENT_ALLIANCE_STRING");
		break;
	case TRADE_PEACE_TREATY:
		szString = gDLL->getText("TXT_KEY_TRADE_PEACE_TREATY_STRING", GC.getDefineINT("PEACE_TREATY_LENGTH"));
		break;
	case TRADE_TECHNOLOGIES:
		szString = GC.getTechInfo((TechTypes)zTradeData.m_iData).getDescription();
		szIcon = GC.getTechInfo((TechTypes)zTradeData.m_iData).getButton();
		break;
	case TRADE_RESOURCES:
		if (bOffer)
		{
			int iNumResources = GET_PLAYER(eOtherPlayer).getNumTradeableBonuses((BonusTypes)zTradeData.m_iData);
			if (bShowingCurrent)
			{
				++iNumResources;
			}
			szString = gDLL->getText("TXT_KEY_TRADE_RESOURCE", GC.getBonusInfo((BonusTypes)zTradeData.m_iData).getDescription(), iNumResources);

		}
		else
		{
			szString.Format( L"%s (%d)", GC.getBonusInfo((BonusTypes)zTradeData.m_iData).getDescription(), getNumTradeableBonuses((BonusTypes)zTradeData.m_iData));
		}
		szIcon = GC.getBonusInfo((BonusTypes)zTradeData.m_iData).getButton();
		break;
	case TRADE_CITIES:
		{
			CvCity* pCity = NULL;
			if (bOffer)
			{
				pCity = GET_PLAYER(eOtherPlayer).getCity(zTradeData.m_iData);
			}
			else
			{
				pCity = getCity(zTradeData.m_iData);
			}
			if (NULL != pCity)
			{
				if (pCity->getLiberationPlayer(false) == eOtherPlayer)
				{
					szString.Format(L"%s (%s)", pCity->getName().GetCString(), gDLL->getText("TXT_KEY_LIBERATE_CITY").GetCString());
				}
				else
				{
					szString = gDLL->getText("TXT_KEY_CITY_OF", pCity->getNameKey());
				}
			}
		}
		break;
	case TRADE_PEACE:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_PEACE_WITH");
			szString += GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		else
		{
			szString = GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		break;
	case TRADE_WAR:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_WAR_WITH");
			szString += GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		else
		{
			szString = GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	// byFra
	case TRADE_WAR_PREPARE:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_PREPARE_WAR_WITH");
			szString += gDLL->getText(" ");
			szString += GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		else
		{
			szString = gDLL->getText(" ");
			szString = GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/
	case TRADE_EMBARGO:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_STOP_TRADING_WITH");
			szString += L" " + GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		else
		{
			szString = GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		break;
	case TRADE_CIVIC:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_ADOPT");
			szString += GC.getCivicInfo((CivicTypes)zTradeData.m_iData).getDescription();
		}
		else
		{
			szString = GC.getCivicInfo((CivicTypes)zTradeData.m_iData).getDescription();
		}
		szIcon = GC.getCivicInfo((CivicTypes)zTradeData.m_iData).getButton();
		break;
	case TRADE_RELIGION:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_CONVERT");
			szString += GC.getReligionInfo((ReligionTypes)zTradeData.m_iData).getDescription();
		}
		else
		{
			szString = GC.getReligionInfo((ReligionTypes)zTradeData.m_iData).getDescription();
		}
		szIcon = GC.getReligionInfo((ReligionTypes)zTradeData.m_iData).getButton();
		break;
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
    case TRADE_WORKER:
        {
            CvUnit* pUnit = NULL;
            if (bOffer)
            {
                pUnit = GET_PLAYER(eOtherPlayer).getUnit(zTradeData.m_iData);
            }
            else
            {
                pUnit = getUnit(zTradeData.m_iData);
            }
            if (pUnit != NULL)
            {
                szString.Format(L"%s", pUnit->getName().GetCString());
				szIcon = GC.getUnitInfo((UnitTypes)pUnit->getUnitType()).getButton();
            }
        }
        break;
    case TRADE_MILITARY_UNIT:
        {
            CvUnit* pUnit = NULL;
            if (bOffer)
            {
                pUnit = GET_PLAYER(eOtherPlayer).getUnit(zTradeData.m_iData);
            }
            else
            {
                pUnit = getUnit(zTradeData.m_iData);
            }
            if (pUnit != NULL)
            {
                CvWStringBuffer szTemp;
                //GAMETEXT.setUnitHelp(szTemp, pUnit, true);
                //szString = CvWString(szTemp.getCString());
				szString.Format(L"%s", pUnit->getName().GetCString());
				szIcon = GC.getUnitInfo((UnitTypes)pUnit->getUnitType()).getButton();
            }
        }
        break;
    case TRADE_CONTACT:
        if (bOffer)
        {
            szString = gDLL->getText("TXT_KEY_TRADE_CONTACT_WITH");
			szString += gDLL->getText(" ");
            szString += GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
        }
        else
        {
			szString = gDLL->getText(" ");
            szString += GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
        }
        break;
	case TRADE_CORPORATION:
        if (bOffer)
        {
            szString = gDLL->getText("TXT_KEY_TRADE_BUY");
			szString += gDLL->getText(" ");
            szString += GC.getCorporationInfo((CorporationTypes)zTradeData.m_iData).getDescription();
        }
        else
        {
			szString = gDLL->getText(" ");
            szString += GC.getCorporationInfo((CorporationTypes)zTradeData.m_iData).getDescription();
        }
        szIcon = GC.getCorporationInfo((CorporationTypes)zTradeData.m_iData).getButton();
        break;
	case TRADE_SECRETARY_GENERAL_VOTE:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_SEC_GEN_VOTE", GET_PLAYER(eOtherPlayer).getNameKey(), GC.getVoteSourceInfo((VoteSourceTypes)zTradeData.m_iData).getDescription());
		}
		else
		{
			szString = GC.getVoteSourceInfo((VoteSourceTypes)zTradeData.m_iData).getDescription();
		}
		break;
	case TRADE_RIGHT_OF_PASSAGE:
		szString = gDLL->getText("TXT_KEY_TRADE_LIMITED_BORDERS_STRING");
		break;
	case TRADE_FREE_TRADE_ZONE:
		szString = gDLL->getText("TXT_KEY_MISC_FREE_TRADE_ZONE");
		break;
	case TRADE_EMBASSY:
        szString = gDLL->getText("TXT_KEY_TRADE_EMBASSY_STRING");
        break;
	case TRADE_WAR_REPARATIONS:
		szString = gDLL->getText("TXT_KEY_TRADE_WAR_REPARATIONS_STRING");
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

	default:
		szString.clear();
		return false;
	}

	return true;
}

void CvPlayer::updateTradeList(PlayerTypes eOtherPlayer, CLinkList<TradeData>& ourInventory, const CLinkList<TradeData>& ourOffer, const CLinkList<TradeData>& theirOffer) const
{
	for (CLLNode<TradeData>* pNode = ourInventory.head(); pNode != NULL; pNode = ourInventory.next(pNode))
	{
		pNode->m_data.m_bHidden = false;

		// Don't show peace treaties when not at war
		if (!::atWar(getTeam(), GET_PLAYER(eOtherPlayer).getTeam()))
		{
			if (pNode->m_data.m_eItemType == TRADE_PEACE_TREATY || pNode->m_data.m_eItemType == TRADE_SURRENDER)
			{
				pNode->m_data.m_bHidden = true;
			}
		}
		// Afforess: Don't show war reparations when at war
		else
		{
			if (pNode->m_data.m_eItemType == TRADE_WAR_REPARATIONS)
			{
				pNode->m_data.m_bHidden = true;
			}
		}

		// Don't show technologies with no tech trading game option
		if (GC.getGame().isOption(GAMEOPTION_NO_TECH_TRADING) && pNode->m_data.m_eItemType == TRADE_TECHNOLOGIES)
		{
			pNode->m_data.m_bHidden = true;
		}
	}

	for (CLLNode<TradeData>* pNode = ourInventory.head(); pNode != NULL; pNode = ourInventory.next(pNode))
	{
		switch (pNode->m_data.m_eItemType)
		{
		case TRADE_PEACE_TREATY:
			for (CLLNode<TradeData>* pOfferNode = ourOffer.head(); pOfferNode != NULL; pOfferNode = ourOffer.next(pOfferNode))
			{
				// Don't show vassal deals if peace treaty is already on the table
				if (CvDeal::isVassal(pOfferNode->m_data.m_eItemType))
				{
					pNode->m_data.m_bHidden = true;
					break;
				}
			}
			break;
		case TRADE_VASSAL:
		case TRADE_SURRENDER:
			for (CLLNode<TradeData>* pOfferNode = theirOffer.head(); pOfferNode != NULL; pOfferNode = theirOffer.next(pOfferNode))
			{
				// Don't show vassal deals if another type of vassal deal is on the table
				if (CvDeal::isVassal(pOfferNode->m_data.m_eItemType))
				{
					pNode->m_data.m_bHidden = true;
					break;
				}
			}

			if (!pNode->m_data.m_bHidden)
			{
				for (CLLNode<TradeData>* pOfferNode = ourOffer.head(); pOfferNode != NULL; pOfferNode = ourOffer.next(pOfferNode))
				{
					// Don't show peace deals if the other player is offering to be a vassal
					if (CvDeal::isEndWar(pOfferNode->m_data.m_eItemType))
					{
						pNode->m_data.m_bHidden = true;
						break;
					}
				}
			}
			break;
		default:
			break;
		}
	}
	/************************************************************************************************/
	/* Afforess	                  Start		5/29/11                                                 */
	/*                                                                                              */
	/* Allow city trades for other items                                                            */
	/************************************************************************************************/
	/*if (!isHuman() || !GET_PLAYER(eOtherPlayer).isHuman())  // everything allowed in human-human trades
	{
		CLLNode<TradeData>* pFirstOffer = ourOffer.head();
		if (pFirstOffer == NULL)
		{
			pFirstOffer = theirOffer.head();
		}

		if (pFirstOffer != NULL)
		{
			if (!CvDeal::isEndWar(pFirstOffer->m_data.m_eItemType) || !::atWar(getTeam(), GET_PLAYER(eOtherPlayer).getTeam()))
			{
				for (CLLNode<TradeData>* pNode = ourInventory.head(); pNode != NULL; pNode = ourInventory.next(pNode))
				{
					if (pFirstOffer->m_data.m_eItemType == TRADE_CITIES || pNode->m_data.m_eItemType == TRADE_CITIES)
					{
						pNode->m_data.m_bHidden = true;
					}
					else if (CvDeal::isAnnual(pFirstOffer->m_data.m_eItemType) != CvDeal::isAnnual(pNode->m_data.m_eItemType))
					{
						pNode->m_data.m_bHidden = true;
					}
				}
			}
		}
	}*/
	/************************************************************************************************/
	/* Afforess	                     END                                                            */
	/************************************************************************************************/
}

int CvPlayer::getIntroMusicScriptId(PlayerTypes eForPlayer) const
{
	CvPlayer& kForPlayer = GET_PLAYER(eForPlayer);
	EraTypes eEra = kForPlayer.getCurrentEra();
	CvLeaderHeadInfo& kLeader = GC.getLeaderHeadInfo(getLeaderType());
	if (GET_TEAM(kForPlayer.getTeam()).isAtWar(getTeam()))
	{
		return kLeader.getDiploWarIntroMusicScriptIds(eEra);
	}
	else
	{
		return kLeader.getDiploPeaceIntroMusicScriptIds(eEra);
	}
}

int CvPlayer::getMusicScriptId(PlayerTypes eForPlayer) const
{
	CvPlayer& kForPlayer = GET_PLAYER(eForPlayer);
	EraTypes eEra = kForPlayer.getCurrentEra();
	CvLeaderHeadInfo& kLeader = GC.getLeaderHeadInfo(getLeaderType());
	if (GET_TEAM(kForPlayer.getTeam()).isAtWar(getTeam()))
	{
		return kLeader.getDiploWarMusicScriptIds(eEra);
	}
	else
	{
		return kLeader.getDiploPeaceMusicScriptIds(eEra);
	}
}


void CvPlayer::getGlobeLayerColors(GlobeLayerTypes eGlobeLayerType, int iOption, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	switch (eGlobeLayerType)
	{
	case GLOBE_LAYER_TRADE:
		getTradeLayerColors(aColors, aIndicators);
		break;
	case GLOBE_LAYER_UNIT:
		getUnitLayerColors((GlobeLayerUnitOptionTypes) iOption, aColors, aIndicators);
		break;
	case GLOBE_LAYER_RESOURCE:
		getResourceLayerColors((GlobeLayerResourceOptionTypes) iOption, aColors, aIndicators);
		break;
	case GLOBE_LAYER_RELIGION:
		// Hide Council of Esus in the Religion globe layer START
		// getReligionLayerColors((ReligionTypes) iOption, aColors, aIndicators);
		{
			int realNumber = 0;
			int optionNumber = 0;
			while (realNumber < GC.getNumReligionInfos())
			{
                if (canSeeReligion((ReligionTypes) realNumber, NULL))
				{
					if (optionNumber == iOption) {
						break;
					}
					optionNumber++;
				}
				realNumber++;
			}
			getReligionLayerColors((ReligionTypes) realNumber, aColors, aIndicators);
		}
		// Hide Council of Esus in the Religion globe layer END
		break;
	case GLOBE_LAYER_CULTURE:
		getCultureLayerColors(aColors, aIndicators);
		break;
	default:
		FAssertMsg(false, "Unknown globe layer type");
		break;
	}
}

void CvPlayer::getTradeLayerColors(std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.resize(GC.getMapINLINE().numPlotsINLINE(), NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	typedef std::map< int, std::vector<int> > PlotGroupMap;
	PlotGroupMap mapPlotGroups;
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); ++iI)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		CvPlotGroup* pPlotGroup = pLoopPlot->getPlotGroup(getID());
		if (pPlotGroup != NULL && pLoopPlot->isRevealed(getTeam(), true) && pLoopPlot->getTeam() == getTeam())
		{
			mapPlotGroups[pPlotGroup->getID()].push_back(iI);
		}
	}

	CvRandom kRandom;
	kRandom.init(42);
	for (PlotGroupMap::iterator it = mapPlotGroups.begin(); it != mapPlotGroups.end(); ++it)
	{
		NiColorA kColor(kRandom.getFloat(), kRandom.getFloat(), kRandom.getFloat(), 0.8f);
		std::vector<int>& aPlots = it->second;
		for (size_t i = 0; i < aPlots.size(); ++i)
		{
			aColors[aPlots[i]] = kColor;
		}
	}
}

void CvPlayer::getUnitLayerColors(GlobeLayerUnitOptionTypes eOption, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.resize(GC.getMapINLINE().numPlotsINLINE(), NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	std::vector< std::vector<float> > aafPlayerPlotStrength(MAX_PLAYERS);
	for (int i = 0; i < MAX_PLAYERS; i++)
	{
		if (GET_PLAYER((PlayerTypes)i).isAlive())
		{
			aafPlayerPlotStrength[i].resize(GC.getMapINLINE().numPlotsINLINE());
		}
	}

	float fMaxPlotStrength = 0.0f;

	// create unit plot indicators...
	// build the trade group texture
	typedef std::map<int, NiColor> GroupMap;
	GroupMap mapColors;

	// Loop through all the players
	CvWStringBuffer szBuffer;
	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
	{
		if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
		{
			for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); ++iI)
			{
				CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
				int iNumUnits = pLoopPlot->getNumUnits();
				float fPlotStrength = 0.0f;

				if (iNumUnits > 0 && pLoopPlot->isVisible(getTeam(), true))
				{
					bool bShowIndicator = false;

					CLLNode<IDInfo>* pUnitNode = pLoopPlot->headUnitNode();
					while (pUnitNode != NULL)
					{
						CvUnit* pUnit = ::getUnit(pUnitNode->m_data);
						pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);

						if (pUnit->getVisualOwner() == iPlayer && !pUnit->isInvisible(getTeam(), GC.getGameINLINE().isDebugMode()))
						{
							// now, is this unit of interest?
							bool bIsMilitary = pUnit->baseCombatStr() > 0;
							bool bIsEnemy = pUnit->isEnemy(getTeam());
							bool bIsOnOurTeam = pUnit->getTeam() == getTeam();
							bool bOfInterest = false;

							switch (eOption)
							{
							case SHOW_ALL_MILITARY:
								{
									bOfInterest = bIsMilitary;
									if (bOfInterest)
									{
										fPlotStrength += ((float) pUnit->currHitPoints() / (float) pUnit->maxHitPoints() * (float) pUnit->baseCombatStr());
									}
									break;
								}
							case SHOW_TEAM_MILITARY:
								{
									bOfInterest = bIsMilitary && bIsOnOurTeam;
									if (bOfInterest)
										fPlotStrength += ((float) pUnit->currHitPoints() / (float) pUnit->maxHitPoints() * (float) pUnit->baseCombatStr());
									break;
								}
							case SHOW_ENEMIES:
								{
									bOfInterest = bIsMilitary && bIsEnemy;
									if (bOfInterest)
										fPlotStrength += ((float) pUnit->currHitPoints() / (float) pUnit->maxHitPoints() * (float) pUnit->baseCombatStr());
									break;
								}

							case SHOW_ENEMIES_IN_TERRITORY:
								{
									bOfInterest = bIsMilitary;
									break;
								}

							case SHOW_PLAYER_DOMESTICS:
								{
									bOfInterest = !bIsMilitary;// && (pUnit->getVisualOwner() == eCurPlayer);
									break;
								}
							default:
								bOfInterest = false;
								break;
							}

							// create the indicator
							if (bOfInterest)
							{
								bShowIndicator = true;
							}

							fMaxPlotStrength = std::max(fPlotStrength, fMaxPlotStrength);
							aafPlayerPlotStrength[iPlayer][iI] = fPlotStrength;
						}
					}

					if (bShowIndicator)
					{
						CvUnit* pUnit = pLoopPlot->getBestDefender(NO_PLAYER);
						if (pUnit != NULL)
						{
							PlayerColorTypes eUnitColor = GET_PLAYER(pUnit->getVisualOwner()).getPlayerColor();
							const NiColorA& kColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(eUnitColor).getColorTypePrimary()).getColor();

							szBuffer.clear();
							GAMETEXT.setPlotListHelp(szBuffer, pLoopPlot, true, true);

							CvPlotIndicatorData kIndicator;
							kIndicator.m_pUnit = pUnit;
							kIndicator.m_strLabel = "UNITS";
							kIndicator.m_strIcon = pUnit->getButton();

							if (eOption == SHOW_ENEMIES_IN_TERRITORY)
							{
								kIndicator.m_kColor.r = 1;
								kIndicator.m_kColor.g = 0;
								kIndicator.m_kColor.b = 0;
							}
							else
							{
								kIndicator.m_kColor.r = kColor.r;
								kIndicator.m_kColor.g = kColor.g;
								kIndicator.m_kColor.b = kColor.b;
							}
							kIndicator.m_strHelpText = szBuffer.getCString();

							//setup visibility
							switch (eOption)
							{
							case SHOW_ENEMIES_IN_TERRITORY:
								kIndicator.m_bTestEnemyVisibility = true;
								kIndicator.m_eVisibility = PLOT_INDICATOR_VISIBLE_ALWAYS;
								break;
							case SHOW_ENEMIES:
								kIndicator.m_eVisibility = PLOT_INDICATOR_VISIBLE_ALWAYS;
								break;
							default:
								kIndicator.m_eVisibility = PLOT_INDICATOR_VISIBLE_ONSCREEN_ONLY;
								break;
							}
							aIndicators.push_back(kIndicator);
						}
					}
				}
			}
		}
	}

	if (fMaxPlotStrength > 0)
	{
		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
		{
			if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
			{
				PlayerColorTypes eCurPlayerColor = GET_PLAYER((PlayerTypes) iPlayer).getPlayerColor();
				const NiColorA& kColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(eCurPlayerColor).getColorTypePrimary()).getColor();

				for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
				{
					CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
					if (pLoopPlot->isVisible(getTeam(), true))
					{
						float fPlotStrength = aafPlayerPlotStrength[iPlayer][iI];
						if (fPlotStrength > 0)
						{
							float fAlpha = (fPlotStrength / fMaxPlotStrength * 0.75f + 0.25f) * 0.8f;
							if (fAlpha > aColors[iI].a)
							{
								aColors[iI] = kColor;
								aColors[iI].a = fAlpha;
							}
						}
					}
				}
			}
		}
	}
}

void CvPlayer::getResourceLayerColors(GlobeLayerResourceOptionTypes eOption, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.clear();
	aIndicators.clear();

	PlayerColorTypes ePlayerColor = getPlayerColor();

	CvWStringBuffer szBuffer;
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		PlayerTypes eOwner = pLoopPlot->getRevealedOwner(getTeam(), true);

		if (pLoopPlot->isRevealed(getTeam(), true))
		{
			BonusTypes eCurType = pLoopPlot->getBonusType((GC.getGame().isDebugMode()) ? NO_TEAM : getTeam());
			if (eCurType != NO_BONUS)
			{
				CvBonusInfo& kBonusInfo = GC.getBonusInfo(eCurType);

				bool bOfInterest = false;
				switch (eOption)
				{
				case SHOW_ALL_RESOURCES:
					bOfInterest = true;
					break;
				case SHOW_STRATEGIC_RESOURCES:
					bOfInterest = (kBonusInfo.getHappiness() == 0) && (kBonusInfo.getHealth() == 0);
					break;
				case SHOW_HAPPY_RESOURCES:
					bOfInterest = (kBonusInfo.getHappiness() != 0 ) && (kBonusInfo.getHealth() == 0);
					break;
				case SHOW_HEALTH_RESOURCES:
					bOfInterest = (kBonusInfo.getHappiness() == 0) && (kBonusInfo.getHealth() != 0);
					break;

				}

				if (bOfInterest)
				{
					CvPlotIndicatorData kData;
					kData.m_strLabel = "RESOURCES";
					kData.m_eVisibility = PLOT_INDICATOR_VISIBLE_ONSCREEN_ONLY;
					kData.m_strIcon = GC.getBonusInfo(eCurType).getButton();

					int x = pLoopPlot->getX();
					int y = pLoopPlot->getY();
					kData.m_Target = NiPoint2(GC.getMapINLINE().plotXToPointX(x), GC.getMapINLINE().plotYToPointY(y));

					if (eOwner == NO_PLAYER)
					{
						kData.m_kColor.r = 0.8f;
						kData.m_kColor.g = 0.8f;
						kData.m_kColor.b = 0.8f;
					}
					else
					{
						PlayerColorTypes eCurPlayerColor = GET_PLAYER(eOwner).getPlayerColor();
						const NiColorA& kColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(eCurPlayerColor).getColorTypePrimary()).getColor();
						kData.m_kColor.r = kColor.r;
						kData.m_kColor.g = kColor.g;
						kData.m_kColor.b = kColor.b;
					}

					szBuffer.clear();
					GAMETEXT.setBonusHelp(szBuffer, eCurType, false);
					kData.m_strHelpText = szBuffer.getCString();

					aIndicators.push_back(kData);
				}
			}
		}
	}
}

void CvPlayer::getReligionLayerColors(ReligionTypes eSelectedReligion, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.resize(GC.getMapINLINE().numPlotsINLINE(), NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	CvRandom kRandom;
	kRandom.init(42 * eSelectedReligion);
	const NiColorA kBaseColor(kRandom.getFloat(), kRandom.getFloat(), kRandom.getFloat(), 1.0f);

	for (int iI = 0; iI  < MAX_PLAYERS; iI ++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			int iLoop;
			for (CvCity* pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
			{
				if (pLoopCity->isRevealed(getTeam(), true))
				{
					if (pLoopCity->isHasReligion(eSelectedReligion))
					{
						float fAlpha = 0.8f;
						if (!pLoopCity->isHolyCity(eSelectedReligion))
						{
							fAlpha *= 0.5f;
						}

						// loop through the city's plots
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//						for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
						for (int iJ = 0; iJ < ::calculateNumCityPlots(getNextCityRadius()); iJ++)
//<<<<Unofficial Bug Fix: End Modify
						{
							CvPlot* pLoopPlot = plotCity(pLoopCity->getX(), pLoopCity->getY(), iJ);
							if (pLoopPlot != NULL)
							{
								// visibility query
								if (pLoopPlot->isRevealed(getTeam(), true))
								{
									int iIndex = GC.getMapINLINE().plotNumINLINE(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());
									if (fAlpha > aColors[iIndex].a)
									{
										aColors[iIndex] = kBaseColor;
										aColors[iIndex].a = fAlpha;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

void CvPlayer::getCultureLayerColors(std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	const int iColorsPerPlot = 4;
	aColors.resize(GC.getMapINLINE().numPlotsINLINE() * iColorsPerPlot, NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	// find maximum total culture
	int iMaxTotalCulture = INT_MIN;
	int iMinTotalCulture = INT_MAX;
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		int iTotalCulture = pLoopPlot->countTotalCulture();
		if (iTotalCulture > iMaxTotalCulture)
		{
			iMaxTotalCulture = iTotalCulture;
		}
		if (iTotalCulture < iMinTotalCulture && iTotalCulture > 0)
		{
			iMinTotalCulture = iTotalCulture;
		}
	}
	iMinTotalCulture = 0;

	// find culture percentages
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		PlayerTypes eOwner = pLoopPlot->getRevealedOwner(getTeam(), true);

		// how many people own this plot?
		std::vector < std::pair<int,int> > plot_owners;
		//int iNumNonzeroOwners = 0;
		// K-Mod
		int iTotalCulture = pLoopPlot->countTotalCulture();
		if (iTotalCulture == 0)
			continue;
		// K-Mod end
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
		{
			if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
			{
				int iCurCultureAmount = pLoopPlot->getCulture((PlayerTypes)iPlayer);
				//if (iCurCultureAmount != 0)
				if (iCurCultureAmount * 100 / iTotalCulture >= 20) // K-Mod (to reduce visual spam from small amounts of culture)
				{
					//iNumNonzeroOwners ++;
					plot_owners.push_back(std::pair<int,int>(iCurCultureAmount, iPlayer));
				}
			}
		}

		// ensure that it is revealed
		if (!plot_owners.empty() && pLoopPlot->getRevealedOwner(getTeam(), true) != NO_PLAYER)
		{
			for (int i = 0; i < iColorsPerPlot; ++i)
			{
				int iCurOwnerIdx = i % plot_owners.size();
				PlayerTypes eCurOwnerID = (PlayerTypes) plot_owners[iCurOwnerIdx].second;
				int iCurCulture = plot_owners[iCurOwnerIdx].first;
				const NiColorA& kCurColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(GET_PLAYER(eCurOwnerID).getPlayerColor()).getColorTypePrimary()).getColor();

				// damp the color by the value...
				aColors[iI * iColorsPerPlot + i] = kCurColor;
				float blend_factor = 0.5f * std::min(1.0f, std::max(0.0f, (float)(iCurCulture - iMinTotalCulture) / iMaxTotalCulture));
				aColors[iI * iColorsPerPlot + i].a = std::min(0.8f * blend_factor + 0.5f, 1.0f);
			}
		}
	}
}

void CvPlayer::cheat(bool bCtrl, bool bAlt, bool bShift)
{
	if (gDLL->getChtLvl() > 0)
	{
		GET_TEAM(getTeam()).setHasTech(getCurrentResearch(), true, getID(), true, false);
	}
}

const CvArtInfoUnit* CvPlayer::getUnitArtInfo(UnitTypes eUnit, int iMeshGroup) const
{
	CivilizationTypes eCivilization = getCivilizationType();

	if (eCivilization == NO_CIVILIZATION)
	{
		eCivilization = (CivilizationTypes) GC.getDefineINT("BARBARIAN_CIVILIZATION");
	}
	UnitArtStyleTypes eStyle = (UnitArtStyleTypes) GC.getCivilizationInfo(eCivilization).getUnitArtStyleType();
	EraTypes eEra = getCurrentRealEra();
	if (eEra == NO_ERA)
	{
		eEra = (EraTypes) 0;
	}
	return GC.getUnitInfo(eUnit).getArtInfo(iMeshGroup, eEra, eStyle);
}

bool CvPlayer::hasSpaceshipArrived() const
{
	VictoryTypes eSpaceVictory = GC.getGameINLINE().getSpaceVictory();
	if (eSpaceVictory != NO_VICTORY)
	{
		int iVictoryCountdown = GET_TEAM(getTeam()).getVictoryCountdown(eSpaceVictory);
		if (((GC.getGameINLINE().getGameState() == GAMESTATE_EXTENDED) && (iVictoryCountdown > 0)) || (iVictoryCountdown == 0))
		{
			return true;
		}
	}

	return false;
}

//FfH Traits: Added by Kael 08/02/2007
bool CvPlayer::canSeeCivic(int iCivic) const
{
    if (GC.getCivicInfo((CivicTypes)iCivic).isHidden())
    {
        if (getCivics((CivicOptionTypes)GC.getCivicInfo((CivicTypes)iCivic).getCivicOptionType()) == iCivic)
        {
            return true;
        }
        return false;
    }
    return true;
}

bool CvPlayer::canSeeReligion(int iReligion, CvCity* pCity) const
{
    if (GC.getReligionInfo((ReligionTypes)iReligion).isHidden())
    {
        if (getStateReligion() == iReligion)
        {
            return true;
        }
        if (pCity != NULL)
        {
            if (pCity->getOwner() == getID())
            {
                return true;
            }
        }
        return false;
    }
    return true;
}

bool CvPlayer::isAdaptive() const
{
    return m_bAdaptive;
}

void CvPlayer::setAdaptive(bool bNewValue)
{
	m_bAdaptive = bNewValue;
}

bool CvPlayer::isAgnostic() const
{
    return m_bAgnostic;
}

void CvPlayer::setAgnostic(bool bNewValue)
{
	m_bAgnostic = bNewValue;
}

bool CvPlayer::isAssimilation() const
{
    return m_bAssimilation;
}

void CvPlayer::setAssimilation(bool bNewValue)
{
	m_bAssimilation = bNewValue;
}

bool CvPlayer::isDeclaringWar() const
{
    return m_bDeclaringWar;
}

void CvPlayer::setDeclaringWar(bool bNewValue)
{
	m_bDeclaringWar = bNewValue;
}

bool CvPlayer::isHideUnits() const
{
    return m_bHideUnits;
}

void CvPlayer::setHideUnits(bool bNewValue)
{
	m_bHideUnits = bNewValue;
}

bool CvPlayer::isIgnoreFood() const
{
    return m_bIgnoreFood;
}

void CvPlayer::setIgnoreFood(bool bNewValue)
{
	m_bIgnoreFood = bNewValue;
}

bool CvPlayer::isInsane() const
{
    return m_bInsane;
}

void CvPlayer::setInsane(bool bNewValue)
{
	m_bInsane = bNewValue;
}

bool CvPlayer::isNoDiplomacyWithEnemies() const
{
    if (m_iNoDiplomacyWithEnemies == 0)
    {
        return false;
    }
    return true;
}

void CvPlayer::changeNoDiplomacyWithEnemies(int iChange)
{
    if (iChange != 0)
    {
        m_iNoDiplomacyWithEnemies += iChange;
    }
}

bool CvPlayer::isSeeInvisible() const
{
    return m_bSeeInvisible;
}

void CvPlayer::setSeeInvisible(bool bNewValue)
{
	m_bSeeInvisible = bNewValue;
}

bool CvPlayer::isSprawling() const
{
    return m_bSprawling;
}

void CvPlayer::setSprawling(bool bNewValue)
{
	m_bSprawling = bNewValue;
}

bool CvPlayer::isHasTech(int iTech) const
{
    return GET_TEAM(getTeam()).isHasTech((TechTypes)iTech);
}

AlignmentTypes CvPlayer::getAlignment() const // lfgr 02/2021: int -> AlignmentTypes
{
    return m_eAlignment;
}

void CvPlayer::setAlignment(AlignmentTypes eNewValue) // lfgr 02/2021: int -> AlignmentTypes
{
    m_eAlignment = eNewValue;
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
}

int CvPlayer::getDisableProduction() const
{
    return m_iDisableProduction;
}

void CvPlayer::changeDisableProduction(int iChange)
{
	if (iChange != 0)
	{
		m_iDisableProduction = (m_iDisableProduction + iChange);
	}
}

int CvPlayer::getDisableResearch() const
{
    return m_iDisableResearch;
}

void CvPlayer::changeDisableResearch(int iChange)
{
	if (iChange != 0)
	{
		m_iDisableResearch += iChange;
	}
}

int CvPlayer::getDisableSpellcasting() const
{
    return m_iDisableSpellcasting;
}

void CvPlayer::changeDisableSpellcasting(int iChange)
{
	if (iChange != 0)
	{
		m_iDisableSpellcasting = (m_iDisableSpellcasting + iChange);
	}
}

int CvPlayer::getEnslavementChance() const
{
    return m_iEnslavementChance;
}

void CvPlayer::changeEnslavementChance(int iChange)
{
	if (iChange != 0)
	{
		m_iEnslavementChance = (m_iEnslavementChance + iChange);
	}
}

int CvPlayer::getFreeXPFromCombat() const
{
    return m_iFreeXPFromCombat;
}

void CvPlayer::changeFreeXPFromCombat(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeXPFromCombat = (m_iFreeXPFromCombat + iChange);
	}
}

int CvPlayer::getNumBuilding(int iBuilding) const
{
   	CvCity* pLoopCity;
	int iLoop;
	int iCount = 0;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iCount += pLoopCity->getNumRealBuilding((BuildingTypes)iBuilding);
	}
	return iCount;
}

int CvPlayer::getMaxCities() const
{
    return m_iMaxCities;
}

void CvPlayer::setMaxCities(int iNewValue)
{
    m_iMaxCities = iNewValue;
}

int CvPlayer::getNumSettlements() const
{
	CvCity* pLoopCity;
	int iCount = 0;
	int iLoop;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
	    if (pLoopCity->isSettlement())
	    {
	        iCount += 1;
	    }
	}
	return iCount;
}

int CvPlayer::getPillagingGold() const
{
    return m_iPillagingGold;
}

void CvPlayer::changePillagingGold(int iChange)
{
	if (iChange != 0)
	{
		m_iPillagingGold += iChange;
	}
}

int CvPlayer::getPlayersKilled() const
{
    return m_iPlayersKilled;
}

void CvPlayer::changePlayersKilled(int iChange)
{
	if (iChange != 0)
	{
		m_iPlayersKilled += iChange;
	}
}

int CvPlayer::getRealPlayer() const
{
    return m_iRealPlayer;
}

void CvPlayer::setRealPlayer(int iNewValue)
{
    m_iRealPlayer = iNewValue;
}

int CvPlayer::getResistEnemyModify() const
{
    return m_iResistEnemyModify;
}

void CvPlayer::changeResistEnemyModify(int iChange)
{
	if (iChange != 0)
	{
		m_iResistEnemyModify += iChange;
	}
}

int CvPlayer::getResistModify() const
{
    return m_iResistModify;
}

void CvPlayer::changeResistModify(int iChange)
{
	if (iChange != 0)
	{
		m_iResistModify += iChange;
	}
}

int CvPlayer::getSanctuaryTimer() const
{
    return m_iSanctuaryTimer;
}

void CvPlayer::changeSanctuaryTimer(int iChange)
{
    if (iChange > 0)
    {
        gDLL->getEngineIFace()->AddGreatWall(getCapitalCity());
    }
	if (iChange != 0)
	{
		m_iSanctuaryTimer += iChange;
	}
	if (m_iSanctuaryTimer == 0)
	{
        gDLL->getEngineIFace()->RemoveGreatWall(getCapitalCity());
	}
}

int CvPlayer::getTempPlayerTimer() const
{
    return m_iTempPlayerTimer;
}

void CvPlayer::changeTempPlayerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iTempPlayerTimer = (m_iTempPlayerTimer + iChange);
	}
}

int CvPlayer::getStartingGold() const
{
    return m_iStartingGold;
}

void CvPlayer::changeStartingGold(int iChange)
{
	if (iChange != 0)
	{
		m_iStartingGold = (m_iStartingGold + iChange);
	}
}

int CvPlayer::getSummonDuration() const
{
    return m_iSummonDuration;
}

void CvPlayer::changeSummonDuration(int iChange)
{
	if (iChange != 0)
	{
		m_iSummonDuration = (m_iSummonDuration + iChange);
	}
}

int CvPlayer::getUpgradeCostModifier() const
{
    return m_iUpgradeCostModifier;
}

void CvPlayer::changeUpgradeCostModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iUpgradeCostModifier = (m_iUpgradeCostModifier + iChange);
	}
}

int CvPlayer::getDiscoverRandModifier() const
{
    return m_iDiscoverRandModifier;
}

void CvPlayer::changeDiscoverRandModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iDiscoverRandModifier = (m_iDiscoverRandModifier + iChange);
	}
}

int CvPlayer::getHealChange() const
{
    return m_iHealChange;
}

void CvPlayer::changeHealChange(int iChange)
{
	if (iChange != 0)
	{
		m_iHealChange = (m_iHealChange + iChange);
	}
}

int CvPlayer::getHealChangeEnemy() const
{
    return m_iHealChangeEnemy;
}

void CvPlayer::changeHealChangeEnemy(int iChange)
{
	if (iChange != 0)
	{
		m_iHealChangeEnemy = (m_iHealChangeEnemy + iChange);
	}
}

void CvPlayer::changeSpecialistTypeExtraCommerce(SpecialistTypes eIndex1, CommerceTypes eIndex2, int iChange)
{
	if (iChange != 0)
	{
		m_ppaaiSpecialistTypeExtraCommerce[eIndex1][eIndex2] = (m_ppaaiSpecialistTypeExtraCommerce[eIndex1][eIndex2] + iChange);
		updateCommerce();
		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getSpecialistTypeExtraCommerce(SpecialistTypes eIndex1, CommerceTypes eIndex2) const
{
	return m_ppaaiSpecialistTypeExtraCommerce[eIndex1][eIndex2];
}

void CvPlayer::setGreatPeopleCreated(int iNewValue)
{
	m_iGreatPeopleCreated = iNewValue;
}

void CvPlayer::setGreatPeopleThresholdModifier(int iNewValue)
{
	m_iGreatPeopleThresholdModifier = iNewValue;
}
//FfH: End Add

// MNAI - Puppet States
bool CvPlayer::isPuppetState() const
{
	return m_bPuppetState;
}

void CvPlayer::setPuppetState(bool newvalue)
{
    m_bPuppetState = newvalue;
}
// MNAI - End Puppet States

/*************************************************************************************************/
/** Sephi AI (Lanun Pirate Coves) (merged from Skyre Mod)                                       **/
/** Rewritten by Kael 09/19/2009                                                                **/
/*************************************************************************************************/
bool CvPlayer::isPirate() const
{
    SpellTypes ePirateCoveSpell = (SpellTypes)GC.getDefineINT("PIRATE_COVE_SPELL");

    if (ePirateCoveSpell != NO_SPELL)
    {
        CivilizationTypes ePirateCiv = (CivilizationTypes)GC.getSpellInfo(ePirateCoveSpell).getCivilizationPrereq();

        if (ePirateCiv == NO_CIVILIZATION || ePirateCiv == getCivilizationType())
        {
            return true;
        }
    }

    return false;
}

/*************************************************************************************************/
/**	Sephi AI (New Functions)                                 					        **/
/*************************************************************************************************/
ReligionTypes CvPlayer::getFavoriteReligion() const
{
	return (ReligionTypes)GC.getLeaderHeadInfo(getLeaderType()).getFavoriteReligion();
}

void CvPlayer::setFavoriteReligion(ReligionTypes newvalue)
{
    m_eFavoriteReligion=newvalue;
}

int CvPlayer::getArcaneTowerVictoryFlag() const
{
    return m_iTowerVicFlag;
}

void CvPlayer::setArcaneTowerVictoryFlag(int newflag)
{
    m_iTowerVicFlag=newflag;
}

bool CvPlayer::AI_isSummonSuicideMode()
{
    return m_bSumSuiMode;
}

void CvPlayer::AI_setSummonSuicideMode(bool newvalue)
{
    m_bSumSuiMode=newvalue;
}


int CvPlayer::countGroupFlagUnits(int Groupflag) const
{
    int countunits=0;
    int iLoop;

    for (CvUnit* pUnit = firstUnit(&iLoop); NULL != pUnit; pUnit = nextUnit(&iLoop))
    {
        if(pUnit)
        {
            if(pUnit->AI_getGroupflag()==Groupflag)
            {
                countunits++;
            }
        }
    }
    return countunits;
}


void CvPlayer::AI_doTowerMastery()
{

	{
		CyArgsList argsList;
		argsList.add(getID());	// pass in unit class
		argsList.add(getArcaneTowerVictoryFlag());	// pass in unit class
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "AI_TowerMastery", argsList.makeFunctionArgs(), &lResult);

		setArcaneTowerVictoryFlag(lResult);
	}
	return;
}
// End Sephi AI

//>>>>Unofficial Bug Fix: Added by Denev 2010/04/04
bool CvPlayer::isRegularCityMaxedOut() const
{
	if (getMaxCities() != -1)
	{
		if (getNumCities() - getNumSettlements() >= getMaxCities())
		{
			return true;
		}
	}

	return false;
}

int CvPlayer::getNextCityRadius() const
{
	int iNextCityRadius = CITY_PLOTS_DEFAULT_RADIUS;

	if (isSprawling())
	{
		iNextCityRadius++;
	}

	if (isRegularCityMaxedOut())
	{
		iNextCityRadius = 1;
	}

	return iNextCityRadius;
}

//>>>>Unofficial Bug Fix: Added by Denev 2009/09/29
//*** Assimilated city produces a unit with original civilization artstyle.
UnitArtStyleTypes CvPlayer::getUnitArtStyleType() const
{
	int iUnitArtStyle = NO_UNIT_ARTSTYLE;

	int iDefaultRace = GC.getCivilizationInfo(getCivilizationType()).getDefaultRace();
	if (iDefaultRace != NO_PROMOTION)
	{
		iUnitArtStyle = GC.getPromotionInfo((PromotionTypes)iDefaultRace).getUnitArtStyleType();
	}
	if (iUnitArtStyle == NO_UNIT_ARTSTYLE)
	{
		iUnitArtStyle = GC.getCivilizationInfo(getCivilizationType()).getUnitArtStyleType();
	}

	return (UnitArtStyleTypes)iUnitArtStyle;
}
//<<<<Unofficial Bug Fix: End Add

// BUG - Reminder Mod - start
#include "CvMessageControl.h"
void CvPlayer::addReminder(int iGameTurn, CvWString szMessage) const
{
	CvMessageControl::getInstance().sendAddReminder(getID(), iGameTurn, szMessage);
}
// BUG - Reminder Mod - end

int CvPlayer::getLeaderCategory() const
{
	return GC.getLeaderHeadInfo(getLeaderType()).getLeaderCategory();
}

/************************************************************************************************/
/* Afforess	                  Start		 07/29/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
bool CvPlayer::isTradingMilitaryBonus(PlayerTypes ePlayer) const
{
	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (GET_PLAYER(ePlayer).AI_militaryBonusVal((BonusTypes)iI) > 0)
		{
			if (getNumTradeImportsByBonus(ePlayer, ((BonusTypes)iI)) > 0)
			{
				return true;
			}
		}
	}
	return false;
}

int CvPlayer::getNumTradeImportsByBonus(PlayerTypes ePlayer, BonusTypes eBonus) const
{
	CLLNode<TradeData>* pNode;
	CvDeal* pLoopDeal;
	int iCount;
	int iLoop;

	FAssert(ePlayer != getID());
	iCount = 0;

	for(pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if ((pLoopDeal->getFirstPlayer() == getID()) && (pLoopDeal->getSecondPlayer() == ePlayer))
		{
			for (pNode = pLoopDeal->headSecondTradesNode(); (pNode != NULL); pNode = pLoopDeal->nextSecondTradesNode(pNode))
			{
				if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
				{
					if (pNode->m_data.m_iData == eBonus)
					{
						iCount++;
					}
				}
			}
		}

		if ((pLoopDeal->getFirstPlayer() == ePlayer) && (pLoopDeal->getSecondPlayer() == getID()))
		{
			for (pNode = pLoopDeal->headFirstTradesNode(); (pNode != NULL); pNode = pLoopDeal->nextFirstTradesNode(pNode))
			{
				if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
				{
					if (pNode->m_data.m_iData == eBonus)
					{
						iCount++;
					}
				}
			}
		}
	}

	return iCount;
}

CvCity* CvPlayer::getBestHQCity(CorporationTypes eCorporation) const
{
    CvCity* pCurrentHQ = GC.getGameINLINE().getHeadquarters(eCorporation);
	CvCity* pLoopCity;
	CvCity* pBestCity = NULL;
	int iValue;
	int iBestValue = 0;

	int iLoop;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
	    iValue = 0;
		//If we find no best city, the capital will do.
		if (pLoopCity->isCapital())
			pBestCity = pLoopCity;
	    if (!pLoopCity->isHasCorporation(eCorporation))
	    {
            if (pLoopCity->isConnectedTo(pCurrentHQ))
            {
                for (int iCorporation = 0; iCorporation < GC.getNumCorporationInfos(); ++iCorporation)
                {
                    if (pLoopCity->isHeadquarters((CorporationTypes)iCorporation))
                    {
                        if (GC.getGameINLINE().isCompetingCorporation((CorporationTypes)iCorporation, eCorporation))
                        {
                            continue;
                        }
                        iValue -= 25;
                    }
                }

                bool bFoundBonus = false;
                for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
                {
                    BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
                    if (NO_BONUS != eBonus)
                    {
                        if (pLoopCity->hasBonus(eBonus))
                        {
                            bFoundBonus = true;
                            iValue += 50;
                        }
                    }
                }

                if (!bFoundBonus)
                {
                    continue;
                }

                iValue += 100;
            }
	    }
	    else
	    {
	        iValue = 300;

	        if (pLoopCity->isConnectedTo(pCurrentHQ))
	        {
	            iValue += 100;
	        }

            for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
            {
                BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
                if (NO_BONUS != eBonus)
                {
                    if (pLoopCity->hasBonus(eBonus))
                    {
                        iValue += 50;
                    }
                }
            }

            for (int iCorporation = 0; iCorporation < GC.getNumCorporationInfos(); ++iCorporation)
            {
                if (pLoopCity->isHeadquarters((CorporationTypes)iCorporation))
                {
                    iValue -= 25;
                }
            }
	    }

	    if (iValue > iBestValue)
	    {
	        iBestValue = iValue;
	        pBestCity = pLoopCity;
	    }
	}

	return pBestCity;
}


TeamTypes CvPlayer::getPledgedSecretaryGeneralVote() const
{
	return (TeamTypes)m_eSecretaryGeneralVote;
}

void CvPlayer::setPledgedSecretaryGeneralVote(TeamTypes eIndex)
{
	m_eSecretaryGeneralVote = eIndex;
}

DenialTypes CvPlayer::AI_corporationTrade(CorporationTypes eCorporation, PlayerTypes ePlayer) const
{

	if (isNoCorporations())
	{
		return DENIAL_NO_GAIN;
	}
	
	CvCity* pLoopCity;
	int iLoop;
	bool bValid = false;
	bool bRequiresBonus = false;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		//If we don't have the corporation
		if (!(pLoopCity->isHasCorporation(eCorporation)))
		{
			for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
			{
				BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
				if (NO_BONUS != eBonus)
				{
					bRequiresBonus = true;
					//if the city can have the corporation
					if (pLoopCity->hasBonus(eBonus))
					{
						bValid = true;
					}
				}
			}
		}
	}
	
	if (!bValid && bRequiresBonus)
	{
		return DENIAL_NO_GAIN;
	}

	if (GET_PLAYER(ePlayer).getTeam() == getTeam())
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAtWar(getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(getTeam()).isVassal(GET_PLAYER(ePlayer).getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (isHuman())
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(getTeam()).AI_getWorstEnemy() == GET_PLAYER(ePlayer).getTeam())
	{
		return DENIAL_WORST_ENEMY;
	}

	if ((getHasCorporationCount(eCorporation) * 2) > getNumCities())
	{
		return DENIAL_NO_GAIN;
	}
	
	if (GET_PLAYER(ePlayer).isNoCorporations())
	{
		return DENIAL_NO_GAIN;
	}
	
	AttitudeTypes eAttitude = GET_PLAYER(getID()).AI_getAttitude(ePlayer);

	if (eAttitude <= GC.getLeaderHeadInfo(getPersonalityType()).getCorporationRefuseAttitudeThreshold())
	{
		return DENIAL_ATTITUDE;
	}
	
    return NO_DENIAL;
}

DenialTypes CvPlayer::AI_secretaryGeneralTrade(VoteSourceTypes eVoteSource, PlayerTypes ePlayer) const
{

	if (GET_PLAYER(ePlayer).getTeam() == getTeam())
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(getTeam()).isVassal(GET_PLAYER(ePlayer).getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAtWar(getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(getTeam()).AI_getWorstEnemy() == GET_PLAYER(ePlayer).getTeam())
	{
		return DENIAL_WORST_ENEMY;
	}

	if (GC.getGameINLINE().isTeamVoteEligible(getTeam(), eVoteSource))
	{
		return DENIAL_JOKING;
	}

	AttitudeTypes eAttitude = GET_PLAYER(getID()).AI_getAttitude(ePlayer);

	if (eAttitude <= GC.getLeaderHeadInfo(getPersonalityType()).getSecretaryGeneralVoteRefuseAttitudeThreshold())
	{
		return DENIAL_ATTITUDE;
	}

	return NO_DENIAL;
}

DenialTypes CvPlayer::AI_workerTrade(CvUnit* pUnit, PlayerTypes ePlayer) const
{

	if (isHuman())
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAtWar(getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(getTeam()).isVassal(GET_PLAYER(ePlayer).getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (GET_PLAYER(ePlayer).getTeam() == getTeam())
	{
		return NO_DENIAL;
	}
	
	if (GET_PLAYER(pUnit->getOriginalOwner()).getID() == GET_PLAYER(ePlayer).getID())
	{
		return DENIAL_JOKING;
	}
	
	if (GET_TEAM(getTeam()).AI_getWorstEnemy() == GET_PLAYER(ePlayer).getTeam())
	{
		return DENIAL_WORST_ENEMY;
	}

	if (GET_TEAM(getTeam()).AI_isSneakAttackPreparing(GET_PLAYER(ePlayer).getTeam()))
	{
		return DENIAL_NO_GAIN;
	}

	if (GET_PLAYER(ePlayer).AI_totalUnitAIs(UNITAI_WORKER) > GET_PLAYER(ePlayer).getNumCities())
	{
		if (GET_PLAYER(ePlayer).calculateUnitCost() > 0)
		{
			return DENIAL_NO_GAIN;
		}
	}

	AttitudeTypes eAttitude = AI_getAttitude(ePlayer);

	if (eAttitude <= GC.getLeaderHeadInfo(getPersonalityType()).getWorkerRefuseAttitudeThreshold())
	{
		return DENIAL_ATTITUDE;
	}

	return NO_DENIAL;
}

DenialTypes CvPlayer::AI_militaryUnitTrade(CvUnit* pUnit, PlayerTypes ePlayer) const
{
	
	if (isHuman())
	{
		return NO_DENIAL;
	}

	if (GET_PLAYER(ePlayer).getTeam() == getTeam())
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(getTeam()).isVassal(GET_PLAYER(ePlayer).getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAtWar(getTeam()))
	{
		return NO_DENIAL;
	}
	
	if (GET_TEAM(getTeam()).AI_isSneakAttackPreparing(GET_PLAYER(ePlayer).getTeam()))
	{
		return DENIAL_NO_GAIN;
	}

	if (GET_PLAYER(pUnit->getOriginalOwner()).getID() == GET_PLAYER(ePlayer).getID())
	{
		return DENIAL_JOKING;
	}
	
	if (GET_TEAM(getTeam()).getAnyWarPlanCount(true) > 0 && !GET_TEAM(getTeam()).AI_shareWar(GET_PLAYER(ePlayer).getTeam()))
	{
		return DENIAL_NO_GAIN;
	}

	if (GET_PLAYER(ePlayer).AI_isFinancialTrouble() && (GET_PLAYER(ePlayer).calculateUnitCost() > 0))
	{
		if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getAtWarCount(true) == 0)
		{
			return DENIAL_NO_GAIN;
		}
	}

	AttitudeTypes eAttitude = GET_PLAYER(getID()).AI_getAttitude(ePlayer);

	if (pUnit->nukeRange() > 0 && GET_PLAYER(ePlayer).getNumNukeUnits() == 0)
	{
		return DENIAL_JOKING;
	}

	if (eAttitude <= GC.getLeaderHeadInfo(getPersonalityType()).getMilitaryUnitRefuseAttitudeThreshold())
	{
		return DENIAL_ATTITUDE;
	}

	return NO_DENIAL;
}

bool CvPlayer::canTradeWarReparations(PlayerTypes ePlayer) const
{
	return AI_getMemoryCount(ePlayer, MEMORY_DECLARED_WAR) > 0 || AI_getMemoryCount(ePlayer, MEMORY_HIRED_WAR_ALLY) > 0 ||
		AI_getMemoryCount(ePlayer, MEMORY_NUKED_US) > 0 || AI_getMemoryCount(ePlayer, MEMORY_RAZED_CITY) > 0 ||
		AI_getMemoryCount(ePlayer, MEMORY_RAZED_HOLY_CITY) > 0 || AI_getMemoryCount(ePlayer, MEMORY_BACKSTAB) > 0;
}

DenialTypes CvPlayer::AI_tradeWarReparations(PlayerTypes ePlayer) const
{
	if (isHuman())
	{
		return NO_DENIAL;
	}

	return DENIAL_JOKING;
}

// Advanced Diplomacy - added by MNAI

bool CvPlayer::isCultureNeedsEmptyRadius() const
{
   	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
	    if (isFullMember((VoteSourceTypes)iI))
	    {
	        if (GC.getGameINLINE().isCultureNeedsEmptyRadius((VoteSourceTypes)iI))
	        {
	            return true;
	        }
	    }
	}
    return false;
}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

/*************************************************************************************************/
/**	CivCounter			               		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
int CvPlayer::getCivCounter() const
{
	return m_iCivCounter;
}

void CvPlayer::changeCivCounter(int iChange)
{
	m_iCivCounter = (m_iCivCounter + iChange);
}

void CvPlayer::setCivCounter(int iNewValue)
{
	m_iCivCounter = iNewValue;
}

int CvPlayer::getCivCounterMod() const
{
	return m_iCivCounterMod;
}

void CvPlayer::changeCivCounterMod(int iChange)
{
	m_iCivCounterMod = (m_iCivCounterMod + iChange);
}

void CvPlayer::setCivCounterMod(int iNewValue)
{
	m_iCivCounterMod = iNewValue;
}
/*************************************************************************************************/
/**	CivCounter								END													**/
/*************************************************************************************************/

// MNAI - new functions

int CvPlayer::countNumOwnedTerrainTypes(TerrainTypes eTerrain) const
{
	PROFILE("CvPlayer::countNumOwnedTerrainTypes");

	CvPlot* pLoopPlot;
	int iCount = 0;

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->getOwnerINLINE() == getID())
		{
			if (pLoopPlot->getTerrainType() == eTerrain)
			{
				iCount++;
			}
		}
	}

	return iCount;
}

int CvPlayer::countNumOwnedHills() const
{
	PROFILE("CvPlayer::countNumOwnedHills");

	CvPlot* pLoopPlot;
	int iCount = 0;

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->getOwnerINLINE() == getID())
		{
			if (pLoopPlot->isHills())
			{
				iCount++;
			}
		}
	}

	return iCount;
}

int CvPlayer::countNumOwnedRiverSide() const
{
	PROFILE("CvPlayer::countNumOwnedRiverSide");

	CvPlot* pLoopPlot;
	int iCount = 0;

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->getOwnerINLINE() == getID())
		{
			if (pLoopPlot->isRiverSide())
			{
				iCount++;
			}
		}
	}

	return iCount;
}

int CvPlayer::countNumAvailablePlotsForImprovement(ImprovementTypes eImprovement) const
{
	PROFILE("CvPlayer::countNumAvailablePlotsForImprovement");

	CvPlot* pLoopPlot;
	int iCount = 0;

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->getOwnerINLINE() == getID())
		{
			if (pLoopPlot->canHaveImprovement(eImprovement, getID()))
			{
				iCount++;
			}
		}
	}

	return iCount;
}

int CvPlayer::getHighestUnitTier(bool bIncludeHeroes, bool bIncludeLimitedUnits) const
{
	CvUnit* pLoopUnit;
	int iLoop;
	int iHighestTier = 0;

	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		CvUnitInfo& kLoopUnit = GC.getUnitInfo(pLoopUnit->getUnitType());
		
		if (!(pLoopUnit->getDuration() > 0)) // dont count temporary units
		{
			if (!isWorldUnitClass(pLoopUnit->getUnitClassType()) || bIncludeHeroes) // dont count heroes unless the flag is set
			{
				if (!isLimitedUnitClass(pLoopUnit->getUnitClassType()) || bIncludeLimitedUnits)// dont count limited units unless the flag is set
				{
					if (kLoopUnit.getTier() > iHighestTier)
					{
						iHighestTier = kLoopUnit.getTier();
					}
				}
			}
		}
	}

	return iHighestTier;
}

// End MNAI

// Automatic OOS detection START
int CvPlayer::getNumTriggersFired() const
{
	return m_triggersFired.size();
}
// Automatic OOS detection END

/************************************************************************************************/
/* GP_NAMES                                 07/2013                                 lfgr        */
/* From CvUnit::init() (modified)                                                               */
/************************************************************************************************/
int CvPlayer::getNewGreatPersonBornName( UnitTypes eUnitType )
{
	CvUnitInfo& kUnitInfo = GC.getUnitInfo( eUnitType );

	int iBestScore = 0;
	std::vector<int> veBestNames;

	for( int eUnitName = 0; eUnitName < kUnitInfo.getNumUnitNames(); eUnitName++ )
	{
		CvWString szName = gDLL->getText( kUnitInfo.getUnitNames( eUnitName ) );
		if( GC.getGameINLINE().isGreatPersonBorn( szName ) )
			continue;

		int eLeader = kUnitInfo.getUnitNameLeader( eUnitName );
		if( eLeader != NO_LEADER )
		{
			bool bLeaderFound = false;
			for( int ePlayer = 0; ePlayer < MAX_PLAYERS; ePlayer++ )
			{
				if( GET_PLAYER( (PlayerTypes) ePlayer ).isAlive()
						&& GET_PLAYER( (PlayerTypes) ePlayer ).getLeaderType() == eLeader )
				{
					bLeaderFound = true;
					break;
				}
			}
			if( bLeaderFound )
				continue;
		}

		int iScore = 0;

		if( kUnitInfo.getUnitNamePreferredCiv( eUnitName ) == getCivilizationType() )
			iScore += 4;
		else
		{
			if( kUnitInfo.getUnitNamePreferredCiv( eUnitName ) == NO_CIVILIZATION )
				iScore += 1;
			if( kUnitInfo.getUnitNameRace( eUnitName ) == GC.getCivilizationInfo( getCivilizationType() ).getDefaultRace() )
				iScore += 1;
		}
		

		if( kUnitInfo.getUnitNameReligion( eUnitName ) != NO_RELIGION )
		{
			if( kUnitInfo.getUnitNameReligion( eUnitName ) == getStateReligion() )
				iScore += 3;
		}
		else // if( kUnitInfo.getUnitNameReligion( eUnitName ) == NO_RELIGION )
			iScore += 1;

		logBBAI( "Score for %S: %d", szName.c_str(), iScore );

		if( iScore > iBestScore )
		{
			iBestScore = iScore;
			veBestNames.clear();
			veBestNames.push_back( eUnitName );
		}
		else if( iScore == iBestScore )
			veBestNames.push_back( eUnitName );
	}

	if( veBestNames.empty() )
		return -1;

	int iRand = GC.getGameINLINE().getSorenRandNum( veBestNames.size(), "great person name" );
	int eBestUnitName = veBestNames[iRand];

	GC.getGameINLINE().addGreatPersonBornName( gDLL->getText( kUnitInfo.getUnitNames( eBestUnitName ) ) );

	return eBestUnitName;
}
/************************************************************************************************/
/* GP_NAMES                                END                                                  */
/************************************************************************************************/
