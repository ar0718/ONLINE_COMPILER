import Dialogbox from './comps/DialogBox'
import { use, useState } from 'react'
import { useEffect } from 'react'

const Signup = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [count, setCount] = useState(0)
    const [data, setData] = useState('')
    const cnt = (value) => {
        setCount(value)
    }
    const hanChange = (value) => {
        if(count === 0){
            setUsername(value)
        }
        else{
            setPassword(value)
        }   
    }
    useEffect(() => {
        if(count === 2){
        const fetchData = async () => {
            const response = await fetch('http://127.0.0.1:8000/signup/', {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                        username: username,
                        password: password
                    })
                })
            const data1 = await response.json()
            console.log(data1)
            setData(data1)
            }
            fetchData();
        }
    },[count]);
    if(count === 0){
        return(
            <Dialogbox
            name="Register"
            title="Welcome new User!"
            placeholder="Enter your Username"
            onSubmit = {cnt}
            handleChange = {hanChange}
            /> 
        )
    }
    else if(count === 1){
        console.log(username)
        console.log(password)
        return(
            <Dialogbox
            name="Register"
            title="Welcome new User!"
            placeholder="Enter your password"
            onSubmit = {cnt}
             handleChange = {hanChange}
             />
        )
    }
    else{
        return(
            <div>
                <h1>Welcome {username}</h1>
                <h1>{data.error}</h1>
                <h2>Your password is {password}</h2>
            </div>
        )
    }
    
}
export default Signup