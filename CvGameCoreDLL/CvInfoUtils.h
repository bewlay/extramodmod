// InfoUtils 04/2020 lfgr

// Functions that are useful when dealing with CvInfos


#ifndef CVINFOUTILS_H_
#define CVINFOUTILS_H_

#pragma once


#include "CvGlobals.h"

namespace info_utils {
	// The actual cost of the given spell, taking game speed into account
	int getRealSpellCost( PlayerTypes ePlayer, SpellTypes eSpell );
}

#endif /* CVINFOUTILS_H_ */