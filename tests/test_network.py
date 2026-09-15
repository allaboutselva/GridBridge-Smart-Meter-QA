import allure


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Network Configuration")
@allure.story("Security Key")
@allure.title("Verify device security key can be configured securely")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_security_key(authenticated_api):

    payload = {
        "device_id": "GB-DEVICE-1001",
        "key": "1234567890ABCDEF1234567890ABCDEF",
    }

    with allure.step("Submit device security key configuration"):
        response = authenticated_api.post(
            "/api/network/security-keys",
            json=payload,
        )

    with allure.step("Verify HTTP status is 201"):
        assert response.status_code == 201

    with allure.step("Verify device ID"):
        assert (
            response.json()["device_id"]
            == payload["device_id"]
        )

    with allure.step("Verify secret key is not exposed"):
        assert payload["key"] not in response.text

    allure.attach(
        response.text,
        name="Network Configuration Response",
        attachment_type=allure.attachment_type.JSON,
    )