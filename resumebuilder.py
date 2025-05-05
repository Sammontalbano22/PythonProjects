import openai
import os
from fpdf import FPDF
from datetime import datetime

# Retrieve the OpenAI API key from the environment variable
openai.api_key = ''
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, 'Samuel Montalbano', align='C', ln=True)
        self.set_font('Arial', '', 8)
        self.cell(0, 5, 'Email: sam.montalbano@du.edu | LinkedIn: linkedin.com/in/samuel-montalbano/  ', align='C', ln=True)
        self.cell(0, 5, 'GitHub: https://github.com/Sammontalbano22', align='C', ln=True)
        self.ln(0)


    def section_title(self, title):
        self.set_font('Arial', 'B', 7)
        self.set_text_color(0, 102, 204)  # Blue color
        self.cell(0, 4, title.upper(), ln=True, border='B')
        self.set_text_color(0, 0, 0)  # Reset to black
        self.ln(1)

    def add_bullet_point(self, text):
        self.set_font('Arial', '', 7)
        self.cell(10)  # Indentation
        self.cell(5, 4, "·", align='C')  # Bullet point
        self.multi_cell(0, 4, text)
        self.ln(1)

    def add_text(self, text, bold=False):
        if bold:
            self.set_font('Arial', 'B', 7)
        else:
            self.set_font('Arial', '', 7)
        self.multi_cell(0, 3, text)
    def add_role_company_date(self, role, company, date):
        self.set_font('Arial', 'B', 7)
        self.cell(0, 6, f"{role}  {company}", ln=False)
        self.set_font('Arial', '', 7)
        self.cell(0, 6, date, align='R', ln=True)

def update_resume(requirements, resume_content):
    print("Updating resume with the following requirements:")
    print(requirements)
    print("Current resume content:")
    print(resume_content)

    # Use OpenAI API to update the resume content based on the requirements
    prompt = f"""You are a professional Software Engineering resume writer. Update the following resume content keeping it to one page in length to highlight how the candidate meets the following job requirements. Only reword what has been provided in the template resume and use all of its content. Make the resumes highly ATS compliant, so they pass screenings. Do not make stuff up that is not shown in the temmplate:

Job Requirements:
{requirements}

Resume Content:
{resume_content}

Updated Resume Content:s
Summary of Changes:"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Updated to the new model API
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7,
    )

    print("Response from OpenAI API:")
    print(response)

    # Extract the updated content and summary of changes from the response
    updated_content = response.choices[0].message.content.strip()
    updated_content_parts = updated_content.split("Summary of Changes:")
    updated_resume_content = updated_content_parts[0].strip()
    summary_of_changes = updated_content_parts[1].strip() if len(updated_content_parts) > 1 else "No changes provided."

    print("Updated resume content:")
    print(updated_resume_content)
    print("Summary of changes:")
    print(summary_of_changes)

    return updated_resume_content, summary_of_changes

def main():
    print("Resume Update Script")
    print("Enable chatbot feature? (yes/no):")
    use_chatbot = input().strip().lower() == "yes"

    # Existing resume content
    resume_content = """

# Education:
- University of Denver - Expected Graduation: June 2026
- Bachelor of Science in Computer Science and Bachelor of Science in Mathematics
- GPA: 3.59 | Major GPA: 3.8 | Dean's List: 2024
- Daniels Fund Scholar | Provost Scholar | Dean's List Recipient

# Technical Skills:
Programming Languages:
- Python(Primary), Java, Swift, MYSQL, HTML, CSS, JS
Tools & Technologies:
- Git, Visual Studio Code, JShell, GAIA GPS, MySQL Workbench, Firebase, Open AI API, Google APIs, MATLAB, Xcode, GPT Models, CO-PILOT


# Professional Experience:

Property Manager(Contracted)| Bachman and Associates (Jun 2024 - Sep 2024)
- Directed 30+ projects, managing $1000+ budgets and materials with 100% customer satisfaction.
- Streamlined construction processes using pre-project efficiency planning, improved completion time by 20%.
Aerospace Intern | Colorado Space Business Roundtable (Jun 2024 - Jul 2024)
- Gained insights into aerospace industry trends through expert-led workshops and events.
- Attended five workshops hosted by Aerospace Leaders; acquired actionable knowledge to enhance project efficiency including MATLAB for flight simulations.
Lead Website Administrator | Breezy Strategies (Jan 2023 - Jul 2024)
- Designed and managed 15+ school district websites for SCAP Colorado in partnership with the University of Colorado, Denver.
- Led statewide training for over 40 participants on website management and accessibility.
- Created the flagship SCAP website, securing a landing page for 20+ districts.
- Utilized CSS, JS, HTML to connect database to web applications.
Summer Assistant Manager | Grandote Peaks Golf Course (Jun 2023 - Sep 2023)
- Managed daily operations of the facility and helped supervise a team of 10 staff members, ensuring seamless experiences for over 100 golfers each day through enhanced service protocols.
- Analyzed sales data and golf trends to curate a targeted Pro Shop inventory, ultimately achieving a 10% increase in overall sales during the summer season for Grandote Peaks Golf Course.
- Planned and directed large-scale golf tournaments including the New Mexico Seniors League event with more than 90 participants; developed structured schedules and layouts to minimize wait times on course.
Trails Accessibility Technician | La Veta Trails (Jun 2022 - Sep 2022)
- Conducted terrain accessibility analysis, presenting findings to La Veta town board in a refined report.
- Improved mapping efficiency by 200% through GAIA GPS technology integration.

# Projects:
CollegePathwaysAI | Swift, Firebase, and Open AI (Oct 2024) 
- Manager and Developer of a Swift and MYSQL virtual college readiness app which uses trained OpenAI API integration for a AI driven Virtial Counselor.
Personal Portfolio Website | HTML, CSS, and JavaScript (Recurring)
- A Python-based resume builder that uses AI to modify a resume template based on job descriptions, saving users 50% more time when applying and increasing ATS screening success-rate by 10%.
Fire Percolation Simulation | Python (Mar 2023)
- Simulated fire spread in Python using DFS and BFS algorithms to predict fire spread by forest density.

# Hobbies:
- Golfing | Fishing | Rocket Design | Classic Literature | DIY Engineering Projects | Vinyl Collecting | Traveling
"""

    updated_resume_content = resume_content
    summary_of_changes = "No changes made."

    if use_chatbot:
        print("Please enter the key job requirements (press Enter twice to finish):")
        requirements = ""
        while True:
            line = input()
            if line:
                requirements += line + "\n"
            else:
                break

        updated_resume_content, summary_of_changes = update_resume(requirements, resume_content)

    today_date = datetime.today().strftime('%Y-%m-%d')
    file_name = f"Samuel-Montalbano-Resume-{today_date}.pdf"
    file_path = f"./{file_name}"

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    pdf.set_auto_page_break(auto=True, margin=10)

    lines = updated_resume_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            pdf.section_title(line[2:])
        elif line.startswith('- '):
            pdf.add_bullet_point(line[2:])
        elif '|' in line:
            parts = line.split('|')
            role_company = parts[0].strip()
            date = parts[1].strip()
            pdf.add_role_company_date(role_company, '', date)
        elif line.strip() in ["Programming Languages", "Programming Languages:", "Tools & Technologies", "Tools & Technologies:"]:
            pdf.add_text(line.strip(), bold=True)
        else:
            pdf.add_text(line.strip())

    pdf.output(file_path, 'F' )
    print(f"Updated resume saved to: {file_path}")
    print(f"Summary of changes: {summary_of_changes}")

if __name__ == "__main__":
    main()
