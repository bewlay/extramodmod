#pragma once

#ifndef CyPlot_h
#define CyPlot_h

//#include "CvEnums.h"

//
// Python wrapper class for CvPlot
//
class CyArea;
class CvPlot;
class CyUnit;
class CyCity;
class CyPlot
{
public:
	DllExport CyPlot();
	DllExport CyPlot(CvPlot*);			// Call from C++
	CvPlot* getPlot() { return m_pPlot; }	// Call from C++
	void setPlot(CvPlot* p) { m_pPlot=p; }	// Call from C++
	bool isNone() { return (m_pPlot==NULL); }
	void erase();
	DllExport NiPoint3 getPoint();
	int getTeam();

	void nukeExplosion(int iRange, CyUnit* pNukeUnit);

	bool isConnectedTo(CyCity* pCity);
	bool isConnectedToCapital(int /*PlayerTypes*/ ePlayer);
	int getPlotGroupConnectedBonus(int /*PlayerTypes*/ ePlayer, int /*BonusTypes*/ eBonus);
	bool isPlotGroupConnectedBonus(int /*PlayerTypes*/ ePlayer, int /*BonusTypes*/ eBonus);
	bool isAdjacentPlotGroupConnectedBonus(int /*PlayerTypes*/ ePlayer, int /*BonusTypes*/ eBonus);

	void updateVisibility();
	bool isAdjacentToArea(CyArea* pArea);
	bool shareAdjacentArea(CyPlot* pPlot);
	bool isAdjacentToLand();
	bool isCoastalLand();

	bool isWithinTeamCityRadius(int /*TeamTypes*/ eTeam, int /*PlayerTypes*/ eIgnorePlayer);

	bool isLake();
	bool isFreshWater();
	bool isPotentialIrrigation();
	bool canHavePotentialIrrigation();
	bool isIrrigationAvailable(bool bIgnoreSelf);

	bool isRiverSide();
	bool isRiver();
	bool isRiverConnection(int /*DirectionTypes*/ eDirection);

	int getNearestLandArea();
	int seeFromLevel(int /*TeamTypes*/ eTeam);
	CyPlot* getNearestLandPlot();
	int seeThroughLevel();
	bool canHaveBonus(int /*BonusTypes*/ eBonus, bool bIgnoreLatitude);
//>>>>Unofficial Bug Fix: Modified by Denev 2010/05/04
//	bool canHaveImprovement(int /* ImprovementTypes */ eImprovement, int /*TeamTypes*/ eTeam, bool bPotential);
	bool canHaveImprovement(int /* ImprovementTypes */ eImprovement, int /*PlayerTypes*/ ePlayer, bool bPotential);
//<<<<Unofficial Bug Fix: End Modify
	bool canBuild(int /*BuildTypes*/ eBuild, int /*PlayerTypes*/ ePlayer, bool bTestVisible);
	int getBuildTime(int /*BuildTypes*/ eBuild);
	int getBuildTurnsLeft(int /*BuildTypes*/ eBuild, int iNowExtra, int iThenExtra);
	int getFeatureProduction(int /*BuildTypes*/ eBuild, int /*TeamTypes*/ eTeam, CyCity* ppCity);

	CyUnit* getBestDefender(int /*PlayerTypes*/ eOwner, int /*PlayerTypes*/ eAttackingPlayer, CyUnit* pAttacker, bool bTestAtWar, bool bTestPotentialEnemy, bool bTestCanMove);
	CyUnit* getSelectedUnit();
	int getUnitPower(int /* PlayerTypes */ eOwner);

	int defenseModifier(int /*TeamTypes*/ iDefendTeam, bool bIgnoreBuilding, bool bHelp);
	int movementCost(CyUnit* pUnit, CyPlot* pFromPlot);

	int getExtraMovePathCost();
	void changeExtraMovePathCost(int iChange);

	bool isAdjacentOwned();
	bool isAdjacentPlayer(int /*PlayerTypes*/ ePlayer, bool bLandOnly);
	bool isAdjacentTeam(int /*TeamTypes*/ eTeam, bool bLandOnly);
	bool isWithinCultureRange(int /*PlayerTypes*/ ePlayer);
	int getNumCultureRangeCities(int /*PlayerTypes*/ ePlayer);
	int /*PlayerTypes*/ calculateCulturalOwner();

	bool isOwned();
	bool isBarbarian();
	bool isRevealedBarbarian();
	bool isVisible(int /*TeamTypes*/ eTeam, bool bDebug);
	bool isActiveVisible(bool bDebug);
	bool isVisibleToWatchingHuman();
	bool isAdjacentVisible(int /*TeamTypes*/ eTeam, bool bDebug);
	bool isAdjacentNonvisible(int /*TeamTypes*/ eTeam);
	bool isAdjacentRevealed(int /*TeamTypes*/ eTeam);
	bool isAdjacentNonrevealed(int /*TeamTypes*/ eTeam);

	void removeGoody();
	bool isGoody();
	bool isRevealedGoody(int /*TeamTypes*/ eTeam);

	bool isCity();
	bool isFriendlyCity(CyUnit* pUnit, bool bCheckImprovement);
	bool isEnemyCity(CyUnit* pUnit);
	bool isOccupation();
	bool isBeingWorked();

	bool isUnit();
	bool isInvestigate(int /*TeamTypes*/ eTeam);
	bool isVisibleEnemyDefender(CyUnit* pUnit);
	int getNumDefenders(int /*PlayerTypes*/ ePlayer);
	int getNumVisibleEnemyDefenders(CyUnit* pUnit);
	int getNumVisiblePotentialEnemyDefenders(CyUnit* pUnit);
	bool isVisibleEnemyUnit(int /*PlayerTypes*/ ePlayer);
	bool isVisibleOtherUnit(int /*PlayerTypes*/ ePlayer);
	bool isFighting();

	bool canHaveFeature(int /*FeatureTypes*/ eFeature);
	bool isRoute();
	bool isNetworkTerrain(int /*TeamTypes*/ eTeam);
	bool isBonusNetwork(int /*TeamTypes*/ eTeam);

	bool isTradeNetworkImpassable(int /*TeamTypes*/ eTeam);
	bool isTradeNetwork(int /*TeamTypes*/ eTeam);
	bool isTradeNetworkConnected(CyPlot* pPlot, int /*TeamTypes*/ eTeam);
	bool isValidDomainForLocation(CyUnit* pUnit) const;
	bool isValidDomainForAction(CyUnit* pUnit) const;
	bool isImpassable();

	int getX();
	int getY();
	bool at(int iX, int iY);
	int getLatitude();
	CyArea* area();
	CyArea* waterArea();
	int getArea();
	int getFeatureVariety();

	int getOwnershipDuration();
	bool isOwnershipScore();
	void setOwnershipDuration(int iNewValue);
	void changeOwnershipDuration(int iChange);

	int getImprovementDuration();
	void setImprovementDuration(int iNewValue);
	void changeImprovementDuration(int iChange);

	int getUpgradeProgress();
	int getUpgradeTimeLeft(int /*ImprovementTypes*/ eImprovement, int /*PlayerTypes*/ ePlayer);

	void setUpgradeProgress(int iNewValue);
	void changeUpgradeProgress(int iChange);

	int getForceUnownedTimer();
	bool isForceUnowned();
	void setForceUnownedTimer(int iNewValue);
	void changeForceUnownedTimer(int iChange);

	int getCityRadiusCount();
	int isCityRadius();

	bool isStartingPlot();
	void setStartingPlot(bool bNewValue);
	bool isNOfRiver();
	void setNOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);
	bool isWOfRiver();
	void setWOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);
	CardinalDirectionTypes getRiverWEDirection();
	CardinalDirectionTypes getRiverNSDirection();
	bool isIrrigated();

	bool isPotentialCityWork();
	bool isPotentialCityWorkForArea(CyArea* pArea);

	bool isFlagDirty();
	void setFlagDirty(bool bNewValue);

	int /*PlayerTypes*/ getOwner();
	void setOwner(int /*PlayerTypes*/ eNewValue);
	void setOwnerNoUnitCheck(int /*PlayerTypes*/ eNewValue);
	PlotTypes getPlotType();
	bool isWater();
	bool isFlatlands();
	bool isHills();
	bool isPeak();

	void setPlotType(PlotTypes eNewValue, bool bRecalculate, bool bRebuildGraphics);
	int /*TerrainTypes*/ getTerrainType();
	void setTerrainType(int /*TerrainTypes*/ eNewValue, bool bRecalculate, bool bRebuildGraphics, bool bTemp = false);
	int /*FeatureTypes*/ getFeatureType();
	void setFeatureType(int /*FeatureTypes*/ eNewValue, int iVariety);
	void setFeatureDummyVisibility(std::string dummyTag, bool show);
	void addFeatureDummyModel(std::string dummyTag, std::string modelTag);
	void setFeatureDummyTexture(std::string dummyTag, std::string textureTag);
	std::string pickFeatureDummyTag(int mouseX, int mouseY);
	void resetFeatureModel();
	int /* BonusTypes */ getBonusType(int /*TeamTypes*/ eTeam);
	int /* BonusTypes */ getNonObsoleteBonusType(int /*TeamTypes*/ eTeam);
	void setBonusType(int /* BonusTypes */ eNewValue);
	int /* ImprovementTypes */ getImprovementType();
	void setImprovementType(int /* ImprovementTypes */ eNewValue);
	int /* RouteTypes */ getRouteType();
	void setRouteType(int /*RouteTypes*/ eNewValue);

	CyCity* getPlotCity();
	CyCity* getWorkingCity();
	CyCity* getWorkingCityOverride();
	int getRiverID() const;
	void setRiverID(int iNewValue);
	int getMinOriginalStartDist();
	int getReconCount();
	int getRiverCrossingCount();
	int getYield(YieldTypes eIndex);
//>>>>Unofficial Bug Fix: Modified by Denev 2010/05/04
/*
	int calculateNatureYield(YieldTypes eIndex, TeamTypes eTeam, bool bIgnoreFeature = false);
	int calculateBestNatureYield(YieldTypes eIndex, TeamTypes eTeam);
	int calculateTotalBestNatureYield(TeamTypes eTeam);
*/
	int calculateNatureYield(YieldTypes eIndex, PlayerTypes ePlayer, bool bIgnoreFeature = false);
	int calculateBestNatureYield(YieldTypes eIndex, PlayerTypes ePlayer);
	int calculateTotalBestNatureYield(PlayerTypes ePlayer);
//<<<<Unofficial Bug Fix: End Modify
	int calculateImprovementYieldChange(int /*ImprovementTypes*/ eImprovement, YieldTypes eYield, int /*PlayerTypes*/ ePlayer, bool bOptimal);
	int calculateYield(YieldTypes eIndex, bool bDisplay);
	bool hasYield();

	int getCulture(int /*PlayerTypes*/ eIndex);
	int countTotalCulture();
	int /*TeamTypes*/ findHighestCultureTeam();

	int calculateCulturePercent(int /*PlayerTypes*/ eIndex);
	int calculateTeamCulturePercent(int /*TeamTypes*/ eIndex);
	void setCulture(int /*PlayerTypes*/ eIndex, int iNewValue, bool bUpdate);
	void changeCulture(int /*PlayerTypes*/ eIndex, int iChange, bool bUpdate);

	int countNumAirUnits(int /*TeamTypes*/ ePlayer);

	int getFoundValue(int /*PlayerTypes*/ eIndex);
	bool isBestAdjacentFound(int /*PlayerTypes*/ eIndex);

	int getPlayerCityRadiusCount(int /*PlayerTypes*/ eIndex);
	bool isPlayerCityRadius(int /*PlayerTypes*/ eIndex);

	int getVisibilityCount(int /*TeamTypes*/ eTeam);
	void changeVisibilityCount(int /*TeamTypes*/ eTeam, int iChange, int /*InvisibleTypes*/ eSeeInvisible);

	int getStolenVisibilityCount(int /*TeamTypes*/ eTeam);

	int /*PlayerTypes*/ getRevealedOwner(int /*TeamTypes*/ eTeam, bool bDebug);
	int /*TeamTypes*/ getRevealedTeam(int /*TeamTypes*/ eTeam, bool bDebug);

	bool isRiverCrossing(DirectionTypes eIndex);

	bool isRevealed(int /*TeamTypes*/ eTeam, bool bDebug);
	void setRevealed(int /*TeamTypes*/ eTeam, bool bNewValue, bool bTerrainOnly, int /*TeamTypes*/ eFromTeam);
	int /* ImprovementTypes */ getRevealedImprovementType(int /*TeamTypes*/ eTeam, bool bDebug);
	int /* RouteTypes */ getRevealedRouteType(int /*TeamTypes*/ eTeam, bool bDebug);
	int getBuildProgress(int /*BuildTypes*/ eBuild);
	bool changeBuildProgress(int /*BuildTypes*/ eBuild, int iChange, int /*TeamTypes*/ eTeam);

	int getCultureRangeCities(int /*PlayerTypes*/ eOwnerIndex, int iRangeIndex);
	bool isCultureRangeCity(int /*PlayerTypes*/ eOwnerIndex, int iRangeIndex);

	int getInvisibleVisibilityCount(int /*TeamTypes*/ eTeam, int /*InvisibleTypes*/ eInvisible);
	bool isInvisibleVisible(int /*TeamTypes*/ eTeam, int /*InvisibleTypes*/ eInvisible);
	void changeInvisibleVisibilityCount(int /*TeamTypes*/ eTeam, int /*InvisibleTypes*/ eInvisible, int iChange);

	int getNumUnits();
	CyUnit* getUnit(int iIndex);

	std::string getScriptData() const;
	void setScriptData(std::string szNewValue);

	//FfH: Added by Kael 08/15/2007
    void changePlotCounter(int iChange) const;
    int getPlotCounter() const;
    int getPortalExitX() const;
    void setPortalExitX(int iNewValue);
    int getPortalExitY() const;
    void setPortalExitY(int iNewValue);
    bool isMoveDisabledAI() const;
	void setMoveDisabledAI(bool bNewValue);
    bool isMoveDisabledHuman() const;
	void setMoveDisabledHuman(bool bNewValue);
    bool isBuildDisabled() const;
	void setBuildDisabled(bool bNewValue);
    bool isFoundDisabled() const;
	void setFoundDisabled(bool bNewValue);
    bool isPythonActive() const;
	void setPythonActive(bool bNewValue);
	bool isAdjacentToWater() const;
	int getMinLevel() const;
	void setMinLevel(int iNewValue);
    int getNumAnimalUnits() const;
	bool isVisibleToCivTeam() const;
	//FfH: End Add

	// Super Forts begin *canal* *choke*
	int getCanalValue();
	void calculateCanalValue();
	int getChokeValue();
	void calculateChokeValue();
	// Super Forts end

	// Temporary Map Items (original code from FFH2 (Kael) and FlavorMod (Jean Elcard) - expanded on for MNAI)

	TerrainTypes getRealTerrainType() const;
	FeatureTypes getRealFeatureType() const;
	int getRealFeatureVariety() const;
	BonusTypes getRealBonusType() const;
	ImprovementTypes getRealImprovementType() const;
	RouteTypes getRealRouteType() const;

	void setRealTerrainType(int /*TerrainTypes*/ eTerrain);
	void setRealFeatureType(int /*FeatureTypes*/ eFeature);
	void setRealFeatureVariety(int iVariety);
	void setRealBonusType(int /*BonusTypes*/ eBonus);
	void setRealImprovementType(int /*RouteTypes*/ eImprovement);
	void setRealRouteType(int /*RouteTypes*/ eRoute);

	void setTempTerrainType(int /*TerrainTypes*/ eNewValue, int iTimer);
	void setTempFeatureType(int /*FeatureTypes*/ eFeature, int iVariety, int iTimer);
	void setTempBonusType(int /*BonusTypes*/ eBonus, int iTimer);
	void setTempImprovementType(int /*ImprovementTypes*/ eImprovement, int iTimer);
	void setTempRouteType(int /*RouteTypes*/ eRoute, int iTimer);

	int getTempTerrainTimer() const;
	int getTempFeatureTimer() const;
	int getTempBonusTimer() const;
	int getTempImprovementTimer() const;
	int getTempRouteTimer() const;

	void changeTempTerrainTimer(int iChange);
	void changeTempFeatureTimer(int iChange);
	void changeTempBonusTimer(int iChange);
	void changeTempImprovementTimer(int iChange);
	void changeTempRouteTimer(int iChange);

	bool isHasTempTerrain();
	bool isHasTempFeature();
	bool isHasTempBonus();
	bool isHasTempImprovement();
	bool isHasTempRoute();
	// End Temporary Map Items

/************************************************************************************************/
/* TERRAIN_FLAVOUR                        03/2013                                 lfgr          */
/************************************************************************************************/
	float calcTerrainFlavourWeight( /*TerrainFlavourTypes*/ int eTerrainFlavour, int iMaxPlotDistance );
/************************************************************************************************/
/* TERRAIN_FLAVOUR                                                                END           */
/************************************************************************************************/

/************************************************************************************************/
/* WILDERNESS                             08/2013                                 lfgr          */
/* ImprovementSpawnTypes, PlotWilderness, SpawnInfo                                             */
/************************************************************************************************/
	bool isLair( bool bIgnoreIsAnimal, bool bAnimal ) const;
	int getWilderness() const;
	int getLairDanger() const;

	int getSpawnValue( int /*SpawnTypes*/ eSpawnType, bool bDungeon ) const;
	void createSpawn( int /*SpawnTypes*/ eSpawnType, int /*UnitAITypes*/ eUnitAI );
/************************************************************************************************/
/* WILDERNESS                                                                     END           */
/************************************************************************************************/

private:
	CvPlot* m_pPlot;
};
#endif	// CyPlot_h

