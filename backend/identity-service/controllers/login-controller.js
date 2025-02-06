import User from "../models/User.js";
import { generateAccessToken, generateRefreshToken } from "../jwt-utils/jwt-utils.js";
import { validationResult } from "express-validator";
import bcrypt from 'bcryptjs';
export const login =async (req,res)=>{
    const errors = validationResult(req)
    if(!errors.isEmpty()){
        return res.status(400).json({error:errors.array()})
    }

    const {email,password} = req.body;

    try {
        const user = await User.findOne({email})
        if (!user){
            return res.status(400).json({success:false,message:"User with email does not exists!!"})
        }

        // console.log("User Found: ",user)
       
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(400).json({success:false ,message: 'Invalid credentials' });
        }


        const accessToken = generateAccessToken(user)
        const refreshToken = generateRefreshToken(user)

        res.cookie('refresh_token', refreshToken, {
            httpOnly: true,    // Can't be accessed via JavaScript (prevents XSS)
            secure: process.env.NODE_ENV === 'production',  // Only use in HTTPS
            maxAge: 30 * 24 * 60 * 60 * 1000,  // Refresh token expires in 30 days
            sameSite: 'None',  // Prevents CSRF attacks
          });
        
        
        return res.status(200).json({
            success:true,
            message:"User logged in successfully",
            user:user,
            accessToken
        })

    } catch (error) {
        console.error(error);
        res.status(500).json({success:false, message: 'Login: Internal server error' });
    }
}