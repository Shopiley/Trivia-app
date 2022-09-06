import os
from selectors import SelectSelector
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
import random

# from models import setup_db, Question, Category
from models import *

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    """
    @TODO:  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app, resources={r'*/questions/*' : {'origins': '*'}})


    """
    @ Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_all_categories():
            categories = Category.query.all()

            if len(categories) == 0:
                abort(404)

            formatted_categories = {category.id:category.type for category in categories}

            return jsonify({
                'success': True,
                'categories' : formatted_categories
            })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def index():
        questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_questions(request, questions)

        categories = Category.query.all()
        formatted_categories = {category.id:category.type for category in categories}
        

        if len(paginated_questions) == 0 | (len(categories) == 0):
            abort(404)

        current_category = paginated_questions[0]['category']

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'current_category': current_category,
            'categories': formatted_categories
        })
  
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['GET', 'DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            print(question)

            if question is None:
                abort(404)
            
            else:
                if request.method == 'DELETE':
                    question.delete()
                    questions = Question.query.order_by(Question.id).all()
                    paginated_questions = paginate_questions(request, questions)

                    return jsonify(
                        {
                            'success': True,
                            'questions': paginated_questions
                        }
                    )
                
                else: 
                    return jsonify({
                        'success': True,
                        'question': question.format()
                    })

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", 1)
        category = body.get("category", 1)
        search_term = body.get("searchTerm", None)
  
        # try:
        if search_term:

            search_result = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(search_term))).all()

            paginated_questions = paginate_questions(request, search_result)

            if len(paginated_questions) == 0:
                abort(404)

            current_category = paginated_questions[0]['category']

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(search_result),
                'current_category': current_category,
            })

        else:
            new_question = Question(
                question = question,
                answer = answer,
                difficulty = difficulty,
                category = category
            )
            new_question.insert()

            return jsonify({
                'success': True
            })
          
        # except:
        #     abort(422)
        # return redirect(url_for('index'))

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions =  Question.query.filter(Question.category == category_id).all()
        paginated_questions = paginate_questions(request, questions)
        current_category = paginated_questions[0]['category']

        if len(paginated_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'current_category': current_category
        })


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_qiuz():
        body = request.get_json()

        quiz_category = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', None)
        
        category_id = quiz_category['id']

        if category_id == 0:
            questions_in_category = Question.query.all()

        else:
            questions_in_category = Question.query.filter(Question.category == category_id).all()
            
        selected_ids = [question.id for question in questions_in_category]
        print(selected_ids)
        random_id = random.choice([r_id for r_id in selected_ids if r_id not in previous_questions])
        random_question = Question.query.get(random_id)       

        return jsonify({
            'question': random_question.format()
        })

        
        

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

