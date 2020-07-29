import sys
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'matplotlib'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'seaborn'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'nltk'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'wordcloud'])

# process output with an API in the subprocess module:
reqs = subprocess.check_output([sys.executable, '-m', 'pip',
                                'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

print(installed_packages)

import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
