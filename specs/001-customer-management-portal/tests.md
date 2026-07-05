# Test Design: Customer Management Portal

**Feature**: Customer Management Portal
**Date**: 2026-07-05
**Source**: [spec.md](spec.md)

## Test Strategy

The feature will use a layered testing approach aligned with the constitution:
- Backend API tests with Pytest for business rules and CRUD behavior
- Browser tests with Playwright for the main user journey and UI feedback

## Unit Test Cases

- Verify required-field validation rejects empty values for name, email, phone, and company
- Verify email validation rejects malformed addresses before persistence
- Verify customer creation, update, and delete logic map correctly to the persisted model

## Backend Test Cases

### API: Create Customer
- Verify a valid customer payload returns HTTP 201 and stores the record
- Verify missing required fields returns HTTP 422
- Verify invalid email format returns HTTP 422
- Verify duplicate email returns HTTP 409

### API: List Customers
- Verify listing returns all persisted customers in descending order by id

### API: Update Customer
- Verify updating an existing customer returns the updated record
- Verify updating a non-existent customer returns HTTP 404

### API: Delete Customer
- Verify deleting an existing customer returns HTTP 204 and removes it from storage
- Verify deleting a non-existent customer returns HTTP 404

## Browser Test Cases

### Portal Rendering
- Verify the main page loads and shows the portal heading and form section

### Customer Creation Flow
- Verify a user can fill the form and create a customer
- Verify a success message is shown after creation
- Verify the new customer appears in the list

### Customer Editing Flow
- Verify a user can edit an existing customer
- Verify the updated values appear in the list after save
- Verify a success message is shown after update

### Customer Deletion Flow
- Verify a user can create a customer, delete it, and confirm it disappears from the list

### Browser Session Notes
- The Playwright suite uses a shared browser page across tests to exercise the CRUD journey in a single session
- Tests are executed serially so the UI state is consistent across create, update, and delete steps
- Each Playwright run saves screenshot artifacts under the test-results folder for visual inspection

### Reporting Notes
- Backend API results should be generated as a browser-openable HTML report
- The HTML report should be reproducible with the pytest command that writes to the backend test report output
- Playwright runs should save screenshot artifacts under the e2e test-results directory for visual inspection

## Coverage Notes

These tests cover the primary P1 and P2 journeys from the feature specification and support the acceptance scenarios for creating, viewing, updating, and deleting customer records.
