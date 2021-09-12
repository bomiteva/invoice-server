docker build -t invoice-server-img .
docker run -d --name invoice-server-container -p 80:80 invoice-server
http://127.0.0.1/docs

Open API documentation
http://127.0.0.1/docs

docker ps - get the id of the running container
docker exec -it <container_id> sh  - interactive mode, we can also get access to a command prompt in a running container
Go to /app/processed_files/invoices_... - to see generated files and images

TODO
- ако има проблем с големината на файла може да се обработва на чънкове
- Влаидация на формата на файла
- по добър еррор хандлинг
- Тестовият процес да бъде идемпотентна операция, 