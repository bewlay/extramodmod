// TERRAIN_FLAVOUR 04/2013 lfgr

#include "CvGameCoreDLL.h"

#include "iPrimal-Custom.h"

#include "iPrimal.h"
#include "BetterBTSAI.h"
#include "FAssert.h"

// Utilities: Need to skip non-alive players; but iPrimal engine needs a compact matrix
int getNumAvailablePlayers()
{
	int iCount = 0;
	for( int i = 0; i < GC.getMAX_PLAYERS(); i++ )
		if( GET_PLAYER( (PlayerTypes) i ).isAlive() && !GET_PLAYER( (PlayerTypes) i ).isBarbarian() )
			iCount++;
	return iCount;
}

CvPlayerAI& getAvailablePlayer( int eAvPlayer )
{
	FAssertMsg( eAvPlayer < getNumAvailablePlayers(), "index out of range" );
	FAssertMsg( eAvPlayer >= 0, "index out of range" );

	int iCount = 0;
	for( int i = 0; i < GC.getMAX_PLAYERS(); i++ )
		if( GET_PLAYER( (PlayerTypes) i ).isAlive() && !GET_PLAYER( (PlayerTypes) i ).isBarbarian() )
		{
			if( iCount == eAvPlayer )
				return GET_PLAYER( (PlayerTypes) i );
			iCount++;
		}
	return *( (CvPlayerAI*) NULL );
}

void reassignStartingPlots()
{
	// solve the minimal cost (maximal gain) problem
	mat vvdCostMatrix = buildCostMatrix();

	Primal primal( vvdCostMatrix );
	
    vector<uint> asgn_vec;
    primal.GreedyApprox2( asgn_vec );
    primal.InitSolution( asgn_vec );

	// save old startingPlots
	int* aiOldXs = new int[getNumAvailablePlayers()];
	int* aiOldYs = new int[getNumAvailablePlayers()];

	// LFGR_TODO ~ CvPlot.setIsStartingPlot() ?
	for( int i = 0; i < getNumAvailablePlayers(); i++ )
	{
		aiOldXs[i] = getAvailablePlayer( i ).getStartingPlot()->getX_INLINE();
		aiOldYs[i] = getAvailablePlayer( i ).getStartingPlot()->getY_INLINE();
		logBBAI( "Starting plot for player %d: %d|%d", i, aiOldXs[i], aiOldYs[i] );
	}
	
	for( int i = 0; i < getNumAvailablePlayers(); i++ )
	{
		int iOtherPlayer = primal.GetAssignedRow( i );
		if( iOtherPlayer != i )
		{
		getAvailablePlayer( i ).setStartingPlot(
				GC.getMapINLINE().plotSorenINLINE( aiOldXs[iOtherPlayer], aiOldYs[iOtherPlayer] ), true /*LFGR_TODO: ?*/ );
		logBBAI( "Pushed player %d to former %d starting plot: %d|%d", i, iOtherPlayer, aiOldXs[iOtherPlayer], aiOldYs[iOtherPlayer] );
		}
		else
			{
				logBBAI( "Pushed player %d stays at old starting plot: %d|%d", i, aiOldXs[iOtherPlayer], aiOldYs[iOtherPlayer] );
		}
	}
	
	SAFE_DELETE_ARRAY( aiOldXs );
	SAFE_DELETE_ARRAY( aiOldYs );
}

mat buildCostMatrix()
{
	mat vvdMatrix;
	
	for( int eAvPlayer = 0; eAvPlayer < getNumAvailablePlayers(); eAvPlayer++ )
	{
		vector<double> row;
		logBBAI( "Scores for player %d:", eAvPlayer );
		
		for( int eAvPlayerStartingPlot = 0; eAvPlayerStartingPlot < getNumAvailablePlayers(); eAvPlayerStartingPlot++ )
		{
			FAssertMsg( getAvailablePlayer( eAvPlayerStartingPlot ).getStartingPlot() != NULL, "player has no starting plot!" );
			
			TerrainFlavourTypes eTerrainFlavour = (TerrainFlavourTypes) GC.getCivilizationInfo( getAvailablePlayer( eAvPlayer ).getCivilizationType() ).getTerrainFlavour();
			CvTerrainAmountCache kTerrainAmounts = getAvailablePlayer( eAvPlayerStartingPlot ).getStartingPlot()->getTerrainAmounts();
			double dScore = getAvailablePlayer( eAvPlayerStartingPlot ).getStartingPlot()->calcTerrainFlavourWeight( eTerrainFlavour, &kTerrainAmounts );

			row.push_back( -dScore );
			
			logBBAI( "  at player %d's starting plot: %f", eAvPlayerStartingPlot, dScore );
		}

		vvdMatrix.push_back( row );
	}
	
	return vvdMatrix;
}
