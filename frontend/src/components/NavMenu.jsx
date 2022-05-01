import React from "react";
import {
  AppBar,
  Toolbar,
  CssBaseline,
  Typography,
} from "@mui/material";
import { makeStyles } from '@mui/styles';
import { Link } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  navlinks: {
    // marginLeft: theme.spacing(10),
    marginLeft: "20px",
    display: "flex",
  },
 logo: {
    flexGrow: "1",
    cursor: "pointer",
  },
  link: {
    textDecoration: "none",
    color: "white",
    fontSize: "20px",
    // marginLeft: theme.spacing(20),
    marginLeft: "20px",
    "&:hover": {
      color: "yellow",
      borderBottom: "1px solid white",
    },
  },
}));

function Navbar() {
  const classes = useStyles();

  return (
    <AppBar position="static">
      <CssBaseline />
      <Toolbar>
        <Typography variant="h4" className={classes.logo}>
          UFC Fight Predictor
        </Typography>

        <div className={classes.navlinks}>
          <Link to="/" className={classes.link}>
            Predict
          </Link>
          <Link to="/upcoming" className={classes.link}>
            Upcoming
          </Link>
          <Link to="/about" className={classes.link}>
            About
          </Link>
        </div>
      </Toolbar>
    </AppBar>
  );
}
export default Navbar;