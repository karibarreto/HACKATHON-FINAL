import datetime #propio de python
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, DateField #ES COMO UN IMPUT
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secreto'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Se crea el formulario de registro, login, institución
class RegisterForm(FlaskForm):
    name = StringField("name")
    email = EmailField("email")
    password = PasswordField("pass")
    submit = SubmitField('Regístrate')
    
class Login(FlaskForm):
    email = EmailField()
    password = PasswordField()
    submit = SubmitField('Ingresa a tu cuenta')

class InstitucionForm(FlaskForm):
    name = StringField('name')
    departamento = StringField('departamento')
    ciudad = StringField('ciudad')
    submit = SubmitField('Enviar')

class Institucion(db.Model):
    id = db.Column(db.Integer(), primary_key=True )
    name = db.Column(db.String(50), nullable = False)
    departamento = db.Column(db.String(10), nullable=False)
    ciudad = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Categorias (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Denuncias_cat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    categoria_id = db.Column(db.Integer(), db.ForeignKey('categorias.id'))
    denuncia_id = db.Column(db.Integer(), db.ForeignKey('denuncias.id'))
    descripcion = db.Column(db.String(300), nullable=True)
    calificacion = db.Column(db.String(), nullable =False)

class Denuncias (db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.Integer(), nullable=False)
    institucion_id = db.Column(db.String(), db.ForeignKey('institucion.id'))
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))

class DenunciaForm(FlaskForm):
    saneamiento_descripcion = StringField('saneamiento_descripcion')
    saneamiento_calificacion = StringField('saneamiento_calificacion')
    agua_descripcion = StringField('agua_descripcion')
    agua_calificacion = StringField('agua_calificacion')
    internet_descripcion = StringField('internet_descripcion')
    internet_calificacion = StringField('internet_calificacion')
    infraestructura_descripcion = StringField('infraestructura_descripcion')
    infraestructura_calificacion = StringField('infraestructura_calificacion')
    mobiliario_descripcion = StringField('mobiliario_descripcion')
    mobiliario_calificacion = StringField('mobiliario_calificacion')
    cableado_descripcion = StringField('cableado_descripcion')
    cableado_calificacion = StringField('cableado_calificacion')
    submit = SubmitField('Reportar')


#Class objeto que crea la tabla base de datos

# class Registro(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_Key=True)
#     name = db.Column(db.String(50), nullable = False) #nullable es para que sea campo que sí o sí debe completarse
#     email = db.Column(db.String(30), nullable = False)
#     password = db.Column(db.String(30), nullable = False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(30), nullable = False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return 'Te has registrado'
    return render_template('index.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            return redirect(url_for('institucion'))
        return "Invalid email or password!"
    
    return render_template('login.html', form=form)

@app.route('/institucion', methods=['POST', 'GET'])
def institucion():
    form = InstitucionForm()
    if form.validate_on_submit():
        new_institution = Institucion(name=form.name.data, departamento=form.departamento.data, ciudad=form.ciudad.data, user_id=current_user.id)
        db.session.add(new_institution)
        db.session.commit()
        return 'Has registrado tu institución'
    return render_template('institucion.html', form=form)

#@app.route('/denuncia_registrada', methods=['POST', 'GET'])
#def confirmacion():
    #print ("Tu reporte ha sido registrado")
    #confirmacion = confirmacion()
    #return render_template('confirmacion.html', confirmacion = confirmacion) 

@app.route('/denuncia', methods=['POST','GET'])
def denuncia():
    form= DenunciaForm()
    user = current_user.name

    inst = Institucion.query.filter_by(user_id=current_user.id).first()
    tipo_denuncia = Categorias.query.all()
    fecha = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    if form.validate_on_submit():
        new_denuncia = Denuncias(fecha=fecha, user_id= current_user.id, institucion_id=inst.id)
        db.session.add(new_denuncia)
        db.session.commit()

        pitokos = {
            'saneamiento': { 
            'calificacion': form.saneamiento_calificacion.data,
            'descripcion': form.saneamiento_descripcion.data
            },
            'agua': {
            'calificacion': form.agua_calificacion.data,
            'descripcion': form.agua_descripcion.data
            },
            'internet': {
            'calificacion': form.internet_calificacion.data,
            'descripcion': form.internet_descripcion.data
            },
            'infraestructura' :{
            'calificacion' : form.infraestructura_calificacion.data, 
            'descripcion' : form.infraestructura_descripcion.data
            },
            'mobiliario': {
            'calificacion': form.mobiliario_calificacion.data,
            'descripcion': form.mobiliario_descripcion
            },
            'cableado': {
            'calificacion': form.cableado_calificacion.data,
            'descripcion': form.cableado_descripcion.data
            }
        }
            
        for tipo in tipo_denuncia:
            new_denuncia_cat = Denuncias_cat(denuncia_id=new_denuncia.id, categoria_id = tipo.id, calificacion= pitokos[tipo.name]['calificacion'], descripcion =pitokos[tipo.name]['descripcion'])
            db.session.add(new_denuncia_cat)
            db.session.commit()
            #return  redirect(url_for('/denuncia_registrada'))

    return render_template('denuncia.html',  inst=inst ,form=form, fecha=fecha, tipo_denuncia=tipo_denuncia)


#def index ():
    #return render_template('index.html')

with app.app_context():
    db.create_all()

if __name__ =="__main__":
    app.run(debug = True)