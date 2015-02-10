from CvPythonExtensions import *

gc = CyGlobalContext()

# Wilderness defines

# Base sell value for animals at level 1
liAnimalValues = [-1] * gc.getNumUnitInfos()
liAnimalValues[gc.getInfoTypeForString( "UNIT_BABY_SPIDER" )] = 5
liAnimalValues[gc.getInfoTypeForString( "UNIT_BEAR" )] = 20
liAnimalValues[gc.getInfoTypeForString( "UNIT_CAVE_BEAR" )] = 30
liAnimalValues[gc.getInfoTypeForString( "UNIT_ELEPHANT" )] = 40
liAnimalValues[gc.getInfoTypeForString( "UNIT_GIANT_SPIDER" )] = 15
liAnimalValues[gc.getInfoTypeForString( "UNIT_GORILLA" )] = 20
liAnimalValues[gc.getInfoTypeForString( "UNIT_GRIFFON" )] = 35
liAnimalValues[gc.getInfoTypeForString( "UNIT_LION" )] = 15
liAnimalValues[gc.getInfoTypeForString( "UNIT_LION_PRIDE" )] = 20
liAnimalValues[gc.getInfoTypeForString( "UNIT_PANTHER" )] = 30
liAnimalValues[gc.getInfoTypeForString( "UNIT_POLAR_BEAR" )] = 20
liAnimalValues[gc.getInfoTypeForString( "UNIT_SCORPION" )] = 15
liAnimalValues[gc.getInfoTypeForString( "UNIT_TIGER" )] = 25
liAnimalValues[gc.getInfoTypeForString( "UNIT_WOLF" )] = 10
liAnimalValues[gc.getInfoTypeForString( "UNIT_WOLF_PACK" )] = 15
liAnimalValues[gc.getInfoTypeForString( "UNIT_SEA_SERPENT" )] = 50
liAnimalValues[gc.getInfoTypeForString( "UNIT_GIANT_TORTOISE" )] = 60
