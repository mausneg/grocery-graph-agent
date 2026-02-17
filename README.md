# invoice-graph-agent

## Menjalankan aplikasi (Streamlit)

### 1) Siapkan database MySQL (Docker)

- Pastikan Anda punya file `.env` yang berisi minimal:
	- `MYSQL_ROOT_PASSWORD`
	- `MYSQL_DATABASE` (default schema di repo ini: `grocery_agent_db`)
	- `MYSQL_USER`
	- `MYSQL_PASSWORD`
	- `MYSQL_PORT` (contoh: `3306`)
	- `MYSQL_DB_PATH` (path ke file `database/init.sql`)

Jalankan:

```bash
docker compose up -d
```

### 2) Jalankan Streamlit

Install dependency via `pyproject.toml` (contoh memakai `uv`):

```bash
uv sync
```

Lalu jalankan UI:

```bash
streamlit run views/app.py
```

Alur penggunaan:
- Unggah invoice PDF untuk diekstrak dan disimpan ke database
- Ajukan pertanyaan (bahasa natural) untuk mendapatkan jawaban dari data di database