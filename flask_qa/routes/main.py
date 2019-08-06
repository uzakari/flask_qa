import requests
from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from flask_qa.extentions import db
from flask_login import current_user, login_required, logout_user
from flask_qa.models import Question, User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    questions = Question.query.filter(Question.answer != None).all()
    context = {
        'questions': questions
    }
    return render_template('home.html', **context)


@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form['question']
        expert = request.form['expert']

        question = Question(
            question=question,
            expert_id=expert,
            asked_by_id=current_user.id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    experts = User.query.filter_by(expert=True).all()
    context = {
        'experts': experts
    }
    return render_template('ask.html', **context)


@main.route('/questions/<int:question_id>')
def questions(question_id):
    question = Question.query.get_or_404(question_id)
    context = {'question': question}
    return render_template('questions.html', **context)


@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
def answer(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()
        return redirect(url_for('main.unanswered'))
    context = {
        'question': question
    }
    return render_template('answer.html', **context)


@main.route('/users')
def users():
    users = User.query.filter_by(admin=False).all()
    context = {'user': users}
    return render_template('users.html', **context)


@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    user = User.query.get_or_404(user_id)
    if user.expert:
        user.expert = False
        db.session.commit()
    else:
        user.expert = True
        db.session.commit()
    return redirect(url_for('main.users'))


@main.route('/unanswered')
@login_required
def unanswered():
    unanswered_questions = Question.query.filter_by(
        expert_id=current_user.id).filter(Question.answer == None).all()
    context = {'unanswered_questions': unanswered_questions}
    return render_template('unanswered.html', **context)


@main.route('/youtube')
def youtube():

    youtube_url = 'https://community-zippopotamus.p.rapidapi.com/us/90210'
    headers = {
        "x-rapidapi-host": "community-zippopotamus.p.rapidapi.com",
        "x-rapidapi-key": "65d7ed5b59msh0e43209e44187a9p1e958ejsn6e3fd388568f"
    }
    serach_prams = {
        "q": "trump"
    }
    r = requests.get(youtube_url, headers=headers)
    print(r.json()["country"])

    def test():
        return True
    return render_template('youtubevideos.html')


@main.route('/api')
def api():
    return jsonify({'result': 'I am working well'})


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
