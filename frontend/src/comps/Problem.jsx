import {React, useState, useEffect} from 'react'
import {useParams} from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import Ide from './Ide'
import './styles/Problem.css'
import Navbar from './Navbar'
const Problem = () => {
    const  id = useParams()
    const [problem, setProblem] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    useEffect (() =>{
        fetchProblem()
    },[id])

    const fetchProblem = async () =>{
        try{
            const response = await fetch('http://127.0.0.1:8000/get_problem/')
            const data = await response.json()
            if(!response.ok){
                setError('failed to fetch problem')
            }
            else{
                // console.log(id)
                // console.log(data.problems)
                data.problems.forEach(function(item){
                    //console.log(item.problem_id)
                    if(item.problem_id === id.id){
                        console.log('ll')
                        setProblem(item)
                    }
                    else{
                         console.log(id)
                    }
                });
            }
        }
        finally{
            setLoading(false)
        }
    }
    if (loading) return <div className="loading">Loading problem...</div>
    if (error) return <div className="error">{error}</div>
    if (!problem) return <div className="error">Problem not found</div>
    return(
    <div className="problem-page">
        <Navbar/>
        <div className="problem-container">
            <div className="problem-details">
                <h1>{problem.title}</h1>
                <div className="meta">
                    <div className="stats">
                    <span className="solved">✓ {problem.solve_count} solved</span>
                    <span className="attempted">☆ {problem.total_submissions} attempts</span>
                    </div>
                </div>
                <div className="description-box">
                    <ReactMarkdown>{problem.description}</ReactMarkdown>
                </div>
            </div>
            <div className="ide-container">
                <Ide showSubmit ={true} problem_id={id.id}/>
            </div>
        </div>
    </div>
    )
}
export default Problem

