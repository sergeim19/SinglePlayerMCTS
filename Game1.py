import numpy as np

#---Customize to specific use case.---#
def GetAction(State):
	# Get the possible actions given a state.
	N = np.sum(State)
	if(State == None):
		return None

	# Get matrix of possible actions.
	# A = ...
	# Assert if len(State) != len(A[0,:])
	AToS = MapActionsToState(State, A)

	return AToS

def MapActionsToState(State, A):
	(m, n) = A.size
	AToS = np.zeros((m, len(State)))

	for i in m:
		a = 0
		for j in len(State):
			if(State[j] and A[a]):
				AToS[i, j] = 1
				a += 1

	return AToS

def ApplyAction(State1, Action):
	State2 = State1 - Action
	for s in State2:
		if(s < 0):
			s = 0

	return State2

def IsTerminal(State):
	if(np.sum(State) == 0):
		return True
	else:
		return False
