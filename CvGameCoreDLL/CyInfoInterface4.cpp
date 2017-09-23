#include "CvGameCoreDLL.h"
#include "CvInfos.h"

//
// Python interface for info classes (formerly structs)
// These are simple enough to be exposed directly - no wrappers
//

// lfgr: added for Wilderness

void CyInfoPythonInterface4()
{
	OutputDebugString("Python Extension Module - CyInfoPythonInterface4\n");
	
/************************************************************************************************/
/* TERRAIN_FLAVOUR                        03/2013                                 lfgr          */
/************************************************************************************************/
	python::class_<CvTerrainFlavourInfo, python::bases<CvInfoBase> >("CvTerrainFlavourInfo")
		.def("getBaseWeight", &CvTerrainFlavourInfo::getBaseWeight, "int ()")
		.def("getIsolationPercentWeight", &CvTerrainFlavourInfo::getIsolationPercentWeight, "int ()")
		.def("getCoastalWeight", &CvTerrainFlavourInfo::getCoastalWeight, "int ()")
		
		.def("getPlotPercentWeight", &CvTerrainFlavourInfo::getPlotPercentWeight, "int (PlotTypes ePlot)")
		.def("getTerrainPercentWeight", &CvTerrainFlavourInfo::getTerrainPercentWeight, "int (TerrainTypes eTerrain)")
		.def("getFeaturePercentWeight", &CvTerrainFlavourInfo::getFeaturePercentWeight, "int (FeatureTypes eFeature)")
		.def("getImprovementCountWeight", &CvTerrainFlavourInfo::getImprovementCountWeight, "int (ImprovementTypes eImprovement)")
		.def("getBonusCountWeight", &CvTerrainFlavourInfo::getBonusCountWeight, "int (BonusTypes eBonus)")
		.def("getYieldOnPlotPercentWeight", &CvTerrainFlavourInfo::getYieldOnPlotPercentWeight, "int (YieldTypes eYield)")
		;
/************************************************************************************************/
/* TERRAIN_FLAVOUR                                                                END           */
/************************************************************************************************/
	
/************************************************************************************************/
/* WILDERNESS                             08/2013                                 lfgr          */
/* SpawnInfo                                                                                    */
/************************************************************************************************/
	python::class_<CvSpawnInfo, python::bases<CvInfoBase> >("CvSpawnInfo")
		.def("getCreateLair", &CvSpawnInfo::getCreateLair, "ImprovementTypes ()")
		.def("getTerrainFlavourType", &CvSpawnInfo::getTerrainFlavourType, "TerrainFlavourTypes ()")
		.def("getUnitArtStyleType", &CvSpawnInfo::getUnitArtStyleType, "UnitArtStyleTypes ()")
		.def("getWeight", &CvSpawnInfo::getWeight, "int ()")
		.def("getValidTerrainWeight", &CvSpawnInfo::getValidTerrainWeight, "int ()")
		.def("getPrereqGlobalCounter", &CvSpawnInfo::getPrereqGlobalCounter, "int ()")
		.def("getMinRandomPromotions", &CvSpawnInfo::getMinRandomPromotions, "int ()")
		.def("getMaxRandomPromotions", &CvSpawnInfo::getMaxRandomPromotions, "int ()")
		.def("isNeverSpawn", &CvSpawnInfo::isNeverSpawn, "bool ()")
		.def("isNoWildernessIgnoreSpawnPrereq", &CvSpawnInfo::isNoWildernessIgnoreSpawnPrereq, "bool ()")
		.def("isExplorationResult", &CvSpawnInfo::isExplorationResult, "bool ()")
		.def("isExplorationNoPush", &CvSpawnInfo::isExplorationNoPush, "bool ()")
		.def("isNoDefender", &CvSpawnInfo::isNoDefender, "bool ()")
		.def("isAnimal", &CvSpawnInfo::isAnimal, "bool ()")
		.def("isWater", &CvSpawnInfo::isWater, "bool ()")
		.def("isNoRace", &CvSpawnInfo::isNoRace, "bool ()")
		.def("getNumSpawnUnits", &CvSpawnInfo::getNumSpawnUnits, "int ( UnitTypes eID )")
		.def("getUnitPromotions", &CvSpawnInfo::getUnitPromotions, "bool ( PromotionTypes eID )")
		;
/************************************************************************************************/
/* WILDERNESS                                                                     END           */
/************************************************************************************************/
/********************************************************************************/
/* EXTRA_CIV_TRAITS                08/2013                              lfgr    */
/********************************************************************************/
	python::class_<CvUnitArtStyleTypeInfo, python::bases<CvInfoBase> >("CvUnitArtStyleTypeInfo")
		.def("getEarlyArtDefineTag", &CvUnitArtStyleTypeInfo::getEarlyArtDefineTag, "string (int iMesh, int iUnit)")
		.def("getMiddleArtDefineTag", &CvUnitArtStyleTypeInfo::getMiddleArtDefineTag, "string (int iMesh, int iUnit)")
		.def("getLateArtDefineTag", &CvUnitArtStyleTypeInfo::getLateArtDefineTag, "string (int iMesh, int iUnit)")
		;
/********************************************************************************/
/* EXTRA_CIV_TRAITS                                                     END     */
/********************************************************************************/
}
