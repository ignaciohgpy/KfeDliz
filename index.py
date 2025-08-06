from api import create_app

app = create_app(instance_relative_config=True)

if __name__ == '__main__':
    app.run(debug=True)




