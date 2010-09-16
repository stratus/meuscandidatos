#!/usr/bin/env python
#
# Copyright 2010 Gustavo Franco <stratus@acm.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing sharepermissions and
# limitations under the License.

"""meuscandidatos."""

__author__ = "stratus@acm.org (Gustavo Franco)"

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms


LOOKUP_BY_KEY = "SELECT * FROM MeusCandidatos WHERE __key__ = KEY ('MeusCandidatos', :1)"


class MeusCandidatos(db.Model):
   deputado_estadual = db.IntegerProperty()
   deputado_federal = db.IntegerProperty()
   senador_primeiro = db.IntegerProperty()
   senador_segundo = db.IntegerProperty()
   governador = db.IntegerProperty()
   presidente = db.IntegerProperty(choices=[13,27,21,45,28,50,29,43,16])
   date = db.DateTimeProperty(auto_now_add=True)


class MeusCandidatosForm(djangoforms.ModelForm):
   class Meta:
      model = MeusCandidatos


class MainPage(webapp.RequestHandler):
   def get(self, id=None):
      if id:
         meuscandidatos = db.GqlQuery(LOOKUP_BY_KEY, int(id))
         template_values = { "meuscandidatos": meuscandidatos }
         path = os.path.join(os.path.dirname(__file__), "meuscandidatos.html")
         self.response.out.write(template.render(path, template_values))
      else:
         meuscandidatosform = MeusCandidatosForm()
         template_values = { "meuscandidatosform": meuscandidatosform }
         path = os.path.join(os.path.dirname(__file__), "index.html")
         self.response.out.write(template.render(path, template_values))
       
   def post(self, unused_id):
      meuscandidatos = MeusCandidatos()
      try:
         meuscandidatos.deputado_estadual = int(self.request.get("deputado_estadual"))
         meuscandidatos.deputado_federal = int(self.request.get("deputado_federal"))
         meuscandidatos.senador_primeiro = int(self.request.get("senador_primeiro"))
         meuscandidatos.senador_segundo = int(self.request.get("senador_segundo"))
         meuscandidatos.governador = int(self.request.get("governador"))
         meuscandidatos.presidente = int(self.request.get("presidente"))
      except:
         template_values = { "intexception": 1 }
         path = os.path.join(os.path.dirname(__file__), "index.html")
         self.response.out.write(template.render(path, template_values))

      try:
         key = meuscandidatos.put()
         self.redirect('/' + str(key.id()))
      except:
         template_values = { "putexception": 1 }
         path = os.path.join(os.path.dirname(__file__), "index.html")
         self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([(r"/(.*)", MainPage)],
                                     debug=True)


def main():
   run_wsgi_app(application)


if __name__ == "__main__":
   main()
