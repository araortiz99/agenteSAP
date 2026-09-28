import asyncio

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target


async def main() -> None:
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
        allowed_tools=("search_resources",),
    )

    async with SapMcpClient(target) as client:
        info = client.server_info()
        print(f"Server: {info.name if info else 'unknown'}")
        print(f"Version: {info.version if info else 'unknown'}")

        tools = await client._require_connected().list_tools()
        tool = next(item for item in tools.tools if item.name == "search_resources")

        print("Tool: search_resources")
        print("Description:")
        print(tool.description or "(none)")
        print("Input schema:")
        print(tool.inputSchema)

        # Do not execute the tool yet. We first need the server's actual schema
        # so that the next smoke test does not guess its arguments.


if __name__ == "__main__":
    asyncio.run(main())
