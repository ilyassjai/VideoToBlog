# test.py

if __name__ == "__main__":
  import sys

  # Access the text passed as a command-line argument
  text = sys.argv[1]

  # Print the received text
  print(f"Received text from Flask app: {text}")