from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

# === CONFIG FASTAPI ===
app = FastAPI(
    title="Bopesi AI Backend",
    description="API pour chatbot médical Flutter (Bopesi AI)",
    version="1.0.0",
)

# === CORS (autorise ton app Flutter) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # mets ton domaine Flutter plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CONFIG GEMINI ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCWX3G8hlOtXhCiLv-KTAUF1m90QhTiCVQ")
genai.configure(api_key=GEMINI_API_KEY)

# === ROUTE PRINCIPALE ===
@app.post("/ai_service")
async def ai_service(request: Request):
    """Reçoit le message de Flutter et renvoie la réponse IA"""
    data = await request.json()
    message = data.get("message", "")

    if not message:
        return {"error": "Message vide"}

    try:
        # Appel modèle gratuit Gemini
        model = genai.GenerativeModel("gemini-2.5-flash")


        prompt = (
            "Tu es un assistant médical bienveillant nommé Bopesi IA. "
            "Tu donnes des conseils de santé généraux, des explications, "
            "mais tu ne poses jamais de diagnostic strict ni de prescription. "
            "Tu encourages toujours à consulter un professionnel de santé. "
            "Réponds de manière claire et empathique.\n\n"
            "Tu dois toujours inclure une recommandation à consulter un professionnel de santé "
            f"Voici la question de l'utilisateur : {message}"
        )

        response = model.generate_content(prompt)
        return {"answer": response.text.strip()}

    except Exception as e:
        return {"error": str(e)}


# === ROUTE DE TEST ===
@app.get("/")
def root():
    return {"status": "Bopesi AI backend en ligne"}
