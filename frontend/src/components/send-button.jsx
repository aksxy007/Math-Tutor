import React from 'react'
import { Button } from './ui/button' 

const SendButton = ({Icon,size}) => {
  return (
        <Button>
            <Icon className="text-white" size={size} />
        </Button>
    
  )
}

export default SendButton