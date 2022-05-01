
import { Typography, CssBaseline } from '@mui/material';
import { makeStyles } from '@mui/styles';
import React from 'react';
import NavMenu from './NavMenu';

const useStyles = makeStyles((theme) => ({
    descpriptionText: {
        marginTop: "50px"

    }
}))

export default function About() {

    

    const classes = useStyles();

    return (
        <>
            <NavMenu />

            <CssBaseline />
        
            <Typography variant='h6' className={classes.descriptionText}>
                This predictor uses the ELO rating system to score fighters on various categories.
                Additionally it uses the logistic regression classifier to classify the result of the fight.
            </Typography>
        </>
    )
}