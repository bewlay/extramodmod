/*
 * CvUniversalPrereqsUnit.h
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

#ifndef CVUNIVERSALPREREQSUNIT_H_
#define CVUNIVERSALPREREQSUNIT_H_


#include "CvEnums.h"

#include "CvUniversalPrereqs.h"

class CvUnit;


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

class CvUnitAlivePrereq : public CvPrereq<CvUnit>
{
public :
	CvUnitAlivePrereq( bool bAlive );
	virtual ~CvUnitAlivePrereq();

	virtual bool isValid( const CvUnit* pUnit ) const;


	static const std::string TAG;

	static CvUnitAlivePrereq* read( CvXMLLoadUtility* pXml );

private :
	bool m_bAlive;
};

class CvUnitHasPromotionPrereq : public CvPrereq<CvUnit>
{
public :
	CvUnitHasPromotionPrereq( PromotionTypes ePromotion );
	virtual ~CvUnitHasPromotionPrereq();

	virtual bool isValid( const CvUnit* pUnit ) const;


	static const std::string TAG;

	static CvUnitHasPromotionPrereq* read( CvXMLLoadUtility* pXml );

private :
	PromotionTypes m_ePromotion;
};



#endif /* CVUNIVERSALPREREQSUNIT_H_ */
