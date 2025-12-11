import React, { useState } from "react";
import api from "../api";

export default function AnalysisUploader() {
  const [file, setFile] = useState(null);
  const [inputField, setInputField] = useState("");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [agentOpsLink, setAgentOpsLink] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please upload a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("input_field", inputField);
    formData.append("user_query", query);

    setLoading(true);

    try {
      const res = await api.post("/analysis/upload-and-analyze", formData);
      setLoading(false);

      setResult(res.data.final_answer || "No summary returned.");
      if (res.data.agentops_dashboard) {
        setAgentOpsLink(res.data.agentops_dashboard);
      }
    } catch (err) {
      setLoading(false);
      alert("❌ Error analyzing the document");
    }
  };

  return (
    <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8 text-white">
      <div className="sm:mx-auto sm:w-full sm:max-w-lg">
        <h2 className="mt-10 text-center text-2xl font-bold tracking-tight">
          Financial Document Analyzer
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-lg bg-white/5 p-6 rounded-xl shadow-lg border border-white/10">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-200">
              Upload PDF/DOCX
            </label>
            <input
              type="file"
              className="mt-2 block w-full text-gray-300"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </div>

          {/* Input Field */}
          <div>
            <label className="block text-sm font-medium text-gray-200">
              Input Field (e.g. Total gross profit)
            </label>
            <input
              type="text"
              value={inputField}
              onChange={(e) => setInputField(e.target.value)}
              className="mt-2 block w-full rounded-md bg-white/5 px-3 py-1.5 text-white
              outline-1 outline-white/10 placeholder-gray-500
              focus:outline-2 focus:outline-indigo-500"
              placeholder="Enter field to extract"
            />
          </div>

          {/* User Query */}
          <div>
            <label className="block text-sm font-medium text-gray-200">
              User Query
            </label>
            <textarea
              rows="4"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="mt-2 block w-full rounded-md bg-white/5 px-3 py-1.5 text-white
              outline-1 outline-white/10 placeholder-gray-500
              focus:outline-2 focus:outline-indigo-500"
              placeholder="Ask a question about the document"
            />
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-2
              text-sm font-semibold text-white hover:bg-indigo-400
              focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
              {loading ? "⏳ Processing..." : "Analyze Document"}
            </button>
          </div>
        </form>

        {/* Results */}
        {result && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold text-gray-100 mb-2">AI Analysis Result</h3>
            <pre className="bg-black/30 p-4 rounded-lg max-h-80 overflow-auto border border-white/10">
              {result}
            </pre>
          </div>
        )}

        {/* AgentOps Link */}
        {agentOpsLink && (
          <div className="mt-4 text-center">
            <a
              href={agentOpsLink}
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-400 hover:text-indigo-300 underline"
            >
              🔍 View AgentOps Dashboard
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
