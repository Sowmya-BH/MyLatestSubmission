import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import ProtectedPage from "./pages/Protected";
import Analysis from "./pages/Analysis";
import AnalysisUploader from './components/AnalysisUploader';
import './index.css'; // Assuming your Tailwind CSS is imported here

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/protected" element={<ProtectedPage />} />
        <Route path="/analysis" element={<Analysis />} />
      </Routes>
    </Router>
  );
}

export default App;


///////////////////////////////////////////////////////////////////////////////////////
// import React from "react";
// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
//
// import Login from "./pages/Login.jsx";
// import ProtectedPage from "./pages/Protected.jsx";
//
// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<Login />} />
//         <Route path="/protected" element={<ProtectedPage />} />
//       </Routes>
//     </Router>
//   );
// }
//
// export default App;
//
//
/////////////////////////////////////////////////////////////////////////////////////////


// import { BrowserRouter, Routes, Route } from "react-router-dom";
// import Login from "./pages/Login";
// // import Register from "./pages/Register";
// import Dashboard from "./pages/Dashboard";
// import QueryPage from "./pages/QueryPage";
//
// export default function App() {
//   return (
//     <BrowserRouter>
//       <Routes>
//         <Route path="/" element={<Login />} />
// {/*         <Route path="/register" element={<Register />} /> */}
//         <Route path="/dashboard" element={<Dashboard />} />
//         <Route path="/query/:id" element={<QueryPage />} />
//       </Routes>
//     </BrowserRouter>
//   );
// }
//
//
//
//
// // import { useState } from 'react'
// // import reactLogo from './assets/react.svg'
// // import viteLogo from '/vite.svg'
// // import './App.css'
// //
// // function App() {
// //   const [count, setCount] = useState(0)
// //
// //   return (
// //     <>
// //       <div>
// //         <a href="https://vite.dev" target="_blank">
// //           <img src={viteLogo} className="logo" alt="Vite logo" />
// //         </a>
// //         <a href="https://react.dev" target="_blank">
// //           <img src={reactLogo} className="logo react" alt="React logo" />
// //         </a>
// //       </div>
// //       <h1>Vite + React</h1>
// //       <div className="card">
// //         <button onClick={() => setCount((count) => count + 1)}>
// //           count is {count}
// //         </button>
// //         <p>
// //           Edit <code>src/App.jsx</code> and save to test HMR
// //         </p>
// //       </div>
// //       <p className="read-the-docs">
// //         Click on the Vite and React logos to learn more
// //       </p>
// //     </>
// //   )
// // }
// //
// // export default App
