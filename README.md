# hashr

hashr is a machine-payable compute server scaffold built with FastAPI.

Endpoints return **HTTP 402 Payment Required** (via x402) when compute work requires payment. The server responds with a JSON quote containing a `price`, `payment_address`, and `job_id`.

## x402 usage
- Call a compute or job endpoint.
- If payment is required, the response will be `402` with a quote.
- Pay the quote and retry with the required x402 payment proof/header.

Service metadata is published at `.well-known/x402`.

## Example 402 response
```
POST /compute/hash HTTP/1.1
Content-Type: application/json

{
  "input": {"text": "hello"}
}
```

**Response**
```
HTTP/1.1 402 Payment Required
Content-Type: application/json

{
  "price": "100",
  "payment_address": "x402://demo",
  "job_id": "job-example"
}
```

## Agent Services
These endpoints help turn hashr into a usable agent service layer. They are machine-payable (x402) and may return `402 Payment Required` with a quote.

- **Proof verification**: POST `/proof/verify` and GET `/proof/{job_id}`
- **Wallet risk analysis**: POST `/wallet/risk`
- **ERC8004 reputation lookup**: POST `/reputation/erc8004`
