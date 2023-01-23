
# S3 Uploader and emailer with link expire

- A simple pyhton script to upload files into s3 bucket with expirey link feature 
- The file link can be send to multple emails with custom email template.

- Change the config_sample.env name into .env also remove the link inside the env
## Usage

To deploy this project run

```bash
  Python3 main.py (expirey time in minutes) (filename/location) (emails seperated by commas)
```

Example
```bash
  Python3 main.py 30 123.txt hai@gmail.com,hello@helo.com
```
