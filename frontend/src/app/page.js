"use client"


import AppBar from "@/components/app-bar";
import GlowingTextArea from "@/components/glowing-textarea";
import Examples from "@/components/question-examples";
import TypyingEffect from "@/components/typing";

export default function Home() {

  return (
    <div className="relative flex flex-col h-screen w-screen overflow-hidden">
      <AppBar/>
      <div className="absolute w-full h-full flex flex-col space-y-10 justify-center items-center dark:bg-[radial-gradient(circle,#1a1a1a_1px,transparent_1px)] dark:bg-[size:10px_10px]">
        <div className="flex flex-col justify-center items-center gap-3">
          <TypyingEffect
            text="Have a question to solve,ask Math Mojo"
            speed={80}
            size="text-4xl"
          />
        
          <p className="text-neutral-400 text-lg">
            Type in your question and let AI help you solve it.
          </p>
        </div>
        {/* Input Box */}
        <div className="flex flex-col justify-center items-center w-full h-50 max-w-3xl p-3 rounded-md space-y-2">
          <div className="grid w-[80%] gap-2">
            <GlowingTextArea/>
          </div>
          <div className="flex w-[80%] items-center">
              <Examples/>
          </div>
        </div>
      </div>
     
    </div>
  );
}
