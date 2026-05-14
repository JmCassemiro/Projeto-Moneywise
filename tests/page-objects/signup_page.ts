import { expect, Page, type Locator } from '@playwright/test';

export class SignupPage {
  private readonly page: Page;
  private readonly usernameField: Locator;
  private readonly emailField: Locator;
  private readonly passwordField: Locator;
  private readonly confirmPasswordField: Locator;
  private readonly birthdateField: Locator;
  private readonly registerBtn: Locator;

  constructor(page: Page) {
    this.page = page;

    this.usernameField = this.page.getByRole('textbox', { name: 'Usuário:' });
    this.emailField = this.page.getByRole('textbox', { name: 'Email:' });
    this.passwordField = this.page.getByRole('textbox', { name: 'Senha:', exact: true });
    this.confirmPasswordField = this.page.getByRole('textbox', { name: 'Confirmar Senha:' });
    this.birthdateField = this.page.getByRole('textbox', { name: 'Aniversário:' });
    this.registerBtn = this.page.getByRole('button', { name: 'Criar Conta' });
  }

  async register(username: string, email: string, password: string, confirmPassword: string, birthdate: string) {
    await this.usernameField.fill(username);
    await this.emailField.fill(email);
    await this.passwordField.fill(password);
    await this.confirmPasswordField.fill(confirmPassword);
    await this.birthdateField.fill(birthdate);
    await this.registerBtn.click();
  }

  async emailError() {
    await expect(this.page.getByText('Invalid email address. ×')).toBeVisible();
  }

  async passwordError() {
    await expect(this.page.getByText('As senhas não coincidem.')).toBeVisible();
  }
}