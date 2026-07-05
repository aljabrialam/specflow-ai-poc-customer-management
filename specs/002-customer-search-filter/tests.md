# Test Design: Customer Search and Filter

**Feature**: Customer Search and Filter
**Date**: 2026-07-05
**Source**: [spec.md](spec.md)

## Backend Test Cases

- Verify the list endpoint returns matching customers for a name search
- Verify the list endpoint returns matching customers for an email search
- Verify the list endpoint returns matching customers for a company search
- Verify an empty result returns an empty list and the UI can render an empty state

## Browser Test Cases

- Verify typing a search term filters the visible customer list
- Verify clearing the search restores the full list
- Verify no-match input shows the empty-state message
