function setTransactionType(type) {
  document.getElementById("transaction_type").value = type;
}

function changeButtonColor(button) {
  document
    .querySelectorAll(".transaction-type-buttons button")
    .forEach((btn) => {
      btn.classList.remove("active");
      btn.style.backgroundColor = "";
      btn.style.color = btn.classList.contains("income-btn")
        ? "#92CA7E"
        : "#CA7E7E";
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

function setupNumberStepper(input) {
  if (!input || input.closest(".number-stepper")) {
    return;
  }

  const wrapper = document.createElement("div");
  wrapper.className = "number-stepper";

  const controls = document.createElement("div");
  controls.className = "number-stepper-controls";

  const incrementButton = document.createElement("button");
  incrementButton.type = "button";
  incrementButton.setAttribute("aria-label", "Aumentar número de parcelas");
  incrementButton.innerHTML =
    '<i class="bi bi-chevron-up" aria-hidden="true"></i>';

  const decrementButton = document.createElement("button");
  decrementButton.type = "button";
  decrementButton.setAttribute("aria-label", "Diminuir número de parcelas");
  decrementButton.innerHTML =
    '<i class="bi bi-chevron-down" aria-hidden="true"></i>';

  input.parentNode.insertBefore(wrapper, input);
  wrapper.appendChild(input);
  controls.appendChild(incrementButton);
  controls.appendChild(decrementButton);
  wrapper.appendChild(controls);

  const updateValue = (direction) => {
    if (!input.value) {
      input.value = input.min || "1";
    }

    if (direction === "up") {
      input.stepUp();
    } else {
      input.stepDown();
    }

    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  };

  incrementButton.addEventListener("click", () => updateValue("up"));
  decrementButton.addEventListener("click", () => updateValue("down"));
}

document.addEventListener("DOMContentLoaded", () => {
  const transactionType = document
    .getElementById("transaction_type")
    .value.trim();

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

  setupNumberStepper(document.getElementById("number_of_payments"));

  const transactionDateInput = document.getElementById("transaction_date");
  if (
    transactionDateInput &&
    typeof transactionDateInput.showPicker === "function"
  ) {
    const openTransactionDatePicker = () => {
      try {
        transactionDateInput.showPicker();
      } catch (error) {
        transactionDateInput.focus();
      }
    };

    transactionDateInput.addEventListener("click", () => {
      openTransactionDatePicker();
    });

    transactionDateInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openTransactionDatePicker();
      }
    });
  }

  document.querySelectorAll("select option").forEach((option) => {
    option.style.color = option.disabled ? "gray" : "white";
  });
});
