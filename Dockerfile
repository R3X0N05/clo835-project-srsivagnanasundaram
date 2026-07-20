FROM python:3.11-slim
WORKDIR /app
COPY apps/python/app.py .
# RUN <build your app, if it needs a build step>
EXPOSE 8080
CMD ["python3", "app.py"]