const express = require("express");
const app = express();
const user = require("./src/User");
const tx = require("./src/transactions")
require("./src/database");
const cors = require("cors");
app.use(cors());

const PORT = 8001;


app.use(express.json());


app.get("/", async (req, res) => {
  res.send("API responce");
});

app.post("/join", async(req, res)=>{
    try {
        const data = new user(req.body)
        await data.save();
        res.send("done")
    } catch (error) {
        console.log(error)
    }   
})

app.post("/join/fillinguser", async(req, res)=>{
    try {
        const {username} = req.body
        const data = await user.findOneAndUpdate({userName:username}, req.body);
        res.status.send("update user")
    } catch (error) {
        console.log(error)
    }   
})

app.post("/join/findcode", async(req, res)=>{
    try {
        const { code } = req.body
        const removingfromInviter = await user.findOneAndUpdate({inviteCodes:code},{ $pull: { inviteCodes: code } });
        res.send("removed code")
    } catch (error) {
        console.log(error)
    }
})


app.post("/tradetx", async(req, res)=>{
    try {
        const data = new tx(req.body)
        await data.save()
        res.send("done")
    } catch (error) {
        console.log(error)
    }
})








app.listen(PORT, () => {
    console.log(`Sever is running on http://localhost:${PORT}`);
  });