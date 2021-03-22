from django.test import TestCase
from .models import Skill, JobPosition
from .controllers import JobPositionController

class JobPositionTestCase(TestCase):
    # def test_successful_torre_api_call(self):
    #     job_positions = JobPositionController()
    #     api_call = job_positions.torre_api_call()
    #     self.assertEqual(api_call.status_code, 200)
    
    # def test_correct_retrieve_of_data(self):
    #     job_positions = JobPositionController()
    #     torre_response = job_positions.torre_api_call()
    #     data_to_show = job_positions.get_job_posts_data(torre_response)
    #     self.assertEqual(len(data_to_show), 5)

    def test_correct_skill_load(self):
        controller = JobPositionController()
        job_position = JobPosition(title="Amazing Job Offer")
        job_position.save()
        controller.load_skill("Java", job_position)

        ajo = JobPosition.objects.get(title="Amazing Job Offer")
        print(ajo.skills.all())
        self.assertEqual(ajo.skills.first().name, "Java")
    
