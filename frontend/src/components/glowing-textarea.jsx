    "use client";

    import React, { useState } from "react";
    import { Textarea } from "./ui/textarea";
    import SendButton from "./send-button";
    import { SendHorizonalIcon } from "lucide-react";
    import {motion} from "framer-motion"

    const GlowingTextArea = () => {

        const [text, setText] = useState("")

        const display = text===""?"hidden":"block"
    return (
        <div className="relative w-[100%] flex items-center justify-center">
        {/* Textarea */}
        <Textarea
            className="relative h-[140px] w-full max-w-lg text-gray-300 resize-none rounded-lg focus:ring-0 focus:border-cyan-400 text-lg 
                    bg-neutral-100 dark:bg-[#141414] p-4"
            placeholder="Type your question here..."
            value={text}
            onChange={(e)=> setText(e.target.value)}
        />
        <span className="absolute inset-x-0 -top-0 h-[1px] bg-gradient-to-r from-transparent via-cyan-500 to-transparent w-3/4 mx-auto"/>
        <div className={`absolute right-12 bottom-2 ${display}`}>
            <SendButton Icon={SendHorizonalIcon} size={20}/>
        </div>
        
        </div>
    );
    };

    export default GlowingTextArea;
