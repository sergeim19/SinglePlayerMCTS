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




