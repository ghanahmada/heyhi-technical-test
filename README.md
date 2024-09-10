# Heyhi Technical Test

Name: Ghana Ahmada Yudistira

## 1. Install virtual environment
```bash
python -m venv env
```

## 2. Activate virtual environment
```bash
# Mac/Linux
source env/bin/activate

# Windows
env/Scripts/activate.bat
```

## 3. Build docker
```bash
docker build -t <IMAGE_NAME>:<IMAGE_TAG>

# Example
docker build -t heyhi-technical-test:1.0
```

## 4. Run docker
```bash
docker run -p 8000:8000 <IMAGE_NAME>:<IMAGE_TAG>

# Example
docker run -p 8000:8000 heyhi-technical-test:1.0
```


