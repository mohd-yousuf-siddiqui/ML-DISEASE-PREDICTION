document.addEventListener('DOMContentLoaded', function() {
    console.log('Disease Prediction System initialized');
    
    // Show loading spinner during form submission
    const forms = document.querySelectorAll('form');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            if (form.checkValidity()) {
                if (loadingSpinner) {
                    loadingSpinner.classList.add('show');
                }
            }
        });
    });
    
    // Range slider value display
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    
    rangeInputs.forEach(input => {
        const output = document.getElementById(input.id + '-value');
        
        if (output) {
            // Set initial value
            output.textContent = input.value;
            
            // Update value on change
            input.addEventListener('input', function() {
                output.textContent = this.value;
            });
        }
    });
    
    // Initialize charts if on results page
    if (document.getElementById('probabilityChart')) {
        initCharts();
    }
    
    // BMI Calculator for Diabetes Form
    const weightInput = document.getElementById('weight');
    const heightInput = document.getElementById('height');
    const bmiInput = document.getElementById('bmi');
    const bmiResult = document.getElementById('bmi-result');
    
    if (weightInput && heightInput && bmiInput) {
        const calculateBMI = function() {
            const weight = parseFloat(weightInput.value);
            const height = parseFloat(heightInput.value) / 100; // convert cm to m
            
            if (weight > 0 && height > 0) {
                const bmi = (weight / (height * height)).toFixed(1);
                bmiInput.value = bmi;
                
                if (bmiResult) {
                    bmiResult.textContent = bmi;
                    
                    // Add BMI category
                    let category = '';
                    if (bmi < 18.5) {
                        category = 'Underweight';
                    } else if (bmi < 25) {
                        category = 'Normal weight';
                    } else if (bmi < 30) {
                        category = 'Overweight';
                    } else {
                        category = 'Obese';
                    }
                    
                    bmiResult.textContent += ' (' + category + ')';
                }
            }
        };
        
        weightInput.addEventListener('input', calculateBMI);
        heightInput.addEventListener('input', calculateBMI);
    }
});

// Initialize Charts.js charts
function initCharts() {
    // Get prediction probability from data attribute
    const probabilityElement = document.getElementById('prediction-probability');
    const probability = parseFloat(probabilityElement.dataset.probability);
    const predictionType = probabilityElement.dataset.type;
    
    // Probability chart
    const probCtx = document.getElementById('probabilityChart').getContext('2d');
    
    // Define colors based on prediction type
    let colors = {
        heart: {
            primary: '#dc3545',
            secondary: 'rgba(220, 53, 69, 0.2)'
        },
        diabetes: {
            primary: '#6f42c1',
            secondary: 'rgba(111, 66, 193, 0.2)'
        },
        pneumonia: {
            primary: '#fd7e14',
            secondary: 'rgba(253, 126, 20, 0.2)'
        }
    };
    
    const selectedColor = colors[predictionType] || colors.heart;
    
    new Chart(probCtx, {
        type: 'doughnut',
        data: {
            labels: ['Risk', 'Safe'],
            datasets: [{
                data: [probability * 100, (1 - probability) * 100],
                backgroundColor: [
                    selectedColor.primary,
                    selectedColor.secondary
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.raw.toFixed(1) + '%';
                        }
                    }
                }
            }
        }
    });
    
    // Add center text inside donut chart
    const probChart = document.getElementById('probabilityChart');
    const probContainer = probChart.parentElement;
    
    const centerText = document.createElement('div');
    centerText.style.position = 'absolute';
    centerText.style.top = '50%';
    centerText.style.left = '50%';
    centerText.style.transform = 'translate(-50%, -50%)';
    centerText.style.textAlign = 'center';
    centerText.style.pointerEvents = 'none';
    
    const percentText = document.createElement('div');
    percentText.style.fontSize = '2rem';
    percentText.style.fontWeight = 'bold';
    percentText.textContent = (probability * 100).toFixed(1) + '%';
    
    const riskText = document.createElement('div');
    riskText.style.fontSize = '1rem';
    riskText.textContent = 'Risk';
    
    centerText.appendChild(percentText);
    centerText.appendChild(riskText);
    
    probContainer.style.position = 'relative';
    probContainer.appendChild(centerText);
}
