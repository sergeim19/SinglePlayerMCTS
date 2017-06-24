import Node as nd
import TestGame as tg

class MCTS:
	def __init__(self, Node):
		self.root = Node

	def Selection(self):		
		Weight = 0.0
		SelectedChild = self.root
		HasChild = False

		# Check if child nodes exist. 
		if(len(SelectedChild.children) > 0):
			HasChild = True
		else:
			HasChild = False

		# Temporary policy: Select child with the biggest weight.
		while(HasChild):
			MaxWeight = 0.0
			for Child in SelectedChild.children:
				Weight = Child.weight				
				if(Weight > MaxWeight):
					MaxWeight = Weight			
					SelectedChild = Child
				elif(Weight == None):
					SelectedChild = Child
					break					

			if(len(SelectedChild.children) == 0):
				HasChild  = False

		return SelectedChild
	
	def Expansion(Leaf):
		if(IsTerminal((Leaf))):
			return Leaf
		else:
			# Expand.
			if(len(Leaf.children) == 0):
<<<<<<< Updated upstream
				EvalChildNodes(Leaf)
			Child = SelectChildNode(Leaf)
			
	def IsTerminal(Node):
		# TO-DO: Evaluate if node is terminal.
		return False

 	def EvalChildNodes(Node):
		# TO-DO: Evaluate child nodes.
	
	def SelectChildNode(Node):
		# Randomly selects a child node.
		Len = len(Node.children)
		i = np.random.randint(0, Len)
		return Node.children[i]

	def Simulation(Node):
		CurrentState = Node.state
		
		# TO-DO: Perform simulation.
		while(!IsTerminal(CurrentState)):
			A = GetActions(CurrentState)
			# Get random action.
			(m, n) = A.shape                                             
			i = np.random.randint(0, m)
			Action = A[i, :]
			CurrentState = ApplyAction(CurrentState, Action)
		
		return Result
	
	def Backpropagation(Node, Result):
		# TO-DO: Update Node's weight.
 		CurrentNode = Node

		while(HasParent(Node)):
			# TO-DO: Update parent node's weight.
			CurrentNode = Node.parent
	
	def HasParent(Node):
		Parent = Node.parent
		if(Parent == None):
			HasParent = False
		else:
			HasParent = True
			
	def Run(MaxIter = 1000):
		for i in MaxIter:
			X = Selection()
			Y = Expansion(S)
			Result = Simulation(Y)
			Backpropagation(Y, Result)
			# TO-DO: Break in case no updates to tree before MaxIter reached.
=======
				Children = EvalChildren(Leaf)
				Leaf.children = Children
			Child = SelectChildNode(Leaf)
			
	def IsTerminal(Node):
		# Evaluate if node is terminal.
		if(tg.IsTerminal(Node.state)):
			return True	
		else:
			return False
		return False
>>>>>>> Stashed changes

 	def EvalChildren(Node):
		# Evaluate child nodes.
		A = GetActions(CurrentState.state)
		Children = []
		for i in len(A[:,0]):
			Action = A[i,:]
			ChildState = ApplyAction(Node.state, Action)
			ChildNode = Node(ChildState)
			Children.append(ChildNode)

		return Children

	def SelectChildNode(Node):
		# Randomly selects a child node.
		Len = len(Node.children)
		i = np.random.randint(0, Len)
		return Node.children[i]

	def Simulation(Node):
		CurrentState = Node.state
		
		# Perform simulation.
		while(not(IsTerminal(CurrentState))):
			A = GetActions(CurrentState)
			# Get random action.
			(m, n) = A.shape                                             
			i = np.random.randint(0, m)
			Action = A[i, :]
			CurrentState = ApplyAction(CurrentState, Action)
		
		return Result
	
	def Backpropagation(Node, Result):
		# TO-DO: Update Node's weight.
 		CurrentNode = Node

		while(HasParent(Node)):
			# TO-DO: Update parent node's weight.
			CurrentNode = Node.parent
	
	def HasParent(Node):
		Parent = Node.parent
		if(Parent == None):
			HasParent = False
		else:
			HasParent = True
			
	def EvalUTC(Node):
		c = np.sqrt(2)
				
	def Run(MaxIter = 1000):
		for i in MaxIter:
			X = Selection()
			Y = Expansion(S)
			Result = Simulation(Y)
			Backpropagation(Y, Result)
			# TO-DO: Break in case no updates to tree before MaxIter reached.