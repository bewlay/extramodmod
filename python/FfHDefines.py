# lfgr 10/2019

from CvPythonExtensions import *

gc = CyGlobalContext()

inst = None
def getInst() :
	global inst
	if inst is None :
		inst = FfHDefinesInstance()
	return inst

class FfHDefinesInstance :
	def __init__( self ) :
		# Planar gates (PlanarGateOverhaul 10/2019 lfgr)
		self.BUILDING_PLANAR_GATE = gc.getInfoTypeForString('BUILDING_PLANAR_GATE')
		self.PLANAR_GATE_CHANCE = gc.getDefineINT('PLANAR_GATE_CHANCE')
		
		self.PLANAR_GATE_UNITS = list( map( gc.getInfoTypeForString, [
			"UNIT_CHAOS_MARAUDER",
			"UNIT_MANTICORE",
			"UNIT_MINOTAUR",
			"UNIT_MOBIUS_WITCH",
			"UNIT_REVELERS",
			"UNIT_SUCCUBUS",
			"UNIT_TAR_DEMON"
		] ) )
		
		self.PLANAR_GATE_HALF_MAX_UNITS = frozenset( map( gc.getInfoTypeForString, [
			"UNIT_MANTICORE",
			"UNIT_MINOTAUR"
		] ) )
