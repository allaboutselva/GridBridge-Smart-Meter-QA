import json
import allure


@allure.epic("GridBridge Smart Meter QA")
@allure.feature("Database Validation")
@allure.story("API vs MySQL")
@allure.title("Verify meter API data matches MySQL database")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_meter_matches_database(
    authenticated_api,
    db,
    meter_serial,
):

    with allure.step(f"Request meter {meter_serial} from API"):
        response = authenticated_api.get(
            f"/api/devices/{meter_serial}"
        )

        assert response.status_code == 200
        api_data = response.json()

    with allure.step("Read the same meter from MySQL"):
        db_data = db.fetch_one(
            """
            SELECT
                serial_number,
                logical_name,
                manufacturer,
                status
            FROM meters
            WHERE serial_number = %s
            """,
            (meter_serial,),
        )

        assert db_data is not None

    with allure.step("Compare API fields with database fields"):
        for field in (
            "serial_number",
            "logical_name",
            "manufacturer",
            "status",
        ):
            assert api_data[field] == db_data[field]

    allure.attach(
        json.dumps(api_data, indent=2, default=str),
        name="API Meter Data",
        attachment_type=allure.attachment_type.JSON,
    )

    allure.attach(
        json.dumps(db_data, indent=2, default=str),
        name="MySQL Meter Data",
        attachment_type=allure.attachment_type.JSON,
    )