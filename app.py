from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 假資料庫，用於存放事件
events = []

@app.route('/')
def index():
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        event = {
            'id': len(events) + 1,
            'name': name,
            'date': datetime.strptime(date, '%Y-%m-%d'),
            'description': description
        }
        events.append(event)
        return redirect(url_for('index'))
    return render_template('add_event.html')

@app.route('/event/<int:event_id>')
def view_event(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    return render_template('view_event.html', event=event)

@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    global events
    events = [e for e in events if e['id'] != event_id]
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = [e for e in events if query.lower() in e['name'].lower()]
        return render_template('search_results.html', events=results, query=query)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
