const mongoose = require("mongoose");

const Super_Admin = new mongoose.Schema({
  wallet_Address: {
    type: String,
    required: false,
  },
  hash:{
    type: String,
    required: false,
  },
  timeAt:{
    type: Number,
    required: false,
  },
  txType:{
    type: String,
    required: false,
  }
});
const EventModel = new mongoose.model("transactions", Super_Admin);
module.exports = EventModel;
