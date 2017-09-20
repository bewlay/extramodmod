/*
 * CvUniversalPrereqsPlayer.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"

// implemented header
#include "CvUniversalPrereqsPlayer.h"



#include "CvPlayer.h"


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


//---------------------------
// CvPlayerCivilizationPrereq
//---------------------------

const std::string CvPlayerCivilizationPrereq::TAG = "CivilizationType";

CvPlayerCivilizationPrereq::CvPlayerCivilizationPrereq( CivilizationTypes eCiv ) :
		m_eCiv( eCiv )
{
}

CvPlayerCivilizationPrereq::~CvPlayerCivilizationPrereq()
{
}

bool CvPlayerCivilizationPrereq::isValid( const CvPlayer* pPlayer ) const
{
	return pPlayer->getCivilizationType() == m_eCiv;
}

CvPlayerCivilizationPrereq* CvPlayerCivilizationPrereq::read( CvXMLLoadUtility* pXml )
{
	std::string sCiv;
	if( ! pXml->GetXmlVal( sCiv ) )
		return NULL;

	int iCiv = pXml->FindInInfoClass( sCiv.c_str() );
	return new CvPlayerCivilizationPrereq( (CivilizationTypes) iCiv );
}


//--------------------
// CvPlayerCivicPrereq
//--------------------

const std::string CvPlayerCivicPrereq::TAG = "CivicType";

CvPlayerCivicPrereq::CvPlayerCivicPrereq( CivicTypes eCivic ) :
		m_eCivic( eCivic )
{
}

CvPlayerCivicPrereq::~CvPlayerCivicPrereq()
{
}

bool CvPlayerCivicPrereq::isValid( const CvPlayer* pPlayer ) const
{
	return pPlayer->isCivic( m_eCivic );
}

CvPlayerCivicPrereq* CvPlayerCivicPrereq::read( CvXMLLoadUtility* pXml )
{
	std::string sCivic;
	if( ! pXml->GetXmlVal( sCivic ) )
		return NULL;

	int eCivic = pXml->FindInInfoClass( sCivic.c_str() );
	return new CvPlayerCivicPrereq( (CivicTypes) eCivic );
}
