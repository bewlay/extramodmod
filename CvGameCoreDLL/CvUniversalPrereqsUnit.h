/*
 * CvUniversalPrereqsUnit.h
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

#ifndef CVUNIVERSALPREREQSUNIT_H_
#define CVUNIVERSALPREREQSUNIT_H_


#include "CvEnums.h"

#include "CvUniversalPrereqs.h"

class CvPlot;
class CvUnit;


/**
 * Requires the plot of the given unit to fulfill the specified requirement.
 */
class CvUnitPlotPrereq : public CvPrereq<CvUnit>
{
public :
	CvUnitPlotPrereq( CvPrereq<CvPlot>* pPlotPrereq );
	virtual ~CvUnitPlotPrereq();

	virtual bool isValid( const CvUnit* pUnit ) const;


	static const std::string TAG;

	static CvUnitPlotPrereq* read( CvXMLLoadUtility* pXml );

private :
	CvPrereq<CvPlot>* m_pPlotPrereq;
};


#endif /* CVUNIVERSALPREREQSUNIT_H_ */
