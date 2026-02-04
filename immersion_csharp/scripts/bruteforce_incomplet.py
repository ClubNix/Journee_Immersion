import subprocess

def generatePasswords():
    """write your password generator and call testPass to check if the password is good"""

def testPass(password: str) -> bool:
    test = subprocess.check_output("./Immersion " + password, shell=True).decode().strip()
    return test != "Haha vous n'aurez pas le mot de passe!!!"

if __name__ == "__main__":
    generatePasswords()