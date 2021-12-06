import React, {useState} from "react";
import { render } from 'react-dom';
// import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";
import FighterEntry from "./components/FighterEntry";
import BarCharts from "./components/BarChart";

function App() {

  const [fighterData, setFighterData] = useState({error: '', winner: ''})

  return (
    <>
      <Header />
      <FighterEntry fighterData={fighterData} setFighterData={setFighterData}/> 
      <BarCharts fighterData={fighterData}/>
    </>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)