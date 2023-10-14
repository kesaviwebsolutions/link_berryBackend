const mongoose = require("mongoose");

mongoose.set("strictQuery", false);
mongoose.connect(
    //"mongodb+srv://kws:Ad9f7TMnsE72oD6x@cluster0.ks0jbmm.mongodb.net/BIF_?retryWrites=true&w=majority",  // Mainnet Database
    "mongodb+srv://kws:Ad9f7TMnsE72oD6x@cluster0.ks0jbmm.mongodb.net/ETHHackathon?retryWrites=true&w=majority",  // Developer Database
    // "mongodb://127.0.0.1:27017/mutualfund",
    {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    }
  )
  .then(() => {
    console.log("Database connection is setup with mongoDB");
  })
  .catch((e) => {
    console.log("there is no mongodb conenction", e);
  });
