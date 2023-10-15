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
        const { userName } = req.body
        const isuser = await user.findOne({userName:userName});
        console.log(isuser)
        if(isuser){
            return res.status(500).send("User already exist")
        }
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
        console.log("User", username)
        const data = await user.findOneAndUpdate({userName:username}, req.body);
        res.send("update user")
    } catch (error) {
        console.log(error)
    }   
})

app.get("/users/all", async(req, res)=>{
    try {
        const data = await user.find();
        res.send(data)
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

app.post("/user/getuser", async(req, res)=>{
    try {
        const { username } = req.body
        const data = await user.findOne({userName:username});
        res.send(data)
    } catch (error) {
        console.log(error)
    }
})

app.post("/user/buy/holdings", async(req, res)=>{
    try {
        const { myusername, boughtusername, units } = req.body
        const hodlingdata = await user.findOneAndUpdate({userName:myusername}, {$push : {holdings: {user:boughtusername, value:units}}});
        const holdersdata = await user.findOneAndUpdate({userName:boughtusername}, {$push : {holders: {user:myusername, value:units}}});
        res.send("done")
    } catch (error) {
        console.log(error)
    }
})
app.post("/user/buysell/tx", async(req, res)=>{
    try {
        const { myusername, method, boughtusername, units } = req.body
        const hodlingdata = await user.findOneAndUpdate({userName:myusername},{$push : {userTx: {user:boughtusername, value:units, method:method}}});
        res.send("done")
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