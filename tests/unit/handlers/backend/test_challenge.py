import json
from http.client import OK, BAD_REQUEST

from flask.testing import FlaskClient
from pytest import mark

PATH = "/backend/challenge"


class TestVehicleFeaturesPost:
    def test_saves_all_vehicles(
        self,
        client: FlaskClient,
        mock_vehicle_store,
        valid_vehicle_features_post: str,
    ):
        response = client.post(
            PATH,
            data=valid_vehicle_features_post,
            headers={"content-type": "application/json; charset=utf-8"},
        )

        assert response.status_code == OK

        parsed_request = json.loads(valid_vehicle_features_post)
        assert mock_vehicle_store.create_vehicle.call_count == len(parsed_request["vehicle"])

    @mark.parametrize("content_type", ["application/x-www-form-urlencoded", ""])
    def test_returns_bad_request_if_content_type_is_invalid(
        self,
        client: FlaskClient,
        mock_vehicle_store,
        valid_vehicle_features_post: str,
        content_type: str,
    ):
        headers = {}
        if content_type:
            headers["content-type"] = content_type

        response = client.post(
            PATH,
            data=valid_vehicle_features_post,
            headers=headers,
        )

        assert response.status_code == BAD_REQUEST
        response_data = response.json
        assert response_data
        assert len(response_data["errors"]) == 1
        error = response_data["errors"][0]
        assert error["loc"] == ["headers", "content-type"]

    @mark.parametrize("json_error", [True, False])
    def test_returns_bad_request_if_body_is_invalid(
        self,
        client: FlaskClient,
        mock_vehicle_store,
        invalid_vehicle_features_post: str,
        json_error: bool,
    ):
        response = client.post(
            PATH,
            data="{" if json_error else invalid_vehicle_features_post,
            headers={"content-type": "application/json"},
        )

        assert response.status_code == BAD_REQUEST
        response_data = response.json
        assert response_data
        assert len(response_data["errors"]) == 1

        error = response_data["errors"][0]
        assert error["type"] == "json_invalid" if json_error else "missing"

        if not json_error:
            assert error["loc"] == ["vehicle", 1, "features", 1, "description", "short"]
