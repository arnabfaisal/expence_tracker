
import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "chartjs-adapter-date-fns";

ChartJS.register(
  CategoryScale,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function LineChart({ incomeData, expenseData, totalData }) {
  const laal = getComputedStyle(document.documentElement).getPropertyValue('--color-laal').trim();
  const shobuj = getComputedStyle(document.documentElement).getPropertyValue('--color-shobuj').trim();
  const maati = getComputedStyle(document.documentElement).getPropertyValue('--color-maati').trim();




  
  const data = {
    datasets: [
      {
        label: "Income",
        data: incomeData,
        borderColor: laal,
        backgroundColor: laal,
        tension: .4,
        fill: false,
      },
      {
        label: "Expense",
        data: expenseData,
        borderColor: shobuj,
        backgroundColor: shobuj,
        tension: 0.4,
        fill: false,
      },
      {
        label: "Total",
        data: totalData,
        borderColor: maati,
        backgroundColor: maati,
        tension: 0.4,
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: "Income vs Expense vs Total",
      },
    },
    scales: {
      x: {
        type: "time",
        time: {
          unit: "minute",
          tooltipFormat: "PPpp",
          displayFormats: {
            minute: "HH:mm",
            second: "HH:mm:ss",
          },
        },
        title: {
          display: true,
          text: "Time",
        },
      },
      y: {
        title: {
          display: true,
          text: "Amount ($)",
        },
        beginAtZero: true,
      },
    },
  };

  return <Line options={options} data={data} />;
}

export default LineChart;
