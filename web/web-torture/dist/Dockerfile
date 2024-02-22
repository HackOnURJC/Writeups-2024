FROM golang:latest

WORKDIR /app

COPY . ./
COPY flag.txt /
RUN chmod 777 /flag.txt
RUN rm /app/flag.txt

RUN go mod download

EXPOSE 3000

CMD ["go", "run", "./main.go"]

