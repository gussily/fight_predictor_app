
import React, {useState, useEffect, useRef} from "react";
import { render } from 'react-dom';
// import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";
import FighterEntry from "./components/FighterEntry";
import BarCharts from "./components/BarChart";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'mdb-react-ui-kit/dist/css/mdb.min.css';


function App() {

  const [fighterData, setFighterData] = useState({error: '', winner: ''})

  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [fighterData])

  return (
    
    
    <div >
    

      <Header />
      <FighterEntry fighterData={fighterData} setFighterData={setFighterData}/> 
      <BarCharts fighterData={fighterData}/>
      <div ref={bottomRef} />

      
    </div>

    

    
  
    
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)