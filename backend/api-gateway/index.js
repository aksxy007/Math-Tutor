import dotenv from 'dotenv'
dotenv.config()

import express from 'express'
import cors from 'cors'
import Redis from 'ioredis'
import helmet from 'helmet'
import rateLimit from 'express-rate-limit'
import RedisStore from 'rate-limit-redis'
import proxy from 'express-http-proxy'
import cookieParser from 'cookie-parser';

import {authenticate} from './middleware/authMIddleware.js'

const PORT = process.env.PORT || 3000
const app =express()
const redisClient = new Redis(process.env.REDIS_URL) 
// ✅ Check if Redis is connected
redisClient.on("connect", () => {
    console.log("✅ Redis connected successfully!");
  });
  
  // ✅ Redis is ready to accept commands
  redisClient.on("ready", () => {
    console.log("✅ Redis is ready!");
  });
  
  // ❌ Handle connection errors
  redisClient.on("error", (err) => {
    console.error("❌ Redis connection error:", err);
  });
  
  // 🔄 Handle reconnection attempts
  redisClient.on("reconnecting", () => {
    console.log("🔄 Redis reconnecting...");
  });
  redisClient.ping()
    .then(() => console.log("✅ Redis is responding to PING!"))
    .catch((err) => console.error("❌ Redis PING failed:", err));

  
// Middleswares
app.use(helmet())
app.use(cors())
app.use(express.json())
app.use(cookieParser());

// Rate limiting 
const limiter = rateLimit({
    store: new RedisStore({
        sendCommand:(...args) => redisClient.call(...args),
    }),
    standardHeaders:true,
    legacyHeaders:false,
    handler:(req,res)=>{
        res.status(429).json({success:false,message:"Too many requests, please try again later..."})
    },
    windowMs:1*60*1000, // 1 minute window
    max:10,
    keyGenerator: (req)=>req.ip 
})


// Proxy Server
const proxyOptions = {
    proxyReqPathResolver: (req)=>{
        return req.originalUrl.replace(/^\/v1/,"/api")
    },
    proxyErrorHandler: (err,res,next)=>{
        console.log(`Proxy error: ${err.message}`)
        res.status(500).json({
            success:false,
            message:"Internal server error",
            error:err.message
        })
    }
}

app.use(limiter)

app.use((req, res, next) => {
    console.log(`Received ${req.method} request to ${req.url}`);
    console.log(`Request body: ${req.body}`);
    next();
  });
  

// set up proxy for identity service 
app.use('/v1/auth',proxy(
    process.env.IDENTITY_SERVICE_URL,
    {   ...proxyOptions,
        proxyReqOptDecorator: (proxyReqOpts,srcReq)=>{
            proxyReqOpts.headers["Content-type"]='application/json'
            return proxyReqOpts
        },
        userResDecorator: (proxyRes,proxyResData,userReq,userRes)=>{
            console.log(`Response recieved from Identity Service: ${proxyRes.statusCode}`)

            return proxyResData;
        }
    }
))


app.use('/v1/tutor',authenticate,proxy(
    process.env.MATH_TUTOR_SERVICE_URL,
    {   ...proxyOptions,
        proxyReqOptDecorator: (proxyReqOpts,srcReq)=>{
            proxyReqOpts.headers["Content-type"]='application/json'
            return proxyReqOpts
        },
        userResDecorator: (proxyRes,proxyResData,userReq,userRes)=>{
            console.log(`Response recieved from Identity Service: ${proxyRes.statusCode}`)

            return proxyResData;
        }
    }
))


app.listen(PORT,()=>{
    console.log(`API Gateway running at port:${PORT}`)
    console.log(`Identity Service running at: ${process.env.IDENTITY_SERVICE_URL}`)
    console.log(`Math Tutor Service running at: ${process.env.MATH_TUTOR_SERVICE_URL}`)
})

process.on("SIGINT", async () => {
    console.log("🔴 Shutting down API Gateway...");
    await redisClient.quit();
    console.log("✅ Redis client disconnected.");
    process.exit(0);
});