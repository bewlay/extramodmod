/*
 * CvUniversalPrereqsPlot.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"


#include "CvPlot.h"

#include "CvUniversalPrereqs.h"
#include "CvUniversalPrereqsHelpers.h"



//------------------
// CvPlotOwnedPrereq
//------------------

#define CvPlotOwnedPrereq CvPropertyEqualPrereq<CvPlot, bool, &CvPlot::isOwned>

template<>
const std::string CvPlotOwnedPrereq::TAG = "bOwned";


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
