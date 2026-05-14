function closeFilterModal(event) {
  if (event.target === document.getElementById("filterModal") || event.target === document.getElementById("closeModal")) {
      document.getElementById("filterModal").style.display = "none";
  }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("filter-button").addEventListener("click", function () {
      document.getElementById("filterModal").style.display = "block";
    });

    document.getElementById('clearFilters').addEventListener('click', function () {
      document.getElementById('filter-type').value = '';
      document.getElementById('filter-category').value = '';
      document.getElementById('filter-start-date').value = '';
      document.getElementById('filter-end-date').value = '';
      document.getElementById('filter-min-amount').value = '';
      document.getElementById('filter-max-amount').value = '';
      document.getElementById('filter-payment-method').value = '';
    });
});