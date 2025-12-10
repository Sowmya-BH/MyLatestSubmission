import { useParams } from "react-router-dom";
import { useState } from "react";
import { queryPDF } from "../api";

export default function QueryPage() {
  const { id } = useParams();
  const [keyword, setKeyword] = useState("");
  const [userQuery, setUserQuery] = useState("");
  const [result, setResult] = useState(null);

  const handleQuery = async () => {
    const res = await queryPDF(id, {
      input_field: keyword,
      user_query: userQuery
    });

    setResult(res.data);
  };

  return (
    <div>
      <h2>Query Document</h2>

      <input placeholder="Keyword" onChange={(e) => setKeyword(e.target.value)} />
      <textarea placeholder="Your Query" onChange={(e) => setUserQuery(e.target.value)} />

      <button onClick={handleQuery}>Run Query</button>

      {result && (
        <div>
          <h3>Answer:</h3>
          <pre>{result.answer}</pre>

          <h3>AgentOps Logs:</h3>
          <pre>{result.logs}</pre>
        </div>
      )}
    </div>
  );
}
