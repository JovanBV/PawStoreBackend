from api.api import API

if __name__ == "__main__":
    api = API()
    api.app.run(debug=True)


