"""연습용 MCP 서버 v1: 승인할 때 보여 주는 정상 버전입니다. stdio 로 실행됩니다."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes-lab")

NOTES = {
    "welcome": "연습용 메모 서버에 오신 것을 환영합니다.",
    "todo": "금요일까지 로그 보관 기간을 점검합니다.",
}


@mcp.tool()
def list_notes() -> list[str]:
    """등록된 메모 이름 목록을 돌려줍니다."""
    return sorted(NOTES)


@mcp.tool()
def read_note(name: str) -> str:
    """메모 이름을 받아 해당 메모의 내용을 돌려줍니다."""
    return NOTES.get(name, "해당 이름의 메모가 없습니다.")


if __name__ == "__main__":
    mcp.run()
