def pairFurtilityNodes(nodeType):
    """
        function that generates a map tying the old furtility nodes to the new ones

        @param nodeType: string representing the type of nodes to pair
        @return: dictionary mapping the old verlet solvers to the new ones
    """
    # fetch all the furtility nodes of a certain type using a custom function
    nodeList = getFurtilityNodes(nodeType)
    nodePairDict = {}

    for node in nodeList:
        # go over the nodes and find the original ones
        if '_nHair' not in node:
            nodePairDict[node]  = ''

    for nodeA in nodeList:
        if '_nHair_' in nodeA:
            newName = nodeA.replace('_nHair', '')
            for nodeB in nodePairDict:
                # compare the stripped version of the one in the list to the current item in the dictionary
                if newName == nodeB:
                    nodePairDict[nodeB] = nodeA
