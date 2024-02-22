FROM --platform=linux/amd64 ubuntu:22.04

RUN apt update && apt full-upgrade -y && apt install xinetd build-essential -y

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./entrypoint.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./chall /chall
COPY ./flag.txt /flag.txt

CMD ["/start.sh"]