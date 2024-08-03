import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import abort,render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    return render_template('index.html')

# albuns
@APP.route('/albuns')
def list_albuns():
    albuns = db.execute(
        '''
        SELECT albumId, titulo, ano_de_lancamento, genero, editora, re_gravacao 
        FROM albuns
        ORDER BY albumId
        ''').fetchall()
    return render_template('albuns-list.html', albuns=albuns)

@APP.route('/albuns/<int:id>/')
def get_album(id):
  albuns = db.execute(
      '''
      SELECT albumId, titulo, ano_de_lancamento, genero, editora, re_gravacao
      FROM albuns 
      WHERE albumId = ?
      ''', [id]).fetchone()

  if albuns is None:
      abort(404, 'Album id {} não existe.'.format(id))
      
  musicas = db.execute(
      '''
      SELECT musicas.musicaId, musicas.titulo
      FROM albuns
      JOIN musicas ON albuns.albumId = musicas.albumId
      WHERE albuns.albumId = ? 
      ORDER BY musicas.musicaId
      ''', [id]).fetchall()
  
  produtores = db.execute(
      '''
      SELECT produtores.produtorId, produtores.name
      FROM produtores
      JOIN producao ON produtores.produtorId = producao.produtorId
      JOIN albuns ON producao.albumId = albuns.albumId 
      WHERE albuns.albumId = ? 
      ORDER BY produtores.produtorId
      ''', [id]).fetchall()
  
  return render_template('albuns.html', 
           albuns=albuns, musicas=musicas, produtores=produtores)

@APP.route('/albuns/search/<expr>/')
def search_album(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  albuns = db.execute(
      ''' 
      SELECT albumId, titulo
      FROM albuns 
      WHERE titulo LIKE ?
      ''', [expr]).fetchall()

  return render_template('albuns-search.html',
           search=search,albuns=albuns)

#musicas
@APP.route('/musicas')
def list_musicas():
    musicas = db.execute(
        '''
        SELECT musicaId, titulo, duracao, from_the_vault
        FROM musicas
        ORDER BY musicaId
        ''').fetchall()
    return render_template('musicas-list.html', musicas=musicas)

@APP.route('/musicas/<int:id>/')
def get_musica(id):
    musicas = db.execute(
        '''
        SELECT musicas.musicaId, musicas.titulo, musicas.duracao, musicas.from_the_vault,
        albuns.albumId, albuns.titulo AS album_titulo
        FROM musicas
        JOIN albuns ON musicas.albumId = albuns.albumId
        WHERE musicas.musicaId = ?
        ''', [id]).fetchone()

    if musicas is None:
        abort(404, 'Música id {} não existe.'.format(id))

    artistas_convidados = db.execute(
        '''
        SELECT artistas_convidados.artistaId, artistas_convidados.nome
        FROM artistas_convidados
        JOIN colaboracoes_NEW ON artistas_convidados.artistaId = colaboracoes_NEW.artistaId
        JOIN musicas ON colaboracoes_NEW.musicaId = musicas.musicaId
        WHERE musicas.musicaId = ? 
        ORDER BY artistas_convidados.artistaId
        ''', [id]).fetchall()

    return render_template('musicas.html', 
            musicas=musicas, artistas_convidados=artistas_convidados)

@APP.route('/musicas/search/<expr>/')
def search_musica(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  musicas = db.execute(
      ''' 
      SELECT musicaId, titulo
      FROM musicas 
      WHERE titulo LIKE ?
      ''', [expr]).fetchall()

  return render_template('musicas-search.html',
           search=search,musicas=musicas)

#concerto
@APP.route('/concertos')
def verconcertos():
    concertos = db.execute(
        '''
        SELECT concertoId, comparecimento, receita, localId
        FROM concertos
        ORDER BY concertoId
        ''').fetchall()
    return render_template('concerto.html', concertos=concertos)

@APP.route('/concertos/<int:id>/')
def get_concerto(id):
  concertos = db.execute(
      '''
      SELECT concertoId, comparecimento, receita, localId
      FROM concertos 
      WHERE concertoId = ?
      ''', [id]).fetchone()

  if concertos is None:
      abort(404, 'Concerto id {} não existe.'.format(id))
      
  locais = db.execute(
      '''
      SELECT locais.localId, locais.estadio
      FROM locais
      JOIN concertos ON locais.localId = concertos.localId
      WHERE concertos.concertoId = ? 
      GROUP BY locais.localId
      ORDER BY locais.localId
      ''', [id]).fetchall()
  
  artistas_convidados = db.execute(
      '''
      SELECT artistas_convidados.artistaId, artistas_convidados.nome
      FROM artistas_convidados
      JOIN atos_de_abertura_NEW ON artistas_convidados.artistaId = atos_de_abertura_NEW.artistaId
      JOIN concertos ON atos_de_abertura_NEW.concertoId = concertos.concertoId
      WHERE concertos.concertoId = ? 
      ORDER BY artistas_convidados.artistaId
      ''', [id]).fetchall()
  
  return render_template('concertos.html', 
           concertos=concertos, locais=locais, artistas_convidados=artistas_convidados)

@APP.route('/locais/search/<expr>/')
def search_local(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  locais = db.execute(
      ''' 
      SELECT localId, pais, estadio
      FROM locais 
      WHERE pais LIKE ?
      ''', [expr]).fetchall()
  return render_template('locais-search.html',
           search=search,locais=locais)

#locais
@APP.route('/locais')
def verlocal():
    locais = db.execute(
        '''
        SELECT localId, pais, cidade, estadio
        FROM locais
        ORDER BY localId
        ''').fetchall()
    return render_template('locais-list.html', locais=locais)

@APP.route('/locais/<int:id>/')
def get_local(id):
  locais = db.execute(
      '''
      SELECT localId, pais, cidade, estadio
      FROM locais 
      WHERE localId = ?
      ''', [id]).fetchone()
      
  concertos = db.execute(
      '''
      SELECT concertos.concertoId
      FROM concertos
      JOIN locais ON concertos.localId = locais.localId
      WHERE locais.localId = ? 
      ORDER BY concertos.concertoId
      ''', [id]).fetchall()
  
  return render_template('locais.html', 
           locais=locais, concertos=concertos )

#produtores
@APP.route('/produtores')
def verprodutor():
    produtores = db.execute(
        '''
        SELECT produtorId, name
        FROM produtores
        ORDER BY produtorId
        ''').fetchall()
    return render_template('produtores.html', produtores=produtores)

@APP.route('/produtores/<int:id>/')
def get_produtor(id):
  produtores = db.execute(
      '''
      SELECT produtorId, name
      FROM produtores 
      WHERE produtorId = ?
      ''', [id]).fetchone()
      
  albuns = db.execute(
      '''
      SELECT albuns.albumId, albuns.titulo 
      FROM albuns
      JOIN producao ON albuns.albumId = producao.albumId
      JOIN produtores ON producao.produtorId = produtores.produtorId
      WHERE produtores.produtorId = ? 
      ORDER BY albuns.albumId
      ''', [id]).fetchall()
  
  return render_template('produtores.html', 
           produtores=produtores,albuns=albuns)

#abertura
@APP.route('/abertura')
def verabertura():
    artistas_convidados = db.execute(
        '''
        SELECT artistaId, nome
        FROM artistas_convidados
        ORDER BY artistaId
        ''').fetchall()
    return render_template('abertura.html', artistas_convidados=artistas_convidados)

@APP.route('/abertura/<int:id>/')
def get_abertura(id):
  artistas_convidados = db.execute(
        '''
        SELECT artistaId, nome
        FROM artistas_convidados
        WHERE artistaId = ?
        ''', [id]).fetchone()
      
  concertos = db.execute(
      '''
      SELECT concertos.concertoId 
      FROM concertos
      JOIN atos_de_abertura_NEW ON concertos.concertoId = atos_de_abertura_NEW.concertoId
      JOIN artistas_convidados ON atos_de_abertura_NEW.artistaId = artistas_convidados.artistaId
      WHERE artistas_convidados.artistaId = ? 
      ORDER BY concertos.concertoId
      ''', [id]).fetchall()
  
  return render_template('abertura.html', 
           artistas_convidados=artistas_convidados,concertos=concertos)

#colaboracoes
@APP.route('/colaboracoes')
def vercolaboracao():
    artistas_convidados = db.execute(
        '''
        SELECT artistaId, nome
        FROM artistas_convidados
        ORDER BY nome
        ''').fetchall()
    return render_template('colaboracoes.html', artistas_convidados=artistas_convidados)

@APP.route('/colaboracoes/<int:id>/')
def get_colaboracao(id):
  artistas_convidados = db.execute(
        '''
        SELECT artistaId, nome
        FROM artistas_convidados
        WHERE artistaId = ?
        ''', [id]).fetchone()
      
  musicas = db.execute(
      '''
      SELECT musicas.musicaId, musicas.titulo 
      FROM musicas
      JOIN colaboracoes_NEW ON musicas.musicaId = colaboracoes_NEW.musicaId
      JOIN artistas_convidados ON colaboracoes_NEW.artistaId = artistas_convidados.artistaId
      WHERE artistas_convidados.artistaId = ? 
      ORDER BY musicas.musicaId
      ''', [id]).fetchall()
  
  return render_template('colaboracoes.html', 
           artistas_convidados=artistas_convidados,musicas=musicas)