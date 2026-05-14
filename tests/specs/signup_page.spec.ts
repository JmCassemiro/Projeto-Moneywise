import { test } from "../fixtures/fixtures"

test.describe("Registration Methods", () => {
  test.afterEach(async ({ transactionsPage, profilePage }) => {
    await transactionsPage.gotoProfilePage();
    await profilePage.deleteUser('!Test12345678');
  });
  
  test("should be able to register with valid credentials", async ({ baseSetup, signupPage, signinPage }) => {
    const userName = `test +${Date.now()}@test.com`;
    const email = `test+${Date.now()}@test.com`;
    const password = '!Test12345678';
    const birthDate = '2002-09-29';
    
    await signupPage.register(userName, email, password, password, birthDate);
    await baseSetup.expectURL('/signin');
    await signinPage.login(email, password);
  });
});

test("should not be able to register with invalid email", async ({ signupPage }) => {
  await signupPage.register('test', 'Invalid Email', '12345678', '12345678', '2002-09-29');
  await signupPage.emailError();
});

test("should not be able to register with different passwords", async ({ signupPage }) => {
  await signupPage.register('test', 'Invalid Email', '12345678', 'different pass', '2002-09-29');
  await signupPage.passwordError();
});