/*
 * CvUniversalPrereqs.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"

// implemented header
#include "CvUniversalPrereqs.h"

//--------------
// DYNAMIC STRUCTS
// for python and AI
//--------------


CvPrereqStruct::CvPrereqStruct( const std::string& szName )
	: m_szName( szName ), m_iValue( -1 ) {}

CvPrereqStruct::CvPrereqStruct( const std::string& szName, int iValue )
	: m_szName( szName ), m_iValue( iValue ) {}

CvPrereqStruct::CvPrereqStruct( const std::string& szName, const std::string& szValue )
	: m_szName( szName ), m_iValue( -1 ), m_szValue( szValue ) {}

CvPrereqStruct::~CvPrereqStruct()
{
	for( size_t i = 0; i < m_vpChildren.size(); i++ ) {
		SAFE_DELETE( m_vpChildren.at( i ) );
	}
	m_vpChildren.clear();
}

int CvPrereqStruct::getIntValue() const
{
	return m_iValue;
}

const char* CvPrereqStruct::getStringValue() const
{
	return m_szValue.c_str();
}

std::string CvPrereqStruct::getName() const
{
	return m_szName;
}

int CvPrereqStruct::getNumChildren() const
{
	return m_vpChildren.size();
}

const CvPrereqStruct* CvPrereqStruct::getChild( int index ) const
{
	return m_vpChildren.at( index );
}


//------
// UTIL
//------

const std::string getCurrentTagName( FXml* xml )
{
	// This seems... dangerous. I found no better way with civ's xml interface, though.
	char sTagNameBuffer[1024];
	gDLL->getXMLIFace()->GetLastLocatedNodeTagName( xml, sTagNameBuffer );
	return std::string( sTagNameBuffer );
}
