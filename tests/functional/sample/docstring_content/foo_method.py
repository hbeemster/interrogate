"""Class with methods only"""


class FooMethod(object):
    """FooMethod class, expected mean score in percentage: 5 / 4 = 80"""

    def method_without_arguments(self):
        """this method should score 2"""
        pass

    def method_with_arguments_without_match(self, param1, param2):
        """this method should score 0"""
        pass

    def method_with_arguments_with_partial_match(self, param1, param2):
        """this method should score 1

        param1: Lorem ipsum dolor sit amet
        """
        pass

    def method_with_arguments_with_full_match(self, param1, param2):
        """this method should score 2

        param1: Lorem ipsum dolor sit amet
        param1: Curabitur pellentesque felis augue
        """
        pass
