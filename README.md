## Trivia App API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable


### Endpoints 
#### GET /categories
- General:
    - Returns a categories object and success value
- Sample: `curl http://127.0.0.1:5000/categories`

```{
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

#### GET /questions
- General:
    - Returns a categories object, current category, a list of question objects, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

```{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": 5,
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
    "total_questions": 21
}
```


#### POST /questions
- General:
    - Creates a new question using the submitted question, answer text category, and difficulty score
    -Returns a success value 
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question": "What is the highest mountain in Africa","answer": "Everest", "difficulty": 2, "category": 3 }'`

- On windows, store the json object in a json.txt file and run the curl command in command prompt like this:
`curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d @json.txt`
```
{
    "success": true
}
```

#### POST /questions
- General (Search):
    - Get questions based on a search term
    - Returns a success value, total_questions, the current_category and a list of any questions for whom the search term is a substring of the question.
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"searchTerm": "country"}'`

```
{
    "current_category": 6,
    "questions": [
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

- On windows, store the json object in a json.txt file and run the curl command in command prompt like this:
`curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d @json.txt`

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns a success value and question list based on current page number to update the frontend. 
- Sample `curl -X DELETE http://127.0.0.1:5000/question/16`

```{
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
    "success": true
} 
```

#### GET /categories/{category_id}/questions
- General:
    - Returns the current category, a list of question objects, success value, and total number of questions based on category (the category_id specified as a query parameter)
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`

```
{
    "current_category": 3,
    "questions": [
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
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Everest",
            "category": 3,
            "difficulty": 2,
            "id": 28,
            "question": "What is the highest mountain in Africa"
        }
    ],
    "success": true,
    "total_questions": 4
}
```

#### POST /quizzes
- General:
    - Takes in category and previous question JSON request data and returns (5)questions in random order, one by one within the given category, if provided, and that is not one of the previous questions.
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"quiz_category": {"type": "Art", "id": "2"}, "previous_questions":[18]}'`

```
{
    "question": {
        "answer": "Escher",
        "category": 2,
        "difficulty": 1,
        "id": 27,
        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    }
}
```
