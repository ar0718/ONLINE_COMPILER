import './styles/AllProblems.css'
import {React, useState, useEffect} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCircleRight } from '@fortawesome/free-solid-svg-icons'
import { useNavigate } from 'react-router-dom'
import Navbar from './Navbar'
const calculateRate = (solved, tried) => {
  if (tried === 0) return { rate: 'N/A', color: 'var(--secondary-text)' }
  
  const percentage = Math.round((solved / tried) * 100)
  const hue = (percentage * 1.2)
  const color = `hsl(${hue}, 80%, 60%)`
  
  return { rate: `${percentage}%`, color }
}



const AllProblems = () => {
const navigate = useNavigate()
const [problems, setProblems] = useState([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState('')
useEffect (() => {
    fetchProblems()
},[])
    const fetchProblems = async () => {
        try{
            const response = await fetch('http://127.0.0.1:8000/get_problem/')
            if (!response.ok){
                setError('Failed to fetch problems')
            }
            else{
                const data = await response.json()
                setProblems(data.problems)
            }
            
        }
        finally{
            setLoading(false)
        }
    }
  if (loading) return <div className="loading">Loading problems...</div>
  if (error) return <div className="error">{error}</div>
 return (
    <div className="problems-container">
      <Navbar/>
      <h1>Practice Problems</h1>
      <div className="problems-list">
        {problems.map(problem => {
          return (
            <div 
              key={problem.problem_id} 
              className="problem-card"
            >
              <div className='important'>
                 <h2>{problem.title}</h2> 
              </div>
              
              <div className="problem-meta">
                <div>
                  <p> Trials </p>
                   <span className="attempted"> {problem.total_submissions}</span> 
                </div>
                <div>
                  <p>Solves</p>
                  <span className="solved"> {problem.solve_count}</span> 
                </div>
                <div>
                  <p>Rate</p>
                    {(() => {
                    const { rate, color } = calculateRate(problem.solve_count, problem.total_submissions)
                    return <span className='rate' style={{ color }}>{rate}</span>
                  })()}  
                </div>
              </div>
                <div className='solve' onClick={() => navigate(`/problem/${problem.problem_id}`)}> Solve Now! <FontAwesomeIcon icon={faCircleRight} /> </div> 
            </div>
          )
        })} 
      </div>
    </div>
  )
}
export default AllProblems