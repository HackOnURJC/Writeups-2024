FROM --platform=linux/amd64 ubuntu:22.04

RUN apt update && apt full-upgrade -y && apt install xinetd build-essential -y && apt install libseccomp-dev -y

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./entrypoint.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./noleak /noleak
RUN chmod +x /noleak

COPY ./flag.txt /flag.txt
#EXPOSE 7676
CMD ["/start.sh"]
