"""
main.py

This is the entry point for the Event Announcement System.
The core backend logic is implemented in the 'event-announcement-backend' directory using Python.
This file serves as a reference point for backend coordination and deployment.
"""
from event_announcement_backend.event_subscription_handler import lambda_handler as subscribe
from event_announcement_backend.event_creation_handler import lambda_handler as create

# Sample event stubs
if __name__ == "__main__":
    test_subscribe_event = {"body": '{"email": "test@example.com"}'}
    test_create_event = {"body": '{"title": "Test", "description": "Testing", "datetime": "Tomorrow"}'}

    print(subscribe(test_subscribe_event, None))
    print(create(test_create_event, None))
