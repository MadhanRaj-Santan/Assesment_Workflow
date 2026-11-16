export default function StatusBadge({ status }) {
  let bg = 'var(--border)';
  let color = 'var(--text-muted)';

  if (status === 'APPROVED') { 
    bg = 'var(--success-bg)'; 
    color = 'var(--success-text)'; 
  }
  if (status === 'REJECTED') { 
    bg = 'var(--danger-bg)'; 
    color = 'var(--danger-text)'; 
  }
  if (status === 'PENDING') { 
    bg = 'var(--warning-bg)'; 
    color = 'var(--warning-text)'; 
  }

  return (
    <span style={{ 
      backgroundColor: bg, 
      color: color, 
      padding: '0.35rem 0.85rem', 
      borderRadius: '9999px', 
      fontSize: '0.75rem', 
      fontWeight: '700',
      textTransform: 'uppercase',
      letterSpacing: '0.05em',
      display: 'inline-block'
    }}>
      {status}
    </span>
  );
}