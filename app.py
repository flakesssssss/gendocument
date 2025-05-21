from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/anketa')
def anketa():
    return render_template ('anketa.html')

# Страница для самозанятых
@app.route('/employed-docs')
def self_employed_docs():
    return render_template('employed-docs.html')

# Страница для ИП
@app.route('/documents-ip')
def ip_docs():
    return render_template('ip-docs.html')

# Страница для ООО
@app.route('/documents-ooo')
def ooo_docs():
    return render_template('ooo-docs.html')

# Загрузка файлов для каждого типа
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('static/documents', filename)


if __name__ == '__main__':
    app.run(debug=True)