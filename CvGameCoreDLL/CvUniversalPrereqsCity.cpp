/*
 * CvUniversalPrereqsCity.cpp
 *
 * UNIVERSAL_PREREQS 02/2021 lfgr
 */

 // Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"

#include "CvCity.h"

#include "CvUniversalPrereqs.h"
#include "CvUniversalPrereqsHelpers.h"

//--------------------------
// CvCityBuildingClassPrereq
//--------------------------

/**
 * Requires the given city to have a building of the specified class
 */
#define CvCityBuildingClassPrereq CvInfoTypeSetPropertyContainsPrereq<\
	CvCity, BuildingClassTypes, &CvCity::isHasBuildingClass>

template<>
const std::string CvCityBuildingClassPrereq::TAG = "HasBuildingClass";


//-------------------
// CvPrereq<CvCity>
//-------------------

template<>
CvPrereq<CvCity>* CvPrereq<CvCity>::readPrereq( CvXMLLoadUtility* pXml )
{
	const std::string sTagName = getCurrentTagName( pXml->GetXML() );

	TRY_READ_RETURN_PREREQ( sTagName, CvAndPrereq<CvCity> )
	TRY_READ_RETURN_PREREQ( sTagName, CvOrPrereq<CvCity> )
	TRY_READ_RETURN_PREREQ( sTagName, CvNotPrereq<CvCity> )
	TRY_READ_RETURN_PREREQ( sTagName, CvCityBuildingClassPrereq )

	return NULL;
}