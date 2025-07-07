import boto3
import os
import json

def lambda_handler(event, context):
    sns = boto3.client('sns')
    topic_arn = os.environ['SNS_TOPIC_ARN']

    try:
        print("EVENT RECEIVED:", json.dumps(event))

        # Case 1: Body is under event['body'] as a string (typical with API Gateway proxy integration)
        # Case 2: Body is directly at top level of event (e.g. when using test event or direct integration)

        # Try extracting email from 'body' field if it exists
        if 'body' in event:
            try:
                body = json.loads(event['body'])
            except Exception:
                body = {}
        else:
            # Assume whole event is the body
            body = event

        email = body.get('email')
        print("Subscribing email:", email)

        if not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Email address is required'})
            }

        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email,
            ReturnSubscriptionArn=True
        )

        print("SNS Subscribe Response:", response)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Subscription initiated. Check your email to confirm.',
                'subscriptionArn': response.get('SubscriptionArn', 'Pending confirmation')
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
