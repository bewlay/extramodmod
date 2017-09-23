/*
 * CvUniversalPrereqs.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"

// implemented header
#include "CvUniversalPrereqs.h"


#include "CvGlobals.h"
#include "CvXMLLoadUtility.h"
#include "CvDLLXMLIFaceBase.h"


//------
// UTIL
//------

const std::string getCurrentTagName( FXml* xml )
{
	// This seems... dangerous. I found no better way with civ's xml interface, though.
	char sTagNameBuffer[1024];
	gDLL->getXMLIFace()->GetLastLocatedNodeTagName( xml, sTagNameBuffer );
	return std::string( sTagNameBuffer );
}


//--------------
// pre-definitions
//--------------

template<>
CvPrereq<CvUnit>* CvPrereq<CvUnit>::readPrereq( CvXMLLoadUtility* pXml );

template<>
CvPrereq<CvPlot>* CvPrereq<CvPlot>::readPrereq( CvXMLLoadUtility* pXml );


//--------------
// GENERIC
//--------------

template<class T>
const std::string CvAndPrereq<T>::TAG = "And";


//--------------
// UNIT PREREQ
//--------------

const std::string CvUnitPlotPrereq::TAG = "UnitPlotPrereq";

CvUnitPlotPrereq::CvUnitPlotPrereq( CvPrereq<CvPlot>* pPlotPrereq ) :
		m_pPlotPrereq( pPlotPrereq )
{
}

CvUnitPlotPrereq::~CvUnitPlotPrereq()
{
}

bool CvUnitPlotPrereq::isValid( const CvUnit* pUnit ) const
{
	return m_pPlotPrereq->isValid( pUnit->plot() );
}

CvUnitPlotPrereq* CvUnitPlotPrereq::read( CvXMLLoadUtility* pXml )
{
	if( gDLL->getXMLIFace()->SetToChild( pXml->GetXML() ) )
	{
		if( pXml->SkipToNextVal() )
		{
			CvPrereq<CvPlot>* pPlotPrereq = CvPrereq<CvPlot>::readPrereq( pXml );
			if( pPlotPrereq == NULL )
				return NULL;

			gDLL->getXMLIFace()->SetToParent( pXml->GetXML() );

			return new CvUnitPlotPrereq( pPlotPrereq );
		}
		else
			gDLL->getXMLIFace()->SetToParent( pXml->GetXML() );
	}

	return NULL;
}

template<>
CvPrereq<CvUnit>* CvPrereq<CvUnit>::readPrereq( CvXMLLoadUtility* pXml )
{
	const std::string sTagName = getCurrentTagName( pXml->GetXML() );

	//std::cout << "Trying to read unit prereq " << sTagName << std::endl;

	if( sTagName == CvAndPrereq<CvUnit>::TAG )
		return CvAndPrereq<CvUnit>::read( pXml );
	else if( sTagName == CvUnitPlotPrereq::TAG )
		return CvUnitPlotPrereq::read( pXml );
	else
		return NULL;
}


//--------------
// PLOT PREREQ
//--------------

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
	pXml->GetXmlVal( &bOwned ); // TODO: check and return NULL

	return new CvPlotOwnedPrereq( bOwned );
}

template<>
CvPrereq<CvPlot>* CvPrereq<CvPlot>::readPrereq( CvXMLLoadUtility* pXml )
{
	const std::string sTagName = getCurrentTagName( pXml->GetXML() );

	//std::cout << "Trying to read plot prereq " << sTagName << std::endl;

	if( sTagName == CvAndPrereq<CvPlot>::TAG )
		return CvAndPrereq<CvPlot>::read( pXml );
	else if( sTagName == CvPlotOwnedPrereq::TAG )
		return CvPlotOwnedPrereq::read( pXml );
	else
		return NULL;
}
