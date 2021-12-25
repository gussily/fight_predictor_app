import React, { useEffect, useState } from "react";
import {Button, TextField, Typography} from '@mui/material';
import {Container, Row, Col} from 'react-bootstrap'
import Stack from '@mui/material/Stack';
import Autocomplete from '@mui/material/Autocomplete';


export default function FighterEntry(props) {
    
    const fighterData = props.fighterData
    const setFighterData = props.setFighterData
    const [fighter0id, setFighter0id] = useState("")
    const [fighter1id, setFighter1id] = useState("")
    const [allFighters, setAllFighters] = useState()

    const handleSubmit = async (event) => {

        var fighter0 = fighter0id.split(' ').join('+');
        var fighter1 = fighter1id.split(' ').join('+');
        
        const response = await fetch(`http://localhost:8000/predict/?fighter0=${fighter0}&fighter1=${fighter1}`)
        const result = await response.json()
        setFighterData(result)
    }

    useEffect(async () => {
        const response = await fetch('http://localhost:8000/all-fighters')
        const result = await response.json()
        setAllFighters(result['all_fighters'])
    }, [])
    
    return (
    
    <div >
    <Container >
        <Row className="userInputs">
            <Col md={{ span: 3, offset: 3 }}>
                <div style={{display: 'flex', justifyContent: 'center'}}>
                    <Autocomplete className="align"
                        id="auto-1"
                        sx={{ width: 250 }}
                        freeSolo
                        options={allFighters}
                        onChange={(event, value) => {setFighter0id(value)}}
                        renderInput={(params) => <TextField {...params} label="Fighter 1" 
                            />}
                    />
                   
                </div>
            </Col>
            <Col md={{ span: 3, offset: 0 }}>
                <div style={{display: 'flex', justifyContent: 'center'}}>
                    <Autocomplete className="align"
                        id="auto-1"
                        sx={{ width: 250 }}
                        freeSolo
                        options={allFighters}
                        onChange={(event, value) => {setFighter1id(value)}}
                        renderInput={(params) => <TextField {...params} label="Fighter 2" 
                            />}
                    />
                </div>
            </Col>
        </Row>

        <Row>
            <Col md={{ span: 2, offset: 5 }}>
                <div style={{display: 'flex', justifyContent: 'center', paddingBottom: 20}}>
                    <Button 
                        variant="contained"
                        onClick={ handleSubmit}
                        size="large"> 
                        predict fight 
                    </Button>
                </div>
            </Col>
            
        </Row>

        <Row >
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <Typography variant="h5" color='secondary'>
                    Predicted Winner: {fighterData['winner']}
                </Typography>
            </div>
        </Row>
        
    </Container>
    </div>

        
    )
}