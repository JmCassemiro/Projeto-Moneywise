document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.getElementById("edit-btn");
  const inputs = document.querySelectorAll(".info input");
  const title = document.querySelector("h2");
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

  let originalValues = [];
  let buttonWrapper = null;

  const cancelBtn = document.createElement("button");
  cancelBtn.textContent = "Cancelar";
  cancelBtn.classList.add("btn-cancelar");

  const saveBtn = document.createElement("button");
  saveBtn.textContent = "Salvar";
  saveBtn.classList.add("btn-salvar");

  cancelBtn.addEventListener("click", () => {
    title.firstChild.textContent = "Perfil";
    inputs.forEach((input, index) => {
      input.value = originalValues[index];
      input.disabled = true;
      input.style.backgroundColor = "#0F0F10";
      input.style.color = "#FFFFFF";
    });

    buttonWrapper.remove();
    buttonWrapper = null;
    editBtn.style.display = "inline";
  });

  saveBtn.addEventListener("click", () => {
    const [name, email, birthday] = [...inputs].map((input) => input.value);

    fetch("/profile/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ name, email, birthday }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert("Perfil atualizado com sucesso!");
          location.reload();
        } else {
          alert(data.message || "Erro ao atualizar perfil.");
        }
      })
      .catch(() => {
        alert("Erro ao atualizar perfil.");
      });
  });

  editBtn.addEventListener("click", () => {
    title.firstChild.textContent = "Editar Perfil";
    editBtn.style.display = "none";

    originalValues = Array.from(inputs).map((input) => input.value);
    inputs.forEach((input) => {
      input.disabled = false;
      input.style.backgroundColor = "#D9D9D9";
      input.style.color = "#000000";
    });

    buttonWrapper = document.createElement("div");
    buttonWrapper.classList.add("button-wrapper");
    buttonWrapper.appendChild(cancelBtn);
    buttonWrapper.appendChild(saveBtn);

    document.querySelector(".info").appendChild(buttonWrapper);
  });

  const deleteBtn = document.getElementById("delete-account-btn");
  const deleteModal = document.getElementById("delete-confirm-modal");
  const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
  const flashMessage = document.querySelector(".flash-message");
  const deleteErrorMessage = document.querySelector("#delete-error-message");
  const passwordField = document.querySelector("#delete-account-confirm-form input[type='password']");

  if (flashMessage) {
    deleteModal.style.display = "block";
  }

  if (deleteBtn) {
    deleteBtn.addEventListener("click", (event) => {
      event.preventDefault();
      deleteModal.style.display = "block";
    });
  }

  if (cancelDeleteBtn) {
    cancelDeleteBtn.addEventListener("click", () => {
      deleteModal.style.display = "none";

      if (deleteErrorMessage) {
        deleteErrorMessage.style.display = "none";
      }

      if (passwordField) {
        passwordField.value = "";
      }
    });
  }
});
