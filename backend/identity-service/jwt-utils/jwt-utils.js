import jwt, { decode } from 'jsonwebtoken'
import dotenv from 'dotenv'

dotenv.config()

const JWT_ACCESS_SECRET = process.env.JWT_ACCESS_SECRET
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET
const ACCESS_TOKEN_EXPIRY = process.env.ACCESS_TOKEN_EXPIRY || "1h"
const REFRESH_TOKEN_EXPIRY = process.env.REFRESH_TOKEN_EXPIRY || '7d'

export const generateAccessToken=(user)=>{
    const payload={
        id:user._id
    }

    return jwt.sign(payload,JWT_ACCESS_SECRET,{expiresIn:ACCESS_TOKEN_EXPIRY})
}

export const generateRefreshToken= (user)=>{
    const payload = {
        id:user._id
    }

    return jwt.sign(payload,JWT_REFRESH_SECRET,{expiresIn:REFRESH_TOKEN_EXPIRY})
}

export const verifyToken = (token,isRefreshToken=false)=>{
    const JWT_SECRET = isRefreshToken?JWT_REFRESH_SECRET:JWT_ACCESS_SECRET
    try {
        const decoded = jwt.verify(token,JWT_SECRET)
        return decoded
    } catch (error) {
        console.log("Invalid or expired token")
        return null
    }
    
}