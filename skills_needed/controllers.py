import requests
from .models import JobPosition, Skill

class JobPositionController:
    def torre_api_call(self):
        url = "https://search.torre.co/opportunities/_search?currency=USD%24&page=0&periodicity=hourly&lang=en&size=20&aggregate=false&offset=0"
        payload="{\n\"and\":[\n{\n\"type\": {\n\"code\": \"internships\"\n}\n},\n{\n\"skill/role\": {\n\"text\": \"software\",\n\"experience\": \"potential-to-develop\"\n}\n}\n]\n}"
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response
    
    def get_job_posts_data(self, torre_response):
        json = torre_response.json()
        results = json['results'][:5]
        job_posts_data = []
        for r in results:
            data = {}
            data['title'] = r['objective'] if r['objective'] else 'No Title'
            data['company_name'] = r['organizations'][0]['name'] if r['organizations'] else 'No Company'
            if r['compensation']:
                compensation = r['compensation']['data']
                data['compensation'] = compensation['currency'] + ' ' + str(compensation['maxAmount']) + ' ' + compensation['periodicity']
            else:
                data['compensation'] = '$0'
            skills = []
            if r['skills']:
                for skill in r['skills']:
                    skills.append(skill['name'])
            data['skills'] = skills
            job_posts_data.append(data)
        return job_posts_data

    def load_skill(self, name, instance):
        skill = None
        try:
            skill = Skill.objects.get(name=name)
        except:
            print("Not Found")
        if skill is None:
            skill = Skill(name=name)
            skill.save()
            instance.skills.add(skill)
        else:
            instance.skills.add(skill)

    def exists_on_db(self, title):
        jp = None
        try:
            jp = JobPosition.objects.get(title=title)
        except:
            print("Not Found")
        if jp is not None:
            return True
        else:
            return False
        
    
    def load_data_to_db(self, job_posts_data):
        for jp in job_posts_data:
            title = jp['title']
            company_name = jp['company_name']
            compensation = jp['compensation']
            skills = jp['skills']
            exists_on_db = self.exists_on_db(title)
            if not exists_on_db:
                job_position = JobPosition(
                    title=title,
                    company_name=company_name,
                    compensation=compensation
                )
                job_position.save()
                for s in skills:
                    self.load_skill(s, job_position)
    
    def run(self):
        torre_response = self.torre_api_call()
        job_posts_data = self.get_job_posts_data(torre_response)
        self.load_data_to_db(job_posts_data)
    
