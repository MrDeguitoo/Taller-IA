import { useState } from 'react';

function App() {
  const [diagnostico, setDiagnostico] = useState('');
  const [resultado, setResultado] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTraducir = async () => {
    if (!diagnostico.trim()) return;
    
    setLoading(true);
    setError('');
    setResultado('');

    try {
      const response = await fetch('http://localhost:8000/traducir', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ diagnostico })
      });

      if (!response.ok) throw new Error('Error de conexión con el Backend de IA');

      const data = await response.json();
      setResultado(data.explicacion);
    } catch (err) {
      setError('Ocurrió un error al procesar el diagnóstico. Asegúrate de que FastAPI y Ollama estén corriendo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <header className="w-full max-w-3xl bg-blue-900 text-white rounded-lg shadow-md p-6 mb-8 text-center">
        <h1 className="text-3xl font-bold flex justify-center items-center gap-3">
          🔧 Taller IA - Traductor de Diagnósticos
        </h1>
        <p className="mt-2 text-blue-200">Convierte jerga mecánica a un lenguaje simple para tus clientes usando RAG</p>
      </header>

      <main className="w-full max-w-3xl bg-white rounded-lg shadow-md p-6 space-y-6">
        <div>
          <label className="block text-gray-700 font-bold mb-2">
            Ingresa el Diagnóstico Técnico del Mecánico:
          </label>
          <textarea
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            rows="4"
            placeholder="Ej: Falla en el sistema de inyección debido a baja presión de combustible provocada por desgaste en bomba..."
            value={diagnostico}
            onChange={(e) => setDiagnostico(e.target.value)}
          ></textarea>
        </div>

        <button
          onClick={handleTraducir}
          disabled={loading || !diagnostico}
          className={`w-full font-bold py-3 px-4 rounded-lg transition ${
            loading || !diagnostico 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg'
          }`}
        >
          {loading ? 'Generando explicación con IA...' : 'Traducir para el Cliente'}
        </button>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
            {error}
          </div>
        )}

        {resultado && (
          <div className="mt-8">
            <h2 className="text-xl font-bold text-gray-800 border-b-2 border-blue-500 pb-2 mb-4">
              Respuesta Simplificada para el Cliente:
            </h2>
            <div className="bg-blue-50 p-5 rounded-lg border border-blue-100 text-gray-800 leading-relaxed text-lg">
              {resultado}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;