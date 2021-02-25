from django.test import TestCase
import random
import string

def star_replace(input_value):

    encrypted_value = random.choice(string.ascii_lowercase)
    for x in input_value:
        encrypted_value += x.replace(x, '*')

    return encrypted_value

