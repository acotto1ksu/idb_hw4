from flask import Flask, render_template, request
import pymysql


db = pymysql.connect(host="dbdev.cs.kent.edu",user= "USER",password= "PASS",database= "acotto1") 

app = Flask(__name__)
app.debug = True


@app.route('/',  methods = ['GET'])
def index():
    if request.method == 'GET':
        cursor = db.cursor()
        query = request.args.get("search", "")
        searchby = request.args.get("by", "name")
        if (searchby == "name"):
            cursor.callproc("pmatch_name", [query])
        elif (searchby == "id"):
            cursor.callproc("pmatch_id", [query])
        result = cursor.fetchall()
        cursor.close()
        return render_template('index.html', **{"results": result})
    

@app.route('/newstudent',  methods = ['GET','POST'])
def newstudent():
    if request.method == 'POST':
        input = [request.form["id"], request.form["name"], request.form["dept"], request.form["credits"]]
        
        cursor = db.cursor()
        cursor.callproc("create_student", input)
        cursor.close()

        db.commit()

        return render_template('newstudent.html')
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.callproc("fetch_depts", [])
        result = cursor.fetchall()
        cursor.close()
        
        depts = []
        for dept in result:
            depts.append(dept[0])

        return render_template('newstudent.html', **{"depts": depts})
    
@app.route('/schedule',  methods = ['GET','POST'])
def schedule():
    if request.method == 'POST':
        return render_template('schedule.html')
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.callproc("get_schedule", [request.args.get("student_id", -1), request.args.get("year", None)])
        scheudle = cursor.fetchall()
        cursor.callproc("schedule_get_years", [request.args.get("student_id", -1)])
        years_table = cursor.fetchall()

        years = []
        for year in years_table:
            years.append(year[0])

        cursor.close()

        return render_template('schedule.html', **{"schedule": scheudle, "years": years})
    

if __name__ == '__main__':    
    app.run(port = 5000)