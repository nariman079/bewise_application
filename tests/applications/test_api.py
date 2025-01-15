import pytest


from tests.utils import assert_response


@pytest.fixture
def application_data():
    return {"user_name": "testUser1", "description": "testDescription1"}


@pytest.mark.asyncio
async def test_create_application(client, application_data):
    assert_response(
        client.post("/api/applications/", json=application_data),
        expected_code=201,
        expected_data={
            "message": "Заявка создана",
            "data": {"id": 1, **application_data},
        },
    )


@pytest.mark.asyncio
async def test_get_application(client, application_data):
    assert_response(
        client.get(
            "/api/applications",
        ),
        expected_code=200,
        expected_data={
            "message": "Заявки получены",
            "data": [{"id": 1, **application_data}],
        },
    )


@pytest.mark.asyncio
async def test_get_application_by_user_name(client):
    response = assert_response(
        client.get("/api/applications", params={"user_name": "testUser1"}),
        expected_code=200,
        expected_data=None,
    )

    for application in response.json()["data"]:
        assert application["user_name"] == "testUser1", application


@pytest.mark.asyncio
async def test_get_application_by_user_name_empty(client):
    assert_response(
        client.get("/api/applications", params={"user_name": "testUser2"}),
        expected_code=200,
        expected_data={"data": []},
    )


@pytest.mark.asyncio
async def test_get_pagindated_application(client, application_data):
    for i in range(10):
        client.post("/api/applications/", json=application_data)
    response = assert_response(
        client.get("/api/applications", params={"page": 1, "size": 3}),
        expected_code=200,
    )
    assert len(response.json()["data"]) == 3
