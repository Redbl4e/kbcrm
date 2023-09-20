let divisionCtx = document.getElementById('efficiencyDivision').getContext('2d')
let efficiencyDivision = new Chart(divisionCtx, {
    type: 'pie',
    options: {
        responsive: false,
    }
})

let usersCtx = document.getElementById("efficiencyUsers").getContext("2d");
let efficiencyUsers = new Chart(usersCtx, {
    type: 'bar',
    options: {
        responsive: false,
    }
});

function loadAllCharts(days) {
    loadChart(efficiencyUsers, `/api/user_tasks/${days}/`);
    loadChart(efficiencyDivision, `/api/division_tasks/${days}/`);
}

function loadChart(chart, endpoint) {
    $.ajax({
        url: endpoint, type: "GET", dataType: "json", success: (jsonResponse) => {
            console.log(jsonResponse)
            // Extract data from the response
            const title = jsonResponse.title;
            const labels = jsonResponse.data.labels;
            const datasets = jsonResponse.data.datasets;

            // Reset the current chart
            chart.data.datasets = [];
            chart.data.labels = [];

            console.log(chart.data)
            // Load new data into the chart
            chart.options.title.text = title;
            chart.options.title.display = true;
            chart.data.labels = labels;
            datasets.forEach(dataset => {
                chart.data.datasets.push(dataset);
            });
            chart.update();
        }, error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
    });
}

$(document).ready(function () {
    loadAllCharts(15)
})

