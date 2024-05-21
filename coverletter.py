# Warning control
import warnings
warnings.filterwarnings('ignore')
import os

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'


from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

def write_cover_letter(company_name ='Rokt', 
                       industry='web design', 
                       position='Front-End Engineer', 
                       job_posting_url='https://au.talent.com/view?id=fb77f0ae8520', 
                       applicant_name='Corgi Tang'):
    searcher_agent = Agent(
        role="searcher",
        goal="Identify actual role descriptions that  "
            "help {applicant_name}, write a cover letter and find a job",
        backstory=(
            "I am scouring the "
            "the digital landscape for role descriptions and recent news to help {applicant_name} look for a job. "
            "I am also scouring the digital landscape to find role descriptions so {applicant_name} knows what he applying for"
            "Armed with cutting-edge tools, you analyze data, to help {applicant_name} get a job. "
            "{applicant_name} is a brilliant consultant"
            "and successfully delivered successful outcomes to key projects"
        ),
        allow_delegation=False,
        verbose=True
    )

    researcher_agent = Agent(
        role="researcher",
        goal="Make sure to do amazing analysis on "
            "job posting to help job applicants",
        tools = [scrape_tool, search_tool],
        backstory=(
            "As a Job Researcher, your prowess in "
            "navigating and extracting critical "
            "information from job postings is unmatched."
            "Your skills help pinpoint the necessary "
            "qualifications and skills sought "
            "by employers, forming the foundation for "
            "effective application tailoring."
        ),
        allow_delegation=False,
        verbose=True
    )

    applicant_agent = Agent(
        role="applicant",
        goal="Get a job for myself. I need to write a customised cover letter directed to the CEO or recruitment manager of a company, to look for work",
        backstory=(

            "I need to persuade a CEO or recruitment manager "
            "why I am the best person for the job and"
            "would be an amazing asset for the company. "
            "I need to be very persuasive. And the letter I write must be completely personalised and witty."
            "I am a brilliant consultant with proven experience in consultancy"
            "and successfully delivered successful outcomes to key projects"
        ),
        allow_delegation=False,
        verbose=True
    )

    searcher_task = Task(
        description=(
            "Conduct an in-depth analysis of the company {company_name}, "
            "a company in the {industry} sector "
            "that recently showed interest in company. "
            "Utilize all available data sources "
            "to compile a detailed profile, "
            "focusing on recent business developments"
            "Also use data-sources that is about specific data science or AI roles of the company"
            "eg linkedin jobs or from their internal job availability sites. "
            "Find specific technologies use in the data science or AI roles, so that you can quote them in a e-mail"
            "Also refer to local Australian news about the company and what they did in Australia. "
            "You must firstly use the serper tool, and then scrape all the websites from the link of serper. "
            "Scrape websites to get all this information if necessary. "
            "This task is crucial for tailoring "
            "our strategy to get {applicant_name} a job.\n"
            "Don't make assumptions and "
            "only use information you absolutely sure about."
        ),
        expected_output=(
            "A comprehensive report on the company {company_name}, "
            "including recent news, recent milestones. "
            "The report must have SPECIFIC Australian news about the company and what they did in Australia. "
            "The report must name the specific role name which is {position} and include specific programming languages. "
            "Highlight potential areas where {applicant_name} can potentially proven great business value in the role, "
            "and suggest ways he can fit in to their vision. "
            "Also highlight the name of the actual role, the specific technologies or technology stack needed for {applicant_name} to work on"
            "You must firstly use the serper tool, and then scrape all the websites from all the links of serper."
        ),
        tools=[search_tool, scrape_tool],
        agent=searcher_agent,
    )

    # Task for Researcher Agent: Extract Job Requirements
    research_task = Task(
        description=(
            "Analyze the job posting URL provided ({job_posting_url}) "
            "to extract key skills, experiences, and qualifications "
            "required. The role name is {position}. Use the tools to gather content and identify "
            "and categorize the requirements."
        ),
        expected_output=(
            "A structured list of job requirements, including necessary "
            "skills, qualifications, and experiences."
        ),
        agent=researcher_agent,
        tools=[scrape_tool]

    )

    application_task = Task(
        description=(
            "Using the insights gathered from "
            "the searcher report on {company_name} and the structured list of job requirements listed in {job_posting_url} "
            "craft a personalized cover letter "
            "for the recruitment manager at {company_name}, "
            "for the {position} to get me a job. "
            "The campaign must address actual recent news of their company"
            "or address actual data science projects, AI projects and actual AI-related initiatives by their organisation"
            "and how I can support their goals and help them get great success. "
            "The campaign must address their ACTUAL social and sustainability initiatives because believes the greater society good"
            "Your communication must resonate "
            "with {company_name}'s company culture and values, "
            "demonstrating a deep understanding of "
            "their business and needs.\n"
            "Based on the roles provided in the lead providing task, name the key technologies and tech stack that {applicant_name} definitely knows about, and say {applicant_name} is very experienced in it. "
            "This should be based on the structured list of job requirements produced from {job_posting_url}. "
            "Also highlight the name of the actual role, the specific programming languages or specific technologies or technology stack needed for {applicant_name} to work on. "
            "Don't make assumptions and only "
            "use information you absolutely sure about."
            "Scrape websites to get all this information if necessary. "
            "The letter is assumed to be written by me, and MUST end with Kind regards, {applicant_name}"
        ),
        expected_output=(
            "A series of personalized email drafts "
            "tailored to {company_name}, "
            "specifically targeting their recruitment manager in order to persuade them that {applicant_name} should be given a job in the company as a {position}."
            "Each draft should include "
            "a compelling narrative that connects why I"
            "should be given a job in the company. "
            "the name of the role in the company is {position} and the cover letter must include this."
            "The email must address their ACTUAL social and sustainability initiatives because {applicant_name} believes the greater society good. Be very specific about this. "
            "The email must also address the ACTUAL and SPECIFIC recent AUSTRALIAN news about the company that has been published."
            "Also highlight the name of the actual role, the specific programming languages, the specific technologies or technology stack needed for {applicant_name} to work on. "
            "The email must address actual data science projects, AI projects and actual AI-related initiatives by their organisation. "
            "Scrape websites to get all this information if necessary. "
            "Ensure the tone is engaging, professional, "
            "and is written for {applicant_name}. The letter MUST end with Kind regards, {applicant_name}. The email is to be assumed to be written by him, NOT a member of the crew. "
            "{applicant_name} is me, refer to {applicant_name} as I"
            "The email must also end with a funny joke about the company, role, in the P.S. section, make sure it is relevant"
        ),
        tools=[search_tool],
        agent=applicant_agent,
    )

    crew = Crew(
        agents=[searcher_agent, researcher_agent,
                applicant_agent],
        tasks=[searcher_task, research_task,
            application_task],
        verbose=2,
        memory=True

    )

    inputs = {
        "company_name": company_name,
        "industry": industry,
        "position": position,
        "job_posting_url" : job_posting_url,
        "applicant_name": applicant_name

    }
    result = crew.kickoff(inputs=inputs)
    return result

if __name__ == "__main__":
    result = write_cover_letter()
    print('FINAL RESULTS')
    print('-------------')
    print(result)
