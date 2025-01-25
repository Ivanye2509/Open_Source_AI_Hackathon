from flask import Flask, request, jsonify
from flask_cors import CORS
from nbclient import NotebookClient
import nbformat

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store messages (for simplicity, use a list)
messages = []

# Define the /api/send route
@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message')
    if user_message:
        messages.append({"sender": "user", "text": user_message})  # Add user message

        # Path to the Jupyter Notebook
        notebook_path = "notebook.ipynb"

        try:
            # Load the notebook
            with open(notebook_path) as f:
                nb = nbformat.read(f, as_version=4)

            # Replace the user_message variable in the notebook
            for cell in nb.cells:
                if cell.cell_type == "code" and "user_message =" in cell.source:
                    cell.source = cell.source.replace('"Hello"', f'"{user_message}"')

            # Execute the notebook
            client = NotebookClient(nb)
            client.execute()

            # Extract the bot response from the notebook
            bot_response = ""
            for cell in nb.cells:
                if cell.cell_type == "code" and "outputs" in cell:
                    for output in cell.outputs:
                        if "text" in output:
                            bot_response += output.text

            # Add the bot's response to the messages list
            messages.append({"sender": "bot", "text": bot_response})
            return jsonify({"status": "success", "messages": messages})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "No message provided"}), 400

# Define the /api/messages route
@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})  # Return all messages

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Run the server on port 5000 with debug mode