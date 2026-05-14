import { expect, type Page } from "@playwright/test";
import dotenv from 'dotenv';
dotenv.config();

let URL = 'http://127.0.0.1:3000';

export class BaseSetup {
  private readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  getPage() {
    return this.page;
  }

  async goto() {
    await this.page.goto(URL);
  }

  async expectURL(currentPage: string) {
    const CURRENT_URL = await this.page.url();
    expect(CURRENT_URL).toContain(currentPage);
  }

}
