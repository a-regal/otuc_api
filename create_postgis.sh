#As shown in https://alexurquhart.com/post/set-up-postgis-with-docker/
docker volume create pg_data

#Initial pull is kind of heavy
docker run --name=postgis -d -e POSTGRES_USER=otuc -e POSTGRES_PASS=otuc_test -e \
        POSTGRES_DBNAME=otuc -e ALLOW_IP_RANGE=0.0.0.0/0 -p 5432:5432 -v pg_data:/var/lib/postgresql \
        --restart=always kartoza/postgis:9.6-2.4
