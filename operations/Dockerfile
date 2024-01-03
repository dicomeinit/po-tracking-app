FROM python:3.10-slim

ENV APP_HOME=/opt
ENV PYTHONPATH=$APP_HOME
ENV DJANGO_SETTINGS_MODULE=app.settings
ENV STATIC_ROOT=$APP_HOME/static

ADD operations/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/requirements.txt
RUN pip install -r requirements.txt
ADD app $APP_HOME/app

WORKDIR $APP_HOME/app
RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "app.wsgi", "-b", "0.0.0.0:8000"]
EXPOSE 8000
