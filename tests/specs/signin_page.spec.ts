import { test } from "../fixtures/fixtures"

test.describe("Login Methods", () => {
  test("should be able to login with valid credentials", async ({
    baseSetup,
    homePage,
    signupPage,
    signinPage,
    transactionsPage,
    profilePage,
  }) => {
    const userName = `test +${Date.now()}@test.com`;
    const email = `test+${Date.now()}@test.com`;
    const password = '!Test12345678';
    const birthDate = '2002-09-29';

    await baseSetup.goto();
    await homePage.gotoSignupPage();
    await signupPage.register(userName, email, password, password, birthDate);
    await signinPage.login(email, password);
    await baseSetup.expectURL('/transactions/');

    await transactionsPage.gotoProfilePage();
    await profilePage.deleteUser(password);
  });

  test("should not be able to login with invalid credentials", async ({
    baseSetup,
    homePage,
    signinPage,
  }) => {
    await baseSetup.goto();
    await homePage.gotoSigninPage();
    await signinPage.login('invalidEmail@test.com', 'invalidPassword');
    await signinPage.expectError();
  });
});
