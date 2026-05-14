import { test } from "../fixtures/fixtures"

test.beforeEach(async ({ baseSetup, homePage, signupPage, signinPage, transactionsPage }) => {
  const userName = `test +${Date.now()}@test.com`;
  const email = `test+${Date.now()}@test.com`;
  const password = '!Test12345678';
  const birthDate = '2002-09-29';
  
  await baseSetup.goto();
  await homePage.gotoSignupPage();
  await signupPage.register(userName, email, password, password, birthDate);
  await signinPage.login(email, password);

  await transactionsPage.gotoProfilePage();
});

test("should delete an account", async ({ transactionsPage, profilePage }) => {
  await profilePage.deleteUser('!Test12345678')
});

test.describe("should manipulate profile", () => {
  test.afterEach(async ({ transactionsPage, profilePage }) => {
    await profilePage.deleteUser('!Test12345678');
  });
  test("should edit a profile", async ({ profilePage }) => {
    await profilePage.editProfile();
  });
});

test.describe("should be redirect to pages", () => {
  test("should go to transactions page", async ({ profilePage }) => {;
    await profilePage.gotoTransactionsPage();
    await profilePage.expectURL('/transactions');
  });
});