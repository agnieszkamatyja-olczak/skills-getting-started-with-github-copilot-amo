"""Tests for the remove participant endpoint (DELETE /activities/{activity_name}/participants/{email})

Tests removing students from activities.
"""

import pytest


class TestRemoveParticipantEndpoint:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_remove_participant_successful(self, client, fresh_activities_state):
        """Should successfully remove an existing participant from an activity
        
        ARRANGE: Set up fresh activities state with existing participant
        ACT: Make DELETE request to remove known participant
        ASSERT: Verify success response and participant is removed
        """
        # ARRANGE
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"  # Known participant

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email_to_remove in data["message"]

    def test_remove_participant_removes_from_list(self, client, fresh_activities_state):
        """After removal, participant should not appear in participants list
        
        ARRANGE: Set up fresh activities, get initial count
        ACT: Remove participant and fetch activities
        ASSERT: Verify participant count decreased by 1 and email is gone
        """
        # ARRANGE
        activity_name = "Programming Class"
        email_to_remove = "emma@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]
        initial_count = len(initial_participants)

        # ACT
        delete_response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]

        # ASSERT
        assert delete_response.status_code == 200
        assert len(final_participants) == initial_count - 1
        assert email_to_remove not in final_participants

    def test_remove_participant_activity_not_found(self, client, fresh_activities_state):
        """Should return 404 when activity doesn't exist
        
        ARRANGE: Set up fresh activities state with non-existent activity
        ACT: Make DELETE request for non-existent activity
        ASSERT: Verify 404 error
        """
        # ARRANGE
        non_existent_activity = "Fantasy Club"
        email = "student@mergington.edu"

        # ACT
        response = client.delete(
            f"/activities/{non_existent_activity}/participants/{email}"
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_remove_participant_not_found_in_activity(self, client, fresh_activities_state):
        """Should return 404 when participant doesn't exist in activity
        
        ARRANGE: Set up fresh activities with valid activity but non-existent participant
        ACT: Make DELETE request for non-existent participant
        ASSERT: Verify 404 error with "Participant not found"
        """
        # ARRANGE
        activity_name = "Chess Club"
        non_existent_email = "notamember@mergington.edu"

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants/{non_existent_email}"
        )

        # ASSERT
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]

    def test_remove_last_participant_from_activity(self, client, fresh_activities_state):
        """Should be able to remove the last participant from an activity
        
        ARRANGE: Set up activity with single participant (or remove all but one)
        ACT: Remove that participant
        ASSERT: Verify participant is removed and activity has empty list
        """
        # ARRANGE
        activity_name = "Chess Club"
        first_email = "michael@mergington.edu"
        second_email = "daniel@mergington.edu"

        # First, remove one to be left with last participant
        client.delete(f"/activities/{activity_name}/participants/{first_email}")

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants/{second_email}"
        )
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]

        # ASSERT
        assert response.status_code == 200
        assert len(final_participants) == 0

    def test_remove_one_participant_preserves_others(self, client, fresh_activities_state):
        """Removing one participant should keep others in the list
        
        ARRANGE: Set up activity with multiple participants
        ACT: Remove one specific participant
        ASSERT: Verify other participants remain
        """
        # ARRANGE
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants/{email_to_remove}"
        )
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]

        # ASSERT
        assert response.status_code == 200
        assert email_to_remove not in final_participants
        assert email_to_keep in final_participants

    def test_remove_participant_returns_correct_message_format(self, client, fresh_activities_state):
        """Remove response should have proper message format
        
        ARRANGE: Set up fresh activities with known participant
        ACT: Make DELETE request
        ASSERT: Verify message format contains email and activity name
        """
        # ARRANGE
        activity_name = "Gym Class"
        email = "john@mergington.edu"

        # ACT
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        message = data["message"]
        assert "Unregistered" in message
        assert email in message
        assert activity_name in message
