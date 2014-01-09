//
//	FILE:	 CvMap.cpp
//	AUTHOR:  Soren Johnson
//	PURPOSE: Game map class
//-----------------------------------------------------------------------------
//	Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//-----------------------------------------------------------------------------
//


#include "CvGameCoreDLL.h"
#include "CvMap.h"
#include "CvCity.h"
#include "CvPlotGroup.h"
#include "CvGlobals.h"
#include "CvGameAI.h"
#include "CvPlayerAI.h"
#include "CvRandom.h"
#include "CvGameCoreUtils.h"
#include "CvFractal.h"
#include "CvPlot.h"
#include "CvGameCoreUtils.h"
#include "CvMap.h"
#include "CvMapGenerator.h"
#include "FAStarNode.h"
#include "CvInitCore.h"
#include "CvInfos.h"
#include "FProfiler.h"
#include "CyArgsList.h"

#include "CvDLLEngineIFaceBase.h"
#include "CvDLLIniParserIFaceBase.h"
#include "CvDLLFAStarIFaceBase.h"
#include "CvDLLFAStarIFaceBase.h"
#include "CvDLLPythonIFaceBase.h"
/************************************************************************************************/
/* WILDERNESS                             08/2013                                 lfgr          */
/* Debug                                                                                        */
/************************************************************************************************/
#include "BetterBTSAI.h"
/************************************************************************************************/
/* WILDERNESS                              END                                                  */
/************************************************************************************************/


// Public Functions...

CvMap::CvMap()
{
	CvMapInitData defaultMapData;

	m_paiNumBonus = NULL;
	m_paiNumBonusOnLand = NULL;

	m_pMapPlots = NULL;

	reset(&defaultMapData);
}


CvMap::~CvMap()
{
	uninit();
}

// FUNCTION: init()
// Initializes the map.
// Parameters:
//	pInitInfo					- Optional init structure (used for WB load)
// Returns:
//	nothing.
void CvMap::init(CvMapInitData* pInitInfo/*=NULL*/)
{
	int iX, iY;

	PROFILE("CvMap::init");
	gDLL->logMemState( CvString::format("CvMap::init begin - world size=%s, climate=%s, sealevel=%s, num custom options=%6", 
		GC.getWorldInfo(GC.getInitCore().getWorldSize()).getDescription(), 
		GC.getClimateInfo(GC.getInitCore().getClimate()).getDescription(), 
		GC.getSeaLevelInfo(GC.getInitCore().getSeaLevel()).getDescription(),
		GC.getInitCore().getNumCustomMapOptions()).c_str() );

	gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "beforeInit");

	//--------------------------------
	// Init saved data
	reset(pInitInfo);

	//--------------------------------
	// Init containers
	m_areas.init();

	//--------------------------------
	// Init non-saved data
	setup();

	//--------------------------------
	// Init other game data
	gDLL->logMemState("CvMap before init plots");
	m_pMapPlots = new CvPlot[numPlotsINLINE()];
	for (iX = 0; iX < getGridWidthINLINE(); iX++)
	{
		gDLL->callUpdater();
		for (iY = 0; iY < getGridHeightINLINE(); iY++)
		{
			plotSorenINLINE(iX, iY)->init(iX, iY);
		}
	}
	calculateAreas();
	gDLL->logMemState("CvMap after init plots");
}


void CvMap::uninit()
{
	SAFE_DELETE_ARRAY(m_paiNumBonus);
	SAFE_DELETE_ARRAY(m_paiNumBonusOnLand);

	SAFE_DELETE_ARRAY(m_pMapPlots);

	m_areas.uninit();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvMap::reset(CvMapInitData* pInitInfo)
{
	int iI;

	//--------------------------------
	// Uninit class
	uninit();

	//
	// set grid size
	// initially set in terrain cell units
	//
	m_iGridWidth = (GC.getInitCore().getWorldSize() != NO_WORLDSIZE) ? GC.getWorldInfo(GC.getInitCore().getWorldSize()).getGridWidth (): 0;	//todotw:tcells wide
	m_iGridHeight = (GC.getInitCore().getWorldSize() != NO_WORLDSIZE) ? GC.getWorldInfo(GC.getInitCore().getWorldSize()).getGridHeight (): 0;

	// allow grid size override
	if (pInitInfo)
	{
		m_iGridWidth	= pInitInfo->m_iGridW;
		m_iGridHeight	= pInitInfo->m_iGridH;
	}
	else
	{
		// check map script for grid size override
		if (GC.getInitCore().getWorldSize() != NO_WORLDSIZE)
		{
			std::vector<int> out;
			CyArgsList argsList;
			argsList.add(GC.getInitCore().getWorldSize());
			bool ok = gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getGridSize", argsList.makeFunctionArgs(), &out);

			if (ok && !gDLL->getPythonIFace()->pythonUsingDefaultImpl() && out.size() == 2)
			{
				m_iGridWidth = out[0];
				m_iGridHeight = out[1];
				FAssertMsg(m_iGridWidth > 0 && m_iGridHeight > 0, "the width and height returned by python getGridSize() must be positive");
			}
		}

		// convert to plot dimensions
		if (GC.getNumLandscapeInfos() > 0)
		{
			m_iGridWidth *= GC.getLandscapeInfo(GC.getActiveLandscapeID()).getPlotsPerCellX();
			m_iGridHeight *= GC.getLandscapeInfo(GC.getActiveLandscapeID()).getPlotsPerCellY();
		}
	}

	m_iLandPlots = 0;
	m_iOwnedPlots = 0;

	if (pInitInfo)
	{
		m_iTopLatitude = pInitInfo->m_iTopLatitude;
		m_iBottomLatitude = pInitInfo->m_iBottomLatitude;
	}
	else
	{
		// Check map script for latitude override (map script beats ini file)

		long resultTop = -1, resultBottom = -1;
		bool okX = gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getTopLatitude", NULL, &resultTop);
		bool overrideX = !gDLL->getPythonIFace()->pythonUsingDefaultImpl();
		bool okY = gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getBottomLatitude", NULL, &resultBottom);
		bool overrideY = !gDLL->getPythonIFace()->pythonUsingDefaultImpl();

		if (okX && okY && overrideX && overrideY && resultTop != -1 && resultBottom != -1)
		{
			m_iTopLatitude = resultTop;
			m_iBottomLatitude = resultBottom;
		}
	}

	m_iTopLatitude = std::min(m_iTopLatitude, 90);
	m_iTopLatitude = std::max(m_iTopLatitude, -90);
	m_iBottomLatitude = std::min(m_iBottomLatitude, 90);
	m_iBottomLatitude = std::max(m_iBottomLatitude, -90);

	m_iNextRiverID = 0;

	//
	// set wrapping
	//
	m_bWrapX = true;
	m_bWrapY = false;
	if (pInitInfo)
	{
		m_bWrapX = pInitInfo->m_bWrapX;
		m_bWrapY = pInitInfo->m_bWrapY;
	}
	else
	{
		// Check map script for wrap override (map script beats ini file)

		long resultX = -1, resultY = -1;
		bool okX = gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getWrapX", NULL, &resultX);
		bool overrideX = !gDLL->getPythonIFace()->pythonUsingDefaultImpl();
		bool okY = gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "getWrapY", NULL, &resultY);
		bool overrideY = !gDLL->getPythonIFace()->pythonUsingDefaultImpl();

		if (okX && okY && overrideX && overrideY && resultX != -1 && resultY != -1)
		{
			m_bWrapX = (resultX != 0);
			m_bWrapY = (resultY != 0);
		}
	}

	if (GC.getNumBonusInfos())
	{
		FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvMap::reset");
		FAssertMsg(m_paiNumBonus==NULL, "mem leak m_paiNumBonus");
		m_paiNumBonus = new int[GC.getNumBonusInfos()];
		FAssertMsg(m_paiNumBonusOnLand==NULL, "mem leak m_paiNumBonusOnLand");
		m_paiNumBonusOnLand = new int[GC.getNumBonusInfos()];
		for (iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiNumBonus[iI] = 0;
			m_paiNumBonusOnLand[iI] = 0;
		}
	}

	m_areas.removeAll();
}


// FUNCTION: setup()
// Initializes all data that is not serialized but needs to be initialized after loading.
void CvMap::setup()
{
	PROFILE("CvMap::setup");

	gDLL->getFAStarIFace()->Initialize(&GC.getPathFinder(), getGridWidthINLINE(), getGridHeightINLINE(), isWrapXINLINE(), isWrapYINLINE(), pathDestValid, pathHeuristic, pathCost, pathValid, pathAdd, NULL, NULL);
	gDLL->getFAStarIFace()->Initialize(&GC.getInterfacePathFinder(), getGridWidthINLINE(), getGridHeightINLINE(), isWrapXINLINE(), isWrapYINLINE(), pathDestValid, pathHeuristic, pathCost, pathValid, pathAdd, NULL, NULL);
	gDLL->getFAStarIFace()->Initialize(&GC.getStepFinder(), getGridWidthINLINE(), getGridHeightINLINE(), isWrapXINLINE(), isWrapYINLINE(), stepDestValid, stepHeuristic, stepCost, stepValid, stepAdd, NULL, NULL);
	gDLL->getFAStarIFace()->Initialize(&GC.getRouteFinder(), getGridWidthINLINE(), getGridHeightINLINE(), isWrapXINLINE(), isWrapYINLINE(), NULL, NULL, NULL, routeValid, NULL, NULL, NULL);
	gDLL->getFAStarIFace()->Initialize(&GC.getBorderFinder(), getGridWidthINLINE(), getGridHeightINLINE(), isWrapXINLINE(), isWrapYINLINE(), NULL, NULL, NULL, borderValid, NULL, NULL, NULL);
	gDLL->getFAStarIFace()->Initialize(&GC.getAreaFinder(), getGridWidthINLINE(), getGridHeightINLINE(), isWrapXINLINE(), isWrapYINLINE(), NULL, NULL, NULL, areaValid, NULL, joinArea, NULL);
	gDLL->getFAStarIFace()->Initialize(&GC.getPlotGroupFinder(), getGridWidthINLINE(), getGridHeightINLINE(), isWrapXINLINE(), isWrapYINLINE(), NULL, NULL, NULL, plotGroupValid, NULL, countPlotGroup, NULL);
}


//////////////////////////////////////
// graphical only setup
//////////////////////////////////////
void CvMap::setupGraphical()
{
	if (!GC.IsGraphicsInitialized())
		return;

	if (m_pMapPlots != NULL)
	{
		int iI;
		for (iI = 0; iI < numPlotsINLINE(); iI++)
		{
			gDLL->callUpdater();	// allow windows msgs to update
			plotByIndexINLINE(iI)->setupGraphical();
		}
	}
}


void CvMap::erasePlots()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->erase();
	}
}


void CvMap::setRevealedPlots(TeamTypes eTeam, bool bNewValue, bool bTerrainOnly)
{
	PROFILE_FUNC();

	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->setRevealed(eTeam, bNewValue, bTerrainOnly, NO_TEAM, false);
	}

	GC.getGameINLINE().updatePlotGroups();
}


void CvMap::setAllPlotTypes(PlotTypes ePlotType)
{
	//float startTime = (float) timeGetTime();

	for(int i=0;i<numPlotsINLINE();i++)
	{
		plotByIndexINLINE(i)->setPlotType(ePlotType, false, false);
	}

	recalculateAreas();

	//rebuild landscape
	gDLL->getEngineIFace()->RebuildAllPlots();

	//mark minimap as dirty
	gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true);
	gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
	
	//float endTime = (float) timeGetTime();
	//OutputDebugString(CvString::format("[Jason] setAllPlotTypes: %f\n", endTime - startTime).c_str());
}


// XXX generalize these funcs? (macro?)
void CvMap::doTurn()
{
	PROFILE("CvMap::doTurn()")

	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->doTurn();
	}
}


void CvMap::updateFlagSymbols()
{
	PROFILE_FUNC();

	CvPlot* pLoopPlot;
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		pLoopPlot = plotByIndexINLINE(iI);

		if (pLoopPlot->isFlagDirty())
		{
			pLoopPlot->updateFlagSymbol();
			pLoopPlot->setFlagDirty(false);
		}
	}
}


void CvMap::updateFog()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateFog();
	}
}


void CvMap::updateVisibility()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateVisibility();
	}
}


void CvMap::updateSymbolVisibility()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateSymbolVisibility();
	}
}


void CvMap::updateSymbols()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateSymbols();
	}
}


void CvMap::updateMinimapColor()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateMinimapColor();
	}
}


void CvMap::updateSight(bool bIncrement)
{
	for (int iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateSight(bIncrement, false);
	}

	GC.getGameINLINE().updatePlotGroups();
}


void CvMap::updateIrrigated()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateIrrigated();
	}
}


void CvMap::updateCenterUnit()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateCenterUnit();
	}
}


void CvMap::updateWorkingCity()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateWorkingCity();
	}
}


void CvMap::updateMinOriginalStartDist(CvArea* pArea)
{
	PROFILE_FUNC();

	CvPlot* pStartingPlot;
	CvPlot* pLoopPlot;
	int iDist;
	int iI, iJ;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		pLoopPlot = plotByIndexINLINE(iI);

		if (pLoopPlot->area() == pArea)
		{
			pLoopPlot->setMinOriginalStartDist(-1);
		}
	}

	for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		pStartingPlot = GET_PLAYER((PlayerTypes)iI).getStartingPlot();

		if (pStartingPlot != NULL)
		{
			if (pStartingPlot->area() == pArea)
			{
				for (iJ = 0; iJ < numPlotsINLINE(); iJ++)
				{
					pLoopPlot = plotByIndexINLINE(iJ);

					if (pLoopPlot->area() == pArea)
					{
						
						//iDist = GC.getMapINLINE().calculatePathDistance(pStartingPlot, pLoopPlot);
						iDist = stepDistance(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());

						if (iDist != -1)
						{
						    //int iCrowDistance = plotDistance(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());
						    //iDist = std::min(iDist,  iCrowDistance * 2);
							if ((pLoopPlot->getMinOriginalStartDist() == -1) || (iDist < pLoopPlot->getMinOriginalStartDist()))
							{
								pLoopPlot->setMinOriginalStartDist(iDist);
							}
						}
					}
				}
			}
		}
	}
}


void CvMap::updateYield()
{
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->updateYield();
	}
}


void CvMap::verifyUnitValidPlot()
{
	for (int iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->verifyUnitValidPlot();
	}
}


void CvMap::combinePlotGroups(PlayerTypes ePlayer, CvPlotGroup* pPlotGroup1, CvPlotGroup* pPlotGroup2)
{
	CLLNode<XYCoords>* pPlotNode;
	CvPlotGroup* pNewPlotGroup;
	CvPlotGroup* pOldPlotGroup;
	CvPlot* pPlot;

	FAssertMsg(pPlotGroup1 != NULL, "pPlotGroup is not assigned to a valid value");
	FAssertMsg(pPlotGroup2 != NULL, "pPlotGroup is not assigned to a valid value");

	if (pPlotGroup1 == pPlotGroup2)
	{
		return;
	}

	if (pPlotGroup1->getLengthPlots() > pPlotGroup2->getLengthPlots())
	{
		pNewPlotGroup = pPlotGroup1;
		pOldPlotGroup = pPlotGroup2;
	}
	else
	{
		pNewPlotGroup = pPlotGroup2;
		pOldPlotGroup = pPlotGroup1;
	}

	pPlotNode = pOldPlotGroup->headPlotsNode();
	while (pPlotNode != NULL)
	{
		pPlot = plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY);
		pNewPlotGroup->addPlot(pPlot);
		pPlotNode = pOldPlotGroup->deletePlotsNode(pPlotNode);
	}
}

CvPlot* CvMap::syncRandPlot(int iFlags, int iArea, int iMinUnitDistance, int iTimeout)
{
	CvPlot* pPlot;
	CvPlot* pTestPlot;
	CvPlot* pLoopPlot;
	bool bValid;
	int iCount;
	int iDX, iDY;

	pPlot = NULL;

	iCount = 0;

	while (iCount < iTimeout)
	{
		pTestPlot = plotSorenINLINE(GC.getGameINLINE().getSorenRandNum(getGridWidthINLINE(), "Rand Plot Width"), GC.getGameINLINE().getSorenRandNum(getGridHeightINLINE(), "Rand Plot Height"));

		FAssertMsg(pTestPlot != NULL, "TestPlot is not assigned a valid value");

		if ((iArea == -1) || (pTestPlot->getArea() == iArea))
		{
			bValid = true;

			if (bValid)
			{
				if (iMinUnitDistance != -1)
				{
					for (iDX = -(iMinUnitDistance); iDX <= iMinUnitDistance; iDX++)
					{
						for (iDY = -(iMinUnitDistance); iDY <= iMinUnitDistance; iDY++)
						{
							pLoopPlot	= plotXY(pTestPlot->getX_INLINE(), pTestPlot->getY_INLINE(), iDX, iDY);

							if (pLoopPlot != NULL)
							{
								if (pLoopPlot->isUnit())
								{
									bValid = false;
								}
							}
						}
					}
				}
			}

			if (bValid)
			{
				if (iFlags & RANDPLOT_LAND)
				{
					if (pTestPlot->isWater())
					{
						bValid = false;
					}
				}
			}

			if (bValid)
			{
				if (iFlags & RANDPLOT_UNOWNED)
				{
					if (pTestPlot->isOwned())
					{
						bValid = false;
					}
				}
			}

			if (bValid)
			{
				if (iFlags & RANDPLOT_ADJACENT_UNOWNED)
				{
					if (pTestPlot->isAdjacentOwned())
					{
						bValid = false;
					}
				}
			}

			if (bValid)
			{
				if (iFlags & RANDPLOT_ADJACENT_LAND)
				{
					if (!(pTestPlot->isAdjacentToLand()))
					{
						bValid = false;
					}
				}
			}

			if (bValid)
			{
				if (iFlags & RANDPLOT_PASSIBLE)
				{
					if (pTestPlot->isImpassable())
					{
						bValid = false;
					}
				}
			}

			if (bValid)
			{
				if (iFlags & RANDPLOT_NOT_VISIBLE_TO_CIV)
				{
					if (pTestPlot->isVisibleToCivTeam())
					{
						bValid = false;
					}
				}
			}

			if (bValid)
			{
				if (iFlags & RANDPLOT_NOT_CITY)
				{
					if (pTestPlot->isCity())
					{
						bValid = false;
					}
				}
			}

			if (bValid)
			{
				pPlot = pTestPlot;
				break;
			}
		}

		iCount++;
	}

	return pPlot;
}


CvCity* CvMap::findCity(int iX, int iY, PlayerTypes eOwner, TeamTypes eTeam, bool bSameArea, bool bCoastalOnly, TeamTypes eTeamAtWarWith, DirectionTypes eDirection, CvCity* pSkipCity)
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	CvCity* pBestCity;
	int iValue;
	int iBestValue;
	int iLoop;
	int iI;

	// XXX look for barbarian cities???

	iBestValue = MAX_INT;
	pBestCity = NULL;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if ((eOwner == NO_PLAYER) || (iI == eOwner))
			{
				if ((eTeam == NO_TEAM) || (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam))
				{
					for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
					{
						if (!bSameArea || (pLoopCity->area() == plotINLINE(iX, iY)->area()) || (bCoastalOnly && (pLoopCity->waterArea() == plotINLINE(iX, iY)->area())))
						{
							if (!bCoastalOnly || pLoopCity->isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
							{
								if ((eTeamAtWarWith == NO_TEAM) || atWar(GET_PLAYER((PlayerTypes)iI).getTeam(), eTeamAtWarWith))
								{
									if ((eDirection == NO_DIRECTION) || (estimateDirection(dxWrap(pLoopCity->getX_INLINE() - iX), dyWrap(pLoopCity->getY_INLINE() - iY)) == eDirection))
									{
										if ((pSkipCity == NULL) || (pLoopCity != pSkipCity))
										{
											iValue = plotDistance(iX, iY, pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE());

											if (iValue < iBestValue)
											{
												iBestValue = iValue;
												pBestCity = pLoopCity;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return pBestCity;
}


CvSelectionGroup* CvMap::findSelectionGroup(int iX, int iY, PlayerTypes eOwner, bool bReadyToSelect, bool bWorkers)
{
	CvSelectionGroup* pLoopSelectionGroup;
	CvSelectionGroup* pBestSelectionGroup;
	int iValue;
	int iBestValue;
	int iLoop;
	int iI;

	// XXX look for barbarian cities???

	iBestValue = MAX_INT;
	pBestSelectionGroup = NULL;

	for (iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if ((eOwner == NO_PLAYER) || (iI == eOwner))
			{
				for(pLoopSelectionGroup = GET_PLAYER((PlayerTypes)iI).firstSelectionGroup(&iLoop); pLoopSelectionGroup != NULL; pLoopSelectionGroup = GET_PLAYER((PlayerTypes)iI).nextSelectionGroup(&iLoop))
				{
					if (!bReadyToSelect || pLoopSelectionGroup->readyToSelect())
					{
						if (!bWorkers || pLoopSelectionGroup->hasWorker())
						{
							iValue = plotDistance(iX, iY, pLoopSelectionGroup->getX(), pLoopSelectionGroup->getY());

							if (iValue < iBestValue)
							{
								iBestValue = iValue;
								pBestSelectionGroup = pLoopSelectionGroup;
							}
						}
					}
				}
			}
		}
	}

	return pBestSelectionGroup;
}


CvArea* CvMap::findBiggestArea(bool bWater)
{
	CvArea* pLoopArea;
	CvArea* pBestArea;
	int iValue;
	int iBestValue;
	int iLoop;

	iBestValue = 0;
	pBestArea = NULL;

	for(pLoopArea = firstArea(&iLoop); pLoopArea != NULL; pLoopArea = nextArea(&iLoop))
	{
		if (pLoopArea->isWater() == bWater)
		{
			iValue = pLoopArea->getNumTiles();

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestArea = pLoopArea;
			}
		}
	}

	return pBestArea;
}


int CvMap::getMapFractalFlags()
{
	int wrapX = 0;
	if (isWrapXINLINE())
	{
		wrapX = (int)CvFractal::FRAC_WRAP_X;
	}

	int wrapY = 0;
	if (isWrapYINLINE())
	{
		wrapY = (int)CvFractal::FRAC_WRAP_Y;
	}

	return (wrapX | wrapY);
}


//"Check plots for wetlands or seaWater.  Returns true if found"
bool CvMap::findWater(CvPlot* pPlot, int iRange, bool bFreshWater)
{
	PROFILE("CvMap::findWater()");

	CvPlot* pLoopPlot;
	int iDX, iDY;

	for (iDX = -(iRange); iDX <= iRange; iDX++)
	{
		for (iDY = -(iRange); iDY <= iRange; iDY++)
		{
			pLoopPlot	= plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY);

			if (pLoopPlot != NULL)
			{
				if (bFreshWater)
				{
					if (pLoopPlot->isFreshWater())
					{
						return true;
					}
				}
				else
				{
					if (pLoopPlot->isWater())
					{
						return true;
					}
				}
			}
		}
	}

	return false;
}


bool CvMap::isPlot(int iX, int iY) const
{
	return isPlotINLINE(iX, iY);
}


int CvMap::numPlots() const																											 
{
	return numPlotsINLINE();
}


int CvMap::plotNum(int iX, int iY) const
{
	return plotNumINLINE(iX, iY);
}


int CvMap::plotX(int iIndex) const
{
	return (iIndex % getGridWidthINLINE());
}


int CvMap::plotY(int iIndex) const
{
	return (iIndex / getGridWidthINLINE());
}


int CvMap::pointXToPlotX(float fX)
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return (int)(((fX + (fWidth/2.0f)) / fWidth) * getGridWidthINLINE());
}


float CvMap::plotXToPointX(int iX)
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return ((iX * fWidth) / ((float)getGridWidthINLINE())) - (fWidth / 2.0f) + (GC.getPLOT_SIZE() / 2.0f);
}


int CvMap::pointYToPlotY(float fY)
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return (int)(((fY + (fHeight/2.0f)) / fHeight) * getGridHeightINLINE());
}


float CvMap::plotYToPointY(int iY)
{
	float fWidth, fHeight;
	gDLL->getEngineIFace()->GetLandscapeGameDimensions(fWidth, fHeight);
	return ((iY * fHeight) / ((float)getGridHeightINLINE())) - (fHeight / 2.0f) + (GC.getPLOT_SIZE() / 2.0f);
}


float CvMap::getWidthCoords()																	
{
	return (GC.getPLOT_SIZE() * ((float)getGridWidthINLINE()));
}


float CvMap::getHeightCoords()																	
{
	return (GC.getPLOT_SIZE() * ((float)getGridHeightINLINE()));
}


int CvMap::maxPlotDistance()
{
	return std::max(1, plotDistance(0, 0, ((isWrapXINLINE()) ? (getGridWidthINLINE() / 2) : (getGridWidthINLINE() - 1)), ((isWrapYINLINE()) ? (getGridHeightINLINE() / 2) : (getGridHeightINLINE() - 1))));
}


int CvMap::maxStepDistance()
{
	return std::max(1, stepDistance(0, 0, ((isWrapXINLINE()) ? (getGridWidthINLINE() / 2) : (getGridWidthINLINE() - 1)), ((isWrapYINLINE()) ? (getGridHeightINLINE() / 2) : (getGridHeightINLINE() - 1))));
}


int CvMap::getGridWidth() const
{
	return getGridWidthINLINE();
}


int CvMap::getGridHeight() const
{
	return getGridHeightINLINE();
}


int CvMap::getLandPlots()
{
	return m_iLandPlots;
}


void CvMap::changeLandPlots(int iChange)
{
	m_iLandPlots = (m_iLandPlots + iChange);
	FAssert(getLandPlots() >= 0);
}


int CvMap::getOwnedPlots()
{
	return m_iOwnedPlots;
}


void CvMap::changeOwnedPlots(int iChange)
{
	m_iOwnedPlots = (m_iOwnedPlots + iChange);
	FAssert(getOwnedPlots() >= 0);
}


int CvMap::getTopLatitude()
{
	return m_iTopLatitude;
}


int CvMap::getBottomLatitude()
{
	return m_iBottomLatitude;
}


int CvMap::getNextRiverID()
{
	return m_iNextRiverID;
}


void CvMap::incrementNextRiverID()
{
	m_iNextRiverID++;
}


bool CvMap::isWrapX()
{
	return isWrapXINLINE();
}


bool CvMap::isWrapY()
{
	return isWrapYINLINE();
}

bool CvMap::isWrap()
{
	return isWrapINLINE();
}

WorldSizeTypes CvMap::getWorldSize()
{
	return GC.getInitCore().getWorldSize();
}


ClimateTypes CvMap::getClimate()
{
	return GC.getInitCore().getClimate();
}


SeaLevelTypes CvMap::getSeaLevel()
{
	return GC.getInitCore().getSeaLevel();
}



int CvMap::getNumCustomMapOptions()
{
	return GC.getInitCore().getNumCustomMapOptions();
}


CustomMapOptionTypes CvMap::getCustomMapOption(int iOption)
{
	return GC.getInitCore().getCustomMapOption(iOption);
}


int CvMap::getNumBonuses(BonusTypes eIndex)													
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiNumBonus[eIndex];
}


void CvMap::changeNumBonuses(BonusTypes eIndex, int iChange)									
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiNumBonus[eIndex] = (m_paiNumBonus[eIndex] + iChange);
	FAssert(getNumBonuses(eIndex) >= 0);
}


int CvMap::getNumBonusesOnLand(BonusTypes eIndex)													
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiNumBonusOnLand[eIndex];
}


void CvMap::changeNumBonusesOnLand(BonusTypes eIndex, int iChange)									
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiNumBonusOnLand[eIndex] = (m_paiNumBonusOnLand[eIndex] + iChange);
	FAssert(getNumBonusesOnLand(eIndex) >= 0);
}


CvPlot* CvMap::plotByIndex(int iIndex) const
{
	return plotByIndexINLINE(iIndex);
}


CvPlot* CvMap::plot(int iX, int iY) const
{
	return plotINLINE(iX, iY);
}


CvPlot* CvMap::pointToPlot(float fX, float fY)													
{
	return plotINLINE(pointXToPlotX(fX), pointYToPlotY(fY));
}


int CvMap::getIndexAfterLastArea()																
{
	return m_areas.getIndexAfterLast();
}


int CvMap::getNumAreas()																		
{
	return m_areas.getCount();
}


int CvMap::getNumLandAreas()
{
	CvArea* pLoopArea;
	int iNumLandAreas;
	int iLoop;

	iNumLandAreas = 0;

	for(pLoopArea = GC.getMap().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMap().nextArea(&iLoop))
	{
		if (!(pLoopArea->isWater()))
		{
			iNumLandAreas++;
		}
	}

	return iNumLandAreas;
}


CvArea* CvMap::getArea(int iID)																
{
	return m_areas.getAt(iID);
}


CvArea* CvMap::addArea()
{
	return m_areas.add();
}


void CvMap::deleteArea(int iID)
{
	m_areas.removeAt(iID);
}


CvArea* CvMap::firstArea(int *pIterIdx, bool bRev)
{
	return !bRev ? m_areas.beginIter(pIterIdx) : m_areas.endIter(pIterIdx);
}


CvArea* CvMap::nextArea(int *pIterIdx, bool bRev)
{
	return !bRev ? m_areas.nextIter(pIterIdx) : m_areas.prevIter(pIterIdx);
}


void CvMap::recalculateAreas()
{
	PROFILE("CvMap::recalculateAreas");

	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->setArea(FFreeList::INVALID_INDEX);
	}

	m_areas.removeAll();

	calculateAreas();
}


void CvMap::resetPathDistance()
{
	gDLL->getFAStarIFace()->ForceReset(&GC.getStepFinder());
}

// Super Forts begin *canal* *choke*
int CvMap::calculatePathDistance(CvPlot *pSource, CvPlot *pDest, CvPlot *pInvalidPlot)
// Super Forts end
{
	FAStarNode* pNode;

	if (pSource == NULL || pDest == NULL)
	{
		return -1;
	}

	// Super Forts begin *canal* *choke*
	// 1 must be added because 0 is already being used as the default value for iInfo in GeneratePath()
	int iInvalidPlot = (pInvalidPlot == NULL) ? 0 : GC.getMapINLINE().plotNum(pInvalidPlot->getX_INLINE(), pInvalidPlot->getY_INLINE()) + 1;

	if (gDLL->getFAStarIFace()->GeneratePath(&GC.getStepFinder(), pSource->getX_INLINE(), pSource->getY_INLINE(), pDest->getX_INLINE(), pDest->getY_INLINE(), false, iInvalidPlot, true))
	// Super Forts end
	{
		pNode = gDLL->getFAStarIFace()->GetLastNode(&GC.getStepFinder());

		if (pNode != NULL)
		{
			return pNode->m_iData1;
		}
	}

	return -1; // no passable path exists
}

// Super Forts begin *canal* *choke*
void CvMap::calculateCanalAndChokePoints()
{
	int iI;
	for(iI = 0; iI < numPlotsINLINE(); iI++)
	{
		plotByIndexINLINE(iI)->calculateCanalValue();
		plotByIndexINLINE(iI)->calculateChokeValue();
		// TEMPORARY HARD CODE for testing purposes
		/*if((plotByIndexINLINE(iI)->getChokeValue() > 0) || (plotByIndexINLINE(iI)->getCanalValue() > 0))
		{
			ImprovementTypes eImprovement = (ImprovementTypes) (plotByIndexINLINE(iI)->isWater() ? GC.getInfoTypeForString("IMPROVEMENT_WHALING_BOATS") : GC.getInfoTypeForString("IMPROVEMENT_FORT"));
			plotByIndexINLINE(iI)->setImprovementType(eImprovement);
		}
		else
		{
			plotByIndexINLINE(iI)->setImprovementType(NO_IMPROVEMENT);
		}*/
	}
}
// Super Forts end

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
// Plot danger cache
void CvMap::invalidateIsActivePlayerNoDangerCache()
{
	PROFILE_FUNC();

	int iI;
	CvPlot* pLoopPlot;

	for( iI = 0; iI < numPlotsINLINE(); iI++ )
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if( pLoopPlot != NULL )
		{
			pLoopPlot->setIsActivePlayerNoDangerCache(false);
		}
	}
}


void CvMap::invalidateIsTeamBorderCache(TeamTypes eTeam)
{
	PROFILE_FUNC();

	int iI;
	CvPlot* pLoopPlot;

	for( iI = 0; iI < numPlotsINLINE(); iI++ )
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if( pLoopPlot != NULL )
		{
			pLoopPlot->setIsTeamBorderCache(eTeam, false);
		}
	}
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/


//
// read object from a stream
// used during load
//
void CvMap::read(FDataStreamBase* pStream)
{
	CvMapInitData defaultMapData;

	// Init data before load
	reset(&defaultMapData);

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iGridWidth);
	pStream->Read(&m_iGridHeight);
	pStream->Read(&m_iLandPlots);
	pStream->Read(&m_iOwnedPlots);
	pStream->Read(&m_iTopLatitude);
	pStream->Read(&m_iBottomLatitude);
	pStream->Read(&m_iNextRiverID);

	pStream->Read(&m_bWrapX);
	pStream->Read(&m_bWrapY);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated");
	pStream->Read(GC.getNumBonusInfos(), m_paiNumBonus);
	pStream->Read(GC.getNumBonusInfos(), m_paiNumBonusOnLand);

	if (numPlotsINLINE() > 0)
	{
		m_pMapPlots = new CvPlot[numPlotsINLINE()];
		int iI;
		for (iI = 0; iI < numPlotsINLINE(); iI++)
		{
			m_pMapPlots[iI].read(pStream);
		}
	}

	// call the read of the free list CvArea class allocations
	ReadStreamableFFreeListTrashArray(m_areas, pStream);

	setup();
}

// save object to a stream
// used during save
//
void CvMap::write(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iGridWidth);
	pStream->Write(m_iGridHeight);
	pStream->Write(m_iLandPlots);
	pStream->Write(m_iOwnedPlots);
	pStream->Write(m_iTopLatitude);
	pStream->Write(m_iBottomLatitude);
	pStream->Write(m_iNextRiverID);

	pStream->Write(m_bWrapX);
	pStream->Write(m_bWrapY);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated");
	pStream->Write(GC.getNumBonusInfos(), m_paiNumBonus);
	pStream->Write(GC.getNumBonusInfos(), m_paiNumBonusOnLand);

	int iI;	
	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		m_pMapPlots[iI].write(pStream);
	}

	// call the read of the free list CvArea class allocations
	WriteStreamableFFreeListTrashArray(m_areas, pStream);
}


//
// used for loading WB maps
//
void CvMap::rebuild(int iGridW, int iGridH, int iTopLatitude, int iBottomLatitude, bool bWrapX, bool bWrapY, WorldSizeTypes eWorldSize, ClimateTypes eClimate, SeaLevelTypes eSeaLevel, int iNumCustomMapOptions, CustomMapOptionTypes * aeCustomMapOptions)
{
	CvMapInitData initData(iGridW, iGridH, iTopLatitude, iBottomLatitude, bWrapX, bWrapY);

	// Set init core data
	GC.getInitCore().setWorldSize(eWorldSize);
	GC.getInitCore().setClimate(eClimate);
	GC.getInitCore().setSeaLevel(eSeaLevel);
	GC.getInitCore().setCustomMapOptions(iNumCustomMapOptions, aeCustomMapOptions);

	// Init map
	init(&initData);
}


//////////////////////////////////////////////////////////////////////////
// Protected Functions...
//////////////////////////////////////////////////////////////////////////

void CvMap::calculateAreas()
{
	PROFILE("CvMap::calculateAreas");
	CvPlot* pLoopPlot;
	CvArea* pArea;
	int iArea;
	int iI;

	for (iI = 0; iI < numPlotsINLINE(); iI++)
	{
		pLoopPlot = plotByIndexINLINE(iI);
		gDLL->callUpdater();
		FAssertMsg(pLoopPlot != NULL, "LoopPlot is not assigned a valid value");

		if (pLoopPlot->getArea() == FFreeList::INVALID_INDEX)
		{
			pArea = addArea();
			pArea->init(pArea->getID(), pLoopPlot->isWater());

			iArea = pArea->getID();

			pLoopPlot->setArea(iArea);

			gDLL->getFAStarIFace()->GeneratePath(&GC.getAreaFinder(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), -1, -1, pLoopPlot->isWater(), iArea);
		}
	}
}

/************************************************************************************************/
/* WILDERNESS                             08/2013                                 lfgr          */
/* PlotWilderness                                                                               */
/* Original by Sephi                                                                            */
/************************************************************************************************/
void CvMap::calculateWilderness()
{
	logBBAI( "calculateWilderness()" );
	// Reset starting points of each player with capital cities
	for( int ePlayer = 0; ePlayer < GC.getMAX_CIV_PLAYERS(); ePlayer++ )
	{
		if( GET_PLAYER( (PlayerTypes) ePlayer ).isAlive() )
		{
			if( GET_PLAYER( (PlayerTypes) ePlayer ).getCapitalCity() != NULL )
			{
				logBBAI( "  Resetting player %d's starting plot to capital", ePlayer );
				GET_PLAYER( (PlayerTypes) ePlayer ).setStartingPlot( GET_PLAYER( (PlayerTypes) ePlayer ).getCapitalCity()->plot(), true );
			}
		}
	}

	// Reset
	for ( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
		plotByIndexINLINE( iPlot )->setWilderness(-1);
	
	logBBAI( "  Area summary" );
#ifdef LOG_AI
	for( int iArea = 0; iArea < getNumAreas(); iArea++ )
		logBBAI( "    Area #%d: %d plots%s%s", iArea, getArea( iArea )->getNumTiles(), getArea( iArea )->isWater() ? ", water" : "",
				getArea( iArea )->getNumStartingPlots() > 0 ? ", inhabited" : "" );
#endif
	
	logBBAI( "  Plot wilderness reset" );

	// LFGR_TODO: The method of using an area array will probably cause trouble if an area was deleted before.
	
	// Continents
	// Find geometric mean for uninhabited continents
	int* piUAreaMeanX = new int[getNumAreas()];
	int* piUAreaMeanY = new int[getNumAreas()];

	// Count number of uninhabited continent tiles
	int iNumUAreaTiles = 0;
	
	for( int iArea = 0; iArea < getNumAreas(); iArea++ )
	{
		if( getArea( iArea )->getNumStartingPlots() == 0 && !getArea( iArea )->isWater() )
		{
			piUAreaMeanX[iArea] = 0;
			piUAreaMeanY[iArea] = 0;
			iNumUAreaTiles += getArea( iArea )->getNumTiles();
		}
		else
		{
			piUAreaMeanX[iArea] = -1;
			piUAreaMeanY[iArea] = -1;
		}
	}

	for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
	{
		CvPlot* pLoopPlot = plotByIndexINLINE( iPlot );
		int iLoopArea = pLoopPlot->getArea() & FLTA_INDEX_MASK; // No idea why plots not simply store 0, 1, 2...
		FAssertMsg( iLoopArea < getNumAreas(), "iLoopArea >= getNumAreas()" );
		if( getArea( iLoopArea )->getNumStartingPlots() == 0 && !getArea( iLoopArea )->isWater() )
		{
			piUAreaMeanX[iLoopArea] += pLoopPlot->getX_INLINE();
			piUAreaMeanY[iLoopArea] += pLoopPlot->getY_INLINE();
		}
	}
	
	logBBAI( "  Uninhabited contintent centers:" );
	for( int iArea = 0; iArea < getNumAreas(); iArea++ )
	{
		if( getArea( iArea )->getNumStartingPlots() == 0 && !getArea( iArea )->isWater() )
		{
			piUAreaMeanX[iArea] /= getArea( iArea )->getNumTiles();
			piUAreaMeanY[iArea] /= getArea( iArea )->getNumTiles();

			logBBAI( "    Area #%d: %d|%d", iArea, piUAreaMeanX[iArea], piUAreaMeanY[iArea] );
		}
	}

	// Store max and min wilderness for all continents
	int* piAreaMaxWilderness = new int[getNumAreas()];
	int* piAreaMinWilderness = new int[getNumAreas()];
	int iWaterAreaMaxWilderness = -1;
	// Store max and min average starting plot distance for all uninhabited continents
	int* piUAreaMinAvDist = new int[getNumAreas()];
	int* piUAreaMaxAvDist = new int[getNumAreas()];
	int iUAreaMaxMaxAvDist = -1;
	// Store max continent size divided by number of players on that continent
	int iMaxInhabitedContinentSizePerPlayer = -1;
	
	for( int iArea = 0; iArea < getNumAreas(); iArea++ )
	{
		piAreaMaxWilderness[iArea] = -1;
		piAreaMinWilderness[iArea] = -1;
		piUAreaMinAvDist[iArea] = -1;
		piUAreaMaxAvDist[iArea] = -1;

		if( !getArea( iArea )->isWater() )
			if( getArea( iArea )->getNumStartingPlots() > 0 )
				if( iMaxInhabitedContinentSizePerPlayer == -1 || getArea( iArea )->getNumTiles() / getArea( iArea )->getNumStartingPlots() > iMaxInhabitedContinentSizePerPlayer )
					iMaxInhabitedContinentSizePerPlayer = getArea( iArea )->getNumTiles() / getArea( iArea )->getNumStartingPlots();
		
		logBBAI( "    Area #%d after init real min and max: %d, %d", iArea, piAreaMinWilderness[iArea], piAreaMaxWilderness[iArea] );
		logBBAI( "    Area #%d after init UArea min and max dist: %d, %d", iArea, piUAreaMinAvDist[iArea], piUAreaMaxAvDist[iArea] );
	}
	
	logBBAI( "  Max inhabited continent size per player: %d", iMaxInhabitedContinentSizePerPlayer );
	logBBAI( "  Looping plots..." );

	// First iteration for wilderness
	for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
	{
		CvPlot* pLoopPlot = plotByIndexINLINE( iPlot );
		int iLoopX = pLoopPlot->getX_INLINE();
		int iLoopY = pLoopPlot->getY_INLINE();
		int iLoopArea = pLoopPlot->getArea() & FLTA_INDEX_MASK; // No idea why plots not simply store 0, 1, 2...
		bool bWaterArea = getArea( iLoopArea )->isWater();

		if( pLoopPlot->getWilderness() == -1 ) // Starting plots are already at 0
		{
			// LFGR_TODO: Wilderness from terrain and feature
			int iWilderness = -1;
			if( getArea( iLoopArea )->getNumStartingPlots() > 0 || bWaterArea )
			{
				// Plots on inhabited continents or in water
				int iNearestDist = -1;
				int iSecondNearestDist = -1;

				for(int iJ = 0;iJ < GC.getMAX_CIV_PLAYERS(); iJ++)
				{
					CvPlayer& pPlayer = GET_PLAYER((PlayerTypes)iJ);
					if( pPlayer.isEverAlive() )
					{
						CvPlot* pStartPlot = pPlayer.getStartingPlot();
						if( pLoopPlot->getArea() == pStartPlot->getArea() || bWaterArea )
						{
							int iDist = stepDistance( iLoopX, iLoopY, pStartPlot->getX_INLINE(), pStartPlot->getY_INLINE() );

							if( iNearestDist == -1 || iDist < iNearestDist )
							{
								iSecondNearestDist = iNearestDist;
								iNearestDist = iDist;
							}
							else if( iDist < iSecondNearestDist )
							{
								iSecondNearestDist = iDist;
							}
						}
					}
				}

				int iAvDist = 100;

				if( iNearestDist != -1 )
				{
					// Arithmetic ean of nearest starting plot distance and average starting plot distance,
					// but not higher then two times nearest distance
					if( iSecondNearestDist != -1 )
						iAvDist = std::min( iNearestDist * 2, ( iNearestDist * 2 + iSecondNearestDist ) / 3 );
					else
						iAvDist = iNearestDist;
				}// iNearestDist == -1should not happen...
				
				iWilderness = std::min( iAvDist, 100 );
				logBBAI( "      Plot at %d|%d #%d/%d inhabited or water; Distances: %d, %d -> %d; Wilderness: %d",
					iLoopX, iLoopY, iLoopArea, getArea( iLoopArea )->getID(), iNearestDist, iSecondNearestDist, iAvDist, iWilderness );
			}
			else
			{
				// Plots on uninhabited continents
				int iDist = stepDistance( iLoopX, iLoopY, piUAreaMeanX[iLoopArea], piUAreaMeanY[iLoopArea] );
				iWilderness = std::max( 100 - iDist, 0 );
				logBBAI( "      Plot at %d|%d #%d/%d uninhabited; Center distance: %d; Wilderness: %d",
						iLoopX, iLoopY, iLoopArea, getArea( iLoopArea )->getID(), iDist, iWilderness );

				// Distance for later normalization
				int iNearestDist = -1;
				int iSecondNearestDist = -1;

				for(int iJ = 0;iJ < GC.getMAX_CIV_PLAYERS(); iJ++)
				{
					CvPlayer& pPlayer = GET_PLAYER((PlayerTypes)iJ);
					if( pPlayer.isEverAlive() )
					{
						CvPlot* pStartPlot = pPlayer.getStartingPlot();
						int iDist = stepDistance( iLoopX, iLoopY, pStartPlot->getX_INLINE(), pStartPlot->getY_INLINE() );

						if( iNearestDist == -1 || iDist < iNearestDist )
						{
							iSecondNearestDist = iNearestDist;
							iNearestDist = iDist;
						}
						else if( iDist < iSecondNearestDist )
						{
							iSecondNearestDist = iDist;
						}
					}
				}

				int iAvDist = 100;

				if( iNearestDist != -1 )
				{
					// Arithmetic ean of nearest starting plot distance and average starting plot distance,
					// but not higher then two times nearest distance
					if( iSecondNearestDist != -1 )
						iAvDist = std::min( iNearestDist * 2, ( iNearestDist * 2 + iSecondNearestDist ) / 3 );
					else
						iAvDist = iNearestDist;
				}
				
				if( !pLoopPlot->isImpassable() )
				{
					if( piUAreaMaxAvDist[iLoopArea] == -1 || iAvDist > piUAreaMaxAvDist[iLoopArea] )
					{
						logBBAI( "      New area max dist!" );
						piUAreaMaxAvDist[iLoopArea] = iAvDist;
					}
					if( piUAreaMinAvDist[iLoopArea] == -1 || iAvDist < piUAreaMinAvDist[iLoopArea] )
					{
						logBBAI( "      New area min dist!" );
						piUAreaMinAvDist[iLoopArea] = iAvDist;
					}
				
					if( iUAreaMaxMaxAvDist == -1 || iAvDist > iUAreaMaxMaxAvDist )
					{
						logBBAI( "      New global max dist!" );
						iUAreaMaxMaxAvDist = iAvDist;
					}
				}
				
				logBBAI( "        Extra norm distance: %d, %d -> %d", iNearestDist, iSecondNearestDist, iAvDist );
			}
			
			if( !pLoopPlot->isImpassable() )
			{
				if( bWaterArea )
				{
					if( iWaterAreaMaxWilderness == -1 || iWilderness > iWaterAreaMaxWilderness )
						iWaterAreaMaxWilderness = iWilderness;
				}
			
				if( piAreaMaxWilderness[iLoopArea] == -1 || iWilderness > piAreaMaxWilderness[iLoopArea] )
				{
					logBBAI( "      New area max wilderness!" );
					piAreaMaxWilderness[iLoopArea] = iWilderness;
				}
				else
					logBBAI( "      Area max wilderness stays %d.", piAreaMaxWilderness[iLoopArea] );

				if( piAreaMinWilderness[iLoopArea] == -1 || iWilderness < piAreaMinWilderness[iLoopArea] )
				{
					piAreaMinWilderness[iLoopArea] = iWilderness;
					logBBAI( "      New area min wilderness!" );
				}
				else
					logBBAI( "      Area min wilderness stays %d.", piAreaMinWilderness[iLoopArea] );
			}
			
			pLoopPlot->setWilderness( iWilderness );
		}
	}

	// NORMALIZATION
	int MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS" );
	int MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS" );
	if( iNumUAreaTiles <= getLandPlots() * GC.getDefineFLOAT( "WILDERNESS_NO_ISLANDS_THRESHOLD" ) )
	{
		MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS_NO_ISLANDS" );
		MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS_NO_ISLANDS" );
	}
	else if( iNumUAreaTiles <= getLandPlots() * GC.getDefineFLOAT( "WILDERNESS_FEW_ISLANDS_THRESHOLD" ) )
	{
		MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS_FEW_ISLANDS" );
		MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS_FEW_ISLANDS" );
	}
	else if( iNumUAreaTiles >= getLandPlots() * GC.getDefineFLOAT( "WILDERNESS_MANY_ISLANDS_THRESHOLD" ) )
	{
		MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS_MANY_ISLANDS" );
		MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS_MANY_ISLANDS" );
	}

	/*
		General normalization formula:
		We have a factor (f) and a shift (s) value for each area. The formula for the wilderness (w) of a plot is:
			w = w * f + s
		To determine f and s, we take the required min (rMin) and max (rMax) and the actual min (aMin) and max (aMax).
			rMin = aMin * f + s
			rMax = aMax * f + s
		It's a simple system of linear equations.
			...
			s = ( rMin - ( aMin * rMax ) / aMax ) / ( 1 - aMin / aMax )
			f = ( rMax - s ) / aMax
	*/

	// f and s
	float* pfAreaNormFactor = new float[getNumAreas()];
	float* pfAreaNormShift = new float[getNumAreas()];

	logBBAI( "  Normalization" );
	logBBAI( "    Water Max Wilderness: %d", iWaterAreaMaxWilderness );
	logBBAI( "    UArea Max Distance: %d", iUAreaMaxMaxAvDist );

	for( int iArea = 0; iArea < getNumAreas(); iArea++ )
	{
		int iActualMin = piAreaMinWilderness[iArea];
		int iActualMax = piAreaMaxWilderness[iArea];
		int iRequiredMin = 0;
		int iRequiredMax = 100;
		if( getArea( iArea )->isWater() )
		{
			// ocean or lake
			logBBAI( "    Area #%d is water", iArea );

			iActualMax = iWaterAreaMaxWilderness; // share max
			iRequiredMin = iActualMin;
			iRequiredMax = 100;
		}
		else if( getArea( iArea )->getNumStartingPlots() > 0 )
		{
			// inhabited continent
			logBBAI( "    Area #%d is inhabited", iArea );

			iRequiredMin = 0;
			iRequiredMax = MIN_MAX_INHABITED_WILDERNESS + ( MAX_MAX_INHABITED_WILDERNESS - MIN_MAX_INHABITED_WILDERNESS )
					* ( getArea( iArea )->getNumTiles() / getArea( iArea )->getNumStartingPlots() ) / iMaxInhabitedContinentSizePerPlayer;
		}
		else
		{
			// uninhabited continent
			logBBAI( "    Area #%d is uninhabited", iArea );

			iActualMax = 100;
			// LFGR_TODO this can lead to a continent with its center near to the player, but streching far away getting high wilderness values. Maybe need iUAreaCenterMaxAvDist.
			iRequiredMax = 100 * piUAreaMaxAvDist[iArea] / iUAreaMaxMaxAvDist;
			// this should be okay
			iRequiredMin = 100 * piUAreaMinAvDist[iArea] / iUAreaMaxMaxAvDist;
		}
		if( iActualMin != iActualMax )
		{
			pfAreaNormShift[iArea] = ( (float) iRequiredMin - ( (float) iActualMin * (float) iRequiredMax ) / (float) iActualMax ) / ( 1.0f - (float) iActualMin / (float) iActualMax );
			pfAreaNormFactor[iArea] = ( (float) iRequiredMax - pfAreaNormShift[iArea] ) / (float) iActualMax;
		}
		else
		{
			logBBAI( "      !!! aMax = aMin !!!" );
			pfAreaNormShift[iArea] = (float) iRequiredMax - iActualMax;
			pfAreaNormFactor[iArea] = 1.0f;
		}
		logBBAI( "      Real min and max: %d, %d", piAreaMinWilderness[iArea], piAreaMaxWilderness[iArea] );
		logBBAI( "      UArea min and max dist: %d, %d", piUAreaMinAvDist[iArea], piUAreaMaxAvDist[iArea] );
		logBBAI( "      Wilderness: %d-%d -> %d-%d", iActualMin, iActualMax, iRequiredMin, iRequiredMax );
		logBBAI( "      Factor: %f, Shift: %f", pfAreaNormFactor[iArea], pfAreaNormShift[iArea] );
	}
	
	logBBAI( "  Apply normalization" );
	for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
	{
		CvPlot* pLoopPlot = plotByIndexINLINE( iPlot );
		int iLoopArea = pLoopPlot->getArea() & FLTA_INDEX_MASK; // No idea why plots not simply store 0, 1, 2...
		int iNewWilderness = (int) ( pfAreaNormFactor[iLoopArea] * (float) pLoopPlot->getWilderness() + pfAreaNormShift[iLoopArea] );
		
		logBBAI( "  Plot %d|%d: %d -> %d", pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), pLoopPlot->getWilderness(), iNewWilderness );
		logBBAI( "    NewWilderness formula: (int) ( %f * (float) %d + %f )", pfAreaNormFactor[iLoopArea], pLoopPlot->getWilderness(), pfAreaNormShift[iLoopArea] );
		pLoopPlot->setWilderness( std::min( 100, iNewWilderness ) );
	}

	
	// LFGR_TEST
	if( GC.getDefineINT( "DEBUG_PAINT_WILDERNESS_" ) == 1 )
	{
		for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
		{
			CvPlot* pLoopPlot = plotByIndexINLINE( iPlot );
			int iWilderness = pLoopPlot->getWilderness();

			if( !pLoopPlot->isWater() )
			{
				if( !pLoopPlot->isPeak() )
				{
					if( pLoopPlot->isHills() )
						pLoopPlot->setPlotType( PLOT_LAND );
					pLoopPlot->setBonusType( NO_BONUS );
					pLoopPlot->setFeatureType( NO_FEATURE );
					if( iWilderness <= 10 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_DESERT" ) );
					else if( iWilderness <= 20 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_PLAINS" ) );
					else if( iWilderness <= 30 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_GRASS" ) );
					else if( iWilderness <= 40 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_MARSH" ) );
					else if( iWilderness <= 50 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_TUNDRA" ) );
					else if( iWilderness <= 60 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_SNOW" ) );
					else if( iWilderness <= 70 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_FIELDS_OF_PERDITION" ) );
					else if( iWilderness <= 80 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_BROKEN_LANDS" ) );
					else if( iWilderness <= 90 )
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_SHALLOWS" ) );
					else
						pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_BURNING_SANDS" ) );
				}
			}
			else
			{
				if( iWilderness <= 50 )
					pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_COAST" ) );
				else
					pLoopPlot->setTerrainType( (TerrainTypes) GC.getInfoTypeForString( "TERRAIN_OCEAN" ) );
			}
		}
	}
	

// LFGR_TODO: choke points?
//	for (iI = 0; iI < numPlotsINLINE(); iI++)
//	{
//		pLoopPlot = plotByIndexINLINE(iI);
//		int iChokeValue = pLoopPlot->getChokeValue();
//		if( iChokeValue >= 5 )
//		{
//			int iChokeMod = std::min( iChokeValue * 3, pLoopPlot->getWilderness() * 2 ); // cannot be higher than wild*2
//			pLoopPlot->setWilderness( std::max( pLoopPlot->getWilderness(), ( iChokeMod + pLoopPlot->getWilderness() ) / 2 ) ); // max is wild*3/2
//			int iLoopX = pLoopPlot->getX_INLINE();
//			int iLoopY = pLoopPlot->getY_INLINE();
//			for( int iX = iLoopX - 1; iX <= iLoopX + 1; iX++ )
//				for( int iY = iLoopY - 1; iY <= iLoopY + 1; iY++ )
//					if( iX >= 0 && iX < getGridWidthINLINE() && iY >= 0 && iY < getGridHeightINLINE()  )
//					{
//						CvPlot* pLoopPlot2 = plot( iX, iY );
//						int iChokeMod2 = std::min( iChokeValue * 2, pLoopPlot2->getWilderness() * 3 / 2 ); // cannot be higher than wild*1.5
//						pLoopPlot2->setWilderness( std::max( pLoopPlot2->getWilderness(), ( iChokeMod + pLoopPlot2->getWilderness() ) / 2 ) ); // max is wild*5/4
//					}
//		}
//	}
}
/************************************************************************************************/
/* WILDERNESS                                                                     END           */
/************************************************************************************************/


// Private Functions...
