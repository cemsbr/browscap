"""Tree to search information about a given user agent.

The tree is built to allow a quick search. It is good enough to build a tree
with the following properties:

- A child has a longer pattern;
- Sibling nodes have different patterns.
- For each browscap pattern, there's one, and only one, FullPattern node
storing its information;
- Other nodes can be created when two browscap patterns have a common prefix.
Their type is PartialPattern;

The properties above allow a fast search by descending the only sibling
having a substring of the new node's patterns.
"""
from abc import ABC, abstractmethod
from typing import List, Union, cast

from .database import Database
from .properties import Properties

# pylint: disable=invalid-name
# Due to list invariance.
NodeList = List[Union['Node', 'PartialPattern', 'FullPattern']]
# pylint: enable=invalid-name


class SearchResult:
    """Store the best result while searching a new node's parent.

    The class variables prevent sending parameters in several calls, including
    recursive ones. As we don't use multiple threads or process, this is safe.
    """

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

    def sort_children(self) -> None:
        """Sort children by :attr:`Node.max_length`, desc."""
        for child in self.children:
            if child.children:
                child.sort_children()
        self.children.sort(key=lambda x: x.max_length, reverse=True)


class Node(Parent):
    """A Node contains a pattern and others nodes as children."""

    def __init__(self, pattern: str, children: NodeList = None) -> None:
        """Assign pattern and optional children."""
        super().__init__(children)
        self.pattern = pattern
        self.max_length: int = 0

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

    def calc_max_length(self) -> int:
        """Calculate the largest pattern that is reachable from this node."""
        if self.children:
            self.max_length = max(child.calc_max_length()
                                  for child in self.children)
        else:
            self.max_length = self.get_pattern_length()
        return self.max_length

    def get_pattern_length(self) -> int:
        """Count characters excluding "*" and "?"."""
        return sum(1 for char in self.pattern if char not in ('*', '?'))


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

    @property
    def properties(self) -> Properties:
        """Return properties from database."""
        return cast(Properties, Database.dictionary[self.pattern])

    @properties.setter
    def properties(self, value: Properties) -> None:
        """Store properties in database."""
        Database.dictionary[self.pattern] = value

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
            self._create_partial_pattern(child, parent)

    def _create_partial_pattern(self, child: 'FullPattern', parent: Parent) \
            -> None:
        """Create partial pattern as a parent node with the common chars."""
        common_prefix = child.pattern[:SearchResult.score]
        children: NodeList = [self, child]
        partial_pattern = PartialPattern(common_prefix, children)
        # Replace self by the new PartialPattern
        parent.children.remove(self)
        parent.children.append(partial_pattern)


class PartialPattern(Node):
    """Partial browscap pattern in common with children."""

    def add_child(self, child: FullPattern, parent: Parent) -> None:
        """Add a child node. If patterns are equal, create a FullPattern.

        When this partial node's pattern and child's are the same, this node
        is replaced by FullPattern node.
        """
        # Assume that child's pattern size >= self's
        if SearchResult.score == len(self.pattern):
            if len(child.pattern) == len(self.pattern):
                self._become_full_pattern(child, parent)
            else:  # > (child has a suffix)
                self.children.append(child)
        else:  # New PartialPattern
            self._split_pattern(child)

    def _become_full_pattern(self, full_pattern: FullPattern,
                             parent: Parent) -> None:
        """Make this PartialPattern a FullPattern.

        Add self's children to full_pattern, then replace self with
        full_pattern in the parent children list.
        """
        full_pattern.children.extend(self.children)
        parent.children.remove(self)
        parent.children.append(full_pattern)

    def _split_pattern(self, full_pattern: FullPattern) -> None:
        """Create a new PartialPattern parent with a smaller pattern size.

        This node will be the parent and its copy and full_pattern, the
        children.
        """
        self_copy = PartialPattern(self.pattern, self.children)
        smaller_prefix = self.pattern[:SearchResult.score]
        self.pattern = smaller_prefix
        self.children = [self_copy, full_pattern]


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

    def optimize(self) -> None:
        """Sort children by the highest length."""
        self._calc_max_length()
        self.sort_children()

    def _calc_max_length(self) -> None:
        """Find largest pattern that is reachable from this node."""
        for child in self.children:
            child.calc_max_length()
