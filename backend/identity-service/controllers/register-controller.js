import User from "../models/User.js";
import { generateAccessToken, generateRefreshToken } from "../jwt-utils/jwt-utils.js";
import { validationResult } from "express-validator";
import bcrypt from 'bcryptjs';
export const register =async (req,res)=>{
    // console.log(`/register : ${req.body}`)
    const errors = validationResult(req)
    if(!errors.isEmpty()){
        return res.status(400).json({error:errors.array()})
    }

    const {username,email,password} = req.body;
    console.log(username,email,password)

    try {
        const existingUser = await User.findOne({email})
        
        if (existingUser){
            console.log("User already exists: ",existingUser.email)
            return res.status(400).json({success:true,message:"User with email already exists!!"})
        }

        const hashedPassword = await bcrypt.hash(password,10)

        const newUser = User({
            username,
            email,
            password:hashedPassword
        })

        await newUser.save()

        const accessToken = generateAccessToken(newUser)
        const refreshToken = generateRefreshToken(newUser)

        res.cookie('refresh_token', refreshToken, {
            httpOnly: true,    // Can't be accessed via JavaScript (prevents XSS)
            secure: process.env.NODE_ENV === 'production',  // Only use in HTTPS
            maxAge: 30 * 24 * 60 * 60 * 1000,  // Refresh token expires in 30 days
            sameSite: 'None',  // Prevents CSRF attacks
          });
        
    
        return res.status(200).json({
            success:true,
            message:"User registered successfully",
            user:newUser,
            accessToken
        })

    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Register: Internal server error' });
    }
}