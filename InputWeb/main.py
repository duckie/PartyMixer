import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import cPickle as pickle


class Vote(db.Model):
    author = db.UserProperty() # Not used for the moment
    web_id = db.IntegerProperty() # Not used for the moment
    mood = db.IntegerProperty()
    like = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('root')

class VotePage(webapp.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
	    path = os.path.join(os.path.dirname(__file__), 'templates/vote.html')
	    template_values = {}
	    self.response.out.write(template.render(path, template_values))

    def post(self):
        vote = Vote()
        vote.mood = int(self.request.get('mood'))
        vote.like = int(self.request.get('like'))
        vote.put()
        self.redirect('/vote')

class GetVotePage(webapp.RequestHandler):
    def get(self):
        votes = Vote.all().order("-date")
        moods=[]
        likes=[]
        for vote in votes:
            moods.append(vote.mood)
            likes.append(vote.like)
            
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(pickle.dumps({'mood':moods,'likes':likes}))

class SeeVotePage(webapp.RequestHandler):
    def get(self):
        votes = Vote.all().order("-date")
        template_values = {'votes':votes}       
        #self.response.headers['Content-Type'] = 'text/plain'
        path = os.path.join(os.path.dirname(__file__), 'templates/see_votes.html')
        self.response.out.write(template.render(path, template_values))

class FlushDB(webapp.RequestHandler):
    def get(self):
        votes = Vote.all()
        db.delete(votes)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('flushed')

class QRPage(webapp.RequestHandler):
    def get(self):
        self.redirect('/vote')

class DumpMean(webapp.RequestHandler):
    def get(self):
        votes = Vote.all()  
        total = 0
        moods = 0;
        likes = 0;
        for vote in votes:
            moods += vote.mood
            likes += vote.like
            total += 1
        self.response.headers['Content-Type'] = 'text/plain'
        if 0 < total:
            self.response.out.write("{\"mood\":\""+str(moods/total)+"\",\"like\":\""+str(likes/total)+"\"}")
        else:
            self.response.out.write("{\"mood\":\"0\",\"like\":\"0\"}")


application = webapp.WSGIApplication(
                                     [('/', MainPage),('/vote', VotePage),('/see_votes', SeeVotePage),('/get_votes', GetVotePage),('/flush', FlushDB),('/qrhome', QRPage),('/dump_mean', DumpMean)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

