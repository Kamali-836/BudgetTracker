function fetchData() {
  fetch('/api/data')
    .then(res => res.json())
    .then(data => {
      document.getElementById("total-budget").innerText = data.budget.toFixed(2);
      document.getElementById("total-expenses").innerText = data.total_expense.toFixed(2);
      document.getElementById("budget-left").innerText = data.budget_left.toFixed(2);

      const table = document.getElementById("expense-table");
      table.innerHTML = "";
      data.expenses.forEach(e => {
        const row = `<tr>
          <td>${e.title}</td>
          <td>${e.amount.toFixed(2)}</td>
          <td><button onclick="deleteExpense(${e.id})" class="remove-btn">Remove</button></td>
        </tr>`;
        table.innerHTML += row;
      });
    });
}

function addBudget() {
  const value = parseFloat(document.getElementById("budget-input").value);
  if (!isNaN(value)) {
    fetch('/api/add_budget', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({amount: value})
    }).then(() => {
      document.getElementById("budget-input").value = '';
      fetchData();
    });
  }
}

function addExpense() {
  const title = document.getElementById("expense-name").value;
  const amount = parseFloat(document.getElementById("expense-amount").value);
  if (title && !isNaN(amount)) {
    fetch('/api/add_expense', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({title, amount})
    }).then(() => {
      document.getElementById("expense-name").value = '';
      document.getElementById("expense-amount").value = '';
      fetchData();
    });
  }
}

function resetBudget() {
  fetch('/api/reset_budget', { method: 'DELETE' })
    .then(() => fetchData());
}

function deleteExpense(id) {
  fetch(`/api/delete_expense/${id}`, { method: 'DELETE' })
    .then(() => fetchData());
}

window.onload = fetchData;
