// calculator.js
document.addEventListener('DOMContentLoaded', function() {
    const calculatorForm = document.getElementById('calculatorForm');
    if (!calculatorForm) return;

    const widthInput = calculatorForm.querySelector('input[name="width"]');
    const lengthInput = calculatorForm.querySelector('input[name="length"]');
    const ceilingTypeSelect = calculatorForm.querySelector('select[name="ceiling_type"]');
    const resultsSection = document.getElementById('results');

    // Проверка, что элемент для результатов существует
    if (!resultsSection) {
        console.warn('Results section not found');
        return;
    }

    // Обновление результатов в DOM
    function updateResults(area, pricePerSqm, totalCost, productName) {
        const areaEl = document.getElementById('areaResult');
        const priceEl = document.getElementById('pricePerSqmResult');
        const totalEl = document.getElementById('totalCostResult');
        const productEl = document.getElementById('productNameResult');

        if (areaEl) areaEl.textContent = area.toFixed(2) + ' m²';
        if (priceEl) priceEl.textContent = `$${pricePerSqm.toFixed(2)}`;
        if (totalEl) totalEl.textContent = `$${totalCost.toFixed(2)}`;
        if (productEl) productEl.textContent = productName;

        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // AJAX сабмит формы
    calculatorForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Простая валидация
        const width = parseFloat(widthInput.value) || 0;
        const length = parseFloat(lengthInput.value) || 0;
        const ceilingType = ceilingTypeSelect.value;

        if (width <= 0 || length <= 0 || !ceilingType) {
            alert('Please fill all fields correctly.');
            return;
        }

        const formData = new FormData(calculatorForm);

        // Кнопка загрузки
        const submitBtn = calculatorForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Calculating...';
        submitBtn.disabled = true;

        fetch('', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updateResults(data.area, data.price_per_sqm, data.cost, data.product_name);
            } else {
                alert('Calculation failed. Please check inputs.');
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert('An error occurred. Please try again.');
        })
        .finally(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    });

    // Реальное время подсчёта при изменении полей
    function calculateLiveCost() {
        const width = parseFloat(widthInput.value) || 0;
        const length = parseFloat(lengthInput.value) || 0;
        const selectedOption = ceilingTypeSelect.selectedOptions[0];

        if (width > 0 && length > 0 && selectedOption) {
            const optionText = selectedOption.textContent;
            const priceMatch = optionText.match(/\$(\d+\.?\d*)/);
            if (priceMatch) {
                const pricePerSqm = parseFloat(priceMatch[1]);
                const area = width * length;
                const totalCost = area * pricePerSqm;
                updateResults(area, pricePerSqm, totalCost, selectedOption.textContent.split(' - ')[0]);
            }
        }
    }

    widthInput.addEventListener('input', debounce(calculateLiveCost, 300));
    lengthInput.addEventListener('input', debounce(calculateLiveCost, 300));
    ceilingTypeSelect.addEventListener('change', calculateLiveCost);

    // Debounce для оптимизации
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
});
