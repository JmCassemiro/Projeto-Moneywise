import { expect, type Locator, type Page } from "@playwright/test";

export class SigninPage {
  private readonly page: Page;
  private readonly emailField: Locator;
  private readonly passwordField: Locator;
  private readonly loginBtn: Locator;

  constructor(page: Page) {
    this.page = page;

    this.emailField = this.page.getByRole('textbox', { name: 'Email:' });
    this.passwordField = this.page.getByRole('textbox', { name: 'Senha:' });
    this.loginBtn = this.page.getByRole('button', { name: 'Login' });
  }

  getPage() {
    return this.page;
  }

  async login(email: string, password: string) {
    await this.emailField.fill(email);
    await this.passwordField.fill(password);
    await this.loginBtn.click();
  }

  async expectError() {
    await expect(this.page.getByText('Email ou senha inválidos')).toBeVisible();
  }
}