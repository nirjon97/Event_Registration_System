                                                                        Event Registration System
                                                                ---------------------------------------------


Brief project description and purpose.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python (3.x)
- Django
- Django Rest Framework
- Postman (for testing APIs)

### Installing

1. Clone the repository:
   git clone https://github.com/yourusername/yourproject.git

2. Install dependencies:
   use command : pip install -r requirements.txt

3. Run migrations:
   use command : python manage.py migrate

4. Create a superuser for accessing the Django admin panel:
   use command : python manage.py createsuperuser
   Follow the prompts to create a superuser account.

5. Run the development server:
   use command : python manage.py runserver

The project should now be running at http://127.0.0.1:8000/.


API Endpoints
-------------------
List of all events:

Endpoint: http://127.0.0.1:8000/api/events/
Method: GET
Details of a specific event:

Endpoint: http://127.0.0.1:8000/api/events/<event_id>/
Method: GET
User registration for an event:

Endpoint: http://127.0.0.1:8000/api/events/<event_id>/register/
Method: POST
Requires authentication
User's registered events:

Endpoint: http://127.0.0.1:8000/api/user/registered-events/
Method: GET
Requires authentication
Testing with Postman
Open Postman.

Create a new request for each endpoint.

Specify the request details, authentication, and body (if required).

Click "Send" to test the endpoint.
