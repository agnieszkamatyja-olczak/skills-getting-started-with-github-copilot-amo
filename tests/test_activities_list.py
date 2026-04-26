"""Tests for the activities list endpoint (GET /activities)

Tests retrieving all available activities from the API.
"""

import pytest


class TestActivitiesListEndpoint:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_returns_dict(self, client, fresh_activities_state):
        """Should return all activities as a dictionary
        
        ARRANGE: Set up fresh activities state
        ACT: Make GET request to /activities
        ASSERT: Verify response is dict with correct format
        """
        # ARRANGE
        # (fresh_activities_state fixture provides setup)

        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)

    def test_get_activities_contains_all_activities(self, client, fresh_activities_state):
        """Should return all 9 activities
        
        ARRANGE: Set up fresh activities state
        ACT: Make GET request to /activities
        ASSERT: Verify all activity names are present
        """
        # ARRANGE
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Swimming Club",
            "Art Studio",
            "Drama Club",
            "Science Olympiad",
            "Debate Team"
        ]

        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        assert len(activities) == 9
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_activity_has_required_fields(self, client, fresh_activities_state):
        """Each activity should have description, schedule, max_participants, and participants
        
        ARRANGE: Set up fresh activities state
        ACT: Make GET request to /activities
        ASSERT: Verify structure of activity data
        """
        # ARRANGE
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"

    def test_participants_list_is_array(self, client, fresh_activities_state):
        """Each activity's participants should be a list
        
        ARRANGE: Set up fresh activities state
        ACT: Make GET request to /activities
        ASSERT: Verify participants field is a list for each activity
        """
        # ARRANGE
        # (no setup needed)

        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"

    def test_chess_club_has_initial_participants(self, client, fresh_activities_state):
        """Chess Club should have 2 initial participants
        
        ARRANGE: Set up fresh activities state
        ACT: Make GET request to /activities
        ASSERT: Verify Chess Club has expected participants
        """
        # ARRANGE
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) == 2
        for email in expected_participants:
            assert email in chess_club["participants"]
