import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { Toaster } from 'sonner';
import { Button } from "@/components/ui/button";

import Landingpage from "./pages/Landingpage";
import Navbar from "./pages/Navbar";
import Footer from "./pages/Footer";
import Dashboard from "./pages/Dashboard";
import Transaction from "./pages/Transaction";
import Goal from "./pages/Goal";


function App() {
  return (
    <div>
      <Toaster position="top-right" richColors />
      <Navbar />
      <Routes>
        <Route path="/" element={<Landingpage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/transactions" element={<Transaction/>} />
        <Route path="/goal" element = {<Goal/>} />
      </Routes>
      <Footer />
    </div>
  );
}

export default App;
