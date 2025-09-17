Running Tests

Your Task Manager API includes unit tests for all endpoints. Follow these steps to run them:

1. Activate the virtual environment
source tmvenv/bin/activate   # Linux/macOS
# or
tmvenv\Scripts\activate     # Windows

2. Run all tests
python manage.py test

Django will create a temporary test database, run all test cases, and then destroy the test database.

Expected output for passing tests:
.......
Ran 7 tests in 6.652s
OK
Destroying test database for alias 'default'...

3. Run tests for a specific app
python manage.py test api

4. Run a specific test class or method
# All tests in TaskManagerAPITest
python manage.py test api.tests.TaskManagerAPITest

# Only a specific test method
python manage.py test api.tests.TaskManagerAPITest.test_create_task
