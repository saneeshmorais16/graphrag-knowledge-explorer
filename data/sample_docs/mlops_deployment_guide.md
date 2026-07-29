# MLOps Deployment Guide

This local demo guide describes an illustrative development setup, not a production deployment.

## Components

FastAPI Inference API uses SQLite. FastAPI Inference API uses MLflow. RAG Support Assistant uses FastAPI Inference API. RAG Support Assistant uses TF-IDF. RAG Support Assistant uses NetworkX.

## Release checks

AI Governance Council requires Rollback Control. Releases require passing unit tests, citation checks, and synthetic-data review. Optional external LLM providers remain disabled by default.
