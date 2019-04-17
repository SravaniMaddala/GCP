#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GENRE_NAME = 'Action'
user = 'None'



# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

'''def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)'''

def genre_key(genre_name=DEFAULT_GENRE_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Genre', genre_name)
def user_key(user_name=user):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('User', user_name)

# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


'''class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]'''

class Genre_Data(ndb.Model):
    title = ndb.StringProperty()
    director = ndb.StringProperty()
    mainactor1 = ndb.StringProperty()
    mainactor2 = ndb.StringProperty()
    yearofrel = ndb.StringProperty()
    duration = ndb.StringProperty()
    buy_price = ndb.FloatProperty()
    rent_price = ndb.FloatProperty()
    author = ndb.StructuredProperty(Author)
class order(ndb.Model):
    title = ndb.StringProperty()
    price = ndb.FloatProperty()
    #rent_price = ndb.FloatProperty()
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    label = ndb.StringProperty()


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        genre_name = self.request.get('genre_name', DEFAULT_GENRE_NAME)
        '''guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)'''

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        template_values = {

            'genre_name': urllib.quote_plus(genre_name),
            'user': user,
            'url': url,
            'url_linktext': url_linktext,

        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START guestbook]
class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.


        genre_name = self.request.get('genre_name',
                                          DEFAULT_GENRE_NAME)
        
        user = users.get_current_user()
        url_linktext1 = 'Back to main page'
        url1 = 'https://www.w3schools.com'
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values1 = {

            'url_linktext1': url_linktext1,

            'genre_name': urllib.quote_plus(genre_name),
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
    
        }
        
        template1 = JINJA_ENVIRONMENT.get_template('enternewmovie.html')
        self.response.write(template1.render(template_values1))
        #self.response.write('Hello')
    def get(self):
        genre_name = self.request.get('category',DEFAULT_GENRE_NAME)
        user = users.get_current_user()                                
        url_linktext1 = 'Back to main page'
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values1 = {

            'url_linktext1': url_linktext1,

            'genre_name': urllib.quote_plus(genre_name),
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
    
        }
        
        template1 = JINJA_ENVIRONMENT.get_template('enternewmovie.html')
        self.response.write(template1.render(template_values1))
        
# [END guestbook]


class Saveinfo(webapp2.RequestHandler):
    def post(self):
        genre_name = self.request.get('genre_name',DEFAULT_GENRE_NAME)

        genre = Genre_Data(parent = genre_key(genre_name.lower()))

        genre.title = self.request.get('title')
        genre.director = self.request.get('director')
        genre.mainactor1 = self.request.get('mainactor1')
        genre.mainactor2 = self.request.get('mainactor2')
        genre.yearofrel = self.request.get('yearofrel')
        genre.duration = self.request.get('duration')
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        if(genre.title == '' or genre.director == '' or genre.yearofrel == '' or genre.duration == ''):
            Error = 'Error: all fields must be filled in'
            template_values = {
             
            'genre_name': urllib.quote_plus(genre_name),
            'Error': Error,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
          
            }

            template = JINJA_ENVIRONMENT.get_template('enternewmovie.html')
            self.response.write(template.render(template_values))
        else:
            genre.buy_price = float(self.request.get('buy_price'))
            genre.rent_price = float(self.request.get('rent_price'))
            genre.put()
            query_params = {'genre_name': genre_name}
            self.redirect('/?' + urllib.urlencode(query_params))
    def get(self):
        genre_name = self.request.get('category',DEFAULT_GENRE_NAME)
        user = users.get_current_user()                                
        url_linktext1 = 'Back to main page'
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values1 = {

            'url_linktext1': url_linktext1,

            'genre_name': urllib.quote_plus(genre_name),
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
    
        }
        
        template1 = JINJA_ENVIRONMENT.get_template('enternewmovie.html')
        self.response.write(template1.render(template_values1))
    
        


class displayinfo(webapp2.RequestHandler):
    def get(self):
        genre_name = self.request.get('category',
                                          DEFAULT_GENRE_NAME)
        genre_query = Genre_Data.query(ancestor=genre_key(genre_name.lower()))
        genre = genre_query.fetch(100)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'genre': genre,
            'genre_name': urllib.quote_plus(genre_name),
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
          
        }

        template = JINJA_ENVIRONMENT.get_template('browseindex.html')
        self.response.write(template.render(template_values))

class searchinfo(webapp2.RequestHandler):

    def get(self):
        genre_name = self.request.get('category',
                                          DEFAULT_GENRE_NAME)
        
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        url_linktext1 = 'Back to main page'
        url1 = 'https://www.w3schools.com'
        template_values1 = {

            'url_linktext1': url_linktext1,

            'genre_name': urllib.quote_plus(genre_name),
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
    
        }
        
        template1 = JINJA_ENVIRONMENT.get_template('searchindex.html')
        self.response.write(template1.render(template_values1))
    def post(self):
        genre_name = self.request.get('genre_name',
                                          DEFAULT_GENRE_NAME)
        user = users.get_current_user()
        genre_query = Genre_Data.query(ancestor=genre_key(genre_name.lower()))
        gettitle = self.request.get('title')
        getdirector = self.request.get('director')
        getmainactor = self.request.get('mainactor')
        getyearofrel = self.request.get('yearofrel')
        print getdirector
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        #print getdirector'''
        #genre_query1 = genre_query.filter(Genre_Data.title == title)
        '''for g in genre_query:
            if(gettitle in g.title):
                print g.title'''
        que = []
        found = 0
        if(getyearofrel == '' and getdirector == '' and getmainactor == '' and gettitle == ''):
            Error = 'Error : at least one field must be entered'
            found = 10
        else:
            Error = ''
            for q in genre_query:
                if(gettitle.lower() in q.title.lower()):
                    if(getdirector.lower() in q.director.lower()):
                        if((getmainactor.lower() in q.mainactor1.lower()) or (getmainactor.lower() in q.mainactor2.lower())):
                            if(getyearofrel == ''):
                                que.append(q)
                                found = 1
                            else:
                                if(getyearofrel == q.yearofrel):
                                    que.append(q)
                                    found = 1
        if(found == 0):
            Found = 'No movies match your search'
        else:
            Found = ''
               
        #genre = genre_query.fetch(50)
        template_values = {
            'genre': que,
            'genre_name': urllib.quote_plus(genre_name),
            'Error': Error,
            'Found': Found,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
          
        }

        template = JINJA_ENVIRONMENT.get_template('searchindex.html')
        self.response.write(template.render(template_values))

class displaycart(webapp2.RequestHandler):
    def get(self):
        genre_name = self.request.get('category',
                                          DEFAULT_GENRE_NAME)
        user = users.get_current_user()
        print(user)
        if(user == None):
            if user:
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_linktext = 'Login'
            template_values = {
                
                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                
          
            }
        
            template = JINJA_ENVIRONMENT.get_template('loginreq.html')
            self.response.write(template.render(template_values))
            
        else:
            ###user_name = self.request.get('user',user.email())
            user_name = user.email()
            user_query = order.query(ancestor=user_key(user_name))
            user_data = user_query.fetch(100)
            print(user_data)
            Total_cost = 0
            for i in user_data:
                Total_cost += i.price
        
            if user:
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_linktext = 'Login'
            template_values = {
                'user_data': user_data,
                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                'Total_cost':Total_cost,
          
            }
        
            template = JINJA_ENVIRONMENT.get_template('displaycart.html')
            self.response.write(template.render(template_values))
        

class addtocart(webapp2.RequestHandler):
    def get(self):
        genre_name = self.request.get('category',
                                          DEFAULT_GENRE_NAME)
        
        genre_query = Genre_Data.query(ancestor=genre_key(genre_name.lower()))
        genre = genre_query.fetch(100)
        status = 'Added to Cart'
        user = users.get_current_user()
        if(user == None):
            if user:
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_linktext = 'Login'
            template_values = {
                
                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                
          
            }
        
            template = JINJA_ENVIRONMENT.get_template('addreq.html')
            self.response.write(template.render(template_values))
        else:
            if user:
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_linktext = 'Login'
            
            
            #print(genre[0].title)
            user_name = user.email()
            ###user_name = self.request.get('user',user)
            
            user_data = order(parent = user_key(user_name))
            user_data.title = self.request.get('title')
            print(self.request.get('label'))
            print('Hi')
            user_data.label = self.request.get('label')
            user_data.price = float(self.request.get('price'))
            ####user_data.price = 100
            #user_data.rent_price = float(self.request.get('rent_price'))
            user_data.email = self.request.get('user')
            user_query_out = order.query(ancestor=user_key(user_name))
            user_data_out = user_query_out.fetch(500)
            present =0;
            status = '';
            for i in user_data_out:
                if(i.title == user_data.title):
                    present = 1;
            
            if(present ==0):       
                user_data.put()
            else:
                status = 'Item already added to cart'

            template_values = {
                'genre': genre,
                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                'status': status,
              
            }
            
            #print(order(parent = user_key(user_name)))
            #print(self.request.get('buy_price') )
            #print(self.request.get('user') )

            template = JINJA_ENVIRONMENT.get_template('browseindex.html')
            self.response.write(template.render(template_values))
            #$query_params = {'genre_name': genre_name}
            #$self.redirect('/display' + urllib.urlencode(query_params))
        
class checkout(webapp2.RequestHandler):
    def get(self):
        genre_name = self.request.get('category',
                                          DEFAULT_GENRE_NAME)
        
        user = users.get_current_user()
        print('while logging out')
        print(user)    
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        
        if(user == None):
            
            template_values = {
                
                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                
          
            }
        
            template = JINJA_ENVIRONMENT.get_template('checkout.html')
            self.response.write(template.render(template_values))
        else:
            user_name = user.email()
            #print(user_name)
            print('HiHI')
            ###user_name = self.request.get('user',user.email())
            user_query = order.query(ancestor=user_key(user_name))
            user_data = user_query.fetch(100)
            for i in user_data:
                i.key.delete()
            template_values = {
                'user_data': user_data,
                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                   
                  
            }
                
            template = JINJA_ENVIRONMENT.get_template('checkout.html')
            self.response.write(template.render(template_values))
class deletefromcart(webapp2.RequestHandler):
    def get(self):
        genre_name = self.request.get('category',
                                          DEFAULT_GENRE_NAME)
        user = users.get_current_user()
        user_name = user.email()
        ###user_name = self.request.get('user',user.email())
        user_query = order.query(ancestor=user_key(user_name))
        user_data = user_query.fetch(100)
        for i in user_data:
            print(i)
            print(i.title)
            if(i.title == self.request.get('title') and i.price == float(self.request.get('price'))):
                print('delete')
                i.key.delete()
                
        user = users.get_current_user()
        user_name = user.email()
        ###user_name = self.request.get('user',user.email())
        user_query = order.query(ancestor=user_key(user_name))
        user_data = user_query.fetch(100)
        Total_cost = 0
        for i in user_data:
            Total_cost += i.price
       
        
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'user_data': user_data,
            'genre_name': urllib.quote_plus(genre_name),
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'Total_cost':Total_cost,
           
          
        }
        
        template = JINJA_ENVIRONMENT.get_template('displaycart.html')
        self.response.write(template.render(template_values))
class addtocart_search(webapp2.RequestHandler):
    def get(self):
        genre_name = self.request.get('category',
                                          DEFAULT_GENRE_NAME)
        
        user = users.get_current_user()
        if(user == None):
            if user:
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_linktext = 'Login'
            template_values = {
                
                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                
          
            }
        
            template = JINJA_ENVIRONMENT.get_template('addreq.html')
            self.response.write(template.render(template_values))
        else:
            if user:
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
            else:
                url = users.create_login_url(self.request.uri)
                url_linktext = 'Login'
            url_linktext1 = 'Back to main page'
            url1 = 'https://www.w3schools.com'
           
            user_name = user.email()
            ###user_name = self.request.get('user',user)
            print(self.request.get('user',user))
            
            user_data = order(parent = user_key(user_name))
            user_data.title = self.request.get('title')
            user_data.price = float(self.request.get('price'))
            ####user_data.price = 100
            #user_data.rent_price = float(self.request.get('rent_price'))
            user_data.email = self.request.get('user')
            user_data.label = self.request.get('label')

            user_query_out = order.query(ancestor=user_key(user_name))
            user_data_out = user_query_out.fetch(500)
            present =0;
            status = '';
            for i in user_data_out:
                if(i.title == user_data.title):
                    present = 1;
            
            if(present ==0):       
                user_data.put()
            else:
                status = 'Item already added to cart'
            
            #print(order(parent = user_key(user_name)))
            print(self.request.get('buy_price') )
            print(self.request.get('user') )
            template_values1 = {

                'url_linktext1': url_linktext1,

                'genre_name': urllib.quote_plus(genre_name),
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                'status':status,
        
            }
            
            template1 = JINJA_ENVIRONMENT.get_template('searchindex.html')
            self.response.write(template1.render(template_values1))

            
# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Enter', Guestbook),
    ('/Save', Saveinfo),
    ('/display', displayinfo),
    ('/search', searchinfo),
    ('/displaycart', displaycart),
    ('/addtocart', addtocart),
    ('/checkout',checkout),
    ('/delete',deletefromcart),
    ('/addtocart_search',addtocart_search)
], debug=True)
# [END app]
