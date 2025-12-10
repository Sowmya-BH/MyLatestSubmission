import { useState } from "react";
import { uploadPDF } from "../api";

export default function PDFUploader() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return;

    await uploadPDF(file);
    alert("PDF uploaded");
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}






// import { useState } from "react";
// import { uploadPDF } from "../api";
//
// export default function PDFUploader() {
//   const [file, setFile] = useState(null);
//
//   const handleUpload = async () => {
//     if (!file) {
//       alert("Please select a PDF file first.");
//       return;
//     }
//
//     if (!file.name.toLowerCase().endsWith(".pdf")) {
//       alert("Only PDF files are allowed.");
//       return;
//     }
//
//     try {
//       const response = await uploadPDF(file);
//       alert("PDF uploaded successfully!");
//       console.log("Uploaded:", response.data);
//     } catch (err) {
//       console.error(err);
//       alert("Upload failed");
//     }
//   };
//
//   return (
//     <div>
//       <input
//         type="file"
//         accept="application/pdf"
//         onChange={(e) => setFile(e.target.files[0])}
//       />
//
//       <button onClick={handleUpload}>
//         Upload PDF
//       </button>
//     </div>
//   );
// }
