import { useState } from 'react';

function App() {
  const [diagnostico, setDiagnostico] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [loading, setLoading] = useState(false);

  const traducir = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/traducir', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ diagnostico })
      });
      const data = await res.json();
    setRespuesta(data.explicacion);
    } catch (error) {
      setRespuesta('Error al conectar con el servidor.');
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: 'auto', fontFamily: 'sans-serif' }}>
      <h2>Traductor IA - Taller Mecánico 🚗</h2>
      <textarea 
        rows="4" 
        style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        placeholder="Ej: Falla en el lazo cerrado de la sonda Lambda..."
        value={diagnostico}
        onChange={(e) => setDiagnostico(e.target.value)}
      />
      <br/>
      <button 
        onClick={traducir} 
        disabled={loading}
        style={{ padding: '10px 20px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
      >
        {loading ? 'Traduciendo...' : 'Traducir para el Cliente'}
      </button>

      {respuesta && (
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px', borderLeft: '5px solid #28a745' }}>
          <strong>Traducción:</strong>
          <p>{respuesta}</p>
        </div>
      )}
    </div>
  );
}

export default App;