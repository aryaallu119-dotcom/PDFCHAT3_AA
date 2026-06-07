import styled from "styled-components"

export const MessageItemContainer = styled.div`
    margin-left: ${props => props.position === 'user' ? 'auto' : 'initial' } !important;
    margin-right: ${props => props.position === 'bot' ? 'auto' : ' initial'} !important;
    background-color:  rgba(0, 192, 251, 0.28);
    border-radius: ${props =>  props.position === 'bot' ? '18px 18px 18px 2px' : '18px 18px 2px 18px'} !important;
    padding: 0px 16px;
    word-break: break-word;
    overflow-wrap: break-word;
`