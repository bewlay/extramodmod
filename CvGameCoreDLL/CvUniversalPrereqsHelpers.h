/*
 * CvUniversalPrereqsHelpers.h
 *
 * UNIVERSAL_PREREQS 07/2019 lfgr
 */

#ifndef CVUNIVERSALPREREQSHELPERS_H_
#define CVUNIVERSALPREREQSHELPERS_H_


#include <string>

#include "CvInfoUtils.h"
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

	CvPrereqStruct* makeStruct() const
	{
		return new CvPrereqStruct( TAG, this->m_expectedReturnValue );
	}

	static const std::string TAG;

	static CvPropertyEqualPrereq<T, R, Getter>* read(
			CvXMLLoadUtility* pXml )
	{
		R val;
		pXml->GetXmlVal( &val ); // TODO: check and maybe return NULL

		return new CvPropertyEqualPrereq<T, R, Getter>( val );
	}

private :
	R m_expectedReturnValue;
};


template<class T, class R, R (T::*Getter)() const>
class CvInfoTypePropertyEqualPrereq : public CvPrereq<T>
{
public :
	CvInfoTypePropertyEqualPrereq( const char* szExpectedInfoType )
			: m_zExpectedInfoType( szExpectedInfoType ) {}

	bool isValid( const T* obj ) const
	{
		return (obj->*Getter)() == m_zExpectedInfoType.getInfoType();
	}

	CvPrereqStruct* makeStruct() const
	{
		return new CvPrereqStruct( TAG, m_zExpectedInfoType.getInfoType() );
	}

	void readPass3()
	{
		m_zExpectedInfoType.readPass3();
	}


	static const std::string TAG;

	static CvInfoTypePropertyEqualPrereq<T, R, Getter>* read(
			CvXMLLoadUtility* pXml )
	{
		std::string sInfoType;
		if( ! pXml->GetXmlVal( sInfoType ) )
			return NULL;

		return new CvInfoTypePropertyEqualPrereq<T, R, Getter>( sInfoType.c_str() );
	}

private :
	LazyInfoTypeStore<R> m_zExpectedInfoType;
};

/**
 * Template for CvPrereqs that check whether a "set array" property contains the
 * specified info type. A "set array" is defined by a getter of the form
 *   bool CLASS:GETTER( E index )
 * where E the element type, an enum type like UnitTypes.
 */
template<class T, class E, bool (T::*Getter)(E) const>
class CvInfoTypeSetPropertyContainsPrereq : public CvPrereq<T>
{
public :
	CvInfoTypeSetPropertyContainsPrereq( const char* szInfoType )
			: m_zElement( szInfoType )
	{
	}

	bool isValid( const T* obj ) const
	{
		return (obj->*Getter)( m_zElement.getInfoType() );
	}

	CvPrereqStruct* makeStruct() const
	{
		return new CvPrereqStruct( TAG, (int) m_zElement.getInfoType() );
	}

	void readPass3()
	{
		m_zElement.readPass3();
	}

	static const std::string TAG;

	static CvInfoTypeSetPropertyContainsPrereq<T, E, Getter>*
		read( CvXMLLoadUtility* pXml )
	{
		std::string sInfoType;
		if( ! pXml->GetXmlVal( sInfoType ) )
			return NULL;

		return new CvInfoTypeSetPropertyContainsPrereq<T, E, Getter>( sInfoType.c_str() );
	}

private :
	LazyInfoTypeStore<E> m_zElement;
};


#endif /* CVUNIVERSALPREREQSHELPERS_H_ */
