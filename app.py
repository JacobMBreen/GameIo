import app as app

if __name__ == '__main__':
    run_app = app.create_app()
    run_app.run(debug=True) 