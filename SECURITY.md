# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in OdooAI, please report it responsibly.

**DO NOT** open a public GitHub issue for security vulnerabilities.

### How to Report

Send an email to: **security@odooai.com** (a configurer)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

### Response Timeline

| Step | Timeline |
|------|----------|
| Acknowledgement | < 24 hours |
| Initial assessment | < 48 hours |
| Fix deployed | < 7 days (critical), < 30 days (other) |
| Public disclosure | After fix is deployed |

### Scope

In scope:
- Application security (authentication, authorization, data exposure)
- Data protection (anonymization bypass, credential exposure)
- LLM security (prompt injection, data exfiltration via LLM)
- Infrastructure security (if self-hosted)
- API security

Out of scope:
- Social engineering
- Physical attacks
- Denial of service (unless application-level vulnerability)

### Security Contacts

| Role | Agent |
|------|-------|
| Security Architect | Agent 07 — Application security |
| DevSecOps | Agent 24 — Infrastructure security |
| Security Auditor | Agent 14 — Testing & verification |
| SOC Analyst | Agent 26 — Real-time monitoring |

### Hall of Fame

We thank security researchers who help us improve. Responsible disclosures will be credited here (with permission).
