# ===============================
# Base image
# ===============================
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy model + code + dependencies
COPY lightfm_model.pkl .
COPY model-server.py .
COPY model-requirements.txt .

# ===============================
# Install system dependencies
# ===============================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Install Python dependencies
# ===============================
# Fix version conflicts (LightFM requires old setuptools)
RUN pip install --no-cache-dir --upgrade pip setuptools==69.5.1 wheel cython==0.29.36

# Preinstall numpy/scipy first (LightFM needs them)
RUN pip install --no-cache-dir numpy scipy

# Install remaining dependencies
RUN pip install --no-cache-dir -r model-requirements.txt

# ===============================
# Expose & run server
# ===============================
EXPOSE 5001

CMD ["python", "model-server.py"]
