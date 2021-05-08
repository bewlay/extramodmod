from CvPythonExtensions import *

gc = CyGlobalContext()


# LFGR_TODO: This now also contains functionality. Maybe move everything to single modules per civ.

# Required gold for the various stages of Khazad vault. First should be 0
_VAULT_MIN_GOLD = [0, 25, 50, 75, 100, 150, 250]

# Dwarven vault buildings, as strings.
_VAULT_TYPES = [
	'BUILDING_DWARVEN_VAULT_EMPTY',
	'BUILDING_DWARVEN_VAULT_LOW',
	'BUILDING_DWARVEN_VAULT',
	'BUILDING_DWARVEN_VAULT_STOCKED',
	'BUILDING_DWARVEN_VAULT_ABUNDANT',
	'BUILDING_DWARVEN_VAULT_FULL',
	'BUILDING_DWARVEN_VAULT_OVERFLOWING'
]

assert len( _VAULT_MIN_GOLD ) == len( _VAULT_TYPES )
assert _VAULT_MIN_GOLD[0] == 0, "Min gold for empty vault should be 0"

# Planar gates (PlanarGateOverhaul 10/2019 lfgr)
_PLANAR_GATE_UNITS = [
	"UNIT_CHAOS_MARAUDER",
	"UNIT_MANTICORE",
	"UNIT_MINOTAUR",
	"UNIT_MOBIUS_WITCH",
	"UNIT_REVELERS",
	"UNIT_SUCCUBUS",
	"UNIT_TAR_DEMON"
]

_PLANAR_GATE_HALF_MAX_UNITS = [
	"UNIT_MANTICORE",
	"UNIT_MINOTAUR"
]


class FfHDefines :
	def __init__( self ) :
		self._vaultsWithMinGold = None
		self._vaultsWithMinGoldReverse = None

	# LFGR_TODO?
	@property
	def BUILDING_PLANAR_GATE( self ) :
		return gc.getInfoTypeForString( 'BUILDING_PLANAR_GATE' )

	@property
	def PLANAR_GATE_CHANCE( self ) :
		return gc.getDefineINT( 'PLANAR_GATE_CHANCE' )

	@property
	def PLANAR_GATE_UNITS( self ) :
		return list( map( gc.getInfoTypeForString, _PLANAR_GATE_UNITS ) )

	@property
	def PLANAR_GATE_HALF_MAX_UNITS( self ) :
		return frozenset( map( gc.getInfoTypeForString, _PLANAR_GATE_HALF_MAX_UNITS ) )

	def applyMobiusWitchPromotions( self, pUnit ) :
		# type: (CyUnit) -> None
		promotions = ['PROMOTION_AIR1', 'PROMOTION_BODY1', 'PROMOTION_CHAOS1', 'PROMOTION_CREATION1',
					  'PROMOTION_DEATH1', 'PROMOTION_DIMENSIONAL1', 'PROMOTION_EARTH1', 'PROMOTION_ENCHANTMENT1',
					  'PROMOTION_ENTROPY1', 'PROMOTION_FORCE1', 'PROMOTION_FIRE1', 'PROMOTION_ICE1', 'PROMOTION_LAW1',
					  'PROMOTION_LIFE1', 'PROMOTION_METAMAGIC1', 'PROMOTION_MIND1', 'PROMOTION_NATURE1',
					  'PROMOTION_SHADOW1', 'PROMOTION_SPIRIT1', 'PROMOTION_SUN1', 'PROMOTION_WATER1']
		pUnit.setLevel(2)
		pUnit.setExperience(5, -1)
		for i in promotions :
			if CyGame().getSorenRandNum(10, "Mobius Witch promotions") == 1 :
				pUnit.setHasPromotion(gc.getInfoTypeForString(i), True)

	def _loadInfoTypes( self ) :
		if self._vaultsWithMinGold is not None :
			return

		self._vaultsWithMinGold = tuple( (gc.getInfoTypeForString( sType ), iMinGold)
				for iMinGold, sType in zip( _VAULT_MIN_GOLD, _VAULT_TYPES ) )
		self._vaultsWithMinGoldReverse = tuple(reversed(self._vaultsWithMinGold))

	def getKhazadVaultsWithMinGold( self ) :
		# type: () -> Iterator[Tuple[int, int]]
		self._loadInfoTypes()
		return self._vaultsWithMinGold
	
	def getKhazadVault( self, pPlayer ) :
		# type: (CyPlayer) -> int
		self._loadInfoTypes()
		iGoldPerCity = pPlayer.getGold() // pPlayer.getNumCities()
		for eVault, iMinGold in self._vaultsWithMinGoldReverse :
			if iGoldPerCity >= iMinGold :
				return eVault
		assert False, iGoldPerCity # One of the vaults should have iMinGold == 0

	def getNextKhazadVaultWithMinGold( self, pPlayer ) :
		# type: (CyPlayer) -> Optional[Tuple[int, int]]
		self._loadInfoTypes()
		iGoldPerCity = pPlayer.getGold() // pPlayer.getNumCities()
		prevVaultWithMinGold = None # The last vault that was too expensive for us
		for eVault, iMinGold in self._vaultsWithMinGoldReverse :
			if iGoldPerCity >= iMinGold :
				return prevVaultWithMinGold
			prevVaultWithMinGold = eVault, iMinGold
		assert False, iGoldPerCity # One of the vaults should have iMinGold == 0




instance = None
def getInstance() :
	# type: () -> FfHDefines
	global instance
	if instance is None :
		instance = FfHDefines()
	return instance