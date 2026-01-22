# 📜 Scrappy-Doo: Colección de Poesía en Español

Proyecto completo para recopilar y visualizar colecciones de poesía en español. Incluye un **scraper en Python** para extraer poemas de la web y un **visor en React** para explorar la colección de forma elegante e interactiva.

## 🎯 Descripción General

Este proyecto consta de dos componentes principales:

1. **Scraper de Poemas** (`scraper.py`) - Script Python que extrae poemas de [amediavoz.com](https://amediavoz.com), una biblioteca de poesía hispanoamericana
2. **Visor de Poemas** (`poem-viewer/`) - Aplicación React/Vite para explorar y leer la colección

## 📁 Estructura del Proyecto

```
scrappy-doo/
├── scraper.py           # Script de web scraping
├── requirements.txt     # Dependencias de Python
├── poemas.json          # Colección de poemas extraídos
├── poemas_tmp.json      # Checkpoint temporal del scraping
├── README.md
└── poem-viewer/         # Aplicación frontend React
    ├── public/
    │   └── poemas.json  # Copia de datos para el visor
    ├── src/
    │   ├── App.jsx      # Componente principal
    │   ├── App.css      # Estilos del componente
    │   ├── main.jsx     # Punto de entrada
    │   └── index.css    # Estilos globales
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🐍 Scraper de Poemas (Python)

### Características

- **Extracción automática** de poemas desde amediavoz.com
- **Navegación inteligente** por índices de autores (A-K, L-Z)
- **Detección de sub-páginas** para autores con múltiples páginas
- **Limpieza de texto** y formato preservado
- **Checkpoints automáticos** cada 100 poemas extraídos
- **Eliminación de duplicados** basada en autor + título
- **Delays configurados** para ser respetuoso con el servidor

### Requisitos

- Python 3.8+
- pip

### Instalación

```bash
pip install -r requirements.txt
```

### Uso

```bash
python scraper.py
```

El scraper:
1. Navega por los índices de autores
2. Extrae poemas de cada página de autor
3. Guarda checkpoints en `poemas_tmp.json`
4. Genera `poemas.json` con todos los poemas únicos

### Dependencias Python

| Paquete | Uso |
|---------|-----|
| `requests` | Peticiones HTTP |
| `beautifulsoup4` | Parsing de HTML |

---

## ⚛️ Visor de Poemas (React)

### Características

- **Exploración visual**: Navega por la colección en una cuadrícula de tarjetas
- **Búsqueda**: Encuentra poemas por título, autor o contenido
- **Filtrado por autor**: Selecciona un autor específico para ver solo sus obras
- **Vista detallada**: Lee cada poema completo con formato preservado
- **Diseño responsive**: Funciona en desktop, tablet y móvil
- **Enlaces a fuentes**: Acceso directo a las fuentes originales

### Requisitos

- Node.js 18+ 
- npm o pnpm

### Instalación y Uso

```bash
cd poem-viewer
npm install
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

### Scripts Disponibles

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Inicia el servidor de desarrollo |
| `npm run build` | Genera la build de producción |
| `npm run preview` | Previsualiza la build de producción |
| `npm run lint` | Ejecuta el linter |

### Producción

```bash
npm run build
```

Los archivos se generarán en la carpeta `dist/`. Puedes servir esta carpeta con cualquier servidor web estático.

---

## 📄 Formato de Datos

El archivo `poemas.json` contiene un array de objetos con la siguiente estructura:

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

## 🔄 Flujo de Trabajo

1. Ejecutar `python scraper.py` para extraer poemas
2. Copiar `poemas.json` a `poem-viewer/public/`
3. Ejecutar el visor con `npm run dev`

## 🛠️ Tecnologías

| Componente | Tecnologías |
|------------|-------------|
| Scraper | Python, Requests, BeautifulSoup4 |
| Visor | React 19, Vite, CSS |

## ⚠️ Notas de Uso

- El scraper incluye delays para ser respetuoso con el servidor origen
- Se desactivan las advertencias SSL para sitios con certificados expirados
- Los checkpoints permiten retomar en caso de interrupción

## 📝 Licencia

MIT
