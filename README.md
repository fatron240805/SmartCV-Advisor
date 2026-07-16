# SmartCV-Advisor

Nền tảng phân tích CV và xây dựng lộ trình phát triển

# frontend:

cd frontend
npm create vite@latest frontend -- --template react
--> select: React, TypeScript, ESLint, Yes
npm install tailwindcss @tailwindcss/vite
npm install react-router-dom
npm install axios

# backend

(môi trường ảo)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

(install trong môi trường ảo)
python -m pip install --upgrade pip

pip install fastapi "uvicorn[standard]" python-multipart pydantic-settings python-dotenv "PyJWT[crypto]" email-validator openai pymupdf python-docx

pip install motor

# run

frontend: npm run dev
backend:
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
--> thoát môi trường ảo: deactive
