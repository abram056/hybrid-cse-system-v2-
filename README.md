# Hybrid CSE System v2

A backend API for hybrid spam classification using both rule-based heuristics and machine learning, designed with a focus on reliability, testability, and containerized deployment.

📌 Overview

The Hybrid CSE System v2 is a backend service that classifies messages as ham, spam or smish using a hybrid approach:

* Rule-based filtering for deterministic checks
* Machine learning model for probabilistic classification
* Combined decision logic to improve accuracy and flexibility

The project is built with a strong emphasis on:

* Clean architecture
* Test coverage
* CI automation
* Containerized deployment
--

🚀 Features
* 🔍 Hybrid spam detection (rules + ML)
* ⚙️ REST API for classification
* 🧪 Unit & integration testing
* 🐳 Dockerized for consistent environments
* 🔁 CI pipeline with automated testing
* 📦 Structured, modular codebase
🧠 System Design
--

The system combines two classification strategies:

1. Rule-Based Engine
  * Applies predefined heuristics
  * Fast and deterministic
  * Useful for obvious spam patterns
2. Machine Learning Model
  * Learns patterns from data
  * Handles ambiguous or unseen inputs
3. Hybrid Decision Layer
  * Aggregates outputs from both systems
  * Produces final classification
  * Can be extended with weighting or confidence logic

🧩 Focus

This project emphasizes:
- modular system design
- hybrid decision systems
- reproducible environments via Docker
- automated testing pipelines

📂 Project Structure
```bash
src/
├── app/                # Core application logic
├── tests/              # Unit and integration tests
├── Dockerfile          # Container configuration
├── pyproject.toml      # Dependency management (Poetry)
├── .github/workflows/  # CI pipeline
└── README.md
```

⚙️ Setup & Installation
Option 1: Local Setup
```bash
git clone https://github.com/abram056/hybrid-cse-system-v2.git
cd hybrid-cse-system-v2

# Install dependencies (Poetry)
poetry install

# Activate virtual environment
poetry shell

# Run the application
```cmd
python main.py
```

Option 2: Docker (Recommended)
```bash
# Build image
docker build -t hybrid-cse-system .

# Run container
docker run -p 8000:8000 hybrid-cse-system
```
--

📡 API Usage
```http
Endpoint
POST /analyse
```

Request Body
```json
{
  "message": "Congratulations! You’ve won a free prize!"
}
```

Response
```json
{
  "label": "spam",
  "confidence": 0.92,
  "reason": "Detected promotional keywords and ML classification"
}
```
🧪 Testing

Run tests with:
```bash
pytest
```

Tests include:

* Unit tests for classification logic
* Integration tests for API endpoints
* Validation of hybrid decision behavior
--

🔁 CI/CD

The project uses GitHub Actions to:

* Run tests on every push
* Ensure code stability before merging
* Maintain consistent build behavior

This helps enforce:

* reliability
* regression prevention
* automated validation
--

🐳 Docker

The application is fully containerized to ensure:

Environment consistency
Easy deployment
Isolation from host dependencies
📈 Future Improvements
Model retraining pipeline
Improved hybrid weighting strategy
Logging & monitoring integration
Performance benchmarking (latency/throughput)
API authentication & rate limiting
👨‍💻 Author

Developed by Shesham Joseph

📜 License

This project is for educational and experimental purposes.
