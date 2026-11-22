# Contributing to Urban Air Quality Assistant (Aura)

Thank you for your interest in contributing to the **Urban Air Quality Assistant** project! We welcome community contributions to help urban families and communities combat toxic winter smog.

## How to Contribute

### 1. Reporting Bugs
- Check the existing GitHub Issues before opening a new issue.
- Clearly describe the bug, including steps to reproduce, operating system, and expected vs actual behavior.

### 2. Proposing Features
- We love new science-backed Indoor Air Quality (IAQ) hacks, local atmospheric data integrations, and community action modules!
- Open an issue describing your proposed feature and how it benefits urban families and communities.

### 3. Pull Request Guidelines
1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/my-new-hack
   ```
2. Ensure dependencies are listed in `requirements.txt`.
3. Test all module imports:
   ```bash
   python -c "import api_service, impact_calculator, iaq_hacks, routines_generator, community_hub, genai_engine"
   ```
4. Commit your changes with clear, descriptive commit messages.
5. Push to your branch and submit a Pull Request to `main`.
