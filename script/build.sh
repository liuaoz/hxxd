
docker build -t hxxd .

docker run -d --name hxxd -p 8080:8080 --env-file hxxd.env hxxd