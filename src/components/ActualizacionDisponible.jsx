import { useRegisterSW } from 'virtual:pwa-register/react';

export default function ActualizacionDisponible() {
  const {
    needRefresh: [needRefresh, setNeedRefresh],
    updateServiceWorker,
  } = useRegisterSW({
    onRegistered(r) {
      console.log('SW Registered:', r);
    },
    onRegisterError(error) {
      console.error('SW registration error:', error);
    },
  });

  if (!needRefresh) return null;

  return (
    <aside
      role="alert"
      className="actualizacion-disponible-banner"
      style={{
        position: 'fixed',
        bottom: '24px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 9999,
        background: '#1e1b4b',
        color: '#f8fafc',
        padding: '0.85rem 1.25rem',
        borderRadius: '12px',
        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5)',
        border: '1px solid #6366f1',
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        fontSize: '0.95rem',
      }}
    >
      <span>Hay una versión nueva de la tienda.</span>
      <button
        type="button"
        onClick={() => updateServiceWorker(true)}
        style={{
          background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
          color: '#ffffff',
          border: 'none',
          padding: '0.45rem 0.9rem',
          borderRadius: '8px',
          fontWeight: 600,
          cursor: 'pointer',
          fontSize: '0.85rem',
          transition: 'transform 0.2s, opacity 0.2s',
        }}
      >
        Actualizar
      </button>
      <button
        type="button"
        onClick={() => setNeedRefresh(false)}
        aria-label="Cerrar aviso"
        style={{
          background: 'transparent',
          color: '#94a3b8',
          border: 'none',
          cursor: 'pointer',
          fontSize: '1rem',
          padding: '0.2rem',
          lineHeight: 1,
        }}
      >
        ✕
      </button>
    </aside>
  );
}
