import mongoose from "mongoose"
import dotenv from 'dotenv'

dotenv.config()

const mongoURI = process.env.MONGODB_URL

export const connectDB =async ()=>{
    try {
        await mongoose.connect(mongoURI).then(()=>{
            console.log('Connected to mongodb')
        })
    } catch (error) {
        console.error('Error connecting to MongoDB:', error.message);
        process.exit(1);
    }
}