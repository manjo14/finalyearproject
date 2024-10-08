import os
import multiprocessing as mp
import spacy
from spacy.matcher import Matcher
import utils

class ResumeParser(object):

    def __init__(self, resume, skills_file=None, custom_regex=None):
        nlp = spacy.load('en_core_web_sm')
        custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'degree': None,
            'no_of_pages': None,
            'feedback': []
        }
        self.__resume = resume
        self._text_raw = utils.extract_text_with_pymupdf(self.__resume)
        self._text = ' '.join(self._text_raw.split())
        self._nlp = nlp(self._text)
        self._custom_nlp = custom_nlp(self._text_raw)
        self._noun_chunks = list(self._nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        cust_ent = utils.extract_entities_with_custom_model(self._custom_nlp)
        name = utils.extract_name(self._nlp, matcher=self.__matcher)
        email = utils.extract_email(self._text)
        mobile = utils.extract_mobile_number(self._text, self.__custom_regex)
        skills = utils.extract_skills(self._nlp, self._noun_chunks, self.__skills_file)
        
        # Extract degree
        degree = cust_ent.get('Degree', None)

        # Extract name
        self.__details['name'] = cust_ent.get('Name', [name])[0]

        # Fill details
        self.__details['email'] = email
        self.__details['mobile_number'] = mobile
        self.__details['skills'] = skills
        self.__details['no_of_pages'] = utils.get_number_of_pages(self.__resume)
        self.__details['degree'] = degree

        # Add feedback
        if not name:
            self.__details['feedback'].append('Name could not be extracted.')
        if not email:
            self.__details['feedback'].append('Email could not be extracted.')
        if not mobile:
            self.__details['feedback'].append('Mobile number could not be extracted.')
        if len(skills) < 5:
            self.__details['feedback'].append('Less than 5 skills extracted.')

def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    resumes = []
    for root, directories, filenames in os.walk('resumes'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [pool.apply_async(resume_result_wrapper, args=(x,)) for x in resumes]
    results = [p.get() for p in results]

    pool.close()
    pool.join()

    print(results)