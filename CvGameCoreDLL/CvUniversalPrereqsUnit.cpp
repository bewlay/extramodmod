/*
 * CvUniversalPrereqsUnit.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"

// implemented header
#include "CvUniversalPrereqsUnit.h"



#include "CvUnit.h"



//----------------
// pre-definitions
//----------------

template<>
CvPrereq<CvPlot>* CvPrereq<CvPlot>::readPrereq( CvXMLLoadUtility* pXml );


//-----------------
// CvPrereq<CvUnit>
//-----------------

template<>
CvPrereq<CvUnit>* CvPrereq<CvUnit>::readPrereq( CvXMLLoadUtility* pXml )
{
	const std::string sTagName = getCurrentTagName( pXml->GetXML() );

	//std::cout << "Trying to read unit prereq " << sTagName << std::endl;

	TRY_READ_RETURN_PREREQ( sTagName, CvAndPrereq<CvUnit> )
	TRY_READ_RETURN_PREREQ( sTagName, CvOrPrereq<CvUnit> )
	TRY_READ_RETURN_PREREQ( sTagName, CvNotPrereq<CvUnit> )
	TRY_READ_RETURN_PREREQ( sTagName, CvUnitPlotPrereq )
	TRY_READ_RETURN_PREREQ( sTagName, CvUnitAlivePrereq )
	TRY_READ_RETURN_PREREQ( sTagName, CvUnitHasPromotionPrereq )

	return NULL;
}

//-----------------
// CvUnitPlotPrereq
//-----------------

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


//------------------
// CvUnitAlivePrereq
//------------------

const std::string CvUnitAlivePrereq::TAG = "bAlive";

CvUnitAlivePrereq::CvUnitAlivePrereq( bool bAlive ) :
	m_bAlive( bAlive )
{
}

CvUnitAlivePrereq::~CvUnitAlivePrereq()
{
}

bool CvUnitAlivePrereq::isValid( const CvUnit* pUnit ) const
{
	return pUnit->isAlive() == m_bAlive;
}

CvUnitAlivePrereq* CvUnitAlivePrereq::read( CvXMLLoadUtility* pXml )
{
	bool bAlive;
	pXml->GetXmlVal( &bAlive ); // TODO: check and maybe return NULL

	return new CvUnitAlivePrereq( bAlive );
}


//-------------------------
// CvUnitHasPromotionPrereq
//-------------------------

const std::string CvUnitHasPromotionPrereq::TAG = "HasPromotion";

CvUnitHasPromotionPrereq::CvUnitHasPromotionPrereq( PromotionTypes ePromotion ) :
		m_ePromotion( ePromotion )
{
}

CvUnitHasPromotionPrereq::~CvUnitHasPromotionPrereq()
{
}

bool CvUnitHasPromotionPrereq::isValid( const CvUnit* pUnit ) const
{
	return pUnit->isHasPromotion( m_ePromotion );
}

CvUnitHasPromotionPrereq* CvUnitHasPromotionPrereq::read( CvXMLLoadUtility* pXml )
{
	std::string sPromotion;
	if( ! pXml->GetXmlVal( sPromotion ) )
		return NULL;

	int iPromotion = pXml->FindInInfoClass( sPromotion.c_str() );
	return new CvUnitHasPromotionPrereq( (PromotionTypes) iPromotion );
}
