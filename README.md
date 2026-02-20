# Code_Reviewer

Hybrid AI-Assisted Static Code Intelligence System for Predictive Bug Detection

This project presents a Hybrid AI-Assisted Static Code Intelligence System designed to perform deterministic and AI-driven source code analysis in a completely offline environment. Unlike traditional LLM-based code reviewers that rely entirely on generative outputs, this system integrates compiler-level static analysis, Abstract Syntax Tree (AST) inspection, deterministic rule engines, and GPU-accelerated local large language model inference to provide explainable, validated, and production-aware code review.

The system is capable of analyzing Python-based software repositories to detect structural flaws, runtime vulnerabilities, maintainability issues, and security threats using a multi-stage hybrid analysis pipeline. The objective of the platform is to combine rule-based deterministic analysis with contextual reasoning provided by locally hosted large language models deployed using Ollama, thereby eliminating dependency on external APIs while maintaining inference performance through GPU-enabled execution environments such as Google Colab.


System Architecture

                User Source Code
                        ↓
        Static Rule-Based Analysis Engine
                        ↓
        AST Structural Inspection Engine
                        ↓
        Hybrid AI Reasoning Layer
           (Ollama + CodeLlama)
                        ↓
        AI-Based Fix Suggestion Module
                        ↓
        Compilation-Level Fix Validator
                        ↓
        Code Difference Generator
                        ↓
        Risk Scoring Engine
                        ↓
        Final Review Report

        
| Component            | Technology Used             |
| -------------------- | --------------------------- |
| Frontend Interface   | Streamlit                   |
| Backend Framework    | FastAPI                     |
| Static Code Analysis | Python AST Module           |
| Local LLM Runtime    | Ollama                      |
| LLM Model            | CodeLlama 7B                |
| GPU Execution        | Google Colab                |
| Secure Tunneling     | Ngrok                       |
| Fix Validation       | Python Compile API          |
| Diff Generation      | Difflib                     |
| Risk Scoring         | Custom Weighted Rule Engine |
| Deployment Mode      | Offline + Remote GPU Hybrid |


This platform is suitable for:

1)Secure offline software review environments

2)Academic code quality analysis

3)DevSecOps pre-deployment validation

4)AI-assisted developer productivity tools

5)Predictive runtime vulnerability detection
