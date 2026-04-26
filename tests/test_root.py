"""Tests for the root endpoint (GET /)

Tests the redirect from the root path to the static HTML interface.
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_html(self, client):
        """Root endpoint should redirect to /static/index.html
        
        ARRANGE: Create test client
        ACT: Make GET request to root endpoint
        ASSERT: Verify redirect status code and location header
        """
        # ARRANGE
        expected_redirect_url = "/static/index.html"

        # ACT
        response = client.get("/", follow_redirects=False)

        # ASSERT
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url

    def test_root_redirect_url_is_static_folder(self, client):
        """Verify that the redirect goes to the static folder
        
        ARRANGE: Create test client
        ACT: Make GET request to root endpoint with follow_redirects
        ASSERT: Verify the final URL contains static content
        """
        # ARRANGE
        # (no setup needed)

        # ACT
        response = client.get("/", follow_redirects=True)

        # ASSERT
        # When following redirects, we should get the HTML content
        # (status 200 for successful HTML retrieval)
        assert response.status_code == 200
