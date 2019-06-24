/*
 * CvUniversalPrereqs.h
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

#ifndef CVUNIVERSALPREREQS_H_
#define CVUNIVERSALPREREQS_H_

#include <string>

#include "CvDLLXMLIFaceBase.h"
#include "CvEnums.h"
#include "CvGlobals.h"
#include "CvXMLLoadUtility.h"


//------
// UTIL
//------

//#define INDENT "  "

#define TRY_READ_RETURN_PREREQ(sTagName, cls) {\
	if( sTagName == cls::TAG )\
		return cls::read( pXml );\
}

const std::string getCurrentTagName( FXml* xml );

//--------------
// GENERIC
//--------------

/**
 * Superclass to check requirements on any given object.
 */
template<class T>
class CvPrereq
{
public :
	virtual ~CvPrereq()
	{
	}

	/**
	 * Whether the given object fulfills the requirements of this.
	 */
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
			FAssertMsg( pChildPrereq != NULL, CvString::format(
					"Couldn't read child prereq <%s>",
					getCurrentTagName( pXml->GetXML() ).c_str() ) );
			vpDest.push_back( pChildPrereq );

			if( ! gDLL->getXMLIFace()->NextSibling( pXml->GetXML() ) )
				break;
		}

		gDLL->getXMLIFace()->SetToParent( pXml->GetXML() );
	}
}


/**
 * Requires the given object to fulfill all of the specified requirements.
 */
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


/**
 * Requires the given object to fulfill at least one of the specified requirements.
 */
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


/**
 * Requires the given object to not fulfill the specified requirement.
 */
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


//----------------
// GENERIC HELPERS
//----------------

// TODO: doc
// Must be subclassed (doesn't define TAG)
template<class T, class R, R (T::*Getter)() const>
class CvPropertyEqualPrereq : public CvPrereq<T>
{
public :
	CvPropertyEqualPrereq( R expectedReturnValue )
		: m_expectedReturnValue( expectedReturnValue )
	{
	}

	bool isValid( const T* obj ) const
	{
		return (obj->*Getter)() == m_expectedReturnValue;
	}


	static CvPropertyEqualPrereq<T, R, Getter>* read( CvXMLLoadUtility* pXml );

private :
	R m_expectedReturnValue;
};


template<class T, class R, R (T::*Getter)() const>
class CvInfoTypePropertyEqualPrereq : public CvPropertyEqualPrereq<T, R, Getter>
{
public :
	CvInfoTypePropertyEqualPrereq( R expectedReturnValue )
			: CvPropertyEqualPrereq<T, R, Getter>( expectedReturnValue )
	{
	}


	static const std::string TAG;

	static CvInfoTypePropertyEqualPrereq<T, R, Getter>* read(
			CvXMLLoadUtility* pXml )
	{
		std::string sInfoType;
		if( ! pXml->GetXmlVal( sInfoType ) )
			return NULL;

		int iInfoType = pXml->FindInInfoClass( sInfoType.c_str() );
		return new CvInfoTypePropertyEqualPrereq<T, R, Getter>(
				(R) iInfoType );
	}
};


/**
 * Template for CvPrereqs that check whether a bool property is true.
 */
template<class T, bool (T::*Getter)() const>
class CvBoolPropertyEqualPrereq : public CvPropertyEqualPrereq<T, bool, Getter>
{
public :
	CvBoolPropertyEqualPrereq( bool bExpectedReturnValue )
			: CvPropertyEqualPrereq<T, bool, Getter>( bExpectedReturnValue )
	{
	}


	static const std::string TAG;

	static CvBoolPropertyEqualPrereq<T, Getter>* read(
			CvXMLLoadUtility* pXml )
	{
		bool bVal;
		pXml->GetXmlVal( &bVal ); // TODO: check and maybe return NULL

		return new CvBoolPropertyEqualPrereq<T, Getter>( bVal );
	}
};

/**
 * Template for CvPrereqs that check whether a "set array" property contains the
 * specified element. A "set array" is defined by a getter of the form
 *   bool CLASS:GETTER( E index )
 * where E the element type, usually an int or an enum type like UnitTypes.
 */
template<class T, class E, bool (T::*Getter)(E) const>
class CvSetPropertyContainsPrereq : public CvPrereq<T>
{
public :
	CvSetPropertyContainsPrereq( E element )
			: m_element( element )
	{
	}

	bool isValid( const T* obj ) const
	{
		return (obj->*Getter)( m_element );
	}

	static CvSetPropertyContainsPrereq<T, E, Getter>*
		read( CvXMLLoadUtility* pXml );

private :
	E m_element;
};

template<class T, class E, bool (T::*Getter)(E) const>
class CvInfoTypeSetPropertyContainsPrereq :
		public CvSetPropertyContainsPrereq<T, E, Getter>
{
public :
	CvInfoTypeSetPropertyContainsPrereq( E element )
			: CvSetPropertyContainsPrereq<T, E, Getter>( element )
	{
	}


	static const std::string TAG;

	static CvInfoTypeSetPropertyContainsPrereq<T, E, Getter>*
		read( CvXMLLoadUtility* pXml )
	{
		std::string sInfoType;
		if( ! pXml->GetXmlVal( sInfoType ) )
			return NULL;

		int iInfoType = pXml->FindInInfoClass( sInfoType.c_str() );
		return new CvInfoTypeSetPropertyContainsPrereq<T, E, Getter>(
				(E) iInfoType );
	}

private :
	E m_element;
};




#endif /* CVUNIVERSALPREREQS_H_ */
