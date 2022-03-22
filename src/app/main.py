'''module for the lambda handler'''

import os
from datetime import datetime

import boto3

from .scraper import get_tournaments, TournamentQueryType

sns_client = boto3.client('sns')


def lambda_handler(event, context):
    '''method as the entry point for the lambda function'''

    print(event)
    print(context)

    topic_arn = os.getenv("SC2_TOURNAMENT_NOTIFIER_TOPIC_ARN")
    today = datetime.now().date()

    # get tournaments Upcoming and Ongoing
    tournaments = get_tournaments([TournamentQueryType.UPCOMING,
                                   TournamentQueryType.ONGOING])
    tournaments_to_notify = {}

    try:
        # for every tournament, check if start day is today to create a notification
        for tournament_query_type_item in tournaments.items():
            for tournament_link_item in tournament_query_type_item[1].items():
                if tournament_link_item[1]['date_from'] == today:
                    tournaments_to_notify[tournament_link_item[0]
                                          ] = tournament_link_item[1]

        # send notification to the SNS Topic
        notification_message = ''
        for tournaments_to_notify_item in tournaments_to_notify.items():
            notification_message += f"Tournament: {tournaments_to_notify_item[0]}, From: {tournaments_to_notify_item[1]['date_from']}, To: {tournaments_to_notify_item[1]['date_to']}\n\n"

        if notification_message != '':
            sns_client.publish(TopicArn=topic_arn, Message=notification_message,
                               Subject='New SC2 Tournament Notification')

            print(
                f'Notification sent to topic: {topic_arn} with content: {notification_message}')

        print(today)
        print(tournaments_to_notify)
        return {
            "statusCode": 200,
            "body": {
                "message": "Done"
            }
        }
    except Exception as ex:
        return {
            "statusCode": 500,
            "body": {
                "message": str(ex)
            }
        }
