function toggleMenu(event) {
  event.stopPropagation();
  const menu = document.getElementById("user-menu");
  menu.style.display = menu.style.display === "flex" ? "none" : "flex";
}

document.addEventListener("click", function (event) {
  const menu = document.getElementById("user-menu");
  const userInfo = document.querySelector(".user-info");
  
  if (!userInfo.contains(event.target)) {
      menu.style.display = "none";
  }
});

function setTransactionAmount() {
  const transactionItems = document.querySelectorAll('.transaction-item');
  const incomeField = document.getElementById('income-value');
  const expenseField = document.getElementById('expense-value');
  const totalField = document.getElementById('total-value');

  let incomeValue = 0;
  let expenseValue = 0;

  transactionItems.forEach(item => {
    console.log(item.style.display);
    if (item.style.display !== "none") {
      const transactionType = item.querySelector('.transaction-type');
      const transactionAmount = item.querySelector('.transaction-amount');

      const amount = parseFloat(transactionAmount.textContent.trim().replace(/[^0-9.-]+/g, ''));

      if (transactionType.textContent.trim().toLowerCase() === 'income') {
        incomeValue += amount;
      } else if (transactionType.textContent.trim().toLowerCase() === 'expense') {
        expenseValue += amount;
      }
    }
  });

  let totalFieldValue = incomeValue - expenseValue;

  incomeField.textContent = `R$ ${incomeValue.toFixed(2)}`;
  expenseField.textContent = `R$ ${expenseValue.toFixed(2)}`;
  totalField.textContent = `R$ ${totalFieldValue.toFixed(2)}`;
}

document.addEventListener('DOMContentLoaded', () => {
  setTransactionAmount();
});
