import allure
from config.settings import settings


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Authentication")
@allure.story("Valid Login")
@allure.title("Verify user can authenticate with valid credentials")
@allure.severity(allure.severity_level.BLOCKER)
def test_valid_login(api):

    with allure.step("Send login request with valid credentials"):
        response = api.post(
            "/api/session",
            json={
                "username": settings.api_username,
                "password": settings.api_password,
            },
        )

    with allure.step("Verify HTTP status is 200"):
        assert response.status_code == 200

    with allure.step("Verify bearer token is returned"):
        data = response.json()
        assert data["token_type"] == "bearer"
        assert data["access_token"]


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Authentication")
@allure.story("Invalid Login")
@allure.title("Verify invalid password is rejected")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalid_login(api):

    with allure.step("Send login request with invalid password"):
        response = api.post(
            "/api/session",
            json={
                "username": settings.api_username,
                "password": "wrong-password-for-test",
            },
        )

    with allure.step("Verify HTTP status is 401"):
        assert response.status_code == 401