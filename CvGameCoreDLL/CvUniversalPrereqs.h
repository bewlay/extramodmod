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

#define TRY_READ_RETURN_PREREQ(sTagName, cls) {\
	if( sTagName == cls::TAG )\
		return cls::read( pXml );\
}

const std::string getCurrentTagName( FXml* xml );


//--------------
// DYNAMIC STRUCTS
// for python and AI
//--------------

struct CvPrereqStruct
{
	CvPrereqStruct() {} // Necessary default constructor
	CvPrereqStruct( const std::string& szName );
	CvPrereqStruct( const std::string& szName, int iValue );
	CvPrereqStruct( const std::string& szName, const std::string& szValue );
	virtual ~CvPrereqStruct();

	int getIntValue() const;
	const char* getStringValue() const;

	// For python
	std::string getName() const;
	int getNumChildren() const;
	const CvPrereqStruct* getChild( int index ) const;

	// Prereq name, usually just the tag
	std::string m_szName;

	// Int/String value, if applicable. Usually only one is used.
	int m_iValue;
	std::string m_szValue;

	// Child structs, if applicable
	std::vector<CvPrereqStruct*> m_vpChildren;
};


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

	/**
	 * Create a CvPrereqStruct from this.
	 *
	 * Allocates memory for it, so make sure to destroy it afterwards.
	 */
	virtual CvPrereqStruct* makeStruct() const = 0;

	/**
	 * Create a CvPrereqStruct from this, containing all requirements that are *not* satisfied.
	 * Returns NULL if requirment is satisfied. Otherwise, allocates memory for it, so make sure
	 * to destroy it afterwards.
	 * 
	 * pObj might be NULL. In this case, this behaves like makeStruct().
	 */
	virtual CvPrereqStruct* makeStruct( const T* pObj ) const
	{
		// Default implementation
		if( pObj == NULL || ! isValid( pObj ) )
		{
			return makeStruct();
		}
		else
		{
			return NULL;
		}
	}


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
		for( size_t i = 0; i < m_vpPrereqs.size(); i++ )
		{
			delete m_vpPrereqs.at( i );
		}
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

	// And is a special case, as it may return a partial child list.
	CvPrereqStruct* makeStruct() const
	{
		return makeStruct( NULL );
	}
	
	CvPrereqStruct* makeStruct( const T* pObj ) const
	{
		CvPrereqStruct* result = new CvPrereqStruct( TAG );

		for( size_t i = 0; i < m_vpPrereqs.size(); i++ )
		{
			CvPrereqStruct* child = m_vpPrereqs.at( i )->makeStruct( pObj );
			if( child != NULL )
			{
				result->m_vpChildren.push_back( child );
			}
		}

		if( result->m_vpChildren.empty() )
		{
			delete result;
			return NULL;
		}
		else
		{
			return result;
		}
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

	// TODO: Duplicate code
	virtual ~CvOrPrereq()
	{
		for( size_t i = 0; i < m_vpPrereqs.size(); i++ )
		{
			delete m_vpPrereqs.at( i );
		}
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
	
	// Or is *not* a special case like And, as Or always has a complete
	//  list of unsatisfied children, or none.
	CvPrereqStruct* makeStruct() const
	{
		CvPrereqStruct* result = new CvPrereqStruct( TAG );

		for( size_t i = 0; i < m_vpPrereqs.size(); i++ )
		{
			result->m_vpChildren.push_back( m_vpPrereqs.at( i )->makeStruct() );
		}

		return result;
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
		SAFE_DELETE_ARRAY( m_pPrereq );
	}

	bool isValid( const T* pObj ) const
	{
		return !m_pPrereq->isValid( pObj );
	}

	CvPrereqStruct* makeStruct() const
	{
		CvPrereqStruct* result = new CvPrereqStruct( TAG );

		result->m_vpChildren.push_back( m_pPrereq->makeStruct() );

		return result;
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
