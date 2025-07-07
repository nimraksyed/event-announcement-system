# Deployment Guide: Event Announcement System

This guide walks through deploying the Event Announcement System using AWS services — including S3, Lambda, API Gateway, and SNS. This system allows users to subscribe via email and receive notifications when new events are created.

---

## 1. Frontend Deployment: S3 Static Website Hosting

### Step 1: Prepare Your Frontend Files

Ensure the following files are organized under your frontend folder (e.g., `event-announcement-frontend`):
- `index.html`
- `script.js`
- `styles.css`
- `events.json` (optional)

---

### Step 2: Create an S3 Bucket

1. Navigate to the [AWS S3 Console](https://s3.console.aws.amazon.com/s3).
2. Click **Create bucket**.
3. Enter a globally unique name like `event-announcement-frontend`.
4. Under **Object Ownership**, select “ACLs disabled”.
5. Uncheck **Block all public access**.
6. Enable **Bucket Versioning** and **Bucket Key**.
7. Click **Create bucket**.

---

### Step 3: Upload Files to S3

1. Open the created bucket.
2. Click **Upload** → **Add files** → Select your frontend files.
3. Click **Upload**.

---

### Step 4: Enable Static Website Hosting

1. Go to the **Properties** tab of your S3 bucket.
2. Scroll to **Static Website Hosting**, click **Edit**.
3. Select **Enable**.
4. Enter `index.html` as the **Index document**.
5. Save changes.
6. Copy the **Website endpoint URL** — this is your public frontend URL.

---

### Step 5: Set Public Bucket Policy

1. Go to the **Permissions** tab → **Bucket Policy**.
2. Add this policy (replace `your-bucket-name` with your actual bucket name):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

---

## 2. Backend Deployment: Lambda + API Gateway + SNS

### Step 1: Create SNS Topic

1. Go to **Amazon SNS**.
2. Create a topic named `event_announcement_topic`.
3. Copy the Topic ARN.

---

### Step 2: Create Lambda Functions

1. Create two Lambda functions:  
   - `event-subscription-handler`  
     - Subscribes email to the SNS topic  
     - Use the provided Python code  
     - Set the `SNS_TOPIC_ARN` as an environment variable  
   - `event-creation-handler`  
     - Publishes new event notifications to the SNS topic  
     - Uses `sns.publish`  

> Note: Both functions must have a basic Lambda execution role and permissions to interact with SNS like `sns:subscribe`, `sns:publish`, etc.

---

### Step 3: API Gateway Integration

1. Create a REST API using API Gateway.
2. Create two resources:  
   - `/subscribe` (Method: POST → Integration: `event-subscription-handler`)  
   - `/create-event` (Method: POST → Integration: `event-creation-handler`)
3. Enable CORS on both methods.
4. Deploy the API (e.g., Stage: Prod).
5. Copy the Invoke URL.

---

### Step 4: Connect the Backend and Frontend Together

1. In your `script.js` file, do this:

```js
const API_BASE_URL = 'https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod';
```

> Replace the placeholder with your real API Gateway base URL.
