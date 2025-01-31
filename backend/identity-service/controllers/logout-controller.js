import { verifyToken } from "../jwt-utils/jwt-utils.js";

export const logout = (req,res)=>{
    try {
        const { refreshToken } = req.cookies;

        if (!refreshToken) {
            return res.status(400).json({ message: 'No refresh token found' });
        }

        // Invalidate the refresh token (remove it from the server-side storage)
        // Assuming `refreshTokens` is a simple object with user ID as keys
        const decoded = verifyToken(refreshToken,true); // Make sure to use the correct secret
        if(!decoded){
            return res.status(500).json({message:"User not verified"})
        }

        // Clear the refresh token cookie
        res.clearCookie('refreshToken', { httpOnly: true, secure: true });

        res.json({ message: 'Logged out successfully' });
    } catch (error) {
        console.log("Error in logging out",error)
        return res.status(500).json({message:"Error in logging out"})
    }
    

}