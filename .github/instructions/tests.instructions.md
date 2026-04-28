---
name: Testing Architect
description: Strict guidelines for tests under /tests, including naming, fixture setup, auth injection, and async mocking patterns.
applyTo: "tests/**/*"
---

# Testing Guidelines

## Naming Convention
- Test methods must use camel-cased action with snake-cased expectation: `testAction_expectedResult`.
- Prefer names that describe behavior, not implementation details.
- Examples:
  - `testEdit_notifiesOwner`
  - `testMonitorNayax_skipsExistingSale`

## Test Class Structure
- Use `django.test.TestCase` for database-backed tests.
- Use `@inject_auth` when tests require organization/owner context.
- Declare key class attributes for readability and type intent (for example: `owner`, `org`, model instances, and shared mocks).

## Fixture and Data Setup
- Prefer JSON fixtures with `load_from_dir` for repeatable setup.
- Keep fixture directory constants at class level when used repeatedly.
- If a loaded fixture is a Django model instance that will be referenced by FK, persist it before use (for example, call `save()` before attaching to another model).
- Use transform callbacks in `load_from_dir` for injecting related objects rather than hardcoding IDs in fixture JSON.

## Test User Setup
- Do not create users inline with `CustomUser.objects.create(...)` in tests.
- Use `create_test_user(...)` from `tests.auth` for fake users.
- Pass explicit IDs only when identity needs to be stable across assertions.

## Mocking and Patching
- For async channel methods (for example `channel_layer.group_send`), use `AsyncMock`, not `MagicMock`.
- Patch module boundaries, not internal implementation details, to preserve behavior-focused tests.
- For external integrations, use shared mocking helpers (for example `patch_module_functions`) where available.

## Assertions
- Assert outcomes that matter to behavior (created records, IDs included, status/field updates).
- Use targeted assertions (`assertEqual`, `assertIn`, `assertIsNotNone`, `assert_not_called`) over broad truthiness checks.
- When a query may return `None`, fail explicitly with a clear message before subsequent assertions.

## Style and Scope
- Keep each test focused on one behavior path.
- Prefer minimal setup required for the assertion.
- Avoid over-mocking database behavior; rely on `TestCase` isolation and real ORM interactions for model logic.
