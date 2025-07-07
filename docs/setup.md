# Setup Instructions: Event Announcement System

This guide walks through how to deploy and configure the Event Announcement System on AWS.

---

## 🛠️ Prerequisites

- AWS Account with full access to:
  - Lambda
  - API Gateway
  - SNS
  - S3
  - IAM
- AWS CLI configured (optional but recommended)
- Basic knowledge of Python, HTML, JS, and AWS console

---

## 🚀 Deployment Steps

### 1. **Frontend Hosting on S3**
- Go to **S3 > Create Bucket**
- Enable **Static Website Hosting**
- Upload files from `event-announcement-frontend/`
- Set index document to `index.html`
- Make bucket content public (or configure CloudFront for production)

---

### 2. **Create SNS Topic**
- Go to **SNS > Create topic**
- Type: `Standard`
- Name: `event_announcement_topic`
- Copy the Topic ARN for later use

---

### 3. **Deploy Lambda Functions**
Deploy both:
- `event-subscription-handler.py`
- `event-creation-handler.py`

For each:
- Go to **Lambda > Create function**
- Use Python 3.9
- Paste the code or upload a `.zip`
- Set environment variable:
  - `SNS_TOPIC_ARN = <your_topic_arn_here>`
- Give it an IAM Role with SNS publish/subscribe permissions

---

### 4. **Set Up API Gateway**
- Go to **API Gateway > Create API > HTTP API**
- Add two routes:
  - `POST /subscribe` → Link to `event-subscription-handler`
  - `POST /create-event` → Link to `event-creation-handler`
- Enable **CORS**
- Deploy and note the endpoint URL

---

### 5. **Connect Frontend to API**
- Update the API endpoint URL in your `script.js` file:
  ```js
  const SUBSCRIBE_URL = 'https://your-api-id.amazonaws.com/subscribe';
  const CREATE_EVENT_URL = 'https://your-api-id.amazonaws.com/create-event';
