import AppBar from "@/components/app-bar";
import SideBar from "@/components/SideBar";
import React from "react";

const layout = ({ children }) => {
  return (
    <div className="relative h-screen w-screen flex">
      <div className="w-[25%] h-full flex">
        <SideBar />
      </div>
      <div className="w-[75%] h-full flex flex-col justify-center dark:bg-[radial-gradient(circle,#1a1a1a_1px,transparent_1px)] dark:bg-[size:10px_10px]">
        <div className="flex absolute w-[75%] h-full ">
          <AppBar />
        </div>
        
        <div className="">
          {children}
        </div>
      </div>
    </div>
  );
};

export default layout;
