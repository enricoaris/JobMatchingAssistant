import { BrowserRouter, Routes, Route } from "react-router-dom"

import './App.css'
import Home from "./pages/Home"
import UploadResume from "./pages/UploadResume"
import UploadJob from "./pages/UploadJob"
import { SignalRProvider } from "./components/SignalRProvider"
import MatchDetail from "./pages/MatchDetail"

function App() {
  return (
    <SignalRProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/resume" element={<UploadResume/>}/>
          <Route path="/job" element={<UploadJob/>}/>
          <Route path="/matches/:id" element={<MatchDetail/>}/>
        </Routes>
      </BrowserRouter>
    </SignalRProvider>
  )
}

export default App
