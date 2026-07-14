# Tasks: Backend Unit and Integration Tests

**Input**: Design documents from `Doc/specs/001-backend-unit-integration-tests/`

**Prerequisites**: `PRD.md`, `spec.md`, `research.md`, `plan.md`, `quickstart.md`

**Tests**: This feature is entirely about creating unit and integration tests. Tests are mandatory.

**Organization**: Tasks are grouped by independently testable stories.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files or has no dependency on another task in the same phase.
- **[Story]**: User story mapping from `spec.md`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add Python test tooling and base directory structure without touching Playwright tests.

- [x] T001 Add `pytest`, `pytest-mock` and `pytest-cov` to `requirements.txt`.
- [x] T002 Create backend Python test directories `tests/unit/` and `tests/integration/`.
- [x] T003 Create `tests/conftest.py` for shared pytest fixtures.
- [x] T004 Add pytest configuration if needed to avoid collecting TypeScript Playwright files.
- [x] T005 Verify existing Playwright folders `tests/specs/`, `tests/fixtures/` and `tests/page-objects/` remain unchanged.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create reusable fixtures and helpers required by all test stories.

**CRITICAL**: No story-specific test file should start until this phase is complete.

- [x] T006 Implement `app` fixture in `tests/conftest.py` using `create_app('testing')`.
- [x] T007 Implement `client` fixture in `tests/conftest.py` using Flask test client.
- [x] T008 Implement database lifecycle fixture in `tests/conftest.py` using `db` and `TEST_DATABASE_URL`.
- [x] T009 Implement fixture/helper for creating `User` records in the test database.
- [x] T010 Implement fixture/helper for creating `Transaction` records in the test database.
- [x] T011 Implement authenticated client helper that creates JWT access cookies for protected routes.
- [x] T012 Implement mail mock helper to prevent real email delivery.
- [x] T013 Validate setup with a smoke test that creates app context and opens the home page.

**Checkpoint**: Fixture foundation ready. User story test implementation can now proceed.

---

## Phase 3: User Story 1 - Unit-test domain behavior (Priority: P1) MVP

**Goal**: Fast backend tests for deterministic rules without real database, browser, network or email delivery.

**Independent Test**: `pytest tests/unit` passes without requiring `TEST_DATABASE_URL`.

### Tests for User Story 1

- [x] T014 [P] [US1] Create `tests/unit/test_transaction_service.py` for `TransactionService._clean_form_data`, `_parse_amount`, `_parse_date`, `_parse_time`, `_parse_int`.
- [x] T015 [P] [US1] Add transaction validation cases for missing required fields, invalid amount, invalid date, invalid time and invalid transaction type.
- [x] T016 [P] [US1] Create `tests/unit/test_statistics_service.py` for dashboard aggregation with mocked `TransactionRepository.list_recent_for_user`.
- [x] T017 [P] [US1] Add statistics cases for empty history, monthly series, category totals, balance and top 5 expenses.
- [x] T018 [P] [US1] Create `tests/unit/test_user_service.py` for `UserService.authenticate`, `_parse_birthday`, validation errors and password checks with repository mocks.
- [x] T019 [P] [US1] Create `tests/unit/test_password_reset_service.py` for token handling and mocked mail send.
- [x] T020 [P] [US1] Create `tests/unit/test_forms.py` for password strength, signup validation and reset password validation.
- [x] T021 [P] [US1] Create `tests/unit/test_tokens.py` for `generate_reset_token` and `confirm_reset_token` in app context.
- [x] T022 [P] [US1] Create `tests/unit/test_errors.py` for `AppError.to_dict`, status codes and JSON error handlers.
- [x] T023 [P] [US1] Create `tests/unit/test_contact_service.py` for `ContactService.send_contact_message` with mocked `mail.send`.

**Checkpoint**: `pytest tests/unit` passes independently.

---

## Phase 4: User Story 2 - Integration-test persistence and isolation (Priority: P2)

**Goal**: Validate repositories and services with the real Flask app context and test database.

**Independent Test**: `pytest tests/integration -k "repository or service or statistics"` validates DB-backed behavior.

### Tests for User Story 2

- [ ] T024 [P] [US2] Create `tests/integration/test_user_repository_and_service.py` for user create, duplicate email, duplicate name, get by id and authentication.
- [ ] T025 [P] [US2] Add profile update, reset password and delete account integration cases in `tests/integration/test_user_repository_and_service.py`.
- [ ] T026 [P] [US2] Create `tests/integration/test_transaction_repository_and_service.py` for create, get, list, update and delete transaction.
- [ ] T027 [P] [US2] Add transaction filter integration cases for search, type, category, payment method, date range and amount range.
- [ ] T028 [P] [US2] Add transaction ordering and cross-user isolation cases in `tests/integration/test_transaction_repository_and_service.py`.
- [ ] T029 [P] [US2] Add rollback/error behavior tests for transaction create/update/delete failures where practical.
- [ ] T030 [P] [US2] Create `tests/integration/test_statistics_integration.py` for dashboard calculations using persisted transactions.
- [ ] T031 [P] [US2] Add statistics integration case proving one user's dashboard excludes another user's transactions.

**Checkpoint**: DB-backed tests pass repeatedly with clean state.

---

## Phase 5: User Story 3 - Integration-test Flask routes (Priority: P3)

**Goal**: Validate route behavior through Flask test client without Playwright.

**Independent Test**: `pytest tests/integration -k "routes or auth"` validates HTTP behavior, cookies, redirects, JSON and persisted state.

### Tests for User Story 3

- [x] T032 [P] [US3] Create `tests/integration/test_auth_routes.py` for signup, signin, logout and authenticated redirect behavior.
- [x] T033 [P] [US3] Add protected route unauthenticated redirect cases for profile, transactions and statistics.
- [ ] T034 [P] [US3] Add `/token/expires` success and missing expiration cases in `tests/integration/test_auth_routes.py`.
- [ ] T035 [P] [US3] Create `tests/integration/test_profile_routes.py` for profile page, profile update JSON and delete account route.
- [x] T036 [P] [US3] Create `tests/integration/test_password_reset_routes.py` for forgot password and reset password routes with mail mocked.
- [x] T037 [P] [US3] Create `tests/integration/test_transaction_routes.py` for transaction list, create, edit and delete routes.
- [x] T038 [P] [US3] Add route cases for invalid transaction form data and not-found transaction access.
- [ ] T039 [P] [US3] Create `tests/integration/test_statistics_routes.py` for statistics page success and service failure redirect.
- [ ] T040 [P] [US3] Create `tests/integration/test_home_routes.py` for home, informations and contact page behavior.

**Checkpoint**: Route integration tests pass without browser automation.

---

## Phase 6: Polish & Cross-Cutting Validation

**Purpose**: Final checks, coverage and documentation alignment.

- [x] T041 Run `pytest tests/unit` and fix failures caused by tests or revealed bugs.
- [x] T042 Run `pytest tests/integration` and fix failures caused by tests or revealed bugs.
- [ ] T043 Run `pytest tests/unit tests/integration --cov=app` and review coverage gaps.
- [ ] T044 Update `Doc/PRD.md` if implementation decisions changed during execution.
- [ ] T045 Update `Doc/specs/001-backend-unit-integration-tests/quickstart.md` with exact commands verified locally.
- [x] T046 Confirm no Playwright/E2E test files were changed for this feature.
- [ ] T047 Confirm no real email was sent during test execution.
- [x] T048 Confirm integration tests can run twice consecutively without state leakage.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on setup and blocks all story-specific tests.
- **US1 Unit Tests (Phase 3)**: Depends on foundational fixtures where app context or mocks are needed.
- **US2 DB Integration Tests (Phase 4)**: Depends on database lifecycle fixtures.
- **US3 Route Integration Tests (Phase 5)**: Depends on app, client, authenticated client and DB fixtures.
- **Polish (Phase 6)**: Depends on selected story phases being complete.

### Parallel Opportunities

- T014-T023 can run in parallel after foundation because they use separate unit test files.
- T024-T031 can run in parallel if database fixture isolation is reliable.
- T032-T040 can run in parallel if each test creates independent users/data.

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3.
3. Validate `pytest tests/unit`.
4. Stop and review whether unit tests reveal bugs before proceeding.

### Incremental Delivery

1. Add unit coverage for deterministic behavior.
2. Add DB integration coverage for persistence and isolation.
3. Add route integration coverage for Flask/JWT behavior.
4. Run coverage and update documentation.

## Notes

- Do not modify Playwright tests for this feature.
- Prefer assertions on status, JSON, redirects, cookies and persisted state over fragile template text.
- Keep fixtures small and explicit.
- Do not send real email in any test.
- Keep production code changes minimal and justified by failing tests.
