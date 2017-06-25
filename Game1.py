import numpy as np
import itertools as iter

#---Customize to specific use case.---#
def GetActions(State):
	# Get the possible actions given a state.
	N = (int)(np.sum(State))

	if(any(State) == None):
		return None

	# Get matrix of possible actions.
	A = np.array(list(iter.product([0, 1], repeat = N)))
	if(len(A) > 0):
		A = np.delete(A, 0, 0)
	# Remove no action.
	AToS = MapActionsToState(State, A)

	return AToS

def MapActionsToState(State, A):
	(m, n) = A.shape
	AToS = np.zeros((m, len(State)))

	for i in range(m):
		a = 0
		for j in range(len(State)):
			if(State[j] == 0):
				continue
			else:
				if(A[i, a] == 1):
					AToS[i,j] = 1
					a += 1
				else:
					a += 1

	# for i in range(m):
	# 	a = 0
	# 	print "State:", State
	# 	print "Action:", A[i, :]
	# 	for j in range(len(State)):
	# 		if(State[j] and A[i, a]):
	# 			AToS[i, j] = 1
	# 			a += 1
	# 	print "AToS:", AToS[i,:]
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
