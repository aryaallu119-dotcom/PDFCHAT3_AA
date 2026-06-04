import {useState} from "react"
import { FaCircleArrowUp } from "react-icons/fa6";
import {ChatContainer,InputTab,InputBox,MessagesContainer,EnterButn} from "./styledComponents"
const Chatpage = () =>{
    const [userInput,setUserInput] = useState("")
    const inputChange =(e)=>{
        console.log(e.target.value)
        setUserInput(e.target.value)
    }
    return(
        <ChatContainer>
            <h1>Chat page</h1>
            <MessagesContainer>
                <p>hlo</p>
            </MessagesContainer>
            <InputTab>
                <InputBox 
                    type="text" 
                    placeholder="Ask Anything about PDF..." 
                    onChange={inputChange} value={userInput}
                />
                {userInput !== "" && <EnterButn><FaCircleArrowUp /></EnterButn>}
            </InputTab>
        </ChatContainer>
    )
}

export default Chatpage