/*
 * CvUniversalPrereqsPlot.h
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

#ifndef CVUNIVERSALPREREQSPLOT_H_
#define CVUNIVERSALPREREQSPLOT_H_

#include "CvUniversalPrereqs.h"

class CvPlot;


class CvPlotOwnedPrereq : public CvPrereq<CvPlot>
{
public :
	CvPlotOwnedPrereq( bool bOwned );
	virtual ~CvPlotOwnedPrereq();


	static const std::string TAG;

	bool isValid( const CvPlot* pPlot ) const;

	static CvPlotOwnedPrereq* read( CvXMLLoadUtility* pXml );

private :
	const bool m_bOwned;
};


#endif /* CVUNIVERSALPREREQSPLOT_H_ */
