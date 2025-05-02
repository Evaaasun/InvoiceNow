from flask import Flask, request, jsonify, render_template
import os
import json
import uuid

app = Flask(__name__)
INVOICE_DIR = "invoices"
os.makedirs(INVOICE_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_invoice", methods=["POST"])
def generate_invoice():
    data = request.json
    invoice_id = data.get("invoiceId", f"INV-{uuid.uuid4().hex[:8].upper()}")
    filename = os.path.join(INVOICE_DIR, f"{invoice_id}.json")

    invoice = {
        "customizationId": "SGPeppol",
        "profileId": "invoice",
        "invoiceId": invoice_id,
        "uuid": str(uuid.uuid4()),
        "issueDate": data["issueDate"],
        "invoiceTypeCode": "380",
        "invoiceCurrencyCode": data["invoiceCurrencyCode"],

        "sellerElectronicAddress": data["sellerElectronicAddress"],
        "sellerAddressSchemeId": "0195",
        "sellerTaxId": data["sellerTaxId"],
        "taxSchemeId": "GST",
        "sellerName": data["sellerName"],
        "sellerLegalRegistrationId": data["sellerLegalRegistrationId"],
        "sellerTradingName": data["sellerTradingName"],
        "sellerAddressLine1": data["sellerAddressLine1"],
        "sellerPostCode": data["sellerPostCode"],
        "sellerCountryCode": data["sellerCountryCode"],

        "buyerElectronicAddress": data["buyerElectronicAddress"],
        "buyerAddressSchemeId": "0195",
        "buyerId": data["buyerId"],
        "buyerTradingName": data["buyerTradingName"],
        "buyerAddressLine1": data["buyerAddressLine1"],
        "buyerPostCode": data["buyerPostCode"],
        "buyerCountryCode": data["buyerCountryCode"],
        "buyerName": data["buyerName"],
        "buyerLegalRegistrationId": data["buyerLegalRegistrationId"],

        "invoiceTotalTaxAmount": float(data["invoiceTotalTaxAmount"]),
        "taxCategoryTaxableAmount": float(data["taxCategoryTaxableAmount"]),
        "taxAmountPerCategory": float(data["taxAmountPerCategory"]),
        "taxCategoryCode": "SR",
        "taxSchemeId": "GST",
        "taxCategoryRate": float(data["taxCategoryRate"]),

        "lineExtensionAmount": float(data["lineExtensionAmount"]),
        "taxExclusiveAmount": float(data["taxExclusiveAmount"]),
        "taxInclusiveAmount": float(data["taxInclusiveAmount"]),
        "payableAmount": float(data["payableAmount"])
    }

    with open(filename, "w") as f:
        json.dump(invoice, f, indent=2)

    return jsonify({"message": "Invoice generated successfully", "invoiceId": invoice_id}), 201

@app.route("/generate_invoices_batch", methods=["POST"])
def generate_invoices_batch():
    invoices = request.json
    result = []
    for data in invoices:
        invoice_id = data.get("invoiceId", f"INV-{uuid.uuid4().hex[:8].upper()}")
        filename = os.path.join(INVOICE_DIR, f"{invoice_id}.json")
        invoice = {
            "customizationId": "SGPeppol",
            "profileId": "invoice",
            "invoiceId": invoice_id,
            "uuid": str(uuid.uuid4()),
            "issueDate": data["issueDate"],
            "invoiceTypeCode": "380",
            "invoiceCurrencyCode": data["invoiceCurrencyCode"],

            "sellerElectronicAddress": data["sellerElectronicAddress"],
            "sellerAddressSchemeId": "0195",
            "sellerTaxId": data["sellerTaxId"],
            "taxSchemeId": "GST",
            "sellerName": data["sellerName"],
            "sellerLegalRegistrationId": data["sellerLegalRegistrationId"],
            "sellerTradingName": data["sellerTradingName"],
            "sellerAddressLine1": data["sellerAddressLine1"],
            "sellerPostCode": data["sellerPostCode"],
            "sellerCountryCode": data["sellerCountryCode"],

            "buyerElectronicAddress": data["buyerElectronicAddress"],
            "buyerAddressSchemeId": "0195",
            "buyerId": data["buyerId"],
            "buyerTradingName": data["buyerTradingName"],
            "buyerAddressLine1": data["buyerAddressLine1"],
            "buyerPostCode": data["buyerPostCode"],
            "buyerCountryCode": data["buyerCountryCode"],
            "buyerName": data["buyerName"],
            "buyerLegalRegistrationId": data["buyerLegalRegistrationId"],

            "invoiceTotalTaxAmount": float(data["invoiceTotalTaxAmount"]),
            "taxCategoryTaxableAmount": float(data["taxCategoryTaxableAmount"]),
            "taxAmountPerCategory": float(data["taxAmountPerCategory"]),
            "taxCategoryCode": "SR",
            "taxSchemeId": "GST",
            "taxCategoryRate": float(data["taxCategoryRate"]),

            "lineExtensionAmount": float(data["lineExtensionAmount"]),
            "taxExclusiveAmount": float(data["taxExclusiveAmount"]),
            "taxInclusiveAmount": float(data["taxInclusiveAmount"]),
            "payableAmount": float(data["payableAmount"])
        }
        with open(filename, "w") as f:
            json.dump(invoice, f, indent=2)
        result.append({"invoiceId": invoice_id, "status": "stored"})
    return jsonify(result), 201

@app.route("/view_invoices/<invoice_id>", methods=["GET"])
def view_invoice(invoice_id):
    path = os.path.join(INVOICE_DIR, f"{invoice_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "Invoice not found"}), 404
    with open(path) as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True)
