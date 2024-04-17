from App.__init__ import app

if __name__ == '__main__' :
    app.run(debug=True, port=8080)


from App import app