ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
COPY rootfs /
RUN chmod a+x /run.sh
RUN apk add --no-cache python3 py3-pip
RUN python3 -m pip install requests

CMD [ "/run.sh" ]
#ENTRYPOINT ["tail", "-f", "/dev/null"]