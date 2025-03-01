import { LoginForm } from '@/components/login-form'
import React from 'react'

function Register() {
  return (
    <div className="flex min-h-svh flex-col items-center justify-center">
        <LoginForm isRegister={true}/>
    </div>
  )
}

export default Register