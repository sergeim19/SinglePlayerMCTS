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
			print "Next Level"
			# Select child that has 0 visits first.
			for Child in SelectedChild.children:
				if(Child.visits > 0.0):
					continue
				else:
					SelectedChild = Child
					Skip = True
					print "Considered child", SelectedChild.state, "UTC: inf", 
					break

			if(not Skip):
				for Child in SelectedChild.children:
						Weight = self.EvalUTC(Child)
						print "Considered child:", Child.state, "UTC:", Weight
						if(Weight > MaxWeight):
							MaxWeight = Weight			
							SelectedChild = Child
							break					

			if(len(SelectedChild.children) == 0):
				HasChild  = False

			SelectedChild.visits += 1.0

		print "\nSelected:", SelectedChild.state
		self.root.visits += 1.0
		return SelectedChild
	
	def Expansion(self, Leaf):
		if(self.IsTerminal((Leaf))):
			return False
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
		CurrentState = Node.state
		#if(any(CurrentState) == False):
		#	return None

		print "Begin Simulation"
		# Perform simulation.
		while(not(game.IsTerminal(CurrentState))):
			A = game.GetActions(CurrentState)
			#if(any(A) == None):
			#	return False
			# Get random action.
			(m, n) = A.shape                                             
			i = np.random.randint(0, m)
			Action = A[i, :]
			CurrentState = game.ApplyAction(CurrentState, Action)
			print "Action:", Action, "\nCurrentState:", CurrentState
		
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

		self.root.wins += Result
	
	def HasParent(self, Node):
		if(Node.parent == None):
			return False
		else:
			return True
			
	def EvalUTC(self, Node):
		#c = np.sqrt(2)
		c = 1
		w = Node.wins
		n = Node.visits
		if(Node.parent == None):
			t = Node.visits
		else:
			t = Node.parent.visits

		UTC = w/n + c * np.sqrt(np.log(t)/n)
		D = 20000
		Correction = np.sqrt((w - n * (w/n)**2 + D)/n)
		return UTC + Correction

	def Run(self, MaxIter = 1000):
		for i in range(MaxIter):
			print "\n===== Begin iteration:", i, "====="
			X = self.Selection()
			Y = self.Expansion(X)
			if(Y):
				Result = self.Simulation(Y)
				self.Backpropagation(Y, Result)
