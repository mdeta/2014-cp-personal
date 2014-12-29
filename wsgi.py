#@+leo-ver=5-thin
#@+node:lee.20141224110313.46: * @file wsgi.py
#@@language python
#@@tabwidth -4

#@+<<decorations>>
#@+node:lee.20141215164031.47: ** <<decorations>>
import cherrypy
import os
from symbol import *
import random
from mako.lookup import TemplateLookup
from asciisymbol import asciiImage
#@-<<decorations>>

#@+others
#@+node:lee.20141215164031.48: ** folder setting
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
    tmp_dir = data_dir + 'tmp'
    templates_dir = os.environ['OPENSHIFT_REPO_DIR'] + 'templates'
    static_dir = os.environ['OPENSHIFT_REPO_DIR'] + 'static'
    std_dir = os.environ['OPENSHIFT_REPO_DIR'] + 'std/'
else:
    # 表示程式在近端執行
    data_dir = _curdir + "/local_data/"
    templates_dir = _curdir + "/templates"
    tmp_dir = data_dir + '/tmp'
    static_dir = _curdir + '/static'
    std_dir = _curdir + '/std/'


env = TemplateLookup(directories=[templates_dir], input_encoding = 'utf-8', output_encoding = 'utf-8', )

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)
#@+node:lee.20141221203113.57: ** student setting
std_class = 'a'
std_list = None
ta_mode = True
ta_list = None

if std_class == 'a':
    std_list = [["403231{0:02d}".format(s), "active"] for s in range(1, 58)]
else:
    std_list = [['40031226', 'active'], ['40223216', 'active']] + [["403232{0:02d}".format(s), "active"] for s in range(1, 57)]

if ta_mode:
    ta_list = [('example', 'active'), ('example1','active'), ('example2','active')]
#@+node:lee.20141229095026.59: ** class Application
class Application(object):
    #@+others
    #@+node:lee.20141215164031.51: *3* _cp_config
    _cp_config = {

        'tools.encode.encoding': 'utf-8',    
        'tools.sessions.on' : True,
        'tools.sessions.storage_type' : 'file',
        'tools.sessions.locking' : 'early',
        'tools.sessions.storage_path' : tmp_dir,
        'tools.sessions.timeout' : 60,
    }
    #@+node:lee.20141229095026.60: *3* def init
    def __init__(self):
        # 你的 github repository url
        self.github_repo_url = 'https://github.com/mdeta/2014-cp-ab'
        # 你的 bitbucket repository url
        self.bitbucket_repo_url = ''



    #@+node:lee.20141229095026.61: *3* def use_template
    def use_template(self, content):
        above = """
        <!DOCTYPE html>
    <html lang="en">
    <head>

      <!-- Basic Page Needs
      –––––––––––––––––––––––––––––––––––––––––––––––––– -->
      <meta charset="utf-8">
      <title>title</title>
      <meta name="description" content="">
      <meta name="author" content="">

      <!-- Mobile Specific Metas
      –––––––––––––––––––––––––––––––––––––––––––––––––– -->
      <meta name="viewport" content="width=device-width, initial-scale=1">

      <!-- FONT
      –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <style>
    @font-face {
      font-family: 'Raleway';
      font-style: normal;
      font-weight: 300;
      src: local('Raleway Light'), local('Raleway-Light'), url(/static/font/Raleway300.woff) format('woff');
    }
    @font-face {
      font-family: 'Raleway';
      font-style: normal;
      font-weight: 400;
      src: local('Raleway'), url(/static/font/Raleway400.woff) format('woff');
    }
    @font-face {
      font-family: 'Raleway';
      font-style: normal;
      font-weight: 600;
      src: local('Raleway SemiBold'), local('Raleway-SemiBold'), url(/static/font/Raleway600.woff) format('woff');
    }
    </style>

      <!-- CSS
      –––––––––––––––––––––––––––––––––––––––––––––––––– -->
      <link rel="stylesheet" href="/static/css/normalize.css">
      <link rel="stylesheet" href="/static/css/skeleton.css">
      <link rel="stylesheet" href="/static/css/custom.css">
      <!-- Favicon
      –––––––––––––––––––––––––––––––––––––––––––––––––– -->
      <link rel="icon" type="image/png" href="/static/images/favicon.png" />

    </head>
    <body>

      <!-- Primary Page Layout
      –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    <!-- .container is main centered wrapper -->
    <div class="container">
    """
        below = """
    </div>
    <footer class="center">
      2014 Computer Programming
    </footer>

    <!-- Note: columns can be nested, but it's not recommended since Skeleton's grid has %-based gutters, meaning a nested grid results in variable with gutters (which can end up being *really* small on certain browser/device sizes) -->

    <!-- End Document
      –––––––––––––––––––––––––––––––––––––––––––––––––– -->
    </body>
    </html>
    """
        return above + self.generate_nav(self.link()) + content + below
    #@+node:lee.20141229095026.62: *3* def generate_nav
    def generate_nav(self, anchors):
        above_side = """
        <div class="row">
            <div class="nav twelve columns">
                <input type="checkbox" id="toggle" />
                <div>
                    <label for="toggle" class="toggle" data-open="Main Menu" data-close="Close Menu" onclick></label>
                    <ul class="menu">
        """

        content = ''
        for link, name in anchors:
            content += '<li><a href="' + link + '">' + name + '</a></li>'

        below_side = """
                    </ul>
                </div>
            </div>
        </div>
        """
        return above_side + content + below_side
    #@+node:lee.20141229095026.63: *3* def generate_form_page
    def generate_form_page(self, form='', output=''):
        content = """
            <div class="content">
            <div class="row">
              <div class="one-half column">
                %s
              </div>
              <div class="one-half column">
                <div class="output u-full-width">
                  <p>Output:</p>
                  <p>
                    %s
                  </p>
                </div>
              </div>
            </div>
          </div>
        """%(form, output)
        return self.use_template(content)
    #@+node:lee.20141229095026.64: *3* def generate_headline_page
    def generate_headline_page(self, headline, output):
        content = """
      <div class="content">
        <div class="row">
          <div class="headline center">%s</div>
          <div class="twelve columns">
            <p>%s</p>
          </div>
        </div>
      </div>
        """ % (headline, output)
        return self.use_template(content)
    #@+node:lee.20141229095026.65: *3* def generate_personal_page
    def generate_personal_page(self, data=None):
        if data is None:
            return ''

        # check data have all we need, if the key not exist, use empty string
        must_have_key = ('photo_url', 'name', 'ID', 'class', 'evaluation')
        for key in must_have_key:
            data[key] = data.get(key, '')


        if 'evaluation' in data:
            table_content = ''
            for projectName, score in data['evaluation']:
                table_content += """<tr><td>%s</td><td>%s</td>"""%(projectName, score)
            data['evaluation'] = table_content
        content = """
    <div class="content">
    <div class="row">
      <div class="one-half column">
        <div class="headline">
          About Me
        </div>
        <div class="photo">
          <img src="{photo_url:s}" alt="photo">
        </div>
        <div class="meta">
          <ul>
            <li>Name: {name:s}</li>
            <li>ID NO. : {ID:s}</li>
            <li>Class: {class:s}</li>
          </ul>
        </div>
      </div>
      <div class="one-half column">
        <div class="headline">
          Self Evaluation
        </div>
        <div>
          <table class="u-full-width">
            <thead>
              <tr>
                <th>Project Name</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
                {evaluation:s}
            </tbody>
          </table>

        </div>
      </div>
    </div>
    </div>
        """.format(**data)
        return self.use_template(content)
    #@+node:lee.20141229095026.66: *3* def link
    def link(self):
        aviable_link = [("index", "HOME"), ("guessForm", "猜數字"), ("asciiForm", "使用圖案列印文字"), (self.github_repo_url, "個人 github repo"), (self.bitbucket_repo_url, "個人 bitbucket repo")]
        return aviable_link
    #@+node:lee.20141229095026.68: *3* def index
    @cherrypy.expose
    def index(self):
        # 這裡是首頁
        return self.generate_headline_page('首頁', '這裡是首頁')
    #@+node:lee.20141229095026.112: *3* def asciiForm
    @cherrypy.expose
    def asciiForm(self, text=None):
        # form, action to asciiOutput
        # set up messages
        messages = {
            'welcome': 'welcome to ascii form',
        }
        content = """
        <form method="get" action="">
            <label for="text">Say....</label>
            <input type="text" name="text" />
            <input type="submit" value="Send" class="button button-primary">
        </form>
        """
        output = ''
        # if text is None, set output to welcome
        if text is None:
            output = messages.get('welcome')
        # if not None, start process
        else:
            # use module asciisymol's asciiImage function
            # one arg, input type string
            output = asciiImage(text)
        return self.generate_form_page(content, output)
    #@+node:lee.20141229095026.113: *3* def guessForm
    @cherrypy.expose
    def guessForm(self, guessNumber=None):
        # get count from session
        count = cherrypy.session.get("count", None)
        # if is None, it mean it does not exist
        if not count:
            # create one
            count = cherrypy.session["count"] = 0

        # get answer from session
        answer = cherrypy.session.get("answer", None)
        # if is None, it mean it does not exist
        if not answer:
            # create one
            answer = cherrypy.session["answer"] = random.randint(1, 100)

        form = """
        <form action="" method="get">
          <label for="guessNumber">Guess Number(1~99)</label>
          <input name="guessNumber" type="text">
          <input type="submit" value="Send" class="button button-primary">
        </form>
        """

        message = {
            "welcome": "guess a number from 1 to 99",
            "error": "must input a number, your input is %s" % str(guessNumber),
            "successful": "correct! your input is %s answer is %d total count %d" % (str(guessNumber), answer, count),
            "smaller": "smaller than %s and total count %d" % (str(guessNumber), count),
            "bigger": "bigger than %s and total count %d" % (str(guessNumber), count),
        }

        if guessNumber is None:
            return self.generate_form_page(form, message["welcome"])
        else:
            # convert guessNumber to int
            try:
                guessNumber = int(guessNumber)
            except:
                # if fail
                # throw error
                return self.generate_form_page(form, message["error"])

            # convert ok, make count plus one, everytime
            cherrypy.session["count"] += 1

            if guessNumber == answer:
                # clear session count and answer
                del cherrypy.session["count"]
                del cherrypy.session["answer"]
                # throw successful
                return self.generate_form_page(form,  message["successful"] + '</h1><a href="guessForm">play again</a>')
            elif guessNumber > answer:
                # throw small than guessNumber
                return self.generate_form_page(form, message["smaller"])
            else:
                # throw bigger than guessNumber
                return self.generate_form_page(form, message["bigger"])
    #@-others
#@+node:lee.20141215164031.86: ** def error_page_404
# handle page 404
def error_page_404(status, message, traceback, version):
    tmpl = env.get_template('404.html')
    return tmpl.render(title='404')

cherrypy.config.update({'error_page.404': error_page_404})
#@+node:lee.20141221203113.43: ** set root
root = Application()
#@+node:lee.20141221203113.44: ** application_conf
# set up app conf
application_conf = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': static_dir
    },
}
#@+node:lee.20141215164031.60: ** run env
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 在 openshift
    application = cherrypy.Application(root, config = application_conf)
else:
    # 在其他環境下執行
    cherrypy.quickstart(root, config = application_conf)
#@-others
#@-leo
