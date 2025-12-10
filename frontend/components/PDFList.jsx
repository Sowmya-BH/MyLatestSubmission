import { useEffect, useState } from "react";
import { listDocs } from "../api";
import { useNavigate } from "react-router-dom";

export default function PDFList() {
  const nav = useNavigate();
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    listDocs().then((r) => setDocs(r.data));
  }, []);

  return (
    <ul>
      {docs.map((d) => (
        <li key={d.id}>
          {d.filename} — <button onClick={() => nav(`/query/${d.id}`)}>Query</button>
        </li>
      ))}
    </ul>
  );
}
