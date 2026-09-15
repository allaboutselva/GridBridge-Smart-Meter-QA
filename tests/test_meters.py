import allure
import pytest


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Meter Management")
@allure.story("Meter Information")
@allure.title("Verify registered smart meter details")
@allure.severity(allure.severity_level.CRITICAL)
def test_existing_meter(authenticated_api, meter_serial):

    with allure.step(f"Request meter information for {meter_serial}"):
        response = authenticated_api.get(
            f"/api/devices/{meter_serial}"
        )

    with allure.step("Verify HTTP response status is 200"):
        assert response.status_code == 200

    with allure.step("Verify returned meter serial number"):
        data = response.json()

        allure.attach(
            response.text,
            name="Meter API Response",
            attachment_type=allure.attachment_type.JSON,
        )

        assert data["serial_number"] == meter_serial


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Meter Management")
@allure.story("Meter State")
@allure.title("Verify registered meter is ONLINE")
@allure.severity(allure.severity_level.CRITICAL)
def test_meter_state(authenticated_api, meter_serial):

    with allure.step(f"Request operational state for {meter_serial}"):
        response = authenticated_api.get(
            f"/api/devices/{meter_serial}/state"
        )

    with allure.step("Verify HTTP response status is 200"):
        assert response.status_code == 200

    with allure.step("Attach meter state response"):
        allure.attach(
            response.text,
            name="Meter State Response",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Verify meter state is ONLINE"):
        assert response.json() == {
            "serial_number": meter_serial,
            "state": "ONLINE",
        }


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Meter Management")
@allure.story("Unknown Meter")
@allure.title("Verify unknown meter returns 404: {serial}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "serial",
    [
        "MTR-99999",
        "UNKNOWN-000",
    ],
)
def test_unknown_meter(authenticated_api, serial):

    with allure.step(f"Request unknown meter {serial}"):
        response = authenticated_api.get(
            f"/api/devices/{serial}"
        )

    with allure.step("Attach API response"):
        allure.attach(
            response.text,
            name=f"Unknown Meter Response - {serial}",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Verify API returns HTTP 404"):
        assert response.status_code == 404