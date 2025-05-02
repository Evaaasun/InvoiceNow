from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)
RECEIVED_DIR = "received_invoices"
os.makedirs(RECEIVED_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return "AP Provider is running."

@app.route("/receive_invoice", methods=["POST"])
def receive_invoice():
    invoice = request.json
    invoice_id = invoice.get("invoiceId")
    if not invoice_id:
        return jsonify({"error": "Missing invoiceId"}), 400

    filename = os.path.join(RECEIVED_DIR, f"{invoice_id}.json")
    with open(filename, "w") as f:
        json.dump(invoice, f, indent=2)

    return jsonify({"message": f"Invoice {invoice_id} received successfully"}), 200

@app.route("/receive_invoices_batch", methods=["POST"])
def receive_invoices_batch():
    invoices = request.json
    results = []

    for invoice in invoices:
        invoice_id = invoice.get("invoiceId")
        if not invoice_id:
            results.append({"error": "Missing invoiceId in one record"})
            continue

        filename = os.path.join(RECEIVED_DIR, f"{invoice_id}.json")
        with open(filename, "w") as f:
            json.dump(invoice, f, indent=2)

        results.append({"invoiceId": invoice_id, "status": "stored"})

    return jsonify(results), 200

@app.route("/view_received/<invoice_id>", methods=["GET"])
def view_received_invoice(invoice_id):
    filename = os.path.join(RECEIVED_DIR, f"{invoice_id}.json")
    if not os.path.exists(filename):
        return jsonify({"error": "Invoice not found"}), 404
    with open(filename) as f:
        invoice = json.load(f)
    return jsonify(invoice)

if __name__ == "__main__":
    app.run(port=5001)
