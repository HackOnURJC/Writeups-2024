FROM python:3.11-alpine 

RUN apk add --no-cache socat

WORKDIR /app
RUN pip install pycryptodome ecdsa   
COPY administration.py library.py /app

ENV FLAG="HackOn{this_is_a_fake_flag_but_you_can_try_to_get_the_real_one.@ELtusilin i!!!!!}"

EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python administration.py"]
