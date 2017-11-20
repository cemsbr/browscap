"""Node used to search for patterns."""
from typing import List, Tuple


class Node:
    """Full browscap pattern or partial with children.

    Attributes:
        pattern (str): Partial browscap pattern, excluding parent's and
            children's.
        children (List[Node]): Children nodes.
        is_pattern (bool): True (default) if this node is a complete browscap
            pattern or False if it is just a partial pattern created to add
            children with a common pattern prefix.

    """

    def __init__(self, pattern: str) -> None:
        """Build a node from a browscap pattern string."""
        self.pattern = pattern
        self.children: List[Node] = []
        self.is_pattern = True

    def add_node(self, node: 'Node') -> None:
        """Add a new node to the tree."""
        prefix_len, parent = self.get_parent(node)
        if node.pattern == parent.pattern:
            if parent.is_pattern:
                raise ValueError("Can't add nodes with the same pattern: "
                                 f'"{node.pattern}".')
            else:
                parent.is_pattern = True
        parent.add_child(node, prefix_len)

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
            self_as_child = self._copy()
            # self becomes the parent with two children
            self.pattern = self.pattern[:prefix_len]
            self.is_pattern = False
            # Create a new list because current one is with a child
            self.children = [self_as_child, child]

    def _copy(self) -> 'Node':
        """Return a shallow copy of self."""
        node = Node(self.pattern)
        node.children = self.children
        node.is_pattern = self.is_pattern
        return node

    def get_parent(self, node: 'Node', parent_match: int = 0) \
            -> Tuple[int, 'Node']:
        """Return the parent Node for a browscap pattern.

        Search in this node and in all children. The parent is the one that
        has more characters in common from the beginning of the pattern.

        Args:
            node (Node): The orphan node.
            parent_match (int): How many chars were matched in the parent. If
                we can't match any other character, do not even search through
                children. This improves performance a lot.

        Returns:
            int, Node: Maximum number of characters in common from the
                beginning of the pattern and the Node.

        """
        # For performance reasons, search through as less children as possible
        self_length = self._get_common_prefix_len(node)
        # No need to check children when:
        # - There's no children; or
        # - Self is not root (root has empty pattern) and we couldn't match any
        #   other character than self's parent.
        if not self.children or (self.pattern and self_length <= parent_match):
            return self_length, self

        # Get the best result from all children
        children_results = (child.get_parent(node, self_length)
                            for child in self.children)
        # Compare only the child_length in key param.
        child_length, child_node = max(children_results, key=lambda x: x[0])

        # Return best child or self
        if child_length > self_length:
            return child_length, child_node
        return self_length, self

    def _get_common_prefix_len(self, node: 'Node') -> int:
        """Compare two browscap patterns and return common prefix length."""
        length = 0
        for char1, char2 in zip(self.pattern, node.pattern):
            if char1 != char2:
                break
            length += 1
        return length
