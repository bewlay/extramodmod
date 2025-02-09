## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
#RevolutionDCM - used by the revwatch advisor code
import CvScreensInterface
import time
import CustomFunctions

# BUG - DLL - start
import BugDll
# BUG - DLL - end

# < Revolution Mod Start >
import RevInstances
game = CyGame()

# < Revolution Mod End >

#FfH: Added by Kael 10/21/2008
import ScenarioFunctions
sf = ScenarioFunctions.ScenarioFunctions()
#FfH: End Add
# BUG - Options - start
import BugCore
import BugOptions
import BugOptionsScreen
import BugPath
import BugUtil
import CityUtil
ClockOpt = BugCore.game.NJAGC
ScoreOpt = BugCore.game.Scores
MainOpt = BugCore.game.MainInterface
CityScreenOpt = BugCore.game.CityScreen
# BUG - Options - end

# RevolutionDCM
RevOpt = BugCore.game.Revolution
iMaxScoreLines = RevOpt.getMaxScoreLines()
g_bScoreShowCivName = RevOpt.isScoreShowCivName()
#RevolutionDCM -end

# BUG - PLE - start
PleOpt = BugCore.game.PLE
# BUG - PLE - end

ffhUIOpt = BugCore.game.FfHUI # lfgr 04/2021

# BUG - Align Icons - start
import Scoreboard
import PlayerUtil
# BUG - Align Icons - end

# BUG - Worst Enemy - start
import AttitudeUtil
# BUG - Refuses to Talk - end

# BUG - Refuses to Talk - start
import DiplomacyUtil
# BUG - Refuses to Talk - end

# BUG - Fractional Trade - start
import TradeUtil
# BUG - Fractional Trade - end

import BugUnitPlot

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# BUG - 3.17 No Espionage - start
import GameUtil
# BUG - 3.17 No Espionage - end

# BUG - Reminders - start
import ReminderEventManager
# BUG - Reminders - end

# BUG - Great General Bar - start
import GGUtil
# BUG - Great General Bar - end


#FfH: Added by Kael 10/29/2007
bshowManaBar = 1
manaTypes1 = [ 'BONUS_MANA_AIR','BONUS_MANA_BODY','BONUS_MANA_CHAOS','BONUS_MANA_CREATION','BONUS_MANA_DEATH','BONUS_MANA_DIMENSIONAL','BONUS_MANA_EARTH','BONUS_MANA_ENCHANTMENT','BONUS_MANA_ENTROPY','BONUS_MANA_FIRE','BONUS_MANA_FORCE','BONUS_MANA_ICE','BONUS_MANA_LAW','BONUS_MANA_LIFE','BONUS_MANA_METAMAGIC','BONUS_MANA_MIND','BONUS_MANA_NATURE','BONUS_MANA_SHADOW','BONUS_MANA_SPIRIT','BONUS_MANA_SUN','BONUS_MANA_WATER' ]
MANA_X_POS = 0
MANA_Y_POS = 103
#FfH: End Add
# BUG - Great Person Bar - start
import GPUtil
GP_BAR_WIDTH = 320
# BUG - Great Person Bar - end

# BUG - Progress Bar - Tick Marks - start
import ProgressBarUtil
# BUG - Progress Bar - Tick Marks - end

# PLE Code
import PLE

g_NumEmphasizeInfos = 0
g_NumCityTabTypes = 0
g_NumHurryInfos = 0
g_NumUnitClassInfos = 0
g_NumBuildingClassInfos = 0
g_NumProjectInfos = 0
g_NumProcessInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

# BUG - city specialist - start
g_iSuperSpecialistCount = 0
g_iCitySpecialistCount = 0
g_iAngryCitizensCount = 0
SUPER_SPECIALIST_STACK_WIDTH = 15
SPECIALIST_ROW_HEIGHT = 34
SPECIALIST_ROWS = 3
MAX_SPECIALIST_BUTTON_SPACING = 30
SPECIALIST_AREA_MARGIN = 45
# BUG - city specialist - end

MAX_SELECTED_TEXT = 5
MAX_DISPLAYABLE_BUILDINGS = 15
MAX_DISPLAYABLE_TRADE_ROUTES = 4
MAX_BONUS_ROWS = 10
MAX_CITIZEN_BUTTONS = 8

SELECTION_BUTTON_COLUMNS = 8
SELECTION_BUTTON_ROWS = 2
NUM_SELECTION_BUTTONS = SELECTION_BUTTON_ROWS * SELECTION_BUTTON_COLUMNS

g_iNumBuildingWidgets = MAX_DISPLAYABLE_BUILDINGS
g_iNumTradeRouteWidgets = MAX_DISPLAYABLE_TRADE_ROUTES

# END OF TURN BUTTON POSITIONS
######################
iEndOfTurnButtonSize = 64
#FfH: Modified by Kael 07/18/2008
iEndOfTurnPosX = 296 # distance from right
iEndOfTurnPosY = 147 # distance from bottom

# MINIMAP BUTTON POSITIONS
######################
iMinimapButtonsExtent = 228
iMinimapButtonsX = 227
iMinimapButtonsY_Regular = 160
iMinimapButtonsY_Minimal = 32
iMinimapButtonWidth = 24
iMinimapButtonHeight = 24

# Globe button
iGlobeButtonX = 48
iGlobeButtonY_Regular = 168
iGlobeButtonY_Minimal = 40
iGlobeToggleWidth = 48
iGlobeToggleHeight = 48

# GLOBE LAYER OPTION POSITIONING
######################
iGlobeLayerOptionsX  = 235
iGlobeLayerOptionsY_Regular  = 170# distance from bottom edge
iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
iGlobeLayerOptionsWidth = 400
iGlobeLayerOptionHeight = 24

# STACK BAR
#####################
iStackBarHeight = 32


# MULTI LIST
#####################
iMultiListXL = 318
iMultiListXR = 332


# TOP CENTER TITLE
#####################
iCityCenterRow1X = 398
iCityCenterRow1Y = 78
iCityCenterRow2X = 398
iCityCenterRow2Y = 104

iCityCenterRow1Xa = 347
iCityCenterRow2Xa = 482


g_iNumTradeRoutes = 0
g_iNumBuildings = 0
g_iNumLeftBonus = 0
g_iNumCenterBonus = 0
g_iNumRightBonus = 0

g_szTimeText = ""

# BUG - NJAGC - start
g_bShowTimeTextAlt = False
g_iTimeTextCounter = -1
# BUG - NJAGC - end

# BUG - Raw Yields - start
import RawYields
g_bRawShowing = False
g_bYieldView, g_iYieldType = RawYields.getViewAndType(0)
g_iYieldTiles = RawYields.WORKED_TILES
RAW_YIELD_HELP = ( "TXT_KEY_RAW_YIELD_VIEW_TRADE",
				   "TXT_KEY_RAW_YIELD_VIEW_FOOD",
				   "TXT_KEY_RAW_YIELD_VIEW_PRODUCTION",
				   "TXT_KEY_RAW_YIELD_VIEW_COMMERCE",
				   "TXT_KEY_RAW_YIELD_TILES_WORKED",
				   "TXT_KEY_RAW_YIELD_TILES_CITY",
				   "TXT_KEY_RAW_YIELD_TILES_OWNED",
				   "TXT_KEY_RAW_YIELD_TILES_ALL" )
# BUG - Raw Yields - end

# 04/2021: lfgr fixes
RESEARCH_BAR_WIDTH = 487

# BUG - field of view slider - start
DEFAULT_FIELD_OF_VIEW = 42
# BUG - field of view slider - end

HELP_TEXT_MINIMUM_WIDTH = 300

g_pSelectedUnit = 0

#FfH: Added by Kael 07/17/2008
iHelpX = 120
#FfH: End Add

#CustomizableBars Start
# This value depends on the x resolution of the screen. It is obtained from the code that places the domestic advisor button and the rest.
xCoordCustomizableBars = 253
yCoordCustomizableBars = 57
widthCustomizableBars = 228
iSeparationCustomizableBars = 8
iMaxCustomizableBars = 4
#CustomizableBars End

# BUG - start
g_mainInterface = None
def onSwitchHotSeatPlayer(argsList):
	g_mainInterface.resetEndTurnObjects()
# BUG - end

class CvMainInterface:
	"Main Interface Screen"
	
	def __init__(self):
	
# BUG - start
		global g_mainInterface
		g_mainInterface = self
# BUG - end

# BUG - draw method
		self.DRAW_METHOD_PLE = "DRAW_METHOD_PLE"
		self.DRAW_METHOD_VAN = "DRAW_METHOD_VAN"
		self.DRAW_METHOD_BUG = "DRAW_METHOD_BUG"
		self.DRAW_METHODS = (self.DRAW_METHOD_PLE, 
							 self.DRAW_METHOD_VAN,
							 self.DRAW_METHOD_BUG)
#		self.sDrawMethod = self.DRAW_METHOD_PLE
# BUG - draw method


# BUG - PLE - start
		self.PLE = PLE.PLE()
#		self.PLE.PLE_initialize()
		
		self.MainInterfaceInputMap = {
			self.PLE.PLOT_LIST_BUTTON_NAME	: self.PLE.getPlotListButtonName,
			self.PLE.PLOT_LIST_MINUS_NAME	: self.PLE.getPlotListMinusName,
			self.PLE.PLOT_LIST_PLUS_NAME	: self.PLE.getPlotListPlusName,
			self.PLE.PLOT_LIST_UP_NAME		: self.PLE.getPlotListUpName,
			self.PLE.PLOT_LIST_DOWN_NAME 	: self.PLE.getPlotListDownName,
			
			"PleViewModeStyle1"				: self.PLE.onClickPLEViewMode,
			self.PLE.PLE_VIEW_MODE			: self.PLE.onClickPLEViewMode,
			self.PLE.PLE_MODE_STANDARD		: self.PLE.onClickPLEModeStandard,
			self.PLE.PLE_MODE_MULTILINE		: self.PLE.onClickPLEModeMultiline,
			self.PLE.PLE_MODE_STACK_VERT	: self.PLE.onClickPLEModeStackVert,
			self.PLE.PLE_MODE_STACK_HORIZ	: self.PLE.onClickPLEModeStackHoriz,
			
			self.PLE.PLOT_LIST_PROMO_NAME	: self.PLE.unitPromotion,
			self.PLE.PLOT_LIST_UPGRADE_NAME	: self.PLE.unitUpgrade,
			
			self.PLE.PLE_RESET_FILTERS		: self.PLE.onClickPLEResetFilters,
			self.PLE.PLE_FILTER_CANMOVE		: self.PLE.onClickPLEFilterCanMove,
			self.PLE.PLE_FILTER_CANTMOVE	: self.PLE.onClickPLEFilterCantMove,
			self.PLE.PLE_FILTER_NOTWOUND	: self.PLE.onClickPLEFilterNotWound,
			self.PLE.PLE_FILTER_WOUND		: self.PLE.onClickPLEFilterWound,
			self.PLE.PLE_FILTER_LAND		: self.PLE.onClickPLEFilterLand,
			self.PLE.PLE_FILTER_SEA			: self.PLE.onClickPLEFilterSea,
			self.PLE.PLE_FILTER_AIR			: self.PLE.onClickPLEFilterAir,
			self.PLE.PLE_FILTER_MIL			: self.PLE.onClickPLEFilterMil,
			self.PLE.PLE_FILTER_DOM			: self.PLE.onClickPLEFilterDom,
			self.PLE.PLE_FILTER_OWN			: self.PLE.onClickPLEFilterOwn,
			self.PLE.PLE_FILTER_FOREIGN		: self.PLE.onClickPLEFilterForeign,
			
			self.PLE.PLE_GRP_UNITTYPE		: self.PLE.onClickPLEGrpUnittype,
			self.PLE.PLE_GRP_GROUPS			: self.PLE.onClickPLEGrpGroups,
			self.PLE.PLE_GRP_PROMO			: self.PLE.onClickPLEGrpPromo,
			self.PLE.PLE_GRP_UPGRADE		: self.PLE.onClickPLEGrpUpgrade,
		}

#		self.iVisibleUnits 			= 0
		self.iMaxPlotListIcons 		= 0

		
		self.bPLECurrentlyShowing	= False
		self.bVanCurrentlyShowing	= False
# BUG - draw method
		self.bBUGCurrentlyShowing	= False
# BUG - draw method

		self.xResolution = 0
		self.yResolution = 0
# BUG - PLE - end

# BUG - field of view slider - start
		self.szSliderTextId = "FieldOfViewSliderText"
		self.sFieldOfView_Text = ""
		self.szSliderId = "FieldOfViewSlider"
		self.iField_View_Prev = -1
# BUG - field of view slider - end

# CCV - Position of Scores - START
		self.szScoreSliderTextId = "ScoreSliderText"
		self.sScrollingScoreboard_Text = ""
		self.szScoreSliderId = "ScoreSlider"
		self.iScrollingScoreboard_Prev = -1

		self.iScoreStart = 1
		self.iScoreStartMax = 1
# CCV - Position of Scores - END

		

############## Basic operational functions ###################

#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################

	def numPlotListButtonsPerRow(self):
		return self.m_iNumPlotListButtonsPerRow

# I know that this is redundent, but CyInterface().getPlotListOffset() (and prob the column one too)
# uses this function
# it is also used in "...\EntryPoints\CvScreensInterface.py" too
	def numPlotListButtons(self):
		# < Revolution Mod Start >
		# simply to stop annoying errors when reloading Python modules in game
		xResolution = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE ).getXResolution()
		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
		# < Revolution Mod End >
		return self.numPlotListButtonsPerRow()

	def numPlotListRows(self):
		return gc.getMAX_PLOT_LIST_ROWS()

	def numPlotListButtons_Total(self):
		return self.numPlotListButtonsPerRow() * self.numPlotListRows()

	def initState (self, screen=None):
		"""
		Initialize screen instance (self.foo) and global variables.
		
		This function is called before drawing the screen (from interfaceScreen() below)
		and anytime the Python modules are reloaded (from CvEventInterface).
		
		THIS FUNCTION MUST NOT ALTER THE SCREEN -- screen.foo()
		"""
		if screen is None:
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		self.xResolution = screen.getXResolution()
		self.yResolution = screen.getYResolution()
		
# BUG - Raw Yields - begin
		global g_bYieldView
		global g_iYieldType
		g_bYieldView, g_iYieldType = RawYields.getViewAndType(CityScreenOpt.getRawYieldsDefaultView())
# BUG - Raw Yields - end

# BUG - PLE - begin
		self.PLE.PLE_CalcConstants(screen)
# BUG - PLE - end

		# Set up our global variables...
		# < Revolution Mod Start >
		global iMaxScoreLines
		iMaxScoreLines = RevOpt.getMaxScoreLines()
		# < Revolution Mod End >		
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos
		
		g_NumEmphasizeInfos = gc.getNumEmphasizeInfos()
		g_NumCityTabTypes = CityTabTypes.NUM_CITYTAB_TYPES
		g_NumHurryInfos = gc.getNumHurryInfos()
		g_NumUnitClassInfos = gc.getNumUnitClassInfos()
		g_NumBuildingClassInfos = gc.getNumBuildingClassInfos()
		g_NumProjectInfos = gc.getNumProjectInfos()
		g_NumProcessInfos = gc.getNumProcessInfos()
		g_NumActionInfos = gc.getNumActionInfos()
		
# BUG - field of view slider - start
		iBtnY = 27
		self.iX_FoVSlider = self.xResolution - 120
		self.iY_FoVSlider = iBtnY + 30
		self.sFieldOfView_Text = localText.getText("TXT_KEY_BUG_OPT_MAININTERFACE__FIELDOFVIEW_TEXT", ())
		if MainOpt.isRememberFieldOfView():
			self.iField_View = int(MainOpt.getFieldOfView())
		else:
			self.iField_View = DEFAULT_FIELD_OF_VIEW
# BUG - field of view slider - end

# CCV - Position of Scores - START
		iBtnY = 27
		self.iX_ScoreSlider = self.xResolution - 120
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
			self.iY_ScoreSlider = screen.getYResolution() - 200
		else:
			self.iY_ScoreSlider = screen.getYResolution() - 82
		self.sScrollingScoreboard_Text = localText.getText("TXT_KEY_CCV_MAININTERFACE__POSITIONOFSCORES_TEXT", ())
		self.iScore_View = self.iScoreStart
# CCV - Position of Scores - END

# BUG - Progress Bar - Tick Marks - start
		xCoord = 268 + (self.xResolution - 1024) / 2
		self.pBarResearchBar_n = ProgressBarUtil.ProgressBar("ResearchBar-Canvas", xCoord, 2, RESEARCH_BAR_WIDTH, iStackBarHeight, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"), ProgressBarUtil.TICK_MARKS, True)
		self.pBarResearchBar_n.addBarItem("ResearchBar")
		self.pBarResearchBar_n.addBarItem("ResearchText")
# BUG - Progress Bar - Tick Marks - end
		
# BUG - Progress Bar - Tick Marks - start
		xCoord = 268 + (self.xResolution - 1440) / 2
		xCoord += 6 + 84
		self.pBarResearchBar_w = ProgressBarUtil.ProgressBar("ResearchBar-w-Canvas", xCoord, 2, RESEARCH_BAR_WIDTH, iStackBarHeight, gc.getInfoTypeForString("COLOR_RESEARCH_RATE"), ProgressBarUtil.TICK_MARKS, True)
		self.pBarResearchBar_w.addBarItem("ResearchBar-w")
		self.pBarResearchBar_w.addBarItem("ResearchText")
# BUG - Progress Bar - Tick Marks - end

# BUG - Progress Bar - Tick Marks - start
		self.pBarPopulationBar = ProgressBarUtil.ProgressBar("PopulationBar-Canvas", iCityCenterRow1X, iCityCenterRow1Y-4, self.xResolution - (iCityCenterRow1X*2), iStackBarHeight, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), ProgressBarUtil.SOLID_MARKS, True)
		self.pBarPopulationBar.addBarItem("PopulationBar")
		self.pBarPopulationBar.addBarItem("PopulationText")
		self.pBarProductionBar = ProgressBarUtil.ProgressBar("ProductionBar-Canvas", iCityCenterRow2X, iCityCenterRow2Y-4, self.xResolution - (iCityCenterRow2X*2), iStackBarHeight, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), ProgressBarUtil.TICK_MARKS, True)
		self.pBarProductionBar.addBarItem("ProductionBar")
		self.pBarProductionBar.addBarItem("ProductionText")
		self.pBarProductionBar_Whip = ProgressBarUtil.ProgressBar("ProductionBar-Whip-Canvas", iCityCenterRow2X, iCityCenterRow2Y-4, self.xResolution - (iCityCenterRow2X*2), iStackBarHeight, gc.getInfoTypeForString("COLOR_YELLOW"), ProgressBarUtil.CENTER_MARKS, False)
		self.pBarProductionBar_Whip.addBarItem("ProductionBar")
		self.pBarProductionBar_Whip.addBarItem("ProductionText")
# BUG - Progress Bar - Tick Marks - end

		self.m_iNumPlotListButtonsPerRow = (self.xResolution - (iMultiListXL+iMultiListXR) - 68) / 34

# BUG - BUG unit plot draw method - start
# bug unit panel
		self.BupPanel = BugUnitPlot.BupPanel(screen, screen.getXResolution(), screen.getYResolution(), iMultiListXL+iMultiListXR, self.numPlotListButtonsPerRow(), self.numPlotListRows())
# BUG - BUG unit plot draw method - end

	def interfaceScreen (self):
		"""
		Draw all of the screen elements.
		
		This function is called once after starting or loading a game.
		
		THIS FUNCTION MUST NOT CREATE ANY INSTANCE OR GLOBAL VARIABLES.
		It may alter existing ones created in __init__() or initState(), however.
		"""
		if ( CyGame().isPitbossHost() ):
			return
		
		# This is the main interface screen, create it as such
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		self.initState(screen)
		screen.setForcedRedraw(True)
		screen.setDimensions(0, 0, self.xResolution, self.yResolution)
		
		# to avoid changing all the code below
		xResolution = self.xResolution
		yResolution = self.yResolution
		
		# Help Text Area
#FfH: Modified by Kael 07/17/2008
#		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
#FfH: End Modify

		# Center Left
		screen.addPanel( "InterfaceCenterLeftBackgroundWidget", u"", u"", True, False, 0, 0, 250, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterLeftBackgroundWidget", "Panel_City_Left_Style" )
		screen.hide( "InterfaceCenterLeftBackgroundWidget" )

		# Top Left
		screen.addPanel( "InterfaceTopLeftBackgroundWidget", u"", u"", True, False, 258, 0, xResolution - 516, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceTopLeftBackgroundWidget", "Panel_City_Top_Style" )
		screen.hide( "InterfaceTopLeftBackgroundWidget" )

		# Center Right
		screen.addPanel( "InterfaceCenterRightBackgroundWidget", u"", u"", True, False, xResolution - 258, 0, 258, yResolution-149, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "InterfaceCenterRightBackgroundWidget", "Panel_City_Right_Style" )
		screen.hide( "InterfaceCenterRightBackgroundWidget" )
		
		screen.addPanel( "CityScreenAdjustPanel", u"", u"", True, False, 10, 44, 238, 105, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityScreenAdjustPanel", "Panel_City_Info_Style" )
		screen.hide( "CityScreenAdjustPanel" )
		
		screen.addPanel( "TopCityPanelLeft", u"", u"", True, False, 260, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelLeft", "Panel_City_TanTL_Style" )
		screen.hide( "TopCityPanelLeft" )
		
		screen.addPanel( "TopCityPanelRight", u"", u"", True, False, xResolution/2, 70, xResolution/2-260, 60, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TopCityPanelRight", "Panel_City_TanTR_Style" )
		screen.hide( "TopCityPanelRight" )
		
		# Top Bar

		# SF CHANGE
		screen.addPanel( "CityScreenTopWidget", u"", u"", True, False, 0, -2, xResolution, 41, PanelStyles.PANEL_STYLE_STANDARD )

		screen.setStyle( "CityScreenTopWidget", "Panel_TopBar_Style" )
		screen.hide( "CityScreenTopWidget" )
		
		# Top Center Title
		screen.addPanel( "CityNameBackground", u"", u"", True, False, 260, 31, xResolution - (260*2), 38, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "CityNameBackground", "Panel_City_Title_Style" )
		screen.hide( "CityNameBackground" )

		# Left Background Widget
		screen.addDDSGFC( "InterfaceLeftBackgroundWidget", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOTTOM_LEFT").getPath(), 0, yResolution - 164, 304, 164, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Center Background Widget
		screen.addPanel( "InterfaceCenterBackgroundWidget", u"", u"", True, False, 296, yResolution - 133, xResolution - (296*2), 133, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceCenterBackgroundWidget", "Panel_Game_HudBC_Style" )
		screen.hide( "InterfaceCenterBackgroundWidget" )

		# Left Background Widget
		screen.addPanel( "InterfaceLeftBackgroundWidget", u"", u"", True, False, 0, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceLeftBackgroundWidget", "Panel_Game_HudBL_Style" )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		# Right Background Widget
		screen.addPanel( "InterfaceRightBackgroundWidget", u"", u"", True, False, xResolution - 304, yResolution - 168, 304, 168, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceRightBackgroundWidget", "Panel_Game_HudBR_Style" )
		screen.hide( "InterfaceRightBackgroundWidget" )
	
		# Top Center Background

		# SF CHANGE
		screen.addPanel( "InterfaceTopCenter", u"", u"", True, False, 257, -2, xResolution-(257*2), 48, PanelStyles.PANEL_STYLE_STANDARD)

		screen.setStyle( "InterfaceTopCenter", "Panel_Game_HudTC_Style" )
		screen.hide( "InterfaceTopCenter" )

		# Top Left Background
		screen.addPanel( "InterfaceTopLeft", u"", u"", True, False, 0, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopLeft", "Panel_Game_HudTL_Style" )
		screen.hide( "InterfaceTopLeft" )

		# Top Right Background
		screen.addPanel( "InterfaceTopRight", u"", u"", True, False, xResolution - 267, -2, 267, 60, PanelStyles.PANEL_STYLE_STANDARD)
		screen.setStyle( "InterfaceTopRight", "Panel_Game_HudTR_Style" )
		screen.hide( "InterfaceTopRight" )

		# FFH Mana - Mana Button
		screen.setImageButton("RawManaButton1", "Art/Interface/Screens/RawManaButton.dds", MANA_X_POS + 12, MANA_Y_POS + 407, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "RawManaButton1" )
		screen.addPanel( "ManaToggleHelpTextPanel", u"", u"", True, True, MANA_X_POS + 55, MANA_Y_POS + 407, 170, 30, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ManaToggleHelpTextPanel" )
#		szText = "<font=2>" + localText.getText("[COLOR_HIGHLIGHT_TEXT]Toggle Manabar Display[COLOR_REVERT]", ()) + "</font=2>"
		szText = "<font=2>" + localText.getText("TXT_KEY_MANA_TOGGLE_HELP", ()) + "</font=2>"
		screen.addMultilineText( "ManaToggleHelpText", szText, MANA_X_POS + 57, MANA_Y_POS + 411, 167, 27, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.hide( "ManaToggleHelpText" )
		# End FFH

		# RevolutionDCM start - LEFT BUTTONS START POSTION CHANGE			   2/03/08			JOHNY SMITH
		iBtnWidth = 28
		iBtnAdvance = 25
		iBtnY = 27
		iBtnX = 100
		
		
		# RevolutionDCM end - LOG BUTTON CHANGE			11/30/07			JOHNY SMITH
		# Turn log Button
		screen.setImageButton( "TurnLogButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
		screen.setStyle( "TurnLogButton", "Button_HUDLog_Style" )
		screen.hide( "TurnLogButton" )

		# MOVE VICTORY AND INFO ADVISOR BUTTONS			2/03/08			JOHNY SMITH
		iBtnX += iBtnAdvance
		screen.setImageButton( "VictoryAdvisorButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "VictoryAdvisorButton", "Button_HUDAdvisorVictory_Style" )
		screen.hide( "VictoryAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "InfoAdvisorButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1 )
		screen.setStyle( "InfoAdvisorButton", "Button_HUDAdvisorRecord_Style" )
		screen.hide( "InfoAdvisorButton" )
		# END  											2/03/08			JOHNY SMITH 
		
#FfH: Added by Kael 09/24/2008 - Trophy Button
		iBtnX += iBtnAdvance
		screen.setImageButton( "TrophyButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TROPHY).getActionInfoIndex(), -1 )
		screen.setStyle( "TrophyButton", "Button_HUDTrophy_Style" )
		screen.hide( "TrophyButton" )
#FfH: End Add

		# < Revolution Mod Start >
		if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) ):
			iBtnX += iBtnAdvance
			
			# Appears name must have a one at the end to register mouseover events ...
			screen.setImageButton("RevWatchButton1", "Art/Interface/Buttons/revbtn.dds", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setStyle( "RevWatchButton1", "Button_HUDSmall_Style" )
			screen.hide( "RevWatchButton1" )
		# < Revolution Mod End >
		
		# RIGHT BUTTONS START POSITION CHANGE			   4/06/09			Glider1
		iBtnX = xResolution - 225 - iBtnWidth
		# END
		
		# Advisor Buttons...
		screen.setImageButton( "DomesticAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "DomesticAdvisorButton", "Button_HUDAdvisorDomestic_Style" )
		screen.hide( "DomesticAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "FinanceAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FINANCIAL_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "FinanceAdvisorButton", "Button_HUDAdvisorFinance_Style" )
		screen.hide( "FinanceAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "CivicsAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVICS_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CivicsAdvisorButton", "Button_HUDAdvisorCivics_Style" )
		screen.hide( "CivicsAdvisorButton" )
		
		iBtnX += iBtnAdvance 
		screen.setImageButton( "ForeignAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ForeignAdvisorButton", "Button_HUDAdvisorForeign_Style" )
		screen.hide( "ForeignAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "MilitaryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "MilitaryAdvisorButton", "Button_HUDAdvisorMilitary_Style" )
		screen.hide( "MilitaryAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "TechAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1 )
		screen.setStyle( "TechAdvisorButton", "Button_HUDAdvisorTechnology_Style" )
		screen.hide( "TechAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "ReligiousAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RELIGION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ReligiousAdvisorButton", "Button_HUDAdvisorReligious_Style" )
		screen.hide( "ReligiousAdvisorButton" )
		
		iBtnX += iBtnAdvance
		screen.setImageButton( "CorporationAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CORPORATION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CorporationAdvisorButton", "Button_HUDAdvisorCorporation_Style" )
		screen.hide( "CorporationAdvisorButton" )
		

#FfH: Modified by Kael 07/25/2008
#		if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE):
#			iBtnX += iBtnAdvance
#			screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
#			screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
#			screen.hide( "EspionageAdvisorButton" )
		iBtnX += iBtnAdvance
		screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
		screen.hide( "EspionageAdvisorButton" )
#FfH: End Modify

# BUG - field of view slider - start
		self.setFieldofView_Text(screen)
		iW = 100
		iH = 15
		screen.addSlider(self.szSliderId, self.iX_FoVSlider + 5, self.iY_FoVSlider, iW, iH, self.iField_View - 1, 0, 100 - 1, WidgetTypes.WIDGET_GENERAL, -1, -1, False);
		screen.hide(self.szSliderTextId)
		screen.hide(self.szSliderId)
# BUG - field of view slider - end

# CCV - Position of Scores - START
		self.setScrollingScoreboard_Text(screen)
		iW = 100
		iH = 15
		screen.addSlider(self.szScoreSliderId, self.iX_ScoreSlider + 5, self.iY_ScoreSlider, iW, iH, self.iScore_View - 1, 0, self.iScoreStartMax - 1, WidgetTypes.WIDGET_GENERAL, -1, -1, False);
		screen.hide(self.szScoreSliderTextId)
		screen.hide(self.szScoreSliderId)
# CCV - Position of Scores - END

		# City Tabs
		iBtnX = xResolution - 324
		iBtnY = yResolution - 94
		iBtnWidth = 24
		iBtnAdvance = 24

		screen.setButtonGFC( "CityTab0", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab0", "Button_HUDJumpUnit_Style" )
		screen.hide( "CityTab0" )

		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab1", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab1", "Button_HUDJumpBuilding_Style" )
		screen.hide( "CityTab1" )
		
		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab2", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 2, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab2", "Button_HUDJumpWonder_Style" )
		screen.hide( "CityTab2" )
		
		# Minimap initialization
		screen.setMainInterface(True)
		
		screen.addPanel( "MiniMapPanel", u"", u"", True, False, xResolution - 214, yResolution - 151, 208, 151, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "MiniMapPanel", "Panel_Game_HudMap_Style" )
		screen.hide( "MiniMapPanel" )

		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )
		gc.getMap().updateMinimapColor()

		self.createMinimapButtons()
	
		# START - MOVE CIVILOPEDIA AND OPTIONS BUTTONS			2/03/08			JOHNY SMITH  
		# Help button (always visible)
		screen.setImageButton( "InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), 227, 2, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1 )
		screen.hide( "InterfaceHelpButton" )

		screen.setImageButton( "MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), xResolution - 28, 2, 24, 24, WidgetTypes.WIDGET_MENU_ICON, -1, -1 )
		screen.hide( "MainMenuButton" )

		# END  											2/03/08			JOHNY SMITH 

		# Globeview buttons
		self.createGlobeviewButtons( )

		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )		
		screen.hide( "BottomButtonContainer" )

		# *********************************************************************************
		# PLOT LIST BUTTONS
		# *********************************************************************************

# BUG - PLE - begin
		for j in range(self.numPlotListRows()):
			yRow = (j - self.numPlotListRows() + 1) * 34
			yPixel = yResolution - 169 + yRow - 3
			xPixel = 315 - 3
			xWidth = self.numPlotListButtonsPerRow() * 34 + 3
			yHeight = 32 + 3

			szStringPanel = "PlotListPanel" + str(j)
			screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

			for i in range(self.numPlotListButtonsPerRow()):
				k = j * self.numPlotListButtonsPerRow() + i

				xOffset = i * 34
				szString = "PlotListButton" + str(k)

# BUG - plot list - start
				szFileNamePromo = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_FRAME").getPath()
				szStringPromoFrame  = szString + "PromoFrame"
				screen.addDDSGFCAt( szStringPromoFrame , szStringPanel, szFileNamePromo, xOffset +  2,  2, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringPromoFrame  )
# BUG - plot list - end

				screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
				screen.hide( szString )

				szStringHealth = szString + "Health"
				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 26, 32, 11, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
				screen.hide( szStringHealth )

				szStringIcon = szString + "Icon"
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
				screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringIcon )

		self.PLE.preparePlotListObjects(screen)
# BUG - PLE - end


		# End Turn Text
		screen.setLabel( "EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - 188, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "EndTurnText", HitTestTypes.HITTEST_NOHIT )

		# Three states for end turn button...
		screen.addDDSGFC( "ACIcon", 'Art/Interface/Screens/armageddon.dds', xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_END_TURN, -1, -1 )
		screen.hide( "ACIcon" )
		screen.setImageButton( "EndTurnButton", "", xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_END_TURN, -1, -1 )
		screen.setStyle( "EndTurnButton", "Button_HUDEndTurn_Style" )
		screen.setEndTurnState( "EndTurnButton", "Red" )
		screen.hide( "EndTurnButton" )

		# *********************************************************************************
		# RESEARCH BUTTONS
		# *********************************************************************************

		i = 0
		for i in range( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.setImageButton( szName, gc.getTechInfo(i).getButton(), 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, i, -1 )
			screen.hide( szName )

		i = 0
		for i in range(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
				szButton = gc.getReligionInfo(i).getGenericTechButton()
			else:
				szButton = gc.getReligionInfo(i).getTechButton()
			screen.setImageButton( szName, szButton, 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, gc.getReligionInfo(i).getTechPrereq(), -1 )
			screen.hide( szName )
		
		# *********************************************************************************
		# CITIZEN BUTTONS
		# *********************************************************************************

		szHideCitizenList = []

		# Angry Citizens
		i = 0
		for i in range(MAX_CITIZEN_BUTTONS):
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - 74 - (26 * i), yResolution - 238, 24, 24, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.hide( szName )
			
		iCount = 0

		# Increase Specialists...
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "IncreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 46, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Decrease specialists
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
			if (gc.getSpecialistInfo(i).isVisible()):
				szName = "DecreaseSpecialist" + str(i)
				screen.setButtonGFC( szName, u"", "", xResolution - 24, (yResolution - 270 - (26 * iCount)), 20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.hide( szName )

				iCount = iCount + 1

		iCount = 0

		# Citizen Buttons
		i = 0
		for i in range( gc.getNumSpecialistInfos() ):
		
			if (gc.getSpecialistInfo(i).isVisible()):
			
				szName = "CitizenDisabledButton" + str(i)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), xResolution - 74, (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_DISABLED_CITIZEN, i, -1 )
				screen.enable( szName, False )
				screen.hide( szName )

				for j in range(MAX_CITIZEN_BUTTONS):
					szName = "CitizenButton" + str((i * 100) + j)
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.hide( szName )

# BUG - city specialist - start
		screen.addPanel( "SpecialistBackground", u"", u"", True, False, xResolution - 243, yResolution - 423, 230, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SpecialistBackground", "Panel_City_Header_Style" )
		screen.hide( "SpecialistBackground" )
		screen.setLabel( "SpecialistLabel", "Background", localText.getText("TXT_KEY_CONCEPT_SPECIALISTS", ()), CvUtil.FONT_CENTER_JUSTIFY, xResolution - 128, yResolution - 415, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "SpecialistLabel" )
# BUG - city specialist - end

		# **********************************************************
		# GAME DATA STRINGS
		# **********************************************************

		szGameDataList = []

		xCoord = 268 + (xResolution - 1024) / 2
		self.xResearchBar = xCoord
		screen.addStackedBarGFC( "ResearchBar", self.xResearchBar, 2, RESEARCH_BAR_WIDTH, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar" )

# BUG - Great General Bar - start
		screen.addStackedBarGFC( "GreatGeneralBar", xCoord, 27, 100, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") ) #gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatGeneralBar" )
# BUG - Great General Bar - end

# BUG - Great Person Bar - start
		xCoord += 7 + 100
		screen.addStackedBarGFC( "GreatPersonBar", xCoord, 27, 380, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GP_PROGRESS_BAR, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar" )
# BUG - Great Person Bar - end

# BUG - Bars on single line for higher resolution screens - start
		xCoord = 268 + (xResolution - 1440) / 2
		screen.addStackedBarGFC( "GreatGeneralBar-w", xCoord, 2, 84, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") ) #gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatGeneralBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatGeneralBar-w" )

		xCoord += 6 + 84
		self.xResearchBarWide = xCoord
		screen.addStackedBarGFC( "ResearchBar-w", self.xResearchBarWide, 2, RESEARCH_BAR_WIDTH, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar-w" )

		xCoord += 6 + RESEARCH_BAR_WIDTH
		screen.addStackedBarGFC( "GreatPersonBar-w", xCoord, 2, 320, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GP_PROGRESS_BAR, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar-w", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar-w" )
# BUG - Bars on single line for higher resolution screens - end

		
		# *********************************************************************************
		# SELECTION DATA BUTTONS/STRINGS
		# *********************************************************************************

		szHideSelectionDataList = []

		screen.addStackedBarGFC( "PopulationBar", iCityCenterRow1X, iCityCenterRow1Y-4, xResolution - (iCityCenterRow1X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColorsAlpha( "PopulationBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), 0.8 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "PopulationBar" )

		screen.addStackedBarGFC( "ProductionBar", iCityCenterRow2X, iCityCenterRow2Y-4, xResolution - (iCityCenterRow2X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_PRODUCTION, -1, -1 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType() )
		screen.setStackedBarColorsAlpha( "ProductionBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), 0.8 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ProductionBar" )

		screen.addStackedBarGFC( "GreatPeopleBar", xResolution - 246, yResolution - 188, 240, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPeopleBar" )

		screen.addStackedBarGFC( "CultureBar", 6, yResolution - 188, 240, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_CULTURE, -1, -1 )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CULTURE_STORED") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "CultureBar" )

		# Holy City Overlay
		for i in range( gc.getNumReligionInfos() ):
			xCoord = xResolution - 242 + (i * 34)
			yCoord = 42
			szName = "ReligionHolyCityDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
			screen.hide( szName )

		for i in range( gc.getNumCorporationInfos() ):
			xCoord = xResolution - 242 + (i * 34)
			yCoord = 66
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
			screen.hide( szName )

		screen.addStackedBarGFC( "NationalityBar", 6, yResolution - 214, 240, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_NATIONALITY, -1, -1 )
		screen.hide( "NationalityBar" )

# < Revolution Mod Start >
		screen.addStackedBarGFC( "RevStatusBar1", 6, yResolution - 240, 240, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "RevStatusBar1" )

		# This button is invisible, only exists to provide mouseover popup info for RevStatusBar1
		screen.setImageButton("RevStatusButton1", "", 16, yResolution - 240, 220, iStackBarHeight, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "RevStatusButton1" )
		self.hideRevStatusInfoPane()
# < Revolution Mod End >

		screen.setButtonGFC( "CityScrollMinus", u"", "", 274, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "CityScrollMinus" )

		screen.setButtonGFC( "CityScrollPlus", u"", "", 288, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "CityScrollPlus" )
		
# BUG - City Arrows - start
		screen.setButtonGFC( "MainCityScrollMinus", u"", "", xResolution - 275, yResolution - 165, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "MainCityScrollMinus" )

		screen.setButtonGFC( "MainCityScrollPlus", u"", "", xResolution - 255, yResolution - 165, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end

# BUG - PLE - begin
		screen.setButtonGFC( "PlotListMinus", u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "PlotListMinus" )

		screen.setButtonGFC( "PlotListPlus", u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "PlotListPlus" )

		screen.setButtonGFC( self.PLE.PLOT_LIST_MINUS_NAME, u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( self.PLE.PLOT_LIST_MINUS_NAME )
		screen.setButtonGFC( self.PLE.PLOT_LIST_PLUS_NAME, u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( self.PLE.PLOT_LIST_PLUS_NAME )

		screen.setImageButton( self.PLE.PLOT_LIST_UP_NAME, ArtFileMgr.getInterfaceArtInfo("PLE_ARROW_UP").getPath(), 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( self.PLE.PLOT_LIST_UP_NAME )
		screen.setImageButton( self.PLE.PLOT_LIST_DOWN_NAME, ArtFileMgr.getInterfaceArtInfo("PLE_ARROW_DOWN").getPath(), 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ) + 5, yResolution - 171 + 5, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( self.PLE.PLOT_LIST_DOWN_NAME )
# BUG - PLE - end

		screen.addPanel( "TradeRouteListBackground", u"", u"", True, False, 10, 157, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "TradeRouteListBackground", "Panel_City_Header_Style" )
		screen.hide( "TradeRouteListBackground" )

		screen.setLabel( "TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 165, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "TradeRouteListLabel" )
		
# BUG - Raw Yields - start
		nX = 10 + 24
		nY = 157 + 5
		nSize = 24
		nDist = 24
		nGap = 10
		szHighlightButton = ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_HIGHLIGHT").getPath()
		
		# Trade
		screen.addCheckBoxGFC( "RawYieldsTrade0", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_TRADE").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 0, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsTrade0")
		
		# Yields
		nX += nDist + nGap
		screen.addCheckBoxGFC( "RawYieldsFood1", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_FOOD").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsFood1")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsProduction2", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_PRODUCTION").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 2, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsProduction2")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsCommerce3", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_COMMERCE").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 3, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsCommerce3")
		
		# Tile Selection
		nX += nDist + nGap
		screen.addCheckBoxGFC( "RawYieldsWorkedTiles4", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_WORKED_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 4, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsWorkedTiles4")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsCityTiles5", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_CITY_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 5, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsCityTiles5")
		nX += nDist
		screen.addCheckBoxGFC( "RawYieldsOwnedTiles6", ArtFileMgr.getInterfaceArtInfo("RAW_YIELDS_OWNED_TILES").getPath(), szHighlightButton, nX, nY, nSize, nSize, WidgetTypes.WIDGET_GENERAL, 6, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.hide("RawYieldsOwnedTiles6")
# BUG - Raw Yields - end

# BUG - BUG Option Button - Start
		iBtnWidth	= 28
		iBtnY = 27
		iBtnX = 27+2*iBtnAdvance

		sBUGOptionsScreenButton = ArtFileMgr.getInterfaceArtInfo("BUG_OPTIONS_SCREEN_BUTTON").getPath()
		screen.setImageButton("BUGOptionsScreenWidget", sBUGOptionsScreenButton,  iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_BUG_OPTION_SCREEN, -1, -1)
		screen.hide("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End

		screen.addPanel( "BuildingListBackground", u"", u"", True, False, 10, 287, 238, 30, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "BuildingListBackground", "Panel_City_Header_Style" )
		screen.hide( "BuildingListBackground" )

		screen.setLabel( "BuildingListLabel", "Background", localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 295, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "BuildingListLabel" )

		# *********************************************************************************
		# UNIT INFO ELEMENTS
		# *********************************************************************************

		i = 0
		szCircleArt = ArtFileMgr.getInterfaceArtInfo("WHITE_CIRCLE_40").getPath()
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.addDDSGFC( szName, gc.getPromotionInfo(i).getButton(), 180, yResolution - 18, 24, 24, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, i, -1 )
			screen.hide( szName )
# BUG - Stack Promotions - start
			szName = "PromotionButtonCircle" + str(i)
			x, y = self.calculatePromotionButtonPosition(screen, i)
			screen.addDDSGFC( szName, szCircleArt, x + 10, y + 10, 16, 16, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, i, -1 )
			screen.hide( szName )
# BUG - Stack Promotions - end

# BUG - PLE - begin
			szName = self.PLE.PLE_PROMO_BUTTONS_UNITINFO + str(i)
			screen.addDDSGFC( szName, gc.getPromotionInfo(i).getButton(), \
								180, yResolution - 18, \
								self.PLE.CFG_INFOPANE_BUTTON_SIZE, self.PLE.CFG_INFOPANE_BUTTON_SIZE, \
								WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(i).getActionInfoIndex(), -1 )
			screen.hide( szName )
# BUG - PLE - end
			
		# *********************************************************************************
		# SCORES
		# *********************************************************************************
		
		screen.addPanel( "ScoreBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ScoreBackground" )

#FfH: Added by Kael 10/29/2007
		screen.addPanel( "ManaBackground", u"", u"", True, False, 0, -150, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ManaBackground" )
#FfH: End Add

		for i in range( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, i, -1 )
			screen.hide( szName )

		# < Revolution Mod Start >
		szName = "ScoreTextSeparator1"
		screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( szName )

		szName = "ExtraCivSeparator1"
		screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( szName )
		# < Revolution Mod End >

		# This should be a forced redraw screen
		screen.setForcedRedraw( True )
		
		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		
		szHideList = []
		
		szHideList.append( "CreateGroup" )
		szHideList.append( "DeleteGroup" )

		# City Tabs
		for i in range( g_NumCityTabTypes ):
			szButtonID = "CityTab" + str(i)
			szHideList.append( szButtonID )
					
		for i in range( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			szHideList.append( szButtonID )

		szHideList.append( "Hurry0" )
		szHideList.append( "Hurry1" )
		
		screen.registerHideList( szHideList, len(szHideList), 0 )

#CustomizableBars Start
		for i in range (iMaxCustomizableBars):
			szBarName = "CustomizableBar" + str(i)
			yCoord = yCoordCustomizableBars + (iSeparationCustomizableBars + iStackBarHeight) * i
			screen.addStackedBarGFC( szBarName, self.xResolution - xCoordCustomizableBars, yCoord, widthCustomizableBars, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setStackedBarColors( szBarName, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
			screen.setStackedBarColors( szBarName, InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
			screen.setStackedBarColors( szBarName, InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
			screen.setStackedBarColors( szBarName, InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
			screen.hide( szBarName )
#CustomizableBars End

		return 0

	# lfgr 04/2021: Helper function
	def isResearchBarWide( self ) :
		# type: () -> bool
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		return screen.getXResolution() >= 1440 and ( MainOpt.isShowGGProgressBar() or MainOpt.isShowGPProgressBar() )

	# Will update the screen (every 250 MS)
	def updateScreen(self):
		
		global g_szTimeText
		global g_iTimeTextCounter

# BUG - Options - start
		BugOptions.write()
# BUG - Options - end
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
#		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34
		
		# This should recreate the minimap on load games and returns if already exists -JW
		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )

		messageControl = CyMessageControl()
		
		bShow = False
		
		# Hide all interface widgets		
		#screen.hide( "EndTurnText" )

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			if (gc.getGame().isPaused()):
				# Pause overrides other messages
				acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
				#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
				screen.setEndTurnState( "EndTurnText", acOutput )
				bShow = True
			elif (messageControl.GetFirstBadConnection() != -1):
				# Waiting on a bad connection to resolve
				if (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
			else:
				# Flash select messages if no popups are present
				if ( CyInterface().shouldDisplayReturn() ):
					acOutput = localText.getText("SYSTEM_RETURN", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingOthers() ):
					acOutput = localText.getText("SYSTEM_WAITING", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayEndTurn() ):
# BUG - Reminders - start
					if ( ReminderEventManager.g_turnReminderTexts ):
						acOutput = u"%s" % ReminderEventManager.g_turnReminderTexts
					else:
						acOutput = localText.getText("SYSTEM_END_TURN", ())
# BUG - Reminders - end
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingYou() ):
					acOutput = localText.getText("SYSTEM_WAITING_FOR_YOU", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
# BUG - Options - start
				elif ( MainOpt.isShowOptionsKeyReminder() ):
					if BugPath.isMac():
						acOutput = localText.getText("TXT_KEY_BUG_OPTIONS_KEY_REMINDER_MAC", (BugPath.getModName(),))
					else:
						acOutput = localText.getText("TXT_KEY_BUG_OPTIONS_KEY_REMINDER", (BugPath.getModName(),))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
# BUG - Options - end

		if ( bShow ):
			screen.showEndTurn( "EndTurnText" )
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isCityScreenUp() ):
				screen.moveItem( "EndTurnText", 0, yResolution - 194, -0.1 )
			else:
				screen.moveItem( "EndTurnText", 0, yResolution - 86, -0.1 )
		else:
			screen.hideEndTurn( "EndTurnText" )

		screen.hide( "ACText" )
		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			iPlayer = gc.getGame().getActivePlayer()
			if iPlayer != -1:
				pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
				ACstr = u"<font=2i><color=%d,%d,%d,%d>%s</color></font>" %(pPlayer.getPlayerTextColorR(),pPlayer.getPlayerTextColorG(),pPlayer.getPlayerTextColorB(),pPlayer.getPlayerTextColorA(),str(CyGame().getGlobalCounter()) + str(" "))
				screen.setText( "ACText", "Background", ACstr, CvUtil.FONT_CENTER_JUSTIFY, xResolution - iEndOfTurnPosX, yResolution - 157, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "ACText", HitTestTypes.HITTEST_NOHIT )

			if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):	

				iHorizontalPosition = 270
				iVerticalPosition = 50

				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES') and pPlayer.getNumCities() > 0 and pPlayer.getMaxCities() != -1:
					iNumCities = pPlayer.getNumCities() - pPlayer.getNumSettlements()
					iMaxCities = pPlayer.getMaxCities()

					if iNumCities > 0 and iMaxCities > 0:
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iNumCities) + str(" / ") + str(iMaxCities) + str(" "))
						screen.setImageButton("KuriotateCities", "Art/Interface/Buttons/Spells/Promote Settlement.dds", iHorizontalPosition, iVerticalPosition, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "KurioText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, iHorizontalPosition + 12, iVerticalPosition + 2, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "KurioText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "KuriotateCities" )
						screen.hide( "KurioText" )

		self.updateEndTurnButton()

# BUG - NJAGC - start
		global g_bShowTimeTextAlt
		if (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			if (ClockOpt.isEnabled()):
				if (ClockOpt.isShowEra()):
					screen.show( "EraText" )
				else:
					screen.hide( "EraText" )
				
				if (ClockOpt.isAlternateTimeText()):
					#global g_iTimeTextCounter (already done above)
					if (CyUserProfile().wasClockJustTurnedOn() or g_iTimeTextCounter <= 0):
						# reset timer, display primary
						g_bShowTimeTextAlt = False
						g_iTimeTextCounter = ClockOpt.getAlternatePeriod() * 1000
						CyUserProfile().setClockJustTurnedOn(False)
					else:
						# countdown timer
						g_iTimeTextCounter -= 250
						if (g_iTimeTextCounter <= 0):
							# timer elapsed, toggle between primary and alternate
							g_iTimeTextCounter = ClockOpt.getAlternatePeriod() * 1000
							g_bShowTimeTextAlt = not g_bShowTimeTextAlt
				else:
					g_bShowTimeTextAlt = False
				
				self.updateTimeText()
				#MOVED YEAR TEXT TO THE RIGHT				2/03/08						 JOHNY SMITH
				screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 31, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				#END										 2/03/08						 JOHNY SMITH
				screen.show( "TimeText" )
			else:
				screen.hide( "EraText" )
				self.updateTimeText()
				#MOVED YEAR TEXT TO THE RIGHT				2/03/08						 JOHNY SMITH
				screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 31, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				#END										 2/03/08						 JOHNY SMITH
				screen.show( "TimeText" )
		else:
			screen.hide( "TimeText" )
			screen.hide( "EraText" )
# BUG - NJAGC - end

# BUG - PLE - start 			
		# this ensures that the info pane is closed after a greater mouse pos change
		self.PLE.checkInfoPane(CyInterface().getMousePos())
# BUG - PLE - end

		return 0

	# Will redraw the interface
	def redraw( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

# BUG - Field of View - start
		self.setFieldofView(screen, CyInterface().isCityScreenUp())
# BUG - Field of View - end

		# Check Dirty Bits, see what we need to redraw...
		if (CyInterface().isDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT) == True):
			# Percent Buttons
			self.updatePercentButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Flag_DIRTY_BIT) == True):
			# Percent Buttons
			self.updateFlag()
			CyInterface().setDirty(InterfaceDirtyBits.Flag_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT) == True ):
			# Miscellaneous buttons (civics screen, etc)
			self.updateMiscButtons()
			CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT) == True ):
			# Info Pane Dirty Bit
			# This must come before updatePlotListButtons so that the entity widget appears in front of the stats
			self.updateInfoPaneStrings()
			CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT) == True ):
			# Plot List Buttons Dirty
			self.updatePlotListButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT) == True ):
			# Selection Buttons Dirty
			self.updateSelectionButtons()
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT) == True ):
			# Research Buttons Dirty
			self.updateResearchButtons()
			CyInterface().setDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT) == True ):
			# Citizen Buttons Dirty

# BUG - city specialist - start
			self.updateCitizenButtons_hide()
			if (CityScreenOpt.isCitySpecialist_Stacker()):
				self.updateCitizenButtons_Stacker()
			elif (CityScreenOpt.isCitySpecialist_Chevron()):
				self.updateCitizenButtons_Chevron()
			else:
				self.updateCitizenButtons()
# BUG - city specialist - end
			
			CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT) == True ):
			# Game Data Strings Dirty
			self.updateGameDataStrings()
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT) == True ):
			# Help Dirty bit
			self.updateHelpStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT) == True ):
			# Selection Data Dirty Bit
			self.updateCityScreen()
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) == True or CyInterface().checkFlashUpdate() ):
			# Scores!
			self.updateScoreStrings()

#FfH: Added by Kael 04/30/2007
			self.updateManaStrings()
#FfH: End Add

			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT) == True ):
			# Globeview and Globelayer buttons
			CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
			self.updateGlobeviewButtons()

		return 0

	# Will update the percent buttons
	def updatePercentButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
			szString = "IncreasePercent" + str(iI)
			screen.hide( szString )
			szString = "DecreasePercent" + str(iI)
			screen.hide( szString )
# BUG - Min/Max Sliders - start
			szString = "MaxPercent" + str(iI)
			screen.hide( szString )
			szString = "MinPercent" + str(iI)
			screen.hide( szString )
# BUG - Min/Max Sliders - start

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if ( not CyInterface().isCityScreenUp() or ( pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() ) or gc.getGame().isDebugMode() ):
			iCount = 0

			if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
				for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
					# Intentional offset...
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
										
					if (gc.getActivePlayer().isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
# BUG - Min/Max Sliders - start
						bEnable = gc.getActivePlayer().isCommerceFlexible(eCommerce)
						if MainOpt.isShowMinMaxCommerceButtons() and not CyInterface().isCityScreenUp():
							iMinMaxAdjustX = 20
							szString = "MaxPercent" + str(eCommerce)
							screen.setButtonGFC( szString, u"", "", 125, 53 + (19 * iCount), 20, 20, 
												 *BugDll.widget("WIDGET_SET_PERCENT", eCommerce, 100, 
												 				WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, 100, 
												 				ButtonStyles.BUTTON_STYLE_CITY_PLUS) )
							screen.show( szString )
							screen.enable( szString, bEnable )
							szString = "MinPercent" + str(eCommerce)
							screen.setButtonGFC( szString, u"", "", 185, 53 + (19 * iCount), 20, 20, 
												 *BugDll.widget("WIDGET_SET_PERCENT", eCommerce, 0, 
												 				WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -100, 
												 				ButtonStyles.BUTTON_STYLE_CITY_MINUS) )
							screen.show( szString )
							screen.enable( szString, bEnable )
						else:
							iMinMaxAdjustX = 0
						
						szString = "IncreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString, u"", "", 125 + iMinMaxAdjustX, 53 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_PLUS )
						screen.show( szString )
						screen.enable( szString, bEnable )
						szString = "DecreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString, u"", "", 145 + iMinMaxAdjustX, 53 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_CHANGE_PERCENT, eCommerce, -gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"), ButtonStyles.BUTTON_STYLE_CITY_MINUS )
						screen.show( szString )
						screen.enable( szString, bEnable )

						iCount = iCount + 1
						# moved enabling above
# BUG - Min/Max Sliders - end
						
		return 0

# BUG - start
	def resetEndTurnObjects(self):
		"""
		Clears the end turn text and hides it and the button.
		"""
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.setEndTurnState( "EndTurnText", u"" )
		screen.hideEndTurn( "EndTurnText" )
		screen.hideEndTurn( "EndTurnButton" )
# BUG - end

	# Will update the end Turn Button
	def updateEndTurnButton( self ):

		global g_eEndTurnButtonState
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
		
			eState = CyInterface().getEndTurnState()
			
			bShow = False
			
			if ( eState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_OVER_DARK ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_GO ):
				screen.setEndTurnState( "EndTurnButton", u"Green" )
				bShow = True
			
			if ( bShow ):
				screen.showEndTurn( "EndTurnButton" )
			else:
				screen.hideEndTurn( "EndTurnButton" )
			
			if ( g_eEndTurnButtonState == eState ):
				return
				
			g_eEndTurnButtonState = eState
			
		else:
			screen.hideEndTurn( "EndTurnButton" )

		# return 0

	# Update the miscellaneous buttons
	def updateMiscButtons( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		xResolution = screen.getXResolution()
#CustomizableBars Start
		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			self.updateCustomizableBars(screen)
#CustomizableBars End

# BUG - Great Person Bar - start
		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			self.updateGreatPersonBar(screen)
# BUG - Great Person Bar - end

		if ( CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.show( "CivilizationFlag" )
			screen.show( "InterfaceHelpButton" )
			screen.show( "MainMenuButton" )
		else:
			screen.hide( "CivilizationFlag" )
			screen.hide( "InterfaceHelpButton" )
			screen.hide( "MainMenuButton" )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			screen.hide( "RawManaButton1" )
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "ACIcon" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.hide( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )

#FfH: Added by Kael 09/24/2008
			screen.hide( "TrophyButton" )
#FfH: End Add

			screen.hide( "EspionageAdvisorButton" )
			# < Revolution Mod Start >
			screen.hide( "RevWatchButton1" )
			# < Revolution Mod End >
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - BUG Option Button - Start
			screen.hide("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End
# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

# CCV - Position of Scores - START
			screen.hide(self.szScoreSliderTextId)
			screen.hide(self.szScoreSliderId)
# CCV - Position of Scores - END
		elif ( CyInterface().isCityScreenUp() ):
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.hide( "RawManaButton1" )
			screen.hide( "ACIcon" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )

#FfH: Added by Kael 09/24/2008
			screen.hide( "TrophyButton" )
#FfH: End Add

			screen.hide( "EspionageAdvisorButton" )
			# < Revolution Mod Start >
			screen.hide( "RevWatchButton1" )
			# < Revolution Mod End >
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - BUG Option Button - Start
			screen.hide("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End
# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

# CCV - Position of Scores - START
			screen.hide(self.szScoreSliderTextId)
			screen.hide(self.szScoreSliderId)
# CCV - Position of Scores - END

		elif ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE):
			screen.hide( "RawManaButton1" )
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			# FFH Start
			screen.hide( "RawManaButton1" )
			screen.hide( "ACIcon" )
			# FFH End
			screen.hide( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )

#FfH: Added by Kael 09/24/2008
			screen.show( "TrophyButton" )
#FfH: End Add

			screen.show( "EspionageAdvisorButton" )
			# < Revolution Mod Start >
			if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) : screen.show( "RevWatchButton1" )
			# < Revolution Mod Start >
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - BUG Option Button - Start
			screen.show("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End
# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

# CCV - Position of Scores - START
			screen.show(self.szScoreSliderTextId)
			screen.show(self.szScoreSliderId)
# CCV - Position of Scores - END

			screen.moveToFront( "TurnLogButton" )
			# < Revolution Mod Start >
			if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) : screen.moveToFront( "RevWatchButton1" )
			# < Revolution Mod Start >
			
#FfH: Added by Kael 09/24/2008
			screen.moveToFront( "TrophyButton" )
#FfH: End Add
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )

		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START):		
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.hide( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.hide( "InterfaceTopLeft" )
			screen.hide( "InterfaceTopCenter" )
			screen.hide( "InterfaceTopRight" )
			screen.hide( "TurnLogButton" )

#FfH: Added by Kael 09/24/2008
			screen.hide( "RawManaButton1" )
			screen.hide( "TrophyButton" )
#FfH: End Add

			screen.hide( "EspionageAdvisorButton" )
			# < Revolution Mod Start >
			screen.hide( "RevWatchButton1" )
			# < Revolution Mod Start >
			screen.hide( "DomesticAdvisorButton" )
			screen.hide( "ForeignAdvisorButton" )
			screen.hide( "TechAdvisorButton" )
			screen.hide( "CivicsAdvisorButton" )
			screen.hide( "ReligiousAdvisorButton" )
			screen.hide( "CorporationAdvisorButton" )
			screen.hide( "FinanceAdvisorButton" )
			screen.hide( "MilitaryAdvisorButton" )
			screen.hide( "VictoryAdvisorButton" )
			screen.hide( "InfoAdvisorButton" )
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - BUG Option Button - Start
			screen.hide("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End

		elif ( CyEngine().isGlobeviewUp() ):
			screen.hide( "InterfaceLeftBackgroundWidget" )
			screen.hide( "InterfaceTopBackgroundWidget" )
			screen.hide( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )

#FfH: Added by Kael 09/24/2008
			screen.hide( "RawManaButton1" )
			screen.show( "TrophyButton" )
#FfH: End Add

			screen.show( "EspionageAdvisorButton" )
			# < Revolution Mod Start >
			if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) : screen.show( "RevWatchButton1" )
			# < Revolution Mod Start >
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
#FfH: Added by Kael 09/24/2008
			screen.show( "TrophyButton" )
#FfH: End Add
# BUG - City Arrows - start
			screen.hide( "MainCityScrollMinus" )
			screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end		
# BUG - BUG Option Button - Start
			screen.show("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End
# BUG - field of view slider - start
			screen.hide(self.szSliderTextId)
			screen.hide(self.szSliderId)
# BUG - field of view slider - end

# CCV - Position of Scores - START
			screen.hide(self.szScoreSliderTextId)
			screen.hide(self.szScoreSliderId)
# CCV - Position of Scores - END

			screen.moveToFront( "TurnLogButton" )
			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
# BUG - BUG Option Button - Start
			screen.moveToFront("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End
# < Revolution Mod Start >
			if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) : screen.moveToFront( "RevWatchButton1" )
# < Revolution Mod Start >
		else:
			screen.show( "InterfaceLeftBackgroundWidget" )
			screen.show( "InterfaceTopBackgroundWidget" )
			screen.show( "InterfaceCenterBackgroundWidget" )
			screen.show( "InterfaceRightBackgroundWidget" )
			screen.show( "MiniMapPanel" )
			screen.show( "InterfaceTopLeft" )
			screen.show( "InterfaceTopCenter" )
			screen.show( "InterfaceTopRight" )
			screen.show( "TurnLogButton" )

#FfH: Added by Kael 09/24/2008
			screen.show( "RawManaButton1" )
			screen.show( "ACIcon" )
			screen.show( "TrophyButton" )
#FfH: End Add

			screen.show( "EspionageAdvisorButton" )
			# < Revolution Mod Start >
			if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) : screen.show( "RevWatchButton1" )
			# < Revolution Mod Start >
			screen.show( "DomesticAdvisorButton" )
			screen.show( "ForeignAdvisorButton" )
			screen.show( "TechAdvisorButton" )
			screen.show( "CivicsAdvisorButton" )
			screen.show( "ReligiousAdvisorButton" )
			screen.show( "CorporationAdvisorButton" )
			screen.show( "FinanceAdvisorButton" )
			screen.show( "MilitaryAdvisorButton" )
			screen.show( "VictoryAdvisorButton" )
			screen.show( "InfoAdvisorButton" )
# BUG - City Arrows - start
			if (MainOpt.isShowCityCycleArrows()):
				screen.show( "MainCityScrollMinus" )
				screen.show( "MainCityScrollPlus" )
			else:
				screen.hide( "MainCityScrollMinus" )
				screen.hide( "MainCityScrollPlus" )
# BUG - City Arrows - end
# BUG - BUG Option Button - Start
			screen.show("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End
# BUG - field of view slider - start
			if (MainOpt.isShowFieldOfView()):
				screen.show(self.szSliderTextId)
				screen.show(self.szSliderId)
			else:
				screen.hide(self.szSliderTextId)
				screen.hide(self.szSliderId)
# BUG - field of view slider - end

# CCV - Position of Scores - START
			if (self.checkScrollingScoreboard() == True):							
				screen.show(self.szScoreSliderTextId)
				screen.show(self.szScoreSliderId)
			else:
				screen.hide(self.szScoreSliderTextId)
				screen.hide(self.szScoreSliderId)								
# CCV - Position of Scores - END

			screen.moveToFront( "TurnLogButton" )

#FfH: Added by Kael 09/24/2008
			screen.moveToFront( "TrophyButton" )
#FfH: End Add

			screen.moveToFront( "EspionageAdvisorButton" )
			screen.moveToFront( "DomesticAdvisorButton" )
			screen.moveToFront( "ForeignAdvisorButton" )
			screen.moveToFront( "TechAdvisorButton" )
			screen.moveToFront( "CivicsAdvisorButton" )
			screen.moveToFront( "ReligiousAdvisorButton" )
			screen.moveToFront( "CorporationAdvisorButton" )
			screen.moveToFront( "FinanceAdvisorButton" )
			screen.moveToFront( "MilitaryAdvisorButton" )
			screen.moveToFront( "VictoryAdvisorButton" )
			screen.moveToFront( "InfoAdvisorButton" )
# BUG - BUG Option Button - Start
			screen.moveToFront("BUGOptionsScreenWidget")
# BUG - BUG Option Button - End
# < Revolution Mod Start >
			if( not game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) : screen.moveToFront( "RevWatchButton1" )
# < Revolution Mod Start >
		screen.updateMinimapVisibility()

		return 0

	# Update plot List Buttons
	def updatePlotListButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		self.updatePlotListButtons_Hide(screen)

		self.updatePlotListButtons_Common(screen)

# BUG - draw methods
		sDrawMethod = self.DRAW_METHODS[PleOpt.getDrawMethod()]
		if sDrawMethod == self.DRAW_METHOD_PLE:
			self.PLE.updatePlotListButtons_PLE(screen, self.xResolution, self.yResolution)
			self.bPLECurrentlyShowing = True
		elif sDrawMethod == self.DRAW_METHOD_VAN:
			self.updatePlotListButtons_Orig(screen)
			self.bVanCurrentlyShowing = True
		else:  # self.DRAW_METHOD_BUG
			self.updatePlotListButtons_BUG(screen)
			self.bBUGCurrentlyShowing = True
# BUG - draw methods

#		BugUtil.debug("updatePlotListButtons end - %s %s %s", self.bVanCurrentlyShowing, self.bPLECurrentlyShowing, self.bBUGCurrentlyShowing)
		return 0

#		if PleOpt.isPLE_Style():
#			self.updatePlotListButtons_PLE(screen)
#			self.bPLECurrentlyShowing = True
#		else:
#			self.updatePlotListButtons_Orig(screen)
#			self.bVanCurrentlyShowing = True
#		return 0

	def updatePlotListButtons_Hide( self, screen ):
#		BugUtil.debug("updatePlotListButtons_Hide - %s %s %s", self.bVanCurrentlyShowing, self.bPLECurrentlyShowing, self.bBUGCurrentlyShowing)

		# hide all buttons
		if self.bPLECurrentlyShowing:
#			BugUtil.debug("updatePlotListButtons_Hide - hiding PLE")
			self.PLE.hidePlotListButtonPLEObjects(screen)
			self.PLE.hideUnitInfoPane()
			self.bPLECurrentlyShowing = False

		if self.bVanCurrentlyShowing:
#			BugUtil.debug("updatePlotListButtons_Hide - hiding Vanilla")
			self.hidePlotListButton_Orig(screen)
			self.bVanCurrentlyShowing = False

# BUG - BUG unit plot draw method - start
		if self.bBUGCurrentlyShowing:
#			BugUtil.debug("updatePlotListButtons_Hide - hiding BUG")
			self.hidePlotListButton_BUG(screen)
			self.bBUGCurrentlyShowing = False
# BUG - BUG unit plot draw method - end

	def updatePlotListButtons_Common( self, screen ):

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		# Capture these for looping over the plot's units
		self.PLE.UnitPlotList_BUGOptions()

		bHandled = False
		if ( CyInterface().shouldDisplayUnitModel() and not CyEngine().isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
			if ( CyInterface().isCitySelection() ):

				iOrders = CyInterface().getNumOrdersQueued()

				for i in range( iOrders ):
					if ( bHandled == False ):
						eOrderNodeType = CyInterface().getOrderNodeType(i)
						if (eOrderNodeType  == OrderTypes.ORDER_TRAIN ):
							screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 1, False )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CONSTRUCT ):
							screen.addBuildingGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.8, False )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CREATE ):
							if(gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).isSpaceship()):
								modelType = 0
								screen.addSpaceShipWidgetGFC("InterfaceUnitModel", 175, yResolution - 138, 123, 132, CyInterface().getOrderNodeData1(i), modelType, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
							else:
								screen.hide( "InterfaceUnitModel" )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_MAINTAIN ):
							screen.hide( "InterfaceUnitModel" )
							bHandled = True
													
				if ( not bHandled ):
					screen.hide( "InterfaceUnitModel" )
					bHandled = True

				screen.moveToFront("SelectedCityText")

			elif ( CyInterface().getHeadSelectedUnit() ):

#FfH: Modified by Kael 07/17/2008
#				screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
				screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), -20, yResolution - 350, 140, 198, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
#FfH: End Modify

#				screen.moveToFront("SelectedUnitText")
			else:
				screen.hide( "InterfaceUnitModel" )
		else:
			screen.hide( "InterfaceUnitModel" )

	# hides all plot list objects
	def hidePlotListButton_Orig(self, screen):
#		BugUtil.debug("hidePlotListButton_Orig - %i", self.numPlotListButtons_Total())
		# hides all unit button objects
		for i in range( self.numPlotListButtons_Total() ):
			szString = "PlotListButton" + str(i)
			screen.hide( szString )
			screen.hide( szString + "Icon" )
			screen.hide( szString + "Health" )
			screen.hide( szString + "MoveBar" )
			screen.hide( szString + "PromoFrame" )
			screen.hide( szString + "ActionIcon" )
			screen.hide( szString + "Upgrade" )

# BUG - draw method
	def hidePlotListButton_BUG(self, screen):
		if self.DRAW_METHODS[PleOpt.getDrawMethod()] != self.DRAW_METHOD_BUG:
			self.BupPanel.clearUnits()
			self.BupPanel.Hide()

		return
		# hides all unit button objects
#		for i in range( self.iMaxPlotListIcons ):
#			szString = "PlotListButton" + str(i)
#			screen.hide( szString )
#			screen.hide( szString + "Icon" )
#			screen.hide( szString + "Health" )
#			screen.hide( szString + "MoveBar" )
#			screen.hide( szString + "PromoFrame" )
#			screen.hide( szString + "ActionIcon" )
#			screen.hide( szString + "Upgrade" )
# BUG - draw method


	def updatePlotListButtons_Orig( self, screen ):

# need to put in something similar to 	def displayUnitPlotListObjects( self, screen, pLoopUnit, nRow, nCol ):

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pPlot = CyInterface().getSelectionPlot()

#		for i in range(gc.getNumPromotionInfos()):
#			szName = "PromotionButton" + str(i)
#			screen.moveToFront( szName )
# BUG - Stack Promotions - start
#		for i in range(gc.getNumPromotionInfos()):
#			szName = "PromotionButtonCircle" + str(i)
#			screen.moveToFront( szName )
#		for i in range(gc.getNumPromotionInfos()):
#			szName = "PromotionButtonCount" + str(i)
#			screen.moveToFront( szName )
# BUG - Stack Promotions - end

		screen.hide( "PlotListMinus" )
		screen.hide( "PlotListPlus" )

		BugUtil.debug("updatePlotListButtons_Orig - column %i, offset %i", CyInterface().getPlotListColumn(), CyInterface().getPlotListOffset())

		if ( pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):

			iVisibleUnits = CyInterface().getNumVisibleUnits()
			iCount = -(CyInterface().getPlotListColumn())

			bLeftArrow = False
			bRightArrow = False

			if (CyInterface().isCityScreenUp()):
				iMaxRows = 1
				iSkipped = (self.numPlotListRows() - 1) * self.numPlotListButtonsPerRow()
				iCount += iSkipped
			else:
				iMaxRows = self.numPlotListRows()
				iCount += CyInterface().getPlotListOffset()
				iSkipped = 0

			BugUtil.debug("updatePlotListButtons_Orig - iCount(%i), iSkipped(%i)", iCount, iSkipped)

			CyInterface().cacheInterfacePlotUnits(pPlot)
			for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
				pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
				if (pLoopUnit):

					if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
						bLeftArrow = True
					elif ((iCount == (self.numPlotListRows() * self.numPlotListButtonsPerRow() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
						bRightArrow = True

					if ((iCount >= 0) and (iCount <  self.numPlotListButtonsPerRow() * self.numPlotListRows())):
						if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()

						elif (pLoopUnit.canMove()):
							if (pLoopUnit.hasMoved()):
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
							else:
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
						else:
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

						szString = "PlotListButton" + str(iCount)
#						screen.changeImageButton( szString, gc.getUnitInfo(pLoopUnit.getUnitType()).getButton() )
						screen.changeImageButton( szString, pLoopUnit.getButton() )
						if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
							bEnable = True
						else:
							bEnable = False
						screen.enable(szString, bEnable)

						if (pLoopUnit.IsSelected()):
							screen.setState(szString, True)
						else:
							screen.setState(szString, False)
						screen.show( szString )

						# place the health bar
						if (pLoopUnit.isFighting()):
							bShowHealth = False
						elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
							bShowHealth = pLoopUnit.canAirAttack()
						else:
							bShowHealth = pLoopUnit.canFight()

						if bShowHealth:
							szStringHealth = szString + "Health"
							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
							if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
							elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
							else:
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
							screen.show( szStringHealth )

						# Adds the overlay first
						szStringIcon = szString + "Icon"
						screen.changeDDSGFC( szStringIcon, szFileName )
						screen.show( szStringIcon )

						if bEnable:
							x = 315 + ((iCount % self.numPlotListButtonsPerRow()) * 34)
							y = yResolution - 169 + (iCount / self.numPlotListButtonsPerRow() - self.numPlotListRows() + 1) * 34

							self.PLE._displayUnitPlotList_Dot( screen, pLoopUnit, szString, iCount, x, y + 4 )
							self.PLE._displayUnitPlotList_Promo( screen, pLoopUnit, szString )
							self.PLE._displayUnitPlotList_Upgrade( screen, pLoopUnit, szString, iCount, x, y )
							self.PLE._displayUnitPlotList_Mission( screen, pLoopUnit, szString, iCount, x, y - 22, 12)

					iCount = iCount + 1

#			BugUtil.debug("updatePlotListButtons_Orig - vis units(%i), buttons per row(%i), max rows(%i)", iVisibleUnits, self.numPlotListButtonsPerRow(), iMaxRows)
			if (iVisibleUnits > self.numPlotListButtonsPerRow() * iMaxRows):
#				BugUtil.debug("updatePlotListButtons_Orig - show arrows %s %s", bLeftArrow, bRightArrow)
				screen.enable("PlotListMinus", bLeftArrow)
				screen.show( "PlotListMinus" )

				screen.enable("PlotListPlus", bRightArrow)
				screen.show( "PlotListPlus" )

		return 0

# BUG - BUG unit plot draw method - start
	def updatePlotListButtons_BUG( self, screen ):

# need to put in something similar to 	def displayUnitPlotListObjects( self, screen, pLoopUnit, nRow, nCol ):

#		xResolution = screen.getXResolution()
#		yResolution = screen.getYResolution()

		pPlot = CyInterface().getSelectionPlot()

		# this moves the promotions for the unit shown in the
		# bottom left so that they sit on top of the unit picture
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.moveToFront( szName )
# BUG - Stack Promotions - start
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButtonCircle" + str(i)
			screen.moveToFront( szName )
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButtonCount" + str(i)
			screen.moveToFront( szName )
# BUG - Stack Promotions - end
		if (not pPlot
		or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL
		or CyEngine().isGlobeviewUp() == True):
			self.BupPanel.clearUnits()
			self.BupPanel.Hide()
			return 0
		self.BupPanel.addPlot(pPlot.getX(), pPlot.getY())

		CyInterface().cacheInterfacePlotUnits(pPlot)
		for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
			pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
			if (pLoopUnit):
				self.BupPanel.addUnit(pLoopUnit)

#		BugUtil.debug("updatePlotListButtons_BUG - C")

#		self.BupPanel.UpdateBUGOptions()

		timer = BugUtil.Timer("draw plot list")
		self.BupPanel.Draw()
		timer.log()
		return 0
		
	# This will update the flag widget for SP hotseat and dbeugging
	def updateFlag( self ):

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()

#FfH: Modified by Kael 07/17/2008
#			screen.addFlagWidgetGFC( "CivilizationFlag", xResolution - 288, yResolution - 138, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)
			screen.addFlagWidgetGFC( "CivilizationFlag", 0, -20, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)
#FfH: End Modify

	# Will hide and show the selection buttons and their associated buttons
	def updateSelectionButtons( self ):
	
		global SELECTION_BUTTON_COLUMNS
		global MAX_SELECTION_BUTTONS
		global g_pSelectedUnit

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos
		
		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
# BUG - Build/Action Icon Size - start
		if MainOpt.isBuildIconSizeLarge():
			screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113 + 18, xResolution - (iMultiListXL+iMultiListXR), 64, 4, 64, 64, TableStyles.TABLE_STYLE_STANDARD )
		elif MainOpt.isBuildIconSizeMedium():
			screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )
		else:
			screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 114, 4, 36, 36, TableStyles.TABLE_STYLE_STANDARD )
		# EF: minimum icon size for disabled buttons to work is 33 so these sizes won't fly
#		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 102, 4, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
#		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 104, 4, 24, 24, TableStyles.TABLE_STYLE_STANDARD )
# BUG - Build/Action Icon Size - end
		screen.clearMultiList( "BottomButtonContainer" )
		screen.hide( "BottomButtonContainer" )
		
		# All of the hides...	
		self.setMinimapButtonVisibility(False)

		screen.hideList( 0 )

		for i in range (g_NumEmphasizeInfos):
			szButtonID = "Emphasize" + str(i)
			screen.hide( szButtonID )

		# Hurry button show...
		for i in range( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			screen.hide( szButtonID )

		# Conscript Button Show
		screen.hide( "Conscript" )
		#screen.hide( "Liberate" )
		screen.hide( "AutomateProduction" )
		screen.hide( "AutomateCitizens" )

		if (not CyEngine().isGlobeviewUp() and pHeadSelectedCity):
		
			self.setMinimapButtonVisibility(True)

			if ((pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer()) or gc.getGame().isDebugMode()):
			
				iBtnX = xResolution - 284
				iBtnY = yResolution - 177
				iBtnW = 64
				iBtnH = 30

				# Liberate button
				#szText = "<font=1>" + localText.getText("TXT_KEY_LIBERATE_CITY", ()) + "</font>"
				#screen.setButtonGFC( "Liberate", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_LIBERATE_CITY, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				#screen.setStyle( "Liberate", "Button_CityT1_Style" )
				#screen.hide( "Liberate" )

				iBtnSX = xResolution - 284
				
				iBtnX = iBtnSX
				iBtnY = yResolution - 140
				iBtnW = 64
				iBtnH = 30

				# Conscript button
				szText = "<font=1>" + localText.getText("TXT_KEY_DRAFT", ()) + "</font>"
				screen.setButtonGFC( "Conscript", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_CONSCRIPT, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Conscript", "Button_CityT1_Style" )
				screen.hide( "Conscript" )

				iBtnY += iBtnH
				iBtnW = 32
				iBtnH = 28
				
				# Hurry Buttons		
				screen.setButtonGFC( "Hurry0", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry0", "Button_CityC1_Style" )
				screen.hide( "Hurry0" )

				iBtnX += iBtnW

				screen.setButtonGFC( "Hurry1", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry1", "Button_CityC2_Style" )
				screen.hide( "Hurry1" )
			
				iBtnX = iBtnSX
				iBtnY += iBtnH
			
				# Automate Production Button
				screen.addCheckBoxGFC( "AutomateProduction", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateProduction", "Button_CityC3_Style" )

				iBtnX += iBtnW

				# Automate Citizens Button
				screen.addCheckBoxGFC( "AutomateCitizens", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateCitizens", "Button_CityC4_Style" )

				iBtnY += iBtnH
				iBtnX = iBtnSX

				iBtnW	= 22
				iBtnWa	= 20
				iBtnH	= 24
				iBtnHa	= 27
			
				# Set Emphasize buttons
				i = 0
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				iBtnY += iBtnH
				
				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )
				
# FlavourMod: Added by Jean Elcard 09/03/2009 (growth control buttons)
				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", xResolution - 260 - iBtnWa, iCityCenterRow2Y, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", xResolution - 260 - iBtnWa, iCityCenterRow1Y, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i-1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )
# FlavourMod: End Add

				g_pSelectedUnit = 0
				screen.setState( "AutomateCitizens", pHeadSelectedCity.isCitizensAutomated() )
				screen.setState( "AutomateProduction", pHeadSelectedCity.isProductionAutomated() )
				
# FlavourMod: Added by Jean Elcard 09/03/2009 (growth control buttons)
				iNumCustomEmphasizeInfos = 2
# FlavourMod: End Add

				for i in range (g_NumEmphasizeInfos):
# FlavourMod: Added by Jean Elcard 09/03/2009 (growth control buttons)
# -> Don't show the buttons, if complete city screen isn't up.
					if (i < g_NumEmphasizeInfos - iNumCustomEmphasizeInfos) or CyInterface().isCityScreenUp():
# FlavourMod: End Add (block below indented)
						if not (pHeadSelectedCity.isSettlement()):
							szButtonID = "Emphasize" + str(i)
							screen.show( szButtonID )
							if ( pHeadSelectedCity.AI_isEmphasize(i) ):
								screen.setState( szButtonID, True )
							else:
								screen.setState( szButtonID, False )

				# City Tabs
				for i in range( g_NumCityTabTypes ):
					szButtonID = "CityTab" + str(i)
					screen.show( szButtonID )

				# Hurry button show...
				for i in range( g_NumHurryInfos ):
					szButtonID = "Hurry" + str(i)
					screen.show( szButtonID )
					screen.enable( szButtonID, pHeadSelectedCity.canHurry(i, False) )

				# Conscript Button Show
				screen.show( "Conscript" )
				if (pHeadSelectedCity.canConscript()):
					screen.enable( "Conscript", True )
				else:
					screen.enable( "Conscript", False )

				# Liberate Button Show
				#screen.show( "Liberate" )
				#if (-1 != pHeadSelectedCity.getLiberationPlayer()):
				#	screen.enable( "Liberate", True )
				#else:
				#	screen.enable( "Liberate", False )

				iCount = 0
				iRow = 0
				bFound = False

				# Units to construct
				for i in range ( g_NumUnitClassInfos ):
					eLoopUnit = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationUnits(i)
					
					if eLoopUnit == -1:
						eLoopUnit = gc.getCivilizationInfo(gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationType()).getCivilizationUnits(i)

#FfH: Added by Kael 10/05/2007
					if eLoopUnit != -1:
#FfH: End Add

						if (pHeadSelectedCity.canTrain(eLoopUnit, False, True)):
							szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)

#FfH: Added by Kael 02/06/2009
							iProm = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getDefaultRace()
							if iProm != -1:
								szButton = gc.getUnitInfo(eLoopUnit).getUnitStyleButton(iProm)
#FfH: End Add

							screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
							screen.show( "BottomButtonContainer" )
						
							if ( not pHeadSelectedCity.canTrain(eLoopUnit, False, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, szButton)
						
							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Buildings to construct
				for i in range ( g_NumBuildingClassInfos ):
					if (not isLimitedWonderClass(i)):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
						if (eLoopBuilding != BuildingTypes.NO_BUILDING):
							if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
								screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
								screen.show( "BottomButtonContainer" )
								
								if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
									screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )
	
								iCount = iCount + 1
								bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Wonders to construct
				i = 0
				for i in range( g_NumBuildingClassInfos ):
					if (isLimitedWonderClass(i)):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
						if (eLoopBuilding != BuildingTypes.NO_BUILDING):
							if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
								screen.appendMultiListButton( "BottomButtonContainer", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
								screen.show( "BottomButtonContainer" )
								
								if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
									screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )
	
								iCount = iCount + 1
								bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Projects
				i = 0
				for i in range( g_NumProjectInfos ):
					if (pHeadSelectedCity.canCreate(i, False, True)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProjectInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CREATE, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						if ( not pHeadSelectedCity.canCreate(i, False, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, gc.getProjectInfo(i).getButton() )
						
						iCount = iCount + 1
						bFound = True

				# Processes
				i = 0
				for i in range( g_NumProcessInfos ):
					if (pHeadSelectedCity.canMaintain(i, False)):
						screen.appendMultiListButton( "BottomButtonContainer", gc.getProcessInfo(i).getButton(), iRow, WidgetTypes.WIDGET_MAINTAIN, i, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1
						bFound = True

				screen.selectMultiList( "BottomButtonContainer", CyInterface().getCityTabSelectionRow() )
							
		elif (not CyEngine().isGlobeviewUp() and pHeadSelectedUnit and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

			self.setMinimapButtonVisibility(True)

			if (CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION):
			
				if ( pHeadSelectedUnit.getOwner() == gc.getGame().getActivePlayer() and g_pSelectedUnit != pHeadSelectedUnit ):
				
					g_pSelectedUnit = pHeadSelectedUnit
					
					iCount = 0

					actions = CyInterface().getActionsToShow()
					for i in actions:

#FfH: Modified by Kael 02/07/2009
#						screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
						szButton = gc.getActionInfo(i).getButton()
						if gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_UPGRADE:
							iProm = gc.getCivilizationInfo(gc.getPlayer(pHeadSelectedUnit.getOwner()).getCivilizationType()).getDefaultRace()
							if iProm != -1:
								szButton = gc.getUnitInfo(gc.getActionInfo(i).getCommandData()).getUnitStyleButton(iProm)
						screen.appendMultiListButton( "BottomButtonContainer", szButton, 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
#FfH: End Modify

						screen.show( "BottomButtonContainer" )
				
						if ( not CyInterface().canHandleAction(i, False) ):
							screen.disableMultiListButton( "BottomButtonContainer", 0, iCount, gc.getActionInfo(i).getButton() )
							
						if ( pHeadSelectedUnit.isActionRecommended(i) ):#or gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_PROMOTION ):
							screen.enableMultiListPulse( "BottomButtonContainer", True, 0, iCount )
						else:
							screen.enableMultiListPulse( "BottomButtonContainer", False, 0, iCount )

						iCount = iCount + 1

					if (CyInterface().canCreateGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), 0, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1

					if (CyInterface().canDeleteGroup()):
						screen.appendMultiListButton( "BottomButtonContainer", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), 0, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1, False )
						screen.show( "BottomButtonContainer" )
						
						iCount = iCount + 1

		elif (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
		
			self.setMinimapButtonVisibility(True)

		return 0
		
	# Will update the research buttons
	def updateResearchButtons( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for i in range( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.hide( szName )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		#screen.hide( "InterfaceOrnamentLeftLow" )
		#screen.hide( "InterfaceOrnamentRightLow" )
			
		for i in range(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().shouldShowResearchButtons() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			iCount = 0
			
			for i in range( gc.getNumTechInfos() ):
				if (gc.getActivePlayer().canResearch(i, False)):

#FfH: Modified by Karl 08/24/2007
#					if (iCount < 20):
					if (iCount < 30):
#FfH: End Modify

						szName = "ResearchButton" + str(i)

						bDone = False
						for j in range( gc.getNumReligionInfos() ):
							if ( not bDone ):
								if (gc.getReligionInfo(j).getTechPrereq() == i):
									if not (gc.getGame().isReligionSlotTaken(j)):
										szName = "ReligionButton" + str(j)
										bDone = True

						screen.show( szName )
						self.setResearchButtonPosition(szName, iCount)

					iCount = iCount + 1
					
		return 0
		
# BUG - city specialist - start
	def updateCitizenButtons_hide( self ):

		global MAX_CITIZEN_BUTTONS
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		for i in range( MAX_CITIZEN_BUTTONS ):
			szName = "FreeSpecialist" + str(i)
			screen.hide( szName )
			szName = "AngryCitizen" + str(i)
			screen.hide( szName )
			szName = "AngryCitizenChevron" + str(i)
			screen.hide( szName )

		for i in range( gc.getNumSpecialistInfos() ):
			szName = "IncreaseSpecialist" + str(i)
			screen.hide( szName )
			szName = "DecreaseSpecialist" + str(i)
			screen.hide( szName )
			szName = "CitizenDisabledButton" + str(i)
			screen.hide( szName )
			for j in range(MAX_CITIZEN_BUTTONS):
				szName = "CitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenChevron" + str((i * 100) + j)
				screen.hide( szName )

				szName = "IncresseCitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "IncresseCitizenBanner" + str((i * 100) + j)
				screen.hide( szName )
				szName = "DecresseCitizenButton" + str((i * 100) + j)
				screen.hide( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.hide( szName )

		global g_iSuperSpecialistCount
		global g_iCitySpecialistCount
		global g_iAngryCitizensCount

		screen.hide( "SpecialistBackground" )
		screen.hide( "SpecialistLabel" )

		for i in range( g_iSuperSpecialistCount ):
			szName = "FreeSpecialist" + str(i)
			screen.hide( szName )
		for i in range( g_iAngryCitizensCount ):
			szName = "AngryCitizen" + str(i)
			screen.hide( szName )

		for i in range( gc.getNumSpecialistInfos() ):
			for k in range( g_iCitySpecialistCount ):
				szName = "IncresseCitizenBanner" + str((i * 100) + k)					
				screen.hide( szName )
				szName = "IncresseCitizenButton" + str((i * 100) + k)					
				screen.hide( szName )
				szName = "DecresseCitizenButton" + str((i * 100) + k)					
				screen.hide( szName )

		return 0
# BUG - city specialist - end


	# Will update the citizen buttons
	def updateCitizenButtons( self ):

		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0
	
		global MAX_CITIZEN_BUTTONS
		
		bHandled = False
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( pHeadSelectedCity.angryPopulation(0) < MAX_CITIZEN_BUTTONS ):
			iCount = pHeadSelectedCity.angryPopulation(0)
		else:
			iCount = MAX_CITIZEN_BUTTONS

		for i in range(iCount):
			bHandled = True
			szName = "AngryCitizen" + str(i)
			screen.show( szName )

		iFreeSpecialistCount = 0
		for i in range(gc.getNumSpecialistInfos()):
			iFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistCount(i)

		iCount = 0

		bHandled = False
		
		if (iFreeSpecialistCount > MAX_CITIZEN_BUTTONS):
			for i in range(gc.getNumSpecialistInfos()):
				if (pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
						screen.show( szName )
						bHandled = true
					iCount += 1
					
		else:				
			for i in range(gc.getNumSpecialistInfos()):
				for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, -1 )
						screen.show( szName )
						bHandled = true

					iCount = iCount + 1

		for i in range( gc.getNumSpecialistInfos() ):
		
			bHandled = False

			if (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode()):
			
				if (pHeadSelectedCity.isCitizensAutomated()):
					iSpecialistCount = max(pHeadSelectedCity.getSpecialistCount(i), pHeadSelectedCity.getForceSpecialistCount(i))
				else:
					iSpecialistCount = pHeadSelectedCity.getSpecialistCount(i)
			
				if (pHeadSelectedCity.isSpecialistValid(i, 1) and (pHeadSelectedCity.isCitizensAutomated() or iSpecialistCount < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
					szName = "IncreaseSpecialist" + str(i)
					screen.show( szName )
					szName = "CitizenDisabledButton" + str(i)
					screen.show( szName )

				if iSpecialistCount > 0:
					szName = "CitizenDisabledButton" + str(i)
					screen.hide( szName )
					szName = "DecreaseSpecialist" + str(i)
					screen.show( szName )
					
			if (pHeadSelectedCity.getSpecialistCount(i) < MAX_CITIZEN_BUTTONS):
				iCount = pHeadSelectedCity.getSpecialistCount(i)
			else:
				iCount = MAX_CITIZEN_BUTTONS

			j = 0
			for j in range( iCount ):
				bHandled = True
				szName = "CitizenButton" + str((i * 100) + j)
				screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
				screen.show( szName )
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xResolution - 74 - (26 * j), (yResolution - 272 - (26 * i)), 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j )
				if ( pHeadSelectedCity.getForceSpecialistCount(i) > j ):
					screen.show( szName )
				else:
					screen.hide( szName )
				
			if ( not bHandled ):
				szName = "CitizenDisabledButton" + str(i)
				screen.show( szName )

		return 0

# BUG - city specialist - start
	def updateCitizenButtons_Stacker( self ):
	
		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0

		global g_iSuperSpecialistCount
		global g_iCitySpecialistCount
		global g_iAngryCitizensCount
		
		bHandled = False
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		currentAngryCitizenCount = pHeadSelectedCity.angryPopulation(0)
		
		if(currentAngryCitizenCount > 0):
			stackWidth = 220 / currentAngryCitizenCount
			if (stackWidth > MAX_SPECIALIST_BUTTON_SPACING):
				stackWidth = MAX_SPECIALIST_BUTTON_SPACING

		for i in range(currentAngryCitizenCount):
			bHandled = True
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - SPECIALIST_AREA_MARGIN - (stackWidth * i), yResolution - (282- SPECIALIST_ROW_HEIGHT), 30, 30, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.show( szName )
			
		# update the max ever citizen counts
		if g_iAngryCitizensCount < currentAngryCitizenCount:
			g_iAngryCitizensCount = currentAngryCitizenCount

		iCount = 0
		bHandled = False
		currentSuperSpecialistCount = 0

		for i in range(gc.getNumSpecialistInfos()):
			if(pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
				currentSuperSpecialistCount = currentSuperSpecialistCount + pHeadSelectedCity.getFreeSpecialistCount(i)

		if(currentSuperSpecialistCount > 0):
			stackWidth = 220 / currentSuperSpecialistCount 
			if (stackWidth > MAX_SPECIALIST_BUTTON_SPACING):
				stackWidth = MAX_SPECIALIST_BUTTON_SPACING

		for i in range(gc.getNumSpecialistInfos()):
			for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):

				szName = "FreeSpecialist" + str(iCount)
				screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - SPECIALIST_AREA_MARGIN  - (stackWidth * iCount)), yResolution - (282 - SPECIALIST_ROW_HEIGHT * 2), 30, 30, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
				screen.show( szName )
				bHandled = true

				iCount = iCount + 1

		# update the max ever citizen counts
		if g_iSuperSpecialistCount < iCount:
			g_iSuperSpecialistCount = iCount

		iXShiftVal = 0
		iYShiftVal = 0
		iSpecialistCount = 0

		for i in range( gc.getNumSpecialistInfos() ):
		
			bHandled = False
			if( iSpecialistCount > SPECIALIST_ROWS ):
				iXShiftVal = 115
				iYShiftVal = (iSpecialistCount % SPECIALIST_ROWS) + 1
			else:
				iYShiftVal = iSpecialistCount

			if (gc.getSpecialistInfo(i).isVisible()):
				iSpecialistCount = iSpecialistCount + 1					
				
			if (gc.getPlayer(pHeadSelectedCity.getOwner()).isSpecialistValid(i) or i == 0):
				iCount = (pHeadSelectedCity.getPopulation() - pHeadSelectedCity.angryPopulation(0)) +  pHeadSelectedCity.totalFreeSpecialists()
			else:
				iCount = pHeadSelectedCity.getMaxSpecialistCount(i)

			# update the max ever citizen counts
			if g_iCitySpecialistCount < iCount:
				g_iCitySpecialistCount = iCount

			RowLength = 110
			if (i == 0):
			#if (i == gc.getInfoTypeForString(gc.getDefineSTRING("DEFAULT_SPECIALIST"))):
				RowLength *= 2
			
			HorizontalSpacing = MAX_SPECIALIST_BUTTON_SPACING	
			if (iCount > 0):
				HorizontalSpacing = RowLength / iCount
			if (HorizontalSpacing > MAX_SPECIALIST_BUTTON_SPACING):
				HorizontalSpacing = MAX_SPECIALIST_BUTTON_SPACING
									
			for k in range (iCount):
				if (k  >= pHeadSelectedCity.getSpecialistCount(i)):
					szName = "IncresseCitizenBanner" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.enable( szName, False )
					screen.show( szName )
					
					szName = "IncresseCitizenButton" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, "", "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1, ButtonStyles.BUTTON_STYLE_LABEL )					
					screen.show( szName )

				else:
					szName = "DecresseCitizenButton" + str((i * 100) + k)					
					screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xResolution - (SPECIALIST_AREA_MARGIN + iXShiftVal) - (HorizontalSpacing * k), (yResolution - 282 - (SPECIALIST_ROW_HEIGHT * iYShiftVal)), 30, 30, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
					screen.show( szName )
					
		screen.show( "SpecialistBackground" )
		screen.show( "SpecialistLabel" )
	
		return 0
# BUG - city specialist - end

# BUG - city specialist - start
	def updateCitizenButtons_Chevron( self ):
	
		if not CyInterface().isCityScreenUp(): return 0

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		if not (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW): return 0

		global MAX_CITIZEN_BUTTONS
		
		bHandled = False
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()


		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		iCount = pHeadSelectedCity.angryPopulation(0)

		j = 0
		while (iCount > 0):
			bHandled = True
			szName = "AngryCitizen" + str(j)
			screen.show( szName )

			xCoord = xResolution - 74 - (26 * j)
			yCoord = yResolution - 238

			szName = "AngryCitizenChevron" + str(j)
			if iCount >= 20:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON20").getPath()
				iCount -= 20
			elif iCount >= 10:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON10").getPath()
				iCount -= 10
			elif iCount >= 5:
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON5").getPath()
				iCount -= 5
			else:
				szFileName = ""
				iCount -= 1

			if (szFileName != ""):
				screen.addDDSGFC( szName , szFileName, xCoord, yCoord, 10, 10, WidgetTypes.WIDGET_CITIZEN, j, False )
				screen.show( szName )

			j += 1

		iFreeSpecialistCount = 0
		for i in range(gc.getNumSpecialistInfos()):
			iFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistCount(i)

		iCount = 0

		bHandled = False
		
		if (iFreeSpecialistCount > MAX_CITIZEN_BUTTONS):
			for i in range(gc.getNumSpecialistInfos()):
				if (pHeadSelectedCity.getFreeSpecialistCount(i) > 0):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, 1 )
						screen.show( szName )
						bHandled = True
					iCount += 1
					
		else:				
			for i in range(gc.getNumSpecialistInfos()):
				for j in range( pHeadSelectedCity.getFreeSpecialistCount(i) ):
					if (iCount < MAX_CITIZEN_BUTTONS):
						szName = "FreeSpecialist" + str(iCount)
						screen.setImageButton( szName, gc.getSpecialistInfo(i).getTexture(), (xResolution - 74  - (26 * iCount)), yResolution - 214, 24, 24, WidgetTypes.WIDGET_FREE_CITIZEN, i, -1 )
						screen.show( szName )
						bHandled = True

					iCount = iCount + 1

		for i in range( gc.getNumSpecialistInfos() ):
		
			bHandled = False

			if (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode()):
			
				if (pHeadSelectedCity.isCitizensAutomated()):
					iSpecialistCount = max(pHeadSelectedCity.getSpecialistCount(i), pHeadSelectedCity.getForceSpecialistCount(i))
				else:
					iSpecialistCount = pHeadSelectedCity.getSpecialistCount(i)
			
				if (pHeadSelectedCity.isSpecialistValid(i, 1) and (pHeadSelectedCity.isCitizensAutomated() or iSpecialistCount < (pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
					szName = "IncreaseSpecialist" + str(i)
					screen.show( szName )
					szName = "CitizenDisabledButton" + str(i)
					screen.show( szName )

				if iSpecialistCount > 0:
					szName = "CitizenDisabledButton" + str(i)
					screen.hide( szName )
					szName = "DecreaseSpecialist" + str(i)
					screen.show( szName )
					
			iCount = pHeadSelectedCity.getSpecialistCount(i)

			j = 0
			while (iCount > 0):
				bHandled = True

				xCoord = xResolution - 74 - (26 * j)
				yCoord = yResolution - 272 - (26 * i)

				szName = "CitizenButton" + str((i * 100) + j)
				screen.addCheckBoxGFC( szName, gc.getSpecialistInfo(i).getTexture(), "", xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL )
				screen.show( szName )

				szName = "CitizenChevron" + str((i * 100) + j)
				if iCount >= 20:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON20").getPath()
					iCount -= 20
				elif iCount >= 10:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON10").getPath()
					iCount -= 10
				elif iCount >= 5:
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_CHEVRON5").getPath()
					iCount -= 5
				else:
					szFileName = ""
					iCount -= 1

				if (szFileName != ""):
					screen.addDDSGFC( szName , szFileName, xCoord, yCoord, 10, 10, WidgetTypes.WIDGET_CITIZEN, i, False )
					screen.show( szName )

				j += 1

			if ( not bHandled ):
				szName = "CitizenDisabledButton" + str(i)
				screen.show( szName )

		return 0
# BUG - city specialist - end

	# Will update the game data strings
	def updateGameDataStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "ResearchText" )
		screen.hide( "GoldText" )
		screen.hide( "TimeText" )
		screen.hide( "ResearchBar" )

# BUG - NJAGC - start
		screen.hide( "EraText" )
# BUG - NJAGC - end

# BUG - Great Person Bar - start
		screen.hide( "GreatPersonBar" )
		screen.hide( "GreatPersonBarText" )
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
		screen.hide( "GreatGeneralBar" )
		screen.hide( "GreatGeneralBarText" )
# BUG - Great General Bar - end

# BUG - Bars on single line for higher resolution screens - start
		screen.hide( "GreatGeneralBar-w" )
		screen.hide( "ResearchBar-w" )
		screen.hide( "GreatPersonBar-w" )
# BUG - Bars on single line for higher resolution screens - end

# BUG - Progress Bar - Tick Marks - start
		self.pBarResearchBar_n.hide(screen)
		self.pBarResearchBar_w.hide(screen)
# BUG - Progress Bar - Tick Marks - end

#CustomizableBars Start
		for i in range (iMaxCustomizableBars):
			screen.hide( "CustomizableBar" + str(i) )
			screen.hide( "CustomizableBarText" + str(i) )
#CustomizableBars Start


		bShift = CyInterface().shiftKey()
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (pHeadSelectedCity):
			ePlayer = pHeadSelectedCity.getOwner()
		else:
			ePlayer = gc.getGame().getActivePlayer()

		if ( ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS() ):
			return 0

		for iI in range(CommerceTypes.NUM_COMMERCE_TYPES):
			szString = "PercentText" + str(iI)
			screen.hide(szString)
			szString = "RateText" + str(iI)
			screen.hide(szString)

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):

			# Percent of commerce
			if (gc.getPlayer(ePlayer).isAlive()):
				iCount = 0
				for iI in range( CommerceTypes.NUM_COMMERCE_TYPES ):
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
					if (gc.getPlayer(ePlayer).isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						szOutText = u"<font=2>%c:%d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), gc.getPlayer(ePlayer).getCommercePercent(eCommerce))
						szString = "PercentText" + str(iI)
						screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 69, 53 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( szString )

						if not CyInterface().isCityScreenUp():
							# ExtraModMod technology propagation START
							#if eCommerce == CommerceTypes.COMMERCE_RESEARCH:
								#iCommerceRate = gc.getPlayer(ePlayer).calculateBaseNetResearch()
							#else:
								#iCommerceRate = gc.getPlayer(ePlayer).getCommerceRate(CommerceTypes(eCommerce))
							# Technology propagation not shown because of http://forums.civfanatics.com/showthread.php?p=13578251#post13578251
							iCommerceRate = gc.getPlayer(ePlayer).getCommerceRate(CommerceTypes(eCommerce))
							# ExtraModMod technology propagation END
							szOutText = u"<font=2>" + localText.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (iCommerceRate, )) + u"</font>"
							szString = "RateText" + str(iI)
# BUG - Min/Max Sliders - start
							if MainOpt.isShowMinMaxCommerceButtons():
								iMinMaxAdjustX = 40
							else:
								iMinMaxAdjustX = 0
							screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 163 + iMinMaxAdjustX, 53 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
# BUG - Min/Max Sliders - end
							screen.show( szString )

						iCount = iCount + 1;

			self.updateTimeText()
			#MOVED YEAR TEXT TO THE RIGHT				2/03/08						 JOHNY SMITH
			screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 31, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			#END										 2/03/08						 JOHNY SMITH
			screen.show( "TimeText" )
			
			if (gc.getPlayer(ePlayer).isAlive()):
				
# BUG - Gold Rate Warning - start
				if MainOpt.isGoldRateWarning():
					pPlayer = gc.getPlayer(ePlayer)
					iGold = pPlayer.getGold()
					iGoldRate = pPlayer.calculateGoldRate()
					if iGold < 0:
						szText = BugUtil.getText("TXT_KEY_MISC_NEG_GOLD", iGold)
						if iGoldRate != 0:
							if iGold + iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", iGoldRate)
							elif iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_POS_WARNING_GOLD_PER_TURN", iGoldRate)
							else:
								szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", iGoldRate)
					else:
						szText = BugUtil.getText("TXT_KEY_MISC_POS_GOLD", iGold)
						if iGoldRate != 0:
							if iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", iGoldRate)
							elif iGold + iGoldRate >= 0:
								szText += BugUtil.getText("TXT_KEY_MISC_NEG_WARNING_GOLD_PER_TURN", iGoldRate)
							else:
								szText += BugUtil.getText("TXT_KEY_MISC_NEG_GOLD_PER_TURN", iGoldRate)
					if pPlayer.isStrike():
						szText += BugUtil.getPlainText("TXT_KEY_MISC_STRIKE")
				else:
					szText = CyGameTextMgr().getGoldStr(ePlayer)
# BUG - Gold Rate Warning - end

#FfH: Added by Kael 12/08/2007
				if gc.getPlayer(ePlayer).getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KHAZAD') \
						and gc.getPlayer(ePlayer).getNumCities() > 0 \
						and ffhUIOpt.isShowKhazadVaultText() : # lfgr 04/2021
					# LFGR_TODO: Don't hardcode here, use FfHDefines
					iGold = gc.getPlayer(ePlayer).getGold() / gc.getPlayer(ePlayer).getNumCities()
					if iGold <= 24 :
						szText = szText + " " + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_EMPTY", ())
					if (iGold >= 25 and iGold <= 49) :
						szText = szText + " " + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_LOW", ())
					if (iGold >= 75 and iGold <= 99) :
						szText = szText + " " + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_STOCKED", ())
					if (iGold >= 100 and iGold <= 149) :
						szText = szText + " " + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_ABUNDANT", ())
					if (iGold >= 150 and iGold <= 249) :
						szText = szText + " " + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_FULL", ())
					if iGold >= 250 :
						szText = szText + " " + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_OVERFLOWING", ())
#FfH: End Add
				#MOVED AMOUNT OF GOLD TEXT							   2/03/08					 JOHNY SMITH
				# lfgr 04/2021: Changed widget type to show Khazad vault tooltip
				screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 80, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PLAYER_GOLD, -1, -1 )
				#END													 2/03/08					 JOHNY SMITH
				screen.show( "GoldText" )
				
				if (((gc.getPlayer(ePlayer).calculateGoldRate() != 0) and not (gc.getPlayer(ePlayer).isAnarchy())) or (gc.getPlayer(ePlayer).getGold() != 0)):
					screen.show( "GoldText" )

# BUG - NJAGC - start
				if ClockOpt.isEnabled() and ClockOpt.isShowEra() :
					szText = localText.getText("TXT_KEY_BUG_ERA", (gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentRealEra()).getDescription(), ))
					if(ClockOpt.isUseEraColor()):
						iEraColor = ClockOpt.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentRealEra()).getType())
						if (iEraColor >= 0):
							szText = localText.changeTextColor(szText, iEraColor)
					screen.setLabel( "EraText", "Background", szText, CvUtil.FONT_RIGHT_JUSTIFY, 250, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( "EraText" )
# BUG - NJAGC - end
				
				if (gc.getPlayer(ePlayer).isAnarchy()):
				
# BUG - Bars on single line for higher resolution screens - start
					if (xResolution >= 1440
					and (MainOpt.isShowGGProgressBar() or MainOpt.isShowGPProgressBar())):
						xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 / 2
					else:
						xCoord = screen.centerX(512)

					yCoord = 5  # Ruff: this use to be 3 but I changed it so it lines up with the Great Person Bar
					szText = localText.getText("INTERFACE_ANARCHY", (gc.getPlayer(ePlayer).getAnarchyTurns(), ))
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
# BUG - Bars on single line for higher resolution screens - end

					if ( gc.getPlayer(ePlayer).getCurrentResearch() != -1 ):
						screen.show( "ResearchText" )
					else:
						screen.hide( "ResearchText" )
					
				elif (gc.getPlayer(ePlayer).getCurrentResearch() != -1):

					szText = CyGameTextMgr().getResearchStr(ePlayer)

# BUG - Bars on single line for higher resolution screens - start
					if self.isResearchBarWide() :
						szResearchBar = "ResearchBar-w"
						xCoord = self.xResearchBarWide + RESEARCH_BAR_WIDTH / 2
					else:
						szResearchBar = "ResearchBar"
						xCoord = screen.centerX(512)

					yCoord = 5  # Ruff: this use to be 3 but I changed it so it lines up with the Great Person Bar
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.show( "ResearchText" )
# BUG - Bars on single line for higher resolution screens - end

					researchProgress = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchProgress(gc.getPlayer(ePlayer).getCurrentResearch())
					overflowResearch = (gc.getPlayer(ePlayer).getOverflowResearch() * gc.getPlayer(ePlayer).calculateResearchModifier(gc.getPlayer(ePlayer).getCurrentResearch()))/100
					researchCost = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchCost(gc.getPlayer(ePlayer).getCurrentResearch())
					researchRate = gc.getPlayer(ePlayer).calculateResearchRate(-1)
					
					screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_STORED, float(researchProgress + overflowResearch) / researchCost )
					if ( researchCost >  researchProgress + overflowResearch):
						screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_RATE, float(researchRate) / (researchCost - researchProgress - overflowResearch))
					else:
						screen.setBarPercentage( szResearchBar, InfoBarTypes.INFOBAR_RATE, 0.0 )

					screen.show( szResearchBar )

# BUG - Progress Bar - Tick Marks - start
					if MainOpt.isShowpBarTickMarks():
						if szResearchBar == "ResearchBar":
							self.pBarResearchBar_n.drawTickMarks(screen, researchProgress + overflowResearch, researchCost, researchRate, researchRate, False)
						else:
							self.pBarResearchBar_w.drawTickMarks(screen, researchProgress + overflowResearch, researchCost, researchRate, researchRate, False)
# BUG - Progress Bar - Tick Marks - end

# BUG - Great Person Bar - start
				self.updateGreatPersonBar(screen)
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
				## ExtraModMod: Great Generals are available unconditionally.
				#if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_TACTICS): ## Suppress display of Great General bar
					#self.updateGreatGeneralBar(screen)
				self.updateGreatGeneralBar(screen)
				## ExtraModMod end
# BUG - Great General Bar - end

#CustomizableBars Start
				self.updateCustomizableBars(screen)
#CustomizableBars End

		return 0
		
# BUG - Great Person Bar - start
	def updateGreatPersonBar(self, screen):
		if (not CyInterface().isCityScreenUp() and MainOpt.isShowGPProgressBar()):
			pGPCity, iGPTurns = GPUtil.getDisplayCity()
			szText = GPUtil.getGreatPeopleText(pGPCity, iGPTurns, GP_BAR_WIDTH, MainOpt.isGPBarTypesNone(), MainOpt.isGPBarTypesOne(), True)
			szText = u"<font=2>%s</font>" % (szText)
			if (pGPCity):
				iCityID = pGPCity.getID()
			else:
				iCityID = -1
				
# BUG - Bars on single line for higher resolution screens - start
			xResolution = screen.getXResolution()
			if (xResolution >= 1440):
				szGreatPersonBar = "GreatPersonBar-w"
				xCoord = 268 + (xResolution - 1440) / 2 + 84 + 6 + 487 + 6 + 320 / 2
				yCoord = 5
			else:
				szGreatPersonBar = "GreatPersonBar"
				xCoord = 268 + (xResolution - 1024) / 2 + 100 + 7 + 380 / 2
				yCoord = 30

			screen.setText( "GreatPersonBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord + 3, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GP_PROGRESS_BAR, -1, -1 )
			if (not pGPCity):
				screen.setHitTest( "GreatPersonBarText", HitTestTypes.HITTEST_NOHIT )
			screen.show( "GreatPersonBarText" )
# BUG - Bars on single line for higher resolution screens - end
			
			if (pGPCity):
				fThreshold = float(gc.getPlayer( pGPCity.getOwner() ).greatPeopleThreshold(False))
				fRate = float(pGPCity.getGreatPeopleRate())
				fFirst = float(pGPCity.getGreatPeopleProgress()) / fThreshold

				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_STORED, fFirst )
				if ( fFirst == 1 ):
					screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold )
				else:
					screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, fRate / fThreshold / ( 1 - fFirst ) )
			else:
				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_STORED, 0 )
				screen.setBarPercentage( szGreatPersonBar, InfoBarTypes.INFOBAR_RATE, 0 )

			screen.show( szGreatPersonBar )
# BUG - Great Person Bar - end

# BUG - Great General Bar - start
	def updateGreatGeneralBar(self, screen):
		if (not CyInterface().isCityScreenUp() and MainOpt.isShowGGProgressBar()):
			pPlayer = gc.getActivePlayer()
			iCombatExp = pPlayer.getCombatExperience()
			iThresholdExp = pPlayer.greatPeopleThreshold(True)
			iNeededExp = iThresholdExp - iCombatExp
			
			szText = u"<font=2>%s</font>" %(GGUtil.getGreatGeneralText(iNeededExp))
			
# BUG - Bars on single line for higher resolution screens - start
			xResolution = screen.getXResolution()
			if (xResolution >= 1440):
				szGreatGeneralBar = "GreatGeneralBar-w"
				xCoord = 268 + (xResolution - 1440) / 2 + 84 / 2
				yCoord = 5
			else:
				szGreatGeneralBar = "GreatGeneralBar"
				xCoord = 268 + (xResolution - 1024) / 2 + 100 / 2
				yCoord = 32

			screen.setLabel( "GreatGeneralBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord + 4, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_GREAT_GENERAL, -1, -1 )
			screen.show( "GreatGeneralBarText" )
# BUG - Bars on single line for higher resolution screens - end

			fProgress = float(iCombatExp) / float(iThresholdExp)
			screen.setBarPercentage( szGreatGeneralBar, InfoBarTypes.INFOBAR_STORED, fProgress )
			screen.show( szGreatGeneralBar )
# BUG - Great General Bar - end

#CustomizableBars Start
	def updateCustomizableBars(self, screen):
		if (CyInterface().isCityScreenUp()):
			return

		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		iCurrentRate = 0
		iCurrentPoints = 0
		iThreshold = 0
		szText = ""
		lCurrentRate = []
		lCurrentPoints = []
		lThreshold = []
		lszText = []

#CustomizableBars: Define any conditions that use one of the bars here.

#AdventurerCounter Start (Imported from Rise from Erebus, modified by Terkhen)
		if (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_GRIGORI') and pPlayer.getNumCities() > 0):
			iCurrentPoints	= pPlayer.getCivCounter()
			iThreshold		= CustomFunctions.CustomFunctions().getAdventurerThreshold(gc.getGame().getActivePlayer())
			iCurrentRate	= CustomFunctions.CustomFunctions().getAdventurerPointRate(gc.getGame().getActivePlayer())

			lCurrentRate.append(iCurrentRate)
			lCurrentPoints.append(iCurrentPoints)
			lThreshold.append(iThreshold)

			if iCurrentRate == 0:
				lszText.append(BugUtil.getText("TXT_KEY_INTERFACE_ADVENTURER_COUNTER_NONE"))
			else:
				iAdventurerTurns = (iThreshold - iCurrentPoints + iCurrentRate - 1) / iCurrentRate
				lszText.append(BugUtil.getText("TXT_KEY_INTERFACE_ADVENTURER_COUNTER_TURNS", (iAdventurerTurns,))) 
#AdventurerCounter End

#Khazad vault display Start
		if (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KHAZAD') and pPlayer.getNumCities() > 0 and (((pPlayer.calculateGoldRate() != 0) and not (pPlayer.isAnarchy())) or (pPlayer.getGold() != 0))):
			iCurrentPoints = pPlayer.getGold() / pPlayer.getNumCities()
			iCurrentRate = pPlayer.calculateGoldRate()
			if iCurrentPoints <= 24:
				iThreshold = 25
				vaultText = BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_EMPTY")
			if (iCurrentPoints >= 25 and iCurrentPoints <= 49):
				iThreshold = 50
				vaultText = BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_LOW")
			if (iCurrentPoints >= 50 and iCurrentPoints <= 74):
				iThreshold = 75
				vaultText = BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_NORMAL")
			if (iCurrentPoints >= 75 and iCurrentPoints <= 99):
				iThreshold = 100
				vaultText = BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_STOCKED")
			if (iCurrentPoints >= 100 and iCurrentPoints <= 149):
				iThreshold = 150
				vaultText = BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_ABUNDANT")
			if (iCurrentPoints >= 150 and iCurrentPoints <= 249):
				iThreshold = 250
				vaultText = BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_FULL")
			if iCurrentPoints >= 250:
				iThreshold = 250
				vaultText = BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_OVERFLOWING")

			lCurrentRate.append(iCurrentRate)
			lCurrentPoints.append(iCurrentPoints)
			lThreshold.append(iThreshold)
			lszText.append(BugUtil.getText("TXT_KEY_DISPLAY_DWARVEN_VAULT_GENERAL", (vaultText,iCurrentPoints)))
#Khazad vault display End

#Adaptive tweaks START
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ADAPTIVE')):
			iBaseCycle = 75
			iCycle = (iBaseCycle * gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getVictoryDelayPercent()) / 100
			iProgress = gc.getGame().getGameTurn() % iCycle

			lCurrentRate.append(1)
			lCurrentPoints.append(iProgress)
			lThreshold.append(iCycle)
			lszText.append(BugUtil.getText("TXT_KEY_DISPLAY_TRAIT_ADAPTIVE", (iCycle - iProgress,)))
#Adaptive tweaks END

#Barbarian bar START
		eTeam = gc.getTeam(gc.getPlayer(gc.getBARBARIAN_PLAYER()).getTeam())
		iTeam = pPlayer.getTeam()
		if eTeam.isAtWar(iTeam) == False:
			iCurrentPoints = 2 * CyGame().getPlayerScore(gc.getGame().getActivePlayer())
			iThreshold = max(1, 3 * CyGame().getPlayerScore(CyGame().getRankPlayer(1)))
			lCurrentRate.append(0)
			lCurrentPoints.append(iCurrentPoints)
			lThreshold.append(iThreshold)
			iPercentage = int(100 * float(min(iThreshold, iCurrentPoints)) / float(iThreshold))
			lszText.append(BugUtil.getText("TXT_KEY_DISPLAY_TRAIT_BARBARIAN", (iPercentage,)))
#Barbarian bar END

		xCoordText = self.xResolution - xCoordCustomizableBars + widthCustomizableBars / 2
		yCoordText = yCoordCustomizableBars + 4

		for i in range (min(len(lCurrentRate), iMaxCustomizableBars)):
			szText = u"<font=2>%s</font>" % lszText[i]
			szBarName = "CustomizableBar" + str(i)
			szTextName = "CustomizableBarText" + str(i)

			yCoord = yCoordText + (iSeparationCustomizableBars + iStackBarHeight) * i
			screen.setText( szTextName, "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoordText, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest( szTextName, HitTestTypes.HITTEST_NOHIT )
			screen.show( szTextName )

			screen.setBarPercentage( szBarName, InfoBarTypes.INFOBAR_STORED, float(lCurrentPoints[i]) / float(lThreshold[i]) )
			# The rate is not displayed if the bar is already at maximum capacity.
			if lCurrentRate[i] > 0 and lThreshold[i] > lCurrentPoints[i]:
				screen.setBarPercentage( szBarName, InfoBarTypes.INFOBAR_RATE, float(lCurrentRate[i]) / float(lThreshold[i] - lCurrentPoints[i]) )

			screen.show( szBarName )
#CustomizableBars End

	def updateTimeText( self ):
		
		global g_szTimeText
		
		ePlayer = gc.getGame().getActivePlayer()
		
# BUG - NJAGC - start
		if (ClockOpt.isEnabled()):
			"""
			Format: Time - GameTurn/Total Percent - GA (TurnsLeft) Date
			
			Ex: 10:37 - 220/660 33% - GA (3) 1925
			"""
			if (g_bShowTimeTextAlt):
				bShowTime = ClockOpt.isShowAltTime()
				bShowGameTurn = ClockOpt.isShowAltGameTurn()
				bShowTotalTurns = ClockOpt.isShowAltTotalTurns()
				bShowPercentComplete = ClockOpt.isShowAltPercentComplete()
				bShowDateGA = ClockOpt.isShowAltDateGA()
			else:
				bShowTime = ClockOpt.isShowTime()
				bShowGameTurn = ClockOpt.isShowGameTurn()
				bShowTotalTurns = ClockOpt.isShowTotalTurns()
				bShowPercentComplete = ClockOpt.isShowPercentComplete()
				bShowDateGA = ClockOpt.isShowDateGA()
			
			if (not gc.getGame().getMaxTurns() > 0):
				bShowTotalTurns = False
				bShowPercentComplete = False
			
			bFirst = True
			g_szTimeText = ""
			
			if (bShowTime):
				bFirst = False
				g_szTimeText += getClockText()
			
			if (bShowGameTurn):
				if (bFirst):
					bFirst = False
				else:
					g_szTimeText += u" - "
				g_szTimeText += u"%d" %( gc.getGame().getElapsedGameTurns() )
				if (bShowTotalTurns):
					g_szTimeText += u"/%d" %( gc.getGame().getMaxTurns() )
			
			if (bShowPercentComplete):
				if (bFirst):
					bFirst = False
				else:
					if (not bShowGameTurn):
						g_szTimeText += u" - "
					else:
						g_szTimeText += u" "
				g_szTimeText += u"%2.2f%%" %( 100 *(float(gc.getGame().getElapsedGameTurns()) / float(gc.getGame().getMaxTurns())) )
			
			if (bShowDateGA and gc.getPlayer(ePlayer).isGoldenAge()):
				## FFH fix: Show only golden age, not date.
				if (bFirst):
					bFirst = False
				else:
					g_szTimeText += u" - "
				g_szTimeText += u"%c(%d)" % (CyGame().getSymbolID(FontSymbols.GOLDEN_AGE_CHAR), gc.getPlayer(ePlayer).getGoldenAgeTurns())
				#szDateGA = unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
				#if(ClockOpt.isUseEraColor()):
					#iEraColor = ClockOpt.getEraColor(gc.getEraInfo(gc.getPlayer(ePlayer).getCurrentRealEra()).getType())
					#if (iEraColor >= 0):
						#szDateGA = localText.changeTextColor(szDateGA, iEraColor)
				#g_szTimeText += szDateGA
		else:
			"""
			Original Clock
			Format: Time - 'Turn' GameTurn - GA (TurnsLeft) Date
			
			Ex: 10:37 - Turn 220 - GA (3) 1925
			"""
			g_szTimeText = localText.getText("TXT_KEY_TIME_TURN", (CyGame().getGameTurn(), )) + u" - " + unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
			if (CyUserProfile().isClockOn()):
				g_szTimeText = getClockText() + u" - " + g_szTimeText
# BUG - NJAGC - end
		
	# Will update the selection Data Strings
	def updateCityScreen( self ):
	
		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS
		
		global g_iNumTradeRoutes
		global g_iNumBuildings
		global g_iNumLeftBonus
		global g_iNumCenterBonus
		global g_iNumRightBonus
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.hide( "PopulationBar" )
		screen.hide( "ProductionBar" )
		screen.hide( "GreatPeopleBar" )
		screen.hide( "CultureBar" )
		screen.hide( "MaintenanceText" )
		screen.hide( "MaintenanceAmountText" )

		screen.hide( "KhazadText" )
		screen.hide( "KuriotateCities" )
		screen.hide( "KurioText" )

# BUG - Progress Bar - Tick Marks - start
		self.pBarPopulationBar.hide(screen)
		self.pBarProductionBar.hide(screen)
		self.pBarProductionBar_Whip.hide(screen)
# BUG - Progress Bar - Tick Marks - end

# BUG - Raw Commerce - start
		screen.hide("RawYieldsTrade0")
		screen.hide("RawYieldsFood1")
		screen.hide("RawYieldsProduction2")
		screen.hide("RawYieldsCommerce3")
		screen.hide("RawYieldsWorkedTiles4")
		screen.hide("RawYieldsCityTiles5")
		screen.hide("RawYieldsOwnedTiles6")
# BUG - Raw Commerce - end
		
		screen.hide( "NationalityText" )
		screen.hide( "NationalityBar" )
# < Revolution Mod Start >
		screen.hide( "RevStatusText" )
		screen.hide( "RevStatusBar1" )
		screen.hide( "RevStatusButton1" )
		if ( not CyInterface().isCityScreenUp() ):
			self.hideRevStatusInfoPane()
# < Revolution Mod End >
		screen.hide( "DefenseText" )
		screen.hide( "CityScrollMinus" )
		screen.hide( "CityScrollPlus" )
		screen.hide( "CityNameText" )
		screen.hide( "PopulationText" )
		screen.hide( "PopulationInputText" )
		screen.hide( "HealthText" )
		screen.hide( "ProductionText" )
		screen.hide( "ProductionInputText" )
		screen.hide( "HappinessText" )
		screen.hide( "CultureText" )
		screen.hide( "GreatPeopleText" )

		for i in range( gc.getNumReligionInfos() ):
			szName = "ReligionHolyCityDDS" + str(i)
			screen.hide( szName )
			szName = "ReligionDDS" + str(i)
			screen.hide( szName )
			
		for i in range( gc.getNumCorporationInfos() ):
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.hide( szName )
			szName = "CorporationDDS" + str(i)
			screen.hide( szName )
			
		for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
			szName = "CityPercentText" + str(i)
			screen.hide( szName )

#FfH: Added by Kael 07/18/2007
#		screen.setPanelSize( "InterfaceCenterBackgroundWidget", 296, yResolution - 133, xResolution - (296*2), 133)
#		screen.setPanelSize( "InterfaceLeftBackgroundWidget", 0, yResolution - 168, 304, 168)
#		screen.setPanelSize( "InterfaceRightBackgroundWidget", xResolution - 304, yResolution - 168, 304, 168)
#		screen.setPanelSize( "MiniMapPanel", xResolution - 214, yResolution - 151, 208, 151)
		iMultiListXR = 332
#FfH: End Add

		screen.addPanel( "BonusPane0", u"", u"", True, False, xResolution - 244, 94, 57, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNL )
		screen.hide( "BonusPane0" )
		screen.addScrollPanel( "BonusBack0", u"", xResolution - 242, 94, 157, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack0" )

		screen.addPanel( "BonusPane1", u"", u"", True, False, xResolution - 187, 94, 68, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNC )
		screen.hide( "BonusPane1" )
		screen.addScrollPanel( "BonusBack1", u"", xResolution - 191, 94, 184, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack1" )

		screen.addPanel( "BonusPane2", u"", u"", True, False, xResolution - 119, 94, 107, yResolution - 520, PanelStyles.PANEL_STYLE_CITY_COLUMNR )
		screen.hide( "BonusPane2" )
		screen.addScrollPanel( "BonusBack2", u"", xResolution - 125, 94, 205, yResolution - 536, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack2" )

		screen.hide( "TradeRouteTable" )
		screen.hide( "BuildingListTable" )
		
		screen.hide( "BuildingListBackground" )
		screen.hide( "TradeRouteListBackground" )
		screen.hide( "BuildingListLabel" )
		screen.hide( "TradeRouteListLabel" )

		i = 0
		for i in range( g_iNumLeftBonus ):
			szName = "LeftBonusItem" + str(i)
			screen.hide( szName )
		
		i = 0
		for i in range( g_iNumCenterBonus ):
			szName = "CenterBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "CenterBonusItemRight" + str(i)
			screen.hide( szName )
		
		i = 0
		for i in range( g_iNumRightBonus ):
			szName = "RightBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "RightBonusItemRight" + str(i)
			screen.hide( szName )
			
		i = 0
		for i in range( 3 ):
			szName = "BonusPane" + str(i)
			screen.hide( szName )
			szName = "BonusBack" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().isCityScreenUp() ):
			if ( pHeadSelectedCity ):
			
				screen.show( "InterfaceTopLeftBackgroundWidget" )
				screen.show( "InterfaceTopRightBackgroundWidget" )
				screen.show( "InterfaceCenterLeftBackgroundWidget" )
				screen.show( "CityScreenTopWidget" )
				screen.show( "CityNameBackground" )
				screen.show( "TopCityPanelLeft" )
				screen.show( "TopCityPanelRight" )
				screen.show( "CityScreenAdjustPanel" )
				screen.show( "InterfaceCenterRightBackgroundWidget" )
				
				if ( pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam() ):
					if ( gc.getActivePlayer().getNumCities() > 1 ):
						screen.show( "CityScrollMinus" )
						screen.show( "CityScrollPlus" )
				
				# Help Text Area
				screen.setHelpTextArea( 390, FontTypes.SMALL_FONT, 0, 0, -2.2, True, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )

				iFoodDifference = pHeadSelectedCity.foodDifference(True)
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True, True)
				iProductionDiffJustFood = (pHeadSelectedCity.getCurrentProductionDifference(False, True) - iProductionDiffNoFood)

				szBuffer = u"<font=4>"
				
				if (pHeadSelectedCity.isCapital()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
				elif (pHeadSelectedCity.isGovernmentCenter()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))

				if (pHeadSelectedCity.isPower()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))
					
				szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())

				if (pHeadSelectedCity.isOccupation()):
					szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())

				szBuffer += u"</font>"

				screen.setText( "CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
				screen.setStyle( "CityNameText", "Button_Stone_Style" )
				screen.show( "CityNameText" )

				# Suppress display of Growth bar on City screen if owner is Fallow or the city is a Settlement
				if (not gc.getPlayer(pHeadSelectedCity.getOwner()).isIgnoreFood()) and (not pHeadSelectedCity.isSettlement()):
	# BUG - Food Assist - start
					if ( CityUtil.willGrowThisTurn(pHeadSelectedCity) or (iFoodDifference != 0) or not (pHeadSelectedCity.isFoodProduction() ) ):
						
# FlavourMod: Changed by Jean Elcard 09/03/2009 (growth control buttons)
						'''
						if (iFoodDifference > 0):
						'''
						if pHeadSelectedCity.AI_stopGrowth():
							szBuffer = localText.getText("INTERFACE_CITY_STAGNANT_GROWTH_CONTROL", ())
					# lfgr BUGFIX 02/2013
						#if (CityUtil.willGrowThisTurn(pHeadSelectedCity)):
						elif (CityUtil.willGrowThisTurn(pHeadSelectedCity)):
					# lfgr end
							szBuffer = localText.getText("INTERFACE_CITY_GROWTH", ())
						elif (iFoodDifference > 0):
# FlavourMod: End Change
							szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))	
						elif (iFoodDifference < 0):
							if (CityScreenOpt.isShowFoodAssist()):
								iTurnsToStarve = pHeadSelectedCity.getFood() / -iFoodDifference + 1
								if iTurnsToStarve > 1:
									szBuffer = localText.getText("INTERFACE_CITY_SHRINKING", (iTurnsToStarve, ))
								else:
									szBuffer = localText.getText("INTERFACE_CITY_STARVING", ()) 
							else:
								szBuffer = localText.getText("INTERFACE_CITY_STARVING", ()) 
	# BUG - Food Assist - end
						else:
							szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())	
	
						screen.setLabel( "PopulationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow1Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "PopulationText", HitTestTypes.HITTEST_NOHIT )
						screen.show( "PopulationText" )
	
					if (not pHeadSelectedCity.isDisorder() and not pHeadSelectedCity.isFoodProduction()):
					
	# BUG - Food Assist - start
						if (CityScreenOpt.isShowFoodAssist()):
							iFoodYield = pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD)
							iFoodEaten = pHeadSelectedCity.foodConsumption(False, 0)
							if iFoodYield == iFoodEaten:
								szBuffer = localText.getText("INTERFACE_CITY_FOOD_STAGNATE", (iFoodYield, iFoodEaten))
							elif iFoodYield > iFoodEaten:
								szBuffer = localText.getText("INTERFACE_CITY_FOOD_GROW", (iFoodYield, iFoodEaten, iFoodYield - iFoodEaten))
							else:
								szBuffer = localText.getText("INTERFACE_CITY_FOOD_SHRINK", (iFoodYield, iFoodEaten, iFoodYield - iFoodEaten))
						else:
							szBuffer = u"%d%c - %d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_FOOD), gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), pHeadSelectedCity.foodConsumption(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
	# BUG - Food Assist - end
	# BUG - Food Rate Hover - start
						# draw label below
						
					else:
	
						szBuffer = u"%d%c" %(iFoodDifference, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
						# draw label below
	
					screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, 
							*BugDll.widget("WIDGET_FOOD_MOD_HELP", -1, -1) )
					screen.show( "PopulationInputText" )
	# BUG - Food Rate Hover - end
	
					if ((pHeadSelectedCity.badHealth(False) > 0) or (pHeadSelectedCity.goodHealth() >= 0)):
						if (pHeadSelectedCity.healthRate(False, 0) < 0):
	# BUG - Negative Health Rate is Positive Eaten Food - start
							szBuffer = localText.getText("INTERFACE_CITY_HEALTH_BAD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False), - pHeadSelectedCity.healthRate(False, 0)))
	# BUG - Negative Health Rate is Positive Eaten Food - end
						elif (pHeadSelectedCity.badHealth(False) > 0):
							szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False)))
						else:
							szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD_NO_BAD", (pHeadSelectedCity.goodHealth(), ))
							
						screen.setLabel( "HealthText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HEALTH, -1, -1 )
						screen.show( "HealthText" )
	
					if (iFoodDifference < 0):
	
						if ( pHeadSelectedCity.getFood() + iFoodDifference > 0 ):
							iDeltaFood = pHeadSelectedCity.getFood() + iFoodDifference
						else:
							iDeltaFood = 0
						if ( -iFoodDifference < pHeadSelectedCity.getFood() ):
							iExtraFood = -iFoodDifference
						else:
							iExtraFood = pHeadSelectedCity.getFood()
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(iDeltaFood) / pHeadSelectedCity.growthThreshold() )
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
						if ( pHeadSelectedCity.growthThreshold() > iDeltaFood):
							screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iExtraFood) / (pHeadSelectedCity.growthThreshold() - iDeltaFood) )
						else:
							screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)
						
					else:
	
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, float(pHeadSelectedCity.getFood()) / pHeadSelectedCity.growthThreshold() )
						if ( pHeadSelectedCity.growthThreshold() >  pHeadSelectedCity.getFood()):
							screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, float(iFoodDifference) / (pHeadSelectedCity.growthThreshold() - pHeadSelectedCity.getFood()) )
						else:
							screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0 )
	
					screen.show( "PopulationBar" )
	
	# BUG - Progress Bar - Tick Marks - start
					if MainOpt.isShowpBarTickMarks():
						self.pBarPopulationBar.drawTickMarks(screen, pHeadSelectedCity.getFood(), pHeadSelectedCity.growthThreshold(), iFoodDifference, iFoodDifference, False)
	# BUG - Progress Bar - Tick Marks - end

# End of Growth bar section for City screen

 				if (not pHeadSelectedCity.isSettlement()):
					if (pHeadSelectedCity.getOrderQueueLength() > 0):
						if (pHeadSelectedCity.isProductionProcess()):
							szBuffer = pHeadSelectedCity.getProductionName()
	# BUG - Whip Assist - start
						else:
							HURRY_WHIP = gc.getInfoTypeForString("HURRY_POPULATION")
							HURRY_BUY = gc.getInfoTypeForString("HURRY_GOLD")
							if (CityScreenOpt.isShowWhipAssist() and pHeadSelectedCity.canHurry(HURRY_WHIP, False)):
								iHurryPop = pHeadSelectedCity.hurryPopulation(HURRY_WHIP)
								iOverflow = pHeadSelectedCity.hurryProduction(HURRY_WHIP) - pHeadSelectedCity.productionLeft()
								if CityScreenOpt.isWhipAssistOverflowCountCurrentProduction():
									iOverflow += pHeadSelectedCity.getCurrentProductionDifference(False, True)
								iMaxOverflow = max(pHeadSelectedCity.getProductionNeeded(), pHeadSelectedCity.getCurrentProductionDifference(False, False))
								iLost = max(0, iOverflow - iMaxOverflow)
								iOverflow = min(iOverflow, iMaxOverflow)
								iItemModifier = pHeadSelectedCity.getProductionModifier()
								iBaseModifier = pHeadSelectedCity.getBaseYieldRateModifier(YieldTypes.YIELD_PRODUCTION, 0)
								iTotalModifier = pHeadSelectedCity.getBaseYieldRateModifier(YieldTypes.YIELD_PRODUCTION, iItemModifier)
								iLost *= iBaseModifier
								iLost /= max(1, iTotalModifier)
								iOverflow = (iBaseModifier * iOverflow) / max(1, iTotalModifier)
								if iLost > 0:
									if pHeadSelectedCity.isProductionUnit():
										iGoldPercent = gc.getDefineINT("MAXED_UNIT_GOLD_PERCENT")
									elif pHeadSelectedCity.isProductionBuilding():
										iGoldPercent = gc.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")
									elif pHeadSelectedCity.isProductionProject():
										iGoldPercent = gc.getDefineINT("MAXED_PROJECT_GOLD_PERCENT")
									else:
										iGoldPercent = 0
									iOverflowGold = iLost * iGoldPercent / 100
									szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_WHIP_PLUS_GOLD", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryPop, iOverflow, iOverflowGold))
								else:
									szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_WHIP", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryPop, iOverflow))
							elif (CityScreenOpt.isShowWhipAssist() and pHeadSelectedCity.canHurry(HURRY_BUY, False)):
								iHurryCost = pHeadSelectedCity.hurryGold(HURRY_BUY)
								szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION_BUY", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft(), iHurryCost))
							else:
								szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))
	# BUG - Whip Assist - end
	
						screen.setLabel( "ProductionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow2Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "ProductionText", HitTestTypes.HITTEST_NOHIT )
						screen.show( "ProductionText" )
					
					if (pHeadSelectedCity.isProductionProcess()):
						szBuffer = u"%d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
					elif (pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0)):
						szBuffer = u"%d%c + %d%c" %(iProductionDiffJustFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
					else:
						szBuffer = u"%d%c" %(iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
						
					screen.setLabel( "ProductionInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1 )
					screen.show( "ProductionInputText" )
	
					if ((pHeadSelectedCity.happyLevel() >= 0) or (pHeadSelectedCity.unhappyLevel(0) > 0)):
						if (pHeadSelectedCity.isDisorder()):
							szBuffer = u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
						elif (pHeadSelectedCity.angryPopulation(0) > 0):
	# BUG - Negative Happy Rate is Positive Angry Population - start
							szBuffer = localText.getText("INTERFACE_CITY_UNHAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0), pHeadSelectedCity.angryPopulation(0)))
	# BUG - Negative Happy Rate is Positive Angry Population - end
						elif (pHeadSelectedCity.unhappyLevel(0) > 0):
							szBuffer = localText.getText("INTERFACE_CITY_HAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0)))
						else:
							szBuffer = localText.getText("INTERFACE_CITY_HAPPY_NO_UNHAPPY", (pHeadSelectedCity.happyLevel(), ))
	
	# BUG - Anger Display - start
						if (CityScreenOpt.isShowAngerCounter()
						and pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam()):
							iAngerTimer = max(pHeadSelectedCity.getHurryAngerTimer(), pHeadSelectedCity.getConscriptAngerTimer())
							if iAngerTimer > 0:
								szBuffer += u" (%i)" % iAngerTimer
	# BUG - Anger Display - end
	
						screen.setLabel( "HappinessText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HAPPINESS, -1, -1 )
						screen.show( "HappinessText" )
	
					if (not(pHeadSelectedCity.isProductionProcess())):
					
						iNeeded = pHeadSelectedCity.getProductionNeeded()
						iStored = pHeadSelectedCity.getProduction()
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_STORED, float(iStored) / iNeeded )
						if iNeeded > iStored:
							screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, float(iProductionDiffNoFood) / (iNeeded - iStored) )
						else:
							screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
						if iNeeded > iStored + iProductionDiffNoFood:
							screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, float(iProductionDiffJustFood) / (iNeeded - iStored - iProductionDiffNoFood) )
						else:
							screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0)
	
						screen.show( "ProductionBar" )
	
	# BUG - Progress Bar - Tick Marks - start
						if MainOpt.isShowpBarTickMarks():
							if (pHeadSelectedCity.isProductionProcess()):
								iFirst = 0
								iRate = 0
							elif (pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0)):
								iFirst = pHeadSelectedCity.getCurrentProductionDifference(False, True)
								iRate = pHeadSelectedCity.getCurrentProductionDifference(False, False)
							else:
								iFirst = pHeadSelectedCity.getCurrentProductionDifference(True, True)
								iRate = pHeadSelectedCity.getCurrentProductionDifference(True, False)
							self.pBarProductionBar.drawTickMarks(screen, pHeadSelectedCity.getProduction(), pHeadSelectedCity.getProductionNeeded(), iFirst, iRate, False)
	
							HURRY_WHIP = gc.getInfoTypeForString("HURRY_POPULATION")
							if pHeadSelectedCity.canHurry(HURRY_WHIP, False):
								iRate = pHeadSelectedCity.hurryProduction(HURRY_WHIP) / pHeadSelectedCity.hurryPopulation(HURRY_WHIP)
								self.pBarProductionBar_Whip.drawTickMarks(screen, pHeadSelectedCity.getProduction(), pHeadSelectedCity.getProductionNeeded(), iFirst, iRate, True)
	# BUG - Progress Bar - Tick Marks - end

				iCount = 0

				for i in range(CommerceTypes.NUM_COMMERCE_TYPES):
					eCommerce = (i + 1) % CommerceTypes.NUM_COMMERCE_TYPES

					if ((gc.getPlayer(pHeadSelectedCity.getOwner()).isCommerceFlexible(eCommerce)) or (eCommerce == CommerceTypes.COMMERCE_GOLD)):
						# lfgr fix 03/2021: Allow negative research
						if pHeadSelectedCity.getCommerceRateTimes100(eCommerce) > 0 :
							szBuffer = u"%d.%02d %c" %(pHeadSelectedCity.getCommerceRate(eCommerce), pHeadSelectedCity.getCommerceRateTimes100(eCommerce)%100, gc.getCommerceInfo(eCommerce).getChar())
						else :
							szBuffer = u"0.00 %c" % gc.getCommerceInfo(eCommerce).getChar()

						iHappiness = pHeadSelectedCity.getCommerceHappinessByType(eCommerce)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u", %d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
							else:
								szTempBuffer = u", %d%c" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
							szBuffer = szBuffer + szTempBuffer

						szName = "CityPercentText" + str(iCount)
						screen.setLabel( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 53 + (19 * iCount) + 4, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_COMMERCE_MOD_HELP, eCommerce, -1 )
						screen.show( szName )
						iCount = iCount + 1

				iCount = 0

				# < Revolution Mod Start >
				if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) ) :
					screen.addTableControlGFC( "BuildingListTable", 3, 10, 317, 238, yResolution - 565, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				else :
					screen.addTableControlGFC( "BuildingListTable", 3, 10, 317, 238, yResolution - 541, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				# < Revolution Mod End >
				screen.setStyle( "BuildingListTable", "Table_City_Style" )
				
# BUG - Raw Yields - start
				bShowRawYields = g_bYieldView and CityScreenOpt.isShowRawYields()
				if (bShowRawYields):
					screen.addTableControlGFC( "TradeRouteTable", 4, 10, 187, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
					screen.setStyle( "TradeRouteTable", "Table_City_Style" )
					screen.setTableColumnHeader( "TradeRouteTable", 0, u"", 111 )
					screen.setTableColumnHeader( "TradeRouteTable", 1, u"", 60 )
					screen.setTableColumnHeader( "TradeRouteTable", 2, u"", 55 )
					screen.setTableColumnHeader( "TradeRouteTable", 3, u"", 10 )
					screen.setTableColumnRightJustify( "TradeRouteTable", 1 )
					screen.setTableColumnRightJustify( "TradeRouteTable", 2 )
				else:
					screen.addTableControlGFC( "TradeRouteTable", 3, 10, 187, 238, 98, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
					screen.setStyle( "TradeRouteTable", "Table_City_Style" )
					screen.setTableColumnHeader( "TradeRouteTable", 0, u"", 158 )
					screen.setTableColumnHeader( "TradeRouteTable", 1, u"", 68 )
					screen.setTableColumnHeader( "TradeRouteTable", 2, u"", 10 )
					screen.setTableColumnRightJustify( "TradeRouteTable", 1 )
# BUG - Raw Yields - end

				screen.setTableColumnHeader( "BuildingListTable", 0, u"", 108 )
				screen.setTableColumnHeader( "BuildingListTable", 1, u"", 118 )
				screen.setTableColumnHeader( "BuildingListTable", 2, u"", 10 )
				screen.setTableColumnRightJustify( "BuildingListTable", 1 )

				screen.show( "BuildingListBackground" )
				screen.show( "TradeRouteListBackground" )
				screen.show( "BuildingListLabel" )
				
# BUG - Raw Yields - start
				if (CityScreenOpt.isShowRawYields()):
					screen.setState("RawYieldsTrade0", not g_bYieldView)
					screen.show("RawYieldsTrade0")
					
					screen.setState("RawYieldsFood1", g_bYieldView and g_iYieldType == YieldTypes.YIELD_FOOD)
					screen.show("RawYieldsFood1")
					screen.setState("RawYieldsProduction2", g_bYieldView and g_iYieldType == YieldTypes.YIELD_PRODUCTION)
					screen.show("RawYieldsProduction2")
					screen.setState("RawYieldsCommerce3", g_bYieldView and g_iYieldType == YieldTypes.YIELD_COMMERCE)
					screen.show("RawYieldsCommerce3")
					
					screen.setState("RawYieldsWorkedTiles4", g_iYieldTiles == RawYields.WORKED_TILES)
					screen.show("RawYieldsWorkedTiles4")
					screen.setState("RawYieldsCityTiles5", g_iYieldTiles == RawYields.CITY_TILES)
					screen.show("RawYieldsCityTiles5")
					screen.setState("RawYieldsOwnedTiles6", g_iYieldTiles == RawYields.OWNED_TILES)
					screen.show("RawYieldsOwnedTiles6")
				else:
					screen.show( "TradeRouteListLabel" )
# BUG - Raw Yields - end
				
				for i in range( 3 ):
					szName = "BonusPane" + str(i)
					screen.show( szName )
					szName = "BonusBack" + str(i)
					screen.show( szName )

				i = 0
				iNumBuildings = 0
# BUG - Raw Yields - start
				self.yields = RawYields.Tracker()
# BUG - Raw Yields - end
				for i in range( gc.getNumBuildingInfos() ):
					if (pHeadSelectedCity.getNumBuilding(i) > 0):

						for k in range(pHeadSelectedCity.getNumBuilding(i)):
							
							szLeftBuffer = gc.getBuildingInfo(i).getDescription()
							szRightBuffer = u""
							bFirst = True
							
							if (pHeadSelectedCity.getNumActiveBuilding(i) > 0):
								iHealth = pHeadSelectedCity.getBuildingHealth(i)

								if (iHealth != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iHealth > 0 ):
										szTempBuffer = u"+%d%c" %( iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"+%d%c" %( -(iHealth), CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer

								iHappiness = pHeadSelectedCity.getBuildingHappiness(i)

								if (iHappiness != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iHappiness > 0 ):
										szTempBuffer = u"+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"+%d%c" %( -(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
										szRightBuffer = szRightBuffer + szTempBuffer

								for j in range( YieldTypes.NUM_YIELD_TYPES):
									iYield = gc.getBuildingInfo(i).getYieldChange(j) + pHeadSelectedCity.getNumBuilding(i) * pHeadSelectedCity.getBuildingYieldChange(gc.getBuildingInfo(i).getBuildingClassType(), j)

									if (iYield != 0):
										if ( bFirst == False ):
											szRightBuffer = szRightBuffer + ", "
										else:
											bFirst = False
											
										if ( iYield > 0 ):
											szTempBuffer = u"%s%d%c" %( "+", iYield, gc.getYieldInfo(j).getChar() )
											szRightBuffer = szRightBuffer + szTempBuffer
										else:
											szTempBuffer = u"%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
											szRightBuffer = szRightBuffer + szTempBuffer
										
# BUG - Raw Yields - start
										self.yields.addBuilding(j, iYield)
# BUG - Raw Yields - end

							for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
								iCommerce = pHeadSelectedCity.getBuildingCommerceByBuilding(j, i) / pHeadSelectedCity.getNumBuilding(i)
	
								if (iCommerce != 0):
									if ( bFirst == False ):
										szRightBuffer = szRightBuffer + ", "
									else:
										bFirst = False
										
									if ( iCommerce > 0 ):
										szTempBuffer = u"%s%d%c" %( "+", iCommerce, gc.getCommerceInfo(j).getChar() )
										szRightBuffer = szRightBuffer + szTempBuffer
									else:
										szTempBuffer = u"%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
										szRightBuffer = szRightBuffer + szTempBuffer
	
							szBuffer = szLeftBuffer + "  " + szRightBuffer
							
							screen.appendTableRow( "BuildingListTable" )
							screen.setTableText( "BuildingListTable", 0, iNumBuildings, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
							screen.setTableText( "BuildingListTable", 1, iNumBuildings, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
							
							iNumBuildings = iNumBuildings + 1
						
				if ( iNumBuildings > g_iNumBuildings ):
					g_iNumBuildings = iNumBuildings
					
				iNumTradeRoutes = 0
				
				for i in range(gc.getDefineINT("MAX_TRADE_ROUTES")):
					pLoopCity = pHeadSelectedCity.getTradeCity(i)

					if (pLoopCity and pLoopCity.getOwner() >= 0):
						player = gc.getPlayer(pLoopCity.getOwner())
						szLeftBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), pLoopCity.getName() )
						szRightBuffer = u""

						for j in range( YieldTypes.NUM_YIELD_TYPES ):
# BUG - Fractional Trade - start
							iTradeProfit = TradeUtil.calculateTradeRouteYield(pHeadSelectedCity, i, j)

							if (iTradeProfit != 0):
								if ( iTradeProfit > 0 ):
									if TradeUtil.isFractionalTrade():
										szTempBuffer = u"%s%d.%02d%c" %( "+", iTradeProfit // 100,  iTradeProfit % 100, gc.getYieldInfo(j).getChar() )
									else:
										szTempBuffer = u"%s%d%c" %( "+", iTradeProfit, gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer
								else:
									if TradeUtil.isFractionalTrade():
										szTempBuffer = u"%s%d.%02d%c" %( "", iTradeProfit // 100,  iTradeProfit % 100, gc.getYieldInfo(j).getChar() )
									else:
										szTempBuffer = u"%s%d%c" %( "", iTradeProfit, gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer
# BUG - Fractional Trade - end
# BUG - Raw Yields - start
								if (j == YieldTypes.YIELD_COMMERCE):
									if pHeadSelectedCity.getTeam() == pLoopCity.getTeam():
										self.yields.addDomesticTrade(iTradeProfit)
									else:
										self.yields.addForeignTrade(iTradeProfit)

						if (not bShowRawYields):
							screen.appendTableRow( "TradeRouteTable" )
							screen.setTableText( "TradeRouteTable", 0, iNumTradeRoutes, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
							screen.setTableText( "TradeRouteTable", 1, iNumTradeRoutes, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
# BUG - Raw Yields - end
						
						iNumTradeRoutes = iNumTradeRoutes + 1
						
				if ( iNumTradeRoutes > g_iNumTradeRoutes ):
					g_iNumTradeRoutes = iNumTradeRoutes

				i = 0  
				iLeftCount = 0
				iCenterCount = 0
				iRightCount = 0

				for i in range( gc.getNumBonusInfos() ):
					bHandled = False
					if ( pHeadSelectedCity.hasBonus(i) ):

						iHealth = pHeadSelectedCity.getBonusHealth(i)
						iHappiness = pHeadSelectedCity.getBonusHappiness(i)
						
						szBuffer = u""
						szLeadBuffer = u""

						szTempBuffer = u"<font=1>%c" %( gc.getBonusInfo(i).getChar() )
						szLeadBuffer = szLeadBuffer + szTempBuffer
						
						if (pHeadSelectedCity.getNumBonuses(i) > 1):
							szTempBuffer = u"(%d)" %( pHeadSelectedCity.getNumBonuses(i) )
							szLeadBuffer = szLeadBuffer + szTempBuffer

						szLeadBuffer = szLeadBuffer + "</font>"
						
						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )

							if ( iHealth > 0 ):
								szTempBuffer += u"<font=1>, +%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )

							szName = "RightBonusItemLeft" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "RightBonusItemRight" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 102, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iRightCount = iRightCount + 1

							bHandled = True

						if (iHealth != 0 and bHandled == False):
							if ( iHealth > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )
								
							szName = "CenterBonusItemLeft" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "CenterBonusItemRight" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 62, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iCenterCount = iCenterCount + 1

							bHandled = True

						szBuffer = u""
						if ( not bHandled ):
						
							szName = "LeftBonusItem" + str(iLeftCount)
							screen.setLabelAt( szName, "BonusBack0", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iLeftCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							
							iLeftCount = iLeftCount + 1

							bHandled = True

				g_iNumLeftBonus = iLeftCount
				g_iNumCenterBonus = iCenterCount
				g_iNumRightBonus = iRightCount
				
				iMaintenance = pHeadSelectedCity.getMaintenanceTimes100()

				szBuffer = localText.getText("INTERFACE_CITY_MAINTENANCE", ())
				
				screen.setLabel( "MaintenanceText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 126, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceText" )
				
				szBuffer = u"-%d.%02d %c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
				screen.setLabel( "MaintenanceAmountText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 125, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceAmountText" )
				
# BUG - Raw Yields - start
				if (bShowRawYields):
					self.yields.processCity(pHeadSelectedCity)
					self.yields.fillTable(screen, "TradeRouteTable", g_iYieldType, g_iYieldTiles)
# BUG - Raw Yields - end

				szBuffer = u""

				for i in range(gc.getNumReligionInfos()):
					xCoord = xResolution - 242 + (i * 34)
					yCoord = 42
					
					bEnable = True
						
					if (pHeadSelectedCity.isHasReligion(i)):

#FfH: Added by Kael 11/03/2007
						if (gc.getPlayer(gc.getGame().getActivePlayer()).canSeeReligion(i)):
#FfH: End Add

							if (pHeadSelectedCity.isHolyCityByType(i)):
								szTempBuffer = u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
								szName = "ReligionHolyCityDDS" + str(i)
								screen.show( szName )
							else:
								szTempBuffer = u"%c" %(gc.getReligionInfo(i).getChar())
							szBuffer = szBuffer + szTempBuffer

						j = 0
						for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getReligionCommerceByReligion(j, i)

							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer

						iHappiness = pHeadSelectedCity.getReligionHappiness(i)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u",+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer
							else:
								szTempBuffer = u",+%d%c" %(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer

						szBuffer = szBuffer + " "
						
						szButton = gc.getReligionInfo(i).getButton()
					
					else:
					
						bEnable = False
						szButton = gc.getReligionInfo(i).getButton()

					szName = "ReligionDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				for i in range(gc.getNumCorporationInfos()):
					xCoord = xResolution - 242 + (i * 34)
					yCoord = 66
					
					bEnable = True
						
					if (pHeadSelectedCity.isHasCorporation(i)):
						if (pHeadSelectedCity.isHeadquartersByType(i)):
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
							szName = "CorporationHeadquarterDDS" + str(i)
							screen.show( szName )
						else:
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getChar())
						szBuffer = szBuffer + szTempBuffer

						for j in range(YieldTypes.NUM_YIELD_TYPES):
							iYield = pHeadSelectedCity.getCorporationYieldByCorporation(j, i)

							if (iYield != 0):
								if ( iYield > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
						
						for j in range(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getCorporationCommerceByCorporation(j, i)

							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer

						szBuffer += " "
						
						szButton = gc.getCorporationInfo(i).getButton()
					
					else:
					
						bEnable = False
						szButton = gc.getCorporationInfo(i).getButton()

					szName = "CorporationDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				szBuffer = u"%d%% %s" %(pHeadSelectedCity.plot().calculateCulturePercent(pHeadSelectedCity.getOwner()), gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationAdjective(0) )
				screen.setLabel( "NationalityText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 210, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "NationalityText", HitTestTypes.HITTEST_NOHIT )
				screen.show( "NationalityText" )
				iRemainder = 100
				iWhichBar = 0
				for h in range( gc.getMAX_PLAYERS() ):
				# DEAD_PLAYER_CULTURE: commented out
				#	if ( gc.getPlayer(h).isAlive() ):
				# DEAD_PLAYER_CULTURE end
				# DEAD_PLAYER_CULTURE: indention changed
					iPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
					if ( iPercent > 0 ):
						screen.setStackedBarColorsRGB( "NationalityBar", iWhichBar, gc.getPlayer(h).getPlayerTextColorR(), gc.getPlayer(h).getPlayerTextColorG(), gc.getPlayer(h).getPlayerTextColorB(), gc.getPlayer(h).getPlayerTextColorA() )
						if ( iRemainder <= 0):
							screen.setBarPercentage( "NationalityBar", iWhichBar, 0.0 )
						else:
							screen.setBarPercentage( "NationalityBar", iWhichBar, float(iPercent) / iRemainder)
						iRemainder -= iPercent
						iWhichBar += 1
				# DEAD_PLAYER_CULTURE end

				screen.show( "NationalityBar" )

# < Revolution Mod Start >
				if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) :
					RevInstances.RevolutionInst.updateLocalRevIndices( CyGame().getGameTurn(), pHeadSelectedCity.getOwner(), subCityList = [pHeadSelectedCity], bNoApply = True)

					divisor = RevInstances.RevolutionInst.revInstigatorThreshold
					revIndex = pHeadSelectedCity.getRevolutionIndex()
					deltaTrend = revIndex - pHeadSelectedCity.getRevIndexAverage()
					revIndex = min([revIndex,divisor])
					if( deltaTrend > RevInstances.RevolutionInst.showTrend or deltaTrend <= -RevInstances.RevolutionInst.showTrend ) :
						deltaTrend = (deltaTrend*max([abs(deltaTrend),divisor/100+1]))/abs(2*deltaTrend)
					else :
						deltaTrend = 0
					adjIndex = max([revIndex - abs(deltaTrend),0])

					print "RevStatus bar: ", revIndex, pHeadSelectedCity.getLocalRevIndex(), deltaTrend, adjIndex

					dangerRed  = "<color=230,0,0,255>" + localText.getText("TXT_KEY_REV_WATCH_DANGER", ())  + "<color=255,255,255,255>"
					danger  = "<color=230,120,0,255>"  + localText.getText("TXT_KEY_REV_WATCH_DANGER", ())  + "<color=255,255,255,255>"
					warning = "<color=225,225,0,255>"  + localText.getText("TXT_KEY_REV_WATCH_WARNING", ()) + "<color=255,255,255,255>"
					safe	= "<color=0,230,0,255>"	+ localText.getText("TXT_KEY_REV_WATCH_SAFE", ())	+ "<color=255,255,255,255>"

					if( pHeadSelectedCity.getRevolutionIndex() >= RevInstances.RevolutionInst.alwaysViolentThreshold ) :
						cityString = dangerRed
					elif( pHeadSelectedCity.getRevolutionIndex() >= RevInstances.RevolutionInst.revInstigatorThreshold ) :
						cityString = danger
					elif( pHeadSelectedCity.getRevolutionIndex() >= RevInstances.RevolutionInst.revReadyFrac*RevInstances.RevolutionInst.revInstigatorThreshold) :
						cityString = warning
					else :
						cityString = safe

					szBuffer = u"%s: %s"%(localText.getText("TXT_KEY_REV_STATUS", ()),cityString)
					screen.setLabel( "RevStatusText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 236, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "RevStatusText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "RevStatusText" )

					fPercent1 = adjIndex/(1.0*divisor)
					fPercent2 = abs(deltaTrend)/(1.0*divisor)
					fPercent2 = min([fPercent2, 1.0-fPercent1])
					screen.setStackedBarColorsRGB( "RevStatusBar1", 0, 100, 100, 100, 255 )
					screen.setBarPercentage( "RevStatusBar1", 0, fPercent1 )

					print "Percentages: ", fPercent1, fPercent2

					if( deltaTrend < 0 ) :
						screen.setStackedBarColorsRGB( "RevStatusBar1", 1, 0, 230, 0, 255 )
					else :
						screen.setStackedBarColorsRGB( "RevStatusBar1", 1, 230, 0, 0, 255 )

					if( fPercent1 == 1 ) :
						screen.setBarPercentage( "RevStatusBar1", 1, fPercent2 )
					else :
						screen.setBarPercentage( "RevStatusBar1", 1, fPercent2/(1.0-fPercent1) )
					screen.show( "RevStatusBar1" )
					screen.show( "RevStatusButton1" )
					screen.moveToFront( "RevStatusButton1" )
# < Revolution Mod End >

				iDefenseModifier = pHeadSelectedCity.getDefenseModifier(False)

				if (iDefenseModifier != 0):
					szBuffer = localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))
					
					if (pHeadSelectedCity.getDefenseDamage() > 0):
						szTempBuffer = u" (%d%%)" %( ( ( gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage() ) * 100 ) / gc.getMAX_CITY_DEFENSE_DAMAGE() )
						szBuffer = szBuffer + szTempBuffer
					szNewBuffer = "<font=4>"
					szNewBuffer = szNewBuffer + szBuffer
					szNewBuffer = szNewBuffer + "</font>"
					screen.setLabel( "DefenseText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 270, 40, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1 )
					screen.show( "DefenseText" )

				if ( pHeadSelectedCity.getCultureLevel != CultureLevelTypes.NO_CULTURELEVEL ):
					iRate = pHeadSelectedCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
					if (iRate%100 == 0):
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), iRate/100))
					else:
						szRate = u"+%d.%02d" % (iRate/100, iRate%100)
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE_FLOAT", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), szRate))
						
# BUG - Culture Turns - start
					if CityScreenOpt.isShowCultureTurns() and iRate > 0:
						iCultureTimes100 = pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())
						iCultureLeftTimes100 = 100 * pHeadSelectedCity.getCultureThreshold() - iCultureTimes100
						szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (((iCultureLeftTimes100 + iRate - 1) / iRate),))
# BUG - Culture Turns - end

					screen.setLabel( "CultureText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 184, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "CultureText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "CultureText" )

				if ((pHeadSelectedCity.getGreatPeopleProgress() > 0) or (pHeadSelectedCity.getGreatPeopleRate() > 0)):
# BUG - Great Person Turns - start
					iRate = pHeadSelectedCity.getGreatPeopleRate()
					if CityScreenOpt.isShowCityGreatPersonInfo():
						iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
						szBuffer = GPUtil.getGreatPeopleText(pHeadSelectedCity, iGPTurns, 230, MainOpt.isGPBarTypesNone(), MainOpt.isGPBarTypesOne(), False)
					else:
						szBuffer = localText.getText("INTERFACE_CITY_GREATPEOPLE_RATE", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pHeadSelectedCity.getGreatPeopleRate()))
						if CityScreenOpt.isShowGreatPersonTurns() and iRate > 0:
							iGPTurns = GPUtil.getCityTurns(pHeadSelectedCity)
							szBuffer += u" " + localText.getText("INTERFACE_CITY_TURNS", (iGPTurns, ))
# BUG - Great Person Turns - end

					screen.setLabel( "GreatPeopleText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution - 126, yResolution - 182, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "GreatPeopleText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "GreatPeopleText" )

					iFirst = float(pHeadSelectedCity.getGreatPeopleProgress()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) )
					screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) )
					else:
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) ) / ( 1 - iFirst ) )
					screen.show( "GreatPeopleBar" )

				iFirst = float(pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())) / float(100 * pHeadSelectedCity.getCultureThreshold())
				screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_STORED, iFirst )
				if ( iFirst == 1 ):
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) )
				else:
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) ) / ( 1 - iFirst ) )
				screen.show( "CultureBar" )
				
		else:
		
			# Help Text Area
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):

#FfH: Modified by Kael 07/17/2008
#				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
#FfH: End Modify

			else:

#FfH: Modified by Kael 07/17/2008
#				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
#FfH: End Modify

			screen.hide( "InterfaceTopLeftBackgroundWidget" )
			screen.hide( "InterfaceTopRightBackgroundWidget" )
			screen.hide( "InterfaceCenterLeftBackgroundWidget" )
			screen.hide( "CityScreenTopWidget" )
			screen.hide( "CityNameBackground" )
			screen.hide( "TopCityPanelLeft" )
			screen.hide( "TopCityPanelRight" )
			screen.hide( "CityScreenAdjustPanel" )
			screen.hide( "InterfaceCenterRightBackgroundWidget" )
			
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				self.setMinimapButtonVisibility(True)

		return 0
		
	# Will update the info pane strings
	def updateInfoPaneStrings( self ):
	
		iRow = 0
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		screen.addPanel( "SelectedUnitPanel", u"", u"", True, False, 8, yResolution - 140, 280, 130, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitPanel", "Panel_Game_HudStat_Style" )
		screen.hide( "SelectedUnitPanel" )

		screen.addTableControlGFC( "SelectedUnitText", 3, 10, yResolution - 109, 183, 102, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedUnitText" )
		screen.hide( "SelectedUnitLabel" )
		
		screen.addTableControlGFC( "SelectedCityText", 3, 10, yResolution - 139, 183, 128, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedCityText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedCityText" )
		
		for i in range(gc.getNumPromotionInfos()):
			szName = "PromotionButton" + str(i)
			screen.hide( szName )
# BUG - Stack Promotions - start
			szName = "PromotionButtonCircle" + str(i)
			screen.hide( szName )
			szName = "PromotionButtonCount" + str(i)
			screen.hide( szName )
# BUG - Stack Promotions - end
		
		if CyEngine().isGlobeviewUp():
			return

		if (pHeadSelectedCity):
		
			iOrders = CyInterface().getNumOrdersQueued()

			screen.setTableColumnHeader( "SelectedCityText", 0, u"", 121 )
			screen.setTableColumnHeader( "SelectedCityText", 1, u"", 54 )
			screen.setTableColumnHeader( "SelectedCityText", 2, u"", 10 )
			screen.setTableColumnRightJustify( "SelectedCityText", 1 )
			
			for i in range( iOrders ):
				
				szLeftBuffer = u""
				szRightBuffer = u""
				
				if ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN ):
					szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

					if (CyInterface().getOrderNodeSave(i)):
						szLeftBuffer = u"*" + szLeftBuffer

# BUG - Production Started - start
					if CityScreenOpt.isShowProductionStarted():
						eUnit = CyInterface().getOrderNodeData1(i)
						if pHeadSelectedCity.getUnitProduction(eUnit) > 0:
							szRightBuffer = BugUtil.colorText(szRightBuffer, "COLOR_CYAN")
# BUG - Production Started - end
					
# BUG - Production Decay - start
					if BugDll.isPresent() and CityScreenOpt.isShowProductionDecayQueue():
						eUnit = CyInterface().getOrderNodeData1(i)
						if pHeadSelectedCity.getUnitProduction(eUnit) > 0:
							if pHeadSelectedCity.isUnitProductionDecay(eUnit):
								szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_THIS_TURN", (szLeftBuffer,))
							elif pHeadSelectedCity.getUnitProductionTime(eUnit) > 0:
								iDecayTurns = pHeadSelectedCity.getUnitProductionDecayTurns(eUnit)
								if iDecayTurns <= CityScreenOpt.getProductionDecayQueueUnitThreshold():
									szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_WARNING", (szLeftBuffer,))
# BUG - Production Decay - end

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT ):
					szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

# BUG - Production Started - start
					if CityScreenOpt.isShowProductionStarted():
						eBuilding = CyInterface().getOrderNodeData1(i)
						if pHeadSelectedCity.getBuildingProduction(eBuilding) > 0:
							szRightBuffer = BugUtil.colorText(szRightBuffer, "COLOR_CYAN")
# BUG - Production Started - end

# BUG - Production Decay - start
					if BugDll.isPresent() and CityScreenOpt.isShowProductionDecayQueue():
						eBuilding = CyInterface().getOrderNodeData1(i)
						if pHeadSelectedCity.getBuildingProduction(eBuilding) > 0:
							if pHeadSelectedCity.isBuildingProductionDecay(eBuilding):
								szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_THIS_TURN", (szLeftBuffer,))
							elif pHeadSelectedCity.getBuildingProductionTime(eBuilding) > 0:
								iDecayTurns = pHeadSelectedCity.getBuildingProductionDecayTurns(eBuilding)
								if iDecayTurns <= CityScreenOpt.getProductionDecayQueueBuildingThreshold():
									szLeftBuffer = BugUtil.getText("TXT_KEY_BUG_PRODUCTION_DECAY_WARNING", (szLeftBuffer,))
# BUG - Production Decay - end

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CREATE ):
					szLeftBuffer = gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getDescription()
					szRightBuffer = "(" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"

# BUG - Production Started - start
					if BugDll.isVersion(3) and CityScreenOpt.isShowProductionStarted():
						eProject = CyInterface().getOrderNodeData1(i)
						if pHeadSelectedCity.getProjectProduction(eProject) > 0:
							szRightBuffer = BugUtil.colorText(szRightBuffer, "COLOR_CYAN")
# BUG - Production Started - end

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_MAINTAIN ):
					szLeftBuffer = gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getDescription()

				screen.appendTableRow( "SelectedCityText" )
				screen.setTableText( "SelectedCityText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.setTableText( "SelectedCityText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
				screen.show( "SelectedCityText" )
				screen.show( "SelectedUnitPanel" )
				iRow += 1

		elif (pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):

#FfH: Modified by Kael 07/17/2008
			screen.setTableColumnHeader( "SelectedUnitText", 0, u"", 100 )
#			screen.setTableColumnHeader( "SelectedUnitText", 1, u"", 75 )
#			screen.setTableColumnHeader( "SelectedUnitText", 2, u"", 10 )
#			screen.setTableColumnHeader( "SelectedUnitText", 0, u"", 85 )
			screen.setTableColumnHeader( "SelectedUnitText", 1, u"", 75 )
			screen.setTableColumnHeader( "SelectedUnitText", 2, u"", 10 )
#FfH: End Modify

			screen.setTableColumnRightJustify( "SelectedUnitText", 1 )
			
			if (CyInterface().mirrorsSelectionGroup()):
				pSelectedGroup = pHeadSelectedUnit.getGroup()
			else:
				pSelectedGroup = 0

			if (CyInterface().getLengthSelectionList() > 1):
				
# BUG - Stack Movement Display - start
				szBuffer = localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), ))
				if MainOpt.isShowStackMovementPoints():
					iMinMoves = 100000
					iMaxMoves = 0
					for i in range(CyInterface().getLengthSelectionList()):
						pUnit = CyInterface().getSelectionUnit(i)
						if (pUnit is not None):
							iLoopMoves = pUnit.movesLeft()
							if (iLoopMoves > iMaxMoves):
								iMaxMoves = iLoopMoves
							if (iLoopMoves < iMinMoves):
								iMinMoves = iLoopMoves
					if (iMinMoves == iMaxMoves):
						fMinMoves = float(iMinMoves) / gc.getMOVE_DENOMINATOR()
						szBuffer += u" %.1f%c" % (fMinMoves, CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
					else:
						fMinMoves = float(iMinMoves) / gc.getMOVE_DENOMINATOR()
						fMaxMoves = float(iMaxMoves) / gc.getMOVE_DENOMINATOR()
						szBuffer += u" %.1f - %.1f%c" % (fMinMoves, fMaxMoves, CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
				
				screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
# BUG - Stack Movement Display - end
				
# BUG - Stack Promotions - start
				if MainOpt.isShowStackPromotions():
					iNumPromotions = gc.getNumPromotionInfos()
					lPromotionCounts = [0] * iNumPromotions
					iNumUnits = CyInterface().getLengthSelectionList()
					for i in range(iNumUnits):
						pUnit = CyInterface().getSelectionUnit(i)
						if (pUnit is not None):
							for j in range(iNumPromotions):
								if (pUnit.isHasPromotion(j)):
									lPromotionCounts[j] += 1
					
					iSPColor = MainOpt.getStackPromotionColor()
					iSPColorAll = MainOpt.getStackPromotionColorAll()
					iPromotionCount = 0
					bShowCount = MainOpt.isShowStackPromotionCounts()
					for i, iCount in enumerate(lPromotionCounts):
						if (iCount > 0):
							szName = "PromotionButton" + str(i)
							x, y = self.setPromotionButtonPosition( szName, iPromotionCount )
							screen.moveToFront( szName )
							screen.show( szName )
							if (bShowCount and iCount > 1):
								szName = "PromotionButtonCircle" + str(i)
								screen.moveItem( szName, x + 10, y + 10, -0.3 )
								screen.moveToFront( szName )
								screen.show( szName )
								szName = "PromotionButtonCount" + str(iPromotionCount)
								szText = u"<font=2>%d</font>" % iCount
								if iCount == iNumUnits:
									szText = BugUtil.colorText(szText, iSPColorAll)
								else:
									szText = BugUtil.colorText(szText, iSPColor)
								screen.setText( szName, "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, x + 17, y + 7, -0.2, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, i, -1 )
								screen.setHitTest( szName, HitTestTypes.HITTEST_NOHIT )
								screen.moveToFront( szName )
								screen.show( szName )
							iPromotionCount += 1
# BUG - Stack Promotions - end
				
				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					if (pHeadSelectedUnit):
						for i in range(gc.getNumUnitInfos()):
							iCount = CyInterface().countEntities(i)

							if (iCount > 0):
								szRightBuffer = u""
								
								szLeftBuffer = gc.getUnitInfo(i).getDescription()

								if (iCount > 1):
									szRightBuffer = u"(" + str(iCount) + u")"

								szBuffer = szLeftBuffer + u"  " + szRightBuffer
								screen.appendTableRow( "SelectedUnitText" )
								screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
								screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
								screen.show( "SelectedUnitText" )
								screen.show( "SelectedUnitPanel" )
								iRow += 1
			else:
			
				if (pHeadSelectedUnit.getHotKeyNumber() == -1):
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (pHeadSelectedUnit.getName(), ))
				else:
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), pHeadSelectedUnit.getName()))
				if (len(szBuffer) > 60):
					szBuffer = "<font=2>" + szBuffer + "</font>"
				screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 137, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
			
				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )

					szBuffer = u""

					szLeftBuffer = u""
					szRightBuffer = u""
					
					if (pHeadSelectedUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
						if (pHeadSelectedUnit.airBaseCombatStr() > 0):
							szLeftBuffer = localText.getText("INTERFACE_PANE_AIR_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.airBaseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.airBaseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
					else:
						if (pHeadSelectedUnit.canFight()):
							szLeftBuffer = localText.getText("INTERFACE_PANE_STRENGTH", ())
							if (pHeadSelectedUnit.isFighting()):
								szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))

#FfH: Modified by Kael 08/18/2007
#							elif (pHeadSelectedUnit.isHurt()):
#								szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
#							else:
#								szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							elif (pHeadSelectedUnit.isHurt()):
								if pHeadSelectedUnit.baseCombatStr() == pHeadSelectedUnit.baseCombatStrDefense():
									szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
								else:
									szRightBuffer = u"%.1f/%.lf%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), ((float(pHeadSelectedUnit.baseCombatStrDefense() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
							else:
								if pHeadSelectedUnit.baseCombatStr() == pHeadSelectedUnit.baseCombatStrDefense():
									szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
								else:
									szRightBuffer = u"%d/%d%c" %(pHeadSelectedUnit.baseCombatStr(), pHeadSelectedUnit.baseCombatStrDefense(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
#FfH: End Modify

					szBuffer = szLeftBuffer + szRightBuffer
					if ( szBuffer ):
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					szLeftBuffer = u""
					szRightBuffer = u""
					
# BUG - Unit Movement Fraction - start
					szLeftBuffer = localText.getText("INTERFACE_PANE_MOVEMENT", ())
					if MainOpt.isShowUnitMovementPointsFraction():
						szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
						if (pHeadSelectedUnit.movesLeft() == 0):
							szRightBuffer = u"0/" + szRightBuffer
						elif (pHeadSelectedUnit.movesLeft() == pHeadSelectedUnit.baseMoves() * gc.getMOVE_DENOMINATOR()):
							pass
						else:
							fCurrMoves = float(pHeadSelectedUnit.movesLeft()) / gc.getMOVE_DENOMINATOR()
							szRightBuffer = (u"%.1f/" % fCurrMoves) + szRightBuffer
					else:
						if ( (pHeadSelectedUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0 ):
							iDenom = 1
						else:
							iDenom = 0
						iCurrMoves = ((pHeadSelectedUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
						if (pHeadSelectedUnit.baseMoves() == iCurrMoves):
							szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
						else:
							szRightBuffer = u"%d/%d%c" %(iCurrMoves, pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
# BUG - Unit Movement Fraction - end

					szBuffer = szLeftBuffer + "  " + szRightBuffer
					screen.appendTableRow( "SelectedUnitText" )
					screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )
					iRow += 1

					if (pHeadSelectedUnit.getLevel() > 0):
					
						szLeftBuffer = localText.getText("INTERFACE_PANE_LEVEL", ())
						szRightBuffer = u"%d" %(pHeadSelectedUnit.getLevel())
						
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					if ((pHeadSelectedUnit.getExperience() > 0) and not pHeadSelectedUnit.isFighting()):
						szLeftBuffer = localText.getText("INTERFACE_PANE_EXPERIENCE", ())
						szRightBuffer = u"(%d/%d)" %(pHeadSelectedUnit.getExperience(), pHeadSelectedUnit.experienceNeeded())
						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

					iPromotionCount = 0
					i = 0
					for i in range(gc.getNumPromotionInfos()):

#FfH: Modified by Kael 08/17/2007
#						if (pHeadSelectedUnit.isHasPromotion(i)):
						iPromNext = gc.getPromotionInfo(i).getPromotionNextLevel()
						if (pHeadSelectedUnit.isHasPromotion(i) and (iPromNext == -1 or pHeadSelectedUnit.isHasPromotion(iPromNext) == False)):
#FfH: End Modify

							szName = "PromotionButton" + str(i)
							self.setPromotionButtonPosition( szName, iPromotionCount )
							screen.moveToFront( szName )
							screen.show( szName )

							iPromotionCount = iPromotionCount + 1

			if (pSelectedGroup):
			
				iNodeCount = pSelectedGroup.getLengthMissionQueue()

				if (iNodeCount > 1):
					for i in range( iNodeCount ):
						szLeftBuffer = u""
						szRightBuffer = u""
					
						if (gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild()):
							if (i == 0):
								szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
								szRightBuffer = localText.getText("INTERFACE_CITY_TURNS", (pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0), ))								
							else:
								szLeftBuffer = u"%s..." %(gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription())
						else:
							szLeftBuffer = u"%s..." %(gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription())

						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

		return 0
		
	# Will update the scores
	def updateScoreStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		screen.hide( "ScoreBackground" )
		
# BUG - Align Icons - start
		for i in range( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.hide( szName )
			szName = "ScoreTech" + str(i)
			screen.hide( szName )
			for j in range( Scoreboard.NUM_PARTS ):
				szName = "ScoreText%d-%d" %( i, j )
				screen.hide( szName )
# BUG - Align Icons - end

#FfH Global Counter: Added by Kael 08/12/2007
		if CyGame().getWBMapScript():
			szName = "GoalTag"
			screen.hide( szName )
		szName = "CutLosersTag"
		screen.hide( szName )
		szName = "DifficultyTag"
		screen.hide( szName )
		szName = "HighToLowTag"
		screen.hide( szName )
		szName = "DisableProductionTag"
		screen.hide( szName )
		szName = "DisableResearchTag"
		screen.hide( szName )
		szName = "DisableSpellcastingTag"
		screen.hide( szName )
		szName = "SanctuaryTimerTag"
		screen.hide( szName )
#FfH: End Add

		# < Revolution Mod Start >
		screen.hide( "ScoreTextSeparator1" )
		screen.hide( "ExtraCivSeparator1" )

		iMinorCount = 0
		iLineCount = 0
		# < Revolution Mod End >

		iWidth = 0
		iCount = 0
		iBtnHeight = 22

# CCV - Position of Scores - START
		iPreCount = 0
		iSelectCount = 0
# CCV - Position of Scores - END
		
		if ((CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY)):
			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyEngine().isGlobeviewUp() == false):

# BUG - Align Icons - start
				bAlignIcons = ScoreOpt.isAlignIcons()
				if (bAlignIcons):
					scores = Scoreboard.Scoreboard()
# BUG - Align Icons - end

# BUG - 3.17 No Espionage - start
				bEspionage = GameUtil.isEspionage()
# BUG - 3.17 No Espionage - end

# BUG - Power Rating - start
				# lfgr 05/2021: Advanced tactics and embassy no longer required
				bShowPower = ScoreOpt.isShowPower()
				if (bShowPower):
					iPlayerPower = gc.getActivePlayer().getPower()
					iPowerColor = ScoreOpt.getPowerColor()
					iHighPowerColor = ScoreOpt.getHighPowerColor()
					iLowPowerColor = ScoreOpt.getLowPowerColor()
					
					if (bEspionage):
						iDemographicsMission = -1
						for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
							if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
								iDemographicsMission = iMissionLoop
								break
						if (iDemographicsMission == -1):
							bShowPower = False

# CCV - Position of Scores - START
				i = gc.getMAX_CIV_TEAMS() - 1
				while (i > -1):
					eTeam = gc.getGame().getRankTeam(i)

					if (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam) or gc.getTeam(eTeam).isHuman() or gc.getGame().isDebugMode()):
						
						j = gc.getMAX_CIV_PLAYERS() - 1
						while (j > -1):
							ePlayer = gc.getGame().getRankPlayer(j)

							if (not CyInterface().isScoresMinimized() or gc.getGame().getActivePlayer() == ePlayer):
								if (gc.getPlayer(ePlayer).isEverAlive() and not gc.getPlayer(ePlayer).isBarbarian()
									and (gc.getPlayer(ePlayer).isAlive() or ScoreOpt.isShowDeadCivs())):
									if (not gc.getPlayer(ePlayer).isMinorCiv() or ScoreOpt.isShowMinorCivs()):
										if (gc.getPlayer(ePlayer).getTeam() == eTeam):											
											iPreCount = iPreCount + 1
							j = j - 1
					i = i - 1

				self.iScoreStartMax = (iPreCount - ScoreOpt.getMaxPlayers() + 1)					
				self.updateScrollingScoreboard(screen)

				if (bAlignIcons):
					scores.setStartScore(self.iScore_View)					
# CCV - Position of Scores - END				
						
# BUG - Power Rating - end

				i = gc.getMAX_CIV_TEAMS() - 1
				while (i > -1):
					eTeam = gc.getGame().getRankTeam(i)

					if (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam) or gc.getTeam(eTeam).isHuman() or gc.getGame().isDebugMode()):
# BUG - Align Icons - start
						if (bAlignIcons):
							scores.addTeam(gc.getTeam(eTeam), i)
# BUG - Align Icons - end
						j = gc.getMAX_CIV_PLAYERS() - 1
						while (j > -1):
							ePlayer = gc.getGame().getRankPlayer(j)

							if (not CyInterface().isScoresMinimized() or gc.getGame().getActivePlayer() == ePlayer):
# BUG - Dead Civs - start
								if (gc.getPlayer(ePlayer).isEverAlive() and not gc.getPlayer(ePlayer).isBarbarian()
									and (gc.getPlayer(ePlayer).isAlive() or ScoreOpt.isShowDeadCivs())):
# BUG - Dead Civs - end
# BUG - Minor Civs - start
									if (not gc.getPlayer(ePlayer).isMinorCiv() or ScoreOpt.isShowMinorCivs()):
# BUG - Minor Civs - end
										if (gc.getPlayer(ePlayer).getTeam() == eTeam):
											szBuffer = u"<font=2>"
# BUG - Align Icons - start
											if (bAlignIcons):
												scores.addPlayer(gc.getPlayer(ePlayer), j)
												# BUG: Align Icons continues throughout -- if (bAlignIcons): scores.setFoo(foo)
# BUG - Align Icons - end
	
											if (gc.getGame().isGameMultiPlayer()):
												if (not (gc.getPlayer(ePlayer).isTurnActive())):
													szBuffer = szBuffer + "*"
													if (bAlignIcons):
														scores.setWaiting()
	
# BUG - Dead Civs - start
											if (ScoreOpt.isUsePlayerName()):
												szPlayerName = gc.getPlayer(ePlayer).getName()
											else:
												szPlayerName = gc.getLeaderHeadInfo(gc.getPlayer(ePlayer).getLeaderType()).getDescription()
											if (ScoreOpt.isShowBothNames()):
												szCivName = gc.getPlayer(ePlayer).getCivilizationShortDescription(0)
												szPlayerName = szPlayerName + "/" + szCivName
											elif (ScoreOpt.isShowBothNamesShort()):
												szCivName = gc.getPlayer(ePlayer).getCivilizationDescription(0)
												szPlayerName = szPlayerName + "/" + szCivName
											elif (ScoreOpt.isShowLeaderName()):
												szPlayerName = szPlayerName
											elif (ScoreOpt.isShowCivName()):
												szCivName = gc.getPlayer(ePlayer).getCivilizationShortDescription(0)
												szPlayerName = szCivName
											else:
												szCivName = gc.getPlayer(ePlayer).getCivilizationDescription(0)
												szPlayerName = szCivName
											
											if (not gc.getPlayer(ePlayer).isAlive() and ScoreOpt.isShowDeadTag()):
												szPlayerScore = localText.getText("TXT_KEY_BUG_DEAD_CIV", ())
												if (bAlignIcons):
													scores.setScore(szPlayerScore)
											else:
												iScore = gc.getGame().getPlayerScore(ePlayer)
												szPlayerScore = u"%d" % iScore
												if (bAlignIcons):
													scores.setScore(szPlayerScore)
# BUG - Score Delta - start
												if (ScoreOpt.isShowScoreDelta()):
													iGameTurn = gc.getGame().getGameTurn()
													if (ePlayer >= gc.getGame().getActivePlayer()):
														iGameTurn -= 1
													if (ScoreOpt.isScoreDeltaIncludeCurrentTurn()):
														iScoreDelta = iScore
													elif (iGameTurn >= 0):
														iScoreDelta = gc.getPlayer(ePlayer).getScoreHistory(iGameTurn)
													else:
														iScoreDelta = 0
													iPrevGameTurn = iGameTurn - 1
													if (iPrevGameTurn >= 0):
														iScoreDelta -= gc.getPlayer(ePlayer).getScoreHistory(iPrevGameTurn)
													if (iScoreDelta != 0):
														if (iScoreDelta > 0):
															iColorType = gc.getInfoTypeForString("COLOR_GREEN")
														elif (iScoreDelta < 0):
															iColorType = gc.getInfoTypeForString("COLOR_RED")
														szScoreDelta = "%+d" % iScoreDelta
														if (iColorType >= 0):
															szScoreDelta = localText.changeTextColor(szScoreDelta, iColorType)
														szPlayerScore += szScoreDelta + u" "
														if (bAlignIcons):
															scores.setScoreDelta(szScoreDelta)
# BUG - Score Delta - end
											
											if (not CyInterface().isFlashingPlayer(ePlayer) or CyInterface().shouldFlash(ePlayer)):
												if (ePlayer == gc.getGame().getActivePlayer()):
													szPlayerName = u"[<color=%d,%d,%d,%d>%s</color>]" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
												else:
													if (not gc.getPlayer(ePlayer).isAlive() and ScoreOpt.isGreyOutDeadCivs()):
														szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(175, 175, 175, gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
													else:
														szPlayerName = u"<color=%d,%d,%d,%d>%s</color>" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), szPlayerName)
											## RevolutionDCM start
											if( gc.getPlayer(ePlayer).isMinorCiv() ) :
												szPlayerName += " (minor)"
											elif( not gc.getTeam(eTeam).isAtWar(gc.getGame().getActiveTeam()) and gc.getTeam(gc.getGame().getActiveTeam()).AI_getWarPlan(eTeam) >= 0):
												szPlayerName += " ("  + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + ")"
											##RevolutionDCM end
											szTempBuffer = u"%s: %s" %(szPlayerScore, szPlayerName)
											szBuffer = szBuffer + szTempBuffer
											if (bAlignIcons):
												scores.setName(szPlayerName)
												scores.setID(u"<color=%d,%d,%d,%d>%d</color>" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), ePlayer))
											
											if (gc.getPlayer(ePlayer).isAlive()):
												if (bAlignIcons):
													scores.setAlive()
												# BUG: Rest of Dead Civs change is merely indentation by 1 level ...
												if (gc.getTeam(eTeam).isAlive()):
													if ( not (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam)) ):
														szBuffer = szBuffer + (" ?")
														if (bAlignIcons):
															scores.setNotMet()
													#szTempBuffer = ""
													if (gc.getTeam(eTeam).isAtWar(gc.getGame().getActiveTeam())):
														szTempBuffer =  u" ("  + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), gc.getInfoTypeForString("COLOR_RED")).upper() + ")"
														szPlayerName = szPlayerName + szTempBuffer
														#scores.setName(szPlayerName)
														#szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setWar()

													# BETTER_BTS_AI_MOD - Show if player is planning war against another civ
#													elif (gc.getTeam(gc.getGame().getActiveTeam()).AI_getWarPlan(eTeam) > -1):
#														szTempBuffer =  u"("  + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + ")"
#														szPlayerName = szPlayerName + szTempBuffer
#														scores.setName(szPlayerName)
														#szBuffer = szBuffer + szTempBuffer
													# BETTER_BTS_AI_MOD end
													#	if (bAlignIcons):
													#		scores.setWar()
													elif (gc.getTeam(gc.getGame().getActiveTeam()).isForcePeace(eTeam)):
														if (bAlignIcons):
															scores.setPeace()
													elif (gc.getTeam(eTeam).isAVassal()):
														for iOwnerTeam in range(gc.getMAX_TEAMS()):
															if (gc.getTeam(eTeam).isVassal(iOwnerTeam) and gc.getTeam(gc.getGame().getActiveTeam()).isForcePeace(iOwnerTeam)):
																if (bAlignIcons):
																	scores.setPeace()
																break
#FfH Alignment: Added by Kael 08/09/2007
													if gc.getPlayer(ePlayer).getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
														szTempBuffer = " (" + localText.getColorText("TXT_KEY_ALIGNMENT_EVIL", (), gc.getInfoTypeForString("COLOR_RED")) + ") "
													if gc.getPlayer(ePlayer).getAlignment() == gc.getInfoTypeForString('ALIGNMENT_NEUTRAL'):
														szTempBuffer = " (" + localText.getColorText("TXT_KEY_ALIGNMENT_NEUTRAL", (), gc.getInfoTypeForString("COLOR_GREY")) + ") "
													if gc.getPlayer(ePlayer).getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
														szTempBuffer = " (" + localText.getColorText("TXT_KEY_ALIGNMENT_GOOD", (), gc.getInfoTypeForString("COLOR_YELLOW")) + ") "
													#szBuffer = szBuffer + szTempBuffer
													szPlayerName = szPlayerName + szTempBuffer
													if (bAlignIcons):
														scores.setName(szPlayerName)
#FfH: End Add
													if (gc.getPlayer(ePlayer).canTradeNetworkWith(gc.getGame().getActivePlayer()) and (ePlayer != gc.getGame().getActivePlayer())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setTrade()
													if (gc.getTeam(eTeam).isOpenBorders(gc.getGame().getActiveTeam())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setBorders()
													if (gc.getTeam(eTeam).isHasEmbassy(gc.getGame().getActiveTeam())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setEmbassy()
													if (gc.getTeam(eTeam).isDefensivePact(gc.getGame().getActiveTeam())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setPact()
													if (gc.getPlayer(ePlayer).getStateReligion() != -1):

		#FfH: Added by Kael 11/04/2007
														if (gc.getPlayer(gc.getGame().getActivePlayer()).canSeeReligion(gc.getPlayer(ePlayer).getStateReligion())):
		#FfH: End Add
											
															if (gc.getPlayer(ePlayer).hasHolyCity(gc.getPlayer(ePlayer).getStateReligion())):
																szTempBuffer = u"%c" %(gc.getReligionInfo(gc.getPlayer(ePlayer).getStateReligion()).getHolyCityChar())
															else:
																szTempBuffer = u"%c" %(gc.getReligionInfo(gc.getPlayer(ePlayer).getStateReligion()).getChar())
															szBuffer = szBuffer + szTempBuffer
															if (bAlignIcons):
																scores.setReligion(szTempBuffer)
													if (bEspionage and gc.getTeam(eTeam).getEspionagePointsAgainstTeam(gc.getGame().getActiveTeam()) < gc.getTeam(gc.getGame().getActiveTeam()).getEspionagePointsAgainstTeam(eTeam)):
														szTempBuffer = u"%c" %(gc.getCommerceInfo(CommerceTypes.COMMERCE_ESPIONAGE).getChar())
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setEspionage()

												bEspionageCanSeeResearch = False
#FfH: Added by Kael 10/01/2008
												if gc.getPlayer(gc.getGame().getActivePlayer()).getNumBuilding(gc.getInfoTypeForString('BUILDING_EYES_AND_EARS_NETWORK')) > 0:
													bEspionageCanSeeResearch = True
#FfH: End Add
												if (bEspionage):
													for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
														if (gc.getEspionageMissionInfo(iMissionLoop).isSeeResearch()):
															bEspionageCanSeeResearch = gc.getActivePlayer().canDoEspionageMission(iMissionLoop, ePlayer, None, -1)
															break
												
												if (((gc.getPlayer(ePlayer).getTeam() == gc.getGame().getActiveTeam()) and (gc.getTeam(gc.getGame().getActiveTeam()).getNumMembers() > 1)) or (gc.getTeam(gc.getPlayer(ePlayer).getTeam()).isVassal(gc.getGame().getActiveTeam())) or gc.getGame().isDebugMode() or bEspionageCanSeeResearch):
													if (gc.getPlayer(ePlayer).getCurrentResearch() != -1):
														szTempBuffer = u"-%s (%d)" %(gc.getTechInfo(gc.getPlayer(ePlayer).getCurrentResearch()).getDescription(), gc.getPlayer(ePlayer).getResearchTurnsLeft(gc.getPlayer(ePlayer).getCurrentResearch(), True))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setResearch(gc.getPlayer(ePlayer).getCurrentResearch(), gc.getPlayer(ePlayer).getResearchTurnsLeft(gc.getPlayer(ePlayer).getCurrentResearch(), True))
												# BUG: ...end of indentation
# BUG - Dead Civs - end
# BUG - Power Rating - start
												# if on, show according to espionage "see demographics" mission
												### ExtraModMod: Allow to see the power ratios inconditionally.
												if (bShowPower 
													and (gc.getGame().getActivePlayer() != ePlayer
														 and (not bEspionage or gc.getActivePlayer().canDoEspionageMission(iDemographicsMission, ePlayer, None, -1)))):
													# lfgr 05/2021: Advanced tactics and embassy no longer required
													iPower = gc.getPlayer(ePlayer).getPower()
													if (iPower > 0): # avoid divide by zero
														fPowerRatio = float(iPlayerPower) / float(iPower)
														if (ScoreOpt.isPowerThemVersusYou()):
															if (fPowerRatio > 0):
																fPowerRatio = 1.0 / fPowerRatio
															else:
																fPowerRatio = 99.0
														cPower = gc.getGame().getSymbolID(FontSymbols.STRENGTH_CHAR)
														szTempBuffer = BugUtil.formatFloat(fPowerRatio, ScoreOpt.getPowerDecimals()) + u"%c" % (cPower)
														if (iHighPowerColor >= 0 and fPowerRatio >= ScoreOpt.getHighPowerRatio()):
															szTempBuffer = localText.changeTextColor(szTempBuffer, iHighPowerColor)
														elif (iLowPowerColor >= 0 and fPowerRatio <= ScoreOpt.getLowPowerRatio()):
															szTempBuffer = localText.changeTextColor(szTempBuffer, iLowPowerColor)
														elif (iPowerColor >= 0):
															szTempBuffer = localText.changeTextColor(szTempBuffer, iPowerColor)
														szBuffer = szBuffer + u" " + szTempBuffer
														if (bAlignIcons):
															scores.setPower(szTempBuffer)
# BUG - Power Rating - end
# BUG - Attitude Icons - start
												if (ScoreOpt.isShowAttitude()):
													if (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(gc.getPlayer(ePlayer).getTeam())): ## Dont display attitude for those we havent met
														if (not gc.getPlayer(ePlayer).isHuman() and (not gc.getPlayer(ePlayer).isHumanDisabled())):
															iAtt = gc.getPlayer(ePlayer).AI_getAttitude(gc.getGame().getActivePlayer())
															cAtt =  unichr(ord(unichr(CyGame().getSymbolID(FontSymbols.POWER_CHAR) + 3)) + iAtt)
															szBuffer += cAtt
															if (bAlignIcons):
																scores.setAttitude(cAtt)
# BUG - Attitude Icons - end
# BUG - Refuses to Talk - start
												if (not DiplomacyUtil.isWillingToTalk(ePlayer, gc.getGame().getActivePlayer())):
													cRefusesToTalk = u"!"
													szBuffer += cRefusesToTalk
													if (bAlignIcons):
														scores.setWontTalk()
# BUG - Refuses to Talk - end

# BUG - Worst Enemy - start
												if (ScoreOpt.isShowWorstEnemy()):
													if (AttitudeUtil.isWorstEnemy(ePlayer, gc.getGame().getActivePlayer())):
														cWorstEnemy = u"%c" %(CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
														szBuffer += cWorstEnemy
														if (bAlignIcons):
															scores.setWorstEnemy()
# BUG - Worst Enemy - end
# BUG - WHEOOH - start
												if (ScoreOpt.isShowWHEOOH()):
													if (PlayerUtil.isWHEOOH(ePlayer, PlayerUtil.getActivePlayerID())):
														szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR))
														szBuffer = szBuffer + szTempBuffer
														if (bAlignIcons):
															scores.setWHEOOH()
# BUG - WHEOOH - end
# BUG - Num Cities - start
												# lfgr 05/2021: Allow seeing number of cities even in non-debug mode
												#   (as long as that information is accessible by the player)
												if (ScoreOpt.isShowCountCities()):
													if (PlayerUtil.canSeeCityList(ePlayer)):
														szTempBuffer = u"%d" % PlayerUtil.getNumCities(ePlayer)
													else:
														szTempBuffer = BugUtil.colorText(u"%d" % PlayerUtil.getNumRevealedCities(ePlayer), "COLOR_CYAN")
													szBuffer = szBuffer + " " + szTempBuffer
													if (bAlignIcons):
														scores.setNumCities(szTempBuffer)
# BUG - Num Cities - end
											
											if (CyGame().isNetworkMultiPlayer()):
												szTempBuffer = CyGameTextMgr().getNetStats(ePlayer)
												szBuffer = szBuffer + szTempBuffer
												if (bAlignIcons):
													scores.setNetStats(szTempBuffer)
											
											if (gc.getPlayer(ePlayer).isHuman() and CyInterface().isOOSVisible()):
												szTempBuffer = u" <color=255,0,0>* %s *</color>" %(CyGameTextMgr().getOOSSeeds(ePlayer))
												szBuffer = szBuffer + szTempBuffer
												if (bAlignIcons):
													scores.setNetStats(szTempBuffer)
												
											szBuffer = szBuffer + "</font>"
	
# BUG - Align Icons - start
											if (not bAlignIcons):

# CCV - Position of Scores - START																								
												if (iPreCount <= ScoreOpt.getMaxPlayers() or ScoreOpt.getMaxPlayers() == 0 or ((iPreCount - iCount) >= (self.iScore_View) and (iPreCount - iCount) <= (self.iScore_View + ScoreOpt.getMaxPlayers() - 1))):																																				
													if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
														iWidth = CyInterface().determineWidth( szBuffer )
# CCV - Position of Scores - END																												
		
												szName = "ScoreText" + str(ePlayer)
												if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
													yCoord = yResolution - 206
												else:
													yCoord = yResolution - 88
		
# BUG - Dead Civs - start
												# Don't try to contact dead civs
												if (gc.getPlayer(ePlayer).isAlive()):
													iWidgetType = WidgetTypes.WIDGET_CONTACT_CIV
													iPlayer = ePlayer
												else:
													iWidgetType = WidgetTypes.WIDGET_GENERAL
													iPlayer = -1

# CCV - Position of Scores - START

												if (iPreCount <= ScoreOpt.getMaxPlayers() or ScoreOpt.getMaxPlayers() == 0 or ((iPreCount - iCount) >= (self.iScore_View) and (iPreCount - iCount) <= (self.iScore_View + ScoreOpt.getMaxPlayers() - 1))):
													offset = 0
													if (self.checkScrollingScoreboard() == True): 
														offset = iBtnHeight																										
													screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - (iSelectCount * iBtnHeight) - offset, -0.3, FontTypes.SMALL_FONT, iWidgetType, iPlayer, -1 )
# BUG - Dead Civs - end
													screen.show( szName )
																									
													CyInterface().checkFlashReset(ePlayer)
													iSelectCount = iSelectCount + 1
# CCV - Position of Scores - END												
												iCount = iCount + 1
# BUG - Align Icons - end
							j = j - 1
					i = i - 1

# BUG - Align Icons - start
				if (bAlignIcons):
					scores.draw(screen)
				else:
					if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
						yCoord = yResolution - 186
					else:
						yCoord = yResolution - 68

# CCV - Position of Scores - START
					if (self.checkScrollingScoreboard() == True): 
						yCoord = yCoord - iBtnHeight
# CCV - Position of Scores - START
					screen.setPanelSize( "ScoreBackground", xResolution - 21 - iWidth, yCoord - (iBtnHeight * iSelectCount) - 4, iWidth + 12, (iBtnHeight * iSelectCount) + 8 )
# CCV - Position of Scores - END

					screen.show( "ScoreBackground" )
# BUG - Align Icons - end
				yCoord = yResolution - 186
#FfH Global Counter: Added by Kael 08/12/2007
				pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
				iCountSpecial = 0

				# UI improvement 01/2022 lfgr
				bIncreasing = gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_INCREASING_DIFFICULTY)
				bHardest = pPlayer.getHandicapType() == gc.getNumHandicapInfos() - 1 # At hardest difficulty already
				bFlexible = gc.getGame().isOption(GameOptionTypes.GAMEOPTION_FLEXIBLE_DIFFICULTY)

				if bIncreasing or bFlexible :
					iCountSpecial += 1
					szName = "DifficultyTag"
					szBuffer = u"<font=2>"
					szBuffer += localText.getColorText("TXT_KEY_MESSAGE_DIFFICULTY", (gc.getHandicapInfo(pPlayer.getHandicapType()).getDescription(), ()), gc.getInfoTypeForString("COLOR_RED"))

					if ffhUIOpt.isShowTurnsUntilDifficultyChange() and ( bFlexible or not bHardest ) :
						iFlexibleTurns = game.getFlexibleDifficultyRemainingTurns()
						iIncreasingTurns = game.getIncreasingDifficultyRemainingTurns()
						if bIncreasing and bFlexible :
							szBuffer += u" " + localText.getColorText( "TXT_KEY_MESSAGE_DIFFICULTY_CHANGE_FLEX_INCR", (iFlexibleTurns, iIncreasingTurns), gc.getInfoTypeForString("COLOR_RED"))
						elif bIncreasing :
							szBuffer += u" " + localText.getColorText( "TXT_KEY_MESSAGE_DIFFICULTY_CHANGE", (iIncreasingTurns,), gc.getInfoTypeForString("COLOR_RED"))
						elif bFlexible :
							szBuffer += u" " + localText.getColorText( "TXT_KEY_MESSAGE_DIFFICULTY_CHANGE", (iFlexibleTurns,), gc.getInfoTypeForString("COLOR_RED"))

					szBuffer += "</font>"
#					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#					screen.show( szName )
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+ ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( szName )

				if (gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_CUT_LOSERS) or gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT)):
					if gc.getGame().countCivPlayersAlive() > 5:
						iCountSpecial += 1
						szName = "CutLosersTag"
						szBuffer = u"<font=2>"
						szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_CUT_LOSERS", (gc.getGame().getCutLosersCounter(), ()), gc.getInfoTypeForString("COLOR_RED"))
						szBuffer = szBuffer + "</font>"
#						screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#						screen.show( szName )
						screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+ ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( szName )

				if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_HIGH_TO_LOW):
					iCountSpecial += 1
					szName = "HighToLowTag"
					szBuffer = u"<font=2>"
					if gc.getGame().getHighToLowCounter() == 0:
						szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_HIGH_TO_LOW_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
					if gc.getGame().getHighToLowCounter() == 1:
						szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_HIGH_TO_LOW_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
					if gc.getGame().getHighToLowCounter() > 1:
						szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_HIGH_TO_LOW_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
					szBuffer = szBuffer + "</font>"
#					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#					screen.show( szName )
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+ ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( szName )

				if CyGame().getWBMapScript():
					iCountSpecial += 1
					szName = "GoalTag"
					szBuffer= sf.getGoalTag(pPlayer)
#					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#					screen.show( szName )
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+ ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( szName )

				iCountSpecial += 1
				if pPlayer.getDisableProduction() > 0:
					iCountSpecial += 1
					szBuffer = u"<font=2>"
					szName = "DisableProductionTag"
					szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_DISABLE_PRODUCTION", (pPlayer.getDisableProduction(), ()), gc.getInfoTypeForString("COLOR_RED"))
					szBuffer = szBuffer + "</font>"
#					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#					screen.show( szName )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+(iCountSpecial*iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( szName )

				if pPlayer.getDisableResearch() > 0:
					iCountSpecial += 1
					szBuffer = u"<font=2>"
					szName = "DisableResearchTag"
					szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_DISABLE_RESEARCH", (pPlayer.getDisableResearch(), ()), gc.getInfoTypeForString("COLOR_RED"))
					szBuffer = szBuffer + "</font>"
#					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#					screen.show( szName )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+(iCountSpecial*iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( szName )

				if pPlayer.getDisableSpellcasting() > 0:
					iCountSpecial += 1
					szBuffer = u"<font=2>"
					szName = "DisableSpellcastingTag"
					szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_DISABLE_SPELLCASTING", (pPlayer.getDisableSpellcasting(), ()), gc.getInfoTypeForString("COLOR_RED"))
					szBuffer = szBuffer + "</font>"
					
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+(iCountSpecial*iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( szName )

				if pPlayer.getSanctuaryTimer() > 0:
					iCountSpecial += 1
					szBuffer = u"<font=2>"
					szName = "SanctuaryTimerTag"
					szBuffer = szBuffer + localText.getColorText("TXT_KEY_MESSAGE_SANCTUARY_TIMER", (pPlayer.getSanctuaryTimer(), ()), gc.getInfoTypeForString("COLOR_GREEN"))
					szBuffer = szBuffer + "</font>"

#					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, yCoord - ((iCount + iCountSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#					screen.show( szName )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 12, 100+(iCountSpecial*iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show( szName )

#FfH: End Add


# CCV - Position of Scores - START
				screen.setPanelSize( "ScoreBackground", xResolution - 21 - iWidth, yCoord - (iBtnHeight * iSelectCount) - 4, iWidth + 12, (iBtnHeight * iSelectCount) + 8 )
# CCV - Position of Scores - END

				screen.show( "ScoreBackground" )
# BUG - Align Icons - end


#FfH: Added by Kael 10/29/2007
	def updateManaStrings( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		global bshowManaBar

		screen.hide( "ManaBackground" )

		for szBonus in manaTypes1:
			szName = "ManaText" + szBonus
			screen.hide( szName )
#		for szBonus in manaTypes2:
#			szName = "ManaText" + szBonus
#			screen.hide( szName )

		iWidth = 0
		iCount = 0
		iBtnHeight = 18

		if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyEngine().isGlobeviewUp() == false and bshowManaBar == 1):
			for szBonus in manaTypes1:
				iBonus = gc.getInfoTypeForString(szBonus)
				szBuffer = u"<font=2>"
				szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
				szBuffer = szBuffer + szTempBuffer
				szBuffer = szBuffer + "</font>"
				if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
					iWidth = CyInterface().determineWidth( szBuffer )
				szName = "ManaText" + szBonus
				screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, MANA_X_POS + 40, MANA_Y_POS + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
				screen.show( szName )
				iCount = iCount + 1
			iCount = 0
#			for szBonus in manaTypes2:
#				iBonus = gc.getInfoTypeForString(szBonus)
#				szBuffer = u"<font=2>"
#				szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
#				szBuffer = szBuffer + szTempBuffer
#				szBuffer = szBuffer + "</font>"
#				if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
#					iWidth = CyInterface().determineWidth( szBuffer )
#				szName = "ManaText" + szBonus
#				screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 80, MANA_Y_POS + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
#				screen.show( szName )
#				iCount = iCount + 1
			screen.setPanelSize( "ManaBackground", MANA_X_POS, MANA_Y_POS + 18, iWidth + 12, (iBtnHeight * 21) + 12 )
			screen.show( "ManaBackground" )
#FfH: End Add

	# Will update the help Strings
	def updateHelpStrings( self ):
	
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL ):
			screen.setHelpTextString( "" )
		else:
			screen.setHelpTextString( CyInterface().getHelpString() )
		
		return 0
		
	# Will set the promotion button position
	def setPromotionButtonPosition( self, szName, iPromotionCount ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
# BUG - Stack Promotions - start
		x, y = self.calculatePromotionButtonPosition(screen, iPromotionCount)
		screen.moveItem( szName, x, y, -0.3 )
		return x, y
# BUG - Stack Promotions - end
	
	def calculatePromotionButtonPosition( self, screen, iPromotionCount ):
		yResolution = screen.getYResolution()
		return (266 - (24 * (iPromotionCount / 6)), yResolution - 144 + (24 * (iPromotionCount % 6)))

	# Will set the selection button position
	def setResearchButtonPosition( self, szButtonID, iCount ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()

# BUG - Bars on single line for higher resolution screens - start
		# lfgr fix 04/2021
		if self.isResearchBarWide() :
			xCoord = self.xResearchBarWide
		else:
			xCoord = self.xResearchBar

		iButtonWidth = 34
		iButtonsPerRow = RESEARCH_BAR_WIDTH // iButtonWidth
		screen.moveItem( szButtonID, xCoord + ( iButtonWidth * ( iCount % iButtonsPerRow ) ),
			( iButtonWidth * ( iCount / iButtonsPerRow ) ), -0.3 )
# BUG - Bars on single line for higher resolution screens - end

	# Will set the selection button position
	def setScoreTextPosition( self, szButtonID, iWhichLine ):
		
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			yCoord = yResolution - 180
		else:
			yCoord = yResolution - 88
		screen.moveItem( szButtonID, 996, yCoord - (iWhichLine * 18), -0.3 )

	# Will build the globeview UI
	def updateGlobeviewButtons( self ):
		kInterface = CyInterface()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()
		iCurrentLayerID = kGLM.getCurrentLayerID()
		
		# Positioning things based on the visibility of the globe
		if kEngine.isGlobeviewUp():

#FfH: Modified by Kael 07/17/2008
#			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
#FfH: End Modify

		else:
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):

#FfH: Modified by Kael 07/17/2008
#				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
#FfH: End Modify

			else:

#FfH: Modified by Kael 07/17/2008
#				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, 7, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
#FfH: End Modify
		
		# Set base Y position for the LayerOptions, if we find them	
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iGlobeLayerOptionsY_Minimal
		else:
			iY = yResolution - iGlobeLayerOptionsY_Regular

		# Hide the layer options ... all of them
		for i in range (20):
			szName = "GlobeLayerOption" + str(i)
			screen.hide(szName)

		# Setup the GlobeLayer panel
		iNumLayers = kGLM.getNumLayers()
		if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
			# set up panel
			if iCurrentLayerID != -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() != 0:
				bHasOptions = True		
			else:
				bHasOptions = False
				screen.hide( "ScoreBackground" )

#FfH: Added by Kael 10/29/2007
				screen.hide( "ManaBackground" )
#FfH: End Add

			# set up toggle button
			screen.setState("GlobeToggle", True)

			# Set GlobeLayer indicators correctly
			for i in range(kGLM.getNumLayers()):
				szButtonID = "GlobeLayer" + str(i)
				screen.setState( szButtonID, iCurrentLayerID == i )
				
			# Set up options pane
			if bHasOptions:
				kLayer = kGLM.getLayer(iCurrentLayerID)

				iCurY = iY
				iNumOptions = kLayer.getNumOptions()
				iCurOption = kLayer.getCurrentOption()
				iMaxTextWidth = -1
				for iTmp in range(iNumOptions):
					iOption = iTmp # iNumOptions - iTmp - 1
					szName = "GlobeLayerOption" + str(iOption)
					szCaption = kLayer.getOptionName(iOption)			
					if(iOption == iCurOption):
						szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
					else:
						szBuffer = "  %s  " % (szCaption)
					iTextWidth = CyInterface().determineWidth( szBuffer )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1 )
					screen.show( szName )

					iCurY -= iGlobeLayerOptionHeight

					if iTextWidth > iMaxTextWidth:
						iMaxTextWidth = iTextWidth

				#make extra space
				iCurY -= iGlobeLayerOptionHeight;
				iPanelWidth = iMaxTextWidth + 32
				iPanelHeight = iY - iCurY
				iPanelX = xResolution - 14 - iPanelWidth
				iPanelY = iCurY
				screen.setPanelSize( "ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
				screen.show( "ScoreBackground" )

#FfH: Added by Kael 10/29/2007
				screen.setPanelSize( "ManaBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
				screen.show( "ManaBackground" )
#FfH: End Add

		else:
			if iCurrentLayerID != -1:
				kLayer = kGLM.getLayer(iCurrentLayerID)
				if kLayer.getName() == "RESOURCES":
					screen.setState("ResourceIcons", True)
				else:
					screen.setState("ResourceIcons", False)

				if kLayer.getName() == "UNITS":
					screen.setState("UnitIcons", True)
				else:
					screen.setState("UnitIcons", False)
			else:
				screen.setState("ResourceIcons", False)
				screen.setState("UnitIcons", False)
				
			screen.setState("Grid", CyUserProfile().getGrid())
			screen.setState("BareMap", CyUserProfile().getMap())
			screen.setState("Yields", CyUserProfile().getYields())
			screen.setState("ScoresVisible", CyUserProfile().getScores())

			screen.hide( "InterfaceGlobeLayerPanel" )
			screen.setState("GlobeToggle", False )

	# Update minimap buttons
	def setMinimapButtonVisibility( self, bVisible):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		kInterface = CyInterface()
		kGLM = CyGlobeLayerManager()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( CyInterface().isCityScreenUp() ):
			bVisible = False
		
		kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
		kGlobeButtons = []
		for i in range(kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)
			kGlobeButtons.append(szButtonID)
		
		if bVisible:
			if CyEngine().isGlobeviewUp():
				kHide = kMainButtons
				kShow = kGlobeButtons
			else:
				kHide = kGlobeButtons
				kShow = kMainButtons
			screen.show( "GlobeToggle" )
			
		else:
			kHide = kMainButtons + kGlobeButtons
			kShow = []
			screen.hide( "GlobeToggle" )
		
		for szButton in kHide:
			screen.hide(szButton)
		
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iMinimapButtonsY_Minimal
			iGlobeY = yResolution - iGlobeButtonY_Minimal 
		else:
			iY = yResolution - iMinimapButtonsY_Regular
			iGlobeY = yResolution - iGlobeButtonY_Regular
			
		iBtnX = xResolution - 39
		screen.moveItem("GlobeToggle", iBtnX, iGlobeY, 0.0)
		
		iBtnAdvance = 28
		iBtnX = iBtnX - len(kShow)*iBtnAdvance - 10
		if len(kShow) > 0:		
			i = 0
			for szButton in kShow:
				screen.moveItem(szButton, iBtnX, iY, 0.0)
				screen.moveToFront(szButton)
				screen.show(szButton)
				iBtnX += iBtnAdvance
				i += 1
				
	
	def createGlobeviewButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		
		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()

		for i in range (kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)

			kLayer = kGLM.getLayer(i)
			szStyle = kLayer.getButtonStyle()
			
			if szStyle == 0 or szStyle == "":
				szStyle = "Button_HUDSmall_Style"
			
			screen.addCheckBoxGFC( szButtonID, "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_GLOBELAYER, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.setStyle( szButtonID, szStyle )
			screen.hide( szButtonID )
				
			
	def createMinimapButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.addCheckBoxGFC( "UnitIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_UNIT_ICONS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "UnitIcons", "Button_HUDGlobeUnit_Style" )
		screen.setState( "UnitIcons", False )
		screen.hide( "UnitIcons" )

		screen.addCheckBoxGFC( "Grid", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GRID).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Grid", "Button_HUDBtnGrid_Style" )
		screen.setState( "Grid", False )
		screen.hide( "Grid" )

		screen.addCheckBoxGFC( "BareMap", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_BARE_MAP).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "BareMap", "Button_HUDBtnClearMap_Style" )
		screen.setState( "BareMap", False )
		screen.hide( "BareMap" )

		screen.addCheckBoxGFC( "Yields", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_YIELDS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Yields", "Button_HUDBtnTileAssets_Style" )
		screen.setState( "Yields", False )
		screen.hide( "Yields" )

		screen.addCheckBoxGFC( "ScoresVisible", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_SCORES).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ScoresVisible", "Button_HUDBtnRank_Style" )
		screen.setState( "ScoresVisible", True )
		screen.hide( "ScoresVisible" )

		screen.addCheckBoxGFC( "ResourceIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RESOURCE_ALL).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ResourceIcons", "Button_HUDBtnResources_Style" )
		screen.setState( "ResourceIcons", False )
		screen.hide( "ResourceIcons" )
		
		screen.addCheckBoxGFC( "GlobeToggle", "", "", -1, -1, 36, 36, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GLOBELAYER).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "GlobeToggle", "Button_HUDZoom_Style" )
		screen.setState( "GlobeToggle", False )
		screen.hide( "GlobeToggle" )

# < Revolution Mod Start >
	def showRevWatchInfoPane(self):
		#CyInterface().addImmediateMessage( "Showing Rev Watch info pane","" )
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Defining the size of the info pane
		InfoPaneX = 8
		InfoPaneY = screen.getYResolution() - 200
		InfoPaneWidth = 264
		InfoPaneHeight = 30

		screen.addPanel( "REV_WATCH_PANE", u"", u"", True, True, \
						InfoPaneX, InfoPaneY, InfoPaneWidth, InfoPaneHeight, \
						PanelStyles.PANEL_STYLE_HUD_HELP )

		# create text
		szText = "<font=2>" + localText.getText("TXT_KEY_REV_WATCH_INFO_PANE", ()) + "</font=2>"


		# create shadow text
		szTextBlack = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_BLACK"))

		# display shadow text
		screen.addMultilineText( "REV_WATCH_TEXT_SHADOW", szTextBlack, \
								InfoPaneX +6, InfoPaneY +6, \
								InfoPaneWidth -3, InfoPaneHeight- 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)


		# display text
		screen.addMultilineText( "REV_WATCH_TEXT", szText, \
								InfoPaneX +5, InfoPaneY +5, \
								InfoPaneWidth -3, InfoPaneHeight- 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)

	def hideRevWatchInfoPane(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide("REV_WATCH_TEXT")
		screen.hide("REV_WATCH_TEXT_SHADOW")
		screen.hide("REV_WATCH_PANE")


	def showRevStatusInfoPane(self): # LFGR_TODO: Replace this by a normal popup, best outsource to RevIdxUtils
		# lfgr 05/2023: Improved and cleaned up
		
		import RevIdxUtils # LFGR_TODO?
		
		pCity = CyInterface().getHeadSelectedCity()
		pPlayerCache = RevIdxUtils.PlayerRevIdxCache( pCity.getOwner() )
		pCityHelper = RevIdxUtils.CityRevIdxHelper( pCity, pPlayerCache )

		szText = "<font=2>"
		# LFGR_TODO: Should clicking instead lead to the advisor?
		if pCity.getOwner() == CyGame().getActivePlayer() :
			szText += localText.getText( "TXT_KEY_REV_STATUS_HEADER", () )
		else :
			szText += "=========================="
		
		szText += u"\n" + pCityHelper.computeRevIdxPopupHelp()
		
		szText += "</font=2>"
		
		self.PLE.displayInfoPane(szText)

	def hideRevStatusInfoPane(self):
		# screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		# screen.hide("REV_STATUS_TEXT")
		# screen.hide("REV_STATUS_PANE")

		self.PLE.hideInfoPane()

	def changeScoreboardDisplay( self ) :
		global iMaxScoreLines

		if( iMaxScoreLines < gc.getMAX_CIV_PLAYERS() ) :
			iMaxScoreLines = gc.getMAX_CIV_PLAYERS() + 1
		else :
			iMaxScoreLines = isMaxScoreLines()

		self.updateScoreStrings()
# < Revolution Mod End >
# < BUG Button Start >
	def showBugOptionsScreen(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

	def hideBugOptionsScreen(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

# < BUG Button End >
	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
# BUG - PLE - start
		if  (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) or \
			(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) or \
			(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (self.MainInterfaceInputMap.has_key(inputClass.getFunctionName())):
				return self.MainInterfaceInputMap.get(inputClass.getFunctionName())(inputClass)
			if (self.MainInterfaceInputMap.has_key(inputClass.getFunctionName() + "1")):
				return self.MainInterfaceInputMap.get(inputClass.getFunctionName() + "1")(inputClass)
# BUG - PLE - end

# BUG - BUG Option Button - Start
			if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
				if inputClass.getFunctionName() == "BUGOptionsScreenWidget":
					BugOptionsScreen.showOptionsScreen()
					return 1
# BUG - BUG Option Button - End


# BUG - Raw Yields - start
		if (inputClass.getFunctionName().startswith("RawYields")):
			return self.handleRawYieldsButtons(inputClass)
# BUG - Raw Yields - end

# BUG - Great Person Bar - start
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName().startswith("GreatPersonBar")):
			# Zoom to next GP city
			iCity = inputClass.getData1()
			if (iCity == -1):
				pCity, _ = GPUtil.findNextCity()
			else:
				pCity = gc.getActivePlayer().getCity(iCity)
			if pCity and not pCity.isNone():
				CyInterface().selectCity(pCity, False)
			return 1
# BUG - Great Person Bar - end

		global bshowManaBar
# BUG - field of view slider - start
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_SLIDER_NEWSTOP):
			if (inputClass.getFunctionName() == self.szSliderId):
				screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
				self.iField_View = inputClass.getData() + 1
				self.setFieldofView(screen, False)
				self.setFieldofView_Text(screen)
				MainOpt.setFieldOfView(self.iField_View)
# BUG - field of view slider - end

# CCV - Position of Scores - START
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_SLIDER_NEWSTOP):
			if (inputClass.getFunctionName() == self.szScoreSliderId):
				screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
				self.iScore_View = inputClass.getData() + 1
				self.iScoreStart = self.iScore_View
				self.setScrollingScoreboard(screen, False)
				self.setScrollingScoreboard_Text(screen)				
# CCV - Position of Scores - END

# < Revolution Mod Start >
		#CyInterface().addImmediateMessage( "Handling input from %s, type %d"%(inputClass.getFunctionName(),inputClass.getNotifyCode()),"")
		if( game.isOption(GameOptionTypes.GAMEOPTION_REVOLUTIONS) and not RevInstances.RevolutionInst == None ) :
			if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and inputClass.getFunctionName() == "RevWatchButton"):
				self.showRevWatchInfoPane()
			elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and inputClass.getFunctionName() == "RevWatchButton"):
				self.hideRevWatchInfoPane()

			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "RevWatchButton"):
				CvScreensInterface.showRevolutionWatchAdvisor(self)

			if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and inputClass.getFunctionName() == "RevStatusButton"):
				self.showRevStatusInfoPane()
			elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and inputClass.getFunctionName() == "RevStatusButton"):
				self.hideRevStatusInfoPane()

			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "RevStatusButton"):
				if( CyInterface().getHeadSelectedCity().getOwner() == CyGame().getActivePlayer() ) :
					RevInstances.RevolutionInst.showBribeCityPopup(CyInterface().getHeadSelectedCity())
					self.hideRevStatusInfoPane()

			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "ExtraCivSeparator"):
				self.changeScoreboardDisplay()
# < Revolution Mod End >

# < BUG Button Start >
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and inputClass.getFunctionName() == "BUGButton"):
			self.showBugOptionsScreen()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and inputClass.getFunctionName() == "BUGButton"):
			self.hideBugOptionsScreen()
			
		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "BUGButton"):
			self.showBugOptionsScreen()
# < BUG Button Mod End >

		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and inputClass.getFunctionName() == "RawManaButton"):
			screen.show("ManaToggleHelpText")
			screen.show("ManaToggleHelpTextPanel")
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and inputClass.getFunctionName() == "RawManaButton"):
			screen.hide("ManaToggleHelpText")
			screen.hide("ManaToggleHelpTextPanel")

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "RawManaButton"):
			if (bshowManaBar == 1):
				bshowManaBar = 0
				self.updateManaStrings()
				return 1
			else:
				bshowManaBar = 1
				self.updateManaStrings()
				return 1

		return 0

# BUG - Raw Yields - start
	def handleRawYieldsButtons(self, inputClass):
		iButton = inputClass.getID()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON):
			self.PLE.displayHelpHover(RAW_YIELD_HELP[iButton])
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			self.PLE.hideInfoPane()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			global g_bYieldView
			global g_iYieldType
			global g_iYieldTiles
			if iButton == 0:
				g_bYieldView = False
			elif iButton in (1, 2, 3):
				g_bYieldView = True
				g_iYieldType = RawYields.YIELDS[iButton - 1]
			elif iButton in (4, 5, 6):
				g_bYieldView = True
				g_iYieldTiles = RawYields.TILES[iButton - 4]
			else:
				return 0
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, True)
			return 1
		return 0
# BUG - Raw Yields - end

	def update(self, fDelta):
		return
	
	def forward(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_NEXTCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_NEXTUNIT)
		
	def back(self):
		if (not CyInterface().isFocused() or CyInterface().isCityScreenUp()):
			if (CyInterface().isCitySelection()):
				CyGame().doControl(ControlTypes.CONTROL_PREVCITY)
			else:
				CyGame().doControl(ControlTypes.CONTROL_PREVUNIT)

# BUG - field of view slider - start
	def setFieldofView(self, screen, bDefault):
		if bDefault or not MainOpt.isShowFieldOfView():
			self._setFieldofView(screen, DEFAULT_FIELD_OF_VIEW)
		else:
			self._setFieldofView(screen, self.iField_View)

	def _setFieldofView(self, screen, iFoV):
		if self.iField_View_Prev != iFoV:
			gc.setDefineFLOAT("FIELD_OF_VIEW", float(iFoV))
			self.iField_View_Prev = iFoV

	def setFieldofView_Text(self, screen):
		zsFieldOfView_Text = "%s [%i]" % (self.sFieldOfView_Text, self.iField_View)
		screen.setLabel(self.szSliderTextId, "", zsFieldOfView_Text, CvUtil.FONT_RIGHT_JUSTIFY, self.iX_FoVSlider, self.iY_FoVSlider + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
# BUG - field of view slider - end

# CCV - Position of Scores - START
	def setScrollingScoreboard(self, screen, bDefault):
		if (bDefault):
			self._setScrollingScoreboard(screen, 1)
		else:
			self._setScrollingScoreboard(screen, self.iScore_View)

	def _setScrollingScoreboard(self, screen, iScores):
		if self.iScrollingScoreboard_Prev != iScores:
			gc.setDefineFLOAT("SCROLLING_SCOREBOARD",float(iScores))
			self.iScrollingScoreboard_Prev = iScores
			self.updateScoreStrings()
			screen.setForcedRedraw(True)

	def setScrollingScoreboard_Text(self, screen):
		zsScrollingScoreboard_Text = "%s [%i]" % (self.sScrollingScoreboard_Text, self.iScore_View)
		self.iX_ScoreSlider = self.xResolution - 120
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
			self.iY_ScoreSlider = screen.getYResolution() - 200
		else:
			self.iY_ScoreSlider = screen.getYResolution() - 82		
		screen.setLabel(self.szScoreSliderTextId, "", zsScrollingScoreboard_Text, CvUtil.FONT_RIGHT_JUSTIFY, self.iX_ScoreSlider, self.iY_ScoreSlider + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def updateScrollingScoreboard(self, screen):
		screen.hide(self.szScoreSliderTextId)
		screen.hide(self.szScoreSliderId)
		
		self.setScrollingScoreboard_Text(screen)

		self.iX_ScoreSlider = self.xResolution - 120
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart()):
			self.iY_ScoreSlider = screen.getYResolution() - 200
		else:
			self.iY_ScoreSlider = screen.getYResolution() - 82		
		
		iW = 100
		iH = 15
		screen.addSlider(self.szScoreSliderId, self.iX_ScoreSlider + 5, self.iY_ScoreSlider, iW, iH, self.iScore_View - 1, 0, self.iScoreStartMax - 1, WidgetTypes.WIDGET_GENERAL, -1, -1, False);
				
		screen.hide(self.szScoreSliderTextId)
		screen.hide(self.szScoreSliderId)
				
		if (self.checkScrollingScoreboard() == True):							
			screen.show(self.szScoreSliderTextId)
			screen.show(self.szScoreSliderId)	

	def checkScrollingScoreboard(self):
		iPreCount = 0
		i = gc.getMAX_CIV_TEAMS() - 1
		while (i > -1):
			eTeam = gc.getGame().getRankTeam(i)

			if (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam) or gc.getTeam(eTeam).isHuman() or gc.getGame().isDebugMode()):
						
				j = gc.getMAX_CIV_PLAYERS() - 1
				while (j > -1):
					ePlayer = gc.getGame().getRankPlayer(j)

					if (not CyInterface().isScoresMinimized() or gc.getGame().getActivePlayer() == ePlayer):
						if (gc.getPlayer(ePlayer).isEverAlive() and not gc.getPlayer(ePlayer).isBarbarian()
							and (gc.getPlayer(ePlayer).isAlive() or ScoreOpt.isShowDeadCivs())):
							if (not gc.getPlayer(ePlayer).isMinorCiv() or ScoreOpt.isShowMinorCivs()):
								if (gc.getPlayer(ePlayer).getTeam() == eTeam):									
									iPreCount = iPreCount + 1
					j = j - 1
			i = i - 1
		if (iPreCount > ScoreOpt.getMaxPlayers() and ScoreOpt.getMaxPlayers() > 0):
			return True
		else:
			return False

# CCV - Position of Scores - END
