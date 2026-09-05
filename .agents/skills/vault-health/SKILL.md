---
name: vault-health
description: Diagnoses vault integrity, finds orphan notes, dead wikilinks, missing frontmatter, and suggests bidirectional connections across courses.
---

# Vault Health & Linker Skill

Use this skill to audit, clean, and enrich the Obsidian second-brain vault.

## Capabilities

### 1. Diagnostic Audit
Execute `python scripts/vault_health.py` to scan the vault for:
- **Dead Wikilinks**: Links pointing to non-existent notes.
- **Orphan Notes**: Notes with zero incoming or outgoing connections.
- **Malformed Frontmatter**: Files missing standard YAML properties.

### 2. Smart Bidirectional Linking
- When reviewing a note, identify unlinked mentions of existing concepts in `03-Concepts/` and suggest converting them to `[[Concept-Name]]`.
- Update relevant Maps of Content (MOCs) in `05-MOCs/` when new evergreen notes are created.
