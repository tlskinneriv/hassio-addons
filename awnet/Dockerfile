ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh /
COPY awnet.py /
RUN chmod a+x /run.sh
RUN apk add --no-cache python3 py3-pip
RUN pip3 install paho-mqtt==1.5.0

CMD [ "/run.sh" ]
#ENTRYPOINT ["tail", "-f", "/dev/null"]