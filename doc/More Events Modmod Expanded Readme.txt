					FFH More Events Modmod Expanded v1.0
					For Fall from Heaven 2 0.41m


This is an expansion of the "FFH More Events ModMod" by Black Imperator, done at his specific request. All the events from that mod are here, updated to patch M, and 24 new random events are added by me, Ostar. About three-quarters of them are my creation, the other come from the 'Ideas Needed: Common Events' thread in the Fall From Heaven forum in CivFanatics.com. A full list of new events (spoilerish) are at the bottom of this file.

The original "More Events Modmod" events are updated to patch M and also now incorporate the bug fixes and streamlining that Sephi applied to them in the "Wildmana" mod. I proofread them and fixed some spelling and grammar errors. Also I noticed all but 1 of the More Events events were set to possibly recur multiple times per player throught the game, unlike almost all FFH events which are set to only occur once per player. So I set the tag (bRecurring) to 0 from 1 for most every event to make the More Events events in line with all other events. Some that seemed likely to recur (plague, a few others) I kept at 1 to allow for a reoccurence.

A few "More Events Modmod" events were still a little bugged or could trigger too early, so I tweaked them. 
Specifically:
Redecoration (Palace) - could trigger before the player even had the chance of having Marble/Gold/Copper, so I set PreReq Techs to Mining and Masonry.
Skilled Jeweler - had a bug where some civs could get the wrong building (like Luichirp a Pallens Engine), so fixed that.
Traveller - all the choices require gold, so I set the trigger to check for a minimum gold amount. 
Board Game - set the PreReq Tech to Writing from None, added a check for minimum gold since all choices require that.
Ancient Burial - fixed a potential bug by checking for the Plot being Empty first.
Younger Council - set the PreReq Tech to Education from None.
That Kind of Day - fixed from firing continually for the Clan, since the original python code keep seeing their own units as Barbarians too.
A couple of events that were pointless for Infernal civs, like Cookbook, I set a python filter (canTriggerInfernalFilter) for them to not trigger on.

Everyone is encouraged to import any or all of theses events for their use. I have code commented almost every file below where possible to show what changes from the original FFH files occurred. 

Also included are a Event with Images for FFH compatible xml and event image dds files for those who want to use my Events with Images for FFH modmod as well.
 
Instructions for install or merging are next.



To Install:

1. Unzip the files into a temporary directory, or directly into your FFH install directory - but be warned that way you will overwrite files mentioned below. Backup those files first. If you choose a temporary directory, follow 2-4 below, but still backup your original files just in case.

2. Copy the Python folder into your Beyond the Sword\Mods\Fall from Heaven 2\Assets folder. 
The are three files in this folder: CvEventManager.py in the python folder, and in the entrypoints subfolder: CvRandomEventInterface.py and CvSpellInterface.py.

3. Copy the XML folder into your Beyond the Sword\Mods\Fall from Heaven 2\Assets. 
There are five subfolders - Buildings, Events, Terrain, Text, and Units. 
The Buildings subfolder has two files: CIV4BuildingClassInfos.xml and CIV4BuildingInfos.xml.
The Events subfolder has two files: CIV4EventInfos.xml and CIV4EventTriggerInfos.xml.
The Terrain subfolder has one file: CIV4ImprovementInfos.xml. 
The Text subfolder has one file: CIV4GameText_More_Events_Expanded.xml.
The Units subfolder has four files: CIV4UnitInfos.xml, CIV4UnitClassInfos.xml, CIV4SpellInfos.xml, and CIV4PromotionInfos.xml. 

4. The Optional and Art/EventImages subfolders are only for using Events with Images for FFH as detailed below. If you are not using that, then ignore/delete them.



To Merge into an existing mod/installation:

You can basically merge either the whole "More Events Modmod Expanded", or just the original "More Events Modmod", or just the "Expanded" portion with the 24 new events. Almost all the 13 files for merging have comments marking the changes as detailed below. 
To include only "More Events Modmod" use those comments (in all 13 files).
To include only the "Expanded" portion use those comments (in 4 files - CIV4EventInfos.xml, CIV4EventTriggerInfos.xml, CIV4GameText_More_Events_Expanded.xml, CvRandomEventInterface.py). 
To include everything include both commented sections (13 files).
Of course you can also pick and choose from them as you wish, using the steps below as an aid.    

OK 1. The CvRandomEventInterface.py file has the additions for this mod at the end. The "More Events Modmod" section is between the comments # More Events Mod starts # and # More Events Mod ends #. The "Expanded" portion is between ######## MORE EVENTS MOD EXPANDED STARTS ######## and ######## MORE EVENTS MOD EXPANDED ENDS ########. One piece of code, def canTriggerInfernalFilter, is shared by both. 

OK 2. The CvEventManager.py and CvSpellInterface.py only have changes from "More Events Modmod", not the "Expanded" portion. The changes are between the comments # More Events Mod starts # and # More Events Mod ends #. 

OK 3. The CIV4EventInfos.xml and CIV4EventTriggerInfos.xml files have the "More Events Modmod" section betweeen the comments <!-- MORE EVENTS MOD STARTS --> and
<!-- MORE EVENTS MOD ENDS -->. The "Expanded" portion is between <!-- MORE EVENTS MOD EXPANDED STARTS --> and <!-- MORE EVENTS MOD EXPANDED ENDS -->.

NO 4. CIV4GameText_Additional_Events.xml is a stand alone file, only having the information needed for the mod itself. It was left out of CIV4GameText_FFH2.xml to make merging easier. You can add the body of this file to CIV4GameText_FFH2.xml if you want. Again, the "More Events Modmod" section is betweeen the comments <!-- MORE EVENTS MOD STARTS --> and <!-- MORE EVENTS MOD ENDS -->. The "Expanded" portion is between <!-- MORE EVENTS MOD EXPANDED STARTS --> and <!-- MORE EVENTS MOD EXPANDED ENDS -->.

NO3OK3 5. CIV4UnitInfos.xml, CIV4UnitClassInfos.xml, CIV4SpellInfos.xml, CIV4PromotionInfos.xml, CIV4BuildingClassInfos.xml, and CIV4BuildingInfos.xml have only changes from "More Events Modmod", not the "Expanded" portion. The changes are betweeen the comments <!-- MORE EVENTS MOD STARTS --> and <!-- MORE EVENTS MOD ENDS -->.

OK 6. CIV4ImprovementInfos.xml is the only uncommented file, because the changes from "More Events Modmod" are within existing tags and can't be commented. There are only two changes, both to the PythonOnMove. 
    A) In IMPROVEMENT_BROKEN_SEPULCHER       <PythonOnMove>onMoveBrokenSepulcher(pCaster, pPlot)</PythonOnMove> 
    B) In IMPROVEMENT_PYRE_OF_THE_SERAPHIC   <PythonOnMove>onMovePyreOfTheSeraphic(pCaster, pPlot)</PythonOnMove>


To use with Events With Images for FFH:

1. You must be using a mod that already uses event images, for example Wildmana or my Events with Images for FFH. This is because there are required dll changes made by those mods to get the images to show. If you are not using such a mod, ignore the rest of this part.

2. Copy the Art folder (containing the EventImages subfolder and the event images dds files) to the Beyond the Sword\Mods\Fall from Heaven 2\Assets folder.

3. In the Optional subfolder - found in the Assets folder wherever you unzipped this mod - copy the file CIV4EventTriggerInfos.xml and overwrite the same file found in Assets/XML/Events. If you are merging, then only copy the events between the <!-- MORE EVENTS MOD and/or <!-- MORE EVENTS MOD EXPANDED into your CIV4EventInfos.xml file.



Credits:

- Black Imperator (the original More Events Modmod creator)
- Ostar (that's me)
- Sephi, Valkrionn, xienwolf (help)

- Kael and the Fall from Heaven 2 Mod Team (for making FFH 2)
- Firaxis (for making Civ IV)


LIST OF EXPANDED EVENTS

Kuriotates Fish; Kuriotates Clam; Kuriotates Crab
	- These three (seperate) events create Fishing Boats improvements (not an actual workboat) for the Kuriotates BUT only a) for settlements with those          unimproved resources, b) if they have no cities on the coast, c) if the Sailing Tech is known. This way the Kuriotates can still use 
        water resources if they have no cities to build workboats. However, each of them only occurs once per game - no building a string of coastal                  settlements just to get free improvements.

Demonic Tower
	- A weakened barbarian demon is trapped on an ancient tower.

Lanun Pirates
	- Only if the Lanun are not a civ, some barbarian "Lanun" privateers appear. Requires a civ with Optics.

Uranium
	- Not a new resource, but modifies an existing mine for good or ill.

Oil
	- Also not a new resource, but modifies a desert flood plain for good or ill.

Winds From Hell
	- Requires Armageddon Counter 20 and windmill improvement.

Sea Serpent
	- A barbarian sea serpent takes over an ocean food resource.

Treant Rage
	- Threatens a lumbermill improvement.

Perfect Storm
	- Threatens a coastal improvement.

Peat			(idea by Jabie)
	- Discover peat (+ 1 hammer) in a swamp.

Bread			(idea by Jabie)
	- Windmill +1 food.

Sutters Mill	(idea by Jabie)
	- Discover silver (not a real resource), workshop +1 commerce.

Frog Legs		(idea by Jabie)
	- Gain 1 Toad resource in a swamp (only for one player a game).

Thread Necromancy	(idea by Izmir Stinger, expanded by me)
	- Citizens re-argue an old issue, for good or ill.

Poisoned Water
	- Espionage vs. your water supply.

Framed
	- A scandal with another civ, for good or ill.

Ancient Tower Lore
	- Discover pre-Age of Ice books.

Stormy Seas
	- Lose 1 naval unit if at sea.

Ralph and Sam
	- Wolves threaten your sheep.

Centaur Tribe
	- Centaurs claim a horse resource as their own, for good or ill.

Monkey See
	- A gorilla threatens your banana resource.

Haunted Castle	(idea by Neomega, expanded by me)
	- Undead threaten your fort or castle, for good or ill.

--------------------
Adjusted for MNAI by lfgr 11/03/2012
Other changes:
	- Fixed a bug in canTriggerPacifistDemonstration (was "player" instead of "pPlayer")