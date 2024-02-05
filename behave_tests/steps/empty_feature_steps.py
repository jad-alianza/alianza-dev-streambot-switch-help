import os

from data_tests_lib.behave_tests.steps.common_steps import *  # pylint: disable=unused-wildcard-import
from data_tests_lib.behave_tests.steps.streaming_steps import *  # pylint: disable=unused-wildcard-import

AQA_PREFIX = "temp-aqa-lab"
AQA_ATHENA_DB_PREFIX = "q2_aqa_test"
AQA_S3_BUCKET = "alz-datalake-q2"
TESTS_DIR = os.path.dirname(__file__)
TESTS_DATA_DIR = f"{TESTS_DIR}/../testdata"
TEMP_DIR = "/tmp/behave_tests/"
RECREATE_RESOURCES = True
INSERT_TEST_DATA = False
RUN_LAMBDA = True
