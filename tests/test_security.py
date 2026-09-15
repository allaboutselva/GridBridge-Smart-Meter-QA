import allure
import requests
from config.settings import settings


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("API Security")
@allure.story("Missing JWT")
@allure.title("Verify protected endpoint rejects missing JWT")
@allure.severity(allure.severity_level.CRITICAL)
def test_missing_token(meter_serial):

    with allure.step("Request protected meter endpoint without JWT"):
        response = requests.get(
            f"{settings.api_base_url}/api/devices/{meter_serial}",
            timeout=settings.request_timeout,
        )

    with allure.step("Verify unauthorized request is rejected"):
        assert response.status_code in (401, 403)


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("API Security")
@allure.story("Invalid JWT")
@allure.title("Verify protected endpoint rejects invalid JWT")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalid_token(api, meter_serial):

    with allure.step("Configure invalid JWT authorization header"):
        api.session.headers.update(
            {
                "Authorization": "Bearer invalid.jwt.token"
            }
        )

    with allure.step("Request protected meter endpoint"):
        response = api.get(
            f"/api/devices/{meter_serial}"
        )

    with allure.step("Verify HTTP status is 401"):
        assert response.status_code == 401