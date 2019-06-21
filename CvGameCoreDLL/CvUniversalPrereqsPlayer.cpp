/*
 * CvUniversalPrereqsPlayer.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"


#include "CvPlayer.h"

#include "CvUniversalPrereqs.h"


//---------------------------
// CvPlayerCivilizationPrereq
//---------------------------


/**
 * Requires the given player to be of the specified civilization.
 */
#define CvPlayerCivilizationPrereq CvInfoTypePropertyEqualPrereq<\
	CvPlayer, CivilizationTypes, &CvPlayer::getCivilizationType>

template<>
const std::string CvPlayerCivilizationPrereq::TAG = "CivilizationType";


//--------------------
// CvPlayerCivicPrereq
//--------------------

/**
 * Requires the given player to have the specified civic.
 */
#define CvPlayerCivicPrereq CvInfoTypeSetPropertyContainsPrereq<\
	CvPlayer, CivicTypes, &CvPlayer::isCivic>

template<>
const std::string CvPlayerCivicPrereq::TAG = "CivicType";



//-------------------
// CvPrereq<CvPlayer>
//-------------------

template<>
CvPrereq<CvPlayer>* CvPrereq<CvPlayer>::readPrereq( CvXMLLoadUtility* pXml )
{
	const std::string sTagName = getCurrentTagName( pXml->GetXML() );

	TRY_READ_RETURN_PREREQ( sTagName, CvAndPrereq<CvPlayer> )
	TRY_READ_RETURN_PREREQ( sTagName, CvOrPrereq<CvPlayer> )
	TRY_READ_RETURN_PREREQ( sTagName, CvNotPrereq<CvPlayer> )
	TRY_READ_RETURN_PREREQ( sTagName, CvPlayerCivilizationPrereq )
	TRY_READ_RETURN_PREREQ( sTagName, CvPlayerCivicPrereq )

	return NULL;
}
