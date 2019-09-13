from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask import jsonify , request, redirect, url_for
from bson.objectid import ObjectId
mongo = PyMongo()

data = [
  {
    'name':'test1',
    'last_name':'test11'
  },
  {
    'name':'test2',
    'last_name':'test22'
  }
]




def get_my_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def create_app():
  app = Flask(__name__)
  app.config.update(
  MONGO_URI='mongodb+srv://admin:testadmin@cluster0-vgyqz.mongodb.net/test?retryWrites=true&w=majority'
  )
  mongo.init_app(app)

  return app

app=create_app()


@app.route('/',methods=['GET','POST'])
def index():
  if request.method == 'POST':
    if request.form.get('insert_name')!= None:
      mongo.db.user.insert_one({'user': request.form.get('name')})
    if request.form.get('search_btn') != None:
      return render_template('index.html',data = mongo.db.user.find(),s=request.form.get('s'))
  return render_template('index.html',data = mongo.db.user.find())

@app.route('/editPost' , methods=['GET','POST'])
def editPost():
  if request.method == "POST":
    if request.form.get('delete_name')!= None :
      myquery={'_id': ObjectId(request.form.get('delete_name'))}
      mongo.db.user.delete_one(myquery)
      print('Deleted:', myquery)
      return redirect(url_for('index'))
    if request.form.get('update_name')!= None :
      myquery={'_id': ObjectId(request.form.get('update_name'))}
      newvalues={"$set": {'user': request.form.get(request.form.get('update_name'))}}
      mongo.db.user.update_one(myquery, newvalues)
      print('Updated:', myquery)
      return redirect(url_for('index'))
  return render_template('index.html')

if __name__ == '__main__':
  app.run(host='192.168.0.37', port=8000, debug=True)
 