export default function FileUpload({ onFileSelect }) {
  return (
    <div style={{ marginBottom: '1rem' }}>
      <label style={{ display: 'block', marginBottom: '0.5rem' }}>Attachment:</label>
      <input
        type="file"
        onChange={(e) => onFileSelect(e.target.files[0])}
        required
      />
    </div>
  );
}