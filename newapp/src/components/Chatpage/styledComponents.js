import styled from "styled-components"

export const ChatContainer= styled.div`
    background-image: url('https://res.cloudinary.com/da00pyggy/image/upload/v1780423651/chat_bg_q2psr4.jpg');
    background-size: cover;
    min-height: 100vh;
    padding: 24px;
    color: #ffffff;
    font-family: roboto;
    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`
export const InputTab = styled.form`
    background-color: #ffffff61;
    border-radius: 30px;
    padding: 12px;
    margin-top: auto;
    width: 100%;
    text-align:left;
    display:flex;
    align-items:center;
`
export const InputBox = styled.input`
    width: 80%;
    border: 1px dotted transparent;
    outline: none;
    margin:0px;
    padding: 2px;
    color: #faf5f5;
    background-color: transparent;
    text-align:left;
    font-size: 16px;
    margin-left: 16px;

    &::placeholder{
        color: #faf5f5;
    }
`
export const EnterButn = styled.button`
    outline: none;
    cursor:pointer;
    background-color: transparent;
    border:0px;
    font-size: 24px;
    margin-left: auto;
    color: #ffffff;
`

export const MessagesContainer = styled.div`
    min-height: 100%;
    width: 100%;
    backgound-color: #36daf41f;
    color: #ffffff;
    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-end;
    margin-left: 24px;
    margin-right: 24px;
`