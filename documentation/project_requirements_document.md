# odoodev Project Requirements Document (PRD)

## 1. Project Overview
odoodev is a Git-based repository designed to become a comprehensive, structured learning hub for Odoo development. In its current state, it contains only a `README.md` placeholder. The goal of this project is to guide beginners and intermediate developers through hands-on Odoo module creation, customization, and best practices via step-by-step tutorials, code samples, and clear documentation.

This repository is being built to fill a gap in easily accessible, example-driven Odoo learning resources. The key objectives for the initial release are: 1) a solid project foundation with an enhanced README, a standardized directory structure for tutorials, and basic contribution guidelines; and 2) a roadmap for at least three starter tutorials, each with code samples and environment setup instructions. Success will be measured by repository clarity, ease of onboarding new contributors, and the initial publication of tutorial skeletons.

## 2. In-Scope vs. Out-of-Scope

**In-Scope (v1.0)**
- Enhanced `README.md` covering project purpose, target audience (beginner/intermediate Odoo devs), prerequisites, and tutorial roadmap.
- Well-defined directory layout under `/tutorials/`, with at least three empty tutorial subfolders:
  - `/tutorials/01_environment_setup/`
  - `/tutorials/02_basic_module/`
  - `/tutorials/03_advanced_features/`
- A `LICENSE` file (MIT) and `CONTRIBUTING.md` with basic contribution process.
- Template `README.md` and code scaffolding in each tutorial folder.
- Environment setup script instructions (Python/Pip, Odoo docker image).

**Out-of-Scope (v1.0)**
- Full draft of each tutorial’s content and complete code examples.
- Live website or static site generator for hosted docs.
- Automated testing or CI/CD pipelines.
- Translations or multi-language support.
- Advanced module packaging and distribution workflows.

## 3. User Flow
When a new learner or contributor visits the repository, they first land on the root `README.md`. This page introduces the project’s mission, lists prerequisites (e.g., Python 3.8+, Docker), and links to individual tutorial folders. The user then clones the repo and follows a quick-start section that guides them through environment setup—either via local Python install or Docker.

After setup, the learner navigates to `/tutorials/01_environment_setup/`, opens its template `README.md` to see next steps, and reviews scaffolded code files. They repeat this pattern for the next tutorial folders (`02_basic_module`, `03_advanced_features`). Contributors follow the `CONTRIBUTING.md` to propose new tutorials by forking the repo, adding content in a new `/tutorials/` subfolder, and opening a pull request.

## 4. Core Features
- **Enhanced Root README**: Clear project description, goals, prerequisites, and tutorial index.
- **Tutorial Directory Structure**: Organized folders under `/tutorials/` with numbered prefixes.
- **Tutorial Templates**: Each tutorial folder contains a placeholder `README.md` and code directories (`/code/`, `/examples/`).
- **License**: `LICENSE` file (MIT) at project root.
- **Contribution Guidelines**: `CONTRIBUTING.md` outlining fork-edit-PR workflow.
- **Environment Setup Section**: Instructions for local Python install and Docker-based Odoo setup.

## 5. Tech Stack & Tools
- **Version Control**: Git on GitHub (public repo).
- **Documentation**: Markdown (`.md`).
- **Primary Framework**: Odoo (version 16.0 or later).
- **Language**: Python 3.x for code examples.
- **Development Tools**: VS Code or PyCharm; optional Docker for containerized Odoo instance.
- **Linting**: Markdown lint (e.g., markdownlint) for consistency.

## 6. Non-Functional Requirements
- Documentation pages must load instantly on GitHub (no heavy assets).
- Markdown files should pass linting checks with zero errors/warnings.
- Code scaffolding must conform to Odoo module structure standards (manifest files, directories). 
- Content readability: tutorials should not exceed 1,500 words each and use consistent heading styles.

## 7. Constraints & Assumptions
- The user has basic Git knowledge and Python installed (or can use Docker).
- Odoo 16 image is publicly available on Docker Hub.
- Contributors will install any additional dependencies locally; no CI is provided initially.
- Internet access is required to fetch Docker images and Python packages.

## 8. Known Issues & Potential Pitfalls
- **Version Mismatch**: Future Odoo version changes may break code examples. Mitigation: specify Odoo version in each tutorial and update roadmap.
- **Directory Confusion**: Without strict naming rules, tutorials might become disorganized. Mitigation: enforce `NN_name` prefix and update CONTRIBUTING guidelines.
- **Lack of CI/CD**: No automated validation. Mitigation: plan for GitHub Actions in a later phase to lint markdown and verify folder structure.
- **Placeholder Overload**: Tutorials might remain empty placeholders. Mitigation: track progress via issues or project board and assign owners for each tutorial.

---
This PRD captures the current scope and roadmap for odoodev. It provides clear, unambiguous guidance for subsequent technical documents and implementation steps, ensuring a smooth path from placeholder repo to a rich Odoo tutorial library.