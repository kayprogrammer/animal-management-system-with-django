const ctx = document.getElementById('lineChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Monthly Milk Production Chart',
            data: [2050, 1900, 2100, 1800, 2800, 2000, 2500, 2600, 2450, 1950, 2300, 2900],
            backgroundColor: [
                'rgba(85,85,85,1)'
            ],
            borderColor: [
               
                'rgb(41,155,99)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive:true
        
    }
});