import requests
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urljoin
import time
import urllib3
import json
import re

BASE_URL = "https://amediavoz.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URLs a excluir (páginas de índice, no de poemas)
EXCLUDE_PATTERNS = [
    "indice", "poetas.htm", "mediavoz.htm", "sensual.htm", 
    "traducciones.htm", "poesiadeoro.htm", "ventanas.htm",
    "tucuerpo.htm", "georgia.zip", "mailto:", "javascript:"
]


def should_exclude(url):
    """Verificar si la URL debe ser excluida"""
    url_lower = url.lower()
    return any(pattern in url_lower for pattern in EXCLUDE_PATTERNS)


def get_poet_links(url):
    """Obtener enlaces a páginas de poetas desde el índice principal"""
    try:
        res = requests.get(url, headers=HEADERS, verify=False, timeout=30)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")

        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith(".htm") and not should_exclude(href):
                full_url = urljoin(url, href)
                if BASE_URL in full_url and not should_exclude(full_url):
                    links.add(full_url)

        return links
    except Exception as e:
        print(f"Error obteniendo enlaces de {url}: {e}")
        return set()


def clean_text(text):
    """Limpiar texto de espacios extra y caracteres especiales"""
    if not text:
        return ""
    # Normalizar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_poems_from_page(url):
    """Extraer todos los poemas de una página de autor"""
    try:
        res = requests.get(url, headers=HEADERS, verify=False, timeout=30)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")
        
        poemas = []
        
        # Obtener el nombre del autor del título de la página o h1
        title_tag = soup.find("title")
        autor = title_tag.text.strip() if title_tag else "Desconocido"
        
        # Buscar blockquotes que contienen los poemas
        blockquotes = soup.find_all("blockquote")
        
        for bq in blockquotes:
            # Buscar todos los párrafos dentro del blockquote
            paragraphs = bq.find_all("p")
            
            current_title = None
            current_poem_lines = []
            
            for p in paragraphs:
                text = p.get_text(separator="\n", strip=True)
                
                if not text:
                    continue
                
                # Detectar si es un título de poema (generalmente texto corto sin muchos saltos de línea)
                # o un separador de imagen
                has_img = p.find("img")
                has_link = p.find("a")
                
                if has_img:
                    # Si hay imagen y tenemos un poema acumulado, guardarlo
                    if current_title and current_poem_lines:
                        poema_texto = "\n".join(current_poem_lines)
                        if len(poema_texto) > 50:  # Solo guardar si tiene contenido significativo
                            poemas.append({
                                "autor": autor,
                                "titulo": current_title,
                                "texto": poema_texto,
                                "fuente": url
                            })
                        current_title = None
                        current_poem_lines = []
                    continue
                
                # Detectar títulos de poemas (texto corto, puede tener formato especial)
                lines = text.split("\n")
                first_line = lines[0] if lines else ""
                
                # Es probablemente un título si:
                # - Es corto (menos de 80 caracteres en la primera línea)
                # - No tiene muchas líneas (menos de 3)
                # - Contiene texto como "Poema", números, o está en el formato típico
                is_title = (
                    len(lines) <= 2 and 
                    len(first_line) < 100 and
                    not first_line.startswith('"') and
                    "©" not in text and
                    "Volver" not in text and
                    "Pulsa" not in text and
                    "www" not in text.lower()
                )
                
                if is_title and len(first_line) > 3:
                    # Guardar poema anterior si existe
                    if current_title and current_poem_lines:
                        poema_texto = "\n".join(current_poem_lines)
                        if len(poema_texto) > 50:
                            poemas.append({
                                "autor": autor,
                                "titulo": current_title,
                                "texto": poema_texto,
                                "fuente": url
                            })
                        current_poem_lines = []
                    
                    current_title = clean_text(first_line)
                    # Si hay más líneas después del título, son parte del poema
                    if len(lines) > 1:
                        current_poem_lines.extend(lines[1:])
                else:
                    # Es contenido del poema
                    current_poem_lines.extend(lines)
            
            # Guardar el último poema del blockquote
            if current_title and current_poem_lines:
                poema_texto = "\n".join(current_poem_lines)
                if len(poema_texto) > 50:
                    poemas.append({
                        "autor": autor,
                        "titulo": current_title,
                        "texto": poema_texto,
                        "fuente": url
                    })
        
        # Si no encontramos poemas en blockquotes, intentar con el body directamente
        if not poemas:
            body = soup.find("body")
            if body:
                # Buscar todos los párrafos del body
                all_paragraphs = body.find_all("p")
                current_title = None
                current_poem_lines = []
                
                for p in all_paragraphs:
                    text = p.get_text(separator="\n", strip=True)
                    
                    if not text or len(text) < 5:
                        continue
                    
                    has_img = p.find("img")
                    
                    if has_img:
                        if current_title and current_poem_lines:
                            poema_texto = "\n".join(current_poem_lines)
                            if len(poema_texto) > 50:
                                poemas.append({
                                    "autor": autor,
                                    "titulo": current_title,
                                    "texto": poema_texto,
                                    "fuente": url
                                })
                            current_title = None
                            current_poem_lines = []
                        continue
                    
                    lines = text.split("\n")
                    first_line = lines[0] if lines else ""
                    
                    # Detectar títulos
                    is_title = (
                        len(lines) <= 2 and 
                        len(first_line) < 100 and
                        len(first_line) > 3 and
                        "©" not in text and
                        "Volver" not in text
                    )
                    
                    if is_title:
                        if current_title and current_poem_lines:
                            poema_texto = "\n".join(current_poem_lines)
                            if len(poema_texto) > 50:
                                poemas.append({
                                    "autor": autor,
                                    "titulo": current_title,
                                    "texto": poema_texto,
                                    "fuente": url
                                })
                            current_poem_lines = []
                        current_title = clean_text(first_line)
                        if len(lines) > 1:
                            current_poem_lines.extend(lines[1:])
                    else:
                        current_poem_lines.extend(lines)
                
                # Guardar último poema
                if current_title and current_poem_lines:
                    poema_texto = "\n".join(current_poem_lines)
                    if len(poema_texto) > 50:
                        poemas.append({
                            "autor": autor,
                            "titulo": current_title,
                            "texto": poema_texto,
                            "fuente": url
                        })
        
        # También buscar enlaces a sub-páginas del mismo autor
        subpage_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith(".htm") and not should_exclude(href):
                full_url = urljoin(url, href)
                # Solo incluir sub-páginas que parecen ser del mismo autor
                if "#" not in full_url and full_url != url:
                    # Verificar si es una variante del mismo autor (ej: neruda2.htm)
                    base_name = url.split("/")[-1].replace(".htm", "")
                    href_name = href.replace("./", "").replace(".htm", "")
                    if base_name in href_name or href_name.startswith(base_name[:5]):
                        subpage_links.add(full_url)
        
        return poemas, subpage_links
        
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        return [], set()


def main():
    print("🔍 Iniciando scraper de amediavoz.com...")
    
    # Obtener enlaces de índices
    index_urls = [
        "https://amediavoz.com/",
        "https://amediavoz.com/indice-A-K.htm",
        "https://amediavoz.com/indice-L-Z.htm"
    ]
    
    all_poet_links = set()
    
    for index_url in index_urls:
        print(f"📚 Explorando índice: {index_url}")
        links = get_poet_links(index_url)
        all_poet_links.update(links)
        time.sleep(1)
    
    print(f"📖 Total páginas de poetas detectadas: {len(all_poet_links)}")
    
    all_poemas = []
    processed_urls = set()
    
    # Procesar cada página de poeta
    poet_links_list = sorted(all_poet_links)
    
    for i, url in enumerate(poet_links_list):
        if url in processed_urls:
            continue
            
        print(f"[{i+1}/{len(poet_links_list)}] 📜 {url}")
        
        try:
            poemas, subpages = extract_poems_from_page(url)
            processed_urls.add(url)
            
            if poemas:
                all_poemas.extend(poemas)
                print(f"   ✅ {len(poemas)} poemas extraídos")
            else:
                print(f"   ⏭️ Sin poemas encontrados")
            
            # Procesar sub-páginas
            for subpage in subpages:
                if subpage not in processed_urls and subpage not in all_poet_links:
                    print(f"   📄 Sub-página: {subpage}")
                    sub_poemas, _ = extract_poems_from_page(subpage)
                    processed_urls.add(subpage)
                    if sub_poemas:
                        all_poemas.extend(sub_poemas)
                        print(f"      ✅ {len(sub_poemas)} poemas extraídos")
                    time.sleep(0.5)
            
            # Checkpoint cada 100 poemas
            if len(all_poemas) % 100 == 0 and len(all_poemas) > 0:
                with open("poemas_tmp.json", "w", encoding="utf-8") as f:
                    json.dump(all_poemas, f, ensure_ascii=False, indent=2)
                print(f"💾 Checkpoint guardado ({len(all_poemas)} poemas)")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Eliminar duplicados basados en autor+título
    seen = set()
    unique_poemas = []
    for poema in all_poemas:
        key = (poema["autor"], poema["titulo"])
        if key not in seen:
            seen.add(key)
            unique_poemas.append(poema)
    
    # Guardado final
    with open("poemas.json", "w", encoding="utf-8") as f:
        json.dump(unique_poemas, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Scraping finalizado!")
    print(f"   📊 Total poemas únicos guardados: {len(unique_poemas)}")
    print(f"   📁 Archivo: poemas.json")


if __name__ == "__main__":
    main()

