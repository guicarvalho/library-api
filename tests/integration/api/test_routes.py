from http import HTTPStatus

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health_check(client: AsyncClient) -> None:
    # Given
    expected_response = {"postgres": "ok"}

    # When
    response = await client.get("/healthz")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response
