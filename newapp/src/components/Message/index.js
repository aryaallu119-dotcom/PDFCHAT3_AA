import {MessageItemContainer} from "./styledComponents"
const Message = props =>{
    const {msgcontent,Msgsource} =props
    return(
        <MessageItemContainer position = {Msgsource}>
            <p>{msgcontent}</p>
        </MessageItemContainer>
    )

}

export default Message