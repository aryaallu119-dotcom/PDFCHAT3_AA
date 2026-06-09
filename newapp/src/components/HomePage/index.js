import {useNavigate} from "react-router-dom"
import {useState} from "react"
import {Watch} from 'react-loader-spinner'
import {FormContainer, FormElement,LoadingContainer,LoadingText,Heading,Labels,InputEle,SubmitButton} from "./styledComponents"
const Home =(props) =>{
    const navigate = useNavigate()
    const [topic,setTopic] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [file,setFile] = useState(null)
    const uploadingFile = async () =>{
        setIsLoading(true)
        try{
            console.log("uploading started")
            const formData = new FormData();
            formData.append("PDF",file)

            const response = await fetch(
                "http://localhost:5000/upload",
                {
                    method: "POST",
                    body: formData,
                }
            )
            console.log("uploaded file")
            const data = await response.json();
            console.log(data.query_response)
            navigate("/chat",{
                state:{
                    query_response: data.response_msg,
                    title: topic,
                }
            })
        }catch(error){
            console.log(`Error at uploadingfile: ${error}`)
        }finally{
            setIsLoading(false)
        }
        
    }
    const submission =  (event)=>{
        event.preventDefault()
        console.log("uploading")
        uploadingFile()
    }

    const topicChange =(event)=>{
        setTopic(event.target.value)
    }

    const loadingView = () =>(
            <LoadingContainer>
                <Watch  color="rgba(0, 192, 251, 0.28)" height="60" width="60" />
                <LoadingText>Processing PDF...</LoadingText>
            </LoadingContainer>
    )

    const renderInputForm = ()=>(
        <FormElement onSubmit={submission}>
            <Heading color="rgb(16, 189, 242)">DOCUCHART</Heading>
            <Labels htmlFor="topic">Enter the topic</Labels>
            <InputEle id="topic" type="text" onChange={topicChange} value={topic}/>
            <Labels htmlFor="File">Upload the File</Labels>
            <InputEle id="File" type="file" accept=".pdf" onChange={(e)=> setFile(e.target.files[0])}/>
            <SubmitButton to="/chat" type="submit">Submit</SubmitButton>
        </FormElement>
    )

    const getrender=()=>{
        if(isLoading){
            return loadingView()
        }else{
            return renderInputForm()
        }
    }

    return(
    <FormContainer>
        {getrender()}
    </FormContainer>
)

}
export default Home