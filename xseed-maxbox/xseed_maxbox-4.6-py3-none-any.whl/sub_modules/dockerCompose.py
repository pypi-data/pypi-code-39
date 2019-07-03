import subprocess as sp
import os
import sys

def createEnvVariable(miniCampus,password, dbusername, dbpassword, buildEnv):
    command = 'sudo chown -R xseed:xseed /var/www/'
    os.system('echo %s|sudo -S %s' % (password, command))
    line1 = "MINICAMPUS_CODE=%s" %miniCampus
    line2 = "MONGO_INITDB_ROOT_USERNAME=%s" %dbusername
    line3 = "MONGO_INITDB_ROOT_PASSWORD=%s" %dbpassword
    line4 = "NODE_ENV=%s" %buildEnv
    file = open("/var/www/.env", "w")
    file.write('{}\n{}\n{}\n{}'.format(line1,line2,line3, line4))
    file.close()

    # os.system('echo "MINICAMPUS_CODE=%s\
    # MONGO_INITDB_ROOT_USERNAME=%s\
    # MONGO_INITDB_ROOT_PASSWORD=%s \
    # BUILD_ENV=%s"| sudo tee /var/www/.env' %(miniCampus, dbusername, dbpassword, buildEnv))

def updatingDockerComposeFile():
    pkgdir = sys.modules['xseed_maxbox'].__path__[0]
    fullpath = os.path.join(pkgdir,"data/docker-compose.yml" )
    os.system('sudo cp %s /var/www/' %fullpath)

def dockerLogin(userName, passWord):
    os.system("echo %s |sudo docker login --username %s --password-stdin" %(passWord, userName))

def configureDocker(miniCampus,password, dbusername, dbpassword, dockerusername, dockerpassword, buildEnv):
    try:
        createEnvVariable(miniCampus,password, dbusername, dbpassword, buildEnv)
        updatingDockerComposeFile()
        dockerLogin(dockerusername, dockerpassword)
    except OSError:
        print (e.message)
        print ("Exiting the process because of above error")
        exit();
