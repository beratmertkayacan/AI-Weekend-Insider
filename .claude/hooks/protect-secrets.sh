#!/bin/bash
T=$(jq -r '.tool_input.file_path // .tool_input.command // empty')
case "$T" in
  *.env* | *secrets*)
    echo "Blocked: secrets are off-limits — don't work around it" >&2
    exit 2 ;;
esac
exit 0
