### THIS IS TASK4_1_xxx.py ###

import flask, sqlite3

app = flask.Flask(__name__)

### for Task 4.1
@app.route('/')
def index():
    return flask.render_template('index.html')

### for Task 4.2
@app.route('/latecomers/')
def latecomers():
    # connect to the db
    db = sqlite3.connect('Task4.db')

    # we can either copy paste the SQL query from TASK4_2.sql
    # or simply read the file contents straight into here
    file = open('TASK4_2.sql', 'r')
    sql = file.read()
    file.close()

    # sql is a string containing the entire file contents of TASK4_2.sql
    cursor = db.execute(sql)

    # fetch all data (list of tuples)
    data = cursor.fetchall()
    
    # remember to close the db file
    db.close()

    # same template for all rounds
    return flask.render_template('latecomers.html', data = data)


### for Task 4.3
@app.route('/add_record/')
def form():
    return flask.render_template('form.html')


### for Task 4.3
@app.route('/process_form/', methods=['POST'])
def process_form():
    # get the form data
    form_data = flask.request.form # dictionary is retrieved, keys are the input names in the HTML form
    
    # render error if direction not correct
    if form_data.get('direction') not in ['entry', 'exit']:
        return flask.render_template('error.html',
                                     visitorId = form_data.get('visitorId'),
                                     date = form_data.get('date'),
                                     time = form_data.get('time'),
                                     direction = form_data.get('direction'))
    
    # connect to the db
    db = sqlite3.connect('Task4.db')
    
    # check existence of visitorId
    cursor = db.execute('''
        SELECT id FROM Person WHERE id = ?
    ''', (form_data.get('visitorId'),))

    # fetch all data (list of tuples)
    data = cursor.fetchall()

    if len(data) == 0:
        # remember to close the db file
        db.close()
    
        # visitorId doesn't exist, render error
        return flask.render_template('error.html',
                                     visitorId = form_data.get('visitorId'),
                                     date = form_data.get('date'),
                                     time = form_data.get('time'),
                                     direction = form_data.get('direction'))

    else:
        # perform SQL insertion on the form data
        # NOTE: SQLite auto assigns id if not provided
        db.execute('''
            INSERT INTO Record(Date, Time, Type, visitorId)
            VALUES(?, ?, ?, ?)
        ''', (form_data.get('date'), form_data.get('time'), form_data.get('direction'), form_data.get('visitorId')))

        db.commit() # remember to commit changes
    
        # remember to close the db file
        db.close()
        
        return flask.render_template('success.html',
                                     visitorId = form_data.get('visitorId'),
                                     date = form_data.get('date'),
                                     time = form_data.get('time'),
                                     direction = form_data.get('direction'))


### only for deploying on Google Cloud Run (so you can preview online)
app.run('0.0.0.0', 8080)

### for running on your local machine, use this
#app.run()
