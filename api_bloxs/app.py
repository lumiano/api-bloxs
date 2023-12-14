from apiflask import APIFlask

app = APIFlask(__name__)


@app.get("/")
def hello():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    app.run(debug=True)
