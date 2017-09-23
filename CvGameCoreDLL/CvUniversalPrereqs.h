/*
 * CvUniversalPrereqs.h
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

#ifndef CVUNIVERSALPREREQS_H_
#define CVUNIVERSALPREREQS_H_


#include "CvPlot.h"
#include "CvUnit.h"


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

		if( gDLL->getXMLIFace()->SetToChild( pXml->GetXML() ) )
		{
			while( pXml->SkipToNextVal() )
			{
				CvPrereq<T>* pChildPrereq = CvPrereq<T>::readPrereq( pXml );
				FAssertMsg( pChildPrereq != NULL, "Error: Couldn't read child Prereq" );
				vpPrereqs.push_back( pChildPrereq );

				if( ! gDLL->getXMLIFace()->NextSibling( pXml->GetXML() ) )
					break;
			}

			gDLL->getXMLIFace()->SetToParent( pXml->GetXML() );
		}

		return new CvAndPrereq<T>( vpPrereqs );
	}

private :
	const std::vector<CvPrereq<T>*> m_vpPrereqs;
};

//--------------
// UNIT PREREQ
//--------------

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


//--------------
// PLOT PREREQ
//--------------

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



#endif /* CVUNIVERSALPREREQS_H_ */
