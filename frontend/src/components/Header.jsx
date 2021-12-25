
import React from "react";
// import { Heading, Flex, Divider } from "@chakra-ui/core";

import {Typography} from '@mui/material';

const Header = () => {
  return (
    <div>
      <Typography variant="h4" color='textPrimary'>
        UFC Fight Predictor
      </Typography>
      <span>&nbsp;&nbsp;</span>
    </div>
    
  );
};

export default Header;