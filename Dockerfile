# ১. অফিশিয়াল পাইথন ৩.১২ ইমেজ ব্যবহার করছি (Lightweight alpine/slim version)
FROM python:3.12-slim

# ২. পাইথনের আউটপুট স্ট্রিম সরাসরি টার্মিনালে পাঠানোর জন্য পরিবেশ পরিবর্তন (Buffering অফ করা)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ৩. কন্টেইনারের ভেতর ওয়ার্কিং ডিরেক্টরি সেট করছি
WORKDIR /app

# ৪. সিস্টেমের ডিপেন্ডেন্সি ও প্রয়োজনীয় টুলস ইনস্টল
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ৫. requirements.txt ফাইল কপি করে প্যাকেজ ইনস্টল করা
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ৬. প্রজেক্টের সমস্ত কোড কন্টেইনারে কপি করা
COPY . /app/