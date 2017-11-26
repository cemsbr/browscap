"""Node used to search for patterns."""
from abc import ABC, abstractmethod
from typing import List, Union

from .properties import Properties

# pylint: disable=invalid-name
# Due to list invariance.
NodeList = List[Union['Node', 'PartialPattern', 'FullPattern']]
# pylint: enable=invalid-name


class SearchResult:
    """Store the best result while searching a new node's parent."""

    #: int: Number of characters in common since the pattern beginning.
    score: int
    #: Parent: The proper parent for a new node.
    parent: 'Parent'
    #: Parent: The grandparent of the new node.
    grandparent: 'Parent'

    @classmethod
    def reset(cls, parent: 'Parent') -> None:
        """Prepare for a search."""
        cls.parent = parent
        cls.grandparent = None
        cls.score = 0

    @classmethod
    def update(cls, extra_score: int, parent: 'Node', grandparent: 'Parent') \
            -> None:
        """Update a result."""
        cls.score += extra_score
        cls.parent, cls.grandparent = parent, grandparent


class Parent(ABC):
    """Have a Node list as children."""

    def __init__(self, children: NodeList = None) -> None:
        """Initialize children."""
        self.children = children or []

    @abstractmethod
    def add_child(self, child: 'FullPattern', parent: 'Parent') -> None:
        """Add a child as one of this node's children.

        You should probably use :meth:`add_node` so the new node can be a
        grandchild for example.
        """
        pass  # pragma: no cover

    def find_parent(self, node: 'Node') -> None:
        """Return the proper parent Node for a new node.

        Recursively search for the node's parent. The best match has the most
        characters in common (from the beginning, consecutive) and, as a second
        criteria, it's the shortest string (closer to the root).
        """
        for child in self.children:
            extra_score: int = child.get_score(node.pattern)
            if extra_score > 0:
                SearchResult.update(extra_score, child, self)
                SearchResult.parent.find_parent(node)
                break


class Node(Parent):
    """A Node contains a pattern and others nodes as children."""

    def __init__(self, pattern: str, children: NodeList = None) -> None:
        """Assign pattern and optional children."""
        super().__init__(children)
        self.pattern = pattern

    @abstractmethod
    def add_child(self, child: 'FullPattern', parent: Parent) -> None:
        """Add a child as one of this node's children and return result.

        You should probably use :meth:`add_node` so the new node can be a
        grandchild for example. Use this method when you are sure this is the
        proper parent for the child.
        """
        pass  # pragma: no cover

    def get_score(self, pattern: str) -> int:
        """Return the increase in the number of common characters."""
        length = 0
        start = SearchResult.score
        for char1, char2 in zip(self.pattern[start:], pattern[start:]):
            if char1 != char2:
                break
            length += 1
        return length


class FullPattern(Node):
    """Browscap pattern and properties.

    Attributes:
        properties (Properties): Browscap properties.
        children (List[Node]): Children nodes.
        pattern (str): Browscap pattern.

    """

    def __init__(self, properties: Properties) -> None:
        """Build a node from a browscap pattern string."""
        super().__init__(properties.PropertyName)
        self.properties = properties

    def add_child(self, child: 'FullPattern', parent: Parent) -> None:
        """Add the child. May create a new PartialPattern node.

        For example, when a pattern 'ab' is added to pattern 'ac', a new
        PartialPattern 'a' will contain 'ab' and 'ac' as children.
        """
        if child.pattern == self.pattern:
            msg = f'Can\'t add nodes with the same pattern "{child.pattern}"'
            raise ValueError(msg)
        # From now on, patterns are different

        if SearchResult.score == len(self.pattern):
            # Self's pattern is contained in child's, so we add a new child.
            self.children.append(child)
        else:  # They have a non-empty difference
            # Create partial pattern as a parent node with the common chars.
            common_prefix = child.pattern[:SearchResult.score]
            children: NodeList = [self, child]
            new_child = PartialPattern(common_prefix, children)
            # Self will go down one generation
            parent.children.remove(self)
            parent.children.append(new_child)


class PartialPattern(Node):
    """Partial browscap pattern in common with children."""

    def add_child(self, child: FullPattern, parent: Parent) -> None:
        """Add a child node. If patterns are equal, create a FullPattern.

        When this partial node's pattern and child's are the same, this node
        is replaced by FullPattern node.
        """
        # Assume that child's pattern size >= self's
        if len(child.pattern) > len(self.pattern):
            self.children.append(child)
        else:  # Same pattern. Replace this partial pattern by a full one.
            # The FullPattern is the child with self's children
            child.children.extend(self.children)
            parent.children.remove(self)
            parent.children.append(child)


class Tree(Parent):
    """Store nodes to match user agents. In other words, the root node."""

    def add_node(self, node: FullPattern) -> None:
        """Search for the proper parent and add node as its child."""
        SearchResult.reset(parent=self)
        self.find_parent(node)
        SearchResult.parent.add_child(node, SearchResult.grandparent)

    def add_child(self, child: Node, parent: Parent) -> None:
        """Append child to children list."""
        self.children.append(child)
