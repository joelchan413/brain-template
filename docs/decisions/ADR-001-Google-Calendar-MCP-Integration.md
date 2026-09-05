# ADR-001: Google Calendar Integration via Model Context Protocol (MCP)

## Status
Accepted

## Date
2026-08-15

## Context
The student Second Brain vault requires dynamic awareness of daily college schedules, classroom locations across campus, exam dates, and available free-time windows.

Requirements:
- Agent access to read upcoming events and schedule study blocks automatically.
- Zero vendor lock-in; markdown files must remain portable without proprietary plugin requirements.
- Safe OAuth 2.0 authentication directly with Google Calendar API.
- Support for bidirectional time-blocking (vault $\leftrightarrow$ calendar).

## Decision
Integrate Google Calendar using the open-standard **Model Context Protocol (MCP)** via `@cocal/google-calendar-mcp` authenticated through Google Cloud Console OAuth 2.0 Desktop App credentials.

## Alternatives Considered

### 1. Obsidian Community Plugins Only (e.g. Full Calendar / ICS)
- **Pros**: Direct visual UI inside Obsidian.
- **Cons**: AI agent cannot autonomously query free/busy slots or programmatically create spaced repetition study blocks based on syllabus milestones.
- **Rejected as sole solution**: Plugins can be used alongside MCP for UI rendering, but MCP is essential for agentic workflow automation.

### 2. Custom Ad-Hoc Python OAuth Script
- **Pros**: Complete custom control over local scripting.
- **Cons**: High maintenance overhead; requires token refresh management, argument validation, and custom tool scaffolding inside agent prompts.
- **Rejected**: MCP provides a standardized, battle-tested tool protocol natively recognized by Antigravity.

## Consequences
- Antigravity possesses live tool definitions (`list-events`, `create-event`, `get-freebusy`, etc.).
- Daily notes (`01-Daily/YYYY-MM-DD.md`) can be generated on demand with accurate lecture times and room numbers.
- Reverse exam planning can insert structured review blocks into Google Calendar without user manual entry.
- Credentials and tokens are securely stored locally in user configuration directories (`~/.config/google-calendar-mcp/` and `~/.gemini/config/mcp_config.json`).
