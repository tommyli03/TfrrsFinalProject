import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavigationBar from "./components/NavigationBar";
import XCHomePage from "./components/XCHomePage";
import "./App.css"

const App = () => {
  return (
    <Router>
      <div>
        {/* Navigation Bar */}
        <NavigationBar />
        
        {/* Define Routes */}
        <Routes>
          <Route path="/" element={<XCHomePage />} /> 
          <Route path="/track" element={<div>Track Data Coming Soon!</div>} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
