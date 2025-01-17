import re
import jwt
import datetime
from flask import render_template, flash,jsonify , request, redirect, url_for , session, json
from projectflask import app, mongo,photos
from projectflask.forms import RegistrationForm,LoginForm,RegisterProductForm
from urllib.parse import urlparse
from functools import wraps

db=mongo.db

def token_required(f):
  @wraps(f)
  def decorated(*args,**kwargs):
    if session.get('token'):
      token = json.loads(session['token'])['token']
      try:
        data = jwt.decode(token,app.config['SECRET_KEY'])
      except:
        flash('Token timed out','danger')
        session.clear('token')
        return redirect(url_for('login'))
    else:
      return redirect(url_for('login'))
    return f(*args,**kwargs)
  return decorated


@app.route('/',methods=['GET','POST'])
def index():
  if request.method == 'POST':
    if request.form.get('insert_name')!= None:
      db.user.insert_one({'user': request.form.get('name')})
    if request.form.get('search_btn') != None:
      return render_template('index.html',products = db.products.find(),s=request.form.get('s') )
  
  return render_template('index.html',products = db.products.find().sort([('_id',-1)]))


@app.route('/register', methods=['GET','POST'])
@token_required
def register():
  form = RegisterProductForm()
  if form.validate_on_submit():
    filename = photos.save(form.photo.data)
    file_url = photos.url(filename)
    db.products.insert_one({'productname': form.productname.data,'description' : form.description.data,'maxEntries': form.maxEntries.data,'entries':0,'photo':urlparse(file_url).path,'videoId': form.videoId.data})
    flash(f'Product "{form.productname.data}" created!', 'success')
    return redirect(url_for('product',productName=form.productname.data))
  return render_template('register.html',title="Register", form=form)


@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if db.users.find_one({'email':form.email.data, 'password' : form.password.data}):
      token =jwt.encode({'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])

      flash('You have been logged in!','success')
      tokenSession = json.dumps({"token": token})
      session['token'] = tokenSession
      return redirect(url_for('register'))
    else:
      flash('Login Unsuccessful. Please check username and password' , 'danger')
  return render_template('login.html',title="Login", form=form)


@app.route('/product/<string:productName>')
def product(productName):
  product=db.products.find_one({'productname': productName})
  
  if product:
    return render_template('product.html',title=productName, product=product)
  else:
    return redirect(url_for('index'))


@app.route('/productName/<string:productName>',methods=['GET','POST'])
def addEntries(productName):
  try:
    if request.method == 'POST':
      if request.form.get('email') and request.form.get('entries') and re.search(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',request.form.get('email')) and request.form.get('entries').isnumeric():
        mongoQuery={'email':request.form.get('email'),'product':productName}
        if db.candidates.find_one(mongoQuery):
          newQuery={'entries':int(request.form.get('entries'))}
          db.candidates.update_one(mongoQuery, {"$inc":newQuery})
        else:
          db.candidates.insert_one({'email':request.form.get('email'),'product':productName,'entries':int(request.form.get('entries'))})
        flash(f'You just got { request.form.get("entries") } entries!','success')
        db.products.update_one({'productname':productName},{"$inc":{'entries':int(request.form.get('entries'))}})
      else:
        flash('Request Failed','danger')
  except:
    flash('Request Failed','danger')
  return redirect(url_for('product',productName=productName))


@app.route('/_show_entries',methods=['POST'])
def showEntries():
  candidate_email=request.form.get("candidate_email")
  productName=request.form.get("productName")
  query={'email':candidate_email,'product':productName}
  candidate=db.candidates.find_one(query,{'entries':1,'_id':0})
  print(candidate_email,productName,candidate)
  return jsonify(candidate=candidate)

