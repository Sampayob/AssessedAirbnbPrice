web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
worker: sh setup.sh && streamlit run ui.py
