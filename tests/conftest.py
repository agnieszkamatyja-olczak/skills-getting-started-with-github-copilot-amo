"""Shared fixtures for all tests"""

import pytest
import sys
from pathlib import Path

# Add src to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app, activities


@pytest.fixture
def client():
    """Provides a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def fresh_activities_state(monkeypatch):
    """Provides a fresh copy of activities and resets the app state for each test
    
    This ensures tests don't interfere with each other by resetting the 
    in-memory activities database to its initial state.
    """
    # Define the fresh state (initial activities)
    fresh_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Team practices and interschool basketball games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training, conditioning, and lap practice",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Practice acting, stagecraft, and prepare performances",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "jack@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science challenges and hands-on experiments",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["amelia@mergington.edu", "mason@mergington.edu"]
        },
        "Debate Team": {
            "description": "Learn argumentation, public speaking, and debate formats",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["charlotte@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Reset the app's activities to the fresh state
    monkeypatch.setattr("app.activities", fresh_activities)
    
    return fresh_activities
