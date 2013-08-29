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
/************************************************************************************************/
	python::class_<CvSpawnInfo, python::bases<CvInfoBase> >("CvSpawnInfo")
		.def("getUnitArtStyleType", &CvSpawnInfo::getUnitArtStyleType, "UnitArtStyleTypes ()")
		.def("getWeight", &CvSpawnInfo::getWeight, "int ()")
		.def("getProbability", &CvSpawnInfo::getProbability, "int ()")
		.def("getMinWilderness", &CvSpawnInfo::getMinWilderness, "int ()")
		.def("getMaxWilderness", &CvSpawnInfo::getMaxWilderness, "int ()")
		.def("getMinRandomPromotions", &CvSpawnInfo::getMinRandomPromotions, "int ()")
		.def("getMaxRandomPromotions", &CvSpawnInfo::getMaxRandomPromotions, "int ()")
		.def("getNumRandomIncludedSpawns", &CvSpawnInfo::getNumRandomIncludedSpawns, "int ()")
		.def("isNeverSpawn", &CvSpawnInfo::isNeverSpawn, "bool ()")
		.def("isExplorationResult", &CvSpawnInfo::isExplorationResult, "bool ()")
		.def("isExplorationNoPush", &CvSpawnInfo::isExplorationNoPush, "bool ()")
		.def("isAnimal", &CvSpawnInfo::isAnimal, "bool ()")
		.def("isWater", &CvSpawnInfo::isWater, "bool ()")
		.def("isNoRace", &CvSpawnInfo::isNoRace, "bool ()")
		.def("getNumSpawnUnits", &CvSpawnInfo::getNumSpawnUnits, "int ( UnitTypes eID )")
		.def("getTerrainWeights", &CvSpawnInfo::getTerrainWeights, "int ( TerrainTypes eID )")
		.def("getFeatureWeights", &CvSpawnInfo::getFeatureWeights, "int ( FeatureTypes eID )")
		.def("getUnitPromotions", &CvSpawnInfo::getUnitPromotions, "bool ( PromotionTypes eID )")
		.def("isIncludedSpawns", &CvSpawnInfo::isIncludedSpawns, "bool ( SpawnTypes eID )")
		.def("getPrereqTechs", &CvSpawnInfo::getPrereqTechs, "int ( TechTypes eID )")
		.def("getObsoleteTechs", &CvSpawnInfo::getObsoleteTechs, "int ( TechTypes eID )")
		;
/************************************************************************************************/
/* WILDERNESS                                                                     END           */
/************************************************************************************************/
}
