// CvDeal.cpp

#include "CvGameCoreDLL.h"
#include "CvGlobals.h"
#include "CvGameAI.h"
#include "CvTeamAI.h"
#include "CvPlayerAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvGameCoreUtils.h"
#include "CvGameTextMgr.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvEventReporter.h"

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/02/09                                jdog5000      */
/*                                                                                              */
/* AI logging                                                                                   */
/************************************************************************************************/
#include "BetterBTSAI.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

// Public Functions...

CvDeal::CvDeal()
{
	reset();
}


CvDeal::~CvDeal()
{
	uninit();
}


void CvDeal::init(int iID, PlayerTypes eFirstPlayer, PlayerTypes eSecondPlayer)
{
	//--------------------------------
	// Init saved data
	reset(iID, eFirstPlayer, eSecondPlayer);

	//--------------------------------
	// Init non-saved data

	//--------------------------------
	// Init other game data
	setInitialGameTurn(GC.getGameINLINE().getGameTurn());
}


void CvDeal::uninit()
{
	m_firstTrades.clear();
	m_secondTrades.clear();
}


// FUNCTION: reset()
// Initializes data members that are serialized.
void CvDeal::reset(int iID, PlayerTypes eFirstPlayer, PlayerTypes eSecondPlayer)
{
	//--------------------------------
	// Uninit class
	uninit();

	m_iID = iID;
	m_iInitialGameTurn = 0;

	m_eFirstPlayer = eFirstPlayer;
	m_eSecondPlayer = eSecondPlayer;
}


void CvDeal::kill(bool bKillTeam)
{
	if ((getLengthFirstTrades() > 0) || (getLengthSecondTrades() > 0))
	{
		CvWString szString;
		CvWStringBuffer szDealString;
		CvWString szCancelString = gDLL->getText("TXT_KEY_POPUP_DEAL_CANCEL");

		if (GET_TEAM(GET_PLAYER(getFirstPlayer()).getTeam()).isHasMet(GET_PLAYER(getSecondPlayer()).getTeam()))
		{
			szDealString.clear();
			GAMETEXT.getDealString(szDealString, *this, getFirstPlayer());
			szString.Format(L"%s: %s", szCancelString.GetCString(), szDealString.getCString());
			gDLL->getInterfaceIFace()->addMessage((PlayerTypes)getFirstPlayer(), true, GC.getEVENT_MESSAGE_TIME(), szString, "AS2D_DEAL_CANCELLED");
		}

		if (GET_TEAM(GET_PLAYER(getSecondPlayer()).getTeam()).isHasMet(GET_PLAYER(getFirstPlayer()).getTeam()))
		{
			szDealString.clear();
			GAMETEXT.getDealString(szDealString, *this, getSecondPlayer());
			szString.Format(L"%s: %s", szCancelString.GetCString(), szDealString.getCString());
			gDLL->getInterfaceIFace()->addMessage((PlayerTypes)getSecondPlayer(), true, GC.getEVENT_MESSAGE_TIME(), szString, "AS2D_DEAL_CANCELLED");
		}
	}

	CLLNode<TradeData>* pNode;

	for (pNode = headFirstTradesNode(); (pNode != NULL); pNode = nextFirstTradesNode(pNode))
	{
		endTrade(pNode->m_data, getFirstPlayer(), getSecondPlayer(), bKillTeam);
	}

	for (pNode = headSecondTradesNode(); (pNode != NULL); pNode = nextSecondTradesNode(pNode))
	{
		endTrade(pNode->m_data, getSecondPlayer(), getFirstPlayer(), bKillTeam);
	}

	GC.getGameINLINE().deleteDeal(getID());
}


void CvDeal::addTrades(CLinkList<TradeData>* pFirstList, CLinkList<TradeData>* pSecondList, bool bCheckAllowed)
{
	CLLNode<TradeData>* pNode;
	bool bAlliance;
	bool bSave;
	int iValue;

	if( gTeamLogLevel >= 2 )
	{
		logBBAI("  BEGIN TRADE DEAL between player %d (%S) and player %d (%S)", getFirstPlayer(), GET_PLAYER(getFirstPlayer()).getCivilizationDescription(0), getSecondPlayer(), GET_PLAYER(getSecondPlayer()).getCivilizationDescription(0) );
	}

	if (isVassalTrade(pFirstList) && isVassalTrade(pSecondList))
	{
		return;
	}

	if (pFirstList != NULL)
	{
		for (pNode = pFirstList->head(); pNode; pNode = pFirstList->next(pNode))
		{
			if (bCheckAllowed)
			{
				if (!(GET_PLAYER(getFirstPlayer()).canTradeItem(getSecondPlayer(), pNode->m_data)))
				{
					return;
				}
			}
		}
	}

	if (pSecondList != NULL)
	{
		for (pNode = pSecondList->head(); pNode; pNode = pSecondList->next(pNode))
		{
			if (bCheckAllowed && !(GET_PLAYER(getSecondPlayer()).canTradeItem(getFirstPlayer(), pNode->m_data)))
			{
				return;
			}
		}
	}

	TeamTypes eFirstTeam = GET_PLAYER(getFirstPlayer()).getTeam();
	TeamTypes eSecondTeam = GET_PLAYER(getSecondPlayer()).getTeam();

	if (atWar(eFirstTeam, eSecondTeam))
	{
		// free vassals of capitulating team before peace is signed
		if (isVassalTrade(pSecondList))
		{
			for (int iI = 0; iI < MAX_TEAMS; iI++)
			{
				TeamTypes eLoopTeam = (TeamTypes) iI;
				CvTeam& kLoopTeam = GET_TEAM(eLoopTeam);
				if ((eLoopTeam != eFirstTeam) && (eLoopTeam != eSecondTeam))
				{
					if (kLoopTeam.isAlive() && kLoopTeam.isVassal(eSecondTeam))
					{
						GET_TEAM(eSecondTeam).freeVassal(eLoopTeam);
						int iSecondSuccess = GET_TEAM(eFirstTeam).AI_getWarSuccess(eSecondTeam) + GC.getWAR_SUCCESS_CITY_CAPTURING() * GET_TEAM(eSecondTeam).getNumCities();
						GET_TEAM(eFirstTeam).AI_setWarSuccess(eLoopTeam, std::max(iSecondSuccess, GET_TEAM(eFirstTeam).AI_getWarSuccess(eLoopTeam)));
					}
				}
			}
		}

		if (isVassalTrade(pFirstList))
		{
			for (int iI = 0; iI < MAX_TEAMS; iI++)
			{
				TeamTypes eLoopTeam = (TeamTypes) iI;
				CvTeam& kLoopTeam = GET_TEAM(eLoopTeam);
				if ((eLoopTeam != eFirstTeam) && (eLoopTeam != eSecondTeam))
				{
					if (kLoopTeam.isAlive() && kLoopTeam.isVassal(eFirstTeam))
					{
						GET_TEAM(eFirstTeam).freeVassal(eLoopTeam);
						int iFirstSuccess = GET_TEAM(eSecondTeam).AI_getWarSuccess(eFirstTeam) + GC.getWAR_SUCCESS_CITY_CAPTURING() * GET_TEAM(eFirstTeam).getNumCities();
						GET_TEAM(eSecondTeam).AI_setWarSuccess(eLoopTeam, std::max(iFirstSuccess, GET_TEAM(eSecondTeam).AI_getWarSuccess(eLoopTeam)));
					}
				}
			}
		}

		GET_TEAM(eFirstTeam).makePeace(eSecondTeam, !isVassalTrade(pFirstList) && !isVassalTrade(pSecondList));
	}
	else
	{
		if (!isPeaceDealBetweenOthers(pFirstList, pSecondList))
		{
			if ((pSecondList != NULL) && (pSecondList->getLength() > 0))
			{
				iValue = GET_PLAYER(getFirstPlayer()).AI_dealVal(getSecondPlayer(), pSecondList, true);

				if ((pFirstList != NULL) && (pFirstList->getLength() > 0))
				{
					GET_PLAYER(getFirstPlayer()).AI_changePeacetimeTradeValue(getSecondPlayer(), iValue);
				}
				else
				{
					GET_PLAYER(getFirstPlayer()).AI_changePeacetimeGrantValue(getSecondPlayer(), iValue);
				}
			}
			if ((pFirstList != NULL) && (pFirstList->getLength() > 0))
			{
				iValue = GET_PLAYER(getSecondPlayer()).AI_dealVal(getFirstPlayer(), pFirstList, true);

				if ((pSecondList != NULL) && (pSecondList->getLength() > 0))
				{
					GET_PLAYER(getSecondPlayer()).AI_changePeacetimeTradeValue(getFirstPlayer(), iValue);
				}
				else
				{
					GET_PLAYER(getSecondPlayer()).AI_changePeacetimeGrantValue(getFirstPlayer(), iValue);
				}
			}
		}
	}

	if (pFirstList != NULL)
	{
		for (pNode = pFirstList->head(); pNode; pNode = pFirstList->next(pNode))
		{
			bSave = startTrade(pNode->m_data, getFirstPlayer(), getSecondPlayer());

			if (bSave)
			{
				insertAtEndFirstTrades(pNode->m_data);
			}
		}
	}

	if (pSecondList != NULL)
	{
		for (pNode = pSecondList->head(); pNode; pNode = pSecondList->next(pNode))
		{
			bSave = startTrade(pNode->m_data, getSecondPlayer(), getFirstPlayer());

			if (bSave)
			{
				insertAtEndSecondTrades(pNode->m_data);
			}
		}
	}

	bAlliance = false;

	if (pFirstList != NULL)
	{
		for (pNode = pFirstList->head(); pNode; pNode = pFirstList->next(pNode))
		{
			if (pNode->m_data.m_eItemType == TRADE_PERMANENT_ALLIANCE)
			{
				bAlliance = true;
			}
		}
	}

	if (pSecondList != NULL)
	{
		for (pNode = pSecondList->head(); pNode; pNode = pSecondList->next(pNode))
		{
			if (pNode->m_data.m_eItemType == TRADE_PERMANENT_ALLIANCE)
			{
				bAlliance = true;
			}
		}
	}

	if (bAlliance)
	{
		if (eFirstTeam < eSecondTeam)
		{
			GET_TEAM(eFirstTeam).addTeam(eSecondTeam);
		}
		else if (eSecondTeam < eFirstTeam)
		{
			GET_TEAM(eSecondTeam).addTeam(eFirstTeam);
		}
	}
}


void CvDeal::doTurn()
{
	int iValue;

	if (!isPeaceDeal())
	{
		if (getLengthSecondTrades() > 0)
		{
			iValue = (GET_PLAYER(getFirstPlayer()).AI_dealVal(getSecondPlayer(), getSecondTrades()) / GC.getDefineINT("PEACE_TREATY_LENGTH"));

			if (getLengthFirstTrades() > 0)
			{
				GET_PLAYER(getFirstPlayer()).AI_changePeacetimeTradeValue(getSecondPlayer(), iValue);
			}
			else
			{
				GET_PLAYER(getFirstPlayer()).AI_changePeacetimeGrantValue(getSecondPlayer(), iValue);
			}
		}

		if (getLengthFirstTrades() > 0)
		{
			iValue = (GET_PLAYER(getSecondPlayer()).AI_dealVal(getFirstPlayer(), getFirstTrades()) / GC.getDefineINT("PEACE_TREATY_LENGTH"));

			if (getLengthSecondTrades() > 0)
			{
				GET_PLAYER(getSecondPlayer()).AI_changePeacetimeTradeValue(getFirstPlayer(), iValue);
			}
			else
			{
				GET_PLAYER(getSecondPlayer()).AI_changePeacetimeGrantValue(getFirstPlayer(), iValue);
			}
		}
	}
}


// XXX probably should have some sort of message for the user or something...
void CvDeal::verify()
{
	bool bCancelDeal = false;

	CvPlayer& kFirstPlayer = GET_PLAYER(getFirstPlayer());
	CvPlayer& kSecondPlayer = GET_PLAYER(getSecondPlayer());

	for (CLLNode<TradeData>* pNode = headFirstTradesNode(); (pNode != NULL); pNode = nextFirstTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
		{
			// XXX embargoes?
			if ((kFirstPlayer.getNumTradeableBonuses((BonusTypes)(pNode->m_data.m_iData)) < 0) ||
				  !(kFirstPlayer.canTradeNetworkWith(getSecondPlayer())) ||
				  GET_TEAM(kFirstPlayer.getTeam()).isBonusObsolete((BonusTypes) pNode->m_data.m_iData) ||
				  GET_TEAM(kSecondPlayer.getTeam()).isBonusObsolete((BonusTypes) pNode->m_data.m_iData))
			{
				bCancelDeal = true;
			}
		}
	}

	for (CLLNode<TradeData>* pNode = headSecondTradesNode(); (pNode != NULL); pNode = nextSecondTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
		{
			// XXX embargoes?
			if ((GET_PLAYER(getSecondPlayer()).getNumTradeableBonuses((BonusTypes)(pNode->m_data.m_iData)) < 0) ||
				  !(GET_PLAYER(getSecondPlayer()).canTradeNetworkWith(getFirstPlayer())) ||
				  GET_TEAM(kFirstPlayer.getTeam()).isBonusObsolete((BonusTypes) pNode->m_data.m_iData) ||
				  GET_TEAM(kSecondPlayer.getTeam()).isBonusObsolete((BonusTypes) pNode->m_data.m_iData))
			{
				bCancelDeal = true;
			}
		}
	}

	if (isCancelable(NO_PLAYER))
	{
		if (isPeaceDeal())
		{
			bCancelDeal = true;
		}
	}
/************************************************************************************************/
/* Advanced Diplomacy                   START                                                   */
/************************************************************************************************/
	// edead: start auto-cancel of POW exchange agreement after X turns
	bool bPOW = false;
	for (CLLNode<TradeData>* pNode = headFirstTradesNode(); (pNode != NULL); pNode = nextFirstTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == TRADE_POW)
		{
			bPOW = true;
			break;
		}
	}

	for (CLLNode<TradeData>* pNode = headSecondTradesNode(); (pNode != NULL); pNode = nextSecondTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == TRADE_POW)
		{
			bPOW = true;
			break;
		}
	}

	if (bPOW)
	{
		if (getInitialGameTurn() + GC.getDefineINT("POW_EXCHANGE_LENGTH") <= GC.getGameINLINE().getGameTurn())
		{
			kill(true);
		}
	}
	// edead: end
/************************************************************************************************/
/* Advanced Diplomacy                        END                                                */
/************************************************************************************************/
	if (bCancelDeal)
	{
		kill();
	}
}


bool CvDeal::isPeaceDeal() const
{
	CLLNode<TradeData>* pNode;

	for (pNode = headFirstTradesNode(); (pNode != NULL); pNode = nextFirstTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == getPeaceItem())
		{
			return true;
		}
	}

	for (pNode = headSecondTradesNode(); (pNode != NULL); pNode = nextSecondTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == getPeaceItem())
		{
			return true;
		}
	}

	return false;
}

bool CvDeal::isVassalDeal() const
{
	return (isVassalTrade(&m_firstTrades) || isVassalTrade(&m_secondTrades));
}

bool CvDeal::isVassalTrade(const CLinkList<TradeData>* pList)
{
	if (pList)
	{
		for (CLLNode<TradeData>* pNode = pList->head(); pNode != NULL; pNode = pList->next(pNode))
		{
			if (isVassal(pNode->m_data.m_eItemType))
			{
				return true;
			}
		}
	}

	return false;
}


bool CvDeal::isUncancelableVassalDeal(PlayerTypes eByPlayer, CvWString* pszReason) const
{
	CLLNode<TradeData>* pNode;
	CvWStringBuffer szBuffer;

	for (pNode = headFirstTradesNode(); (pNode != NULL); pNode = nextFirstTradesNode(pNode))
	{
		if (isVassal(pNode->m_data.m_eItemType))
		{
			if (eByPlayer == getSecondPlayer())
			{
				if (pszReason)
				{
					*pszReason += gDLL->getText("TXT_KEY_MISC_DEAL_NO_CANCEL_EVER");
				}

				return true;
			}
		}

		if (pNode->m_data.m_eItemType == TRADE_SURRENDER)
		{
			CvTeam& kVassal = GET_TEAM(GET_PLAYER(getFirstPlayer()).getTeam());
			TeamTypes eMaster = GET_PLAYER(getSecondPlayer()).getTeam();

			if (!kVassal.canVassalRevolt(eMaster))
			{
				if (pszReason)
				{
					szBuffer.clear();
					GAMETEXT.setVassalRevoltHelp(szBuffer, eMaster, GET_PLAYER(getFirstPlayer()).getTeam());
					*pszReason = szBuffer.getCString();
				}

				return true;
			}
		}
	}

	for (pNode = headSecondTradesNode(); (pNode != NULL); pNode = nextSecondTradesNode(pNode))
	{
		if (isVassal(pNode->m_data.m_eItemType))
		{
			if (eByPlayer == getFirstPlayer())
			{
				if (pszReason)
				{
					*pszReason += gDLL->getText("TXT_KEY_MISC_DEAL_NO_CANCEL_EVER");
				}

				return true;
			}
		}

		if (pNode->m_data.m_eItemType == TRADE_SURRENDER)
		{
			CvTeam& kVassal = GET_TEAM(GET_PLAYER(getSecondPlayer()).getTeam());
			TeamTypes eMaster = GET_PLAYER(getFirstPlayer()).getTeam();

			if (!kVassal.canVassalRevolt(eMaster))
			{
				if (pszReason)
				{
					if (pszReason)
					{
						szBuffer.clear();
						GAMETEXT.setVassalRevoltHelp(szBuffer, eMaster, GET_PLAYER(getFirstPlayer()).getTeam());
						*pszReason = szBuffer.getCString();
					}
				}

				return true;
			}
		}
	}

	return false;
}

bool CvDeal::isVassalTributeDeal(const CLinkList<TradeData>* pList)
{
	for (CLLNode<TradeData>* pNode = pList->head(); pNode != NULL; pNode = pList->next(pNode))
	{
		if (pNode->m_data.m_eItemType != TRADE_RESOURCES)
		{
			return false;
		}
	}

	return true;
}

bool CvDeal::isPeaceDealBetweenOthers(CLinkList<TradeData>* pFirstList, CLinkList<TradeData>* pSecondList) const
{
	CLLNode<TradeData>* pNode;

	if (pFirstList != NULL)
	{
		for (pNode = pFirstList->head(); pNode; pNode = pFirstList->next(pNode))
		{
			if (pNode->m_data.m_eItemType == TRADE_PEACE)
			{
				return true;
			}
		}
	}

	if (pSecondList != NULL)
	{
		for (pNode = pSecondList->head(); pNode; pNode = pSecondList->next(pNode))
		{
			if (pNode->m_data.m_eItemType == TRADE_PEACE)
			{
				return true;
			}
		}
	}

	return false;
}


int CvDeal::getID() const
{
	return m_iID;
}


void CvDeal::setID(int iID)
{
	m_iID = iID;
}


int CvDeal::getInitialGameTurn() const
{
	return m_iInitialGameTurn;
}


void CvDeal::setInitialGameTurn(int iNewValue)
{
	m_iInitialGameTurn = iNewValue;
}


PlayerTypes CvDeal::getFirstPlayer() const
{
	return m_eFirstPlayer;
}


PlayerTypes CvDeal::getSecondPlayer() const
{
	return m_eSecondPlayer;
}


void CvDeal::clearFirstTrades()
{
	m_firstTrades.clear();
}


void CvDeal::insertAtEndFirstTrades(TradeData trade)
{
	m_firstTrades.insertAtEnd(trade);
}


CLLNode<TradeData>* CvDeal::nextFirstTradesNode(CLLNode<TradeData>* pNode) const
{
	return m_firstTrades.next(pNode);
}

/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/

void CvDeal::removeFirstTradeNode(CLLNode<TradeData>* pNode)
{
	m_firstTrades.deleteNode(pNode);
}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
int CvDeal::getLengthFirstTrades() const
{
	return m_firstTrades.getLength();
}


CLLNode<TradeData>* CvDeal::headFirstTradesNode() const
{
	return m_firstTrades.head();
}


const CLinkList<TradeData>* CvDeal::getFirstTrades() const
{
	return &(m_firstTrades);
}


void CvDeal::clearSecondTrades()
{
	m_secondTrades.clear();
}


void CvDeal::insertAtEndSecondTrades(TradeData trade)
{
	m_secondTrades.insertAtEnd(trade);
}


CLLNode<TradeData>* CvDeal::nextSecondTradesNode(CLLNode<TradeData>* pNode) const
{
	return m_secondTrades.next(pNode);
}

/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/

void CvDeal::removeSecondTradeNode(CLLNode<TradeData>* pNode)
{
	m_secondTrades.deleteNode(pNode);
}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
int CvDeal::getLengthSecondTrades() const
{
	return m_secondTrades.getLength();
}


CLLNode<TradeData>* CvDeal::headSecondTradesNode() const
{
	return m_secondTrades.head();
}


const CLinkList<TradeData>* CvDeal::getSecondTrades() const
{
	return &(m_secondTrades);
}


void CvDeal::write(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iID);
	pStream->Write(m_iInitialGameTurn);

	pStream->Write(m_eFirstPlayer);
	pStream->Write(m_eSecondPlayer);

	m_firstTrades.Write(pStream);
	m_secondTrades.Write(pStream);
}

void CvDeal::read(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iID);
	pStream->Read(&m_iInitialGameTurn);

	pStream->Read((int*)&m_eFirstPlayer);
	pStream->Read((int*)&m_eSecondPlayer);

	m_firstTrades.Read(pStream);
	m_secondTrades.Read(pStream);
}

// Protected Functions...

// Returns true if the trade should be saved...
bool CvDeal::startTrade(TradeData trade, PlayerTypes eFromPlayer, PlayerTypes eToPlayer)
{
	CivicTypes* paeNewCivics;
	CvCity* pCity;
/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	CvUnit* pUnit;
	CvCity* pNewHQCity;
	CvWString szBuffer;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	CvPlot* pLoopPlot;
	bool bSave;
	int iI;

	bSave = false;

	switch (trade.m_eItemType)
	{
	case TRADE_TECHNOLOGIES:
		GET_TEAM(GET_PLAYER(eToPlayer).getTeam()).setHasTech(((TechTypes)trade.m_iData), true, eToPlayer, true, true);
		GET_TEAM(GET_PLAYER(eToPlayer).getTeam()).setNoTradeTech(((TechTypes)trade.m_iData), true);

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades tech %S due to TRADE_TECHNOLOGIES with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), GC.getTechInfo((TechTypes)trade.m_iData).getDescription(), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eToPlayer).getTeam())
				{
					GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(eFromPlayer, MEMORY_TRADED_TECH_TO_US, 1);
				}
				else
				{
					if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isHasMet(GET_PLAYER(eToPlayer).getTeam()))
					{
						GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(eToPlayer, MEMORY_RECEIVED_TECH_FROM_ANY, 1);
					}
				}
			}
		}
		break;

	case TRADE_RESOURCES:
		GET_PLAYER(eFromPlayer).changeBonusExport(((BonusTypes)trade.m_iData), 1);
		GET_PLAYER(eToPlayer).changeBonusImport(((BonusTypes)trade.m_iData), 1);

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades bonus type %S (value: %d) due to TRADE_RESOURCES with %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), GC.getBonusInfo((BonusTypes)trade.m_iData).getDescription(), GET_PLAYER(eFromPlayer).AI_bonusVal((BonusTypes)trade.m_iData), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		bSave = true;
		break;

	case TRADE_CITIES:
		pCity = GET_PLAYER(eFromPlayer).getCity(trade.m_iData);
		if (pCity != NULL)
		{
			if( gTeamLogLevel >= 2 )
			{
				logBBAI("      Player %d (%S) gives a city due to TRADE_CITIES with %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
			}
			pCity->doTask(TASK_GIFT, eToPlayer);
		}
		break;
/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	case TRADE_WORKER:
	case TRADE_MILITARY_UNIT:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
	        pUnit = GET_PLAYER(eFromPlayer).getUnit(trade.m_iData);
	        if (pUnit != NULL)
	        {
				if( gTeamLogLevel >= 2 )
				{
					logBBAI("      Player %d (%S) gives a %S (ID %d) due to TRADE_MILITARY_UNIT with %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), pUnit->getName().GetCString(), pUnit->getID(), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
				}
	            pUnit->tradeUnit(eToPlayer);
	        }
		}
        break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	case TRADE_GOLD:
		GET_PLAYER(eFromPlayer).changeGold(-(trade.m_iData));
		GET_PLAYER(eToPlayer).changeGold(trade.m_iData);
		GET_PLAYER(eFromPlayer).AI_changeGoldTradedTo(eToPlayer, trade.m_iData);

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades gold %d due to TRADE_GOLD with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), trade.m_iData, eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		// Python Event
		CvEventReporter::getInstance().playerGoldTrade(eFromPlayer, eToPlayer, trade.m_iData);

		break;

	case TRADE_GOLD_PER_TURN:
		GET_PLAYER(eFromPlayer).changeGoldPerTurnByPlayer(eToPlayer, -(trade.m_iData));
		GET_PLAYER(eToPlayer).changeGoldPerTurnByPlayer(eFromPlayer, trade.m_iData);

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades gold per turn %d due to TRADE_GOLD_PER_TURN with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), trade.m_iData, eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		bSave = true;
		break;

	case TRADE_MAPS:
		for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
		{
			pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

			if (pLoopPlot->isRevealed(GET_PLAYER(eFromPlayer).getTeam(), false))
			{
				pLoopPlot->setRevealed(GET_PLAYER(eToPlayer).getTeam(), true, false, GET_PLAYER(eFromPlayer).getTeam(), false);
			}
		}

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eToPlayer).getTeam())
				{
					GET_PLAYER((PlayerTypes)iI).updatePlotGroups();
				}
			}
		}

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades maps due to TRADE_MAPS with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}
		break;

	case TRADE_SURRENDER:
	case TRADE_VASSAL:
		if (trade.m_iData == 0)
		{
			startTeamTrade(trade.m_eItemType, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), false);
			GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setVassal(GET_PLAYER(eToPlayer).getTeam(), true, TRADE_SURRENDER == trade.m_eItemType);

			if( gTeamLogLevel >= 2 )
			{
				if( TRADE_SURRENDER == trade.m_eItemType )
				{
					logBBAI("      Player %d (%S) trades themselves as vassal due to TRADE_SURRENDER with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
				}
				else
				{
					logBBAI("      Player %d (%S) trades themselves as vassal due to TRADE_VASSAL with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
				}
			}
		}
		else
		{
			bSave = true;
		}


		break;

	case TRADE_PEACE:
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Team %d (%S) makes peace with team %d due to TRADE_PEACE with %d (%S)", GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eFromPlayer).getCivilizationDescription(0), trade.m_iData, eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).makePeace((TeamTypes)trade.m_iData);
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (GET_TEAM(GET_PLAYER((PlayerTypes)iI).getTeam()).isHasMet(GET_PLAYER(eFromPlayer).getTeam()))
					{
						GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(eFromPlayer, MEMORY_MADE_PEACE, 1);
					}
				}
			}
		}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
		break;

	case TRADE_WAR:
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Team %d (%S) declares war on team %d due to TRADE_WAR with %d (%S)", GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eFromPlayer).getCivilizationDescription(0), trade.m_iData, eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).declareWar(((TeamTypes)trade.m_iData), true, NO_WARPLAN);
/************************************************************************************************/
/* Afforess	                  Start		 		                                                */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
		GET_TEAM(GET_PLAYER(eToPlayer).getTeam()).setHiredWarAlly(GET_PLAYER(eFromPlayer).getTeam(), true);
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == ((TeamTypes)trade.m_iData))
				{
/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
					szBuffer = gDLL->getText("TXT_KEY_MISC_HIRED_WAR_ALLY", GET_PLAYER(eToPlayer).getCivilizationAdjectiveKey(), GET_PLAYER(eFromPlayer).getCivilizationAdjectiveKey());
					gDLL->getInterfaceIFace()->addMessage(GET_PLAYER((PlayerTypes)iI).getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BUILD_BARRACKS", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_RED"));
					GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(eToPlayer, MEMORY_HIRED_WAR_ALLY, 1);
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/						
				}
			}
		}
		break;

/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	//byFra
	case TRADE_WAR_PREPARE:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).AI_setWarPlan((TeamTypes)trade.m_iData, WARPLAN_PREPARING_LIMITED);
		}
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/

	case TRADE_EMBARGO:
		GET_PLAYER(eFromPlayer).stopTradingWithTeam((TeamTypes)trade.m_iData);

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == ((TeamTypes)trade.m_iData))
				{
					GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(eToPlayer, MEMORY_HIRED_TRADE_EMBARGO, 1);
				}
			}
		}

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) signs embargo against team %d due to TRADE_EMBARGO with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), (TeamTypes)trade.m_iData, eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		break;

	case TRADE_CIVIC:
		paeNewCivics = new CivicTypes[GC.getNumCivicOptionInfos()];

		for (iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			paeNewCivics[iI] = GET_PLAYER(eFromPlayer).getCivics((CivicOptionTypes)iI);
		}

		paeNewCivics[GC.getCivicInfo((CivicTypes)trade.m_iData).getCivicOptionType()] = ((CivicTypes)trade.m_iData);

		GET_PLAYER(eFromPlayer).revolution(paeNewCivics, true);

		if (GET_PLAYER(eFromPlayer).AI_getCivicTimer() < GC.getDefineINT("PEACE_TREATY_LENGTH"))
		{
			GET_PLAYER(eFromPlayer).AI_setCivicTimer(GC.getDefineINT("PEACE_TREATY_LENGTH"));
		}

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) switched civics due to TRADE_CIVICS with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		SAFE_DELETE_ARRAY(paeNewCivics);
		break;

	case TRADE_RELIGION:
		GET_PLAYER(eFromPlayer).convert((ReligionTypes)trade.m_iData);

		if (GET_PLAYER(eFromPlayer).AI_getReligionTimer() < GC.getDefineINT("PEACE_TREATY_LENGTH"))
		{
			GET_PLAYER(eFromPlayer).AI_setReligionTimer(GC.getDefineINT("PEACE_TREATY_LENGTH"));
		}

		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) switched religions due to TRADE_RELIGION with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

		break;

/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
  case TRADE_EMBASSY:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
	        if (trade.m_iData == 0)
	        {
	            startTeamTrade(TRADE_EMBASSY, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), true);
	            GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setHasEmbassy(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
	        }
	        else
	        {
	            bSave = true;
	        }
		}
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades Embassy due to TRADE_EMBASSY with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}

        break;

    case TRADE_CONTACT:
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades contact with (todo) due to TRADE_CONTACT with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
       		 GET_TEAM(GET_PLAYER(eToPlayer).getTeam()).meet((TeamTypes)trade.m_iData, false); //Was true...
		}
        break;

	case TRADE_WAR_REPARATIONS:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			GET_PLAYER(eFromPlayer).changeGold(-(trade.m_iData));
			GET_PLAYER(eToPlayer).changeGold(trade.m_iData);

			GET_PLAYER(eToPlayer).AI_changeMemoryCount(eFromPlayer, MEMORY_DECLARED_WAR , -GET_PLAYER(eToPlayer).AI_getMemoryCount(eFromPlayer, MEMORY_DECLARED_WAR));
			GET_PLAYER(eToPlayer).AI_changeMemoryCount(eFromPlayer, MEMORY_HIRED_WAR_ALLY, -GET_PLAYER(eToPlayer).AI_getMemoryCount(eFromPlayer, MEMORY_HIRED_WAR_ALLY));
			GET_PLAYER(eToPlayer).AI_changeMemoryCount(eFromPlayer, MEMORY_NUKED_US, -GET_PLAYER(eToPlayer).AI_getMemoryCount(eFromPlayer, MEMORY_NUKED_US));
			GET_PLAYER(eToPlayer).AI_changeMemoryCount(eFromPlayer, MEMORY_RAZED_CITY, -GET_PLAYER(eToPlayer).AI_getMemoryCount(eFromPlayer, MEMORY_RAZED_CITY));
			GET_PLAYER(eToPlayer).AI_changeMemoryCount(eFromPlayer, MEMORY_RAZED_HOLY_CITY, -GET_PLAYER(eToPlayer).AI_getMemoryCount(eFromPlayer, MEMORY_RAZED_HOLY_CITY));
			GET_PLAYER(eToPlayer).AI_changeMemoryCount(eFromPlayer, MEMORY_BACKSTAB, -GET_PLAYER(eToPlayer).AI_getMemoryCount(eFromPlayer, MEMORY_BACKSTAB));
			GET_PLAYER(eToPlayer).AI_changeMemoryCount(eFromPlayer, MEMORY_EVENT_GOOD_TO_US, 2);
		}
		break;
    case TRADE_CORPORATION:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			CvCity* pOldHeadquarters = GC.getGameINLINE().getHeadquarters((CorporationTypes)trade.m_iData);
			pNewHQCity = GET_PLAYER(eToPlayer).getBestHQCity((CorporationTypes)trade.m_iData);
			pNewHQCity->setHasCorporation((CorporationTypes)trade.m_iData, true, false, false);
			GC.getGameINLINE().setHeadquarters((CorporationTypes)trade.m_iData, pNewHQCity, true);
			//Move the HQ building over to the new city.
			for (int i = 0; i < GC.getNumBuildingInfos(); i++)
			{
				//if (i != NO_BUILDING)
				{
					if ((CorporationTypes)GC.getBuildingInfo((BuildingTypes)i).getGlobalCorporationCommerce() == ((CorporationTypes)trade.m_iData))
					{
						pNewHQCity->setNumRealBuilding((BuildingTypes)i, 1);
						pOldHeadquarters->setNumRealBuilding((BuildingTypes)i, 0);
						break;
					}
				}
			}
			
			//The old HQ city still has the corporation, just not the HQ. 
			if (pOldHeadquarters != NULL)
				pOldHeadquarters->setHasCorporation((CorporationTypes)trade.m_iData, true, false, false);
				
			GET_PLAYER(eToPlayer).updateCorporation();
			GET_PLAYER(eFromPlayer).updateCorporation();
			for (int i = 0; i < MAX_PLAYERS; i++)
			{
				if (GET_TEAM(GET_PLAYER((PlayerTypes)i).getTeam()).isHasMet(GET_PLAYER(eToPlayer).getTeam()) || GET_TEAM(GET_PLAYER((PlayerTypes)i).getTeam()).isHasMet(GET_PLAYER(eFromPlayer).getTeam()))
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_TRADE", GC.getCorporationInfo((CorporationTypes)trade.m_iData).getDescription(), GET_PLAYER(eFromPlayer).getCivilizationDescriptionKey(), GET_PLAYER(eToPlayer).getCivilizationDescriptionKey()).GetCString();
					gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)i), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_GOLDAGESTART", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
				}
			}
		}
		break;

    case TRADE_SECRETARY_GENERAL_VOTE:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			GET_PLAYER(eFromPlayer).setPledgedSecretaryGeneralVote(GET_PLAYER(eToPlayer).getTeam());
		}
		break;

/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	case TRADE_OPEN_BORDERS:
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades Open Borders due to TRADE_OPEN_BORDERS with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}
		if (trade.m_iData == 0)
		{
			startTeamTrade(TRADE_OPEN_BORDERS, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), true);
			GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setOpenBorders(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
/************************************************************************************************/
/* Afforess	                  Start		 06/16/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
			endTeamTrade(TRADE_RIGHT_OF_PASSAGE, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
		}
		else
		{
			bSave = true;
		}
		break;

/************************************************************************************************/
/* Afforess	                  Start		 06/26/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	case TRADE_RIGHT_OF_PASSAGE:
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (trade.m_iData == 0)
			{
				startTeamTrade(TRADE_RIGHT_OF_PASSAGE, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), true);
				GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setLimitedBorders(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
			}
			else
			{
				bSave = true;
			}

			if( gTeamLogLevel >= 2 )
			{
				logBBAI("      Player %d (%S) trades Right of Passage due to TRADE_RIGHT_OF_PASSAGE with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
			}
		}
		break;

	case TRADE_FREE_TRADE_ZONE:
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades Free Trade Zone to player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (trade.m_iData == 0)
			{
				startTeamTrade(TRADE_FREE_TRADE_ZONE, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), true);
				GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setFreeTradeAgreement(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
			}
			else
			{
				bSave = true;
			}
		}
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

	case TRADE_DEFENSIVE_PACT:
		if (trade.m_iData == 0)
		{
			startTeamTrade(TRADE_DEFENSIVE_PACT, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), true);
			GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setDefensivePact(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
			if( gTeamLogLevel >= 2 )
			{
				logBBAI("      Player %d (%S) signs defensive pact due to TRADE_DEFENSIVE_PACT with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
			}
		}
		else
		{
			bSave = true;
		}
		break;

	case TRADE_PERMANENT_ALLIANCE:
		break;

	case TRADE_PEACE_TREATY:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setForcePeace(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) signs peace treaty due to TRADE_PEACE_TREATY with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}
		bSave = true;
		break;


/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	case TRADE_NON_AGGRESSION:
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades Non-agression pact with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (trade.m_iData == 0)
			{
				startTeamTrade(TRADE_NON_AGGRESSION, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), true);
				GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setHasNonAggression(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
			}
			else
			{
				bSave = true;
			}
		}
		break;

	case TRADE_POW:
		if( gTeamLogLevel >= 2 )
		{
			logBBAI("      Player %d (%S) trades TRADE_POW with player %d (%S)", eFromPlayer, GET_PLAYER(eFromPlayer).getCivilizationDescription(0), eToPlayer, GET_PLAYER(eToPlayer).getCivilizationDescription(0) );
		}
		if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
		{
			if (trade.m_iData == 0)
			{
				startTeamTrade(TRADE_POW, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam(), true);
				GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setHasPOW(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), true);
	
				for (iI = 0; iI < MAX_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eFromPlayer).getTeam())
						{
							for (int iJ = 0; iJ < MAX_PLAYERS; iJ++)
							{
								if (GET_PLAYER((PlayerTypes)iJ).isAlive())
								{
									if (GET_PLAYER((PlayerTypes)iJ).getTeam() == GET_PLAYER(eToPlayer).getTeam())
									{
										GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(((PlayerTypes)iJ), MEMORY_TRADED_POW, 1);
									}
								}
							}
						}
					}
				}



				//for (iI = 0; iI < MAX_CIV_PLAYERS; iI++)
				//{
					//if (GET_PLAYER((PlayerTypes)iI).isAlive())
					//
						//if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eToPlayer).getTeam())
						//{
						//	GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(((PlayerTypes)iI), MEMORY_TRADED_POW, 1);
						//}
					//}
				//}
			}
			else
			{
				bSave = true;
			}
		}

		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/
	default:
		FAssert(false);
		break;
	}

	return bSave;
}


void CvDeal::endTrade(TradeData trade, PlayerTypes eFromPlayer, PlayerTypes eToPlayer, bool bTeam)
{
	int iI, iJ;

	switch (trade.m_eItemType)
	{
	case TRADE_TECHNOLOGIES:
		FAssert(false);
		break;

	case TRADE_RESOURCES:
		GET_PLAYER(eToPlayer).changeBonusImport(((BonusTypes)trade.m_iData), -1);
		GET_PLAYER(eFromPlayer).changeBonusExport(((BonusTypes)trade.m_iData), -1);
		break;

	case TRADE_CITIES:
/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	case TRADE_WORKER:
	case TRADE_MILITARY_UNIT:
	case TRADE_CONTACT:
	case TRADE_CORPORATION:
	case TRADE_SECRETARY_GENERAL_VOTE:
	case TRADE_WAR_REPARATIONS:
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	case TRADE_GOLD:
		FAssert(false);
		break;

	case TRADE_GOLD_PER_TURN:
		GET_PLAYER(eFromPlayer).changeGoldPerTurnByPlayer(eToPlayer, trade.m_iData);
		GET_PLAYER(eToPlayer).changeGoldPerTurnByPlayer(eFromPlayer, -(trade.m_iData));
		break;

	case TRADE_MAPS:
	case TRADE_PEACE:
	case TRADE_WAR:
/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	case TRADE_WAR_PREPARE:
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/
	case TRADE_EMBARGO:
	case TRADE_CIVIC:
	case TRADE_RELIGION:
		FAssert(false);
		break;

	case TRADE_VASSAL:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setVassal(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false, false);
		if (bTeam)
		{
			endTeamTrade(TRADE_VASSAL, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}
		break;

	case TRADE_SURRENDER:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setVassal(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false, true);
		if (bTeam)
		{
			endTeamTrade(TRADE_SURRENDER, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}
		break;
		
/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
   case TRADE_EMBASSY:
        GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setHasEmbassy(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
        if (bTeam)
        {
            endTeamTrade(TRADE_EMBASSY, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
			endTeamTrade(TRADE_OPEN_BORDERS, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
			endTeamTrade(TRADE_DEFENSIVE_PACT, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
			endTeamTrade(TRADE_FREE_TRADE_ZONE, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
        	endTeamTrade(TRADE_NON_AGGRESSION, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eFromPlayer).getTeam())
				{
					for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iJ).getTeam() == GET_PLAYER(eToPlayer).getTeam())
							{
								GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(((PlayerTypes)iJ), MEMORY_RECALLED_AMBASSADOR, 1);
							}
						}
					}
				}
			}
		}
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/	

	case TRADE_OPEN_BORDERS:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setOpenBorders(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
		if (bTeam)
		{
			endTeamTrade(TRADE_OPEN_BORDERS, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
/************************************************************************************************/
/* Afforess	                  Start		 06/16/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
			endTeamTrade(TRADE_RIGHT_OF_PASSAGE, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
		}

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eToPlayer).getTeam())
				{
					for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iJ).getTeam() == GET_PLAYER(eFromPlayer).getTeam())
							{
								GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(((PlayerTypes)iJ), MEMORY_CANCELLED_OPEN_BORDERS, 1);
							}
						}
					}
				}
			}
		}
		break;

/************************************************************************************************/
/* Afforess	                  Start		 06/26/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	case TRADE_RIGHT_OF_PASSAGE:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setLimitedBorders(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
		if (bTeam)
		{
			endTeamTrade(TRADE_RIGHT_OF_PASSAGE, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eToPlayer).getTeam())
				{
					for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iJ).getTeam() == GET_PLAYER(eFromPlayer).getTeam())
							{
								GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(((PlayerTypes)iJ), MEMORY_CANCELLED_OPEN_BORDERS, 1);
							}
						}
					}
				}
			}
		}
		break;

	case TRADE_FREE_TRADE_ZONE:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setFreeTradeAgreement(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
		if (bTeam)
		{
			endTeamTrade(TRADE_FREE_TRADE_ZONE, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}
		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eToPlayer).getTeam())
				{
					for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iJ).getTeam() == GET_PLAYER(eFromPlayer).getTeam())
							{
								GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(((PlayerTypes)iJ), MEMORY_CANCELLED_FREE_TRADE_AGREEMENT, 1);
							}
						}
					}
				}
			}
		}
		break;
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/

	case TRADE_DEFENSIVE_PACT:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setDefensivePact(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
		if (bTeam)
		{
			endTeamTrade(TRADE_DEFENSIVE_PACT, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}
		break;

	case TRADE_PERMANENT_ALLIANCE:
		FAssert(false);
		break;

	case TRADE_PEACE_TREATY:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setForcePeace(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       START															     */
/*************************************************************************************************/
	case TRADE_NON_AGGRESSION:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setHasNonAggression(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
		if (bTeam)
		{
			endTeamTrade(TRADE_NON_AGGRESSION, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}

		for (iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == GET_PLAYER(eToPlayer).getTeam())
				{
					for (iJ = 0; iJ < MAX_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							if (GET_PLAYER((PlayerTypes)iJ).getTeam() == GET_PLAYER(eFromPlayer).getTeam())
							{
								GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(((PlayerTypes)iJ), MEMORY_CANCELLED_NON_AGGRESSION, 1);
							}
						}
					}
				}
			}
		}
		break;

	case TRADE_POW:
		GET_TEAM(GET_PLAYER(eFromPlayer).getTeam()).setHasPOW(((TeamTypes)(GET_PLAYER(eToPlayer).getTeam())), false);
		if (bTeam)
		{
			endTeamTrade(TRADE_POW, GET_PLAYER(eFromPlayer).getTeam(), GET_PLAYER(eToPlayer).getTeam());
		}
		break;
/*************************************************************************************************/
/** Advanced Diplomacy       END															     */
/*************************************************************************************************/
	default:
		FAssert(false);
		break;
	}
}

void CvDeal::startTeamTrade(TradeableItems eItem, TeamTypes eFromTeam, TeamTypes eToTeam, bool bDual)
{
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayer& kLoopFromPlayer = GET_PLAYER((PlayerTypes)iI);
		if (kLoopFromPlayer.isAlive() )
		{
			if (kLoopFromPlayer.getTeam() == eFromTeam)
			{
				for (int iJ = 0; iJ < MAX_PLAYERS; iJ++)
				{
					CvPlayer& kLoopToPlayer = GET_PLAYER((PlayerTypes)iJ);
					if (kLoopToPlayer.isAlive())
					{
						if (kLoopToPlayer.getTeam() == eToTeam)
						{
							TradeData item;
							setTradeItem(&item, eItem, 1);
							CLinkList<TradeData> ourList;
							ourList.insertAtEnd(item);
							CLinkList<TradeData> theirList;
							if (bDual)
							{
								theirList.insertAtEnd(item);
							}
							GC.getGame().implementDeal((PlayerTypes)iI, (PlayerTypes)iJ, &ourList, &theirList);
						}
					}
				}
			}
		}
	}
}

void CvDeal::endTeamTrade(TradeableItems eItem, TeamTypes eFromTeam, TeamTypes eToTeam)
{
	CvDeal* pLoopDeal;
	int iLoop;
	CLLNode<TradeData>* pNode;

	for (pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if (pLoopDeal != this)
		{
			bool bValid = true;

			if (GET_PLAYER(pLoopDeal->getFirstPlayer()).getTeam() == eFromTeam && GET_PLAYER(pLoopDeal->getSecondPlayer()).getTeam() == eToTeam)
			{
				if (pLoopDeal->getFirstTrades())
				{
					for (pNode = pLoopDeal->getFirstTrades()->head(); pNode; pNode = pLoopDeal->getFirstTrades()->next(pNode))
					{
						if (pNode->m_data.m_eItemType == eItem)
						{
							bValid = false;
						}
					}
				}
			}

			if (bValid && GET_PLAYER(pLoopDeal->getFirstPlayer()).getTeam() == eToTeam && GET_PLAYER(pLoopDeal->getSecondPlayer()).getTeam() == eFromTeam)
			{
				if (pLoopDeal->getSecondTrades() != NULL)
				{
					for (pNode = pLoopDeal->getSecondTrades()->head(); pNode; pNode = pLoopDeal->getSecondTrades()->next(pNode))
					{
						if (pNode->m_data.m_eItemType == eItem)
						{
							bValid = false;
						}
					}
				}
			}

			if (!bValid)
			{
				pLoopDeal->kill(false);
			}
		}
	}
}

bool CvDeal::isCancelable(PlayerTypes eByPlayer, CvWString* pszReason)
{
	if (isUncancelableVassalDeal(eByPlayer, pszReason))
	{
		return false;
	}

	int iTurns = turnsToCancel(eByPlayer);
	if (pszReason)
	{
		if (iTurns > 0)
		{
			*pszReason = gDLL->getText("TXT_KEY_MISC_DEAL_NO_CANCEL", iTurns);
		}
	}

	return (iTurns <= 0);
}

int CvDeal::turnsToCancel(PlayerTypes eByPlayer)
{
	return (getInitialGameTurn() + GC.getDefineINT("PEACE_TREATY_LENGTH") - GC.getGameINLINE().getGameTurn());
}

// static
bool CvDeal::isAnnual(TradeableItems eItem)
{
	switch (eItem)
	{
	case TRADE_RESOURCES:
	case TRADE_GOLD_PER_TURN:
	case TRADE_VASSAL:
	case TRADE_SURRENDER:
	case TRADE_OPEN_BORDERS:
	case TRADE_DEFENSIVE_PACT:
	case TRADE_PERMANENT_ALLIANCE:
/************************************************************************************************/
/* Afforess	                  Start		 06/16/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	case TRADE_RIGHT_OF_PASSAGE:
	case TRADE_FREE_TRADE_ZONE:
	case TRADE_EMBASSY:
	case TRADE_NON_AGGRESSION:
	case TRADE_POW:
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
		return true;
		break;
	}

	return false;
}

// static
bool CvDeal::isDual(TradeableItems eItem, bool bExcludePeace)
{
	switch (eItem)
	{
	case TRADE_OPEN_BORDERS:
	case TRADE_DEFENSIVE_PACT:
	case TRADE_PERMANENT_ALLIANCE:
/************************************************************************************************/
/* Afforess	                  Start		 06/16/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	case TRADE_EMBASSY:
	case TRADE_RIGHT_OF_PASSAGE:
	case TRADE_FREE_TRADE_ZONE:
	case TRADE_NON_AGGRESSION: 
	case TRADE_POW:
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
		return true;
	case TRADE_PEACE_TREATY:
		return (!bExcludePeace);
	}

	return false;
}

// static
bool CvDeal::hasData(TradeableItems eItem)
{
/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_TACTICS))
	{
		return (eItem != TRADE_MAPS &&
			eItem != TRADE_VASSAL &&
			eItem != TRADE_SURRENDER &&
			eItem != TRADE_OPEN_BORDERS &&
			eItem != TRADE_DEFENSIVE_PACT &&
			eItem != TRADE_PERMANENT_ALLIANCE &&
			eItem != TRADE_PEACE_TREATY &&
			eItem != TRADE_EMBASSY &&
			eItem != TRADE_NON_AGGRESSION && 
			eItem != TRADE_POW);
	}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
	return (eItem != TRADE_MAPS &&
		eItem != TRADE_VASSAL &&
		eItem != TRADE_SURRENDER &&
		eItem != TRADE_OPEN_BORDERS &&
		eItem != TRADE_DEFENSIVE_PACT &&
		eItem != TRADE_PERMANENT_ALLIANCE &&
		eItem != TRADE_PEACE_TREATY);
}

bool CvDeal::isGold(TradeableItems eItem)
{
	return (eItem == getGoldItem() || eItem == getGoldPerTurnItem());
}

bool CvDeal::isVassal(TradeableItems eItem)
{
	return (eItem == TRADE_VASSAL || eItem == TRADE_SURRENDER);
}

bool CvDeal::isEndWar(TradeableItems eItem)
{
	if (eItem == getPeaceItem())
	{
		return true;
	}

	if (isVassal(eItem))
	{
		return true;
	}

	return false;
}

TradeableItems CvDeal::getPeaceItem()
{
	return TRADE_PEACE_TREATY;
}

TradeableItems CvDeal::getGoldItem()
{
	return TRADE_GOLD;
}

TradeableItems CvDeal::getGoldPerTurnItem()
{
	return TRADE_GOLD_PER_TURN;
}

/************************************************************************************************/
/* Afforess	                  Start		 07/17/10                                               */
/* Advanced Diplomacy                                                                           */
/************************************************************************************************/
bool CvDeal::isEmbassy()
{
	CLLNode<TradeData>* pNode;

	for (pNode = headFirstTradesNode(); (pNode != NULL); pNode = nextFirstTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == TRADE_EMBASSY)
		{
			return true;
		}
	}

	for (pNode = headSecondTradesNode(); (pNode != NULL); pNode = nextSecondTradesNode(pNode))
	{
		if (pNode->m_data.m_eItemType == TRADE_EMBASSY)
		{
			return true;
		}
	}
	
	return false;
}
/************************************************************************************************/
/* Advanced Diplomacy         END                                                               */
/************************************************************************************************/
