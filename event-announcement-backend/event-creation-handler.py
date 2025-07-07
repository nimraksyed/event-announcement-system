import json
import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize SNS client
    sns = boto3.client('sns')

    # Get SNS topic ARN from environment variable
    topic_arn = os.environ['SNS_TOPIC_ARN']

    try:
        # Parse request body
        if event.get('body'):
            body = json.loads(event['body'])
        else:
            body = event

        event_name = body.get('eventName')
        event_description = body.get('eventDescription')
        event_date = body.get('eventDate')

        if not all([event_name, event_description, event_date]):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'error': 'All event fields are required (eventName, eventDescription, eventDate)'
                })
            }

        # Create notification message
        message = f"""
🎉 New Event Alert! 🎉

Event: {event_name}
Description: {event_description}
Date: {event_date}

Don't miss out on this exciting event!

---
This is an automated notification from the Event System.
        """.strip()

        # Create subject
        subject = f"New Event: {event_name}"
        
        print("Publishing message to SNS...")
        print("SNS Topic ARN:", topic_arn)
        print("Subject:", subject)
        print("Message:", message)

        # Publish to SNS topic
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )

        print("SNS publish response:", response)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'message': 'Event created and notifications sent successfully!',
                'messageId': response['MessageId'],
                'event': {
                    'name': event_name,
                    'description': event_description,
                    'date': event_date,
                    'created_at': datetime.now().isoformat()
                }
            })
        }

    except ClientError as e:
        print(f"AWS Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'error': 'Failed to create event or send notifications'
            })
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }
