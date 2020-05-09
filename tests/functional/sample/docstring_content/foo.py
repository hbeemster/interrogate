"""Sample module-level docs"""


class Foo(object):
    """Foo class"""

    def method_without_arguments(self):
        """this method should score 2"""
        pass

    def method_with_arguments_no_match(self, param1, param2):
        """this method should score 0"""
        pass

    def method_with_arguments_partial_match(self, param1, param2):
        """this method should score 1

        param1: Lorem ipsum dolor sit amet
        """
        pass

    def method_with_arguments_full_match(self, param1, param2):
        """this method should score 2

        param1: Lorem ipsum dolor sit amet
        param1: Curabitur pellentesque felis augue
        """
        pass

