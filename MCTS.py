import Node as nd

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




