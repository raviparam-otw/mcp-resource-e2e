"""Integration tests require: pip install -r requirements.txt"""
import unittest
from fastmcp import Client
from server import mcp

class FastMCPIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_resource_and_tools(self):
        async with Client(mcp) as client:
            result = await client.call_tool('discover_catalog', {})
            self.assertIn('catalog://queries/all', str(result))
            resource = await client.read_resource('catalog://queries/all')
            self.assertIn('Active checking accounts', str(resource))
            page_result = await client.call_tool('read_catalog_page', {'offset': 999})
            self.assertIn('Q1000', str(page_result))

if __name__ == '__main__': unittest.main()
