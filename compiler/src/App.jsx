
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Ide from './comps/Ide'
import Dialogbox from './comps/DialogBox'
import ReactDom from 'react-dom/client'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import Signup from './Signup'
import Login from './Login'
import Addproblem from './comps/Addproblem'
import AllProblems from './comps/AllProblems'
import Problem from './comps/Problem'

function App() {
  return (
    <BrowserRouter>
        <Routes>
          <Route path = "signup" element = {<Signup/>}/>
          <Route path = "/" element = {<Ide/>}/>
          <Route path = "ide" element = {<Ide/>}/>
          <Route path = "login" element = {<Login/>}/> 
          <Route path = "addproblem" element = {<Addproblem/>}/>
          <Route path = "allproblems" element = {<AllProblems/>}/>
          <Route path = "problem/:id" element = {<Problem/>}/> 
        </Routes>
    </BrowserRouter>
  )
}

export default App
