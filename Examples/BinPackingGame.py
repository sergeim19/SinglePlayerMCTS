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
	if(CurrentBinVolume == MAX_VOLUME):
		return PossibleActions
	else:
		for i in range(len(CurrentState.items)):
			if((CurrentBinVolume + CurrentState.items[i]) <= MAX_VOLUME):
				PossibleActions.append(i)
		return PossibleActions

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
	i = np.random.randint(0, len(Actions))
	Action = Actions[i]
	NextState = ApplyAction(CurrentState, Action)
	return NextState

def GetVolume(Bin):
	return sum(Bin)

def IsTerminal(State):
	if(sum(State.items) == 0.0):
		return True
	else:
		return False

def GetStateRepresentation(State):
	return State.bins

def EvalNextStates(CurrentState):
	A = GetActions(CurrentState)
	NextStates = []
	#for i in range(len(A[:,0])):
	for i in range(len(A)):
		#Action = A[i,:]
		Action = A[i]
		NextState = ApplyAction(CurrentState, Action)
		NextStates.append(NextState)

	if(A == []):
		NextState = ApplyAction(CurrentState, A)
		NextStates.append(NextState)

	return NextStates
