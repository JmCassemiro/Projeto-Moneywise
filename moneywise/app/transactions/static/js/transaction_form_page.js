function setTransactionType(type) {
  document.getElementById("transaction_type").value = type;
}

function changeButtonColor(button) {
  document.querySelectorAll(".transaction-type-buttons button").forEach((btn) => {
    btn.classList.remove("active");
    btn.style.backgroundColor = "";
    btn.style.color = btn.classList.contains("income-btn") ? "#92CA7E" : "#CA7E7E";
  });

  if (button) {
    button.classList.add("active");
    button.style.backgroundColor = button.classList.contains("income-btn")
      ? "#92CA7E"
      : "#CA7E7E";
    button.style.color = "#18181B";
  }
}

function toggleNumberOfPayments() {
  const checkbox = document.getElementById("checkbox");
  const container = document.getElementById("number-of-payments-container");
  const input = document.getElementById("number_of_payments");

  if (!checkbox || !container || !input) {
    return;
  }

  if (checkbox.checked) {
    container.style.display = "block";
    input.setAttribute("required", "required");
  } else {
    container.style.display = "none";
    input.removeAttribute("required");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const transactionType = document.getElementById("transaction_type").value.trim();

  if (transactionType === "income") {
    changeButtonColor(document.getElementById("income-btn"));
  } else if (transactionType === "expense") {
    changeButtonColor(document.getElementById("expense-btn"));
  }

  toggleNumberOfPayments();

  const recurringCheckbox = document.getElementById("checkbox");
  if (recurringCheckbox) {
    recurringCheckbox.addEventListener("change", toggleNumberOfPayments);
  }

  document.querySelectorAll("select option").forEach((option) => {
    option.style.color = option.disabled ? "gray" : "white";
  });
});
