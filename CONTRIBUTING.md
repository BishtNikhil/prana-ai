# Contributing to PranaAI (प्राण AI)

Thank you for your interest in contributing to **PranaAI**, the autonomous urban air quality assistant and winter smog copilot built for the **PromptWars Virtual Challenge 06** (Google for Developers).

---

## 🏛️ Architecture & Core Principles

1. **Deterministic Atmospheric & Math Invariance:**
   - CPCB / US EPA PM2.5 breakpoint interpolations, Berkeley Earth cigarette equivalence math, and CADR room sizing formulas are calculated deterministically via computational engines (`AQIEngine`, `IAQEngine`, `ImpactEngine`).
   - Generative AI is never used to hallucinate raw physical or physiological constants.

2. **The Ponytail Method & Zero-Secret Law:**
   - Never commit API keys, secrets, or authentication tokens to Git. All credentials must be read from environment variables via `app.config.AppConfig`.
   - Keep repository tree lean, clean, and contained with zero dead code or loose temporary files.

3. **Resilient Offline Fallback Guarantee:**
   - Every GenAI touchpoint must possess an intelligent, science-grounded deterministic fallback guaranteeing 100% service uptime even when external APIs are unreachable or unconfigured.

---

## 🛠️ Development Setup & Quality Standards

1. **Virtual Environment & Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Automated Testing Protocol:**
   Every contribution must pass the complete automated test matrix:
   ```bash
   python -m pytest tests/ -v
   ```

3. **Code Style & Type Annotations:**
   - Strict Python 3.11+ type hints (`typing.Dict`, `typing.List`, `typing.Optional`, `typing.Tuple`).
   - Clean docstrings with architectural rationale and physics descriptions.
   - Pydantic v2 schemas for all API payloads and response contracts.

4. **Accessibility (WCAG 2.1 AA Compliance):**
   - High-contrast color scales for air quality categories.
   - Screen-reader accessible semantic HTML with ARIA labels and roles.
   - Keyboard accessible navigation across all views and interactive controls.

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
