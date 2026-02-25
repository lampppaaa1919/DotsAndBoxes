class Node:
    def __init__(self, value, children=None):
        if children is None:
            children = []
        self.value = value
        self.children = children
        # self.left = None
        # self.right = None


# Initializing Nodes to None
def root(v):
    return Node(v)

def new_node(v, parent):
    temp = Node(v)
    parent.children.append(temp)
    return temp


# Getting expectimax
def expectimax(node, is_max):
    # Condition for Terminal node
    if len(node.children) == 0:
        return node.value

    # Maximizer node. Chooses the max from the
    # left and right subtrees
    if is_max:
        max_val = node.children[0].value
        for child in node.children:
            max_val = max(max_val, expectimax(child, False))
        # return max(expectimax(node.left, False), expectimax(node.right, False))
        return max_val

    # Chance node. Returns the average of
    # the left and right subtrees
    else:
        # return (expectimax(node.left, True) + expectimax(node.right, True)) / 2
        sum_nodes = 0
        for child in node.children:
            sum_nodes += expectimax(child, True)
        return sum_nodes / len(node.children)


# Driver code
if __name__ == '__main__':
    # Non leaf nodes.
    # If search is limited
    # to a given depth,
    # their values are
    # taken as heuristic value.
    # But because the entire tree
    # is searched their
    # values don't matter
    root = root(0)
    child1 = new_node(0,root)
    for v in [10,20,30]:
        new_node(v, child1)
    child2 = new_node(0,root)
    for v in [5,10,15]:
        new_node(v, child2)
    child3 = new_node(0,root)
    for v in [20,20,25]:
        new_node(v, child3)
    child4 = new_node(0,root)
    for v in [40,48]:
        new_node(v, child4)

    res = expectimax(root,True)
    # root.left = new_node(0)
    # root.right = new_node(0)

    # Assigning values to Leaf nodes
    # root.left.left = new_node(10)
    # root.left.right = new_node(10)
    # root.right.left = new_node(9)
    # root.right.right = new_node(100)

    # res = expectimax(root, True)
    print("Expectimax value is " + str(res))