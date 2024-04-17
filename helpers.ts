import { Buffer } from "buffer";

const MEMPOOL_BROADCAST_SERVICE = "https://blockstream.info/testnet/api/tx";

export const transactionSubmitter = async (txHex: string) => {
  const request = await fetch(MEMPOOL_BROADCAST_SERVICE, {
    method: "POST",
    body: txHex,
  });

  const data = await request.text();

  return data;
};

export const assembleScript = (pubkey: any, xop: string) => {
  const xopHex = Buffer.from(xop);

  const script = [
    pubkey,
    "OP_CHECKSIG",
    "OP_0",
    "OP_IF",
    Buffer.from("ord"),
    "01",
    Buffer.from("text/plain"),
    "07",
    xopHex,
    "OP_0",
    xopHex,
    "OP_ENDIF",
  ];

  return script;
};
