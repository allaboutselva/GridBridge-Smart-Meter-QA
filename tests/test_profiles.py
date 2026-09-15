import allure


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Profiles / OBIS")
@allure.story("Meter Measurements")
@allure.title("Verify meter measurements contain OBIS information")
@allure.severity(allure.severity_level.CRITICAL)
def test_measurements_include_obis(
    authenticated_api,
    meter_serial,
):

    with allure.step(f"Request measurements for {meter_serial}"):
        response = authenticated_api.get(
            f"/api/devices/{meter_serial}/measurements"
        )

    with allure.step("Verify HTTP status is 200"):
        assert response.status_code == 200

    with allure.step("Attach measurement response"):
        allure.attach(
            response.text,
            name="OBIS Measurement Response",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Verify measurements belong to requested meter"):
        data = response.json()
        assert data["device_serial"] == meter_serial

    with allure.step("Verify measurement data is available"):
        assert data["measurements"]

    with allure.step("Verify required OBIS measurement fields"):
        first_measurement = data["measurements"][0]

        for field in (
            "obis_code",
            "value",
            "unit",
            "reading_time",
        ):
            assert field in first_measurement