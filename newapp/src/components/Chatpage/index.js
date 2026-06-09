import {useState,useEffect,useRef} from "react"
import { useLocation } from "react-router-dom";
import { FaCircleArrowUp } from "react-icons/fa6";
import {MagnifyingGlass} from 'react-loader-spinner'
import {ChatContainer,InputTab,InputBox,MessagesContainer,EnterButn,LoadingContainer} from "./styledComponents"
import Message from "../Message"
const Chatpage = () =>{
    const {state} = useLocation()
    const [userInput,setUserInput] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef(null)
    const [responseMsgs,setResponseMsgs] = useState([])

    useEffect(()=>{
        console.log("Effect ran");
        setResponseMsgs(prev =>[
            ...prev,
            {
            id: Date.now(),
            message: state.query_response,
            sender: "bot"
            }])
        },[state.query_response])
    
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [responseMsgs])
    
    const inputChange =(event)=>{
        setUserInput(event.target.value)
    }

    const getResponseFromLLM =async (query)=>{
        setIsLoading(true)
        try{
            console.log("send request to nodejs(port 5000)")
            const response = await fetch(
                "http://localhost:5000/response",
                {
                    method: "POST",
                    headers:{
                        "Content-type": "application/json"
                    },
                    body: JSON.stringify({
                        query: query,
                        status: "False"
                    })
                }
            )
            console.log("got response from  nodejs(port 5000)")
            const data = await response.json();
            console.log("Response message:")
            console.log(data)
            setResponseMsgs(prev =>[
                ...prev,
                {
                id: Date.now(),
                message: data.response_msg,
                sender: data.sender
                }]
            )
        }catch (error){
            console.log(`Error at nodejs(port 5000): ${error}`)
        }finally{
            setIsLoading(false)
        }
        
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
                    <Message key={each.id} msgcontent={each.message} msgsource={each.sender}/>
                ))}
                {isLoading && (
                    <LoadingContainer>
                        <MagnifyingGlass  color="rgb(19, 18, 18)" height="40" width="40" />
                    </LoadingContainer>
                )}
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