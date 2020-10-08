web: sh setup.sh && streamlit run ui.py
server: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
