import json
import os
import requests
#temp list of packages
url = 'https://eyescary-development.github.io/CDN/agpm_packages/packagelist.json'
def fetchlist():
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def checkpackagelist(item):
    response = requests.get(url)
    response.raise_for_status()
    pkglist = fetchlist()
    try:
        temp=pkglist[item]
        return True
    except Exception:
        return False

def lookup(item):
    metadata=fetchlist()
    print("package name: " + str(item))
    print("description: " + str(metadata[item]["description"]))
    print("latest release notes: " + str(metadata[item]["releaseNotes"]))

def install(item):
    os.system("curl -O https://eyescary-development.github.io/CDN/agpm_packages/"+item+"/protocols/install.sh && bash install.sh && rm install.sh")
    path=os.path.join(os.path.expanduser('~'), '.agpm', 'localmetadata.json')
    try:
      with open(path, 'r') as f:
        localmetadata = json.load(f)
    except Exception:
      with open(path, 'w') as f:
          f.write("{}")
      localmetadata = {}
    cloudmetadata=fetchlist()
    localmetadata[item]=cloudmetadata[item]
    with open(path, 'w') as f:
        json.dump(localmetadata, f, indent=2)

def uninstall(item):
    os.system("curl -O https://eyescary-development.github.io/CDN/agpm_packages/"+item+"/protocols/uninstall.sh && bash uninstall.sh && rm uninstall.sh")
    file_path=os.path.join(os.path.expanduser('~'), '.agpm', 'localmetadata.json')
    with open(file_path, 'r') as f:
        localmetadata=json.load(f)
    localmetadata.pop(item, None)
    with open(file_path, 'w') as f:
        json.dump(localmetadata, f, indent=2)

def update(item):
    metadata=fetchlist()
    cloudver = metadata[item]["version"]
    file_path = os.path.join(os.path.expanduser('~'), '.agpm', 'localmetadata.json')
    with open(file_path, 'r') as f:
        localmetadata = json.load(f)
    localver = localmetadata[item]["version"]
    if localver != cloudver:
        os.system("curl -O https://eyescary-development.github.io/CDN/agpm_packages/"+item+"/protocols/update.sh && bash update.sh && rm update.sh")
        localmetadata[item]=cloudmetadata[item]
        with open(file_path, 'w') as f:
            json.dump(localmetadata, f, indent=2)
    else:
        print("Package already up to date, command already satisfied")

def operate(task, app):
    if checkpackagelist(app):
        match task:
            case "install":
                install(app)
            case "uninstall":
                uninstall(app)
            case "update":
                update(app)
            case "search":
                lookup(app)
    else:
        print("package doesn't exist :(")

def main():
    while True:
        task,app = input("operation: "), input("app to operate: ")
        operate(task,app)
main()
