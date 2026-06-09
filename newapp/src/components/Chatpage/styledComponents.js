import styled from "styled-components"

export const ChatContainer= styled.div`
    background-image: url('https://res.cloudinary.com/da00pyggy/image/upload/v1780423651/chat_bg_q2psr4.jpg');
    background-size: cover;
    height: 100vh;
    padding: 24px;
    color: #ffffff;
    font-family: roboto;
    display:flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    overflow: hidden;
`
export const InputTab = styled.form`
    background-color: #ffffff61;
    border-radius: 0px 0px 30px 30px;
    padding: 12px;
    width: 100%;
    text-align:left;
    display:flex;
    align-items:center;
    flex-shrink: 0;
`
export const InputBox = styled.input`
    width: 100%;
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
    flex: 1;
    width: 100%;
    background-color: #36dbf414;
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 12px;
    margin: 12px 24px;
    margin-bottom: 0px;
    padding: 12px;
    margin-bottom: 4px;
    border-radius: 8px 8px 0px 0px;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: none;
    -ms-overflow-style: none;
    
    &::-webkit-scrollbar {
        display: none;
    }
`

export const LoadingContainer = styled.div`
    width:79px;
    background-image: url('https://res.cloudinary.com/da00pyggy/image/upload/v1781030761/92e1bc06-9928-4eda-929e-c9b2e13f7ee7.png');
    background-size: cover;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding: 20px;
    margin: 8px;
    margin-top: 12px;
`