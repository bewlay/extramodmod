/*
 * CvUniversalPrereqPlayer.h
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

#ifndef CVUNIVERSALPREREQSPLAYER_H_
#define CVUNIVERSALPREREQSPLAYER_H_


#include "CvEnums.h"

#include "CvUniversalPrereqs.h"

class CvPlayer;


class CvPlayerCivicPrereq : public CvPrereq<CvPlayer>
{
public :
	CvPlayerCivicPrereq( CivicTypes eCiv );

	virtual ~CvPlayerCivicPrereq();

	bool isValid( const CvPlayer* pPlayer ) const;


	static const std::string TAG;

	static CvPlayerCivicPrereq* read( CvXMLLoadUtility* pXml );

private :
	CivicTypes m_eCivic;
};


class CvPlayerCivilizationPrereq : public CvPrereq<CvPlayer>
{
public :
	CvPlayerCivilizationPrereq( CivilizationTypes eCiv );

	virtual ~CvPlayerCivilizationPrereq();

	bool isValid( const CvPlayer* pPlayer ) const;


	static const std::string TAG;

	static CvPlayerCivilizationPrereq* read( CvXMLLoadUtility* pXml );

private :
	CivilizationTypes m_eCiv;
};


#endif /* CVUNIVERSALPREREQSPLAYER_H_ */
