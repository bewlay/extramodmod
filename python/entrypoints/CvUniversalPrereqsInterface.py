# Python help for UniversalPrereqs
# TODO: more doc

from CvPythonExtensions import *
import CvUtil


gc = CyGlobalContext()
localText = CyTranslator()

DEBUG_OUTPUT = True


### Helper functions and classes

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


# For OR

def _get_spanish_or( next ) :
	# type: (unicode) -> unicode
	if next.startswith( u"o" ) or next.startswith( u"ho" ) :
		return u" u "
	elif len( next ) > 0 and next[0].isdigit() :
		return u" \xc3\xb3 " # Accent before numbers
	else :
		return u" o "


def join_or( ls ) :
	""" Join a list of strings with 'or's """
	if CyGame().getCurrentLanguage() == 2 : # German
		sep = u", "
		lastSep = lambda x: u" oder "
	elif CyGame().getCurrentLanguage() == 4 : # Spanish
		sep = u", "
		lastSep = _get_spanish_or
	else : # English (default)
		sep = u", "
		if len( ls ) >= 3 :
			lastSep = lambda x: u", or " # Serial comma
		else :
			lastSep = lambda x: u" or "

	result = u""
	for idx, s in enumerate( ls ) :
		if idx == 0 :
			result += s
		elif idx == len( ls ) - 1 :
			result += lastSep( s )
			result += s
		else :
			result += sep
			result += s
	return result


# For generic non-composite prereqs

class InfoDescriptionPrereqHelpHelper :
	def __init__( self, infoGetter, szText, szNegatedText, bBlockShortHelp = False ) :
		# type: (Callable[[int], Any], str, str, bool) -> None
		self._infoGetter = infoGetter
		self._szText = szText
		self._szNegatedText = szNegatedText
		self._bBlockShortHelp = bBlockShortHelp
	
	def short_help( self, pPrereq, *extraArgs ) :
		# type: (Any, Any) -> Optional[unicode]
		if self._bBlockShortHelp :
			return None
		else :
			return self._infoGetter( pPrereq.getIntValue() ).getDescription()
	
	def long_help( self, pPrereq, bNegated, *extraArgs ) :
		# type: (Any, bool, Any) -> unicode
		szDesc = self._infoGetter( pPrereq.getIntValue() ).getDescription()
		if not bNegated :
			return localText.getText( self._szText, (szDesc,) )
		else :
			return localText.getText( self._szNegatedText, (szDesc,) )


### Base event help

def getEventHelp( pPrereq, shortFunc, longFunc, bNegated = False, extraArgs = () ) :
	# type: (Any, Callable[..., Optional[unicode]], Callable[..., unicode], bool, Sequence[Any] ) -> unicode
	if pPrereq.getName() in ("And", "Or", "Not") :
		if ( pPrereq.getName() == "And" and not bNegated ) or ( pPrereq.getName() == "Or" and bNegated ) : # TODO?
			return "\n".join( getEventHelp( pChild, shortFunc, longFunc, bNegated, extraArgs ) for pChild in prereqChildren( pPrereq ) )
		elif pPrereq.getName() == "Not" :
			return getEventHelp( pPrereq.getChild( 0 ), shortFunc, longFunc, not bNegated, extraArgs )
		elif pPrereq.getName() == "Or" and not bNegated : # TODO: Handle bNegated?
			lsChildThings = [shortFunc( child, *extraArgs ) for child in prereqChildren( pPrereq )]
			if None not in lsChildThings :
				return localText.getText( "TXT_KEY_UP_REQUIRES", ( join_or( lsChildThings ),) )
			# else: give up and return u""
		elif DEBUG_OUTPUT :
			CvUtil.pyPrint( "Cannot create help for the following Prereq" + ( bNegated and " (negated)" or "" ) + ":" )
			CvUtil.pyPrint( _debugPrereqHelp( pPrereq ) )
	else :
		return longFunc( pPrereq, bNegated, *extraArgs )
	
	return u""


### Game

GAME_HELPERS = {
	"UnitNotCreated" : InfoDescriptionPrereqHelpHelper( gc.getUnitInfo,
			"[ICON_BULLET][COLOR_RED]Reqs no %s1_unit to be ever created[COLOR_REVERT]", # TODO: Translate
			"[ICON_BULLET][COLOR_RED]Reqs %s1_unit to be created[COLOR_REVERT]", bBlockShortHelp = True )
}

def getEventGameShortRequiredHelp( pPrereq ) :
	"""
	Returns the "thing" that is required by the given prereq, to displayed in the form
		"Reqs [thing], [thing], ... or [thing]".
	Returns None if this is not possible.
	"""
	helper = GAME_HELPERS.get( pPrereq.getName() )
	if helper is not None :
		return helper.short_help( pPrereq )
	
	return None

def getEventGameHelp( pPrereq, bNegated ) :
	helper = GAME_HELPERS.get( pPrereq.getName() )
	if helper is not None :
		return helper.long_help( pPrereq, bNegated )
	elif DEBUG_OUTPUT :
		CvUtil.pyPrint( "Cannot create game help for the following prereq" + ( bNegated and " (negated)" or "" ) + ":" )
		CvUtil.pyPrint( _debugPrereqHelp( pPrereq ) )
	
	return u""


### Player

PLAYER_HELPERS = {
	"IsCivilization" : InfoDescriptionPrereqHelpHelper( gc.getCivilizationInfo,
			"TXT_KEY_UP_REQUIRES", "TXT_KEY_UP_NOT_CIVILIZATION" ),
	"IsAlignment" : InfoDescriptionPrereqHelpHelper( gc.getAlignmentInfo,
			"TXT_KEY_UP_REQUIRES", "TXT_KEY_UP_NOT_ALIGNMENT" ),
	"HasCivic" : InfoDescriptionPrereqHelpHelper( gc.getCivicInfo,
			"TXT_KEY_UP_REQUIRES", "TXT_KEY_UP_NOT_CIVIC" ),
	"HasTrait" : InfoDescriptionPrereqHelpHelper( gc.getTraitInfo,
			"TXT_KEY_UP_REQUIRES", "TXT_KEY_UP_NOT_TRAIT" )
}

def getEventPlayerShortRequiredHelp( pPrereq, ePlayer ) :
	helper = PLAYER_HELPERS.get( pPrereq.getName() )
	if helper is not None :
		return helper.short_help( pPrereq, ePlayer )

	return None

def getEventPlayerHelp( pPrereq, bNegated, ePlayer ) :
	helper = PLAYER_HELPERS.get( pPrereq.getName() )
	if helper is not None :
		return helper.long_help( pPrereq, bNegated, ePlayer )
	elif DEBUG_OUTPUT :
		CvUtil.pyPrint( "Cannot create player help for the following prereq" + ( bNegated and " (negated)" or "" ) + ":" )
		CvUtil.pyPrint( _debugPrereqHelp( pPrereq ) )
	
	return u""


# City

CITY_HELPERS = {
	"HasBuildingClass" : InfoDescriptionPrereqHelpHelper( gc.getBuildingClassInfo,
			"TXT_KEY_UP_REQUIRES", "TXT_KEY_UP_NOT_BUILDINGCLASS" ) # TODO: Add text key TXT_KEY_UP_NOT_BUILDINGCLASS
}

def getEventCityShortRequiredHelp( pPrereq, iX, iY ) :
	helper = CITY_HELPERS.get( pPrereq.getName() )
	if helper is not None :
		return helper.short_help( pPrereq, iX, iY )

	return None

def getEventCityHelp( pPrereq, bNegated, iX, iY ) :
	helper = CITY_HELPERS.get( pPrereq.getName() )
	if helper is not None :
		return helper.long_help( pPrereq, bNegated, iX, iY )
	elif DEBUG_OUTPUT :
		CvUtil.pyPrint( "Cannot create city help for the following prereq" + ( bNegated and " (negated)" or "" ) + ":" )
		CvUtil.pyPrint( _debugPrereqHelp( pPrereq ) )
	
	return u""
	

# Called from DLL
def eventGameHelp( argsList ) :
	(pPrereq,) = argsList
	return getEventHelp( pPrereq, getEventGameShortRequiredHelp, getEventGameHelp )

# Called from DLL
def eventPlayerHelp( argsList ) :
	pPrereq, ePlayer = argsList
	return getEventHelp( pPrereq, getEventPlayerShortRequiredHelp, getEventPlayerHelp, extraArgs = [ePlayer] )

# Called from DLL
def eventCityHelp( argsList ) :
	pPrereq, iX, iY = argsList
	return getEventHelp( pPrereq, getEventCityShortRequiredHelp, getEventCityHelp, extraArgs = [iX, iY] )

# Called from DLL
def eventPlotHelp( argsList ) :
	pPrereq, iX, iY = argsList
	return u"" # TODO

# Called from DLL
def eventUnitHelp( argsList ) :
	pPrereq, ePlayer, iUnitIdx = argsList
	return u"" # TODO
