import React from 'react'
import Ide from './comps/Ide.jsx'
import Navbar from './comps/Navbar.jsx'
import './comps/styles/Home.css'
function Home() {
  return (
    <div className="home">
        <div className="header1">
            <Navbar/>
        </div>
        <div className="idq">
            <Ide/>
        </div>
    </div>
  )
}

export default Home