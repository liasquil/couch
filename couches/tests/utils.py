from ..models import Couch

def create_couch(host, capacity, smoking_possibility=''):
    return Couch.objects.create(host=host, capacity=capacity, smoking_possibility=smoking_possibility)