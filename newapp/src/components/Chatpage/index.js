import {useState,useEffect,useRef} from "react"
import { useLocation } from "react-router-dom";
import { FaCircleArrowUp } from "react-icons/fa6";
import {ChatContainer,InputTab,InputBox,MessagesContainer,EnterButn} from "./styledComponents"
import Message from "../Message"
const Chatpage = () =>{
    const {state} = useLocation()
    const [userInput,setUserInput] = useState("")
    const messagesEndRef = useRef(null)
    const [responseMsgs,setResponseMsgs] = useState([{
        id:1780853165270,
        message: "Hi! which topic are you intrested in given PDF!....",
        sender: "bot"
    }])

    useEffect(()=>{
        console.log("Effect ran");
        setResponseMsgs(prev =>[
            ...prev,
            {
            id: Date.now(),
            message: state.responseText,
            sender: "bot"
            }])
        },[state.responseText])
    
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [responseMsgs])
    
    const inputChange =(event)=>{
        setUserInput(event.target.value)
    }

    const getResponseFromLLM =async (query)=>{
        console.log("send request to nodejs(port 5000)")
        const response = await fetch(
            "http://localhost:5000/response",
            {
                method: "POST",
                headers:{
                    "Content-type": "application/json"
                },
                body: JSON.stringify({
                    query: query
                })
            }
        )
        console.log("got response from  nodejs(port 5000)")
        const data = await response.json();
        console.log("Response message:")
        console.log(data)
    }

    const onEnterInput = (event)=>{
        event.preventDefault()
        getResponseFromLLM(userInput)
        setResponseMsgs(prev =>[
            ...prev,
            {
            id: Date.now(),
            message: userInput,
            sender: "user"
            }
        ])
        setUserInput("")
    }


    return(
        <ChatContainer>
            <h1>{state.title}</h1>
            <MessagesContainer>
                {responseMsgs.map(each => (
                    <Message key={each.id} msgcontent={each.message} Msgsource={each.sender}/>
                ))}
                <div ref={messagesEndRef} />
            </MessagesContainer>
            <InputTab onSubmit={onEnterInput}>
                <InputBox 
                    type="text" 
                    placeholder="Ask Anything about PDF..." 
                    onChange={inputChange} value={userInput}
                />
                {userInput !== "" && <EnterButn type="submit"><FaCircleArrowUp /></EnterButn>}
            </InputTab>
        </ChatContainer>
    )
}

export default Chatpage