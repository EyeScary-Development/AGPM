import json
import os
import requests
#temp list of packages
url = ''
metapath = os.path.join(os.path.expanduser('~'), '.agpm', 'localmetadata.json')
settingspath = os.path.join(os.path.expanduser('~'), '.agpm', 'sources.escnf')

def fetchsource():
    try:
      with open(settingspath, 'r') as file:
        source = file.readline()
        print("Source url: " + source)
        return source
    except Exception:
        return "https://eyescary-development.github.io/CDN/agpm_packages/packagelist.json"

def setsource():
    with open(settingspath, 'w') as file:
        file.write(input("Input your new source url: "))

def fetchlist():
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetchlocalmet():
    with open(metapath, 'r') as f:
        localmetadata = json.load(f)
    return localmetadata

def checkpackagelist(item):
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

def metawrite(metadata, path):
    with open(path, 'w') as f:
        json.dump(metadata, f, indent=2)

def install(item):
    os.system("curl -O https://eyescary-development.github.io/CDN/agpm_packages/"+item+"/protocols/install.sh && bash install.sh && rm install.sh")
    try:
      with open(path, 'r') as f:
        localmetadata = json.load(f)
    except Exception:
        localmetadata = {}
        metawrite(localmetadata, metapath)
    cloudmetadata=fetchlist()
    localmetadata[item]=cloudmetadata[item]
    metawrite(localmetadata, metapath)

def uninstall(item):
    os.system("curl -O https://eyescary-development.github.io/CDN/agpm_packages/"+item+"/protocols/uninstall.sh && bash uninstall.sh && rm uninstall.sh")
    localmetadata = fetchlocalmet()
    localmetadata.pop(item, None)
    metawrite(localmetadata, metapath)

def update(item):
    metadata=fetchlist()
    cloudver = metadata[item]["version"]
    localmetadata = fetchlocalmet()
    localver = localmetadata[item]["version"]
    if localver != cloudver:
        os.system("curl -O https://eyescary-development.github.io/CDN/agpm_packages/"+item+"/protocols/update.sh && bash update.sh && rm update.sh")
        localmetadata[item]=cloudmetadata[item]
        metawrite(localmetadata, metapath)
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
    global url
    url = fetchsource()
    usin = input("set (s)ource, or install/lookup/update/uninstall a package (o)?: ")
    match usin:
        case 'o':
          while True:
            task,app = input("operation: "), input("app to operate: ")
            operate(task,app)
        case 's':
            setsource()
main()
