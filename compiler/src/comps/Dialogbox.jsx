import './styles/Dialogbox.css'
import {React, useState, useEffect, use} from 'react'
const Dialogbox = (props) => {
    const [input, setInput] = useState('')
    const [count, setCount] = useState(0)
    useEffect(() => {
        setInput('')
    }, [count])
    return(
        <div className="mainbox">
            <div className="logo">CodeIT!!</div>
            <div className="welcome">
                {props.title}
            </div>
            <div className="bigbox">
                <div className="register">
                    {props.name}
                </div>
                <input value = {input} placeholder = {props.placeholder} className="smallbox" onChange={(e) => {setInput(e.target.value); props.handleChange(input)}}/>
                <div className="terms">
                    By registering, you agree to our terms & conditions.
                </div>
                <button className="button" 
                    onClick = {() => {
                            if(input != ''){
                                props.handleChange(input)
                                const newcnt = count + 1
                                setCount(newcnt)
                                props.onSubmit(newcnt)

                            }
                        }
                    }  
                >
                    {console.log(count)}
                    Next
                </button>
                <div className="info">
                    {props.info}
                </div>
            </div>
        </div>
    )
}
export default Dialogbox