from CT.app import app

# Only executes if it was called from standard input, a script, or from an interactive prompt
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
