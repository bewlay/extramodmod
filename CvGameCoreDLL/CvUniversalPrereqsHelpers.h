/*
 * CvUniversalPrereqsHelpers.h
 *
 * UNIVERSAL_PREREQS 07/2019 lfgr
 */

#ifndef CVUNIVERSALPREREQSHELPERS_H_
#define CVUNIVERSALPREREQSHELPERS_H_


#include <string>

#include "CvUniversalPrereqs.h"
#include "CvXMLLoadUtility.h"
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

protected :
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

	CvPrereqStruct* makeStruct() const
	{
		return new CvPrereqStruct( TAG, this->m_expectedReturnValue );
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

	// TODO: duplicate code
	CvPrereqStruct* makeStruct() const
	{
		return new CvPrereqStruct( TAG, this->m_expectedReturnValue );
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

protected :
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

	// TODO: duplicate code
	CvPrereqStruct* makeStruct() const
	{
		return new CvPrereqStruct( TAG, (int) this->m_element );
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
};


#endif /* CVUNIVERSALPREREQSHELPERS_H_ */
