import { test } from "../fixtures/fixtures"

test.beforeEach(async ({ baseSetup, homePage, signupPage, signinPage }) => {
  const userName = `test +${Date.now()}@test.com`;
  const email = `test+${Date.now()}@test.com`;
  const password = '!Test12345678';
  const birthDate = '2002-09-29';
  
  await baseSetup.goto();
  await homePage.gotoSignupPage();
  await signupPage.register(userName, email, password, password, birthDate);
  await signinPage.login(email, password);
});

test.afterEach(async ({ transactionsPage, profilePage }) => {
  await transactionsPage.gotoProfilePage();
  await profilePage.deleteUser('!Test12345678');
});

test("should be able to create a transaction", async ({ transactionsPage }) => {
  const transactionData = {
    title: "Transaction",
    paymentMethod: "PIX",
    value: "100.00",
    date: "2023-10-01",
    category: "Casa",
    description: "Test Description",
    is_recurring: true,
    installments: "5",
    type: "Despesa"
  };
  
  await transactionsPage.clickNewTransactionBtn();
  await transactionsPage.fillTransactionFields(transactionData);
  await transactionsPage.submitCreateForm();
  await transactionsPage.expectTransactionToBeViewed(transactionData);
});

test("should be able to update a transaction", async ({ transactionsPage, page }) => {
  const transactionData = {
    title: "Transaction",
    paymentMethod: "PIX",
    value: "100.00",
    date: "2023-10-01",
    category: "Casa",
    description: "Test Description",
    is_recurring: false,
    type: "Despesa"
  };

  const updatedTransactionData = {
    title: "Updated Transaction",
    paymentMethod: "Credito",
    value: "150.00",
    date: "2023-10-02",
    category: "Entretenimento",
    description: "Updated Description",
    is_recurring: true,
    installments: "3",
    type: "Receita"
  };

  await transactionsPage.clickNewTransactionBtn();
  await transactionsPage.fillTransactionFields(transactionData);
  await transactionsPage.submitCreateForm();
  await page.getByText('Transaction').click();
  await transactionsPage.fillTransactionFields(updatedTransactionData);
  await transactionsPage.submitEditForm();
  await transactionsPage.expectTransactionToBeViewed(updatedTransactionData);
});

test("should be able to delete a transaction", async ({ transactionsPage }) => {
  const transactionData = {
    title: "Transaction to Delete",
    paymentMethod: "PIX",
    value: "100.00",
    date: "2023-10-01",
    category: "Casa",
    description: "Test Description",
    is_recurring: false,
    type: "Despesa"
  };

  await transactionsPage.clickNewTransactionBtn();
  await transactionsPage.fillTransactionFields(transactionData);
  await transactionsPage.submitCreateForm();
  await transactionsPage.viewTransaction(transactionData.title);
  await transactionsPage.deleteTransaction(transactionData.title);
  await transactionsPage.expectTransactionNotToExist(transactionData.title);
});
