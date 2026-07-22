FROM python:3.11-slim
WORKDIR /app
#To install Flask
RUN pip install --no-cache-dir flask==3.0.3
COPY apps/python/app.py .
# RUN <build your app, if it needs a build step>
EXPOSE 8080
CMD ["python3", "app.py"]