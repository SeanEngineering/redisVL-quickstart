import { useState } from 'react';

export default function ImageUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/images', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('Upload failed');

      setStatus('✅ Image uploaded successfully');
    } catch (err) {
      setStatus('❌ Upload failed');
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type='file'
        accept='image/*'
        onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
      />
      <button type='submit'>Upload</button>
      <p>{status}</p>
    </form>
  );
}
