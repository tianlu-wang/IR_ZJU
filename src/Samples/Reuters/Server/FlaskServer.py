# -*- coding: utf-8 -*-
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from Samples.Reuters.Reuters import ReutersData

# create our little application :)
app = Flask(__name__)
# app.debug = True

@app.route('/', methods=['GET'])
def search_home():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def do_search():
    query = request.form['query']
    action = request.form['submit']
    entries = []
    print(type(query), query, action)
    spell = Reuters.CheckSpell(query)
    print("Spell: ", spell)
    if action == 'query':
        print('Do query...')
        for docId, score in Reuters.ScoredQuery(query, 20):
            entries.append(Reuters.documentMap[docId])
        print('Done')
    elif action == 'boolean':
        print('Do boolean query...')
        for docId, score in Reuters.BooleanQuery(query):
            entries.append(Reuters.documentMap[docId])
        print('Done')
    elif action == 'phrase':
        print('Do phrase query...')
        for docId, score in Reuters.PhraseQuery(query, 20):
            entries.append(Reuters.documentMap[docId])
        print('Done')
    elif action == 'similar':
        print('Do similar query...')
        for docId, score in Reuters.SimilarQuery(query, 20):
            entries.append(Reuters.documentMap[docId])
        query = Reuters.queryStr
        print('Done')

    return render_template('show_entries.html', entries=entries, query=query, spell=spell, showSpell=len(spell)>0)

def run(reuters: ReutersData):
    global Reuters
    Reuters = reuters
    app.run(host='0.0.0.0')
