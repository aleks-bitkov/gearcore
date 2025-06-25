function showAlert(message, type = 'dark-custom') {
  const container = document.getElementById('alert-container');
  const alert = document.createElement('div');

  alert.className = `alert alert-${type} alert-dismissible fade show mb-2 alert-dark-custom`;
  alert.role = 'alert';
  alert.innerHTML = `
    ${message}
    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

  container.appendChild(alert);

  // Удаление через 4 секунды
  setTimeout(() => {
    const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
    bsAlert.close();
  }, 4000);
}


