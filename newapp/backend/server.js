const express = require("express");
const cors = require("cors")
const multer = require("multer")

const app = express()

app.use(cors())

const upload = multer({
    dest: "/Uploads"
})

app.get("/",(req,res)=>{
    res.send("Backend Working TNS....")
})

app.post("/upload",upload.single("PDF"),(req,res)=>{
    console.log(req.file)
    res.json({
        message: "File recieved",
        path: req.file.path
    })
})

app.listen(5000,()=>{
    console.log("Seerver is running at port: 5000")
})

