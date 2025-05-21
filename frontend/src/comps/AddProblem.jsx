import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './styles/AddProblem.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCircleRight } from '@fortawesome/free-solid-svg-icons'
import { useEffect } from 'react'

const AddProblem = () => {

    const [title, setTitle] = useState('')
    const [description, setDescription] = useState('')
    const [input, setInput] = useState('')
    const [output, setOutput] = useState('')
    const [loading, setLoading] = useState(false)
    const jwt_token = localStorage.getItem('jwt')
    const [data, setData] = useState('')
    const [info, setInfo] = useState('')
    if(!jwt_token){
        window.location.href = '/login'
    }
    useEffect(() => {
        if(data.error === ""){
                // alert('problem added successfully')
                // window.location.href = '/addproblem'
                setInfo('problem added successfully')
        }
        else if(data.error){
            // alert('problem not added')
            // alert(data.error)
            setInfo(data.error)
        }
    }, [data]);

    function handleSubmit() {
        const fetchData = async () => {
            const response = await fetch('http://127.0.0.1:8000/add_problem/', {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                        title: title,
                        description: description,
                        input_format: input,
                        output_format: output,
                        jwt: jwt_token
                    })
                })
            const data1 = await response.json()
            console.log(data1)
            setData(data1)
        }
        setLoading(true)
        fetchData();
        setLoading(false)
        
    }
        
    
  return (
    <div className='add-problem'>
      <h1>Add Problem</h1>
      <input 
        type='text' 
        placeholder='Problem Title' 
        className='title'
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <div className='container'>
        <textarea 
          placeholder='Problem Description' 
          className='description'
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <div className='test-cases'>
          <textarea 
            placeholder='Test Inputs' 
            className='input'
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <textarea 
            placeholder='Expected Outputs' 
            className='output'
            value={output}
            onChange={(e) => setOutput(e.target.value)}
          />
        </div>
        <button 
          className='submit' 
        onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? 'Submitting...' : 'Submit'}
          <FontAwesomeIcon icon={faCircleRight} className='arrow-icon' />
        </button>
        <div className = "info">
            <h3>{info}</h3>
        </div>
      </div>
    </div>
  )
}

export default AddProblem