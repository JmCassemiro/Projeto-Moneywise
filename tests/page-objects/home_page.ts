import { Page, type Locator } from '@playwright/test';

export class HomePage {
  private readonly page: Page;
  private readonly informationsPageBtn: Locator;
  private readonly contactPageBtn: Locator;
  private readonly loginPageBtn: Locator;
  private readonly registerPageBtn: Locator;

  constructor(page: Page) {
    this.page = page;

    this.informationsPageBtn = this.page.getByRole('link', { name: 'Informações' });
    this.contactPageBtn = this.page.getByRole('link', { name: 'Contato' });
    this.loginPageBtn = this.page.getByRole('link', { name: 'Entrar' });
    this.registerPageBtn = this.page.getByRole('link', { name: 'Comece Agora!' });
  }

  getPage() {
    return this.page;
  }

  async gotoInformationsPage() {
    await this.informationsPageBtn.click();
  }

  async gotoContactPage() {
    await this.contactPageBtn.click();
  }

  async gotoSigninPage() {
    await this.loginPageBtn.click();
  }

  async gotoSignupPage() {
    await this.registerPageBtn.click();
  }

  async returnToHomePage() {
    await this.page.getByRole('link', { name: 'Logo' }).click();
  };
}