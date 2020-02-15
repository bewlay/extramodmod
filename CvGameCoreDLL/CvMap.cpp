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
#include <map>
#include <queue>
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
// Comparison function for the priority queue
template<class V>
struct PairComparator
{
    bool operator()( std::pair<float, V> a, std::pair<float, V> b ) const
    {
        return a.first > b.first;
    }
};

void CvMap::calculateWilderness()
{
	// Variable used for area iterators
	int iLoop;

	logTo( "wilderness - %S.log", "calculateWilderness()" );
	logTo( "wilderness - %S.log", "Mapscript: %S, size: %dx%d%s%s, %d players alive", GC.getIniInitCore().getMapScriptName().GetCString(),
			GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE(),
			GC.getGameINLINE().isOption( GAMEOPTION_RAGING_BARBARIANS ) ? ", ranging barbarians" : "",
			GC.getGameINLINE().isOption( GAMEOPTION_DOUBLE_ANIMALS ) ? ", double animals" : "",
			GC.getGameINLINE().countCivPlayersAlive()
			 );
	logTo( "wilderness - %S.log", "Mapscript: %S", GC.getIniInitCore().getMapScriptName().GetCString() );
	logTo( "wilderness - %S.log", "Map Size: %dx%d", GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE() );
	logTo( "wilderness - %S.log", "Game Speed: %S", GC.getGameSpeedInfo( GC.getGameINLINE().getGameSpeedType() ).getDescription() );
	logTo( "wilderness - %S.log", "Raging Barbarians: %s", GC.getGameINLINE().isOption( GAMEOPTION_RAGING_BARBARIANS ) ? "yes" : "no" );
	logTo( "wilderness - %S.log", "Double Animals: %s", GC.getGameINLINE().isOption( GAMEOPTION_DOUBLE_ANIMALS ) ? "yes" : "no" );
	logTo( "wilderness - %S.log", "Number of Players: %d", GC.getGameINLINE().countCivPlayersAlive() );

	bool bLogVerbose = false;

	// Reset starting points of each player with capital cities
	for( int ePlayer = 0; ePlayer < GC.getMAX_CIV_PLAYERS(); ePlayer++ )
	{
		if( GET_PLAYER( (PlayerTypes) ePlayer ).isAlive() )
		{
			if( GET_PLAYER( (PlayerTypes) ePlayer ).getCapitalCity() != NULL )
			{
				logTo( "wilderness - %S.log", "  Resetting player %d's starting plot to capital", ePlayer );
				GET_PLAYER( (PlayerTypes) ePlayer ).setStartingPlot( GET_PLAYER( (PlayerTypes) ePlayer ).getCapitalCity()->plot(), true );
			}
		}
	}
	
	logTo( "wilderness - %S.log", "  Area summary" );
//#ifdef LOG_AI
	for( int iArea = 0; iArea < getNumAreas(); iArea++ )
		logTo( "wilderness - %S.log", "    Area #%d: %d plots%s%s", getArea( iArea )->getID(), getArea( iArea )->getNumTiles(), getArea( iArea )->isWater() ? ", water" : "",
				getArea( iArea )->getNumStartingPlots() > 0 ? ", inhabited" : "" );
//#endif

	// Continents
	// Find geometric mean for uninhabited continents
	std::map<int, int> miiUAreaMeanX;
	std::map<int, int> miiUAreaMeanY;

	// Count number of uninhabited continent tiles
	int iNumUAreaTiles = 0;
	
	for( CvArea* pLoopArea = firstArea( &iLoop ); pLoopArea != NULL; pLoopArea = nextArea( &iLoop ) )
	{
		if( pLoopArea->getNumStartingPlots() == 0 && !pLoopArea->isWater() )
		{
			miiUAreaMeanX[pLoopArea->getID()] = 0;
			miiUAreaMeanY[pLoopArea->getID()] = 0;
			iNumUAreaTiles += pLoopArea->getNumTiles();
		}
		else
		{
			miiUAreaMeanX[pLoopArea->getID()] = -1;
			miiUAreaMeanY[pLoopArea->getID()] = -1;
		}
	}

	for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
	{
		CvPlot* pLoopPlot = plotByIndexINLINE( iPlot );
		int iLoopArea = pLoopPlot->getArea();
		if( getArea( iLoopArea )->getNumStartingPlots() == 0 && !getArea( iLoopArea )->isWater() )
		{
			miiUAreaMeanX[iLoopArea] += pLoopPlot->getX_INLINE();
			miiUAreaMeanY[iLoopArea] += pLoopPlot->getY_INLINE();
		}
	}
	
	logTo( "wilderness - %S.log", "  Uninhabited contintent centers:" );
	for( CvArea* pLoopArea = firstArea( &iLoop ); pLoopArea != NULL; pLoopArea = nextArea( &iLoop ) )
	{
		if( pLoopArea->getNumStartingPlots() == 0 && !pLoopArea->isWater() )
		{
			miiUAreaMeanX[pLoopArea->getID()] /= pLoopArea->getNumTiles();
			miiUAreaMeanY[pLoopArea->getID()] /= pLoopArea->getNumTiles();

			logTo( "wilderness - %S.log", "    Area #%d: %d|%d", pLoopArea->getID(), miiUAreaMeanX[pLoopArea->getID()], miiUAreaMeanY[pLoopArea->getID()] );
		}
	}
	const float WILDERNESS_NEAREST_DISTANCE_FACTOR = GC.getDefineFLOAT( "WILDERNESS_NEAREST_DISTANCE_FACTOR" );
	const float WILDERNESS_SEC_NEAREST_DISTANCE_FACTOR = GC.getDefineFLOAT( "WILDERNESS_SEC_NEAREST_DISTANCE_FACTOR" );
	
	// Store max and min wilderness for all continents
	std::map<int, int> miiAreaMaxWilderness;
	std::map<int, int> miiAreaMinWilderness;
	int iWaterAreaMaxWilderness = -1;

	// Store max and min average starting plot distance for all uninhabited continents
	std::map<int, int> miiUAreaMinAvDist;
	std::map<int, int> miiUAreaMaxAvDist;
	int iUAreaMaxMaxAvDist = -1;
	// Store max continent size divided by number of players on that continent
	int iMaxInhabitedContinentSizePerPlayer = -1;
	// Store first iteration wilderness values. Use float since it's scaled after normalization.
	// LFGR_TODO: Best remove all floating point calculations to prevent OOS
	float* pfPlotWilderness = new float[numPlotsINLINE()];

	for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
		pfPlotWilderness[iPlot] = -1;
	
	for( CvArea* pLoopArea = firstArea( &iLoop ); pLoopArea != NULL; pLoopArea = nextArea( &iLoop ) )
	{
		int iArea = pLoopArea->getID();
		miiAreaMaxWilderness[iArea] = -1;
		miiAreaMinWilderness[iArea] = -1;
		miiUAreaMinAvDist[iArea] = -1;
		miiUAreaMaxAvDist[iArea] = -1;


		if (!getArea(iArea)->isWater()) {
			if (getArea(iArea)->getNumStartingPlots() > 0) {
				iMaxInhabitedContinentSizePerPlayer = std::max( iMaxInhabitedContinentSizePerPlayer, getArea(iArea)->getNumTiles() / getArea(iArea)->getNumStartingPlots() );
			}
		}
		//logTo( "wilderness - %S.log", "    Area #%d after init real min and max: %d, %d", iArea, miiAreaMinWilderness[iArea], miiAreaMaxWilderness[iArea] );
		//logTo( "wilderness - %S.log", "    Area #%d after init UArea min and max dist: %d, %d", iArea, miiUAreaMinAvDist[iArea], miiUAreaMaxAvDist[iArea] );
	}
	
	logTo( "wilderness - %S.log", "  Max inhabited continent size per player: %d", iMaxInhabitedContinentSizePerPlayer );
	
	// Using a modificated version of Dijkstra's algorithm to compute distances from starting plots
	// Since the graph is very sparse (max degree 8, a constant), this should run O(n*log(n)), with n being the number of plots.

	std::priority_queue< std::pair<float, int>, std::vector< std::pair<float, int> >, PairComparator<int> > queue;

	logTo( "wilderness - %S.log", "  Initializing starting distances" );
	// Set starting plot distance to 0
	for( int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++ )
	{
		CvPlayer& pPlayer = GET_PLAYER( (PlayerTypes) iPlayer );
		if( pPlayer.isAlive() )
		{
			CvPlot* pStartingPlot = pPlayer.getStartingPlot();
			if( pStartingPlot != NULL )
			{
				int iPlot = plotNumINLINE( pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE() );
				FAssert( iPlot >= 0 && iPlot < numPlotsINLINE() );
				queue.push( std::pair<float, int>( 0, iPlot ) );
			}
		}
	}

	const int WILDERNESS_IMPASSABLE_MOVEMENT_COST = GC.getDefineINT( "WILDERNESS_IMPASSABLE_MOVEMENT_COST", 30 );
	const int WILDERNESS_CHOKE_MAX_MOVEMENT_COST = GC.getDefineINT( "WILDERNESS_CHOKE_MAX_MOVEMENT_COST", 20 );
	const int WILDERNESS_CHOKE_MOVEMENT_DIVISOR = GC.getDefineINT( "WILDERNESS_CHOKE_MOVEMENT_DIVISOR", 10 );

	logTo( "wilderness - %S.log", "  Starting Dijkstra" );
	// Set wilderness for all plots
	while( !queue.empty() )
	{
		// Update distance for top plot
		std::pair<float, int> kPair = queue.top();
		queue.pop();

		int iPlot = kPair.second;
		// Plot already reached?
		if( pfPlotWilderness[iPlot] != -1 )
			continue;
		
		float fDistance = kPair.first;
		CvPlot* pPlot = plotByIndexINLINE( iPlot );

		pfPlotWilderness[iPlot] = fDistance;
		if( bLogVerbose )
			logTo( "wilderness - %S.log", "    Distance at %d|%d: %f", pPlot->getX_INLINE(), pPlot->getY_INLINE(), fDistance );

		bool bWater = getArea( pPlot->getArea() )->isWater();

		// Add steps to nearby plots in same area
		for( int iNX = pPlot->getX_INLINE() - 1; iNX <= pPlot->getX_INLINE() + 1; iNX++ )
		{
			for( int iNY = pPlot->getY_INLINE() - 1; iNY <= pPlot->getY_INLINE() + 1; iNY++ )
			{
				if( iNX != pPlot->getX_INLINE() || iNY != pPlot->getY_INLINE() )
				{
					int iNPlot = plotNumINLINE( iNX, iNY );
					CvPlot* pNPlot = plotINLINE( iNX, iNY ); // Don't use iNPlot to be sure to get NULL if out of range

					// Neighbour plot must exist, mustn't yet be reached
					if( pNPlot != NULL && pfPlotWilderness[iNPlot] == -1 )
					{
						bool bNWater = getArea( pNPlot->getArea() )->isWater();

						// We can't walk from a water to a land plot
						if( !( bWater && !bNWater ) )
						{
							float fNDistance = fDistance;
							if( pNPlot->isImpassable() )
								fNDistance += WILDERNESS_IMPASSABLE_MOVEMENT_COST;
							else
							{
								fNDistance += std::min( WILDERNESS_CHOKE_MAX_MOVEMENT_COST, pNPlot->getChokeValue() / WILDERNESS_CHOKE_MOVEMENT_DIVISOR );
								if( pNPlot->getFeatureType() == NO_FEATURE )
									fNDistance += GC.getTerrainInfo( pNPlot->getTerrainType() ).getMovementCost();
								else
									fNDistance += GC.getFeatureInfo( pNPlot->getFeatureType() ).getMovementCost();
								if ( pNPlot->isHills() )
									fNDistance += GC.getHILLS_EXTRA_MOVEMENT();
							}
							queue.push( std::pair<float, int>( fNDistance, iNPlot ) );
						}
					}
				}
			}
		}
	}
	
	// Wilderness for uninhabited continents and min/max wilderness per area / in water
	logTo( "wilderness - %S.log", "  Computing uninhabited contintent wilderness" );
	for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
	{
		CvPlot* pLoopPlot = plotByIndexINLINE( iPlot );
		int iLoopX = pLoopPlot->getX_INLINE();
		int iLoopY = pLoopPlot->getY_INLINE();
		int iLoopArea = pLoopPlot->getArea();
		bool bWaterArea = getArea( iLoopArea )->isWater();

		if( getArea( iLoopArea )->getNumStartingPlots() == 0 && !bWaterArea )
		{
			// Uninhabited
			int iNearestDist = -1;
			int iSecondNearestDist = -1;

			for(int iJ = 0;iJ < GC.getMAX_CIV_PLAYERS(); iJ++)
			{
				CvPlayer& pPlayer = GET_PLAYER((PlayerTypes)iJ);
				if( pPlayer.isEverAlive() )
				{
					CvPlot* pStartPlot = pPlayer.getStartingPlot();
					if( getArea( iLoopArea )->getNumStartingPlots() == 0 || pLoopPlot->getArea() == pStartPlot->getArea() )
					{
						int iDist = stepDistance( iLoopX, iLoopY, pStartPlot->getX_INLINE(), pStartPlot->getY_INLINE() );

						if( iNearestDist == -1 || iDist < iNearestDist )
						{
							iSecondNearestDist = iNearestDist;
							iNearestDist = iDist;
						}
						else if( iSecondNearestDist == -1 || iDist < iSecondNearestDist )
						{
							iSecondNearestDist = iDist;
						}
					}
				}
			}
		
			float fAvDist = 100.0f;

			if( iNearestDist != -1 )
			{
				if( iSecondNearestDist == -1 )
					iSecondNearestDist = iNearestDist;

				// Not higher then nearest distance, to get not more than +1 Wilderness per plot (before normalization).
				fAvDist = 0.5f * ( iNearestDist * WILDERNESS_NEAREST_DISTANCE_FACTOR + iSecondNearestDist * WILDERNESS_SEC_NEAREST_DISTANCE_FACTOR );
				fAvDist = std::min( (float) iNearestDist, fAvDist );
			}
			else // iNearestDist == -1 should not happen...
				FAssertMsg( false, "iNearestDist == -1" );
		
			float fWilderness = -1.0f;
			int iDist = stepDistance( iLoopX, iLoopY, miiUAreaMeanX[iLoopArea], miiUAreaMeanY[iLoopArea] );
			fWilderness = std::max( 100.0f - iDist, 0.0f );
			if( bLogVerbose )
				logTo( "wilderness - %S.log", "      Plot at %d|%d #%d/%d uninhabited; Center distance: %d; Wilderness: %f",
						iLoopX, iLoopY, iLoopArea, getArea( iLoopArea )->getID(), iDist, fWilderness );
			
			if( !pLoopPlot->isImpassable() )
			{
				if( miiUAreaMaxAvDist[iLoopArea] == -1 || (int) fAvDist > miiUAreaMaxAvDist[iLoopArea] )
				{
					if( bLogVerbose )
						logTo( "wilderness - %S.log", "      New area max dist!" );
					miiUAreaMaxAvDist[iLoopArea] = (int) fAvDist;
				}
				if( miiUAreaMinAvDist[iLoopArea] == -1 || (int) fAvDist < miiUAreaMinAvDist[iLoopArea] )
				{
					if( bLogVerbose )
						logTo( "wilderness - %S.log", "      New area min dist!" );
					miiUAreaMinAvDist[iLoopArea] = (int) fAvDist;
				}
			
				if( iUAreaMaxMaxAvDist == -1 || (int) fAvDist > iUAreaMaxMaxAvDist )
				{
					if( bLogVerbose )
						logTo( "wilderness - %S.log", "      New global max dist!" );
					iUAreaMaxMaxAvDist = (int) fAvDist;
				}
			}
			
			if( bLogVerbose )
				logTo( "wilderness - %S.log", "        Extra norm distance: %d, %d -> %d", iNearestDist, iSecondNearestDist, (int) fAvDist );
		
			pfPlotWilderness[iPlot] = fWilderness;
		}

		// Updating max/min wilderness for *each* plot, not only in uninhabited areas
		if( !pLoopPlot->isImpassable() )
		{
			if( bWaterArea )
			{
				if( iWaterAreaMaxWilderness == -1 || (int) pfPlotWilderness[iPlot] > iWaterAreaMaxWilderness )
					iWaterAreaMaxWilderness = (int) pfPlotWilderness[iPlot];
			}
			
			if( miiAreaMaxWilderness[iLoopArea] == -1 || (int) pfPlotWilderness[iPlot] > miiAreaMaxWilderness[iLoopArea] )
			{
				miiAreaMaxWilderness[iLoopArea] = (int) pfPlotWilderness[iPlot];
			}

			if( miiAreaMinWilderness[iLoopArea] == -1 || (int) pfPlotWilderness[iPlot] < miiAreaMinWilderness[iLoopArea] )
			{
				miiAreaMinWilderness[iLoopArea] = (int) pfPlotWilderness[iPlot];
			}
		}
	}

	// NORMALIZATION
	logTo( "wilderness - %S.log", "  Starting normalization" );
	logTo( "wilderness - %S.log", "    Number of land plots in uninhabited areas: %d/%d", iNumUAreaTiles, getLandPlots() );
	int MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS" );
	int MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS" );
	if( iNumUAreaTiles <= getLandPlots() * GC.getDefineFLOAT( "WILDERNESS_NO_ISLANDS_THRESHOLD" ) )
	{
		logTo( "wilderness - %S.log", "      -> No Islands" );
		MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS_NO_ISLANDS" );
		MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS_NO_ISLANDS" );
	}
	else if( iNumUAreaTiles <= getLandPlots() * GC.getDefineFLOAT( "WILDERNESS_FEW_ISLANDS_THRESHOLD" ) )
	{
		logTo( "wilderness - %S.log", "      -> Few Islands" );
		MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS_FEW_ISLANDS" );
		MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS_FEW_ISLANDS" );
	}
	else if( iNumUAreaTiles >= getLandPlots() * GC.getDefineFLOAT( "WILDERNESS_MANY_ISLANDS_THRESHOLD" ) )
	{
		logTo( "wilderness - %S.log", "      -> Many Islands" );
		MIN_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MIN_MAX_INHABITED_WILDERNESS_MANY_ISLANDS" );
		MAX_MAX_INHABITED_WILDERNESS = GC.getDefineINT( "WILDERNESS_MAX_MAX_INHABITED_WILDERNESS_MANY_ISLANDS" );
	}
	logTo( "wilderness - %S.log", "    Max wilderness for inhabited areas: %d-%d", 
			MIN_MAX_INHABITED_WILDERNESS, MAX_MAX_INHABITED_WILDERNESS );

	float WILDERNESS_MAX_INHABITED_INCREASE_PER_PLOT = GC.getDefineFLOAT( "WILDERNESS_MAX_INHABITED_INCREASE_PER_PLOT" );

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
	std::map<int,float> mifAreaNormFactor;
	std::map<int,float> mifAreaNormShift;

	logTo( "wilderness - %S.log", "    Water Max Wilderness: %d", iWaterAreaMaxWilderness );
	logTo( "wilderness - %S.log", "    UArea Max Distance: %d", iUAreaMaxMaxAvDist );
	
	for( CvArea* pLoopArea = firstArea( &iLoop ); pLoopArea != NULL; pLoopArea = nextArea( &iLoop ) )
	{
		int iArea = pLoopArea->getID();
		int iActualMin = miiAreaMinWilderness[iArea];
		int iActualMax = miiAreaMaxWilderness[iArea];
		int iRequiredMin = 0;
		int iRequiredMax = 100;
		if( pLoopArea->isWater() )
		{
			// ocean or lake
			logTo( "wilderness - %S.log", "    Area #%d is water", iArea );

			iActualMax = iWaterAreaMaxWilderness; // share max
			iRequiredMin = iActualMin;
			iRequiredMax = 100;
		}
		else if( pLoopArea->getNumStartingPlots() > 0 )
		{
			// inhabited continent
			logTo( "wilderness - %S.log", "    Area #%d is inhabited", iArea );

			iRequiredMin = 0;
			iRequiredMax = MIN_MAX_INHABITED_WILDERNESS + ( MAX_MAX_INHABITED_WILDERNESS - MIN_MAX_INHABITED_WILDERNESS )
					* ( pLoopArea->getNumTiles() / pLoopArea->getNumStartingPlots() ) / iMaxInhabitedContinentSizePerPlayer;
		}
		else
		{
			// uninhabited continent
			logTo( "wilderness - %S.log", "    Area #%d is uninhabited", iArea );

			iActualMax = 100;
			// LFGR_TODO this can lead to a continent with its center near to the player, but streching far away getting high wilderness values. Maybe need iUAreaCenterMaxAvDist.
			iRequiredMax = 100 * miiUAreaMaxAvDist[iArea] / iUAreaMaxMaxAvDist;
			// this should be okay
			iRequiredMin = 100 * miiUAreaMinAvDist[iArea] / iUAreaMaxMaxAvDist;
		}
		if( iActualMin != iActualMax )
		{
			mifAreaNormShift[iArea] = ( (float) iRequiredMin - ( (float) iActualMin * (float) iRequiredMax ) / (float) iActualMax ) / ( 1.0f - (float) iActualMin / (float) iActualMax );
			mifAreaNormFactor[iArea] = ( (float) iRequiredMax - mifAreaNormShift[iArea] ) / (float) iActualMax;
		}
		else
		{
			logTo( "wilderness - %S.log", "      !!! aMax = aMin !!! Tiles: %d", getArea( iArea )->getNumTiles() );
			mifAreaNormShift[iArea] = (float) iRequiredMax - iActualMax;
			mifAreaNormFactor[iArea] = 1.0f;
		}

		if( pLoopArea->getNumStartingPlots() > 0 || pLoopArea->isWater() )
		{
			// Now, since we ensured a maximum increase of 1.0 per plot before normalization, we can check the factor.
			if( mifAreaNormFactor[iArea] > WILDERNESS_MAX_INHABITED_INCREASE_PER_PLOT )
			{
				logTo( "wilderness - %S.log", "      Factor %f exceeds limit", mifAreaNormFactor[iArea] );
				mifAreaNormFactor[iArea] = WILDERNESS_MAX_INHABITED_INCREASE_PER_PLOT;

				// We want to retain min wilderness.
				// rMin = aMin * f + s => s = rMin - aMin * f
				mifAreaNormShift[iArea] = (float) iRequiredMin - iActualMin * mifAreaNormFactor[iArea];

#ifdef LOG_AI
				// Update for logging
				iRequiredMax = (int) ( iActualMax * mifAreaNormFactor[iArea] + mifAreaNormShift[iArea] );
#endif
			}
		}

		//logTo( "wilderness - %S.log", "      Real min and max: %d, %d", miiAreaMinWilderness[iArea], miiAreaMaxWilderness[iArea] );
		if( pLoopArea->getNumStartingPlots() > 0 ) {
			logTo( "wilderness - %S.log", "      UArea min and max dist: %d, %d", miiUAreaMinAvDist[iArea], miiUAreaMaxAvDist[iArea] );
		}
		//logTo( "wilderness - %S.log", "      Factor: %f, Shift: %f", mifAreaNormFactor[iArea], mifAreaNormShift[iArea] );
		logTo( "wilderness - %S.log", "      Wilderness: %d-%d -> %d-%d", iActualMin, iActualMax, iRequiredMin, iRequiredMax );
	}

	// Count wilderness distribution in next step, for log
	int aiPassableLandWildernessDistribution[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
	int iTotalPassableLand = 0;
	
	logTo( "wilderness - %S.log", "  Apply normalization" );
	for( int iPlot = 0; iPlot < numPlotsINLINE(); iPlot++ )
	{
		CvPlot* pLoopPlot = plotByIndexINLINE( iPlot );
		int iLoopArea = pLoopPlot->getArea();
		int iNewWilderness = (int) ( mifAreaNormFactor[iLoopArea] * pfPlotWilderness[iPlot] + mifAreaNormShift[iLoopArea] );
		if( bLogVerbose )
		{
			logTo( "wilderness - %S.log", "    Plot %d|%d: %f -> %d", pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), pfPlotWilderness[iPlot], iNewWilderness );
			//logTo( "wilderness - %S.log", "      NewWilderness formula: (int) ( %f * (float) %d + %f )", pfAreaNormFactor[iLoopArea], pfPlotWilderness[iPlot], pfAreaNormShift[iLoopArea] );
		}
		pLoopPlot->setWilderness( std::min( 100, iNewWilderness ) );

		if( !pLoopPlot->isWater() && !pLoopPlot->isImpassable() ) {
			aiPassableLandWildernessDistribution[std::min( 99, iNewWilderness ) / 10]++;
			iTotalPassableLand++;
		}
	}
	
	SAFE_DELETE_ARRAY( pfPlotWilderness );

	logTo( "wilderness - %S.log", "  Wilderness distribution:" );
	for( int i = 0; i < 10; i++ ) {
		logTo( "wilderness - %S.log", "    %d-%d: %d (%d%%)",
				i * 10, (i == 9 ? 100 : i * 10 + 9), aiPassableLandWildernessDistribution[i],
				100 * aiPassableLandWildernessDistribution[i] / iTotalPassableLand );
	}
	
	// LFGR_TEST
	if( GC.getDefineINT( "DEBUG_PAINT_WILDERNESS" ) == 1 )
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
}
/************************************************************************************************/
/* WILDERNESS                                                                     END           */
/************************************************************************************************/


// Private Functions...
