
class LegoTreeNode (object):
    def __init__(self, tirp):
        self.tirp = tirp
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_max_depth(self):
        if len(self.nodes) == 0:
            if self.tirp is None:
                return 0
            else:
                return 1
        _max = 0
        for node in self.nodes:
            depth = node.get_max_depth()
            if depth > _max:
                _max = depth
        return _max + 1

    def get_all_leafs(self):
        leafs = []
        if len(self.nodes) == 0:
            if self.tirp is not None:
                leafs.append(self)
        else:
            for node in self.nodes:
                leafs.extend(node.get_all_leafs())
        return leafs
