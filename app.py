from flask import Flask, render_template, request, url_for
from service import compare2files

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def compare_files():
    if request.method == 'POST':
        files = request.files
        docs = []
        for file in files:
            docs.append(files.get(file))
        try:
            left, right, p_repeat, s_repeat = compare2files(docs[0], docs[1])
            return render_template('rendering_files.html', left=left, right=right, p_repeat=p_repeat, s_repeat=s_repeat)
        except MemoryError as error:
            message = 'Ошибка памяти'
            return render_template('errors.html', error=error, message=message)
        except IndexError as error:
            message = 'Индекс Эррор. Попробуйте заново.'
            return render_template('errors.html', error=error, message=message)
        except Exception as error:
            message = 'Неизвестная ошибка'
            return render_template('errors.html', error=error, message=message)
    else:
        return render_template('start_page.html')


if __name__ == '__main__':
    app.run(debug=True)
