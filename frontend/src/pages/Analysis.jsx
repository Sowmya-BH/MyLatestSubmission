import PDFUploader from "../components/PDFUploader";
import PDFList from "../components/PDFList";

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <PDFUploader />
      <PDFList />
    </div>
  );
}
