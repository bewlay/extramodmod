/*
 * CvUniversalPrereqs.h
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

#ifndef CVUNIVERSALPREREQS_H_
#define CVUNIVERSALPREREQS_H_


#include "CvDLLXMLIFaceBase.h"
#include "CvEnums.h"
#include "CvGlobals.h"
#include "CvXMLLoadUtility.h"

class CvPlot;
class CvUnit;


//------
// UTIL
//------

#define TRY_READ_RETURN_PREREQ(sTagName, cls) {\
	if( sTagName == cls::TAG )\
		return cls::read( pXml );\
}

const std::string getCurrentTagName( FXml* xml );

//--------------
// GENERIC
//--------------

template<class T>
class CvPrereq
{
public :
	virtual ~CvPrereq()
	{
	}

	virtual bool isValid( const T* pObj ) const = 0;


	static CvPrereq<T>* readPrereq( CvXMLLoadUtility* pXml );
};


// Helper func
template<class T>
void readChildPrereqs( CvXMLLoadUtility* pXml, std::vector<CvPrereq<T>*>& vpDest )
{
	if( gDLL->getXMLIFace()->SetToChild( pXml->GetXML() ) )
	{
		while( pXml->SkipToNextVal() )
		{
			CvPrereq<T>* pChildPrereq = CvPrereq<T>::readPrereq( pXml );
			FAssertMsg( pChildPrereq != NULL, "Error: Couldn't read child Prereq" );
			vpDest.push_back( pChildPrereq );

			if( ! gDLL->getXMLIFace()->NextSibling( pXml->GetXML() ) )
				break;
		}

		gDLL->getXMLIFace()->SetToParent( pXml->GetXML() );
	}
}


template<class T>
class CvAndPrereq : public CvPrereq<T>
{
public :
	CvAndPrereq( const std::vector<CvPrereq<T>*>& vpPrereqs ) :
			m_vpPrereqs( vpPrereqs )
	{
	}

	virtual ~CvAndPrereq()
	{
	}

	bool isValid( const T* pObj ) const
	{
		for( size_t i = 0; i < m_vpPrereqs.size(); i++ )
		{
			if( ! m_vpPrereqs[i]->isValid( pObj ) )
				return false;
		}

		return true;
	}


	static const std::string TAG;

	static CvAndPrereq<T>* read( CvXMLLoadUtility* pXml )
	{
		std::vector<CvPrereq<T>*> vpPrereqs;

		readChildPrereqs( pXml, vpPrereqs );

		return new CvAndPrereq<T>( vpPrereqs );
	}

private :
	const std::vector<CvPrereq<T>*> m_vpPrereqs;
};

template<class T>
const std::string CvAndPrereq<T>::TAG = "And";


template<class T>
class CvOrPrereq : public CvPrereq<T>
{
public :
	CvOrPrereq( const std::vector<CvPrereq<T>*>& vpPrereqs ) :
			m_vpPrereqs( vpPrereqs )
	{
	}

	virtual ~CvOrPrereq()
	{
	}

	bool isValid( const T* pObj ) const
	{
		for( size_t i = 0; i < m_vpPrereqs.size(); i++ )
		{
			if( m_vpPrereqs[i]->isValid( pObj ) )
				return true;
		}

		return false;
	}


	static const std::string TAG;

	static CvOrPrereq<T>* read( CvXMLLoadUtility* pXml )
	{
		std::vector<CvPrereq<T>*> vpPrereqs;

		readChildPrereqs( pXml, vpPrereqs );

		return new CvOrPrereq<T>( vpPrereqs );
	}

private :
	const std::vector<CvPrereq<T>*> m_vpPrereqs;
};

template<class T>
const std::string CvOrPrereq<T>::TAG = "Or";


template<class T>
class CvNotPrereq : public CvPrereq<T>
{
public :
	CvNotPrereq( CvPrereq<T>* pPrereq ) :
			m_pPrereq( pPrereq )
	{
	}

	virtual ~CvNotPrereq()
	{
	}

	bool isValid( const T* pObj ) const
	{
		return !m_pPrereq->isValid( pObj );
	}


	static const std::string TAG;

	static CvNotPrereq<T>* read( CvXMLLoadUtility* pXml )
	{
		CvPrereq<T>* pChildPrereq = NULL;

		if( gDLL->getXMLIFace()->SetToChild( pXml->GetXML() ) )
		{
			if( pXml->SkipToNextVal() )
			{
				pChildPrereq = CvPrereq<T>::readPrereq( pXml );
			}

			gDLL->getXMLIFace()->SetToParent( pXml->GetXML() );
		}

		if( pChildPrereq == NULL )
		{
			FAssertMsg( pChildPrereq != NULL, "Error: Couldn't read child Prereq" );
			return NULL;
		}
		else
			return new CvNotPrereq<T>( pChildPrereq );
	}

private :
	const CvPrereq<T>* m_pPrereq;
};

template<class T>
const std::string CvNotPrereq<T>::TAG = "Not";


#endif /* CVUNIVERSALPREREQS_H_ */
