import pytest

from tests.utils import assert_response
from tests.conftest import client

@pytest.fixture
def application_data():
    return {
            'user_name': 'testUser1',
            'description': 'testDescription1'
        }

@pytest.mark.asyncio
async def test_create_application(client, application_data):
    assert_response(
        client.post(
            '/api/applications/',
            json=application_data
        ),
        expected_code=201,
        expected_data={
            'message': "Заявка создана",
            'data': {
                "id":1
                **application_data
            }
        }
    )

@pytest.mark.asyncio
async def test_get_application(client, application_data):
    assert_response(
        client.get(
            '/api/applications',
        ),
        expected_code=200,
        expected_data={
            'message':"Заявки получены",
            'data': [
                {
                    'id': 1,
                    **application_data
                }
            ]
        }
    )

@pytest.mark.asyncio
async def test_get_application_by_user_name(client):
    pass

@pytest.mark.asyncio
async def test_get_pagindated_application():
    pass