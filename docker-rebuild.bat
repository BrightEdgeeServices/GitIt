@ECHO $1
setlocal

:: Stop the existing container if it's running
docker stop beetools || echo No running container named beetools

:: Remove the stopped container
docker rm beetools || echo No container to remove

:: Build the new image
docker build -t beetools .

:: Run the container
docker run -d -p 3333:22 --name beetools -e LINUX_ROOT_PWD=%LINUX_ROOT_PWD% -e INSTALLER_USERID=%INSTALLER_USERID% -e INSTALLER_PWD=%INSTALLER_PWD% beetools

endlocal
