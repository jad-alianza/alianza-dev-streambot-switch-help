import logging
import os
import random
import shutil
import string
from datetime import datetime, timedelta

import allure
from behave import use_step_matcher  # type:ignore
from behave.runner import Context  # type:ignore
from data_tests_lib.behave_tests.environment import _initialise_sdk
from data_tests_lib.behave_tests.utilities.tests_resources_utilities import _clear_scenario_aws_resources, _clear_stale_resources

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
use_step_matcher("re")

AQA_PREFIX = "temp-aqa-lab"
AQA_ATHENA_DB_PREFIX = "q2_aqa_test"
AQA_S3_BUCKET = "alz-datalake-q2"
AQA_S3_TEMP_BUCKET = "temp-aqa-lab"
USE_SUFFIX = True
DELETE_TEST_RESOURCES = True
TEMP_DIR = "/tmp/behave_tests/"


class Placeholder:
    """Placeholder class for storing entities in context."""


def before_all(context):  # noqa:unused-function
    """Test suite prerequisites.

    :param: context: Behave context object.
    """
    _initialise_sdk(context)
    if DELETE_TEST_RESOURCES:
        _clear_stale_resources(context, days_to_keep=1)


def before_scenario(context: Context, _):  # noqa:unused-function
    """Prerequisites for each scenario.

    :param: context: Behave context object.
    """
    if os.path.exists(TEMP_DIR):
        if DELETE_TEST_RESOURCES:
            shutil.rmtree(TEMP_DIR)
            os.makedirs(TEMP_DIR)
    else:
        os.makedirs(TEMP_DIR)
    today_date = datetime.now().strftime("%Y%m%d")
    suffix = "".join(random.sample(string.ascii_lowercase, 5))
    context.scenario.athena_db_prefix = AQA_ATHENA_DB_PREFIX
    context.scenario.suffix = f"_{today_date}_{suffix}" if USE_SUFFIX else f"_{today_date}"
    context.scenario.athena_output_location = f"{context.scenario.athena_db_prefix}{context.scenario.suffix}"
    context.scenario.unique_key_value = context.scenario.athena_output_location

    context.scenario.test_resources = {}
    for resources_type in ["athena", "sns", "sqs", "s3", "secrets"]:
        context.scenario.test_resources[resources_type] = []
    context.sdk.athena_adapter.location_base = f"{AQA_PREFIX}{context.scenario.suffix}"
    context.scenario.test_resources["s3"].append({"bucket_name": AQA_S3_BUCKET, "object_path": f"{AQA_PREFIX}{context.scenario.suffix}/"})
    today_date = datetime.utcnow()
    yesterday = today_date - timedelta(days=1)
    week_ago = today_date - timedelta(days=7)
    context.scenario.yesterday_iso = yesterday.strftime("%Y-%m-%d")
    context.scenario.yesterday_year = yesterday.strftime("%Y")
    context.scenario.yesterday_month = yesterday.strftime("%m")
    context.scenario.yesterday_day = yesterday.strftime("%d")
    context.scenario.today_iso = today_date.strftime("%Y-%m-%d")
    context.scenario.today_year = today_date.strftime("%Y")
    context.scenario.today_month = today_date.strftime("%m")
    context.scenario.today_day = today_date.strftime("%d")
    context.scenario.week_ago_iso = week_ago.strftime("%Y-%m-%d")
    context.scenario.week_ago_digits = week_ago.strftime("%Y%m%d")


def after_scenario(context, _):
    if DELETE_TEST_RESOURCES:
        _clear_scenario_aws_resources(context)
    log_capture = context.log_capture.getvalue()
    context.log_capture.flush()
    if log_capture:
        allure.attach(log_capture, name="log_capture", attachment_type=allure.attachment_type.TEXT)


def after_all(context):
    if DELETE_TEST_RESOURCES:
        _clear_stale_resources(context, days_to_keep=1)
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
