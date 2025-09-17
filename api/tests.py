# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import TaskManager

# User = get_user_model()


# class TaskManagerAPITest(APITestCase):
#     def setUp(self):
#         # Create a test user with email
#         self.user = User.objects.create_user(
#             email="testuser@example.com",
#             username="testuser",  # still required by AbstractUser
#             password="testpass123"
#         )

#         self.client = APIClient()

#         # Generate JWT token
#         refresh = RefreshToken.for_user(self.user)
#         self.access_token = str(refresh.access_token)

#         # Authenticate with JWT
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

#         # Create a sample task
#         self.task = TaskManager.objects.create(
#             title="Test Task",
#             description="This is a test task",
#             completed=False
#         )

#     def test_get_all_tasks(self):
#         response = self.client.get("/api/tasks/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.data), 1)

#     def test_create_task(self):
#         data = {"title": "New Task", "description": "Task created via test", "completed": False}
#         response = self.client.post("/api/tasks/", data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["title"], "New Task")

#     def test_get_single_task(self):
#         response = self.client.get(f"/api/task_details/?task_id={self.task.id}")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["title"], "Test Task")

#     def test_update_task(self):
#         data = {"completed": True}
#         response = self.client.put(f"/api/task_details/?task_id={self.task.id}", data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["completed"], True)

#     def test_delete_task(self):
#         response = self.client.delete(f"/api/task_details/?task_id={self.task.id}")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(TaskManager.objects.filter(id=self.task.id).exists())

#     def test_task_not_found(self):
#         response = self.client.get("/api/task_details/?task_id=999")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["error"], "Task not found")

#     def test_delete_without_task_id(self):
#         response = self.client.delete("/api/task_details/")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data["error"], "Please provide task id")



from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TaskManager

User = get_user_model()


class TaskManagerAPITest(APITestCase):
    def setUp(self):
        # Create a test user with email
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",  # still required by AbstractUser
            password="testpass123"
        )

        self.client = APIClient()

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Authenticate with JWT
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Create a sample task (linked to user)
        self.task = TaskManager.objects.create(
            title="Test Task",
            description="This is a test task",
            completed=False,
            user=self.user
        )

    def test_get_all_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Since pagination is enabled, results are in response.data["results"]
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "Task created via test",
            "completed": False,
            "user": self.user.id  # required since TaskManager has user FK
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")
        self.assertEqual(response.data["user"], self.user.id)

    def test_get_single_task(self):
        response = self.client.get(f"/api/task_details/?task_id={self.task.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task")

    def test_update_task(self):
        data = {"completed": True, "user": self.user.id}
        response = self.client.put(f"/api/task_details/?task_id={self.task.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed"], True)

    def test_delete_task(self):
        response = self.client.delete(f"/api/task_details/?task_id={self.task.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TaskManager.objects.filter(id=self.task.id).exists())

    def test_task_not_found(self):
        response = self.client.get("/api/task_details/?task_id=999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Task not found")

    def test_delete_without_task_id(self):
        self.user.is_staff = True  # ensure it gets past IsAdminToDelete
        self.user.save()
        response = self.client.delete("/api/task_details/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Please provide task id")


