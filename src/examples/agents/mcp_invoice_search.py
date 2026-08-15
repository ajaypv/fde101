"""A small MCP-style tool loop with client-side policy.

This is a standard-library simulation. Real MCP clients exchange JSON-RPC
messages with servers. The model proposes; the host and client preflight the
request; the server must independently authorize and validate it again.
"""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    read_only: bool


@dataclass(frozen=True)
class UserSession:
    user_id: str
    tenant_id: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class ToolCallResult:
    matches: tuple[dict[str, str], ...] = ()
    error_code: str | None = None
    error_message: str | None = None

    @property
    def is_error(self) -> bool:
        return self.error_code is not None


MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)


TOOL_SPECS = {
    "search_gmail": ToolSpec(
        name="search_gmail",
        description=(
            "Search email messages and attachments. Use for items a sender may "
            "have emailed; do not use for files uploaded directly to Drive."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "vendor": {"type": "string", "maxLength": 120},
                "month": {"type": "string", "enum": list(MONTHS)},
            },
            "required": ["vendor", "month"],
            "additionalProperties": False,
        },
        read_only=True,
    ),
    "search_drive": ToolSpec(
        name="search_drive",
        description=(
            "Search files stored in Drive, including manually uploaded invoices; "
            "do not use to search email messages."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "vendor": {"type": "string", "maxLength": 120},
                "month": {"type": "string", "enum": list(MONTHS)},
            },
            "required": ["vendor", "month"],
            "additionalProperties": False,
        },
        read_only=True,
    ),
    "send_slack": ToolSpec(
        name="send_slack",
        description="Send a Slack message. This creates an external side effect.",
        input_schema={
            "type": "object",
            "properties": {
                "channel": {"type": "string"},
                "message": {"type": "string"},
            },
            "required": ["channel", "message"],
        },
        read_only=False,
    ),
}


EMAIL_FIXTURES = [
    {
        "tenant_id": "tenant-a",
        "vendor": "ABC Technologies",
        "month": "June",
        "id": "mail-104",
    },
    {
        "tenant_id": "tenant-b",
        "vendor": "ABC Technologies",
        "month": "July",
        "id": "mail-private",
    },
]

DRIVE_FIXTURES = [
    {
        "tenant_id": "tenant-a",
        "vendor": "ABC Technologies",
        "month": "July",
        "id": "drive-208",
    },
]


def _search(rows: list[dict[str, str]], args: dict[str, str]) -> list[dict[str, str]]:
    return [
        {key: row[key] for key in ("id", "vendor", "month")}
        for row in rows
        if row["tenant_id"] == args["tenant_id"]
        and row["vendor"].casefold() == args["vendor"].casefold()
        and row["month"].casefold() == args["month"].casefold()
    ]


HANDLERS: dict[str, Callable[[dict[str, str]], list[dict[str, str]]]] = {
    "search_gmail": lambda args: _search(EMAIL_FIXTURES, args),
    "search_drive": lambda args: _search(DRIVE_FIXTURES, args),
}


def invoke_read_tool(
    name: str,
    arguments: dict[str, Any],
    allowed_tools: frozenset[str],
    session: UserSession,
) -> ToolCallResult:
    """Perform client-side checks and return an MCP-style structured result."""
    if name not in allowed_tools:
        return ToolCallResult(error_code="TOOL_NOT_ALLOWED", error_message=name)

    spec = TOOL_SPECS.get(name)
    if spec is None:
        return ToolCallResult(error_code="UNKNOWN_TOOL", error_message=name)
    if not spec.read_only:
        return ToolCallResult(error_code="APPROVAL_REQUIRED", error_message=name)
    if "invoice:read" not in session.scopes:
        return ToolCallResult(error_code="FORBIDDEN", error_message="missing invoice:read")
    if not session.user_id or not session.tenant_id:
        return ToolCallResult(error_code="INVALID_SESSION", error_message="missing identity")
    if name not in HANDLERS:
        return ToolCallResult(error_code="TOOL_UNAVAILABLE", error_message=name)

    required = set(spec.input_schema["required"])
    if set(arguments) != required:
        return ToolCallResult(
            error_code="INVALID_ARGUMENTS",
            error_message=f"expected exactly {sorted(required)}",
        )

    normalized: dict[str, str] = {}
    properties = spec.input_schema["properties"]
    for key, value in arguments.items():
        rules = properties[key]
        if rules.get("type") == "string" and not isinstance(value, str):
            return ToolCallResult(error_code="INVALID_ARGUMENTS", error_message=key)
        cleaned = value.strip()
        if key == "month":
            cleaned = cleaned.title()
        if not cleaned or len(cleaned) > rules.get("maxLength", len(cleaned)):
            return ToolCallResult(error_code="INVALID_ARGUMENTS", error_message=key)
        if "enum" in rules and cleaned not in rules["enum"]:
            return ToolCallResult(error_code="INVALID_ARGUMENTS", error_message=key)
        normalized[key] = cleaned

    # Tenant identity comes from the authenticated session, never model arguments.
    normalized["tenant_id"] = session.tenant_id
    return ToolCallResult(matches=tuple(HANDLERS[name](normalized)))


def find_invoice(
    vendor: str,
    month: str,
    session: UserSession,
) -> tuple[str | None, list[str]]:
    """Use a known read-only fallback order and keep an inspectable trace."""
    allowed = frozenset({"search_gmail", "search_drive"})
    arguments = {"vendor": vendor, "month": month}
    trace: list[str] = []

    for name in ("search_gmail", "search_drive"):
        result = invoke_read_tool(name, arguments, allowed, session)
        if result.is_error:
            trace.append(f"{name}: rejected ({result.error_code})")
            return None, trace
        trace.append(f"{name}: {len(result.matches)} match(es)")
        if result.matches:
            return result.matches[0]["id"], trace

    return None, trace


if __name__ == "__main__":
    current_user = UserSession(
        user_id="user-17",
        tenant_id="tenant-a",
        scopes=frozenset({"invoice:read"}),
    )
    invoice_id, calls = find_invoice("ABC Technologies", "July", current_user)
    print("\n".join(calls))
    print(f"invoice: {invoice_id or 'not found'}")
