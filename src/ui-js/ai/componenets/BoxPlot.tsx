
import React from 'react';
import Plot from 'react-plotly.js';

export interface BoxPlotData {
    label: string;
    data: {
      min: number;
      q1: number;
      median: number;
      q3: number;
      max: number;
    }[];
  }

  export function BoxPlot(props: BoxPlotData) {
    const { label, data } = props;
    
    const trace = {
      y: data.map((d) => [d.min, d.q1, d.median, d.q3, d.max]),
      type: 'box',
      name: label,
      boxpoints: 'all',
      jitter: 0.5,
      whiskerwidth: 0.2,
      fillcolor: 'cls',
      marker: {
        size: 2
      },
      line: {
        width: 1
      }
    };
  
    const layout = {
      title: 'Box Plot',
      yaxis: {
        autorange: true,
        showgrid: true,
        zeroline: true,
        dtick: 5,
        gridcolor: 'rgb(255, 255, 255)',
        gridwidth: 1,
        zerolinecolor: 'rgb(255, 255, 255)',
        zerolinewidth: 2
      },
      margin: {
        l: 40,
        r: 30,
        b: 80,
        t: 100
      },
      paper_bgcolor: 'rgb(243, 243, 243)',
      plot_bgcolor: 'rgb(243, 243, 243)',
      showlegend: false
    };
    
    if (data.length === 0) {
      return <></>;
    }
    return (
      <Plot
        data={[trace]}
        layout={layout}
      />
    );
  }
