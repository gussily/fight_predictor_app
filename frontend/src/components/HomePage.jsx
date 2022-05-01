import React, {useState, useEffect, useRef} from "react";

import Header from "./Header";
import FighterEntry from "./FighterEntry";
import BarCharts from "./BarChart";
import NavMenu from "./NavMenu";

export default function HomePage() {

    const [fighterData, setFighterData] = useState({error: '', winner: ''})
  
    const bottomRef = useRef(null)
  
    useEffect(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [fighterData])
  
    return (
      <div >
      
        <NavMenu />
        <FighterEntry fighterData={fighterData} setFighterData={setFighterData}/> 
        <BarCharts fighterData={fighterData}/>
        <div ref={bottomRef} />
  
      </div>
    )
  }