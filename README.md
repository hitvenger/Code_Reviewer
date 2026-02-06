# Code_Reviewer
Offline AI Code Review Agent (Ollama-Powered)

The Offline AI Code Review Agent is a developer-focused tool designed to analyze Python codebases without relying on cloud services or paid APIs. The project combines traditional static analysis techniques with locally hosted large language models using Ollama, enabling intelligent code review entirely offline. It is built to simulate real-world code review systems while remaining secure, fast, and suitable for academic or restricted environments.

This project performs automated code reviews by scanning Python files and identifying common programming issues such as logical errors, resource mismanagement, type risks, portability issues, and code smells. In addition to rule-based detection, it optionally uses a locally running AI model to generate human-like feedback, explain detected issues, scaledown code without compromisingquality and suggest improvements. Since the AI model runs locally, no source code or data ever leaves the user’s machine.

The application provides a modern and intuitive user interface built with Streamlit. Users can select a single Python file or an entire project folder for analysis. The results are displayed through a clean dashboard showing severity-based metrics, detailed issue breakdowns, line-highlighted code snippets, and optional AI-generated review comments. Each file is analyzed independently, making it easy to understand and debug large projects.

For AI-assisted review, the project integrates with Ollama, which runs open-source code models such as CodeLLaMA or DeepSeek locally. This allows the system to provide natural-language explanations, refactoring suggestions, and high-level code quality feedback without any dependency on external APIs
