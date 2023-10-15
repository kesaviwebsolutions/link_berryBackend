const mongoose = require("mongoose");

const Super_Admin = new mongoose.Schema({
  wallet_Address: {
    type: String,
    required: false,
  },
  userName: {
    type: String,
    required: false,
  },
  inviter: {
    type: String,
    required: false,
  },
  followers:{
    type: Number,
    required: false,
  },
  profileImage:{
    type: String,
    required: false,
  },
  joinAt:{
    type: Number,
    required: false,
  },
  connections:{
    type: Number,
    required: false,
  },
  inviteCodes:{
    type: Array,
    required: false,
  },
  walletType:{
    type: String,
    required: false,
  },
  walletKey:{
    type: String,
    required: false,
  },
  userTx:{
    type: Array,
    required: false,
  },
  holders:{
    type: Array,
    required: false,
  },
  holdings:{
    type: Array,
    required: false,
  },
});
const EventModel = new mongoose.model("User", Super_Admin);
module.exports = EventModel;
