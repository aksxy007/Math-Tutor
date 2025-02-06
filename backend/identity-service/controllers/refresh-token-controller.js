import { generateAccessToken, verifyToken } from "../jwt-utils/jwt-utils.js";
import User from "../models/User.js";

export const refreshToken =async (req,res)=>{

    try {
        const refreshToken = req.cookies?.refresh_token

        if(!refreshToken){
            return res.status(500).json({error:"No refresh token found!"})
        }

        const decoded = verifyToken(refreshToken,true)
        if(!decoded){
            return res.status(500).json({message:"Not a valid refresh token"})
        }

        const user = await User.findById({_id:decoded.id})

        const newAccessToken = generateAccessToken(user)

        return res.status(200).json({success:true,message:"Token refreshed",accessToken:newAccessToken})
    } catch (error) {
        console.log("Error refreshing token")
        return res.status(500).json({success:false,message:"error in refreshing token"})
    }
    
}   