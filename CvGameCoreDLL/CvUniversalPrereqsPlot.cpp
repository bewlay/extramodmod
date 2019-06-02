/*
 * CvUniversalPrereqsPlot.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"

// implemented header
#include "CvUniversalPrereqsPlot.h"



#include "CvPlot.h"


//-----------------
// CvPrereq<CvPlot>
//-----------------

template<>
CvPrereq<CvPlot>* CvPrereq<CvPlot>::readPrereq( CvXMLLoadUtility* pXml )
{
	const std::string sTagName = getCurrentTagName( pXml->GetXML() );

	//std::cout << "Trying to read plot prereq " << sTagName << std::endl;

	TRY_READ_RETURN_PREREQ( sTagName, CvAndPrereq<CvPlot> )
	TRY_READ_RETURN_PREREQ( sTagName, CvOrPrereq<CvPlot> )
	TRY_READ_RETURN_PREREQ( sTagName, CvNotPrereq<CvPlot> )
	TRY_READ_RETURN_PREREQ( sTagName, CvPlotOwnedPrereq )

	return NULL;
}


//------------------
// CvPlotOwnedPrereq
//------------------

const std::string CvPlotOwnedPrereq::TAG = "bOwned";

CvPlotOwnedPrereq::CvPlotOwnedPrereq( bool bOwned ) :
	m_bOwned( bOwned )
{
}

CvPlotOwnedPrereq::~CvPlotOwnedPrereq()
{
}

bool CvPlotOwnedPrereq::isValid( const CvPlot* pPlot ) const
{
	return pPlot->isOwned() == m_bOwned;
}

CvPlotOwnedPrereq* CvPlotOwnedPrereq::read( CvXMLLoadUtility* pXml )
{
	bool bOwned;
	pXml->GetXmlVal( &bOwned ); // TODO: check and maybe return NULL

	return new CvPlotOwnedPrereq( bOwned );
}
