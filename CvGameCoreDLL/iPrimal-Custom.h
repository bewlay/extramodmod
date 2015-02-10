// TERRAIN_FLAVOUR 04/2013 lfgr

#pragma once

#ifndef IPRIMAL_CUSTOM_H
#define IPRIMAL_CUSTOM_H

#include "CvGlobals.h"

#include "iPrimal-Define.h"
#include "iPrimal.h"

void reassignStartingPlots();
mat buildCostMatrix();
double getScore( int ePlayer, int ePlayerStartingPlot );

#endif
