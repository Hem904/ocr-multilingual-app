import React, { useState, useEffect } from "react";
import axios from "axios";

const OCRForm = () => {
  const [image, setImage] = useState(null);
  const [lang, setLang] = useState("hin");
  const [languages, setLanguages] = useState({});
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios
      .get("http://localhost:8000/languages/")
      .then((res) => setLanguages(res.data))
      .catch((err) => console.error("Error fetching languages:", err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      alert("Please choose an image first");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);
    formData.append("lang", lang);

    setLoading(true);
    setResult("");

    try {
      const res = await axios.post("http://localhost:8000/OCR", formData);
      if (res.data.text) {
        setResult(res.data.text);
      } else if (res.data.error) {
        setResult(`Error: ${res.data.error}`);
      } else {
        setResult("Error: unknown response format");
      }
    } catch (err) {
      console.error("OCR request failed:", err);
      setResult("Error: OCR request failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files[0])}
        required
      />

      <select value={lang} onChange={(e) => setLang(e.target.value)}>
        {Object.entries(languages).map(([code, name]) => (
          <option key={code} value={code}>
            {name} ({code})
          </option>
        ))}
      </select>

      <button type="submit">Run OCR</button>

      {loading && <p>Processing…</p>}

      {result && (
        <div className="ocr-result">
          <h4>OCR Result:</h4>
          <p>{result}</p>
        </div>
      )}
    </form>
  );
};

export default OCRForm;
