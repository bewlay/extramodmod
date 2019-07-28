# Python help for UniversalPrereqs
# TODO: more doc

from CvPythonExtensions import *
import CvUtil


gc = CyGlobalContext()
localText = CyTranslator()

DEBUG_OUTPUT = True


def prereqChildren( pPrereq ) :
	for i in range( pPrereq.getNumChildren() ) :
		yield pPrereq.getChild( i )

def _debugPrereqHelp( pPrereq, indent = "" ) :
	if pPrereq is None :
		return "NONE"
	szHelp = "%s%s (%d/%s)\n" % ( indent, pPrereq.getName(), pPrereq.getIntValue(), pPrereq.getStringValue() )
	for childPrereq in prereqChildren( pPrereq ) :
		szHelp += _debugPrereqHelp( childPrereq, indent + "  " )
	return szHelp

def _handleAndPrereq( pPrereq, getHelpFunc ) :
	szName = ""
	for childPrereq in prereqChildren( pPrereq ) :
		szName += getHelpFunc( childPrereq )
	return szName


def getEventGameHelp( pPrereq, bNegated = False ) :
	if pPrereq.getName() == "And" and not bNegated :
		return _handleAndPrereq( pPrereq, getEventGameHelp )
	elif pPrereq.getName() == "Not" :
		return getEventGameHelp( pPrereq.getChild( 0 ), bNegated = not bNegated )
	elif pPrereq.getName() == "UnitNotCreated" : # TODO: Should be "UnitCreated"
		szUnitDesc = gc.getUnitInfo( pPrereq.getIntValue() ).getDescription()
		if not bNegated :
			return localText.getText( "[ICON_BULLET][COLOR_RED]Reqs no %s1_unit to be ever created[COLOR_REVERT]", (szUnitDesc,) ) # TODO: translate
		else :
			return localText.getText( "[ICON_BULLET][COLOR_RED]Reqs %s1_unit to be created[COLOR_REVERT]", (szUnitDesc,) ) # TODO: translate
	elif DEBUG_OUTPUT :
		CvUtil.pyPrint( "Cannot create help for the following Prereq" + ( bNegated and " (negated)" or "" ) + ":" )
		CvUtil.pyPrint( _debugPrereqHelp( pPrereq ) )
	
	return ""


def getEventPlayerHelp( pPrereq, bNegated = False ) :
	if pPrereq.getName() == "And" and not bNegated :
		return _handleAndPrereq( pPrereq, getEventPlayerHelp )
	elif pPrereq.getName() == "Not" :
		return getEventPlayerHelp( pPrereq.getChild( 0 ), bNegated = not bNegated )
	elif pPrereq.getName() == "IsCivilization" :
		szDesc = gc.getCivilizationInfo( pPrereq.getIntValue() ).getDescription()
		if not bNegated :
			return localText.getText( "TXT_KEY_UP_REQUIRES", (szDesc,) ) + "\n" # TODO: translate
		else :
			return localText.getText( "TXT_KEY_UP_NOT_CIVILIZATION", (szDesc,) ) + "\n" # TODO: translate
	elif pPrereq.getName() == "HasCivic" :
		szDesc = gc.getCivicInfo( pPrereq.getIntValue() ).getDescription()
		if not bNegated :
			return localText.getText( "TXT_KEY_UP_REQUIRES", (szDesc,) ) + "\n" # TODO: translate
		else :
			return localText.getText( "TXT_KEY_UP_NOT_CIVIC", (szDesc,) ) + "\n" # TODO: translate
	elif pPrereq.getName() == "HasTrait" :
		szDesc = gc.getTraitInfo( pPrereq.getIntValue() ).getDescription()
		if not bNegated :
			return localText.getText( "TXT_KEY_UP_REQUIRES", (szDesc,) ) + "\n" # TODO: translate
		else :
			return localText.getText( "TXT_KEY_UP_NOT_TRAIT", (szDesc,) ) + "\n" # TODO: translate
	elif DEBUG_OUTPUT :
		CvUtil.pyPrint( "Cannot create help for the following Prereq" + ( bNegated and " (negated)" or "" ) + ":" )
		CvUtil.pyPrint( _debugPrereqHelp( pPrereq ) )
	
	return ""
	

# Called from DLL
def eventGameHelp( argsList ) :
	(pPrereq,) = argsList
	return getEventGameHelp( pPrereq )

# Called from DLL
def eventPlayerHelp( argsList ) :
	pPrereq, ePlayer = argsList
	return getEventPlayerHelp( pPrereq, ePlayer )

# Called from DLL
def eventPlotHelp( argsList ) :
	pPrereq, iX, iY = argsList
	return "" # TODO

# Called from DLL
def eventUnitHelp( argsList ) :
	pPrereq, ePlayer, iUnitIdx = argsList
	return "" # TODO
