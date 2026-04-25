# main.py
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_puzzle(level: int):
    """
    Generates dynamic math puzzles based on the level.
    Uses safe generation logic rather than vulnerable eval() functions.
    """
    if level <= 5:
        # Basic Arithmetic
        a, b = random.randint(1, 10 * level), random.randint(1, 10 * level)
        ops = [('+', a + b), ('-', a - b), ('*', a * b)]
        op_char, ans = random.choice(ops)
        if level <= 2 and op_char == '*': # Keep it easy for first 2 levels
            op_char, ans = '+', a + b
        return f"{a} {op_char} {b} = ?", ans
        
    elif level <= 10:
        # Linear Algebra (Solve for x)
        x = random.randint(1, 10)
        a = random.randint(2, 9)
        b = random.randint(1, 20)
        c = a * x + b
        return f"Solve for x: {a}x + {b} = {c}", x
        
    elif level <= 15:
        # Determinant of 2x2 matrix
        matrix = [[random.randint(1, 9) for _ in range(2)] for _ in range(2)]
        ans = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return f"Det of |[{matrix[0][0]}, {matrix[0][1]}], [{matrix[1][0]}, {matrix[1][1]}]|", ans
        
    else:
        # Basic Calculus: Evaluate derivative of ax^3 at x=b
        a = random.randint(2, 6)
        b = random.randint(2, 5)
        ans = 3 * a * (b ** 2)
        return f"Evaluate d/dx ({a}x^3) at x={b}", ans

@app.get("/api/puzzle")
def get_puzzle(level: int = 1):
    if level > 20:
        # The ultimate genius win state
        return {"status": "win", "message": "बधाई हो, आप एक प्रतिभाशाली हैं"}
        
    equation, answer = generate_puzzle(level)
    
    # Time limits: Starts at 10s, drops aggressively to 2s at level 20.
    time_limit_ms = max(2000, 10000 - ((level - 1) * 420))
    
    return {
        "status": "playing",
        "level": level,
        "equation": equation,
        "answer": str(answer),
        "time_limit": time_limit_ms
    }
