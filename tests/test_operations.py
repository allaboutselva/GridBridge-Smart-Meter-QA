import allure


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Meter Operations")
@allure.story("Meter Command")
@allure.title("Verify meter command is queued")
@allure.severity(allure.severity_level.CRITICAL)
def test_meter_command(authenticated_api):

    payload = {
        "meters": ["MTR-61594"],
        "description": "Meter command test",
        "priority": 5,
        "timeout": 3600,
        "retries": 0,
    }

    with allure.step("Create meter command"):
        response = authenticated_api.post(
            "/api/operations/meter-command",
            json=payload,
        )

    with allure.step("Verify HTTP status is 201"):
        assert response.status_code == 201

    with allure.step("Attach operation response"):
        allure.attach(
            response.text,
            name="Meter Command Response",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Verify operation type"):
        assert response.json()["type"] == "METER_COMMAND"

    with allure.step("Verify operation enters QUEUED state"):
        assert response.json()["status"] == "QUEUED"