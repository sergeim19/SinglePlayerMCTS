import numpy as np
import itertools as iter
import copy

# States are given as:
# bins = np.array([v1, v2,..., vn])
# state = np.array([v1, v2, v3, ..., vk])
MAX_VOLUME = 10.0

class State:
	def __init__(self, items, bins):
		self.items = items
		self.bins = bins

def GetActions(CurrentState):
	Bins = CurrentState.bins
	CurrentBinVolume = GetVolume(Bins[-1])

	PossibleActions = [-1.0]
	if(CurrentBinVolume == 10.0):
		return PossibleActions
	else:
		for i in range(len(CurrentState.items)):
			if((CurrentBinVolume + CurrentState.items[i]) <= MAX_VOLUME):
				PossibleActions.append(i)	
		return PossibleActions

def MapActionsToState(CurrentState, Actions):
	#if(len(Actions) == 0):
	#	Items = CurrentState.items[:]
	#	Bins = copy.deepcopy(CurrentState.bins[:])
	#	Bins.append([])
	#	NextStates = State(Items, Bins)
	#else:
	for i in len(Actions):
		NextStates.append(ApplyAction(CurrentState(Actions[i])))

	return NextStates

def ApplyAction(CurrentState, Action):
	Items = CurrentState.items[:]
	Bins = copy.deepcopy(CurrentState.bins[:])
	if(Action == -1.0):
		Bins.append([])
		State2 = State(Items, Bins)
	else:
		Bins[-1].append(Items[Action])
		del Items[Action]
		State2 = State(Items, Bins)
     
	return State2

def GetNextState(CurrentState):
	Actions = GetActions(CurrentState)
	# Get random action.            
	#if(Actions == []):
	#	NextState = ApplyAction(CurrentState, Actions)
	#else:
	i = np.random.randint(0, len(Actions))
	Action = Actions[i]
	NextState = ApplyAction(CurrentState, Action)
#	else:
#		Items = CurrentState.items[:]
#		Bins = copy.deepcopy(CurrentState.bins[:])
#		Bins.append([])
#		NextState = State(Items, Bins)

	return NextState

def GetVolume(Bin):
	return sum(Bin)

#---Customize to specific use case.---#
# def GetNextState(CurrentState):
# 	MaxVolume = 10.0
# 	NextBin = []
# 	Items = CurrentState.items[:]

# 	print "Items: ", Items
# 	while(np.sum(NextBin) < 10.0):
# 		i = np.random.randint(0, len(Items))
# 		if(Items[i] > 0.0):
# 			NextBin.append(Items[i])
# 			Items[i] = 0.0

# 	NextState = State(Items, NextBin)	

# 	return NextState

def IsTerminal(State):
	if(sum(State.items) == 0.0):
		return True
	else:
		return False

def GetState():
	return State.state


