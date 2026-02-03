import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from quiz.models import Category, Question, Option, QuestionPaper
from content.models import BlogPost, Vacancy, VideoSource, HeroSlide
from django.utils import timezone

# Clear existing data
Category.objects.all().delete()
BlogPost.objects.all().delete()
Vacancy.objects.all().delete()
VideoSource.objects.all().delete()
HeroSlide.objects.all().delete()
QuestionPaper.objects.all().delete()

cats_data = {
    'General Knowledge': [
        ('What is the capital of France?', 'Paris', ['London', 'Berlin', 'Madrid'], 'Paris is the largest city in France.'),
        ('Which is the largest planet?', 'Jupiter', ['Earth', 'Mars', 'Saturn'], 'Jupiter is a gas giant.'),
        ('What year did World War II end?', '1945', ['1918', '1939', '1950'], 'WWII ended in 1945.'),
        ('Who wrote "Romeo and Juliet"?', 'William Shakespeare', ['Charles Dickens', 'Mark Twain', 'Jane Austen'], 'Shakespeare wrote it in the late 16th century.'),
        ('What is the currency of Japan?', 'Yen', ['Won', 'Yuan', 'Dollar'], 'The Yen is the official currency of Japan.')
    ],
    'Science': [
        ('What is the chemical symbol for Water?', 'H2O', ['CO2', 'O2', 'H2'], 'Water consists of hydrogen and oxygen.'),
        ('What speed does light travel at?', '300,000 km/s', ['150,000 km/s', '1,000,000 km/s', '500,000 km/s'], 'Light travels at approximately 300,000 kilometers per second.'),
        ('What is the power house of the cell?', 'Mitochondria', ['Nucleus', 'Ribosome', 'Golgi body'], 'Mitochondria generate most of the cell\'s energy.'),
        ('Who developed the theory of relativity?', 'Albert Einstein', ['Isaac Newton', 'Galileo', 'Nicola Tesla'], 'Einstein published it in the early 20th century.'),
        ('What is the hardest natural substance?', 'Diamond', ['Gold', 'Iron', 'Quartz'], 'Diamond is made of pure carbon.')
    ],
    'History': [
        ('Who was the first man to walk on the moon?', 'Neil Armstrong', ['Buzz Aldrin', 'Yuri Gagarin', 'Michael Collins'], 'Armstrong walked on the moon in 1969.'),
        ('In which year did Nepal become a Republic?', '2008', ['2001', '2006', '2015'], 'Nepal was declared a republic on May 28, 2008.'),
        ('Who was the first woman Prime Minister of the UK?', 'Margaret Thatcher', ['Theresa May', 'Angela Merkel', 'Indira Gandhi'], 'Thatcher served from 1979 to 1990.'),
        ('The Great Wall of China was built to protect against?', 'Mongols', ['Romans', 'Greeks', 'Persians'], 'It was built for defense against northern invasions.'),
        ('Who discovered America?', 'Christopher Columbus', ['Vasco da Gama', 'James Cook', 'Marco Polo'], 'Columbus reached the Americas in 1492.')
    ],
    'Technology': [
        ('What does CPU stand for?', 'Central Processing Unit', ['Core Processing Unit', 'Central Power Unit', 'Computer Processing Unit'], 'The CPU is the brain of the computer.'),
        ('Who is known as the father of Computers?', 'Charles Babbage', ['Alan Turing', 'Bill Gates', 'Steve Jobs'], 'Babbage designed the first mechanical computer.'),
        ('What year was the first iPhone released?', '2007', ['2005', '2008', '2010'], 'Steve Jobs introduced the iPhone in 2007.'),
        ('What does WWW stand for?', 'World Wide Web', ['World Wide Wave', 'Web Wide World', 'World Web Wide'], 'The WWW was invented by Tim Berners-Lee.'),
        ('Which company owns Android?', 'Google', ['Apple', 'Microsoft', 'Samsung'], 'Google acquired Android Inc. in 2005.')
    ],
    'Administration': [
        ('What is the full form of HRM?', 'Human Resource Management', ['Head Resource Manager', 'Human Right Mission', 'Head Rule Method'], 'HRM stands for Human Resource Management.'),
        ('Which style of leadership involves team participation?', 'Democratic', ['Autocratic', 'Laissez-faire', 'Paternalistic'], 'Democratic leadership involves group decision making.')
    ],
    'Engineering': [
        ('What is the unit of Force?', 'Newton', ['Watt', 'Joule', 'Pascal'], 'Force is measured in Newtons.'),
        ('Which material has high electrical conductivity?', 'Copper', ['Glass', 'Rubber', 'Wood'], 'Copper is a great conductor of electricity.')
    ],
    'Medical': [
        ('What is the normal body temperature of a human?', '98.6°F', ['95.4°F', '100.2°F', '97.8°F'], 'Standard human body temperature is 98.6 degrees Fahrenheit.'),
        ('Which organ filters blood?', 'Kidney', ['Heart', 'Lungs', 'Liver'], 'The kidneys filter blood and produce urine.')
    ]
}

for cat_name, questions in cats_data.items():
    cat = Category.objects.create(name=cat_name, description=f'Detailed questions about {cat_name}')
    for q_text, correct, others, expl in questions:
        q = Question.objects.create(category=cat, text=q_text, explanation=expl)
        Option.objects.create(question=q, text=correct, is_correct=True)
        for other in others:
            Option.objects.create(question=q, text=other, is_correct=False)

# Add Blogs
for i in range(5):
    BlogPost.objects.create(
        title=f'Mastering {list(cats_data.keys())[i%4]}: A Guide {i+1}',
        content=f'<p>This is a detailed guide on how to master {list(cats_data.keys())[i%4]}. Learning is essential for growth and success in any field.</p>',
        author='Expert Team'
    )

# Add Vacancies
for i in range(6):
    Vacancy.objects.create(
        title=f'Full Stack Developer (Level {i+1})',
        company='NepalAI Labs',
        description=f'Seeking a skilled developer to join our growing team. Experience in Django and Next.js is a plus.',
        deadline=timezone.now() + timezone.timedelta(days=15 + i),
        link='https://example.com/apply'
    )

# Add Videos
for i in range(6):
    VideoSource.objects.create(
        title=f'Mastering {list(cats_data.keys())[i%4]} (Part {i+1})',
        description=f'In-depth tutorial on {list(cats_data.keys())[i%4]}. Part {i+1} covers advanced concepts.',
        youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    )

# Add Hero Slides
HeroSlide.objects.create(
    title='Focus on Your Goals',
    quote='"The secret of getting ahead is getting started." – Mark Twain',
    order=1
)
HeroSlide.objects.create(
    title='Reach New Heights',
    quote='"Success is not final; failure is not fatal: it is the courage to continue that counts." – Winston Churchill',
    order=2
)
HeroSlide.objects.create(
    title='Master the Matrix',
    quote='"The beautiful thing about learning is that no one can take it away from you." – B.B. King',
    order=3
)

# Add Sample Question Papers
eng_cat = Category.objects.get(name='Engineering')
med_cat = Category.objects.get(name='Medical')
admin_cat = Category.objects.get(name='Administration')

QuestionPaper.objects.create(
    title='Civil Engineering 2080 - Loksewa Paper',
    category=eng_cat,
    description='Full retrospective of the 2080 Civil Engineering public service commission exam.',
    file='question_papers/civil_2080.pdf'
)
QuestionPaper.objects.create(
    title='Medical Officer Screening 2079',
    category=med_cat,
    description='Past paper for medical officer entrance exams.',
    file='https://images.unsplash.com/photo-1576091160550-217359f42f8c?auto=format&fit=crop&q=80&w=1000'
)
QuestionPaper.objects.create(
    title='Administrative Officer Mock Paper',
    category=admin_cat,
    description='Updated mock paper for administrative section officer exam.',
    file='question_papers/admin_mock.pdf'
)

print("Successfully seeded extensive data including papers.")
