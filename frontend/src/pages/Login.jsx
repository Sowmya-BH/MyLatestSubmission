import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
      setLoading(true);

      const res = await fetch("http://localhost:8001/auth/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        setError(data.detail || "Login failed");
        return;
      }

      localStorage.setItem("token", data.access_token);
      navigate("/analysis");
    } catch (err) {
      setLoading(false);
      setError("Network error");
    }
  };

  return (
    <div className="flex min-h-screen flex-col justify-center px-6 py-12 bg-gray-900">
      <div className="sm:mx-auto sm:w-full sm:max-w-sm">
        {/* Removed image */}
        <h2 className="mt-10 text-center text-2xl font-bold tracking-tight text-white">
          Sign in to your account
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Username field */}
          <div>
            <label
              htmlFor="username"
              className="block text-sm font-medium text-gray-100"
            >
              Username
            </label>
            <div className="mt-2">
              <input
                id="username"
                name="username"
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-white
                  outline outline-1 outline-white/10
                  placeholder-gray-500
                  focus:outline-2 focus:outline-indigo-500"
              />
            </div>
          </div>

          {/* Password field */}
          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-100"
            >
              Password
            </label>
            <div className="mt-2">
              <input
                id="password"
                name="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="block w-full rounded-md bg-white/5 px-3 py-1.5 text-white
                  outline outline-1 outline-white/10
                  placeholder-gray-500
                  focus:outline-2 focus:outline-indigo-500"
              />
            </div>
          </div>

          {/* Submit button */}
          <div>
            <button
              type="submit"
              disabled={loading}
              className="flex w-full justify-center rounded-md bg-indigo-500 
                px-3 py-1.5 text-sm font-semibold text-white hover:bg-indigo-400
                focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500
                disabled:opacity-50"
            >
              {loading ? "Logging in..." : "Sign in"}
            </button>
          </div>

          {/* Error message */}
          {error && (
            <p className="text-red-400 text-center text-sm mt-2">{error}</p>
          )}
        </form>
      </div>
    </div>
  );
}
