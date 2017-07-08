#------------------------------------------------------------------------#
#
# Written by sergeim19 (Created June 21, 2017)
# https://github.com/sergeim19/
# Last Modified July 7, 2017
#
# Description:
# Single Player Monte Carlo Tree Search implementation.
# This is a Python implementation of the single player
# Monte Carlo tree search as described in the paper:
# https://dke.maastrichtuniversity.nl/m.winands/documents/CGSameGame.pdf
#
#------------------------------------------------------------------------#

import Node as nd
import numpy as np
import BinPackingGame as game

#------------------------------------------------------------------------#
# Class for Single Player Monte Carlo Tree Search implementation.
#------------------------------------------------------------------------#
class MCTS:

	#-----------------------------------------------------------------------#
	# Description: Constructor.
	# Node 	  - Root node of the tree of class Node.
	# Verbose - True: Print details of search during execution.
	# 			False: Otherwise
	#-----------------------------------------------------------------------#
	def __init__(self, Node, Verbose = False):
		self.root = Node
		self.verbose = Verbose

	#-----------------------------------------------------------------------#
	# Description: Performs selection phase of the MCTS.
	#-----------------------------------------------------------------------#
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
			print "\nSelected: ", game.GetStateRepresentation(SelectedChild.state)

		return SelectedChild

	#-----------------------------------------------------------------------#
	# Description:
	#	Given a Node, selects the first unvisited child Node, or if all
	# 	children are visited, selects the Node with greatest UTC value.
	# Node	- Node from which to select child Node from.
	#-----------------------------------------------------------------------#
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

	#-----------------------------------------------------------------------#
	# Description: Performs expansion phase of the MCTS.
	# Leaf	- Leaf Node to expand.
	#-----------------------------------------------------------------------#
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

	#-----------------------------------------------------------------------#
	# Description: Checks if a Node is terminal (it has no more children).
	# Node	- Node to check.
	#-----------------------------------------------------------------------#
	def IsTerminal(self, Node):
		# Evaluate if node is terminal.
		if(game.IsTerminal(Node.state)):
			return True
		else:
			return False
		return False # Why is this here?

	#-----------------------------------------------------------------------#
	# Description:
	#	Evaluates all the possible children states given a Node state
	#	and returns the possible children Nodes.
	# Node	- Node from which to evaluate children.
	#-----------------------------------------------------------------------#
 	def EvalChildren(self, Node):
 		NextStates = game.EvalNextStates(Node.state)
 		Children = []
 		for State in NextStates:
 			ChildNode = nd.Node(State)
 			Children.append(ChildNode)

		return Children

	#-----------------------------------------------------------------------#
	# Description:
	#	Selects a child node randomly.
	# Node	- Node from which to select a random child.
	#-----------------------------------------------------------------------#
	def SelectChildNode(self, Node):
		# Randomly selects a child node.
		Len = len(Node.children)
		assert Len > 0, "Incorrect length"
		i = np.random.randint(0, Len)
		return Node.children[i]

	#-----------------------------------------------------------------------#
	# Description:
	#	Performs the simulation phase of the MCTS.
	# Node	- Node from which to perform simulation.
	#-----------------------------------------------------------------------#
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

		#--- Result: Game specific ---#
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

	#-----------------------------------------------------------------------#
	# Description:
	#	Performs the backpropagation phase of the MCTS.
	# Node		- Node from which to perform Backpropagation.
	# Result	- Result of the simulation performed at Node.
	#-----------------------------------------------------------------------#
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

	#-----------------------------------------------------------------------#
	# Description:
	#	Checks if Node has a parent..
	# Node - Node to check.
	#-----------------------------------------------------------------------#
	def HasParent(self, Node):
		if(Node.parent == None):
			return False
		else:
			return True

	#-----------------------------------------------------------------------#
	# Description:
	#	Evaluates the Single Player modified UTC. See:
	#	https://dke.maastrichtuniversity.nl/m.winands/documents/CGSameGame.pdf
	# Node - Node to evaluate.
	#-----------------------------------------------------------------------#
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
		Modification = np.sqrt((sumsq - n * (w/n)**2 + D)/n)
		Node.sputc = UTC + Modification
		return Node.sputc

	#-----------------------------------------------------------------------#
	# Description:
	#	Gets the level of the node in the tree.
	# Node - Node to evaluate the level.
	#-----------------------------------------------------------------------#
	def GetLevel(self, Node):
		Level = 0.0
		while(Node.parent):
			Level += 1.0
			Node = Node.parent
		return Level

	#-----------------------------------------------------------------------#
	# Description:
	#	Prints the tree to file.
	#-----------------------------------------------------------------------#
	def PrintTree(self):
		f = open('Tree.txt', 'w')
		Node = self.root
		self.PrintNode(f, Node, "", False)
		f.close()

	#-----------------------------------------------------------------------#
	# Description:
	#	Prints the tree Node and its details to file.
	# Node			- Node to print.
	# Indent		- Indent character.
	# IsTerminal	- True: Node is terminal. False: Otherwise.
	#-----------------------------------------------------------------------#
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

	#-----------------------------------------------------------------------#
	# Description:
	#	Runs the SP-MCTS.
	# MaxIter	- Maximum iterations to run the search algorithm.
	#-----------------------------------------------------------------------#
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
				#--- Result: Game specific ---#
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
