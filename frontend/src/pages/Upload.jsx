import React from "react";
import ImageUploader from "../components/ImageUploader";
import { api } from "../api";

export default function Upload() {
  async function onUpload(file) {
    const fd = new FormData();
    fd.append("file", file);
    const resp = await api.post("/meals/", fd, { headers: {"Content-Type": "multipart/form-data"} });
    alert("Uploaded — processing in background. Check history in a few seconds.");
  }
  return (
    <div>
      <h2 className="text-lg mb-4">Upload meal photo</h2>
      <ImageUploader onUpload={onUpload} />
    </div>
  );
}
