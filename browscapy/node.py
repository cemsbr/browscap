"""Node used to search for patterns."""
from typing import List, Tuple


class Node:
    """Full browscap pattern or partial with children.

    Attributes:
        pattern (str): Partial browscap pattern, excluding parent's and
            children's.
        children (List[Node]): Children nodes.

    """

    def __init__(self, pattern: str) -> None:
        """Build a node from a browscap pattern string."""
        self.pattern = pattern
        self.children: List[Node] = []

    def add_node(self, node: 'Node') -> 'Node':
        """Add a new node to the tree."""
        prefix_len, parent = self.get_parent(node)
        if node.pattern == parent.pattern:
            raise ValueError("Can't add nodes with the same pattern: "
                             f'"{node.pattern}".')
        parent.add_child(node, prefix_len)
        return self

    def add_child(self, child: 'Node', prefix_len: int) -> None:
        """Add a child as one of this node's children, in place.

        You should probably use :meth:`add_node` so the new node can be a
        grandchild for example.

        This node (self) can be modified to become a parent with a sub-pattern
        of the current one.
        """
        # If the new pattern starts with self.pattern, add a child
        if prefix_len == len(self.pattern):
            self.children.append(child)
        else:  # Create a parent node with common prefix (may be empty)
            # A copy of self will be a child
            self_as_child = Node(self.pattern)
            self_as_child.children = self.children
            # self becomes the parent with two children
            self.pattern = self.pattern[:prefix_len]
            # Create a new list because current one is with a child
            self.children = [self_as_child, child]

    def get_parent(self, node: 'Node') -> Tuple[int, 'Node']:
        """Return the parent Node for a browscap pattern.

        Search in this node and in all children. The parent is the one that
        has more characters in common from the beginning of the pattern.

        Returns:
            int, Node: Maximum number of characters in common from the
                beginning of the pattern and the Node.

        """
        # Get the best result from all children
        children_results = (c.get_parent(node) for c in self.children)
        # Compare only the child_length in key param.
        child_length, child_node = max(children_results, key=lambda x: x[0],
                                       default=(0, None))

        # Return best child or self
        this_length = self._get_common_prefix_len(node)
        if child_length > this_length:
            return child_length, child_node
        return this_length, self

    def _get_common_prefix_len(self, node: 'Node') -> int:
        """Return the common prefix length."""
        length = 0
        for char1, char2 in zip(self.pattern, node.pattern):
            if char1 != char2:
                break
            length += 1
        return length
