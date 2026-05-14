import { test as base } from "@playwright/test";
import { BaseSetup } from "../page-objects/base_setup";
import { HomePage } from "../page-objects/home_page";
import { SigninPage } from "../page-objects/signin_page";
import { SignupPage } from "../page-objects/signup_page";
import { TransactionsPage } from "../page-objects/transactions_page";
import { ProfilePage } from "../page-objects/profile_page";

type MyFixtures = {
  baseSetup: BaseSetup;
  homePage: HomePage;
  signinPage: SigninPage;
  signupPage: SignupPage;
  transactionsPage: TransactionsPage;
  profilePage: ProfilePage;
};

export const test = base.extend<MyFixtures>({
  context: async ({ browser }, use) => {
    const context = await browser.newContext();
    await use(context);
    await context.close();
  },

  page: async ({ context }, use) => {
    const page = await context.newPage();
    await use(page);
  },

  baseSetup: async ({ page }, use) => {
    const baseSetup = new BaseSetup(page);
    await use(baseSetup);
  },

  homePage: async ({ baseSetup }, use) => {
    await baseSetup.goto();
    const homePage = new HomePage(baseSetup.getPage());
    await use(homePage);
  },

  signinPage: async ({ page }, use) => {
    const signinPage = new SigninPage(page);
    await use(signinPage);
  },

  signupPage: async ({ homePage }, use) => {
    await homePage.gotoSignupPage();
    const signupPage = new SignupPage(homePage.getPage());
    await use(signupPage);
  },

  transactionsPage: async ({ page }, use) => {
    const transactionsPage = new TransactionsPage(page);
    await use(transactionsPage);
  },

  profilePage: async ({ page }, use) => {
    const profilePage = new ProfilePage(page);
    await use(profilePage);
  },
});
