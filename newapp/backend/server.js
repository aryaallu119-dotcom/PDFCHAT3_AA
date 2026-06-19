require("dotenv").config({
    path: "./.env"
});
const FormData = require("form-data");
const axios =require("axios")
const express = require("express");
const cors = require("cors")
const multer = require("multer")
const streamifier = require("streamifier");
const cloudinary = require("./config/cloudinary");




const app = express()

app.use(cors())

const storage = multer.memoryStorage();

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 500 * 1024 * 1024  // 500MB
    }
});

app.use(express.json())



app.get("/",(req,res)=>{
    res.send("Backend Working TNS....")
})

// app.post("/upload/:topic", upload.single("PDF"), async (req,res)=>{
//     console.log("========== FILE ==========");
//     console.log(JSON.stringify(req.file, null, 2));
//     const pdfPath = req.file.path;
//     const {session_id}= req.body
//     const topicName = req.params.topic;
//     console.log(session_id)
//     try{
//         const response = await axios.post(
//             "http://localhost:8000/process",
//             {
//                 pdf_path: pdfPath,
//                 topic: topicName,
//                 session_id: session_id
//             }
//         );
//         res.json(response.data);
//     }catch(error){
//         console.log("========== ERROR ==========");

//         console.log(error.message);

//         if(error.response){
//             console.log(error.response.data);
//         }

//         console.log(error.stack);

//         res.status(500).json({
//             error:"Failed to process PDF",
//             details:error.message
//         });

//     }
    
// })

app.post("/upload/:topic", upload.single("PDF"), async (req, res) => {

    try {

        const session_id = req.body.session_id;
        const topicName = req.params.topic;

        console.log("Session:", session_id);
        console.log("Topic:", topicName);

        const MAX_CLOUDINARY_SIZE = 10 * 1024 * 1024; // 10 MB

        let uploadResult = null;

        if (req.file.size <= MAX_CLOUDINARY_SIZE) {

            uploadResult = await new Promise((resolve, reject) => {

                const stream = cloudinary.uploader.upload_stream(
                    {
                        folder: `pdf_chatbot/${topicName}`,
                        resource_type: "raw",
                        public_id: Date.now().toString()
                    },
                    (error, result) => {

                        if (error) {
                            return reject(error);
                        }

                        resolve(result);
                    }
                );

                streamifier
                    .createReadStream(req.file.buffer)
                    .pipe(stream);

            });

            console.log("✅ Uploaded to Cloudinary");
            console.log("Cloudinary URL:");
            console.log(uploadResult.secure_url);

        } else {

            console.log("⚠️ File size exceeds 10 MB. Skipping Cloudinary upload.");

        }

    
        
        const form = new FormData();

        form.append("pdf", req.file.buffer, {
            filename: req.file.originalname,
            contentType: req.file.mimetype
        });

        form.append("topic", topicName);

        form.append("session_id", session_id);
        // console.log("******************Formdata:")
        // console.log(form);

        const response = await axios.post(
            "http://localhost:8000/process",
            form,
            {
                headers: form.getHeaders()
            }
        );

        res.json(response.data);

    } catch (error) {

        console.log("========== ERROR ==========");

        console.log(error.message);

        if (error.response) {
            console.log(error.response.data);
        }

        console.log(error);

        res.status(500).json({
            error: "Failed to process PDF",
            details: error.message
        });

    }

});


app.post("/response",async (req,res)=>{
    console.log(req.body.status)
    const {session_id, topic_name}= req.body
    console.log("send request to python(port 8000)")
    try{
        const response = await axios.post(
            "http://localhost:8000/response",
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
    console.log("Server is running at port: 5000")
})

