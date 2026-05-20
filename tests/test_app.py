import copy

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
}


def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


class TestApp:
    def setup_method(self):
        reset_activities()

    def test_get_activities(self):
        response = client.get("/activities")
        assert response.status_code == 200
        payload = response.json()
        assert "Chess Club" in payload
        assert payload["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert payload["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]

    def test_signup_activity(self):
        email = "newstudent@mergington.edu"
        response = client.post("/activities/Chess Club/signup", params={"email": email})
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for Chess Club"}
        assert email in app_module.activities["Chess Club"]["participants"]

    def test_remove_participant(self):
        email = "michael@mergington.edu"
        response = client.delete("/activities/Chess Club/participants", params={"email": email})
        assert response.status_code == 200
        assert response.json() == {"message": f"Removed {email} from Chess Club"}
        assert email not in app_module.activities["Chess Club"]["participants"]

    def test_signup_unknown_activity(self):
        response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_remove_unknown_participant(self):
        response = client.delete("/activities/Chess Club/participants", params={"email": "missing@mergington.edu"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
