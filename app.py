from flask import Flask, request, Response, render_template, jsonify, json, redirect
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Regexp
import re

class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators= [
        Regexp(r'(^[a-z]+$)|^$', message="must contain letters only")
    ])
    submit = SubmitField("Go")

webkey = "adf108c0-1345-4493-8857-c59b57237d24"
csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"

csrf.init_app(app)
if __name__ == '__main__':
    app.run(debug=True)
    # This is debug run code
    # delete when done

@app.route('/') #index
@app.route('/home')
def index():
    form = WordForm()
    return render_template("index.html", form=form)


@app.route('/words', methods=['POST','GET'])
def letters_2_words():
    

        length = 0
        length = int(request.form.get('length'))

        pattern = str(request.form.get('pattern'))
        print("pattern: ", pattern , " Length: ", len(pattern))

        print ("length is: ", length) #delete
        form = WordForm()

        if form.validate_on_submit():
            letters = form.avail_letters.data
        else:
            return render_template("index.html", form=form)

        with open('sowpods.txt') as f:
            good_words = set(x.strip().lower() for x in f.readlines())

        word_set = set()
        print("String length:")
        print(len(letters))

        if (len(letters) == 0 and pattern == ""):
            #add some indication as to what is happening
            return  render_template("index.html", form=form)
        else:
            if(len(letters)== 0):
                if (length != 0):
                    for w in good_words:
                        if(len(w) == length):
                            if(len(pattern)>0):
                                regW = re.findall(pattern,w)
                                if(len(regW)!=0):
                                    word_set.add(w)
                            else:
                                word_set.add(w)
                
                else:
                    for w in good_words:
                        if(len(pattern) > 0):
                            regW = re.findall(pattern,w)
                            if(len(regW)!=0):
                                word_set.add(w)
                        else:
                            word_set.add(w)

            else:
                if (length != 0):
                    for l in range(3,len(letters)+1):
                        for word in itertools.permutations(letters,l):
                            w = "".join(word)
                            if w in good_words and len(w) == length:
                                if (len(pattern)>0):
                                    regW= re.findall(pattern,w)
                                    print(regW)
                                    if (len(regW) != 0):
                                        word_set.add(w)
                                else:
                                    word_set.add(w)

                else:
                    for l in range(3,len(letters)+1):
                        for word in itertools.permutations(letters,l):
                            w = "".join(word)
                            if w in good_words:
                                if (len(pattern)>0):
                                    regW= re.findall(pattern, w)
                                    print(regW)
                                    if (len(regW) != 0):
                                        word_set.add(w)
                                else:
                                    word_set.add(w)  
            return render_template('wordlist.html',
                    wordlist=sorted(sorted(word_set), key=len),
                    name="Nathen Slater")



@app.route('/Response/<string:w>', methods=['GET', 'POST'])
def Response( w):
    #w = str(request.form.get("myModal"))
    w = str(w)
    #print("the word list is: ", wordlist)
    print("the sent word is: ", w)
    response = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/"+ w +"?key="+webkey)
    item = response.json()
    print(item)
    if(len(item)>0):
        text = json.dumps(item[0], sort_keys=True, indent=4)
        data = json.loads(str(text))
        definition = data['def'][0]['sseq'][0][0][1]['dt'][0][1]
        definition = definition[4:]
        print(definition)
    else:
        print("Word not found")

    return render_template('wordlist.html', defin = definition)







#if satement when nothing is entered
   

##############################################

#onclick function look for the word
#display in grids "good pratice"

@app.route('/proxy')
def proxy(w):
    #w = cat
    print(w)
    result = requests.get(request.args["https://www.dictionaryapi.com/api/v3/references/collegiate/json/"+ w +"?key="+webkey])
    resp = Response(result.text)
    resp.headers['Content-Type'] = 'application/json'
    print (resp)
    return resp



@app.route("/about")
def about():
    return render_template('about.html')