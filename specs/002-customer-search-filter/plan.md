# Implementation Plan: Customer Search and Filter

**Branch**: `002-customer-search-filter` | **Date**: 2026-07-05 | **Spec**: [spec.md](spec.md)

## Summary

Add a lightweight search experience to the customer management portal so users can filter the visible list by name, email, or company.

## Technical Context

**Frontend**: React + TypeScript + Vite
**Backend**: FastAPI + SQLite
**Testing**: Pytest + Playwright

## Implementation Approach

- Extend the backend customer list endpoint to accept an optional search query.
- Add a search input to the frontend customer list view.
- Update the UI to show an empty-state message when no records match.
- Add backend and browser tests for the new behavior.
