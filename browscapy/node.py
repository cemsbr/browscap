"""Node used to search for patterns."""
from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from .properties import Properties

# pylint: disable=invalid-name
# Due to list invariance.
NodeList = List[Union['Node', 'PartialPattern', 'FullPattern']]
SearchResult = Tuple[int, 'Node', NodeList]
# pylint: enable=invalid-name


class Node(ABC):
    """A Node contains a pattern and a children list."""

    def __init__(self, pattern: str, children: NodeList = None) -> None:
        """Initialize children."""
        self.pattern = pattern
        self.children = children or []

    @abstractmethod
    def add_child(self, child: 'FullPattern', common_length: int) -> 'Node':
        """Add a child as one of this node's children and return result.

        You should probably use :meth:`add_node` so the new node can be a
        grandchild for example.
        """
        pass  # pragma: no cover

    def find_parent(self, node: 'Node', siblings: NodeList,
                    partial_score: int = -1) -> SearchResult:
        """Return the proper parent Node for a new node.

        Recursive search that returns the best match for this subtree (self as
        its root node). The best match has the most characters in common (from
        the beginning, consecutive) and, as a second criteria, it's the
        shortest string (closer to the root).

        Args:
            node (Node): The orphan node.
            siblings (List[Node]): Siblings of self, at least 1. This method
                does not modify it. The siblings will be manipulated by the
                caller.
            partial_score (int): Default is -1. Number of characters in common
                with the parent.

        Returns:
            int, Node, List[Node]: The best result of this subtree: score
                (number of characters in common with the parent), parent,
                siblings including the parent.

        """
        start_index = 0 if partial_score == -1 else partial_score
        self_score = self._get_common_length(node.pattern, start_index)

        if self_score == partial_score:
            # We can't get better because suffix has nothing in common.
            return 0, None, None  # Ignore this subtree, including self.

        self_result = self_score, self, siblings
        if not self.children:
            return self_result

        return self._compare_with_children(node, self_result)

    def _compare_with_children(self, node: 'Node', self_result: SearchResult) \
            -> SearchResult:
        self_score = self_result[0]

        children_result: SearchResult = (self_score, None, None)
        for child in self.children:
            if len(child.pattern) > children_result[0]:
                result = child.find_parent(node, self.children, self_score)
                if result[0] > children_result[0]:
                    children_result = result

        if children_result[0] > self_score:
            return children_result  # Found a child with a higher score
        return self_result          # return self_score

    def _get_common_length(self, pattern: str, start: int) -> int:
        """Return the length of the longest common prefix."""
        length = 0
        for char1, char2 in zip(self.pattern[start:], pattern[start:]):
            if char1 != char2:
                break
            length += 1
        return length + start


class FullPattern(Node):
    """Browscap pattern and properties.

    Attributes:
        properties (Properties): Browscap properties.
        children (List[Node]): Children nodes.
        pattern (str): Browscap pattern.

    """

    def __init__(self, properties: Properties) -> None:
        """Build a node from a browscap pattern string."""
        self.properties = properties
        super().__init__(self.properties.PropertyName)

    def add_child(self, child: 'FullPattern', common_length: int) \
            -> Node:
        """Return a partial pattern with both child and self as children."""
        if child.pattern == self.pattern:
            msg = f'Can\'t add nodes with the same pattern "{child.pattern}"'
            raise ValueError(msg)

        if common_length == len(self.pattern):
            # Only possible case: child.pattern = self.pattern + a suffix
            self.children.append(child)
            return self

        # Create partial pattern as a parent node
        pattern = self.pattern[:common_length]
        children: NodeList = [self, child]
        return PartialPattern(pattern, children)


class PartialPattern(Node):
    """Partial browscap pattern in common with children."""

    def add_child(self, child: FullPattern, common_length: int) -> Node:
        """Add a child node."""
        # We already know that child.pattern >= self.pattern (there's an
        # assertion for that).
        if len(child.pattern) > len(self.pattern):
            self.children.append(child)
            return self
        # Same pattern. This partial pattern becomes a full one.
        return self._to_full_pattern(child)

    def _to_full_pattern(self, full_pattern: FullPattern) -> FullPattern:
        """Return a full pattern from this partial pattern.

        Reuse node by adding :attr:`children` to it.
        """
        full_pattern.children.extend(self.children)
        return full_pattern


class Tree:
    """Store nodes to match user agents. In other words, the root node."""

    def __init__(self):
        """Initialize an empty list of children."""
        self.children: NodeList = []

    def add_node(self, node: FullPattern) -> None:
        """Add a new node."""
        if not self.children:
            self.children.append(node)
        else:
            self._add_to_children(node)

    def _add_to_children(self, node: FullPattern) -> None:
        """Add node to the proper existent node."""
        common_length, parent, parents = self.find_parent(node)
        new_parent = parent.add_child(node, common_length)
        if new_parent is not parent:    # PartialPattern became FullPattern
            parents.remove(parent)      # Remove the PartialPattern node
            parents.append(new_parent)  # Add the new FullPattern node

    def find_parent(self, node: Node) -> SearchResult:
        """Find the proper parent for a new node."""
        results = (child.find_parent(node, self.children)
                   for child in self.children)
        return max(results, key=lambda x: x[0])
