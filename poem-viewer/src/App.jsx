import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [poemas, setPoemas] = useState([])
  const [filteredPoemas, setFilteredPoemas] = useState([])
  const [selectedPoema, setSelectedPoema] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedAutor, setSelectedAutor] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/poemas.json')
      .then(res => {
        if (!res.ok) throw new Error('Error al cargar los poemas')
        return res.json()
      })
      .then(data => {
        setPoemas(data)
        setFilteredPoemas(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    let result = poemas

    if (selectedAutor) {
      result = result.filter(p => p.autor === selectedAutor)
    }

    if (searchTerm) {
      const term = searchTerm.toLowerCase()
      result = result.filter(p =>
        p.titulo.toLowerCase().includes(term) ||
        p.autor.toLowerCase().includes(term) ||
        p.texto.toLowerCase().includes(term)
      )
    }

    setFilteredPoemas(result)
  }, [searchTerm, selectedAutor, poemas])

  const autores = [...new Set(poemas.map(p => p.autor))].sort()

  const formatTexto = (texto) => {
    return texto.split('\n').map((line, i) => (
      <span key={i}>
        {line}
        <br />
      </span>
    ))
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Cargando poemas...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error</h2>
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <h1>SuperDuper Visualizador</h1>
        <p className="subtitle">Explora una colección de poesía en español</p>
      </header>

      <div className="filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Buscar por título, autor o texto..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        <div className="filter-box">
          <select
            value={selectedAutor}
            onChange={(e) => setSelectedAutor(e.target.value)}
            className="autor-select"
          >
            <option value="">Todos los autores</option>
            {autores.map(autor => (
              <option key={autor} value={autor}>{autor}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="stats">
        Mostrando {filteredPoemas.length} de {poemas.length} poemas
      </div>

      {selectedPoema ? (
        <div className="poema-detail">
          <button className="back-btn" onClick={() => setSelectedPoema(null)}>
            ← Volver a la lista
          </button>
          <article className="poema-full">
            <h2 className="poema-title">{selectedPoema.titulo}</h2>
            <p className="poema-autor">Por: <strong>{selectedPoema.autor}</strong></p>
            <div className="poema-texto">
              {formatTexto(selectedPoema.texto)}
            </div>
            {selectedPoema.fuente && (
              <a
                href={selectedPoema.fuente}
                target="_blank"
                rel="noopener noreferrer"
                className="source-link"
              >
                Ver fuente original
              </a>
            )}
          </article>
        </div>
      ) : (
        <div className="poemas-grid">
          {filteredPoemas.map((poema, index) => (
            <article
              key={index}
              className="poema-card"
              onClick={() => setSelectedPoema(poema)}
            >
              <h3 className="card-title">{poema.titulo}</h3>
              <p className="card-autor">{poema.autor}</p>
              <p className="card-preview">
                {poema.texto.substring(0, 150)}...
              </p>
              <span className="read-more">Leer más →</span>
            </article>
          ))}
        </div>
      )}

      {filteredPoemas.length === 0 && (
        <div className="no-results">
          <p>No se encontraron poemas con los filtros seleccionados.</p>
          <button onClick={() => { setSearchTerm(''); setSelectedAutor(''); }}>
            Limpiar filtros
          </button>
        </div>
      )}

      <footer className="footer">
        <p>Colección de poemas en español</p>
      </footer>
    </div>
  )
}

export default App
