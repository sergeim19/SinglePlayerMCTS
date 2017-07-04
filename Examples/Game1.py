import numpy as np
import itertools as iter

#---Customize to specific use case.---#
def GetNextState(State):
	A = self.GetActions(State)
	# Get random action.
	(m, n) = A.shape                                            
	i = np.random.randint(0, m)
	Action = A[i, :]
	NextState = self.ApplyAction(State, Action)

	return NextState
	
def GetActions(State):
	# Get the possible actions given a state.
	N = (int)(np.sum(State))

	if(any(State) == None):
		return None

	# Get matrix of possible actions.
	A = np.array(list(iter.product([0, 1], repeat = N)))

	AToS = MapActionsToState(State, A)

	#print "Before Illegal:", AToS
	AToS = RemoveIllegalActions(AToS)
	#print "After Illegal:", AToS

	# Remove no action.
	if(len(A) > 0):
		A = np.delete(A, 0, 0)

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

	return AToS

def RemoveIllegalActions(Actions):
	(m, n) = Actions.shape
	
	IllegalActions = np.array([[1.,1.,1.,1.],
		[1.,1.,0.,0.],
		[0.,0.,1.,1.],
		[1.,1.,0.,1.],
		[1.,0.,1.,1.],
		[0.,1.,1.,1.],
		[1.,1.,1.,0.]])

	(p, q) = IllegalActions.shape

	ActionsAfter = np.array([[0.,0.,0.,0.]])
	for i in range(m):
		Illegal = False
		for j in range(p):
			if(all(Actions[i,:] == IllegalActions[j,:])):
				Illegal = True
				break
		if(not Illegal):
			ActionsAfter = np.vstack([ActionsAfter, Actions[i,:]])

	return ActionsAfter

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
