import os
from flask import Flask, render_template, flash
from flask_pymongo import PyMongo
from flask import jsonify , request, redirect, url_for , session, json
from bson.objectid import ObjectId
from forms import RegistrationForm,LoginForm
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class 
from urllib.parse import urlparse
from apprun import host,debug,port
mongo = PyMongo()
basedir = os.path.abspath(os.path.dirname(__file__))



from forms import RegisterProductForm




def get_my_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '85cda92639ad685150b4d89ff3d1b7cc'
  app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploads') # you'll need to create a folder named uploads
  app.config.update(
  MONGO_URI='mongodb+srv://admin:testadmin@cluster0-vgyqz.mongodb.net/test?retryWrites=true&w=majority'
  )
  mongo.init_app(app)


  return app

app=create_app()
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB



@app.route('/',methods=['GET','POST'])
def index():
  if request.method == 'POST':
    if request.form.get('insert_name')!= None:
      mongo.db.user.insert_one({'user': request.form.get('name')})
    if request.form.get('search_btn') != None:
      return render_template('index.html',products = mongo.db.products.find(),s=request.form.get('s') )
  return render_template('index.html',products = mongo.db.products.find())

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

@app.route('/register', methods=['GET','POST'])
def register():
  # secret = request.args['secret']  # counterpart for url_for()
  # counterpart for session
  if session.get('secret') and json.loads(session['secret'] )['secret'] == "SqvEuIGOgE2fhrzuCq5ErQ":
    print('asd')
    form = RegisterProductForm()
    if form.validate_on_submit():
      
      filename = photos.save(form.photo.data)
      file_url = photos.url(filename)
      mongo.db.products.insert_one({'productname': form.productname.data,'description' : form.description.data,'maxEntries': form.maxEntries.data,'entries':0,'photo':urlparse(file_url).path,'videoId': form.videoId.data})
      flash(f'Product "{form.productname.data}" created!', 'success')
      return redirect(url_for('register'))
    return render_template('register.html',title="Register", form=form)
  else:
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if mongo.db.users.find_one({'email':form.email.data, 'password' : form.password.data}):
      flash('You have been logged in!','success')
      secret = json.dumps({"secret":"SqvEuIGOgE2fhrzuCq5ErQ"})
      session['secret'] = secret
      return redirect(url_for('register', secret=secret))
    else:
      flash('Login Unsuccessful. Please check username and password' , 'danger')
  return render_template('login.html',title="Login", form=form)

@app.route('/product/<string:productName>')
def product(productName):
  print(productName,'aaaaaa')
  product=mongo.db.products.find_one({'productname': productName})
  
  if product:
    return render_template('product.html',title=productName, product=product)
  else:
    return redirect(url_for('index'))

@app.route('/productName/<string:productName>',methods=['GET','POST'])
def addEntries(productName):
  if request.method == 'POST':
    if request.form.get('email') and request.form.get('entries'):
      mongoQuery={'email':request.form.get('email'),'product':productName}
      if mongo.db.candidates.find_one(mongoQuery):
        newQuery={'entries':(mongo.db.candidates.find_one(mongoQuery)['entries']+int(request.form.get('entries')))}
        mongo.db.candidates.update_one(mongoQuery, {"$set":newQuery})
      else:
        mongo.db.candidates.insert_one({'email':request.form.get('email'),'product':productName,'entries':int(request.form.get('entries'))})
      mongo.db.products.update_one({'productname':productName},{"$set":{'entries':(mongo.db.products.find_one({'productname':productName})['entries']+int(request.form.get('entries')))}})
  return redirect(url_for('product',productName=productName))




if __name__ == '__main__':
  app.run(host=host, port=port, debug=debug)