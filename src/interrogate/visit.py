# Copyright 2020 Lynn Root
"""AST traversal for finding docstrings."""

import ast
import os

import attr


@attr.s(eq=False)
class CovNode:
    """Coverage of an AST Node.

    :param str name: Name of node (module, class, method or function
        names).
    :param str path: Pseudo-import path to node (i.e. ``sample.py:
        MyClass.my_method``).
    :param int level: Level of recursiveness/indentation
    :param int lineno: Line number of class, method, or function.
    :param bool covered: Has a docstring
    :param bool perc_function_quality_score: Quality of the docstring
    :param str node_type: type of node (e.g "module", "class", or
        "function").
    """

    name = attr.ib()
    path = attr.ib()
    level = attr.ib()
    lineno = attr.ib()
    covered = attr.ib()
    # perc_function_quality_score = attr.ib()
    node_type = attr.ib()


class CoverageVisitor(ast.NodeVisitor):
    """NodeVisitor for a Python file to find docstrings.

    :param str filename: filename to parse coverage.
    :param config.InterrogateConfig config: configuration.
    """

    def __init__(self, filename, config):
        self.filename = filename
        self.stack = []
        self.nodes = []
        self.config = config

    @staticmethod
    def _has_doc(node):
        """Return if node has docstrings."""
        return (
            ast.get_docstring(node) is not None
            and ast.get_docstring(node).strip() != ""
        )

    @staticmethod
    def _function_quality_score(node):
        """Return Quality score of the docstring.

        0: not match between docstring and signature
        1: partial match between docstring and signature
        2: full match between docstring and signature
        """
        if not CoverageVisitor._has_doc(node):
            return 0


        return CoverageVisitor._visit_arguments(node)

        # # test for args
        # # function
        # if not node.args.args:
        #     return 2
        # # class method
        # elif node.args.args and len(node.args.args) == 1 and node.args.args[0].arg == "self":
        #     return 2
        # else:
        #     return 0

    @staticmethod
    def _visit_arguments(node):
        scores = 0
        # if hasattr(node, 'posonlyargs') and node.posonlyargs:
        #     node.posonlyargs = [CoverageVisitor._visit_arg(a) for a in node.posonlyargs]

        if node.args:
            scores = sum(CoverageVisitor._visit_arg(a, ast.get_docstring(node)) for a in node.args.args)

        # if hasattr(node, 'kwonlyargs') and node.kwonlyargs:
        #     node.kwonlyargs = [CoverageVisitor._visit_arg(a) for a in node.kwonlyargs]
        #
        # if hasattr(node, 'varargannotation'):
        #     node.varargannotation = None
        # else:
        #     if node.vararg:
        #         node.vararg = CoverageVisitor._visit_arg(node.vararg)
        #
        # if hasattr(node, 'kwargannotation'):
        #     node.kwargannotation = None
        # else:
        #     if node.kwarg:
        #         node.kwarg = CoverageVisitor._visit_arg(node.kwarg)

        return scores

    def _visit_arg(node, docstring):
        """get score"""
        # node.annotation = None
        if node.arg == "self":
            return 2
        elif node.arg in docstring:
            return 2
        else:
            return 0

    def _visit_helper(self, node):
        """Recursively visit AST node for docstrings."""
        if not hasattr(node, "name"):
            node_name = os.path.basename(self.filename)
        else:
            node_name = node.name

        parent = None
        path = node_name

        if self.stack:
            parent = self.stack[-1]
            parent_path = parent.path
            if parent_path.endswith(".py"):
                path = parent_path + ":" + node_name
            else:
                path = parent_path + "." + node_name

        lineno = None
        if hasattr(node, "lineno"):
            lineno = node.lineno
        cov_node = CovNode(
            name=node_name,
            path=path,
            covered=self._has_doc(node),
            level=len(self.stack),
            node_type=type(node).__name__,
            lineno=lineno,
        )
        if cov_node.node_type == "FunctionDef" and cov_node.covered:
            cov_node.function_quality_score = self._function_quality_score(node)


        self.stack.append(cov_node)
        self.nodes.append(cov_node)

        self.generic_visit(node)

        self.stack.pop()

    def _is_private(self, node):
        """Is node private (i.e. __MyClass, __my_func)."""
        if node.name.endswith("__"):
            return False
        if not node.name.startswith("__"):
            return False
        return True

    def _is_semiprivate(self, node):
        """Is node semiprivate (i.e. _MyClass, _my_func)."""
        if node.name.endswith("__"):
            return False
        if node.name.startswith("__"):
            return False
        if not node.name.startswith("_"):
            return False
        return True

    def _is_ignored_common(self, node):
        """Commonly-shared ignore checkers."""
        is_private = self._is_private(node)
        is_semiprivate = self._is_semiprivate(node)

        if self.config.ignore_private and is_private:
            return True
        if self.config.ignore_semiprivate and is_semiprivate:
            return True

        if self.config.ignore_regex:
            for regexp in self.config.ignore_regex:
                regex_result = regexp.match(node.name)
                if regex_result:
                    return True
        return False

    def _is_func_ignored(self, node):
        """Should the AST visitor ignore this func/method node."""
        is_init = node.name == "__init__"
        is_magic = all(
            [
                node.name.startswith("__"),
                node.name.endswith("__"),
                node.name != "__init__",
            ]
        )

        if self.config.ignore_init_method and is_init:
            return True
        if self.config.ignore_magic and is_magic:
            return True
        return self._is_ignored_common(node)

    def _is_class_ignored(self, node):
        """Should the AST visitor ignore this class node."""
        return self._is_ignored_common(node)

    def visit_Module(self, node):
        """Visit module for docstrings.

        :param ast.Module node: a module AST node.
        """
        self._visit_helper(node)

    def visit_ClassDef(self, node):
        """Visit class for docstrings.

        :param ast.ClassDef node: a class AST node.
        """
        if self._is_class_ignored(node):
            return
        self._visit_helper(node)

    def visit_FunctionDef(self, node):
        """Visit function or method for docstrings.

        :param ast.FunctionDef node: a function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function or method for docstrings.

        :param ast.AsyncFunctionDef node: a async function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)
