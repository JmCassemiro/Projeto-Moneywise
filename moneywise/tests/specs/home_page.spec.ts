import { test } from "../fixtures/fixtures"


test.describe("should go to pages", () => {
  test.afterEach(async ({ homePage }) => {
    await homePage.returnToHomePage();
  });
  
  test("should go to informations page", async ({ baseSetup, homePage }) => {
    await homePage.gotoInformationsPage();
    await baseSetup.expectURL('/informations')
  });

  test("should go to contact page", async ({ baseSetup, homePage }) => {
    await homePage.gotoContactPage();
    await baseSetup.expectURL('/contact')
  });

  test("should go to login page", async ({ baseSetup, homePage }) => {
    await homePage.gotoSigninPage();
    await baseSetup.expectURL('/signin')
  });

  test("should go to register page", async ({ baseSetup, homePage }) => {
    await homePage.gotoSignupPage();
    await baseSetup.expectURL('/signup');
  });
});
