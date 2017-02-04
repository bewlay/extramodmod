#
#   FILE:       Discworld.py
#   AUTHOR:     Terkhen
#   PURPOSE:    Generates a flat world shaped like a disc, with warm regions near the border and cold regions in the center. Based on the Discworld novels by Terry Pratchett.
#-----------------------------------------------------------------------------
# CHANGELOG
#-----------------------------------------------------------------------------
#   0.1.0:
#       - Initial release.


from CvPythonExtensions import *
import CvMapGeneratorUtil
import math
import sys

# Global values that determine how the MapScript works.


fSnowRadius = 0.10
"""
Amount of the Discworld radius in which the terrain will be snow.
"""


fTundraRadius = 0.25
"""
Amount of the Discworld radius in which the terrain will be tundra.
"""


iTerrainGrain = 3
"""
Grain used for terrainVarFractal.
"""


iFeatureGrain = 4
"""
Grain used for featuresVarFractal.
"""


lStartingPlotAreas = list()
"""
List of map area polygons (see MapAreaPolygon class definition in this file) in which civilizations can start playing
the game.
"""


map = CyGlobalContext().getMap()
"""
Access to map global context.
"""


game = CyGlobalContext().getGame()
"""
Access to game global context.
"""

terrainVarFractal = None
"""
Fractal used to introduce random variations to terrain types depending on their distance to the center of the disc.
"""


featuresVarFractal = None
"""
Fractal used to introduce random variations to feature types depending on their distance to the center of the disc.
"""


def isAdvancedMap():
	"""
	This map should not show up in simple mode.
	:return: The map is an advanced map.
	"""
	return 1


def isClimateMap():
	"""
	Discworld uses the climate options.
	:return: True
	"""
	return True


def isSeaLevelMap():
	"""
	Discworld uses the sea level options.
	:return: True
	"""
	return True


def getGridSize(argsList):
	"""
	In a Discworld, the playable area is reduced as the corners of the rectangle are cut to form a round border. The
	grid size is scaled up to let the disc have the same playable area than a rectangular map of the same world size.
	:param argsList: List containing the chosen world size as its single element. This element can be -1 on loads.
	:return: tuple with the chosen map width and height.
	"""
	print "[DISCWORLD] -- getGridSize()"
	if argsList[0] == -1: return [] # (-1,) is passed to function on loads

	[eWorldSize] = argsList
	# Discworld map should have a similar playable area than the chosen world size.
	iOrigWidth = CyGlobalContext().getWorldInfo(eWorldSize).getGridWidth()
	iOrigHeight = CyGlobalContext().getWorldInfo(eWorldSize).getGridHeight()
	iOrigArea = iOrigWidth * iOrigHeight
	# Discworld is a disc and not a rectangle, though.
	iDiscDiameter = int(math.ceil(2 * math.sqrt(iOrigArea / math.pi)))

	return iDiscDiameter, iDiscDiameter


def getWrapX():
	"""
	The Discworld is flat.
	:return: False
	"""
	return False


def getWrapY():
	"""
	The Discworld is flat.
	:return: False
	"""
	return False


def isBonusIgnoreLatitude():
	"""
	The latitude calculations made in Civilization IV are not appropiate for placing bonuses on a flat disc.
	:return:
	"""
	return True


def generatePlotTypes():
	"""
	Generates the PlotTypes for all plots in the map. See DiscworldMultilayeredFractal for details. This method also
	creates the border of the Discworld.
	:return: List of the PlotTypes generated for each plot of the map.
	"""
	print "[DISCWORLD] -- generatePlotTypes()"

	plotGenerator = DiscworldMultilayeredFractal()
	plotTypes = plotGenerator.generatePlotsByRegion()

	# Create Discworld border first pass: water.
	for iX in range(map.getGridWidth()):
		for iY in range(map.getGridHeight()):
			if isOutsideDisc(iX, iY):
				plotTypes[iY * map.getGridWidth() + iX] = PlotTypes.PLOT_OCEAN

	return plotTypes


def generateTerrainTypes():
	"""
	Generates terrain types for all the plots of the map. They are created as if the maximum "latitude" is at the center
	of the disc, while it reaches 0 at its borders.
	:return: List of generated terrain types.
	"""
	print "[DISCWORLD] -- generateTerrainTypes()"

	global terrainVarFractal
	terrainVarFractal = getVariationFractal(iTerrainGrain)
	terrainGen = DiscworldTerrainGenerator(fSnowLatitude = 1.0 - fSnowRadius, fTundraLatitude = 1.0 - fTundraRadius)
	terrainTypes = terrainGen.generateTerrain()

	return terrainTypes


def addFeatures():
	"""
	Generates feature types for all the plots of the map. They are created as if the maximum "latitude" is at the center
	of the disc, while it reaches 0 at its borders.
	This method also removes all rivers from the peak area used to represent the area outside of the disc.
	:return: 0
	"""
	print "[DISCWORLD] -- addFeatures()"

	# Create Discworld border second pass: Add ice.
	iFeatureIce = CyGlobalContext().getInfoTypeForString("FEATURE_ICE")
	for iX in range(map.getGridWidth()):
		for iY in range(map.getGridHeight()):
			if isOutsideDisc(iX, iY):
				map.plot(iX, iY).setFeatureType(iFeatureIce, -1)

	# Add other features.
	global featuresVarFractal
	featuresVarFractal = getVariationFractal(iFeatureGrain)
	featureGen = DiscworldFeatureGenerator()
	featureGen.addFeatures()

	return 0


def findStartingPlot(argsList):
	"""
	Find starting plot for a certain player. Civilizations are only allowed to start in the main continent or in the
	counterweight continent.
	:param argsList: List that contains the playerID of the player.
	:return: Starting plot
	"""
	[playerID] = argsList

	def isInsidePlayableRegion(pID, iX, iY):
		global lStartingPlotAreas
		for mapAreaPolygon in lStartingPlotAreas:
			if mapAreaPolygon.isInside(iX, iY):
				return True

		return False

	return CvMapGeneratorUtil.findStartingPlot(playerID, isInsidePlayableRegion)


# All utility classes and methods used by the MapScript are implemented below.


class DiscworldMultilayeredFractal(CvMapGeneratorUtil.MultilayeredFractal):
	"""
	Multilayered fractal customized for Discworld. The world should always have a mountainous central region, a big
	continent with a smaller counterweight continent in the opposite side of the disc and some random islands.

	Along with MapAreaPolygon, this implementation of MultilayeredFractal allows to place regions with arbitrary
	polygonal shapes, and to rotate them along the center of the disc for any angle. These shapes are distorted and
	randomized slightly to make them appear more natural (see MapAreaPolygon).
	"""


	def generatePlotsByRegion(self):
		"""
		Generate all of the regions of the Discworld.
		:return: Plots generated.
		"""
		# Remove all elements from the starting plot areas list.
		del lStartingPlotAreas[:]
		iBaseSeaLevel = 70 + self.gc.getSeaLevelInfo(self.map.getSeaLevel()).getSeaLevelChange()
		# Each region of the Discworld has a separate method for creating it.
		self.generatePlotsCentralHub(iBaseSeaLevel)
		# generatePlotsMainContinent also determines the angle in which most of the land will be.
		fMainAngle = self.generatePlotsMainContinent(iBaseSeaLevel)
		self.generatePlotsCounterweightContinent(iBaseSeaLevel, fMainAngle)
		fIslandsAngle = self.generatePlotsIslands(fMainAngle)
		# XXXX
		self.generatePlotsXXXX(iBaseSeaLevel, fIslandsAngle)

		return self.wholeworldPlotTypes


	def generatePlotsCentralHub(self, iBaseSeaLevel):
		"""
		The central hub is a mountainous region in the center of the disc.
		:param iBaseSeaLevel: Base sea level.
		"""
		iCentralHubGrain = 3
		iCentralHubHillsGrain = 1

		# The real center should always be land.
		iCentralHubCoreSizeX = int(self.iW * fSnowRadius * 0.7)
		iCentralHubCoreSizeY = int(self.iH * fSnowRadius * 0.7)
		iCentralHubCoreWestLon = int((self.iW / 2.0) - int(iCentralHubCoreSizeX / 2.0))
		iCentralHubCoreSouthLat = int((self.iH / 2.0) - int(iCentralHubCoreSizeY / 2.0))
		self.generatePlotsInRegion(
			iBaseSeaLevel - 60,
			iCentralHubCoreSizeX,
			iCentralHubCoreSizeY,
			iCentralHubCoreWestLon,
			iCentralHubCoreSouthLat,
			iCentralHubGrain,
			iCentralHubHillsGrain,
			self.iRoundFlags,
			self.iTerrainFlags,
			CyFractal.FracVals.DEFAULT_FRAC_Y_EXP,
			CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)

		iCentralHubSizeX = int(self.iW * fSnowRadius * 1.8)
		iCentralHubSizeY = int(self.iH * fSnowRadius * 1.8)
		iCentralHubWestLon = int((self.iW / 2.0) - int(iCentralHubSizeX / 2.0))
		iCentralHubSouthLat = int((self.iH / 2.0) - int(iCentralHubSizeY / 2.0))

		# The terrain near the center is sparse.
		self.generatePlotsInRegion(
			iBaseSeaLevel + 10,
			iCentralHubSizeX,
			iCentralHubSizeY,
			iCentralHubWestLon,
			iCentralHubSouthLat,
			iCentralHubGrain,
			iCentralHubHillsGrain,
			self.iRoundFlags,
			self.iTerrainFlags,
			CyFractal.FracVals.DEFAULT_FRAC_Y_EXP,
			CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)


	def generatePlotsMainContinent(self, iBaseSeaLevel):
		"""
		The main continent is the biggest landmass in the Discworld. It surrounds most of the hub, and the rest of the
		land is in a general direction determined by mainAngle.
		:param iBaseSeaLevel: Base sea level.
		:return: Angle in radians in which the land of the main continent will be placed.
		"""
		iMainContinentGrain = 2
		iMainContinentHillsGrain = 4

		# Determine the main angle randomly.
		fMainAngle = math.radians(game.getMapRand().get(360, "[DiscWorld] - Angle of the main continent."))

		# Define the area occupied by the main continent.
		fMiddleX = self.iW / 2.0
		fMiddleY = self.iH / 2.0
		fCentralHubSizeX = self.iW * fSnowRadius * 1.2

		lMainContinentPolygon = [
			[fMiddleX - fCentralHubSizeX, fMiddleY],
			[fMiddleX + fCentralHubSizeX, fMiddleY],
			[fMiddleX + fMiddleX / 1.67, fMiddleY - fMiddleY / 3.0],
			[fMiddleX + fMiddleX / 2.25, fMiddleY - fMiddleY / 1.25],
			[fMiddleX - fMiddleX / 2.25, fMiddleY - fMiddleY / 1.25],
			[fMiddleX - fMiddleX / 1.67, fMiddleY - fMiddleY / 3.0],
		]

		# Create the map area polygon.
		mainContinentMapArea = MapAreaPolygon("Main Continent", lMainContinentPolygon, fMainAngle)

		# Add the area to the list of regions in which civilizations can start.
		global lStartingPlotAreas
		lStartingPlotAreas.append(mainContinentMapArea)

		self.generatePlotsInMapAreaPolygon(
			iBaseSeaLevel - 15, mainContinentMapArea, iMainContinentGrain, iMainContinentHillsGrain, self.iRoundFlags,
			self.iTerrainFlags, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)

		return fMainAngle


	def generatePlotsCounterweightContinent(self, iBaseSeaLevel, fMainAngle):
		"""
		The counterweight continent is smaller than the main one, and placed in roughly the opposite direction.
		:param iBaseSeaLevel: Base sea level.
		:param fMainAngle: Angle in radians in which most of the land of the main continent is placed.
		"""
		iCounterweightContinentGrain = 2
		iCounterweightContinentHillsGrain = 3

		# The counterweight continent is situated roughly in the opposite direction of the main continent...
		fCounterAngle = fMainAngle +  math.radians(180)
		# ... with some randomization, of course. Who wants a predictable world?
		fCounterAngle += math.radians(game.getMapRand().get(40, "[DiscWorld] - Randomization of the angle of the counterweight continent.") - 20.0)

		# Define the area occupied by the counterweight continent.
		fMiddleX = self.iW / 2.0

		if game.getMapRand().get(2, "[DiscWorld] - Randomization of the angle of the islands.") == 0:
			fLeftDisplacement = self.iW / 7.0
			fRightDisplacement = self.iW / 10.0
		else:
			fLeftDisplacement = self.iW / 10.0
			fRightDisplacement = self.iW / 7.0

		fPeninsulaWidth = max(4.0, self.iW / 15.0)
		fLowestHeight = self.iH / 8.0
		fBiggestHeight = self.iH / 3.5
		fPeninsulaHeight = self.iH / 3.0

		lCounterContPolygon = [
			# Roughly rectangular area, not centered.
			[fMiddleX - fLeftDisplacement, fBiggestHeight],
			[fMiddleX - fLeftDisplacement, fLowestHeight],
			[fMiddleX + fRightDisplacement, fLowestHeight],
			[fMiddleX + fRightDisplacement ,fBiggestHeight],
			# Peninsula closer to the hub, centered.
			[fMiddleX + fPeninsulaWidth, fBiggestHeight],
			[fMiddleX + fPeninsulaWidth, fPeninsulaHeight],
			[fMiddleX - fPeninsulaWidth, fPeninsulaHeight],
			[fMiddleX - fPeninsulaWidth, fBiggestHeight],
		]

		# Create the map area polygon.
		counterweightContinentMapArea = MapAreaPolygon("Counterweight Continent", lCounterContPolygon, fCounterAngle)

		# Add the area to the list of regions in which civilizations can start.
		global lStartingPlotAreas
		lStartingPlotAreas.append(counterweightContinentMapArea)

		self.generatePlotsInMapAreaPolygon(
			iBaseSeaLevel - 20, counterweightContinentMapArea, iCounterweightContinentGrain,
			iCounterweightContinentHillsGrain, self.iRoundFlags, self.iTerrainFlags,
			CyFractal.FracVals.DEFAULT_FRAC_Y_EXP, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)


	def generatePlotsIslands(self, fMainAngle):
		"""
		Region with small islands.
		:param iBaseSeaLevel: Base sea level.
		:param fMainAngle: Angle in radians in which most of the land of the main continent is placed.
		:return: Direction in which the islands lay, as the XXXX will be in the opposite direction.
		"""
		iIslandsGrain = 4
		iIslandsHillsGrain = 3

		# The islands may be at the right or at the left of the main continent.
		fIslandsAngle = fMainAngle
		if game.getMapRand().get(2, "[DiscWorld] - Randomization of the angle of the islands.") == 0:
			fIslandsAngle += math.radians(90)
		else:
			fIslandsAngle -= math.radians(90)

		# Define the area occupied by the islands.
		fMiddleX = self.iW / 2.0
		fMiddleY = self.iH / 2.0

		lIslandsPolygon = [
			[self.iW / 6.0, 0.0],
			[fMiddleX - fMiddleX / 5.0, fMiddleY - fMiddleY / 5.0],
			[fMiddleX + fMiddleX / 5.0, fMiddleY - fMiddleY / 5.0],
			[self.iW - self.iW / 6.0, 0.0],
		]

		# Create the map area polygon.
		islandsMapArea = MapAreaPolygon("Islands", lIslandsPolygon, fIslandsAngle)

		self.generatePlotsInMapAreaPolygon(
			90, islandsMapArea, iIslandsGrain, iIslandsHillsGrain, self.iRoundFlags,
			self.iTerrainFlags, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)

		return fIslandsAngle


	def generatePlotsXXXX(self, iBaseSeaLevel, fIslandsAngle):
		"""
		XXXX
		:param iBaseSeaLevel: Base sea level.
		:param fMainAngle: Angle in radians in which the islands are placed.
		"""

		iXXXXGrain = 2
		iXXXXHillsGrain = 3

		fXXXXAngle = fIslandsAngle +  math.radians(180)
		fXXXXAngle += math.radians(game.getMapRand().get(20, "[DiscWorld] - XXXX") - 10.0)

		fMiddleX = self.iW / 2.0

		lXXXXPolygon = [
			[fMiddleX - self.iW / 8.0, 0.0],
			[fMiddleX + self.iW / 8.5, 0.0],
			[fMiddleX + self.iW / 8.5, self.iH / 6.0],
			[fMiddleX - self.iW / 8.0, self.iH / 6.0],
		]

		xxxxMapArea = MapAreaPolygon("XXXX", lXXXXPolygon, fXXXXAngle)

		self.generatePlotsInMapAreaPolygon(
			iBaseSeaLevel, xxxxMapArea, iXXXXGrain, iXXXXHillsGrain, self.iRoundFlags, self.iTerrainFlags,
			CyFractal.FracVals.DEFAULT_FRAC_Y_EXP, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)


	def generatePlotsInMapAreaPolygon(self, iWaterPercent, mapArea, iRegionGrain, iRegionHillsGrain, iRegionPlotFlags,
	                                  iRegionTerrainFlags, iRegionFracXExp = -1, iRegionFracYExp = -1):
		"""
		Generate plots in a region that is not a rectangle, but an arbitrary polygon. See MapAreaPolygon for details.
		:param iWaterPercent:
		:param mapArea: Polygonal shape inside which the region will be created.
		:type mapArea: MapAreaPolygon
		:param iRegionGrain: Fractal grain used for generating the terrain.
		:param iRegionHillsGrain: Fractal grain used for generating hills and peaks.
		:param iRegionPlotFlags: Flags used for the plot fractal.
		:param iRegionTerrainFlags: Flags used for the hills and peaks fractals.
		:param iRegionFracXExp:
		:param iRegionFracYExp:
		:return:
		"""
		# Obtain size and position from the map area.
		iRegionWidth = mapArea.iRegionWidth
		iRegionHeight = mapArea.iRegionHeight
		fMinX = mapArea.fMinX
		fMinY = mapArea.fMinY

		# Init the plot types array and the regional fractals
		self.plotTypes = [] # reinit the array for each pass
		self.plotTypes = [PlotTypes.PLOT_OCEAN] * (iRegionWidth * iRegionHeight)
		regionContinentsFrac = CyFractal()
		regionHillsFrac = CyFractal()
		regionPeaksFrac = CyFractal()
		regionContinentsFrac.fracInit(iRegionWidth, iRegionHeight, iRegionGrain, self.dice, iRegionPlotFlags, iRegionFracXExp, iRegionFracYExp)
		regionHillsFrac.fracInit(iRegionWidth, iRegionHeight, iRegionHillsGrain, self.dice, iRegionTerrainFlags, iRegionFracXExp, iRegionFracYExp)
		regionPeaksFrac.fracInit(iRegionWidth, iRegionHeight, iRegionHillsGrain+1, self.dice, iRegionTerrainFlags, iRegionFracXExp, iRegionFracYExp)

		iWaterThreshold = regionContinentsFrac.getHeightFromPercent(iWaterPercent)
		iHillsBottom1 = regionHillsFrac.getHeightFromPercent(max((25 - self.gc.getClimateInfo(self.map.getClimate()).getHillRange()), 0))
		iHillsTop1 = regionHillsFrac.getHeightFromPercent(min((25 + self.gc.getClimateInfo(self.map.getClimate()).getHillRange()), 100))
		iHillsBottom2 = regionHillsFrac.getHeightFromPercent(max((75 - self.gc.getClimateInfo(self.map.getClimate()).getHillRange()), 0))
		iHillsTop2 = regionHillsFrac.getHeightFromPercent(min((75 + self.gc.getClimateInfo(self.map.getClimate()).getHillRange()), 100))
		iPeakThreshold = regionPeaksFrac.getHeightFromPercent(self.gc.getClimateInfo(self.map.getClimate()).getPeakPercent())

		# Loop through the region's plots
		for iRegionX in range(iRegionWidth):
			for iRegionY in range(iRegionHeight):
				val = regionContinentsFrac.getHeight(iRegionX, iRegionY)
				if val <= iWaterThreshold:
					pass
				else:
					# Checking if the plot is inside the polygon is expensive, so it is done here at the last possible
					# chance.
					if mapArea.isInside(iRegionX + fMinX, iRegionY + fMinY):
						iPlotIndex = iRegionY * iRegionWidth + iRegionX
						hillVal = regionHillsFrac.getHeight(iRegionX, iRegionY)
						if hillVal >= iHillsBottom1 and hillVal <= iHillsTop1 or hillVal >= iHillsBottom2 and hillVal <= iHillsTop2:
							peakVal = regionPeaksFrac.getHeight(iRegionX, iRegionY)
							if peakVal <= iPeakThreshold:
								self.plotTypes[iPlotIndex] = PlotTypes.PLOT_PEAK
							else:
								self.plotTypes[iPlotIndex] = PlotTypes.PLOT_HILLS
						else:
							self.plotTypes[iPlotIndex] = PlotTypes.PLOT_LAND

		# Apply the region's plots to the global plot array.
		for iRegionX in range(iRegionWidth):
			iWholeworldX = int(iRegionX + fMinX)
			if iWholeworldX < 0 or iWholeworldX > (self.iW - 1):
				continue
			for iRegionY in range(iRegionHeight):
				iWholeworldY = int(iRegionY + fMinY)
				if iWholeworldY < 0 or iWholeworldY > (self.iH - 1):
					continue
				iPlotIndex = iRegionY * iRegionWidth + iRegionX
				if self.plotTypes[iPlotIndex] == PlotTypes.PLOT_OCEAN:
					continue
				iWorld = iWholeworldY * self.iW + iWholeworldX
				self.wholeworldPlotTypes[iWorld] = self.plotTypes[iPlotIndex]

		# This region is done.
		return


class DiscworldTerrainGenerator(CvMapGeneratorUtil.TerrainGenerator):
	"""
	Terrain generator customized for Discworld. This means creating terrain as if the "latitude" is maximum at the
	center, and it decreases progressively until it reaches 0 right at the border.
	"""

	def getLatitudeAtPlot(self, iX, iY):
		"""
		Given a plot (iX,iY) such that (0,0) is in the NW, returns a value between 0.0 (tropical) and 1.0 (polar). In
		Discworld, this "latitude" is altered to represent the inverted distance from the center to the chosen plot,
		where 0.0 means the border and 1.0 means the center.
		:param iX: x coordinate of the plot
		:param iY: y coordinate of the plot.
		:return: Calculated latitude.
		"""
		return getInvertedDistanceToCenter(iX, iY, terrainVarFractal)


class DiscworldFeatureGenerator(CvMapGeneratorUtil.FeatureGenerator):
	"""
	Feature generator customized for Discworld. This means placing features as if the "latitude" is maximum at the
	center, and it decreases progressively until it reaches 0 right at the border. Also, Discworld needs to have
	less ice than normal maps. Otherwise, the ice will clutter the center of the disc.
	"""

	def getLatitudeAtPlot(self, iX, iY):
		"""
		Given a plot (iX,iY) such that (0,0) is in the NW, returns a value between 0.0 (tropical) and 1.0 (polar). In
		Discworld, this "latitude" is altered to represent the inverted distance from the center to the chosen plot,
		where 0.0 means the border and 1.0 means the center.
		:param iX: x coordinate of the plot.
		:param iY: y coordinate of the plot.
		:return: Calculated latitude.
		"""
		return getInvertedDistanceToCenter(iX, iY, featuresVarFractal)


	def addIceAtPlot(self, pPlot, iX, iY, lat):
		"""
		Randomly add ice at plot. Discworld has less ice than normal maps.
		:param pPlot: Plot
		:param iX: x coordinate of the plot.
		:param iY: y coordinate of the plot.
		:param lat: Latitude of the plot.
		:return:
		"""
		if pPlot.canHaveFeature(self.featureIce):
			rand = self.mapRand.get(100, "[DiscWorld] - Add ice") / 100.0
			if rand < 7 * (lat - (1.0 - (self.gc.getClimateInfo(self.map.getClimate()).getRandIceLatitude() / 2.0))):
				pPlot.setFeatureType(self.featureIce, -1)


class MapAreaPolygon:
	"""
	Class that defines a map area that can have any polygonal shape. Randomized distortion using both fractals and
	coordinate changes is applied, to make sure that the final area shape is not too regular and unpredictable, while
	still following roughly the desired shape.
	Uses the PNPOLY algorithm. See: https://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
	"""

	__DISPLACEMENT_FRACTAL_GRAIN = 2
	"""
	Grain used for the displacement fractals.
	"""


	def __init__(self, sRegionName, lOriginalPolygonPoints, fAngle):
		"""
		Initializes the polygonal map area.
		:param lOriginalPolygonPoints: List of tuples that contain the x and y coordinates of each of the points.
		:param fAngle: The polygon will be rotated by this angle.
		"""
		if len(lOriginalPolygonPoints) < 3:
			raise Exception("[DiscWorld] - " + sRegionName + " - A polygon must have at least three vertices.")

		# Rotate the polygon and apply random displacement.
		lPolygonPoints = list()

		self.__iRandomDisplacement = int(max(2.0, map.getGridWidth() / 12.0))
		fMiddleX = map.getGridWidth() / 2.0
		fMiddleY = map.getGridHeight() / 2.0
		fSinAngle = math.sin(fAngle)
		fCosAngle = math.cos(fAngle)

		for pX, pY in lOriginalPolygonPoints:
			pXInitial = pX - fMiddleX
			pYInitial = pY - fMiddleY
			pXRotated = pXInitial * fCosAngle - pYInitial * fSinAngle + fMiddleX + self.__getRandomDisplacement()
			pYRotated = pXInitial * fSinAngle + pYInitial * fCosAngle + fMiddleY + self.__getRandomDisplacement()
			lPolygonPoints.append([pXRotated, pYRotated])

		# Calculate the rest of the values that depend on the shape of the polygon.
		self.__fMinX = sys.maxint
		self.__fMinY = sys.maxint
		self.__fMaxX = -sys.maxint - 1
		self.__fMaxY = -sys.maxint - 1

		for pX, pY in lPolygonPoints:
			self.__fMinX = min(self.__fMinX, pX)
			self.__fMinY = min(self.__fMinY, pY)
			self.__fMaxX = max(self.__fMaxX, pX)
			self.__fMaxY = max(self.__fMaxY, pY)

		# Give room for fractal displacement.
		self.__fMinX -= 4.0
		self.__fMinY -= 4.0
		self.__fMaxX += 4.0
		self.__fMaxY += 4.0

		# Used for creating displacement fractals and initial isInside checks.
		self.__iRegionWidth = int(self.__fMaxX - self.__fMinX + 1)
		self.__iRegionHeight = int(self.__fMaxY - self.__fMinY + 1)

		# Perfect polygons are boring. These fractals are used to distort the shape of the resulting landmass slightly.
		self.__horizontalDisplacementFrac = CyFractal()
		self.__horizontalDisplacementFrac.fracInit(
			self.__iRegionWidth, self.__iRegionHeight, self.__DISPLACEMENT_FRACTAL_GRAIN, game.getMapRand(),
			CyFractal.FracVals.FRAC_POLAR, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)

		self.__verticalDisplacementFrac = CyFractal()
		self.__verticalDisplacementFrac.fracInit(
			self.__iRegionWidth, self.__iRegionHeight, self.__DISPLACEMENT_FRACTAL_GRAIN, game.getMapRand(),
			CyFractal.FracVals.FRAC_POLAR, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
		)

		# Since all points need to be accessed at least once, they can be calculated on init.
		self.__bInsideMatrix = [[False for iY in range(self.__iRegionHeight)] for iX in range(self.__iRegionWidth)]

		# PNPOLY algorithm for determining if a given plot is inside of the polygon or not.
		for iX in range(self.__iRegionWidth):
			for iY in range(self.__iRegionHeight):
				# Apply displacement values between -4.0 and 4.0.
				fHorizontalDisp = self.__horizontalDisplacementFrac.getHeight(iX, iY) / 32.0 - 4.0
				fVerticalDisp = self.__verticalDisplacementFrac.getHeight(iX, iY) / 32.0 - 4.0

				fRealX = self.__fMinX + iX + fHorizontalDisp
				fRealY = self.__fMinY + iY + fVerticalDisp

				iPoint = 0
				jPoint = len(lPolygonPoints) - 1
				bInside = False

				while iPoint < len(lPolygonPoints):
					lFirstPoint = lPolygonPoints[iPoint]
					lSecondPoint = lPolygonPoints[jPoint]
					if (lFirstPoint[1] > fRealY) != (lSecondPoint[1] > fRealY):
						fValue = float(lSecondPoint[0] - lFirstPoint[0])
						fValue *= fRealY - lFirstPoint[1]
						fValue /= lSecondPoint[1] - lFirstPoint[1]
						fValue += lFirstPoint[0]
						if fRealX < fValue:
							bInside = not bInside

					# Prepare the next pair of points.
					jPoint = iPoint
					iPoint += 1

				if bInside:
					self.__bInsideMatrix[iX][iY] = True

		# Uncommenting this code displays all regions in the log.
		"""
		print "[DiscWorld] - " + sRegionName + " - MapAreaPolygon map area:"
		for iY in range(self.__iRegionHeight - 1, -1, -1):
			sLine = ""
			for iX in range(self.__iRegionWidth):
				if self.__bInsideMatrix[iX][iY]:
					sLine += "#"
				else:
					sLine += " "
			print sLine
		"""


	def __getRandomDisplacement(self):
		"""
		Allows to apply a random displacement to one of the coordinates of one of the points of the polygon.
		:return: Calculated displacement.
		"""
		return self.__iRandomDisplacement / 2 - game.getMapRand().get(
			self.__iRandomDisplacement,
			"[DiscWorld] - Randomization of the points of one of the areas.")


	@property
	def iRegionWidth(self):
		return self.__iRegionWidth


	@property
	def iRegionHeight(self):
		return self.__iRegionHeight


	@property
	def fMinX(self):
		return self.__fMinX


	@property
	def fMinY(self):
		return self.__fMinY


	def isInside(self, fX, fY):
		"""
		Checks if the point (fX, fY) is inside of the polygon.
		:param fX: x coordinate of the point.
		:param fY: y coordinate of the point.
		:return: True if the point is inside of the polygon, false otherwise.
		"""
		iRealX = int(fX - self.__fMinX)
		iRealY = int(fY - self.__fMinY)

		if iRealX < 0 or iRealX >= self.__iRegionWidth:
			return False
		if iRealY < 0 or iRealY >= self.__iRegionHeight:
			return False

		return self.__bInsideMatrix[iRealX][iRealY]


def getVariationFractal(iGrain):
	"""
	Initializes a fractal that can be used to introduce random variations.
	:return: New fractal.
	"""
	varFractal = CyFractal()
	iFlags = 0  # Disallow FRAC_POLAR flag, to prevent "zero row" problems.

	varFractal.fracInit(
		map.getGridWidth(), map.getGridHeight(), iGrain, game.getMapRand(), iFlags,
		# The Discworld has the same width and height.
		CyFractal.FracVals.DEFAULT_FRAC_Y_EXP, CyFractal.FracVals.DEFAULT_FRAC_Y_EXP
	)

	return varFractal


def getDistanceToCenterUnscaled(iX, iY, varFractal=None):
	"""
	Calculates an approximate distance from the point to the center of the disc.
	:param iX: x coordinate of the plot
	:param iY: y coordinate of the plot.
	:param varFractal: Fractal used to introduce random variations in the calculated distance.
	:return: Calculated distance.
	"""
	fHorizontal = ((map.getGridWidth() - 1) / 2.0 - iX) / ((map.getGridWidth() - 1) / 2.0)
	fVertical = ((map.getGridHeight() - 1) / 2.0 - iY) / ((map.getGridHeight() - 1) / 2.0)

	fDistance = math.sqrt(fHorizontal * fHorizontal + fVertical * fVertical)

	# Adjust value using the variation fractal, to mix things up:
	if varFractal is not None:
		fDistance += (128 - varFractal.getHeight(iX, iY)) / (255.0 * 5.0)

	return fDistance


def getInvertedDistanceToCenter(iX, iY, varFractal):
	"""
	Returns the approximate distance from the center of the disc to the plot. The distance is inverted, so 1.0 means
	that the plot is in the center of the Discworld, while 0.0 means that it is in the border.
	:param iX: x coordinate of the plot
	:param iY: y coordinate of the plot.
	:param varFractal: Fractal used to introduce random variations in the calculated distance.
	:return: Calculated distance, limited between 0.0 and 1.0.
	"""
	fDistance = getDistanceToCenterUnscaled(iX, iY, varFractal)

	# Limit to the range [0, 1]:
	if fDistance < 0:
		fDistance = 0.0
	elif fDistance > 1:
		fDistance = 1.0

	return 1.0 - fDistance


def isOutsideDisc(iX, iY):
	"""
	Checks if a specific plot is outside of the disc.
	:param iX: x coordinate of the plot
	:param iY: y coordinate of the plot.
	:return: True if the plot is outside of the disc, False otherwise.
	"""
	return getDistanceToCenterUnscaled(iX, iY) > 1.0