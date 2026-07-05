import { test, expect } from '@playwright/test';

test.describe.configure({ mode: 'serial' });

let page: any;

test.beforeAll(async ({ browser }) => {
  page = await browser.newPage();
});

test.afterAll(async () => {
  await page.close();
});

test('renders the customer management portal', async ({}, testInfo) => {
  await page.goto('/');
  await expect(page.getByText('Customer Management Portal')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Create customer' })).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath('portal-render.png'), fullPage: true });
});

test('allows creating and reading a customer from the form', async ({}, testInfo) => {
  await page.goto('/');

  const email = `test-customer-${Date.now()}@example.com`;

  await page.getByLabel('Name').fill('Test Customer');
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Phone').fill('+1-555-0000');
  await page.getByLabel('Company').fill('Contoso');
  await page.getByRole('button', { name: 'Create customer' }).click();

  await expect(page.getByText('Customer created.')).toBeVisible();
  await expect(page.locator('article').filter({ hasText: 'Test Customer' }).filter({ hasText: email })).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath('create-customer.png'), fullPage: true });
});

test('allows updating an existing customer', async ({}, testInfo) => {
  await page.goto('/');

  const createdEmail = `editable-${Date.now()}@example.com`;
  const editedEmail = `edited-${Date.now()}@example.com`;

  await page.getByLabel('Name').fill('Editable Customer');
  await page.getByLabel('Email').fill(createdEmail);
  await page.getByLabel('Phone').fill('+1-555-1111');
  await page.getByLabel('Company').fill('Fabrikam');
  await page.getByRole('button', { name: 'Create customer' }).click();

  await page.getByRole('button', { name: 'Edit' }).first().click();
  await page.getByLabel('Email').fill(editedEmail);
  await page.getByRole('button', { name: 'Save changes' }).click();

  await expect(page.getByText('Customer updated.')).toBeVisible();
  await expect(page.getByText(editedEmail)).toBeVisible();
  await page.screenshot({ path: testInfo.outputPath('update-customer.png'), fullPage: true });
});

test('allows deleting the created customer', async ({}, testInfo) => {
  await page.goto('/');

  const email = `delete-me-${Date.now()}@example.com`;

  await page.getByLabel('Name').fill('Delete Me');
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Phone').fill('+1-555-9999');
  await page.getByLabel('Company').fill('Contoso');
  await page.getByRole('button', { name: 'Create customer' }).click();

  await page.locator('article').filter({ hasText: 'Delete Me' }).filter({ hasText: email }).getByRole('button', { name: 'Delete' }).click();

  await expect(page.getByText('Customer deleted.')).toBeVisible();
  await expect(page.locator('article').filter({ hasText: 'Delete Me' }).filter({ hasText: email })).toHaveCount(0);
  await page.screenshot({ path: testInfo.outputPath('delete-customer.png'), fullPage: true });
});
