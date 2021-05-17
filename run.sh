#!/bin/bash

if ! docker-compose up -d --scale web=2; then
  echo "=> Failed to build docker. Exit"
  exit 1
fi
echo "=> Running System Tests..."
sleep 5s
if python3 -m unittest test; then
    echo $'\n' "=> All tests passed. Container is running..."
else
  echo "=> System tests were failed. Shutting down container..."
  docker-compose down
  exit 1
fi