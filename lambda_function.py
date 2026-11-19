import boto3
import os

rekognition = boto3.client('rekognition')
sns = boto3.client('sns')

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

ALERT_LABELS = [
    'Weapon', 'Gun', 'Rifle', 'Pistol', 'Knife',
    'Violence', 'Fighting', 'Explosion', 'Fire'
]
CONFIDENCE_THRESHOLD = 75


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f'Scanning image: {key} in bucket: {bucket}')

    # Detect weapon / object labels
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MinConfidence=CONFIDENCE_THRESHOLD
    )

    # Detect moderation / violent content
    moderation_response = rekognition.detect_moderation_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MinConfidence=CONFIDENCE_THRESHOLD
    )

    detected_labels = [
        f"{label['Name']} ({label['Confidence']:.1f}%)"
        for label in response['Labels']
        if label['Name'] in ALERT_LABELS
    ]

    detected_moderation = [
        f"{label['Name']} ({label['Confidence']:.1f}%)"
        for label in moderation_response['ModerationLabels']
    ]

    all_detected = detected_labels + detected_moderation

    if all_detected:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='Rekognition Weapons/Violence Alert',
            Message=f'ALERT\nImage: {key}\nDetected: {all_detected}'
        )

    return {'statusCode': 200, 'detected': all_detected}
