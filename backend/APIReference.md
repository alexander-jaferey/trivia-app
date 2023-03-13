# Trivia API

## Introduction

The Trivia API is a RESTful API that allows users to interact with the trivia database, and serves endpoints used by the frontend of the UdaciTrivia application. The API is built around resource-oriented URLs. It accepts standard form-encoded request bodies and returns responses in JSON format, and uses standard HTTP methods and response codes.

<br>

___

## Getting Started

* Base URL: The application runs locally and can be accessed on the local machine at `http://127.0.0.1:5000`. Further instructions on setting up and running the backend application can be found in [the readme](../README.md#getting-started).
* Authentication/keys: The application does not require authentication in its current state.

<br>

___

## Error Handling

The API returns JSON objects with standard HTTP response codes for all requests. Unsuccessful requests will have a code in the `4xx` range. Errors are returned with the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

### Attributes

**success (boolean)**  
Indicates whether the request was successful  

**error (integer)**  
The HTTP response code triggered by the error  

**message (string)**  
A brief description of the error  

### Error Codes

| Code | Message | Description |
| ---- | ------- | ----------- |
| 400 | Bad Request | The request could not be processed (usually due to improper formatting) |
| 404 | Not Found | The requested resource could not be found |
| 405 | Method Not Allowed | The HTTP method used is not accepted by the requested endpoint |
| 422 | Unprocessable | The request was properly formatted, but could not be fulfilled due to semantic errors | 

<br>

__

## Endpoints

These are the endpoints available for interaction:

### GET /categories

Returns a list of categories and a success value.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/categories
```

#### **SAMPLE RESPONSE**
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET /questions

Returns a list of all questions in the database, along with a list of categories, the total number of questions, and a success value. Questions are paginated in groups of 10, and a page argument can be appended to the URL to specify a page number.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/questions
```

#### **SAMPLE RESPONSE**
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

### DELETE /questions/<question_id>

Deletes the question with given ID, if it exists. Returns the deleted question's ID and a success value.

#### **SAMPLE REQUEST**
```
curl -X DELETE http://127.0.0.1:5000/questions/25
```

#### **SAMPLE RESPONSE**
```
{
  "id": 25,
  "success": true
}
```

### POST /questions

This endpoint has two functions, depending on the request body. The first is to upload a new trivia question, and the second is to use a string to search existing trivia questions.

To upload a new question, the request should be sent with question, answer, category, and difficulty attributes. The API will return a success value.

#### **SAMPLE UPLOAD REQUEST**
```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the lightest noble gas?", "answer":"Helium", "category":1, "difficulty":2}'
```

#### **SAMPLE UPLOAD RESPONSE**
```
{
  "success": true
}
```

To search existing questions, the request should be sent with a search term. The API will return a paginated list of questions matching the (case-insensitive) search term, the total number of matching questions, and a success value.

#### **SAMPLE SEARCH REQUEST**
```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'
```

#### **SAMPLE SEARCH RESPONSE**
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### GET /categories/<category_id>/questions

Returns a paginated list of all questions with the given category ID, along with the total number of questions in the category, the category ID, and a success value. Questions are paginated in groups of 10, and a page argument can be appended to the URL to specify a page number.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/categories/2/questions
```

#### **SAMPLE RESPONSE**
```
{
  "current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### POST /quizzes

Returns a question to play the quiz game. Given a request including an optional category inside a form object and an optional list of previous question IDs, the API will return a single question, not in the list of previous questions, from the requested category (or from any category if none is specified), along with a success value.

#### **SAMPLE REQUEST**
```
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": null, "quiz_category": {"id": 2}}'
```

#### **SAMPLE RESPONSE**
```
{
  "question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  "success": true
}
```