from httpx import Response


def assert_response(
    response: Response, expected_code: int, expected_data: dict | None = None
) -> Response:
    assert response.status_code == expected_code, (
        f"{response.status_code} != {expected_code}, {response.json()}"
    )
    if expected_data:
        for key, value in expected_data.items():
            respose_value = response.json().get(key)
            assert respose_value == value, f"{respose_value} != {value}"
    return response
