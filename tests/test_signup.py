"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)

Tests signing up students for activities.
"""

import pytest


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful_new_student(self, client, fresh_activities_state):
        """Student should be able to sign up for an activity
        
        ARRANGE: Set up fresh activities state with an available activity
        ACT: Make POST request to signup endpoint with new email
        ASSERT: Verify success response and participant is added
        """
        # ARRANGE
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, fresh_activities_state):
        """After signup, the student should appear in participants list
        
        ARRANGE: Set up fresh activities state, get initial count
        ACT: Sign up new student and fetch activities
        ASSERT: Verify participant count increased by 1
        """
        # ARRANGE
        activity_name = "Programming Class"
        new_email = "newstudent@mergington.edu"
        initial_response = client.get("/activities")
        initial_participants = len(initial_response.json()[activity_name]["participants"])

        # ACT
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]

        # ASSERT
        assert signup_response.status_code == 200
        assert len(final_participants) == initial_participants + 1
        assert new_email in final_participants

    def test_signup_activity_not_found(self, client, fresh_activities_state):
        """Should return 404 when activity doesn't exist
        
        ARRANGE: Set up fresh activities state with non-existent activity
        ACT: Make POST request to signup for non-existent activity
        ASSERT: Verify 404 error and appropriate message
        """
        # ARRANGE
        non_existent_activity = "Non-existent Club"
        email = "student@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{non_existent_activity}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student_error(self, client, fresh_activities_state):
        """Should return 400 when student already signed up for activity
        
        ARRANGE: Set up fresh activities state with existing participant
        ACT: Try to signup student who is already enrolled
        ASSERT: Verify 400 error and appropriate message
        """
        # ARRANGE
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # ASSERT
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_different_activities_same_student(self, client, fresh_activities_state):
        """Student can sign up for multiple different activities
        
        ARRANGE: Set up fresh activities state with new student email
        ACT: Sign up same student for two different activities
        ASSERT: Verify student is added to both activities
        """
        # ARRANGE
        new_email = "freestudent@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # ACT
        response1 = client.post(f"/activities/{activity1}/signup", params={"email": new_email})
        response2 = client.post(f"/activities/{activity2}/signup", params={"email": new_email})
        
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert new_email in activities[activity1]["participants"]
        assert new_email in activities[activity2]["participants"]

    def test_signup_returns_correct_message_format(self, client, fresh_activities_state):
        """Signup response should have proper message format
        
        ARRANGE: Set up fresh activities state with new email
        ACT: Make POST request to signup endpoint
        ASSERT: Verify message format contains email and activity name
        """
        # ARRANGE
        activity_name = "Gym Class"
        new_email = "athlete@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        message = data["message"]
        assert "Signed up" in message or "Signed" in message
        assert new_email in message
        assert activity_name in message
