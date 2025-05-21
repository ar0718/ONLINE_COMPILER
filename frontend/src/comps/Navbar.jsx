import React from 'react'
import './styles/Navbar.css'
const Navbar = () =>{
    return(
        <div className = "navbar">
            <ul>
                <li><a href="/">IDE</a></li>
                <li><a href="/addproblem">Add-Problem</a></li>
                <li><a href="/allproblems">Practice-Problems</a></li>
                <li><a href="/login">Login</a></li>
                <li><a href="/signup">Sign-Up</a></li>
            </ul>

        </div>
    )
}
export default Navbar