import { expect, type Page } from "@playwright/test";

export class ProfilePage {
  private readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async gotoTransactionsPage() {
    await this.page.getByRole('link', { name: 'Transações' }).click();
  }

  async expectURL(currentPage: string) {
    const CURRENT_URL = await this.page.url();
    expect(CURRENT_URL).toContain(currentPage);
  }

  async deleteUser(password: string) {
    await this.page.getByRole('link', { name: 'Deletar Conta' }).click();
    await this.page.getByRole('textbox', { name: 'Confirme sua senha:' }).fill(password);
    await this.page.getByRole('button', { name: 'Excluir' }).click();
  }

  async editProfile() {
      await this.page.getByRole('button', { name: 'Editar perfil' }).click();
      await this.page.getByRole('textbox').first().fill('teste editado');
      await this.page.getByRole('textbox').nth(1).fill('teste.editado@teste.com');
      await this.page.getByRole('textbox').nth(2).fill('29/09/2010');
      this.page.once('dialog', dialog => {
        console.log(`Dialog message: ${dialog.message()}`);
        dialog.dismiss().catch(() => {});
      });
      await this.page.getByRole('button', { name: 'Salvar' }).click();
  }
}
