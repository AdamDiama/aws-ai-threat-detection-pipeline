# AWS Rekognition Alert System — Serverless Image Threat Detection
Fully automated image scanning pipeline on AWS. Detects weapons and violent content using Amazon Rekognition AI and sends instant email alerts via SNS. Fully serverless — responds in under 10 seconds.

Group project — ATU Sligo, Cloud Computing (Year 2, Semester 2) — Graded 77%

Group: Adam Diamantidis (S00270094), Thomas McNabola, Colin Stewart Jr

How it works
Image Upload → S3 → Lambda → Rekognition → SNS → Email Alert
Image uploaded to S3 bucket fires an event
Lambda (Python 3.12) runs automatically — calls DetectLabels + DetectModerationLabels
If threat found above 75% confidence → SNS publishes email alert instantly
No servers, no polling, no cron — pure event-driven, auto-scales to 1,000 parallel uploads
Monitored: Weapon, Gun, Rifle, Pistol, Knife, Violence, Fighting, Explosion, Fire — threshold 75%

Results
✅ Tested on 30 sample images
✅ Alerts delivered in under 10 seconds from upload
✅ Verified end-to-end in CloudWatch logs (Scanning image: ..., ALERT SENT)
Services used
Service	Name	Role
S3	rekognition-alert-images (eu-west-1)	Storage + event trigger on PUT
Lambda	rekognition-alert (Python 3.12)	Analysis brain, serverless
Rekognition	DetectLabels + DetectModerationLabels	AI vision, no training needed
SNS	rekognition-alerts	Email alerts (confirmed subscription)
IAM	lambda-rekognition-role	Least-privilege: Rekognition + SNS + S3 read + basic execution
CloudWatch	Lambda Logs	Monitoring + debugging
Quick setup
S3: Create bucket rekognition-alert-images (eu-west-1, Block Public Access ON)
SNS: Create Standard topic rekognition-alerts → Create email subscription → confirm link in inbox
IAM: Create role lambda-rekognition-role (trusted: Lambda) + attach AmazonRekognitionFullAccess, AmazonSNSFullAccess, AmazonS3ReadOnlyAccess, AWSLambdaBasicExecutionRole
Lambda: Create function rekognition-alert, Python 3.12, use existing role lambda-rekognition-role → paste lambda_function.py → Deploy
Env var: Configuration → Environment variables → add SNS_TOPIC_ARN = your topic ARN
Trigger: Configuration → Triggers → Add S3 trigger → bucket rekognition-alert-images, all object create events
Test: Upload knife.jpg + safe image → check Monitor → CloudWatch Logs for Scanning image: line
See lambda_function.py for the full function — reads ARN from env var, no hardcoded secrets.

Issues we hit (real-world lessons)
IAM permissions — default Lambda role has no Rekognition/SNS access → fixed with custom least-privilege role
SCP block — college AWS org applied a Service Control Policy blocking rekognition:*. Custom IAM policies can't override SCPs — only org admins can. Documented as enterprise cloud governance example.
Concepts covered: event-driven architecture, serverless scaling, AI-as-a-Service, IAM vs SCPs, config-driven infrastructure.

Files
lambda_function.py — S3-triggered Lambda function (Python 3.12)
docs/ — full step-by-step build guide PDF (put your Word doc here as PDF
