import re 
from fastapi import HTTPException

def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise HTTPException(400, "password must include at least a number")


def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise HTTPException(400, "password must include at least a letter")


def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise HTTPException(400, "password must include at least a special character")


def min_length_validator(password):
    if len(password) < 8:
        raise HTTPException(400, "password length must be at least 8")

def simple_email_validator(email: str):

    if email.find("@") == -1:
        raise HTTPException(400, "Please enter a valid email address!")

    user_part, domain_part = email.split("@")

    if domain_part.find(".com") == -1:
        raise HTTPException(400, "Email address should end with .com")
