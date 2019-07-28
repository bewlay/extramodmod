/*
 * CvUniversalPrereqsPlayer.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"


#include "CvPlayer.h"

#include "CvUniversalPrereqs.h"
#include "CvUniversalPrereqsHelpers.h"


//---------------------------
// CvPlayerCivilizationPrereq
//---------------------------


/**
 * Requires the given player to be of the specified civilization.
 */
#define CvPlayerCivilizationPrereq CvInfoTypePropertyEqualPrereq<\
	CvPlayer, CivilizationTypes, &CvPlayer::getCivilizationType>

template<>
const std::string CvPlayerCivilizationPrereq::TAG = "IsCivilization";


//--------------------
// CvPlayerCivicPrereq
//--------------------

/**
 * Requires the given player to have the specified civic.
 */
#define CvPlayerCivicPrereq CvInfoTypeSetPropertyContainsPrereq<\
	CvPlayer, CivicTypes, &CvPlayer::isCivic>

template<>
const std::string CvPlayerCivicPrereq::TAG = "HasCivic";


//--------------------
// CvPlayerTraitPrereq
//--------------------

/**
 * Requires the given player to have the specified trait.
 */
#define CvPlayerTraitPrereq CvInfoTypeSetPropertyContainsPrereq<\
	CvPlayer, TraitTypes, &CvPlayer::hasTrait>

template<>
const std::string CvPlayerTraitPrereq::TAG = "HasTrait";



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
	TRY_READ_RETURN_PREREQ( sTagName, CvPlayerTraitPrereq )

	return NULL;
}
