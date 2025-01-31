import mongoose from "mongoose";

const UserSchema = mongoose.Schema({
    username:{
        type:String,
        required:[true,"Username is required!"],
    },
    email:{
        type:String,
        required:[true,"Email is required"],
        unique: true,
        lowercase: true,
        match: [/^\S+@\S+\.\S+$/, 'Please provide a valid email address'],
    },
    password:{
        type: String,
        required: [true, 'Password is required'],
        minlength: [6, 'Password must be at least 6 characters'],
    }
},{timestamps:true}

)

const User = mongoose.model("User",UserSchema);

export default User;