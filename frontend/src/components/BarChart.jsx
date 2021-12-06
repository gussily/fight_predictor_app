import React from "react";
import ".././styles.css";

import { Line, Bar } from "react-chartjs-2";

// fixes an error
import Chart from 'chart.js/auto'





export default function BarCharts(props) {

    const fighterData = props.fighterData

    // return(<></>)
    const data = !fighterData.fight_info_retrieved ? {} : {
        labels: fighterData.fighter_stats,
        datasets: [
          {
            label: fighterData.fighter0,
            data: Object.values(fighterData.fighter0_stats),
            fill: true,
            backgroundColor: "rgba(87, 115, 153)",
            borderColor: "rgba(75,192,192,1)"
          },
          {
            label: fighterData.fighter1,
            data: Object.values(fighterData.fighter1_stats),
            fill: true,
            backgroundColor: "rgba(189, 213, 234)",
            borderColor: "#02AAB0"
          }
        ]
    };
   
    if (! fighterData.fight_info_retrieved) {
        return(<></>)
    }
    return (
    <div className='BarCharts'>
        <Bar data={data} />
    </div>
    );
}