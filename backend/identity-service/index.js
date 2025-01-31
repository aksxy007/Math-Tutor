import express from 'express'
import morgan from 'morgan'
import cors from 'cors'
import { connectDB } from './db/mongo-connection.js'
import dotenv from 'dotenv' 

// Routes
import AuthRouter from './routes/auth.js'

dotenv.config()
const PORT = process.env.PORT || 5000


const app = express()
app.use(morgan('dev'))
app.use(cors(

))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

connectDB()

app.use("/auth",AuthRouter)

app.listen(PORT,()=>{
    console.log(`Identity Service Running at PORT: ${PORT}`)
})