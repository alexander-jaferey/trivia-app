import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # initialize flask-CORS
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS'
        )
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # get categories
    @app.route('/categories')
    def get_categories():
        query = Category.query.order_by(Category.id).all()
        categories = {}
        # format categories in dict as {id: type}
        for i in query:
            categories[i.id] = i.type

        return jsonify({
            "success": True,
            "categories": categories
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
    # get questions
    @app.route('/questions')
    def get_questions():
        # set up pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        questions = Question.query.order_by(Question.id).all()
        query = Category.query.order_by(Category.id).all()

        categories = {}
        # format categories in dict as {id: type}
        for i in query:
            categories[i.id] = i.type

        # format and paginate questions
        formatted_questions = [question.format() for question in questions]
        paginated_questions = formatted_questions[start:end]

        # abort 404 if no questions in list
        if len(paginated_questions) == 0:
            abort(404)

        else:
            return jsonify({
                'success': True, 
                'questions': paginated_questions,
                'total_questions': len(formatted_questions), 
                'categories': categories,
                'current_category': None
            })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    # delete question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        # abort 404 if no question with given ID
        if question is None:
            abort(404)

        else:
            question.delete()
        
        return jsonify({
            'success': True,
            'id': question_id
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # search questions and submit new question
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        try:
            body = request.get_json()

            # abort 400 if request has no body
            if body is None:
                abort(400)
        except:
            abort(400)

        else:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)
            search_term = body.get('searchTerm', None)

            # clause for searching via this endpoint
            if search_term:
                # case-insensitive filtering for search term
                search_result = Question.query.order_by(Question.id).filter(Question.question.ilike(f"%{search_term}%"))
                
                # set up pagination
                page = request.args.get('page', 1, type=int)
                start = (page - 1) * QUESTIONS_PER_PAGE
                end = start + QUESTIONS_PER_PAGE
                
                # format and paginate questions
                formatted_questions = [question.format() for question in search_result]
                questions = formatted_questions[start:end]

                return jsonify({
                    'success': True, 
                    'questions': questions, 
                    'total_questions': len(formatted_questions), 
                    'current_category': None
                })

            # clause for posting new question
            # abort 422 if body is missing an attribute
            elif not (new_question and new_answer and new_category and new_difficulty):
                abort(422)

            else:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()
                
                return jsonify({
                    'success': True
                    })


    """
    @TODO: DONE
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # get questions by category
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # set up pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # get list of questions with given category id
        query = Question.query.order_by(Question.id).filter(Question.category == category_id)

        # format and paginate questions
        formatted_questions = [question.format() for question in query]
        
        # abort 404 if no questions in list
        if len(formatted_questions) == 0:
            abort(404)

        questions = formatted_questions[start:end]

        return jsonify({
            'success': True, 
            'questions': questions, 
            'total_questions': len(formatted_questions), 
            'current_category': category_id
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
    def send_quiz_questions():
        try:
            body = request.get_json()
            # abort 400 if request has no body
            if body is None:
                abort(400)
        except:
            abort(400)

        previous_ids = []
        category = body['quiz_category']['id']
        previous_questions = body['previous_questions']

        # get ids of previous questions (if any) to avoid resending them
        if previous_questions:
            for question in previous_questions:
                previous_ids.append(question)

        # get questions, filtering by category if given
        if category == 0:
            query = Question.query.all()
        else:
            query = Question.query.filter(Question.category == category).all()

        # set up list of formatted questions to work with
        query_questions = [question.format() for question in query]
        question_candidates = []

        # remove any questions in previous questions
        for question in query_questions:
            if question['id'] not in previous_ids:
                question_candidates.append(question)

        # set response question to none if all questions have been used
        if len(question_candidates) == 0:
            question_choice = None
        else:
            # select random question from list of candidates
            question_choice = random.choice(question_candidates)

        return jsonify({
            'success': True, 
            'question': question_choice
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return( 
            jsonify({
                'success': False,
                'error': 404, 
                'message': 'resource not found',
            }), 404
        )
    
    @app.errorhandler(422)
    def unprocessable(error):
        return(
            jsonify({
                'success': False, 
                'error': 422, 
                'message': 'unprocessable'
            }), 422
        )
    
    @app.errorhandler(400)
    def bad_request(error):
        return(
            jsonify({
                'success': False, 
                'error': 400, 
                'message': 'bad request'
            }), 400
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return(
            jsonify({
                'success': False, 
                'error': 405, 
                'message': 'method not allowed'
            }), 405
        )

    return app
