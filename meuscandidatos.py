import cgi

#from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class MeusCandidatos(db.Model):
    deputado_estadual = db.IntegerProperty()
    deputado_federal = db.IntegerProperty()
    senador_primeiro = db.IntegerProperty()
    senador_segundo = db.IntegerProperty()
    governador = db.IntegerProperty()
    presidente = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')

        candidatos = db.GqlQuery("SELECT * FROM MeusCandidatos ORDER BY date DESC LIMIT 10")

        self.response.out.write('Ultimos presidentes registrados')
        for candidato in candidatos:
           self.response.out.write('<b>%s</b> para presidente.' % candidato.presidente)

        self.response.out.write("""
              <form action="/registrar" method="post">
                <div><input type="text" name="deputado_estadual"></input></div>
                <div><input type="text" name="deputado_federal"></input></div>
                <div><input type="text" name="senador_primeiro"></input></div>
                <div><input type="text" name="senador_segundo"></input></div>
                <div><input type="text" name="governador"></input></div>
                <div><input type="text" name="presidente"></input></div>
                <div><input type="submit" value="Enviar"></div>
              </form>
            </body>
          </html>""")

class Candidatos(webapp.RequestHandler):
    def post(self):
        meuscandidatos = MeusCandidatos()
        meuscandidatos.deputado_estadual = int(self.request.get('deputado_estadual'))
        meuscandidatos.deputado_federal = int(self.request.get('deputado_federal'))
        meuscandidatos.senador_primeiro = int(self.request.get('senador_primeiro'))
        meuscandidatos.senador_segundo = int(self.request.get('senador_segundo'))
        meuscandidatos.governador = int(self.request.get('governador'))
        meuscandidatos.presidente = int(self.request.get('presidente'))
        meuscandidatos.put()
        self.redirect('/')


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/registrar', Candidatos)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
