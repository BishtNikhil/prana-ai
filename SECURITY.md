# Security Policy & The Ponytail Method Compliance

PranaAI (प्राण AI) is engineered with security, privacy, and architectural sanitation as fundamental design constraints. This document details our security posture, secret hygiene, and repository containment standards for **PromptWars Virtual Challenge 06** (Google for Developers).

---

## 🔒 1. The Ponytail Method: Clean, Contained & Zero Loose Ends

The **"Ponytail Method"** enforces that all sensitive credentials, runtime configurations, build artifacts, and development debris are tightly bound, isolated, and strictly excluded from public version control:

1. **Zero Hardcoded Secrets (Zero-Secret Law):**
   - No API keys, passwords, bearer tokens, or cryptographic private keys exist anywhere in source code (`.py`, `.js`, `.html`, `.json`, `.toml`).
   - All external integrations (such as Google Gemini 2.5 Flash) rely strictly on runtime environment variables managed via an isolated `.env` file (enforced by `.gitignore`).
   - A sanitized `.env.example` is provided with dummy placeholders for reproduction.
   - Intelligent deterministic fallbacks ensure 100% application resilience even without cloud credentials.

2. **Airtight Exclusion Boundary (`.gitignore`):**
   - Environment configurations (`.env`, `.env.*`, `.env.local`)
   - Cryptographic keys, certs, and identity files (`*.pem`, `*.key`, `*.pfx`, `*.id_rsa*`)
   - Python bytecode and virtual environments (`__pycache__/`, `venv/`, `.venv/`)
   - Test results and coverage caches (`.pytest_cache/`, `.coverage`, `htmlcov/`)
   - Platform and deployment state files (`.vercel/`)
   - Operating system and IDE metadata (`.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/`)

3. **Autonomous Guardrails & Sanitization:**
   - GenAI interactions utilize strict typed Pydantic v2 schemas (`ChatMessageRequest` and `ChatMessageResponse`).
   - Prompt sanitization prevents prompt injection, token bloat, or arbitrary code execution.
   - Comprehensive OWASP standard headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Permissions-Policy`) are injected into every HTTP response.

---

## 🔍 2. Secret Scan & Sanitization Verification

Prior to pushing to GitHub, the repository was audited using automated regex and semantic pattern scanning:

| Category | Checked Patterns | Verification Result |
| :--- | :--- | :--- |
| **Google Gemini API Keys** | `AIza[0-9A-Za-z-_]{35}` | ✅ **0 matches found** |
| **OpenAI / Anthropic Keys** | `sk-[a-zA-Z0-9]{20,}` | ✅ **0 matches found** |
| **GitHub Access Tokens** | `ghp_*`, `gho_*`, `github_pat_*` | ✅ **0 matches found** |
| **Private Keys & Certs** | `-----BEGIN PRIVATE KEY-----`, `*.pem`, `*.key` | ✅ **0 matches found** |
| **Database Connection Strings** | `postgres://*:*@`, `mysql://*:*@`, `mongodb://*:*@` | ✅ **0 matches found** |

---

## 🛡️ 3. Responsible Vulnerability Disclosure

If you discover any security consideration, privacy risk, or potential vulnerability within PranaAI, please open an advisory or contact the maintainers directly:

- **Lead Engineer:** Nikhil Singh Bisht
- **Contact:** nikhilbisht2807@gmail.com
- **Hackathon:** PromptWars Virtual Challenge 06 (Google for Developers)
- **Response SLA:** Within 24 hours of notification
