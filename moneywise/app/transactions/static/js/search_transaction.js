function searchTransaction() {
  var input, filter, transactions, transactionItems, i, txtValue, found = false;
  
  input = document.getElementById("search");
  filter = input.value.toUpperCase();
  
  transactions = document.querySelector(".transactions");
  if (!transactions) return;

  transactionItems = transactions.getElementsByClassName("transaction-item");

  for (i = 0; i < transactionItems.length; i++) {
      let titleElement = transactionItems[i].querySelector(".transaction-name");
      
      if (titleElement) {
          txtValue = titleElement.textContent || titleElement.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
              transactionItems[i].style.display = "";
              found = true;
          } else {
              transactionItems[i].style.display = "none";
          }
      }
  }

  let noResultMessage = document.getElementById("no-transaction-message");
  if (!noResultMessage) {
      noResultMessage = document.createElement("p");
      noResultMessage.id = "no-transaction-message";
      noResultMessage.style.color = "white";
      noResultMessage.style.textAlign = "center";
      noResultMessage.textContent = "Nenhuma transação encontrada";
      transactions.appendChild(noResultMessage);
  }

  noResultMessage.style.display = found ? "none" : "block";
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("search").addEventListener("keyup", searchTransaction);
  document.getElementById("search").addEventListener("keyup", setTransactionAmount);
});