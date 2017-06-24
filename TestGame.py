import Node as nd
import numpy as np
import MCTS

RootState = np.array([1.,1.,1.,1.])
Root = nd.Node(RootState)

x = MCTS.MCTS(Root)
x.Run()
