#!/bin/bash
pip install -r requirements.txt
uvicorn contratos_api:app --host 0.0.0.0 --port $PORT
