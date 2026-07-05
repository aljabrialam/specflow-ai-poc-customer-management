# SpecFlow AI Constitution

## Core Principles

### I. Specification First

All development must begin with a documented specification.

No implementation shall begin until:
- Requirements are defined
- Specification is approved
- Clarifications are resolved

Required flow:

Requirement → Specification → Plan → Tasks → Implementation

---

### II. End-to-End Traceability

Every artifact must be traceable.

Required traceability chain:

Requirement → Specification → Plan → Tasks → Tests → Code

Every task must reference a requirement.

Every test must reference a requirement.

Every implementation must reference a task.

---

### III. Testing Pyramid (Non-Negotiable)

All applications shall follow the Testing Pyramid.

Target distribution:

- 70% Unit Tests
- 20% Integration Tests
- 10% End-to-End Tests

All generated solutions must include:

- Unit Tests
- Integration Tests
- End-to-End Tests

Features are not complete until required tests pass.

---

### IV. Cloud-Ready Architecture

All applications must support:

- Local Development
- Docker Deployment
- Azure Deployment
- AWS Deployment

Applications should remain cloud agnostic whenever practical.

---

### V. AI-Assisted Development

AI shall assist in generating:

- Specifications
- Technical Plans
- Task Breakdowns
- Test Designs
- Test Cases
- Implementation Guidance

All AI-generated outputs must remain reviewable and editable by humans.

## Technology Standards

### Frontend

- React
- TypeScript
- Vite

### Backend

- FastAPI
- Python

### Database

- SQLite for local development
- PostgreSQL-ready architecture

### Testing

- Pytest
- Playwright

### Infrastructure

- Docker
- GitHub Actions
- Azure Container Apps
- AWS ECS Fargate

## Development Workflow

The approved workflow is:

Constitution
↓
Specify
↓
Clarify
↓
Plan
↓
Tasks
↓
Test Design
↓
Test Generate
↓
Implement
↓
CI/CD

Custom workflow extensions:

- speckit.test-design
- speckit.test-generate

shall be treated as first-class workflow stages.

## Governance

This Constitution supersedes all project-specific guidance.

Any deviation must be documented and approved.

All generated artifacts must comply with this Constitution before implementation proceeds.

**Version**: 1.0.0

**Ratified**: 2026-06-24

**Last Amended**: 2026-06-24