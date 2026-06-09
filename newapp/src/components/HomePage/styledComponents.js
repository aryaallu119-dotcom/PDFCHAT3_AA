import styled from "styled-components"

export const FormContainer = styled.div`
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-image: url('https://res.cloudinary.com/da00pyggy/image/upload/v1780422843/opoy7_obpl9c.jpg');
    background-size: cover;
`

export const FormElement = styled.form`
    display: flex;
    flex-direction: column;
    color: #ffffff;
    padding: 24px;
    border: 1px dashed rgb(16, 189, 242);
    border-radius: 8px;
    width: 400px;
`

export const LoadingText = styled.p`
    color:rgba(0, 192, 251, 0.28);
    text-align:center;
`
export const LoadingContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding: 20px;
    margin-top: 12px;
`

export const Heading = styled.h1`
    font-family: roboto;
    color: ${props => props.color};
`
export const Labels = styled.label`
    margin-bottom: 8px;
    text-align: start;
`
export const InputEle = styled.input`
    width:100%;
    background-color: rgba(16, 189, 242, 0.14) !important;
    border: 1px solid rgb(16, 189, 242);
    color: #ffffff;
    padding: 6px;
`

export const SubmitButton = styled.button`
    background-color: transparent;
    color: rgb(16, 189, 242);
    border: 1px solid rgb(16, 189, 242);
    padding: 4px;
    margin-top: 8px;
    border-radius: 4px;
    width: 30%;
    cursor: pointer;
`
