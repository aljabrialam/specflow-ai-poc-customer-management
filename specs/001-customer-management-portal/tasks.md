# Tasks: Customer Management Portal

**Input**: Design documents from [spec.md](spec.md), [plan.md](plan.md), and [tests.md](tests.md)

**Prerequisites**: [plan.md](plan.md) and [spec.md](spec.md)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the backend, frontend, test, and container structure needed for the portal.

- [x] T001 Create the backend and frontend project structure under [backend/](../../backend) and [frontend/](../../frontend)
- [x] T002 Create the backend dependency manifest in [backend/requirements.txt](../../backend/requirements.txt)
- [x] T003 Create the frontend dependency manifest and Vite entrypoint in [frontend/package.json](../../frontend/package.json) and [frontend/index.html](../../frontend/index.html)
- [x] T004 Create container deployment assets in [Dockerfile](../../Dockerfile) and [docker-compose.yml](../../docker-compose.yml)
- [ ] T004a Prepare deployment-ready configuration notes for Azure Container Apps and AWS ECS in [docker-compose.yml](../../docker-compose.yml) and [README.md](../../README.md)

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the shared application foundation that all customer stories depend on.

- [x] T005 Create the FastAPI app shell, SQLite initialization, and CORS configuration in [backend/app/main.py](../../backend/app/main.py)
- [x] T006 Define the customer entity and validation models for required fields and email validation in [backend/app/main.py](../../backend/app/main.py)
- [x] T007 Add health and API endpoints for customer CRUD in [backend/app/main.py](../../backend/app/main.py)
- [x] T008 Create the initial React UI shell, customer form, list view, and styling in [frontend/src/App.tsx](../../frontend/src/App.tsx) and [frontend/src/App.css](../../frontend/src/App.css)

## Phase 3: User Story 1 - Create and Review a Customer Record (Priority: P1) 🎯 MVP

**Goal**: Allow a user to create a new customer and immediately see it in the portal list.

**Independent Test**: A reviewer can submit a valid customer form and confirm that the record appears in the list.

### Tests for User Story 1

- [x] T009 Add backend create/list coverage in [backend/tests/test_api.py](../../backend/tests/test_api.py)
- [x] T010 Add browser tests for portal rendering and creation in [e2e/tests/customer-portal.spec.ts](../../e2e/tests/customer-portal.spec.ts)

### Implementation for User Story 1

- [x] T011 Implement create and list customer endpoints in [backend/app/main.py](../../backend/app/main.py)
- [x] T012 Render the customer form and list view in [frontend/src/App.tsx](../../frontend/src/App.tsx)
- [x] T013 Wire form submission and success messaging for the create flow in [frontend/src/App.tsx](../../frontend/src/App.tsx)

## Phase 4: User Story 2 - Update and Remove Customer Information (Priority: P2)

**Goal**: Allow a user to edit an existing customer and remove it when needed.

**Independent Test**: A reviewer can edit an existing record, save it, and then delete it to confirm the UI and API reflect the changes.

### Tests for User Story 2

- [x] T014 Add backend update/delete coverage in [backend/tests/test_api.py](../../backend/tests/test_api.py)
- [x] T015 Extend the browser flow to cover editing and deletion in [e2e/tests/customer-portal.spec.ts](../../e2e/tests/customer-portal.spec.ts)

### Implementation for User Story 2

- [x] T016 Implement update and delete customer endpoints with not-found handling in [backend/app/main.py](../../backend/app/main.py)
- [x] T017 Add edit and delete actions to the customer list in [frontend/src/App.tsx](../../frontend/src/App.tsx)
- [x] T018 Refresh the customer list after updates and deletions in [frontend/src/App.tsx](../../frontend/src/App.tsx)

## Phase 5: User Story 3 - Demonstrate the Workflow for Spec-Driven Delivery (Priority: P3)

**Goal**: Make the portal easy to review, run, and demonstrate as a spec-driven delivery reference implementation.

**Independent Test**: A reviewer can run the documented local or Docker workflow and execute the test commands without extra setup.

- [x] T019 Verify the local startup, Docker compose flow, and automated test commands in [README.md](../../README.md), [docker-compose.yml](../../docker-compose.yml), and the test suites

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finalize UX, validation, and regression confidence across the portal.

- [x] T020 Improve the portal styling and empty-state experience in [frontend/src/App.css](../../frontend/src/App.css)
- [x] T021 Tighten backend validation and error messaging in [backend/app/main.py](../../backend/app/main.py)
- [ ] T023 Add unit tests for validation and CRUD business logic in [backend/tests/test_api.py](../../backend/tests/test_api.py)
- [ ] T024 Configure pytest HTML reporting and Playwright screenshot artifact capture in [backend/tests/generate_report.py](../../backend/tests/generate_report.py), [e2e/playwright.config.ts](../../e2e/playwright.config.ts), and [README.md](../../README.md)
- [x] T022 Run the backend test suite, frontend build, and Playwright verification to validate the full flow
