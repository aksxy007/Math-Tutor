import { Geist, Geist_Mono,Poppins,Roboto } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import AppBar from "@/components/app-bar";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const roboto = Roboto({
  variable:"--font-roboto",
  weight: ['400', '700'],
  subsets: ['latin'],
  display: 'swap',
 })
 const poppins = Poppins({
  variable: "--font-poppins",
  weight: ['400','600','800'],
  subsets: ['latin'],
  display: 'swap',
 })

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Math Mojo",
  description: "Ai powered math tutor",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${poppins.variable} antialiased min-h-screen`}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        > 
    
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
