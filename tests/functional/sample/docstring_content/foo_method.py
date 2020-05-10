"""Class with methods only"""


class FooMethod(object):
    """FooMethod class, expected total score : 2.333, percentage: 100 * 2.333 / 4 = 58.3%"""

    def method_without_arguments(self):
        """this method should score 1.0"""
        pass

    def method_with_arguments_without_match(self, param1, param2, param3):
        """this method should score 0.0"""
        pass

    def method_with_arguments_with_partial_match(self, param1, param2, param3):
        """this method should score 0.333

        param1: Lorem ipsum dolor sit amet
        """
        pass

    def method_with_arguments_with_full_match(self, param1, param2, param3):
        """this method should score 1.0

        param1: Lorem ipsum dolor sit amet
        param2: Curabitur pellentesque felis augue
        param3: Vivamus at fringilla tortor
        """
        pass
