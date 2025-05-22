FROM python:3.11-slim

# Install cron
RUN apt-get update && apt-get install -y cron

# Set work directory
WORKDIR /app

# Copy python script and crontab
COPY code/ /app/
COPY requirements.txt /app/
COPY crontab.txt /etc/cron.d/my-cron-job
# Give execution rights
RUN chmod 0644 /etc/cron.d/my-cron-job && \
    touch /var/log/cron.log

# Apply the cron job
RUN crontab /etc/cron.d/my-cron-job

# Run cron in foreground
CMD ["cron", "-f"]