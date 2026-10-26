#!/bin/bash
# MCP filesystem 서버를 설정에 넣고, 읽기 도구 7개만 노출합니다. 컨테이너 안에서 실행합니다.
set -e
hermes config set mcp_servers.filesystem.command npx
hermes config set mcp_servers.filesystem.args '["-y","@modelcontextprotocol/server-filesystem","/home/agent/practice/shared"]'
hermes config set mcp_servers.filesystem.tools.include '["read_text_file","read_multiple_files","list_directory","directory_tree","search_files","get_file_info","list_allowed_directories"]'
hermes mcp list
