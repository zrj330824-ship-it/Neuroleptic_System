# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

**Related**:
- [AGENTS.md](AGENTS.md) - Agent configuration
- [WORKFLOW_VPS_DEPLOYMENT.md](WORKFLOW_VPS_DEPLOYMENT.md) - VPS setup

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- API Tokens (encrypted/secure)
- Anything environment-specific

---

## 🔐 Credentials & Tokens

### VPS SSH

- **Host**: 8.208.78.10 (London)
- **User**: root
- **Key**: `~/.ssh/vps_key`
- **Path**: `/root/polymarket_quant_fund/`

### GitHub

- **Username**: zrj330824-ship-it
- **Email**: zrj330824@gmail.com
- **Repository**: https://github.com/zrj330824-ship-it/Neuroleptic_System
- **Token**: `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`
- **Token Scope**: repo (full control of private repositories)
- **Stored**: 2026-02-25 12:28
- **Expires**: 2026-05-26 (90 days)
- **Next Rotation**: 2026-05-01

### Cookie Storage (VPS)

- **Path**: `/root/polymarket_quant_fund/cookies/`
- **Files**: medium.json, x.json, reddit.json, substack.json
- **Permissions**: chmod 600

### API Tokens (.env file)

- **Location**: `/root/polymarket_quant_fund/.env`
- **Permissions**: chmod 600
- **Never commit to Git**

---

## 📊 Platform Configuration

### Cameras

- [None configured yet]

### SSH Hosts

- **home-server**: [Not configured]
- **vps-london**: 8.208.78.10, user: root

### TTS

- **Preferred voice**: [Not configured]
- **Default speaker**: [Not configured]

### Trading

- **Platform**: Polymarket
- **VPS**: 8.208.78.10 (London)
- **Parameters**: min_arbitrage_threshold: 0.25%, safety_margin: 1.2
- **Target**: 3-4 trades/hour

---

## 🛠️ Workflow Notes

### GitHub Token Workflow

**When token is needed**:
1. Check environment: `echo $GITHUB_TOKEN`
2. If empty, check TOOLS.md (this file)
3. If not here, ask user
4. Store in environment for session: `export GITHUB_TOKEN=ghp_xxxx`

**Security**:
- Never commit token to Git
- Never share in chat
- Use environment variable or secure storage
- Rotate every 90 days

### Daily Workflow

1. **Morning (06:00)**: Check daily plan (auto-generated)
2. **Midday (12:00)**: Check platform status
3. **Evening (18:00)**: Review progress
4. **Night (00:30)**: Auto-sync to share directory

### Scientific Integrity Workflow

Before ANY publication:
1. Open WORKFLOW_SCIENTIFIC_INTEGRITY.md
2. Complete verification checklist
3. Confirm no Red Flags
4. Label appropriately (Verified/Preliminary/Theoretical)
5. Then publish

---

*Last updated: 2026-02-25*  
*Next review: When credentials change*
