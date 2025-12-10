import { useState } from "react";
import { runQuery } from "../api";

export default function QueryBox({ documentId }) {
  const [inputField, setInputField] = useState("");
  const [userQuery, setUserQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    if (!documentId) {
      alert("Please upload/select a PDF first.");
      return;
    }

    setLoading(true);
    try {
      const res = await runQuery(documentId, {
        input_field: inputField,
        user_query: userQuery,
      });

      setResponse(res.data);
    } catch (err) {
      console.error(err);
      alert("Query failed!");
    }
    setLoading(false);
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <h2 className="font-semibold mb-3">Ask Questions</h2>

      {/* Keyword Search */}
      <label className="block text-sm font-medium">Keyword Search</label>
      <input
        type="text"
        value={inputField}
        onChange={(e) => setInputField(e.target.value)}
        placeholder="e.g., Total gross profit"
        className="border p-2 w-full rounded mb-3"
      />

      {/* Semantic Query */}
      <label className="block text-sm font-medium">Your Question</label>
      <textarea
        value={userQuery}
        onChange={(e) => setUserQuery(e.target.value)}
        placeholder="e.g., Give a short analysis of company performance"
        className="border p-2 w-full rounded mb-3"
      />

      <button
        onClick={handleQuery}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        {loading ? "Running..." : "Run Query"}
      </button>

      {/* Response Box */}
      {response && (
        <div className="mt-4 p-3 bg-white border rounded">
          <h3 className="font-semibold">Result</h3>
          <pre className="whitespace-pre-wrap text-sm mt-2">{response.answer}</pre>

          {response.logs && (
            <>
              <h4 className="mt-3 font-medium">AgentOps Logs</h4>
              <pre className="whitespace-pre-wrap text-xs bg-gray-100 p-2 rounded">
                {response.logs}
              </pre>
            </>
          )}
        </div>
      )}
    </div>
  );
}
