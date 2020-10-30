import paramiko
import os
import datetime


def bytecount(sofar,total):
    print("{0:.2f}% transfered".format(sofar/total*100),end="\r")


localPath="/home/vikas/Desktop/ServerBackup/"
os.makedirs(localPath,exist_ok=True)
remotePaths={
              "Auth":"/mpd/auth/",
             "Static_data":"/mpd/site/",
             "Code":"/mpd/django/abcd/",
              "Apache":"/etc/apache2/",
             "Ipdata":"/ipdata/",
             "Important_Data":"/important/",
             "Mysql":{'loc':"/mysqlBackup/",'databaseName':"vikas"}
             }

def sync(remotePath,tarFilename):
    
    
    sourceFilepath=os.path.join(os.path.dirname(os.path.dirname(remotePath)),tarFilename)
    
    try: 
        a,b,c=ssh_obj.exec_command(f"tar -cf  {sourceFilepath}  {remotePath}")
    except :
        print("Error")
        for i in c:
            print(i)
    else:
        print("Warning\Message")
        for i in c:
            print(i)
            
        sftp_cli=ssh_obj.open_sftp()
        sftp_cli.get(sourceFilepath,localPath+tarFilename,callback=bytecount)
        print("\n")
        
        print("Back up Saved  at ",localPath+tarFilename)
        sftp_cli.remove(sourceFilepath)
        print("deleteted ",sourceFilepath)
        sftp_cli.close()
      


    
ssh_obj=paramiko.SSHClient()
ssh_obj.load_system_host_keys()
ssh_obj.connect(hostname="172.105.39.102",username="root",password="1@Million")



dd=datetime.datetime.now().strftime("%y-%m-%dT%H:%M:%S")
sqlBackupFile=f"mysqldumpVikas{dd}.sql"
sqlBackupFilePath=os.path.join(remotePaths['Mysql']['loc'],sqlBackupFile)
ssh_obj.exec_command(f"mkdir {remotePaths['Mysql']['loc']}")
try:
    temp=ssh_obj.exec_command(f"mysqldump {remotePaths['Mysql']['databaseName']}>{sqlBackupFilePath}")
except:
    print("Error")
else:
    for i in temp[2]:
        print(i)
    print("My Sql Dump Created")    

    
for i,remotePath in remotePaths.items():

    dd=datetime.datetime.now().strftime("%y-%m-%dT%H:%M:%S")
    tarFilename=f"{i}-{dd}.tar"
    print(f"******************creating Backup of {remotePath} with Filename {tarFilename}*******************")  
    if i =="Mysql":
        sync(remotePath['loc'],tarFilename)
    else:
        sync(remotePath,tarFilename)
    print(f"___________________________________________{i} Done_____________________________________________")


ssh_obj.exec_command(f"rm {remotePaths['Mysql']['loc']}*.*")
ssh_obj.close()
