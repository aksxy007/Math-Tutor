import jwt from 'jsonwebtoken';
import axios from 'axios';

export const authenticate = async (req, res, next) => {
    try {
        const accessToken = req.headers.authorization?.split(" ")[1];

        console.log("Authenticate middleware called")

        if (!accessToken) {
            console.log("No access token found!");
            return res.status(401).json({ success: false, message: "No access token found!" });
        }

        // ✅ Synchronous `jwt.verify` with try/catch
        try {
            const decoded = jwt.verify(accessToken, process.env.ACCESS_TOKEN_SECRET);
            req.user = decoded._id;  // Store user ID
            return next();  // ✅ If access token is valid, proceed
        } catch (err) {
            console.log("⚠️ Access token expired or invalid, trying refresh token...");
        }

        // ✅ Refresh token logic
        const refreshToken = req.cookies?.refresh_token;
        console.log(refreshToken)
        if (!refreshToken) {
            console.log("❌ No refresh token found.");
            return res.status(401).json({ success: false, message: "Session expired. Please log in again." });
        }

        
        // ✅ Await refresh response
        try {
            const response = await axios.get(`${process.env.IDENTITY_SERVICE_URL}/api/auth/refresh-token`, {
                headers: { cookie: `refresh_token=${refreshToken}` },
                withCredentials: true
            });

            console.log("refresh response",response.data)

            if (response.data.success) {
                const newAccessToken = response.data.accessToken;
                req.headers.authorization = `Bearer ${newAccessToken}`;  // ✅ Update header
                req.user = jwt.verify(newAccessToken, process.env.ACCESS_TOKEN_SECRET)._id;  // ✅ Decode user ID
                return next();
            } else {
                console.log("❌ Refresh token request failed:", response.data);
                return res.status(401).json({ success: false, message: "Session expired. Please log in again." });
            }
        } catch (error) {
            console.error("❌ Refresh token failed:", error.response?.data || error.message);
            return res.status(401).json({ success: false, message: "Session expired. Please log in again." });
        }
    } catch (error) {
        console.error("❌ Authentication middleware error:", error);
        return res.status(500).json({ success: false, message: "Internal server error" });
    }
};
