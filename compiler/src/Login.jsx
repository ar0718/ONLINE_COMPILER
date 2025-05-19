import Dialogbox from './comps/DialogBox'
import { use, useState } from 'react'
import { useEffect } from 'react'

const Login = () => {
    const jwt_token = localStorage.getItem('jwt')
    if(jwt_token){
        window.location.href = '/ide'
    }
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [count, setCount] = useState(0)
    const [data, setData] = useState('')
    const [info, setInfo] = useState('')
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
            const response = await fetch('http://127.0.0.1:8000/login/', {
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
    useEffect(() =>{
        if(data){
            if(data.error === ""){
                localStorage.setItem('jwt', data.jwt)
                window.location.href = '/ide'
            }
            else{
                console.log("chai")
                console.log(data.error)
                setInfo(data.error)
                setCount(0)
            }
        }
    },[data]);
    if(count === 0){
        return(
            <Dialogbox
            name="Login"
            title="Welcome back!"
            placeholder="Enter your Username"
            onSubmit = {cnt}
            handleChange = {hanChange}
            info = {info}
            /> 
        )
    }
    else if(count === 1){
        console.log(username)
        console.log(password)
        return(
            <Dialogbox
            name="Login"
            title="Welcome back!"
            placeholder="Enter your password"
            onSubmit = {cnt}
             handleChange = {hanChange}
            info = ""
             />
        )
    }
    
}
export default Login;