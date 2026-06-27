# Use a lightweight Python image
FROM python:3.11-slim

# Set the working folder inside the container
WORKDIR /app

# Copy dependency list first
COPY requirements-app.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements-app.txt

# Copy the full project into the container
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Run the Streamlit app
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
