/*
 * CvUniversalPrereqsGame.h
 *
 *  Created on: Sep 24, 2017
 */

#ifndef CVUNIVERSALPREREQSGAME_H_
#define CVUNIVERSALPREREQSGAME_H_


#include "CvEnums.h"

#include "CvUniversalPrereqs.h"

#include "CvInfoUtils.h"

class CvGame;


/**
 * Requires that the specified unit wasn't ever created.
 */
class CvGameUnitCreatedPrereq : public CvPrereq<CvGame>
{
public :
	CvGameUnitCreatedPrereq( const char* szUnit );

	virtual ~CvGameUnitCreatedPrereq();

	bool isValid( const CvGame* pGame ) const;

	CvPrereqStruct* makeStruct() const;

	void readPass3();


	static const std::string TAG;

	static CvGameUnitCreatedPrereq* read( CvXMLLoadUtility* pXml );

private :
	LazyInfoTypeStore<UnitTypes> m_zUnit;
};





#endif /* CVUNIVERSALPREREQSGAME_H_ */
