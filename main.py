from flask import Flask, render_template, request, redirect, url_for

# variáveis globais
main = Flask('__name__')

# Rota para página main
@main.route('/')
def read_index():
    return render_template("index.html")

if __name__ == '__main__':
    main.run(debug=True)