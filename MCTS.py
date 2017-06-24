import Node as nd
import numpy as np
import Game1 as game

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

		Skip = False
		while(HasChild and not Skip):
			MaxWeight = 0.0

			for Child in SelectedChild.children:
				if(Child.visits > 0.0):
					continue
				else:
					SelectedChild = Child
					Skip = True
					break

			if(not Skip):
				for Child in SelectedChild.children:
						Weight = self.EvalUTC(Child)
						if(Weight > MaxWeight):
							MaxWeight = Weight			
							SelectedChild = Child
							break					

			if(len(SelectedChild.children) == 0):
				HasChild  = False

		print "Selected:",SelectedChild.state
		SelectedChild.visits += 1.0
		return SelectedChild
	
	def Expansion(self, Leaf):
		if(self.IsTerminal((Leaf))):
			return Leaf
		else:
			# Expand.
			if(len(Leaf.children) == 0):
				Children = self.EvalChildren(Leaf)
				for NewChild in Children:
					if(np.all(NewChild.state == Leaf.state)):
						continue
					Leaf.AppendChild(NewChild)
			Child = self.SelectChildNode(Leaf)

		print "Expanded: ", Child.state
		return Child
			
	def IsTerminal(self, Node):
		# Evaluate if node is terminal.
		if(game.IsTerminal(Node.state)):
			return True	
		else:
			return False
		return False

 	def EvalChildren(self, Node):
		# Evaluate child nodes.
		A = game.GetActions(Node.state)
		Children = []
		for i in range(len(A[:,0])):
			Action = A[i,:]
			ChildState = game.ApplyAction(Node.state, Action)
			ChildNode = nd.Node(ChildState)
			Children.append(ChildNode)

		return Children

	def SelectChildNode(self, Node):
		# Randomly selects a child node.
		Len = len(Node.children)
		i = np.random.randint(0, Len)
		return Node.children[i]

	def Simulation(self, Node):
		if(Node == None):
			return None

		CurrentState = Node.state
		if(CurrentState == None):
			return None

		# Perform simulation.
		while(not(game.IsTerminal(CurrentState))):
			A = game.GetActions(CurrentState)
			if(A == None):
				return False
			# Get random action.
			(m, n) = A.shape                                             
			i = np.random.randint(0, m)
			Action = A[i, :]
			CurrentState = game.ApplyAction(CurrentState, Action)
			print "Action:", Action, "CurrentState:", CurrentState
		
		Result = 1.0
		print "Result:", Result
		return Result
	
	def Backpropagation(self, Node, Result):
		# Update Node's weight.
 		CurrentNode = Node
		CurrentNode.wins += Result

		while(self.HasParent(CurrentNode)):
			# Update parent node's weight.
			CurrentNode = CurrentNode.parent
			CurrentNode.wins += Result

	
	def HasParent(self, Node):
		if(Node.parent == None):
			return False
		else:
			return True
			
	def EvalUTC(self, Node):
		c = np.sqrt(2)
		w = Node.wins
		n = Node.visits
		if(Node.parent == None):
			t = Node.visits
		else:
			t = Node.parent.visits

		return w/n + c * np.sqrt(np.log(t)/n)

	def Run(self, MaxIter = 100):
		for i in range(MaxIter):
			X = self.Selection()
			Y = self.Expansion(X)
			Result = self.Simulation(Y)
			#if(Result == None):
			#	break
			self.Backpropagation(Y, Result)