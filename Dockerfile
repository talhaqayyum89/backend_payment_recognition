FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone https://x-token-auth:ATCTT3xFfGN0moPw3MfvNJNlzNWWJJ0tTLOCGG70xKv_MFNBDLnduP6TrE6xKRe3Z_rABdbFRApTx5BgrXloF5djhVUJhYss80AJ6-kpFom3PHd8lFeaMm71hm0YItsQt8ByzPQGlQZWWdUEr2hUxE0r01A-9-TONpmGkc0yimeNLhCUej8aLUA=929F2274@bitbucket.org/renmoney-itops/backend_payment_recognition.git
COPY . .

COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
RUN pip install streamlit

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8500/_stcore/health

COPY / ./
# ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8500", "--server.address=0.0.0.0"]
CMD streamlit run main.py
