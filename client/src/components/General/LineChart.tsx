import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
    ChartOptions,
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

type LineChartProps = {
    title: string;
    timesArray: number[];
    chartColor: string;
};

const LineChart = ({ title, timesArray, chartColor}: LineChartProps) => {
    const labels = Array.from(
        { length: timesArray.length },
        (_, index) => `Sample ${index + 1}`
    );

    const data = {
        labels,
        datasets: [
            {
                label: title,
                data: timesArray,
                borderColor: chartColor,
                backgroundColor: 'rgba(0, 0, 255, 0.1)',
                tension: 0.4,
            },
        ],
    };

    const options: ChartOptions<'line'> = {
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
                grid: {
                    display: false,
                },
            },
            y: {
                grid: {
                    display: true,
                },
                beginAtZero: true,
            },
        },
    };

    return <Line data={data} options={options} />;
};

export default LineChart;
