import {useNavigate} from "react-router-dom"
import {useState} from "react"
import {FormContainer, FormElement,Heading,Labels,InputEle,SubmitButton} from "./styledComponents"
const Home =(props) =>{
    const navigate = useNavigate()
    const [file,setFile] = useState(null)
    const uploadingFile = async () =>{
        const formData = new FormData();
        formData.append("PDF",file)

        const response = await fetch(
            "http://localhost:5000/upload",
            {
                method: "POST",
                body: formData,
            }
        )

        const data = await response.json();
        
        console.log(data);
    }
    const submission =  (event)=>{
        event.preventDefault()
        console.log("submitted")
        console.log(file)
        navigate("/chat")
        uploadingFile()
    }

    return(
    <FormContainer>
        <FormElement onSubmit={submission}>
            <Heading color="rgb(16, 189, 242)">DOCUCHART</Heading>
            <Labels htmlFor="topic">Enter the topic</Labels>
            <InputEle id="topic" type="text"/>
            <Labels htmlFor="File">Upload the File</Labels>
            <InputEle id="File" type="file" accept=".pdf" onChange={(e)=> setFile(e.target.files[0])}/>
            <SubmitButton to="/chat" type="submit" >Submit</SubmitButton>
        </FormElement>
    </FormContainer>
)

}
export default Home