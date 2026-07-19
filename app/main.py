from fastapi import FastAPI

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": " Expense Tracker API Running"
    }
