import React, { useState } from "react";
import { motion } from "framer-motion";
const Examples = () => {

  const [mousePos, setMousePos] = useState({ x: -100, y: -100 });

  const data = [
    "How to find the area of tripezium?",
    "Can u give a math puzzle.",
    "Area of a isoceles triangle.",
    "Probality of getting tails in 6 tosses.",
  ];

  // Function to determine grid size based on text length
  const getSize = (text) => {
    const length = text.length;

    if (length < 4) return "col-span-1 row-span-1"; // Small
    if (length < 10) return "col-span-2 row-span-1"; // Medium
    return "col-span-2 row-span-2"; // Large
  };

  return (
    <div className="grid grid-cols-4 gap-4 p-8 max-w-6xl mx-auto justify-center items-center"
    onMouseMove={(e) => setMousePos({ x: e.clientX, y: e.clientY })}
    >
      {data.map((query,index) => (

          <motion.div
          key={index}
          className={`group relative p-3 rounded-xl text-[0.85rem] h-[10px] flex items-center justify-center border broder-gray-200 shadow-md cursor-pointer transition-all text-neutral-400 dark:bg-[#141414]
                      ${getSize(query)}`}
          whileHover={{ scale: 1.05 ,}}
          whileTap={{ scale: 0.95 }}
        >
          <span className="group-hover:text-cyan-500 transition-colors duration-300">{query}</span>
          <span 
            className="absolute inset-x-0 -top-px h-[1px] bg-gradient-to-r from-transparent via-cyan-500 to-transparent w-3/4 mx-auto"
          />
          <span 
            className="absolute group-hover:opacity-100 opacity-0 transition-opacity duration-300 inset-x-0 -top-px h-[3px] bg-gradient-to-r from-transparent via-cyan-500 to-transparent w-3/4 mx-auto blur-md"
          />
        </motion.div>
        
        ))}
    </div>
  );
};

export default Examples;
