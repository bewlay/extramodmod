/*
 * CvUniversalPrereqsGame.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */


// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"


// implemented header
#include "CvUniversalPrereqsGame.h"


#include <sstream>

#include "CvGame.h"

//-----------------
// CvPrereq<CvGame>
//-----------------

template<>
CvPrereq<CvGame>* CvPrereq<CvGame>::readPrereq( CvXMLLoadUtility* pXml )
{
	const std::string sTagName = getCurrentTagName( pXml->GetXML() );

	TRY_READ_RETURN_PREREQ( sTagName, CvAndPrereq<CvGame> )
	TRY_READ_RETURN_PREREQ( sTagName, CvOrPrereq<CvGame> )
	TRY_READ_RETURN_PREREQ( sTagName, CvNotPrereq<CvGame> )
	TRY_READ_RETURN_PREREQ( sTagName, CvGameUnitNotCreatedPrereq )

	return NULL;
}

const std::string CvGameUnitNotCreatedPrereq::TAG = "UnitNotCreated";

CvGameUnitNotCreatedPrereq::CvGameUnitNotCreatedPrereq( UnitTypes eUnit ) :
		m_eUnit( eUnit )
{
}

CvGameUnitNotCreatedPrereq::~CvGameUnitNotCreatedPrereq()
{
}

bool CvGameUnitNotCreatedPrereq::isValid( const CvGame* pGame ) const
{
	return pGame->getUnitCreatedCount( m_eUnit ) == 0;
}

CvGameUnitNotCreatedPrereq* CvGameUnitNotCreatedPrereq::read( CvXMLLoadUtility* pXml )
{
	std::string sUnit;
	if( ! pXml->GetXmlVal( sUnit ) )
		return NULL;

	int iUnit = pXml->FindInInfoClass( sUnit.c_str() );
	return new CvGameUnitNotCreatedPrereq( (UnitTypes) iUnit );
}



