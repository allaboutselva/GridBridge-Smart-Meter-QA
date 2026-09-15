import allure


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Meter Events")
@allure.story("Event Retrieval")
@allure.title("Verify smart meter events can be retrieved")
@allure.severity(allure.severity_level.CRITICAL)
def test_meter_events(authenticated_api, meter_serial):

    with allure.step(f"Request events for meter {meter_serial}"):
        response = authenticated_api.get(
            f"/api/devices/{meter_serial}/events"
        )

    with allure.step("Verify HTTP status is 200"):
        assert response.status_code == 200

    with allure.step("Attach meter event response"):
        allure.attach(
            response.text,
            name="Meter Events Response",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Verify response belongs to requested meter"):
        data = response.json()
        assert data["device_serial"] == meter_serial

    with allure.step("Verify at least one meter event exists"):
        assert data["events"]

    with allure.step("Verify expected smart-meter event type exists"):
        event_types = {
            event["event_type"]
            for event in data["events"]
        }

        expected_events = {
            "SUPPLY_LOST",
            "SUPPLY_RESTORED",
            "ENCLOSURE_TAMPER",
        }

        assert event_types & expected_events