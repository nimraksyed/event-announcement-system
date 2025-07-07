# System Architecture: Event Announcement System

This document describes the architecture of the Event Announcement System, which enables users to subscribe via email and receive automated notifications when new events are created. The system is built using AWS serverless services which ensure scalability, low maintenance, and cost-efficiency!

## Architecture Flow

Frontend(HTML + CSS + JS on S3) --> API Gateway --> Lambda Functions(2) --> Amazon SNS --> Email Notifications

---

## Components

### 1. **Frontend**
- **Technology:** HTML, CSS, JavaScript
- **Hosted on:** AWS S3 (Static Website Hosting)
- **Purpose:** 
  - UI for users to enter their email
  - UI for admins to create events

---

### 2. **API Gateway**
- **Type:** REST API
- **Endpoints:**
  - `POST /subscribe` → triggers email subscription Lambda
  - `POST /create-event` → triggers event creation Lambda

---

### 3. **Lambda Functions**
#### a. `event-subscription-handler.py`
- Subscribes user email to an SNS Topic using `sns.subscribe`
- Validates email input

#### b. `event-creation-handler.py`
- Accepts event info (title, description, date & time)
- Publishes formatted message to SNS Topic

---

### 4. **Amazon SNS**
- **Topic:** `event_announcement_topic`
- **Subscribers:** Email addresses submitted by users
- **Functionality:** Sends out broadcast notifications when a new event is created

---

### 5. **IAM Roles**
- Grants Lambda functions permission to:
  - Call `sns.subscribe` and `sns.publish`
  - Log to CloudWatch

---

## Security & Permissions
- **CORS:** Enabled for cross-origin requests from the frontend
- **IAM Policies:** Scoped only to necessary actions on SNS and logging

---

## Potential Future Enhancements

- Store created events in DynamoDB for history/logs
- Add SMS support via SNS
- Add Admin authentication for event creation
- Use EventBridge for scheduled reminder notifications
