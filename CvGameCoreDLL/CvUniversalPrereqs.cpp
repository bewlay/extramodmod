/*
 * CvUniversalPrereqs.cpp
 *
 * UNIVERSAL_PREREQS 08/2017 lfgr
 */

// Obligatory include for precompiled headers (?)
#include "CvGameCoreDLL.h"

// implemented header
#include "CvUniversalPrereqs.h"


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
