const axios =require("axios")
const express = require("express");
const cors = require("cors")
const multer = require("multer")
const fs = require("fs");



const app = express()
let topicName = null;

app.use(cors())

const storage = multer.diskStorage({
    destination: (req,file,cb)=>{
        const topic = req.params.topic;
        topicName = topic
        console.log(topic)

        const folderName =topic
            .trim()
            .toLowerCase()
            .replace(/\s+/g, "_")
        console.log(folderName)
        const dir = `Uploads/${folderName}`

        if (!fs.existsSync(dir)){
            fs.mkdirSync(dir,{recursive:true})
        }
        cb(null,dir)
    },
    filename: (req,file,cb) =>{
        cb(null, file.originalname)
    }
})

const upload = multer({ storage })

app.use(express.json())

app.get("/",(req,res)=>{
    res.send("Backend Working TNS....")
})

app.post("/upload/:topic",upload.single("PDF"),async (req,res)=>{
    // console.log(req.file.path);
    const pdfPath = req.file.path;
    const {session_id}= req.body
    console.log(session_id)
    try{
        const response = await axios.post(
            "https://pdfchat-143.onrender.com/process",
            {
                pdf_path: pdfPath,
                topic: topicName,
                session_id: session_id
            }
        );
        res.json(response.data);
    }catch (error){
        console.log(`Error at server.js API call:${error}`)
        res.status(500).json({
            error: "Failed to process PDF",
            details: error.message
        })
    }
    
})


app.post("/response",async (req,res)=>{
    console.log(req.body.status)
    const {session_id, topic_name}= req.body
    console.log("send request to python(port 8000)")
    try{
        const response = await axios.post(
            "https://pdfchat-143.onrender.com/response",
            {
                query: req.body.query,
                status:req.body.status,
                session_id: session_id,
                topic_name: topic_name
            }
        );
        console.log(response.data)
        if(response.data.sender === 'error'){
            throw new Error("Tokens Limit occered!")
        }
        res.json(response.data)
    }catch(error){
        console.log(`Error at server.js API call:${error}`)
        res.status(500).json({
            error: "Python service call failed",
            details: error
        })
    }
})

app.listen(5000,()=>{
    console.log("Seerver is running at port: 5000")
})

