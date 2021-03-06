var h_title = 'Время';

function drawChart() {
    var data = google.visualization.arrayToDataTable([
    [h_title, v_title],
    ['2013',  1000],
    ['2014',  1170],
    ['2015',  660],
    ['2016',  1030]
]);

var options = {
    title: title_chart,
    colors: [color_chart],
    titleTextStyle: {
        italic: true,
        bold: false,
        fontSize: 20
    },
    hAxis: {
        title: h_title,
        titleTextStyle: {
            color: '#000',
            fontSize: 20
        },
        textStyle: {
            fontSize: 16
        },
    },
    legend: {position: 'none'},
    chartArea: {'width': '96%', 'height': '80%',},
    vAxis: {
        titleTextStyle: {
            color: '#000'
        },
        textStyle: {
            fontSize: 16
        },
        textPosition: 'in',
        viewWindowMode: 'pretty'
    }
};

var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
