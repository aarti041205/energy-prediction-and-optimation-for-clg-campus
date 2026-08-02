import pytest
import asyncio
import httpx
from src.api.app import app

class FastAPIAppClient:
    """
    Synchronous test client wrapper using httpx.ASGITransport and AsyncClient.
    Bypasses starlette/httpx version mismatch issues cleanly.
    """
    def __init__(self, app):
        self.transport = httpx.ASGITransport(app=app)
        self.base_url = "http://testserver"

    def get(self, url: str, **kwargs):
        async def _req():
            async with httpx.AsyncClient(transport=self.transport, base_url=self.base_url) as c:
                return await c.get(url, **kwargs)
        return asyncio.run(_req())

    def post(self, url: str, **kwargs):
        async def _req():
            async with httpx.AsyncClient(transport=self.transport, base_url=self.base_url) as c:
                return await c.post(url, **kwargs)
        return asyncio.run(_req())

@pytest.fixture(scope="module")
def client():
    yield FastAPIAppClient(app)
