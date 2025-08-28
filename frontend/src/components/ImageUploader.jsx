import React, { useState } from "react";

export default function ImageUploader({ onUpload }) {
  const [file, setFile] = useState(null);
  const submit = async (e) => {
    e.preventDefault();
    if (!file) return;
    await onUpload(file);
  };
  return (
    <form onSubmit={submit}>
      <input accept="image/*" onChange={(e) => setFile(e.target.files[0])} type="file" />
      {file && <img src={URL.createObjectURL(file)} alt="preview" style={{maxWidth: 320}} />}
      <div><button className="mt-2 btn">Upload</button></div>
    </form>
  );
}
