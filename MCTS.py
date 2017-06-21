import Node as nd

class MCTS:
	def __init__(self, Node):
		self.root = Node

	def Selection(self):		
		MaxWeight = 0
		Weight = 0
		Index = 0
		HasChild = False
		if(len(self.root.children) > 0):
			HasChild = True

		i = 0
		# Temporary. Select children with biggest weights.
		while(HasChild):
			Weight = self.root.children[i].weight

			if(Weight > MaxWeight):
				MaxWeight = Weight			
				Index = i

			i += 1

		return self.root.children[Index]




