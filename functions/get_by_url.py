# ...existing code...
from pathlib import Path
from urllib.parse import urlsplit, unquote
import requests

def download_csv_from_url(url: str, dest_path: str | Path | None = None, filename: str | None = None, timeout: int = 10) -> Path:
    """
    Descarga un archivo CSV desde una URL y lo guarda en la ruta indicada.
    - url: URL del CSV (ej. https://.../disney_plus_titles.csv)
    - dest_path: ruta de destino. Por defecto la raíz del proyecto (carpeta del repo).
    - filename: nombre de archivo de salida. Por defecto se extrae de la URL.
    - timeout: timeout en segundos para la conexión.
    Retorna: Path al archivo guardado.
    """
    if not url:
        raise ValueError("Se requiere una URL válida.")

    project_root = Path(__file__).resolve().parents[1]
    dest = Path(dest_path) if dest_path else project_root
    dest.mkdir(parents=True, exist_ok=True)

    # Nombre de archivo por defecto desde la URL
    if filename:
        out_name = filename
    else:
        path_from_url = urlsplit(url).path
        out_name = unquote(Path(path_from_url).name) or "download.csv"

    if not out_name.lower().endswith(".csv"):
        out_name += ".csv"

    out_file = dest / out_name

    # Descargar en streaming y guardar
    with requests.get(url, stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        with open(out_file, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return out_file

if __name__ == "__main__":
    # Ejemplo de uso
    destination_path = "./data"
    output_file = "disney_titles.csv"
    test_url = "https://desafio-rkd.s3.amazonaws.com/disney_plus_titles.csv"
    downloaded_file = download_csv_from_url(test_url, dest_path=destination_path)
    print(f"Archivo descargado en: {downloaded_file}")