
docker build -t hxxd .

docker run -d --name hxxd -p 8080:8080 -v /data/cert/wx_cert:/data/cert --env-file hxxd.env hxxd