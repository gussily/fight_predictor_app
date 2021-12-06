import React, { useEffect, useState } from "react";
import {Button, TextField, Typography} from '@mui/material';

export const FighterContext = React.createContext({
    fighterData: '', fetchFighter: (fighterid) => {}
})


export default function FighterEntry(props) {
    
    const fighterData = props.fighterData
    const setFighterData = props.setFighterData
    const [fighter0id, setFighter0id] = useState("")
    const [fighter1id, setFighter1id] = useState("")

    const handleSubmit = async (event) => {

        var fighter0 = fighter0id.split(' ').join('+');
        var fighter1 = fighter1id.split(' ').join('+');
        
        const response = await fetch(`http://localhost:8000/predict/?fighter0=${fighter0}&fighter1=${fighter1}`)
        const result = await response.json()
        setFighterData(result)
    }
    

    useEffect(() => {
        // fetchTodos()
        // handleSubmit('0')
    }, [])

    
    return (
    <>
        
        <TextField
            label="Fighter 1"
            onChange={(event) => {setFighter0id(event.target.value)}}
        />
        <TextField
            label="Fighter 2"
            onChange={(event) => {setFighter1id(event.target.value)}}
        />
        <div>
            <Button 
                variant="contained"
                onClick={ handleSubmit}> 
                predict fight 
            </Button>
        </div>
        
        
        {/* {JSON.stringify(fighterData)} */}
        <span>&nbsp;&nbsp;</span>

        <Typography variant="h5" color='secondary'>
            Predicted Winner: {fighterData['winner']}
        </Typography>
    </>
    )
}