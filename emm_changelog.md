## 0.6.0-beta8

# Changelog

Includes MNAI 2.9.1u and the next five commits

### AI
* AI does't explore lairs if it has nearby undefended cities

### Gameplay
* Added Nikis-Knight's map (edits by by [to_xp]Gekko)

### UI
* Small text changes


## 0.6.0-beta7

Includes MNAI 2.9u

### Gameplay
* Revised "Ash Cough", "Dead Angel", and "Orphaned goblin" events
* Tweaked oil event

### Fixes
* Dwarves vs. Lizardmen exploration outcome should now work correctly
* Too much death damage from Gela/Pike of Tears event (reported by Tielby@civfanatics)
* Unit auto-disbanding from "War games" event
* Spawned Möbius Witches now properly get spell spheres (report by kvaak@civfanatics)
* Error from Khazad vault tooltip when player has no cities
* Remove reference to removed "Divided Soul" promotion, so that adding to flesh golem works again

### UI
* Disabled non-functional "Show Khazad Vault Text" BUG option


## 0.6.0-beta6

Includes MNAI 2.9-beta3u

### Fixes
* Python exception in Fertility spell help (reported by kvaak@civfanatics)
* Mod should now really work without having keeping the FfH2 or MNAI mod folders.


## 0.6.0-beta5

Includes MNAI 2.9-beta2u.

### Fixes
* Mod now works without installing More Naval AI alongside


## 0.6.0-beta4u

Includes MNAI versions 2.8.1u and 2.9-beta1u.

### AI
* Adjusted power values for the units introduced in BarbsPlus

### Fixes
* No more unlimited Treants and Kraken (reported by westamastaflash@civfanatics)
* "Lead any civ" works for leader selection again

### Gameplay
* Tweaked Planar Gate unit spawning and building (report by westamastaflash@civfanatics)
	* Spawning chance is the same on normal, but scales by Gamespeed. The limit on units is now much lower.
* Adapted wilderness tiers: Stronger animals now generally spawn slightly closer to player
* New, very strong "gargantuan" animals spawn in high wilderness.
* Chokepoints are now considered in wilderness calculation. This way remote valleys e.g. from the Erebus mapscript have higher wilderness
* Giant lizard now passes the diseased promotion to units in combat

### UI
* Translated some of the EventsEnhanced BUG options
* Disabled selection of classifier game options

### Code
* More documentation, fixed typos
* Some tweaks to CvUniversalPrereqs
