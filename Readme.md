
# S3 Uploader and emailer with link expiry

- A simple Python script to upload files into an s3 bucket with an expiry link feature 
- The file link can be sent to multiple emails with a custom email template.

- Change the config_sample.env name into .env also remove the link inside the env
## Usage

To deploy this project run

```bash
  Python3 main.py (expiry time in minutes) (filename/location) (emails separated by commas)
```

Example
```bash
  Python3 main.py 30 123.txt hai@gmail.com,hello@helo.com
```
