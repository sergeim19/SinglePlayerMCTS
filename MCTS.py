import Node as nd
import numpy as np
import Game1 as game

class MCTS:
	def __init__(self, Node):
		self.root = Node

	def Selection(self):
		SelectedChild = self.root
		HasChild = False

		# Check if child nodes exist. 
		if(len(SelectedChild.children) > 0):
			HasChild = True
		else:
			HasChild = False

		while(HasChild):
			SelectedChild = self.SelectChild(SelectedChild)
			if(len(SelectedChild.children) == 0):
				HasChild  = False
			#SelectedChild.visits += 1.0

		print "\nSelected:", SelectedChild.state
		#self.root.visits += 1.0

		return SelectedChild

	def SelectChild(self, Node):
		if(len(Node.children) == 0):
			return Node

		for Child in Node.children:
			if(Child.visits > 0.0):
				continue
			else:
				print "Considered child", Child.state, "UTC: inf", 
				return Child

		MaxWeight = 0.0
		for Child in Node.children:
			Weight = self.EvalUTC(Child)
			print "Considered child:", Child.state, "UTC:", Weight
			if(Weight > MaxWeight):
				MaxWeight = Weight			
				SelectedChild = Child
		return SelectedChild
		
	def Expansion(self, Leaf):
		if(self.IsTerminal((Leaf))):
			return False
		elif(Leaf.visits == 0):
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
		CurrentState = Node.state
		#if(any(CurrentState) == False):
		#	return None

		print "Begin Simulation"

		Level = self.GetLevel(Node)
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
			Level += 1.0
			print "Action:", Action, "\nCurrentState:", CurrentState
		
		Result = 1.0 / Level # Game specific
		print "Result:", Result
		return Result
	
	def Backpropagation(self, Node, Result):
		# Update Node's weight.
 		CurrentNode = Node
		CurrentNode.wins += Result
		CurrentNode.ressq += Result**2
		CurrentNode.visits += 1

		while(self.HasParent(CurrentNode)):
			# Update parent node's weight.
			CurrentNode = CurrentNode.parent
			CurrentNode.wins += Result
			CurrentNode.visits += 1

		self.root.wins += Result
	
	def HasParent(self, Node):
		if(Node.parent == None):
			return False
		else:
			return True
			
	def EvalUTC(self, Node):
		#c = np.sqrt(2)
		c = 1.
		w = Node.wins
		n = Node.visits
		sumsq = Node.ressq
		if(Node.parent == None):
			t = Node.visits
		else:
			t = Node.parent.visits

		UTC = w/n + c * np.sqrt(np.log(t)/n)
		D = 20000.
		Correction = np.sqrt((sumsq - n * (w/n)**2 + D)/n)
		return UTC + Correction

	def GetLevel(self, Node):
		Level = 0.0
		while(Node.parent):
			Level += 1.0
			Node = Node.parent
		return Level

	def PrintTree(self):
		f = open('Tree.txt', 'w')
		Node = self.root
		self.PrintNode(f, Node, "", False)
		f.close()

	def PrintNode(self, file, Node, Indent, IsTerminal):
		file.write(Indent)
		if(IsTerminal):
			file.write("\-")
			Indent += "  "
		else:
			file.write("|-")
			Indent += "| "

		string = str(self.GetLevel(Node)) + ") (["
		for i in Node.state:
			string += str(i) + ", " 
		string += "], W: " + str(Node.wins) + ", N: " + str(Node.visits) + ") \n"
		file.write(string)

		for Child in Node.children:
			self.PrintNode(file, Child, Indent, self.IsTerminal(Child))
			
	def Run(self, MaxIter = 100):
		for i in range(MaxIter):
			print "\n===== Begin iteration:", i, "====="
			X = self.Selection()
			Y = self.Expansion(X)
			if(Y):
				Result = self.Simulation(Y)
				self.Backpropagation(Y, Result)
			else:
				Level = self.GetLevel(X)
				Result = 1.0/Level
				self.Backpropagation(X, Result)
