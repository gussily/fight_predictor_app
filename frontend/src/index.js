import React from "react";
import { render } from 'react-dom';
// import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";
import Todos from "./components/Todos";


function App() {
  return (
    <>
      <Header />
      <Todos />  {/* new */}
    </>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)