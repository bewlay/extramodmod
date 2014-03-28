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
}
