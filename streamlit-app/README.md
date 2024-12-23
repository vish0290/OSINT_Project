# Streamlit Application for Document Retrieval

This project is a Streamlit application that allows users to input questions and retrieve answers based on a set of documents. The application utilizes a retrieval chain to process the input and provide relevant responses.

## Project Structure

```
streamlit-app
├── src
│   ├── app.py          # Main entry point of the Streamlit application
│   ├── rag.py          # Logic for loading documents and retrieval chain
│   └── types
│       └── index.py    # Custom types and interfaces
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd streamlit-app
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Execute the following command to start the Streamlit application:
   ```bash
   streamlit run src/app.py
   ```

## Usage

- Open your web browser and navigate to `http://localhost:8501` to access the application.
- Enter your question in the input field and submit to receive an answer based on the provided context.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.