#!/bin/bash

echo "Starting Ollama server in background..."
# Start the Ollama server in the background.
ollama serve &

apt-get update && apt-get install -y curl

# Get the Process ID (PID) of the background Ollama server.
OLLAMA_PID=$!

echo "Waiting for Ollama server to be ready..."
# Loop to check if the Ollama server is responsive.
# It attempts to curl the local Ollama API endpoint until it succeeds or times out.
for i in $(seq 1 30); do # Try for up to 30 times with a 5-second delay (total 150 seconds).
  curl -s http://localhost:11434 > /dev/null
  if [ $? -eq 0 ]; then
    echo "Ollama server is ready."
    break # Exit the loop if the server is responsive.
  fi
  echo "Still waiting for Ollama server... (attempt $i/30)"
  sleep 5 # Wait for 5 seconds before retrying.
done

# Check if the background Ollama server process is still running.
if ! ps -p $OLLAMA_PID > /dev/null; then
  echo "Error: Ollama server did not start or stopped unexpectedly."
  exit 1 # Exit with an error if the server process is not found.
fi

echo "Pulling Ollama models..."
# Now that the server is confirmed to be running, pull the models.
ollama pull mxbai-embed-large
ollama pull llama3

# Check if the model pulls were successful.
if [ $? -ne 0 ]; then
    echo "Warning: Failed to pull one or more Ollama models. Please check logs for details."
    # The script will continue to keep the server running even if model pulls fail,
    # but you might want to uncomment the 'exit 1' line below if you want the container
    # to stop on model pull failure.
    # exit 1
fi

echo "Models pulled. Keeping Ollama server running as the main process."
# Wait for the background Ollama server process to complete.
# This ensures that the container remains active as long as Ollama is serving.
wait $OLLAMA_PID