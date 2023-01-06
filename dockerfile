FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
EXPOSE 88

# Puerto para la escucha del servicio de mensajeria
# EXPOSE 85

# Servicio backend API
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "88", "--reload"]

# Servicio de mensajeria que siempre debe de estar a la escucha
# Debe tener su propio contenedo levantado
# CMD [ "python", "-u", "consumer.py" ]
