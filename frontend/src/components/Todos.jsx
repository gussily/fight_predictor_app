import React, { useEffect, useState } from "react";


export const FighterContext = React.createContext({
    fighterData: '', fetchFighter: (fighterid) => {}
})


export default function FighterButton() {
    
    const [fighterData, setFighterData] = useState('test')
    const [fighterid, setFighterid] = useState("")

    const handleSubmit = async (event) => {

        const response = await fetch("http://localhost:8000/items/?fighter=" + fighterid)
        const result = await response.json()
        setFighterData(JSON.stringify(result.data))
    }
    

    useEffect(() => {
        // fetchTodos()
        handleSubmit('0')
    }, [])

    
    return (
    <>
        <button onClick={ handleSubmit}> abc </button>
            <input
            onChange={(event) => {setFighterid(event.target.value)}}
            />
        
        {fighterData}
    </>
    )
}