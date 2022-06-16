from flask import Flask, render_template, redirect, request,flash
# from flask_debugtoolbar import DebugToolbarExtension
from flask import session, make_response
from surveys import surveys

app=Flask(__name__)

app.config['SECRET_KEY'] = 'hopper'
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# toolbar = DebugToolbarExtension(app)


survey_idx=0 
responses=[]
survey=(list(surveys.values()))[survey_idx]

@app.route('/')
def get_questions():
    """show surveys, allow user to select survey"""
    vals=list(surveys.values())
    length=len(vals)
    return render_template('start.html', surveys=surveys, length=length, values=vals)

@app.route('/start', methods=["POST"])
def first_question():
    """show first question of the selected survey"""
    session.clear()
    responses.clear()
    session['responses']=responses
    # start with an empty response list and clear sessions every time you start
    list_i=request.form["survey_list_num"]
    survey_idx=list_i
    print(f"Survey index is {survey_idx}")
    # survey_idx is printing correctly but isn't updating globally
    return redirect("/questions/0")

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Show question and choices"""
    if(len(responses)!=qid):
        flash(f"Cannot answer questions out of order!")
        # flash not appearing, but appears in sessions
        return redirect(f'/questions/{len(responses)}')
    question=survey.questions[qid].question
    choices=survey.questions[qid].choices
    return render_template('questions.html', question_num=qid, question=question, choices=choices, id=qid)
    
@app.route('/next', methods=['POST'])
def store_answer():
    """store the answer and redirect to next question"""
    try: 
        answer=request.form['answer']
            
    except: 
        flash("Please select an answer!")
        return redirect(f'/questions/{len(responses)}')  
   
    else:
        responses.append(answer)
        session['responses']=responses   
        qid=len(responses)
        print(responses)
        survey=(list(surveys.values()))[survey_idx]
        total_questions=survey.questions            
        if len(responses)<len(total_questions):
            return redirect(f"/questions/{qid}")
        else:
            return render_template('done.html')
      