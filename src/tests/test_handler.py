'''module for main handler testing'''

import os

from unittest import mock
import pytest

from src.app.main import lambda_handler

NOTIFICATION_TOPIC_ARN = "arn:aws:sns:us-east-1:170177254108:sc2-tournaments-notifier-topic"


@pytest.fixture(name="cloudwatch_scheduler_event")
def fixture_cloudwatch_scheduler_event():
    '''function to create a sample cloudwatch scheduler event'''
    return {}


def test_lambda_handler(cloudwatch_scheduler_event):
    '''test for the lambda handler function'''

    with mock.patch.dict(os.environ, {"SC2_TOURNAMENT_NOTIFIER_TOPIC_ARN": NOTIFICATION_TOPIC_ARN}):
        ret = lambda_handler(cloudwatch_scheduler_event, "")

        assert ret["statusCode"] == 200
