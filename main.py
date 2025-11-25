#!/usr/bin/env python3
import sys
import time

print("Container started in manual mode.")
print("Run: docker exec -it evaluator python src/evaluator.py --trials 348 --seed 42")
print("Keeping container alive...")

while True:
    time.sleep(3600)
