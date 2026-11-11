import sys
import os
import time
import io
import tracemalloc

# Add project root to Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hoa_core.auth import authenticate
from hoa_core.documents import upload_document
from hoa_core.issues import create_issue
from hoa_core.messages import post_message

uploader = "alice"

print("\n=== HOA Digital Management System Performance Metrics ===\n")

# Login latency
start = time.perf_counter()
authenticate("alice", "password123")
end = time.perf_counter()
print(f"Login latency: {end - start:.6f} seconds")

# Document upload latency
fake_file = io.BytesIO(b"This is test content")
start = time.perf_counter()
upload_document(fake_file, "testfile.txt", uploader)
end = time.perf_counter()
print(f"Document upload latency: {end - start:.6f} seconds")

# Issue creation latency
start = time.perf_counter()
create_issue("Test Issue", "Performance test issue", uploader)
end = time.perf_counter()
print(f"Issue creation latency: {end - start:.6f} seconds")

# Message posting latency
start = time.perf_counter()
post_message("general", "Performance test message", uploader)
end = time.perf_counter()
print(f"Message posting latency: {end - start:.6f} seconds")

# Throughput test
start = time.perf_counter()
for i in range(20):
    fake_file = io.BytesIO(b"Test content")
    upload_document(fake_file, f"file_{i}.txt", uploader)
end = time.perf_counter()
ops_per_sec = 20 / (end - start)
print(f"Throughput: {ops_per_sec:.2f} operations per second")

# Memory footprint test
tracemalloc.start()
fake_file = io.BytesIO(b"Memory test content")
upload_document(fake_file, "memory_test.txt", uploader)
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"Memory footprint: current={current/1024:.2f} KB, peak={peak/1024:.2f} KB")

print("\n=== End of Performance Metrics ===\n")
