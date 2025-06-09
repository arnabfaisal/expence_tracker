import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

import { Button } from "@/components/ui/button";

import Landingpage from "./pages/Landingpage";
import Navbar from "./pages/Navbar";
import Footer from "./pages/Footer";
import Dashboard from "./pages/Dashboard";
function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Landingpage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
      <Footer />
    </div>
  );
}

export default App;
