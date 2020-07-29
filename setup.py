# Install required packages and update:
def get_packages():
    import sys
    import subprocess
    import pkg_resources
    from subprocess import call

    # Update existing packages:
    packages = [dist.project_name for dist in pkg_resources.working_set]
    call("pip install --upgrade " + ' '.join(packages), shell=True)

    # implement pip as a subprocess to install the following packages:
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


# Install required libraries:
def get_libs():
    import nltk
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
