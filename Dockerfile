#FROM ubuntu:23.10
#FROM python:3.11
FROM python:3.11-slim as base

# Set the working directory to /app
WORKDIR /app

# Install SSH server
RUN apt update && \
    apt upgrade -y && \
    apt-get clean && \
    apt-get install -y sudo && \
    apt-get install -y ufw&& \
    apt-get install -y openssh-server && \
    apt-get install -y --no-install-recommends python3-venv  && \
    rm -rf /var/lib/apt/lists/* && \
    if [ ! -d "/var/run/sshd" ]; then mkdir /var/run/sshd; fi

# Allow root login and password authentication
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Add the startup script
COPY install.sh /usr/local/bin/install.sh
RUN chmod +x /usr/local/bin/install.sh

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it
RUN python3 -m venv /app/venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Update pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install the current directory in editable mode and install other dependencies
RUN pip install --no-cache-dir -e .[dev]

# Do the script installation
CMD ["/usr/local/bin/install.sh"]
