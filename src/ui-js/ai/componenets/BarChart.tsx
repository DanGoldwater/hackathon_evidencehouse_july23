import React from 'react';
import Plot from 'react-plotly.js';

type BarChartProps = {
  data: number[];
  labels: string[];
};

const BarChart: React.FC<BarChartProps> = ({ data, labels }) => {

  const plotData = [
    {
      x: labels,
      y: data,
      type: 'bar',
      marker: {
        color: 'blue'
      },
    }
  ];

  const layout = {
    title: 'Bar Chart',
    width: 500,
    height: 500,
  };

  return (
    <Plot
      data={plotData}
      layout={layout}
    />
  );
};

export default BarChart;