FROM python:3.7-slim
LABEL org.opencontainers.image.authors="eric.chan.24@gmail.com"
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN mkdir ~/.streamlit  
COPY .streamlit/config.toml ~/.streamlit/config.toml
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . /app     
ENTRYPOINT ["streamlit", "run"]
CMD ["b_app.py"]