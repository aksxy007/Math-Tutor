"use client"

import { motion } from "framer-motion";

import React, { useEffect, useState } from "react";

const TypyingEffect = ({
  text = "Loading...",
  speed = 100,
  size = "text-xl",
}) => {
  const [displayedText, setDisplayedText] = useState("");
  const [index,setIndex] = useState(0)

  useEffect(() => {
    if (index < text.length) {
        const interval = setInterval(() => {
            setDisplayedText(text.slice(0,index+1));
            setIndex(index+1)
        },speed)

        return ()=>clearInterval(interval)
    }
    else {
        setTimeout(()=>{
            setDisplayedText("")
            setIndex(0)
        },1000)
        
      }
  }, [index,text, speed]);

  return (
    <motion.p
      className={`font-bold text-black dark:text-gray-100 ${size}`}
      initial={{ opacity: 0 }}
      animate={{ opacity: [0, 1] }}
      transition={{ duration: 0.4 }}
    >
      {displayedText}
      <motion.span
        className="text-green-500"
        animate={{ opacity: [0, 1, 0] }}
        transition={{ repeat: Infinity, duration: 1 }}
      >
        |
      </motion.span>
    </motion.p>
  );
};

export default TypyingEffect;
