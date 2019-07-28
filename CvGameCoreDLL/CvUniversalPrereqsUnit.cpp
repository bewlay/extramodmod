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

#include "CvUniversalPrereqsHelpers.h"


// Forward declarations
class CvPlot;


//-------------------
// Extern definitions
//-------------------

// For CvUnitPlotPrereq;
template<>
CvPrereq<CvPlot>* CvPrereq<CvPlot>::readPrereq( CvXMLLoadUtility* pXml );


//------------------
// CvUnitAlivePrereq
//------------------

/**
 * Requires the given unit to be alive (not e.g. a zombie).
 */
#define CvUnitAlivePrereq CvBoolPropertyEqualPrereq<CvUnit, &CvUnit::isAlive>

template<>
const std::string CvUnitAlivePrereq::TAG = "bAlive";


//-------------------------
// CvUnitHasPromotionPrereq
//-------------------------

/**
 * Requires the given unit to have the specified promotion.
 */
#define CvUnitHasPromotionPrereq CvInfoTypeSetPropertyContainsPrereq\
		<CvUnit, PromotionTypes, &CvUnit::isHasPromotion>

template<>
const std::string CvUnitHasPromotionPrereq::TAG = "HasPromotion";


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

CvPrereqStruct* CvUnitPlotPrereq::makeStruct() const
{
	CvPrereqStruct* result = new CvPrereqStruct( TAG );

	result->m_vpChildren.push_back( m_pPlotPrereq->makeStruct() );

	return result;
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
