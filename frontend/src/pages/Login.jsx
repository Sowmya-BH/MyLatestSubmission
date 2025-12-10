// src/pages/Login.jsx
// src/pages/Login.jsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api";


export default function Login() {
  const [username, setUsername] = useState("");
  // REMOVED: const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    // Since the backend model still expects a password, we must send one,
    // even if it will be ignored on the server side.
    const DUMMY_PASSWORD = "password_is_ignored";

    try {
      // **1. Perform API Call to Backend**
      const payload = {
          username: username,
          password: DUMMY_PASSWORD // Pass the dummy password
      };
      const res = await loginUser(payload);

      // **2. Success: Save JWT and Redirect**
      localStorage.setItem("token", res.data.access_token);
      navigate("/documents");

    } catch (error) {
      // **3. Failure: Handle Errors**
      const errorMessage = error.response?.data?.detail || "Login failed. Invalid username.";
      alert(errorMessage);
    }
  };

  return (
    <div className="w-full h-screen flex justify-center items-center bg-gradient-to-br from-slate-900 to-slate-700">
      <div className="backdrop-blur-lg bg-white/10 shadow-xl border border-white/20 rounded-2xl p-10 w-[420px]">
        <h2 className="text-3xl font-bold text-white text-center mb-6">
          Financial Advisor Login
        </h2>

        <form onSubmit={handleLogin} className="flex flex-col space-y-5">
          <div>
            <label className="text-sm text-gray-200">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full mt-1 px-4 py-2 rounded-xl bg-white/20 text-white placeholder-gray-300 outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="Enter your username (e.g., admin@example.com)"
            />
          </div>

          {/* REMOVED PASSWORD INPUT FIELD */}

          <button
            type="submit"
            className="w-full py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl font-semibold transition-all shadow-lg"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

// import { useState } from "react";
// import { Link } from "react-router-dom";
//
// export default function Login() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//
//   const handleLogin = (e) => {
//     e.preventDefault();
//     console.log("Logging in:", email, password);
//   };
//
//   return (
//     <div className="w-full h-screen flex justify-center items-center bg-gradient-to-br from-slate-900 to-slate-700">
//       <div className="backdrop-blur-lg bg-white/10 shadow-xl border border-white/20 rounded-2xl p-10 w-[420px]">
//         <h2 className="text-3xl font-bold text-white text-center mb-6">
//           Welcome Back
//         </h2>
//
//         <form onSubmit={handleLogin} className="flex flex-col space-y-5">
//           <div>
//             <label className="text-sm text-gray-200">Email</label>
//             <input
//               type="email"
//               className="w-full mt-1 px-4 py-2 rounded-xl bg-white/20 text-white placeholder-gray-300 outline-none focus:ring-2 focus:ring-blue-400"
//               placeholder="Enter your email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//             />
//           </div>
//
//           <div>
//             <label className="text-sm text-gray-200">Password</label>
//             <input
//               type="password"
//               className="w-full mt-1 px-4 py-2 rounded-xl bg-white/20 text-white placeholder-gray-300 outline-none focus:ring-2 focus:ring-blue-400"
//               placeholder="Enter your password"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//             />
//           </div>
//
//           <button
//             type="submit"
//             className="w-full py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl font-semibold transition-all shadow-lg"
//           >
//             Login
//           </button>
//         </form>
//
//         <p className="text-center text-gray-300 mt-6 text-sm">
//           Don’t have an account?{" "}
//           <Link
//             to="/signup"
//             className="text-blue-300 hover:underline cursor-pointer"
//           >
//             Sign Up
//           </Link>
//         </p>
//       </div>
//     </div>
//   );
// }
//
//
//
// // import { useState } from "react";
// // import { loginUser } from "../api";
// // import { useNavigate } from "react-router-dom";
// //
// // export default function Login() {
// //   const nav = useNavigate();
// //   const [form, setForm] = useState({ username: "", password: "" });
// //
// //   const handleLogin = async () => {
// //     try {
// //       const res = await loginUser(form);
// //       localStorage.setItem("token", res.data.access_token);
// //       nav("/dashboard");
// //     } catch (e) {
// //       alert("Login failed");
// //     }
// //   };
// //
// //   return (
// //     <div>
// //       <h1>Login</h1>
// //       <input placeholder="Username" onChange={(e) => setForm({ ...form, username: e.target.value })} />
// //       <input placeholder="Password" type="password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
// //       <button onClick={handleLogin}>Login</button>
// //     </div>
// //   );
// // }
