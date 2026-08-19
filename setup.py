from setuptools import setup,find_packages


HYPEN_E_DOT= "-e ."
def get_requirements(file_path):
    requirements = []
    with open(file_path) as file:
        lines=file.readlines()  ### Reading each line of requirements.txt
        requirements =[line.replace("\n","") for line in lines]  ## Saving result back to requirements
        if HYPEN_E_DOT in lines:
            lines.remove(HYPEN_E_DOT)

    return requirements     



setup(
    name = "Car Price Prediction",
    version = "0.0.1",
    author = "Muhammad Abdullah",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt")  # read from requirements.txt
)