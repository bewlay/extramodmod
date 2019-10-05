/*
 * CvUniversalPrereqsGame.h
 *
 *  Created on: Sep 24, 2017
 */

#ifndef CVUNIVERSALPREREQSGAME_H_
#define CVUNIVERSALPREREQSGAME_H_


#include "CvEnums.h"

#include "CvUniversalPrereqs.h"

class CvGame;


/**
 * Requires that the specified unit wasn't ever created.
 */
class CvGameUnitCreatedPrereq : public CvPrereq<CvGame>
{
public :
	CvGameUnitCreatedPrereq( UnitTypes eUnit );

	virtual ~CvGameUnitCreatedPrereq();

	bool isValid( const CvGame* pGame ) const;

	CvPrereqStruct* makeStruct() const;


	static const std::string TAG;

	static CvGameUnitCreatedPrereq* read( CvXMLLoadUtility* pXml );

private :
	UnitTypes m_eUnit;
};





#endif /* CVUNIVERSALPREREQSGAME_H_ */
