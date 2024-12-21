# metal_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass
import math

app = FastAPI()

# Activer CORS pour permettre les requêtes depuis votre site SvelteKit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de développement SvelteKit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Point(BaseModel):
    x: float
    y: float


class MetalPiece(BaseModel):
    points: List[Point]
    thickness: float
    material: str


def validate_measurements(piece: MetalPiece) -> tuple[bool, str]:
    """Valide les mesures de la pièce"""
    if len(piece.points) < 3:
        return False, "La pièce doit avoir au moins 3 points"

    # Vérifier l'épaisseur minimale et maximale
    if piece.thickness < 0.5 or piece.thickness > 50:
        return False, "L'épaisseur doit être entre 0.5mm et 50mm"

    # Vérifier les dimensions maximales
    max_x = max(p.x for p in piece.points)
    max_y = max(p.y for p in piece.points)
    if max_x > 3000 or max_y > 3000:
        return False, "Les dimensions ne peuvent pas dépasser 3000mm"

    # Vérifier les angles minimaux (éviter les angles trop aigus)
    min_angle = 30  # degrés
    for i in range(len(piece.points)):
        p1 = piece.points[i]
        p2 = piece.points[(i + 1) % len(piece.points)]
        p3 = piece.points[(i + 2) % len(piece.points)]

        # Calculer l'angle entre les segments
        angle = calculate_angle(p1, p2, p3)
        if angle < min_angle:
            return False, f"L'angle au point {i+2} est trop aigu (minimum {min_angle}°)"

    return True, "OK"


def calculate_angle(p1: Point, p2: Point, p3: Point) -> float:
    """Calcule l'angle entre trois points en degrés"""
    a = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    b = math.sqrt((p2.x - p3.x)**2 + (p2.y - p3.y)**2)
    c = math.sqrt((p3.x - p1.x)**2 + (p3.y - p1.y)**2)

    # Loi des cosinus
    cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
    angle = math.degrees(math.acos(max(-1, min(1, cos_angle))))
    return angle


@app.post("/validate-piece")
async def validate_piece(piece: MetalPiece):
    is_valid, message = validate_measurements(piece)
    return {"valid": is_valid, "message": message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
