from services.repository import save_response

def save_assessment(project, assessment_type, responses):
    for r in responses:
        save_response(project, assessment_type, *r)
