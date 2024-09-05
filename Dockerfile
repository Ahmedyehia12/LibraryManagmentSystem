# 1. Use a base image with Python installed
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the current directory contents into the container at /app
COPY . /app

# 4. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Set Flask environment (optional)
ENV FLASK_ENV=production

# 6. Expose the port your application runs on
EXPOSE 5000

# 7. Run the application
CMD ["python", "app.py"]


#hi there