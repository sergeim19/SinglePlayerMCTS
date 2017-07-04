import Node as nd
import numpy as np
import BinPackingGame as game

class MCTS:
	def __init__(self, Node, Verbose = False):
		self.root = Node
		self.verbose = Verbose

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

		if(self.verbose):
			#print "\nSelected:", SelectedChild.state.bins
			print "\nSelected: ", game.GetStateRepresentation(SelectedChild.state)
		#self.root.visits += 1.0

		return SelectedChild

	def SelectChild(self, Node):
		if(len(Node.children) == 0):
			return Node

		for Child in Node.children:
			if(Child.visits > 0.0):
				continue
			else:
				if(self.verbose):
					print "Considered child", game.GetStateRepresentation(Child.state), "UTC: inf",
				return Child

		MaxWeight = 0.0
		for Child in Node.children:
			Weight = self.EvalUTC(Child)
			if(self.verbose):
				print "Considered child:", game.GetStateRepresentation(Child.state), "UTC:", Weight
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
			assert (len(Leaf.children) > 0), "Error"
			Child = self.SelectChildNode(Leaf)

		if(self.verbose):
			print "Expanded: ", game.GetStateRepresentation(Child.state)
		return Child

	def IsTerminal(self, Node):
		# Evaluate if node is terminal.
		if(game.IsTerminal(Node.state)):
			return True
		else:
			return False
		return False # Why is this here?

 	def EvalChildren(self, Node):
 		NextStates = game.EvalNextStates(Node.state)
 		Children = []
 		for State in NextStates:
 			ChildNode = nd.Node(State)
 			Children.append(ChildNode)

		return Children

	def SelectChildNode(self, Node):
		# Randomly selects a child node.
		Len = len(Node.children)
		assert Len > 0, "Incorrect length"
		i = np.random.randint(0, Len)
		return Node.children[i]

	def Simulation(self, Node):
		CurrentState = Node.state
		#if(any(CurrentState) == False):
		#	return None
		if(self.verbose):
			print "Begin Simulation"

		Level = self.GetLevel(Node)
		# Perform simulation.
		while(not(game.IsTerminal(CurrentState))):
			CurrentState = game.GetNextState(CurrentState)
			Level += 1.0
			if(self.verbose):
				print "CurrentState:", game.GetStateRepresentation(CurrentState)

		#--- Game specific ---#
		Result = 100.0 / len(CurrentState.bins)
		# if(game.CheckStateInterference(CurrentState)):
		# 	Result = 0.0
		# else:
		# 	#avgLen = 0.0
		# 	#for Table in CurrentState.tables:
		# 	#	avgLen += len(Table)
		# 	#avgLen /= len(CurrentState.tables)
		# 	1000.0 / len(CurrentState.tables) + 1000.0/(len(CurrentState.peopleIDs) + 1)

		if(self.verbose):
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
			CurrentNode.ressq += Result**2
			CurrentNode.visits += 1

		self.root.wins += Result

	def HasParent(self, Node):
		if(Node.parent == None):
			return False
		else:
			return True

	def EvalUTC(self, Node):
		#c = np.sqrt(2)
		c = 0.1
		w = Node.wins
		n = Node.visits
		sumsq = Node.ressq
		if(Node.parent == None):
			t = Node.visits
		else:
			t = Node.parent.visits

		UTC = w/n + c * np.sqrt(np.log(t)/n)
		D = 1000.
		Correction = np.sqrt((sumsq - n * (w/n)**2 + D)/n)
		Node.sputc = UTC + Correction
		return Node.sputc

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
		# for i in Node.state.bins: # game specific (scrap)
		# 	string += str(i) + ", "
		string += str(game.GetStateRepresentation(Node.state))
		string += "], W: " + str(Node.wins) + ", N: " + str(Node.visits) + ", UTC: " + str(Node.sputc) + ") \n"
		file.write(string)

		for Child in Node.children:
			self.PrintNode(file, Child, Indent, self.IsTerminal(Child))

	def Run(self, MaxIter = 30000):
		for i in range(MaxIter):
			if(self.verbose):
				print "\n===== Begin iteration:", i, "====="
			X = self.Selection()
			Y = self.Expansion(X)
			if(Y):
				Result = self.Simulation(Y)
				self.Backpropagation(Y, Result)
			else:
				#--- Game specific ---#
				Result = 100.0 / len(X.state.bins)
				# if(game.CheckStateInterference(X.state)):
				# 	Result = 0.0
				# else:
				# 	#avgLen = 0.0
				# 	#for Table in CurrentState.tables:
				# 	#	avgLen += len(Table)
				# 	#avgLen /= len(CurrentState.tables)
				# 	Result = 1000.0 / len(CurrentState.tables) + 1000.0/(len(CurrentState.peopleIDs) + 1)# + 10.0 * avgLen

				if(self.verbose):
					print "Result: ", Result
				self.Backpropagation(X, Result)
