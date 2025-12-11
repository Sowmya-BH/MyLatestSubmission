import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function ProtectedPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const verify = async () => {
      try {
        await api.get("/");
      } catch {
        localStorage.removeItem("token");
        navigate("/");
      }
    };
    verify();
  }, [navigate]);

  return <div>You are authenticated.</div>;
}

export default ProtectedPage;
