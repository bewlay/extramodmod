#pragma once

// unitAI.h

#ifndef CIV4_UNIT_AI_H
#define CIV4_UNIT_AI_H

#include "CvUnit.h"

class CvCity;

class CvUnitAI : public CvUnit
{

public:

  CvUnitAI();
  virtual ~CvUnitAI();

    void AI_init(UnitAITypes eUnitAI);
	void AI_uninit();
	void AI_reset(UnitAITypes eUnitAI = NO_UNITAI);
	bool AI_update();
	//bool AI_follow();
	bool AI_follow(bool bFirst = true); // K-Mod
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      04/05/10                                jdog5000      */
/*                                                                                              */
/* Unit AI                                                                                      */
/************************************************************************************************/
	bool AI_load(UnitAITypes eUnitAI, MissionAITypes eMissionAI, UnitAITypes eTransportedUnitAI = NO_UNITAI, int iMinCargo = -1, int iMinCargoSpace = -1, int iMaxCargoSpace = -1, int iMaxCargoOurUnitAI = -1, int iFlags = 0, int iMaxPath = MAX_INT, int iMaxTransportPath = MAX_INT);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	void AI_upgrade();
	void AI_promote();
	int AI_groupFirstVal();
	int AI_groupSecondVal();
	int AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const;
	bool AI_bestCityBuild(CvCity* pCity, CvPlot** ppBestPlot = NULL, BuildTypes* peBestBuild = NULL, CvPlot* pIgnorePlot = NULL, CvUnit* pUnit = NULL);
	bool AI_isCityAIType() const;
	int AI_getBirthmark() const;
	int AI_getBirthmark2() const;
	int AI_getBirthmark3() const;
	int AI_getBarbLeadership() const;
	int AI_getBarbLeadership(int &iFollowers) const;
	bool AI_groupBarbLeader(int iMaxRange) const;
	void AI_setBirthmark(int iNewValue);
	void AI_setBirthmark2(int iNewValue);
	void AI_setBirthmark3(int iNewValue);
	UnitAITypes AI_getUnitAIType() const;
	void AI_setUnitAIType(UnitAITypes eNewValue);
	int AI_sacrificeValue(const CvPlot* pPlot) const;

// Sephi AI (New Functions Definition)
    bool AI_groupheal(int iDamagePercent = 0, int iMaxPath = MAX_INT);
    void AI_feastingmove();
    void AI_ConquestMove();
    void AI_PatrolMove();
    void AI_HiddenNationalityMove();

// WILDERNESS 02/2016 lfgr // WildernessAI
	bool AI_wantsToExplore( int iX, int iY ) const;
// WILDERNESS end
	bool AI_exploreLairSea(int iRange = 0); // added by Tholal
	bool AI_exploreLair(int iRange = 0); // added by Tholal
	bool AI_pickupEquipment(int iRange = 0); // added by Tholal
    void AI_InquisitionMove();
	void AI_SvartalfarKidnapMove();
	void AI_ShadeMove();

    int AI_getGroupflag() const;
    void AI_setGroupflag(int newflag);
    void AI_chooseGroupflag();

    bool isUnitAllowedPermDefense();

	// heroes
    void AI_heromove();
    bool AI_Govannonmove();
    bool AI_Lokimove();
    bool AI_Rantinemove();

	bool AI_mageMove();
	void AI_mageCast();
    void AI_terraformerMove();
    void AI_upgrademanaMove();
    bool isSummoner();
    void AI_SummonCast();
    bool isDirectDamageCaster();
    void AI_DirectDamageCast(int Threshold);
    bool isDeBuffer();
    void AI_DeBuffCast();
    bool isMovementCaster();
    void AI_MovementCast();
    bool isBuffer();
    void AI_BuffCast();
	bool isSuicideSummon();
    void setSuicideSummon(bool newvalue);
	bool isPermanentSummon();
    void setPermanentSummon(bool newvalue);
// End Sephi AI

//FfH Spell System: Modified by Kael 07/23/2007
	int AI_promotionValue(PromotionTypes ePromotion);
//FfH: End Add

	// Tholal AI
	bool isInquisitor();
    bool isChanneler();
    bool isDivine();
	bool isVampire();
	bool isIllusionary();
	int getChannelingLevel();

	void AI_lairGuardianMove();
	bool AI_seekLair(int iRange);
	bool AI_seekDefensiveGround(int iRange, bool bIncludeHealing);
	// End Tholal AI

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

protected:

	int m_iBirthmark;

	UnitAITypes m_eUnitAIType;

	int m_iAutomatedAbortTurn;

// Sephi AI(New Functions Definition)
    int m_iGroupflag;
	bool m_bSuicideSummon;
	bool m_bPermanentSummon;
    bool m_bAllowedPermDefense;
// End Sephi AI

	void AI_animalMove();
	void AI_settleMove();
	void AI_workerMove();
	void AI_barbAttackMove();
	void AI_attackMove();
	void AI_attackCityMove();
	void AI_attackCityLemmingMove();
	void AI_collateralMove();
	void AI_pillageMove();
	void AI_reserveMove();
	void AI_counterMove();
	void AI_paratrooperMove();
	void AI_cityDefenseMove();
	void AI_cityDefenseExtraMove();
	void AI_exploreMove();
	void AI_missionaryMove();
	void AI_prophetMove();
	void AI_artistMove();
	void AI_scientistMove();
	void AI_generalMove();
	void AI_merchantMove();
	void AI_engineerMove();
	void AI_spyMove();
	void AI_ICBMMove();
	void AI_workerSeaMove();
	void AI_barbAttackSeaMove();
	void AI_pirateSeaMove();
	void AI_attackSeaMove();
	void AI_reserveSeaMove();
	void AI_escortSeaMove();
	void AI_exploreSeaMove();
	void AI_assaultSeaMove();
	void AI_settlerSeaMove();
	void AI_missionarySeaMove();
	void AI_spySeaMove();
	void AI_carrierSeaMove();
	void AI_missileCarrierSeaMove();
	void AI_attackAirMove();
	void AI_defenseAirMove();
	void AI_carrierAirMove();
	void AI_missileAirMove();

	void AI_networkAutomated();
	void AI_cityAutomated();

//FfH Spell System: Modified by Kael 07/23/2007 (this function is moved public)
//	int AI_promotionValue(PromotionTypes ePromotion);
	void AI_summonAttackMove();
//FfH: End Add

/************************************************************************************************/
/* BETTER_BTS_AI_MOD  - Unit AI           04/01/10                                jdog5000      */
/************************************************************************************************/
/* original bts code
	bool AI_shadow(UnitAITypes eUnitAI, int iMax = -1, int iMaxRatio = -1, bool bWithCargoOnly = true);
*/
	bool AI_shadow(UnitAITypes eUnitAI, int iMax = -1, int iMaxRatio = -1, bool bWithCargoOnly = true, bool bOutsideCityOnly = false, int iMaxPath = MAX_INT);
	bool AI_group(UnitAITypes eUnitAI, int iMaxGroup = -1, int iMaxOwnUnitAI = -1, int iMinUnitAI = -1, bool bIgnoreFaster = false, bool bIgnoreOwnUnitType = false, bool bStackOfDoom = false, int iMaxPath = MAX_INT, bool bAllowRegrouping = false, bool bWithCargoOnly = false, bool bInCityOnly = false, MissionAITypes eIgnoreMissionAIType = NO_MISSIONAI);
	//bool AI_load(UnitAITypes eUnitAI, MissionAITypes eMissionAI, UnitAITypes eTransportedUnitAI = NO_UNITAI, int iMinCargo = -1, int iMinCargoSpace = -1, int iMaxCargoSpace = -1, int iMaxCargoOurUnitAI = -1, int iFlags = 0, int iMaxPath = MAX_INT, int iMaxTransportPath = MAX_INT);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	bool AI_guardCityBestDefender();
	bool AI_guardCityMinDefender(bool bSearch = true);
	bool AI_guardCity(bool bLeave = false, bool bSearch = false, int iMaxPath = MAX_INT);
	bool AI_guardCityAirlift();
	bool AI_guardBonus(int iMinValue = 0);
	int AI_getPlotDefendersNeeded(CvPlot* pPlot, int iExtra);
	bool AI_guardFort(bool bSearch = true);
	bool AI_guardFortMinDefender(bool bSearch = true); // Super Forts *AI_defense*
	bool AI_guardCitySite();
	bool AI_guardSpy(int iRandomPercent);
	bool AI_destroySpy();
	bool AI_sabotageSpy();
	bool AI_pickupTargetSpy();
	bool AI_chokeDefend();
	bool AI_heal(int iDamagePercent = 0, int iMaxPath = MAX_INT);
	bool AI_afterAttack();
	bool AI_goldenAge();
	bool AI_spreadReligion();
	bool AI_spreadCorporation();
	bool AI_spreadReligionAirlift();
	bool AI_spreadCorporationAirlift();
	bool AI_discover(bool bThisTurnOnly = false, bool bFirstResearchOnly = false);
	bool AI_lead(std::vector<UnitAITypes>& aeAIUnitTypes);
	bool AI_join(int iMaxCount = MAX_INT);
	bool AI_construct(int iMaxCount = MAX_INT, int iMaxSingleBuildingCount = MAX_INT, int iThreshold = 0); // iThreshold was 15
	bool AI_switchHurry();
	bool AI_hurry();
	bool AI_greatWork();
	bool AI_offensiveAirlift();
	bool AI_paradrop(int iRange);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/01/09                                jdog5000      */
/************************************************************************************************/
	bool AI_protect(int iOddsThreshold, int iMaxPathTurns = MAX_INT);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	bool AI_patrol();
	bool AI_defend();
	bool AI_safety();
	bool AI_hide();
	bool AI_goody(int iRange);
	bool AI_explore();
	bool AI_exploreRange(int iRange);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      03/29/10                                jdog5000      */
/* War tactics AI                                                                               */
/************************************************************************************************/
	CvCity* AI_pickTargetCity(int iFlags = 0, int iMaxPath = MAX_INT, bool bHuntBarbs = false);
	bool AI_goToTargetCity(int iFlags = 0, int iMaxPath = MAX_INT, CvCity* pTargetCity = NULL);
	bool AI_goToTargetBarbCity(int iMaxPath = 10);
	bool AI_pillageAroundCity(CvCity* pTargetCity, int iBonusValueThreshold = 0, int iMaxPathTurns = MAX_INT);
	bool AI_bombardCity();
	bool AI_cityAttack(int iRange, int iOddsThreshold, bool bFollow = false);
	bool AI_anyAttack(int iRange, int iOddsThreshold, int iMinStack = 0, bool bAllowCities = true, bool bFollow = false);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	bool AI_rangeAttack(int iRange);
	bool AI_leaveAttack(int iRange, int iThreshold, int iStrengthThreshold);
	bool AI_blockade();
	bool AI_pirateBlockade();
	bool AI_seaBombardRange(int iMaxRange);
	bool AI_pillage(int iBonusValueThreshold = 0);
	bool AI_pillageRange(int iRange, int iBonusValueThreshold = 0);
	bool AI_found();
	bool AI_foundRange(int iRange, bool bFollow = false);
	bool AI_assaultSeaTransport(bool bBarbarian = false);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/04/09                                jdog5000      */
/************************************************************************************************/
	bool AI_assaultSeaReinforce(bool bBarbarian = false);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	bool AI_settlerSeaTransport();
	bool AI_settlerSeaFerry();
	bool AI_specialSeaTransportMissionary();
	bool AI_specialSeaTransportSpy();
	bool AI_carrierSeaTransport();
	bool AI_connectPlot(CvPlot* pPlot, int iRange = 0);
	bool AI_improveCity(CvCity* pCity);
	bool AI_improveLocalPlot(int iRange, CvCity* pIgnoreCity);
	bool AI_nextCityToImprove(CvCity* pCity);
	bool AI_nextCityToImproveAirlift();
	bool AI_irrigateTerritory();
	bool AI_fortTerritory(bool bCanal, bool bAirbase);

	// FFH_AI 05/2020 lfgr: Added optional argument bInsideBordersOrCurrentPlot: Don't build outside borders,
	//   except on the plot we're standing on (super forts)
	bool AI_improveBonus(int iMinValue = 0, CvPlot** ppBestPlot = NULL, BuildTypes* peBestBuild = NULL,
			int* piBestValue = NULL, bool bInsideBordersOrCurrentPlot = false);
	bool AI_improvePlot(CvPlot* pPlot, BuildTypes eBuild);
	BuildTypes AI_betterPlotBuild(CvPlot* pPlot, BuildTypes eBuild);
	bool AI_connectBonus(bool bTestTrade = true);
	bool AI_connectCity();
	bool AI_routeCity();
	bool AI_routeTerritory(bool bImprovementOnly = false);
	bool AI_travelToUpgradeCity();
	bool AI_retreatToCity(bool bPrimary = false, bool bAirlift = false, int iMaxPath = MAX_INT);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/15/09                                jdog5000      */
/* Naval AI                                                                                     */
/************************************************************************************************/
	bool AI_pickup(UnitAITypes eUnitAI, bool bCountProduction = false, int iMaxPath = MAX_INT);
	bool AI_pickupStranded(UnitAITypes eUnitAI = NO_UNITAI, int iMaxPath = MAX_INT);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	bool AI_airOffensiveCity();
	bool AI_airDefensiveCity();
	bool AI_airCarrier();
	bool AI_missileLoad(UnitAITypes eTargetUnitAI, int iMaxOwnUnitAI = -1, bool bStealthOnly = false);
	bool AI_airStrike();
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						9/26/08				jdog5000	    */
/* 	Air AI																	    */
/********************************************************************************/
	int AI_airOffenseBaseValue( CvPlot* pPlot );
	bool AI_defensiveAirStrike();
	bool AI_defendBaseAirStrike();
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								    */
/********************************************************************************/
	bool AI_airBombPlots();
	bool AI_airBombDefenses();	
	bool AI_exploreAir();
	bool AI_nuke();
	bool AI_nukeRange(int iRange);
	bool AI_trade(int iValueThreshold);
	bool AI_infiltrate();
	bool AI_reconSpy(int iRange);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/20/09                                jdog5000      */
/* Espionage AI                                                                                 */
/************************************************************************************************/
	bool AI_revoltCitySpy();
	bool AI_bonusOffenseSpy(int iMaxPath);
	bool AI_cityOffenseSpy(int iRange, CvCity* pSkipCity = NULL);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	bool AI_espionageSpy();
	bool AI_moveToStagingCity();
	bool AI_seaRetreatFromCityDanger();
	bool AI_airRetreatFromCityDanger();
	bool AI_airAttackDamagedSkip();

	bool AI_followBombard();

	bool AI_potentialEnemy(TeamTypes eTeam, const CvPlot* pPlot = NULL);

	bool AI_defendPlot(CvPlot* pPlot);
	int AI_pillageValue(CvPlot* pPlot, int iBonusValueThreshold = 0);
	int AI_nukeValue(CvCity* pCity);
	bool AI_canPillage(CvPlot& kPlot) const;

	int AI_searchRange(int iRange);
	bool AI_plotValid(CvPlot* pPlot);

	int AI_finalOddsThreshold(CvPlot* pPlot, int iOddsThreshold);

	int AI_stackOfDoomExtra();

	bool AI_stackAttackCity(int iRange, int iPowerThreshold, bool bFollow = true);
	bool AI_moveIntoCity(int iRange);

	bool AI_groupMergeRange(UnitAITypes eUnitAI, int iRange, bool bBiggerOnly = true, bool bAllowRegrouping = false, bool bIgnoreFaster = false);

	bool AI_artistCultureVictoryMove();

	bool AI_poach();
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      03/31/10                              jdog5000        */
/* War tactics AI                                                                               */
/************************************************************************************************/
	bool AI_choke(int iRange = 1, bool bDefensive = false);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	bool AI_solveBlockageProblem(CvPlot* pDestPlot, bool bDeclareWar);

	int AI_calculatePlotWorkersNeeded(CvPlot* pPlot, BuildTypes eBuild);

	int AI_getEspionageTargetValue(CvPlot* pPlot, int iMaxPath);

	bool AI_canGroupWithAIType(UnitAITypes eUnitAI) const;
	bool AI_allowGroup(const CvUnit* pUnit, UnitAITypes eUnitAI) const;

// Sephi AI (Lanun Pirate Coves) merged from Skyre Mod
    bool AI_buildPirateCove();
// End Sephi AI

	// lfgr 04/2021
	// Whether this unit is for ready for further orders from an AI method
	bool AI_readyToMoveOrCast();

	// added so under cheat mode we can call protected functions for testing
	friend class CvGameTextMgr;

};

// lfgr 03/2021: Helper function, to ensure consistency
bool isCityAIType( UnitAITypes eUnitAI );

#endif
