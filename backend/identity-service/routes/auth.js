import {login} from "../controllers/login-controller.js";
import { register } from "../controllers/register-controller.js";
import { refreshToken } from "../controllers/refresh-token-controller.js";
import { logout } from "../controllers/logout-controller.js";
import { Router } from "express";


const router = Router()

router.post("/login",login)
router.post("/register",register)
router.get("/refresh-token",refreshToken)
router.get("/logout",logout)

export default router



