# 📜 Visor de Poemas

Frontend para visualizar colecciones de poesía en español. Esta aplicación React consume datos JSON generados por el scraper de poemas y los presenta en una interfaz elegante y fácil de usar.

## 🌟 Características

- **Exploración visual**: Navega por la colección de poemas en una cuadrícula de tarjetas
- **Búsqueda**: Encuentra poemas por título, autor o contenido
- **Filtrado por autor**: Selecciona un autor específico para ver solo sus obras
- **Vista detallada**: Lee cada poema completo con formato preservado
- **Diseño responsive**: Funciona en desktop, tablet y móvil
- **Enlaces a fuentes**: Acceso directo a las fuentes originales

## 🚀 Inicio Rápido

### Requisitos

- Node.js 18+ 
- npm o pnpm

### Instalación

```bash
cd poem-viewer

npm install

npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## 📦 Scripts Disponibles

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Inicia el servidor de desarrollo |
| `npm run build` | Genera la build de producción |
| `npm run preview` | Previsualiza la build de producción |
| `npm run lint` | Ejecuta el linter |

## 📁 Estructura del Proyecto

```
poem-viewer/
├── public/
│   └── poemas.json      # Datos de poemas (generados por el scraper)
├── src/
│   ├── App.jsx          # Componente principal
│   ├── App.css          # Estilos del componente
│   ├── main.jsx         # Punto de entrada
│   └── index.css        # Estilos globales
├── index.html
├── package.json
└── vite.config.js
```

## 📄 Formato de Datos

El archivo `poemas.json` debe contener un array de objetos con la siguiente estructura:

```json
[
  {
    "autor": "Nombre del Autor",
    "titulo": "Título del Poema",
    "texto": "Contenido del poema...",
    "fuente": "https://url-de-la-fuente.com"
  }
]
```

## 🔧 Producción

Para generar la build de producción:

```bash
npm run build
```

Los archivos se generarán en la carpeta `dist/`. Puedes servir esta carpeta con cualquier servidor web estático.

## 🛠️ Tecnologías

- [React 19](https://react.dev/)
- [Vite](https://vite.dev/)

## 🔗 Proyectos Relacionados

Este visor forma parte de un proyecto más amplio que incluye:

- **Scraper de Poemas** (Python) - Extrae poemas de fuentes web
- **Visor de Poemas** (React) - Este proyecto

## 📝 Licencia

MIT
