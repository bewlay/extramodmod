## EventsEnhancedOptionsTab
##
## Tab for the Events Enhanced Mod
##
## 05/2013
##
## Author: lfgr

import BugOptionsTab

class EventsEnhancedOptionsTab(BugOptionsTab.BugOptionsTab):
	"Events Enhanced Options Screen Tab"
	
	def __init__(self, screen):
		BugOptionsTab.BugOptionsTab.__init__(self, "EE", "Events Enhanced")

	def create(self, screen):
		tab = self.createTab(screen)
		panel = self.createMainPanel(screen)
		column = self.addOneColumnLayout(screen, panel)
		
		self.addCheckbox(screen, column, "EventsEnhanced__HideUnavailableOptions")
		self.addCheckbox(screen, column, "EventsEnhanced__WUPopupHuman")
		self.addCheckbox(screen, column, "EventsEnhanced__WUPopupAI")
		self.addCheckbox(screen, column, "EventsEnhanced__GPPopupHuman")
		self.addCheckbox(screen, column, "EventsEnhanced__GPPopupAI")
