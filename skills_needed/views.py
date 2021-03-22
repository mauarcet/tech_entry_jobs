from django.http import HttpResponse
from django.template import loader


from .models import Skill, JobPosition
from .controllers import JobPositionController


def index(request):
    controller = JobPositionController()
    controller.run()
    job_positions = JobPosition.objects.order_by('created_at')[:5]
    skills = job_positions[0].skills.all()
    template = loader.get_template('skills_needed/index.html')

    context = {}
    data = {}
    for iterator, jp in enumerate(job_positions):
        skills = jp.skills.all()
        skills_data = []
        resource_data = []
        for skill in skills:
            skills_data.append(skill.name)
            resource_data.append(skill.resource)
        data[iterator] = {
            'title' : jp.title,
            'company_name' : jp.company_name,
            'compensation' : jp.compensation,
            'skills': skills_data,
            'resources': resource_data
        }
    context['job_positions'] = data
    return HttpResponse(template.render(context, request))