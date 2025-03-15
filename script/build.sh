
docker build -t hxxd .

docker run -d -p 8000:8000 --env-file hxxd.env hxxd