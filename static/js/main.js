// FoodExpress - Main JS

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });
});

// Confirm before destructive actions (handled inline via onclick)
// Quantity input: prevent values below 0
document.querySelectorAll('input[type="number"]').forEach(function (input) {
    input.addEventListener('change', function () {
        if (parseInt(this.value) < 0) this.value = 0;
    });
});
