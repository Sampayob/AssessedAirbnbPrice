web: streamlit run ui.py
worker: gunicorn -w 3 -k uvicorn.workers.UvicornWorker main:app