# New XML tags

This document contains an overview of new and changed XML tags in Extramodmod. It does not contain tags that MNAI or FfH2 changed or added; for that, see `tags.md`. It is still work in progress. For BtS tags, see e.g. civfantics' [modiki](http://modiki.civfanatics.com/index.php?title=Civ4_XML_Reference).

### Gameinfo/CIV4SpawnInfos.xml

New file. Contains rules to spawn barbarian units in three contexts: (a) randomly every turn, everywhere; (b) randomly every turn on lairs; (c) as a result of a lair exploration. These three contexts are referred by (a)/(b)/(c) below. By default, a spawn is considered for (a), but not for (c). A spawn is considered for (b) if it is referenced in `Terrain/CIV4ImprovementInfos.xml` accordingly.

**Spawn choice and weight**

TODO

** Movement restriction **

TODO

**New tags**

Tag(s) | Description
--- | ---
`<Type>SPAWN_XYZ</Type>` | **Required.** TODO
`<Description>DESC</Description>` | TODO
`<iBaseWeight>Z</iBaseWeight>` | **Required.** Weight of this spawn is Z plus modifiers (see below). May be negative.
`<TerrainFlavourType>TERRAIN_FLAVOUR_SPAWN_XYZ</TerrainFlavourType>` | Adds the tile value according to `TERRAIN_FLAVOUR_SPAWN_XYZ` to the weight. No effect if included with `<bIgnoreTerrain>1</bIgnoreTerrain>`.
`<iValidTerrainWeight>N</iValidTerrainWeight>` | If the weight from tile value is at least one, add N to the weight. Default: `0`
`<SpawnPrereqType>SPAWN_PREREQ_XYZ</SpawnPrereqType>` <br/> `<iMinSpawnTier>M</iMinSpawnTier>` <br/> `<iMaxSpawnTier>N</iMaxSpawnTier>` | | **All three Required.** Can only spawn if some tier between M and N (both inclusive) is valid on the tile according to `SPAWN_PREREQ_XYZ`. See also: GameInfo/CIV4SpawnPrereqInfos.xml
`<bNoWildernessIgnoreSpawnPrereq>1</bNoWildernessIgnoreSpawnPrereq>` | If the "No Wilderness" option is enabled, this ignores spawn tier checks (see `<SpawnPrereqType>`)
`<iPrereqGlobalCounter>N</iPrereqGlobalCounter>` | Can only spawn if the Armaggeddon counter is at least N.
`<bNeverSpawn>1</bNeverSpawn>` | Disables Spawning in context (a)
`<bExplorationResult>1</bExplorationResult>` | Enables spawning in context (c)
`<bExplorationNoPush>1</bExplorationNoPush>` | When spawned from (c), spawn next to lair instead of pushing units out of lair.
`<bNoDefender>1</bNoDefender>` | Spawned units don't receive UNITAI_LAIRGUARDIAN to guard lairs.
`<bAnimal>1</bAnimal>` | Cannot spawn on tiles owned a non-barbarian player, unless included with `<bIgnoreTerrain>1</bIgnoreTerrain>`.
`<bWater>1</bWater>` | Indicates this can only spawn on water tiles; otherwise, it can only spawn on land tiles. Non-animal water spawns start with UNITAI_ATTACK_SEA; non-animal land spawns start with UNITAI_ATTACK. No effect if included with `<bIgnoreTerrain>1</bIgnoreTerrain>`.
`<bNoRace>1</bNoRace>` | Removes default race (e.g. orc for barbarians)
`<bNoMinWilderness>1</bNoMinWilderness>` | No movement restriction based on wilderness.
`<UnitArtStyleType>TODO</UnitArtStyleType>` | TODO
`<UnitAIType>TODO</UnitAIType>` | TODO
`<SpawnUnits>TODO</SpawnUnits>` | **Required.** TODO
`<iMinRandomPromotions>TODO</iMinRandomPromotions>` | TODO
`<iMaxRandomPromotions>TODO</iMaxRandomPromotions>` | TODO
`<UnitPromotions>TODO</UnitPromotions>` | TODO
`<iMinIncludedSpawns>TODO</iMinIncludedSpawns>` | TODO
`<iMaxIncludedSpawns>TODO</iMaxIncludedSpawns>` | TODO
`<IncludedSpawns>TODO</IncludedSpawns>` | TODO
`<PrereqTechs>TODO</PrereqTechs>` | TODO
`<ObsoleteTechs>TODO</ObsoleteTechs>` | TODO
`<CreateLair>TODO</CreateLair>` | TODO
`<iCreateLairAge>TODO</iCreateLairAge>` | TODO
`<iCreateLairLevel>TODO</iCreateLairLevel>` | TODO
