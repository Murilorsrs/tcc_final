from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import generate_password_hash, check_password_hash
from models import db, Usuario, Configuracao, AgendaIrrigacaoAutomatica

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/tcc_final'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

        user = Usuario.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha, senha):
            return redirect(url_for('config'))
        else:
            flash('Email ou senha incorretos', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        telefone = request.form['phone']
        senha = request.form['password']

        # Criptografar a senha antes de salvar
        senha_hash = generate_password_hash(senha).decode('utf-8')

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senha_hash
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/config')
def config():
    return render_template('config.html')


@app.route('/salvar_configuracao', methods=['POST'])
def salvar_configuracao():
    id_usuario = request.form['id_usuario']
    umidade_min = request.form['umidade_min']
    umidade_max = request.form['umidade_max']

    nova_configuracao = Configuracao(
        id_usuario=id_usuario,
        umidade_min=umidade_min,
        umidade_max=umidade_max,
    )

    db.session.add(nova_configuracao)
    db.session.commit()

    return 'Configuração salva com sucesso!'


@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        data_ini = request.form['data_ini']
        data_fim = request.form['data_fim']
        hora_ini = request.form['hora_ini']
        id_config = request.form['id_config']

        nova_agenda = AgendaIrrigacaoAutomatica(
            id_usuario=id_usuario,
            data_ini=data_ini,
            data_fim=data_fim,
            hora_ini=hora_ini,
            id_config=id_config
        )

        db.session.add(nova_agenda)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('agenda.html')


if __name__ == '__main__':
    app.run(debug=True)
