# Code assessment for full-stack Python engineer

## Tasks

Please use **Python3**, **FastAPI** + **SQLAlchemy** + **Pytest** to complete the following tasks:
1. Create a SQLite database named `reviews` with tables `reviews`,`tags`,`review_tags`,`review_review_tag`. Please define and implement the relevant functionality using SQLAlchemy ORM model. At the end, please remember to commit SQLite files to the repository.
   1. `reviews`:
      1. id: integer type, primary key, auto-growth
      2. text: character type, maximum length is 2048 characters
      3. is_tagged: bool type
   2. `tags`:
      1. id: integer, primary key, auto-growing
      2. name: character type, max length is 50 characters
   3. `review_tag`:
      1. id: integer, primary key, auto-growth
      2. is_ai_tag: bool type, can't be null, default false
      3. tag_id: integer type, foreign key constraint for `tags` table
   4. `reveiw_review_tags`.
      1. id: integer, primary key, auto-growth
      2. review_id: integer, `review` table foreign key constraint
      3. review_tag_id: integer, foreign key constraint on `review_tag` table
2. Create a FastAPI application, compliant with the OpenAPI specification, with the following routes
   1. `POST /reviews/{review_id}/tags`: adds a `Tag` to the specified review, can add multiple ones
   2. `GET /reviews`: Returns a list of all reviews, requires paging support, and looks up the associated `Tag` information. This API can use multiple `Tag` table ids for conditional queries.
   3. `POST /tags`: Create a new `Tag`.
   4. `DELETE /tags/{tag_id}`: Delete the `Tag`, if deleted you need to delete the associated `review_tag`.
3. Write Pytest test cases to test the correctness of each route and the associations in the data table.

## Instruction
To start the code assessment, fork this repository and finish the code assessment in your own Github account.
Create a PR that including all of your tasks and leeting `Nicky` `Terry` to review it. Also leave a comment to the PR including the infos below, so that we could better recognize you and your CV. Leave a comment like this:
```
Name: Terry
Email: wh9112@gmail.com
Application channel: Linkedin/UpWork/Yodo1 official website
Position:
```

Thanks for your time~
