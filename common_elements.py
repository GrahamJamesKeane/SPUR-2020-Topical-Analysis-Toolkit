import sqlite3
from datetime import datetime

primary_query_words = ['APPLIED COMPUTING', 'COMPUTER SYSTEMS ORGANISATION', 'COMPUTING METHODOLOGIES',
                       'GENERAL & REFERENCE', 'HARDWARE', 'HUMAN-CENTERED COMPUTING', 'INFORMATION SYSTEMS',
                       'MATHEMATICS OF COMPUTING', 'NETWORKS', 'SECURITY & PRIVACY', 'SOCIAL & PROFESSIONAL TOPICS',
                       'SOFTWARE & ITS ENGINEERING', 'THEORY OF COMPUTATION', 'UNCLASSIFIABLE']

secondary_query_words = ['ACCESSIBILITY', 'ARCHITECTURES', 'ARTIFICIAL INTELLIGENCE', 'ARTS & HUMANITIES',
                         'COLLABORATIVE & SOCIAL COMPUTING', 'COMMON', 'COMMUNICATION HARDWARE, INTERFACES & STORAGE',
                         'COMPUTATIONAL COMPLEXITY & CRYPTOGRAPHY', 'COMPUTER FORENSICS',
                         'COMPUTER GRAPHICS', 'COMPUTERS IN OTHER DOMAINS', 'COMPUTING / TECHNOLOGY POLICY',
                         'CONCURRENT COMPUTING METHODOLOGIES', 'CONTINUOUS MATHEMATICS',
                         'CROSS-COMPUTING TOOLS & TECHNIQUES', 'CRYPTOGRAPHY', 'DATA MANAGEMENT SYSTEMS',
                         'DATABASE & STORAGE SECURITY', 'DEPENDABLE & FAULT-TOLERANT SYSTEMS & NETWORKS',
                         'DESIGN & ANALYSIS OF ALGORITHMS', 'DISCRETE MATHEMATICS',
                         'DISTRIBUTED COMPUTING METHODOLOGIES', 'DOCUMENT MANAGEMENT & TEXT PROCESSING',
                         'DOCUMENT TYPES', 'EDUCATION', 'ELECTRONIC COMMERCE', 'ELECTRONIC DESIGN AUTOMATION',
                         'EMBEDDED & CYBER-PHYSICAL SYSTEMS', 'EMERGING TECHNOLOGIES', 'ENTERPRISE COMPUTING',
                         'FORMAL LANGUAGES & AUTOMATA THEORY', 'FORMAL METHODS & THEORY OF SECURITY', 'HARDWARE TEST',
                         'HARDWARE VALIDATION', 'HUMAN & SOCIETAL ASPECTS OF SECURITY & PRIVACY',
                         'HUMAN COMPUTER INTERACTION (HCI)', 'INFORMATION RETRIEVAL', 'INFORMATION STORAGE SYSTEMS',
                         'INFORMATION SYSTEMS APPLICATIONS', 'INFORMATION THEORY', 'INTEGRATED CIRCUITS',
                         'INTERACTION DESIGN',
                         'INTRUSION / ANOMALY DETECTION & MALWARE MITIGATION', 'LAW, SOCIAL & BEHAVIORAL SCIENCES',
                         'LIFE & MEDICAL SCIENCES', 'LOGIC', 'MACHINE LEARNING', 'MATHEMATICAL ANALYSIS',
                         'MATHEMATICAL SOFTWARE', 'MODELLING & SIMULATION', 'MODELS OF COMPUTATION',
                         'NETWORK ALGORITHMS', 'NETWORK ARCHITECTURES', 'NETWORK COMPONENTS',
                         'NETWORK PERFORMANCE EVALUATION', 'NETWORK PROPERTIES', 'NETWORK PROTOCOLS',
                         'NETWORK SECURITY', 'NETWORK SERVICES', 'NETWORK TYPES',
                         'OPERATIONS RESEARCH', 'PARALLEL COMPUTING METHODOLOGIES', 'PHYSICAL SCIENCES & ENGINEERING',
                         'POWER & ENERGY', 'PRINTED CIRCUIT BOARDS', 'PROBABILITY & STATISTICS', 'PROFESSIONAL TOPICS',
                         'RANDOMNESS, GEOMETRY & DISCRETE STRUCTURES', 'REAL-TIME SYSTEMS', 'ROBUSTNESS',
                         'SECURITY IN HARDWARE', 'SECURITY SERVICES', 'SEMANTICS & REASONING',
                         'SOFTWARE & APPLICATION SECURITY', 'SOFTWARE CREATION & MANAGEMENT',
                         'SOFTWARE NOTATIONS & TOOLS', 'SOFTWARE ORGANISATION & PROPERTIES',
                         'SYMBOLIC & ALGEBRAIC MANIPULATION', 'SYSTEMS SECURITY',
                         'THEORY & ALGORITHMS FOR APPLICATION DOMAINS', 'UBIQUITOUS & MOBILE COMPUTING',
                         'UNCLASSIFIABLE', 'USER CHARACTERISTICS', 'VERY LARGE SCALE INTEGRATION DESIGN',
                         'VISUALISATION', 'WORLD WIDE WEB']

excluded_words = ['&', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'able', 'about', 'achieved', 'administer',
                  'adv', 'against', 'aim', 'aims', 'all', 'allow', 'almost', 'also', 'an', 'and', 'any', 'any', 'apply',
                  'appreciate', 'approaches', 'appropriate', 'are', 'arise', 'around', 'as', 'aspects', 'assess',
                  'associated', 'at', 'attain', 'attention', 'based', 'based', 'basic', 'basis', 'be', 'before',
                  'begin', 'better', 'between', 'both', 'by', 'ca', 'can', 'carry', 'challenges', 'comes', 'completion',
                  'compt', 'concepts', 'course', 'covering', 'cs', 'csse', 'define', 'depend', 'describe', 'different',
                  'do', 'drawn', 'ds', 'e', 'each', 'each', 'equip', 'error', 'especially', 'evaluate', 'explain',
                  'exam',
                  'final', 'find', 'findings', 'firm', 'first', 'focuses', 'for', 'from', 'fyp', 'g', 'give', 'given',
                  'gives', 'goal', 'goals', 'grasp', 'has', 'have', 'having', 'help', 'higher', 'hon', 'how', 'i',
                  'identify', 'ii', 'iii', 'importance', 'important', 'in', 'include', 'includes', 'including',
                  'into', 'intro', 'introduce', 'introduces', 'introducing', 'introduction', 'involving', 'is',
                  'issues', 'it', 'its', 'know', 'knowledge', 'known', 'large', 'learn', 'lectures', 'level', 'lo1',
                  'lo1', 'lo2', 'lo3', 'lo4', 'lo5', 'lo6', 'lo7', 'lost', 'make', 'makes', 'may', 'meant', 'merits',
                  'might', 'module', 'more', 'most', 'multiple', 'near', 'necessary', 'need', 'never', 'new', 'no',
                  'none', 'objective', 'objectives', 'of', 'on', 'one', 'or', 'other', 'others', 'our', 'out',
                  'overcome', 'own', 'part', 'particular', 'paying', 'perform', 'persuasive', 'practical', 'previous',
                  'problems', 'prove', 'provide', 'provision', 'pure', 'related', 'relevance', 'relevant',
                  'requirements', 'sci', 'seen', 'seminars', 'sense', 'several', 'should', 'significantly', 'simple',
                  'single', 'small', 'so', 'solve', 'some', 'specific', 'starting', 'stopping', 'student', 'students',
                  'substantive', 'successful', 'such', 'suitable', 'syllabus', 'take', 'teach', 'terms', 'than', 'that',
                  'the', 'their', 'them', 'themselves', 'these', 'they', 'this', 'those', 'through', 'timely', 'to',
                  'together', 'topics', 'two', 'typed', 'types', 'ug', 'ui', 'understand', 'understanding', 'unseen',
                  'up', 'us', 'use', 'used', 'uses', 'using', 'ux', 'value', 'variety', 'various', 'view', 'was',
                  'ways', 'we', 'well', 'when', 'what', 'where', 'whether', 'which', 'while', 'wide', 'will', 'with',
                  'within',
                  'without', 'work', 'workshops', 'write', 'year']


# This is only used when adding new words to the excluded_words list:
# It alphabetically sorts the entries and transforms them to lowercase
def alphabetically_sort_text_lists(text_list):
    text_list.sort()
    for i in range(len(text_list)):
        text_list[i] = text_list[i].lower()
    print(list(text_list))


def open_sqlite():
    conn = sqlite3.connect('TEST_DB_SPUR.db')
    c = conn.cursor()
    return c


def output_to_png(fig, filename, location):
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output_files/{location}/{filename}_{stamp}.png"
    fig.savefig(file_name)


def output_to_csv(database, filename, location):
    stamp = str(datetime.today()).replace(":", ".")
    file_name = f"Output_files/{location}/{filename}_{stamp}.csv"
    database.to_csv(file_name)


def get_region_list():
    c = open_sqlite()
    region_list = []
    query = f"SELECT Country FROM Universities GROUP BY Country;"
    for row in c.execute(query):
        region_list.append(str(row[0]))
    c.close()
    return region_list


def get_course_list():
    c = open_sqlite()
    course_list = []
    query = f"SELECT CourseCode FROM CourseList ORDER BY CourseCode;"
    for row in c.execute(query):
        course_list.append(str(row[0]))
    c.close()
    return course_list


def get_uni_list(region):
    c = open_sqlite()
    uni_list = []
    query = f"SELECT UniversityName FROM Universities " \
            f"WHERE Country = '{region}' ORDER BY UniversityName;"
    for row in c.execute(query):
        uni_list.append(str(row[0]))
    c.close()
    return uni_list


# alphabetically_sort_text_lists(excluded_words)
