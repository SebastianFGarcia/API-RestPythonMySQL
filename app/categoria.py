from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/apipython'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db=SQLAlchemy(app)
ma=Marshmallow(app)

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desc')

categoria_schema = CategoriaSchema()

categorias_schema= CategoriaSchema(many=True)



class Categoria(db.Model):
    cat_id= db.Column(db.Integer,primary_key=True)
    cat_nom= db.Column(db.String(100))
    cat_desc= db.Column(db.String(100))

    def __init__(self,cat_nom,cat_desc):
        self.cat_nom = cat_nom
        self.cat_desc = cat_desc

db.create_all()

#Mensaje de bienvenida
@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenidos'})
#GET
@app.route('/categoria',methods=['GET'])
def get_categorias():
    all_categorias= Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)
#GET by ID
@app.route('/categoria/<id>', methods=['GET'])
def get_by_id(id):
    one_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(one_categoria)

#POST
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desc = data['cat_desc']
    nuevo_registro = Categoria(cat_nom,cat_desc)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)

#PUT
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    idcat = Categoria.query.get(id)

    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desc = data['cat_desc']

    idcat.cat_desc = cat_desc
    idcat.cat_nom = cat_nom

    db.session.commit()

    return categoria_schema.jsonify(idcat)

#DELETE
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    idcat = Categoria.query.get(id)

    db.session.delete(idcat)
    db.session.commit()

    return categoria_schema.jsonify(idcat)

if __name__=="__main__":
    app.run(debug=True)