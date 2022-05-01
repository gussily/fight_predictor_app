import React from "react";
import ".././styles.css";

import { Line, Bar } from "react-chartjs-2";
import {Container, Row, Col} from 'react-bootstrap'


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
            backgroundColor: "rgba(240, 93, 94)",
            borderColor: "rgba(75,192,192,1)"
          },
          {
            label: fighterData.fighter1,
            data: Object.values(fighterData.fighter1_stats),
            fill: true,
            backgroundColor: "rgba(15, 113, 115)",
            borderColor: "#02AAB0"
          }
        ]
    };
   
    if (! fighterData.fight_info_retrieved) {
        return(<></>)
    }
    return (

      <>
      
      <Container md={12} style={{paddingTop: '100px', paddingBottom: '30px'}}>

        <Row />

        <Row>
          <Col md={{ span: 10, offset: 1 }}>
        
            {/* <div className='BarCharts'> */}
                <Bar data={data} />
            {/* </div> */}
          </Col>
        </Row>

      </Container>

      </>
    );
}