#!/bin/bash
# test database initialization script
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql