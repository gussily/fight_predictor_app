import React, { useEffect, useState } from "react";


export const FighterContext = React.createContext({
    fighterData: '', fetchFighter: (fighterid) => {}
})


export default function FighterButton() {
    
    const [fighterData, setFighterData] = useState('test')
    const [fighter0id, setFighter0id] = useState("")
    const [fighter1id, setFighter1id] = useState("")

    const handleSubmit = async (event) => {

        // const response = await fetch("http://localhost:8000/items/?fighter=" + fighter0id)
        // const result = await response.json()
        // setFighterData(JSON.stringify(result.data))

        var fighter0 = fighter0id.split(' ').join('+');
        var fighter1 = fighter1id.split(' ').join('+');
        
        console.log(`http://localhost:8000/predict/?fighter0=${fighter0}&fighter1=${fighter1}`)
        const response = await fetch(`http://localhost:8000/predict/?fighter0=${fighter0}&fighter1=${fighter1}`)
        const result = await response.json()
        setFighterData(JSON.stringify(result.data))
    }
    

    useEffect(() => {
        // fetchTodos()
        // handleSubmit('0')
    }, [])

    
    return (
    <>
        <button onClick={ handleSubmit}> predict fight </button>
            <input
            onChange={(event) => {setFighter0id(event.target.value)}}
            />

            <input
            onChange={(event) => {setFighter1id(event.target.value)}}
            />
        
        {fighterData}
    </>
    )
}