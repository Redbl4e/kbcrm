(async function () {
    const data = [
        {member: 'Решетнев', count_1: 10, count_2: 8},
        {member: 'Богданов', count_1: 20, count_2: 18},
        {member: 'Редько', count_1: 15, count_2: 10},
        {member: 'Аввакумов', count_1: 25, count_2: 18},
        {member: 'Базаев', count_1: 22, count_2: 15},
        {member: 'Иванов', count_1: 30, count_2: 30},
        {member: 'Белоус', count_1: 28, count_2: 28},
    ];

    new Chart(
        document.getElementById('test_chart_1'),
        {
            type: 'bar',
            data: {
                labels: data.map(row => row.member),
                datasets: [
                    {
                        label: 'Выполнено:',
                        backgroundColor: '#EEE8DA',
                        data: data.map(row => row.count_2)
                    },
                    {
                        label: 'Всего:',
                        backgroundColor: '#30627A',
                        data: data.map(row => row.count_1)
                    }
                ]
            }
        }
    );
})();

(async function () {
    new Chart(
        document.getElementById('test_chart_2'),
        {
            type: 'pie',
            data: {
                labels: [
                    'Выполнено',
                    'Не выполнено'
                ],
                datasets: [
                    {
                        label: 'Общая статистика',
                        data: [20, 10],
                        backgroundColor: [
                            '#EEE8DA',
                            '#30627A'
                        ]
                    }
                ]
            }
        }
    );
})();