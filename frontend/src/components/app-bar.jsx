import Link from "next/link";
import React from "react";
import { Button } from "./ui/button";

const AppBar = () => {
  return (
    <div className="relative w-[96%] lg:w-[84%] left-1/2 -translate-x-1/2 h-[7%] my-8 lg:my-4 z-20">
      <div className="flex h-full justify-center min-w-fit">
        <div className="group relative mx-auto w-full h-full flex justify-center items-center rounded-xl border bg-[#111111] opacity-95 backdrop-blur-md">
          <span className="absolute inset-x-0 mx-auto bottom-0 h-[1px] w-3/4 bg-gradient-to-r from-transparent via-cyan-500 to-transparent " />
          <span className="absolute opacity-0 group-hover:opacity-100 transition-opacity duration-300 inset-x-0 mx-auto bottom-0 h-[3px] w-3/4 bg-gradient-to-r from-transparent via-cyan-500 to-transparent " />
          <div className="w-[30%] h-full flex justify-start items-center p-4">
            <Link
              href={"/"}
              className="dark:text-white text-black text-lg transition-colors duration-100"
            >
              Math Mojo
            </Link>
          </div>
          <div className="w-[70%] mx-1 p-1 h-full flex justify-end items-center gap-x-2">
            <Button variant="ghost"
                className="dark:bg-[#2A2A2A]"
            >
              <Link href={"/login"} >
                Sign in
              </Link>
            </Button>

            <Button className="dark:text-white">Get Started</Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AppBar;
