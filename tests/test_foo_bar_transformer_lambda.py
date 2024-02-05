# import os
# import unittest
#
# from data_tests_lib.tests.base_transformer_lambda_tests import BaseTransformerLambdasTests
# from streaming_lib.utils.structural import Struct
#
# from lambdas import foo_bar_transformer_lambda
#
# TESTS_DIR = os.path.dirname(__file__)
# TESTS_DATA_DIR = "foo_bar_transformer_lambda_tests_data"
#
#
# class FooBarTransformerLambdasTests(BaseTransformerLambdasTests):
#     def setUp(self) -> None:
#         self.maxDiff = None
#         self.context = Struct.make({"aws_request_id": "9e7840f7-3750-4623-ad69-16718bf6f5c2"})
#         self.test_data_dir = f"{TESTS_DIR}/foo_bar_transformer_lambda_tests_data"
#         self.test_lambda_handler = foo_bar_transformer_lambda.lambda_handler
#         self.test_lambda_class = foo_bar_transformer_lambda.FooBarTransformer
#
#
# del BaseTransformerLambdasTests
#
# if __name__ == "__main__":
#     unittest.main()
