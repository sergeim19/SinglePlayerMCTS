import Node as nd
import numpy as np
import MCTS
import BinPackingGame as game

items = [4.0, 8.0, 5.0, 1.0, 7.0, 6.0, 1.0, 4.0, 2.0, 2.0]
Bins = [[]]
RootState = game.State(items, Bins)
Root = nd.Node(RootState)

x = MCTS.MCTS(Root, True)
x.Run()
