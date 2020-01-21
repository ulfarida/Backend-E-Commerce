FROM python:3.6.5
MAINTAINER Your Name "ulfah@alterra.id"
RUN mkdir -p /portofolio-be
COPY . /portofolio-be
RUN pip install -r /portofolio-be/requirement.txt
WORKDIR /portofolio-be
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

