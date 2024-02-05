# import copy
# import json
# import os
# import sys
# import unittest
# from unittest.mock import MagicMock, Mock, patch
#
# from data_tests_lib.tests.base_snapshotter_lambda_tests import EXPECTED_QUERIES_TEMPLATE, BaseSnapshotterLambdaTests, _adjust_date_string
# from streaming_lib.utils.structural import Struct
#
# import lambdas.daily_snapshotter_lambda
#
# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#
# TEST_ENV = "d2"
# TESTS_DIR = os.path.dirname(__file__)
# TESTS_DATA_DIR = f"{TESTS_DIR}/snapshotter_tests_data"
# TEST_UUID = "74cdf772-fb3d-4598-84db-4dd413783949"
#
# TEST_PROJECT = "test_project"
# TEST_ENTITY = "foo_bar"
# TEST_RAW_DATABASE = f"{TEST_ENV}_{TEST_PROJECT}_raw"
# TEST_STREAM_DATABASE = f"{TEST_ENV}_{TEST_PROJECT}_stream"
# TEST_SNAP_DATABASE = f"{TEST_ENV}_{TEST_PROJECT}_snap"
# TEST_SNAP_BUCKET = f"{TEST_ENV}-datalake-layer3-snap-us-east-2"
# TEST_SNAP_PREFIX = f"snap/projection/{TEST_PROJECT}"
# TEST_ATHENA_S3_LOCATION = f"s3://athena-misc-{TEST_ENV}/streaming_{TEST_PROJECT}"
#
# all_cols = "LIST COLUMNS HERE"
# delete_cols = ", _delete.col, _delete.type" if "_delete" in all_cols else ""
# final_query_template = """
# COPY AND UPDATE table.projection_sql from lambdas/daily_snapshotter_lambda.py
# """  # noqa
#
#
# final_table_query = (
#     final_query_template.replace("{start_date}", "{yesterday_iso}")
#     .replace("{end_date}", "{yesterday_iso}")
#     .replace("{extra_stream_cols}", "")
#     .replace("{extra_snap_cols}", "")
# )
# final_view_query = (
#     final_query_template.replace("{start_date}", "{today_iso}")
#     .replace("{end_date}", "{tomorrow_iso}")
#     .replace("{extra_stream_cols}", ", _year, _month, _day, 'stream' as _source")
#     .replace("{extra_snap_cols}", ", _year, _month, _day, 'snap' as _source")
# )
#
# athena_mock = Mock(name="athena_mock")
# with open(f"{TESTS_DATA_DIR}/input/test_fetch_stream_tables.json") as f:
#     athena_mock.list_table_metadata = Mock(return_value=json.load(f))
# with open(f"{TESTS_DATA_DIR}/input/athena_query_start.json") as f:
#     athena_mock.start_query_execution = Mock(return_value=json.load(f))
#
# s3_mock = MagicMock(name="s3mock")
#
#
# def boto_session_mock(client_type, **kwargs):
#     return athena_mock if client_type == "athena" else s3_mock
#
#
# @patch.dict(
#     "os.environ",
#     {
#         "ENVIRONMENT_TYPE": TEST_ENV,
#         "STREAM_DATABASE": TEST_STREAM_DATABASE,
#         "SNAP_DATABASE": TEST_SNAP_DATABASE,
#         "SNAP_BUCKET": TEST_SNAP_BUCKET,
#         "SNAP_PREFIX": TEST_SNAP_PREFIX,
#         "SNAP_TABLES": TEST_ENTITY,
#         "SNAP_DUMP_FULL_SQL": "true",
#         "SNAP_DRY_RUN": "false",
#         "ATHENA_RESULTS_LOCATION": TEST_ATHENA_S3_LOCATION,
#     },
# )
# @patch("boto3.Session.client", name="boto_session_mock", side_effect=boto_session_mock)
# @patch("random.randint", return_value=0.1)
# @patch("uuid.uuid1", return_value=TEST_UUID)
# class SnapshotterLambdaTests(BaseSnapshotterLambdaTests):
#     def setUp(self) -> None:
#         super().setUp()
#         self.context = Struct.make({"aws_request_id": "9e7840f7-3750-4623-ad69-16718bf6f5c2"})
#         self.project = TEST_PROJECT
#         self.entity = TEST_ENTITY
#         self.raw_database = TEST_RAW_DATABASE
#         self.stream_database = TEST_STREAM_DATABASE
#         self.snap_database = TEST_SNAP_DATABASE
#         self.athena_s3_location = TEST_ATHENA_S3_LOCATION
#         self.test_uuid = TEST_UUID
#         self.athena_mock = athena_mock
#         self.athena_mock.reset_mock()
#         self.test_lambda_class = lambdas.daily_snapshotter_lambda.DailySnapshotter
#         self.test_data_dir = f"{TESTS_DIR}/snapshotter_tests_data"
#
#     def _prepare_expected_queries(self):
#         expected_queries = copy.deepcopy(EXPECTED_QUERIES_TEMPLATE)
#         expected_queries["prepare_snap_table"] = expected_queries["prepare_snap_table"].replace("{all_cols}", all_cols)
#         expected_queries["lookup_sys_columns"] = expected_queries["lookup_sys_columns"].replace("{delete_cols}", delete_cols)
#         expected_queries["execute_ctas_snap"] = expected_queries["execute_ctas_snap"].replace("{final_table_query}", final_table_query)
#         expected_queries["add_realtime_view_create"] = expected_queries["add_realtime_view_create"].replace("{final_view_query}", final_view_query)
#         self.expected_queries = {
#             k: _adjust_date_string(v.replace("{table_name}", self.entity).replace("{schema_name}", self.project), date=self.test_date)
#             for k, v in expected_queries.items()
#         }
#
#
# del BaseSnapshotterLambdaTests
#
# if __name__ == "__main__":
#     unittest.main()
