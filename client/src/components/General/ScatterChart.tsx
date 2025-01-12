import { Scatter } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
    ChartOptions,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, Tooltip, Legend);

type ScatterChartProps = {
    title: string;
    timesArray: number[];
    chartColor: string;
};

const ScatterChart = ({ title, timesArray, chartColor }: ScatterChartProps) => {
    const scatterData = timesArray.map((time, index) => ({
        x: index + 1,
        y: time,
    }));

    const data = {
        datasets: [
            {
                label: title,
                data: scatterData,
                backgroundColor: chartColor,
            },
        ],
    };

    const options: ChartOptions<'scatter'> = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                enabled: true,
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Sample Index',
                },
                grid: {
                    display: false,
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Time Value (ms)',
                },
                grid: {
                    display: true,
                },
                beginAtZero: true,
            },
        },
    };

    return <Scatter data={data} options={options} />;
};

export default ScatterChart;
