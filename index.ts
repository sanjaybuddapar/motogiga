import fs from "fs";
import * as readline from 'readline';
import { Address, Signer, Tap, Tx } from "@cmdcode/tapscript";
import util from "@cmdcode/crypto-utils";
import { assembleScript, transactionSubmitter } from "./helpers";

const seckey = Buffer.from("PRIVATE KEY EXPORT HERE", "hex");
const pubkey = util.keys.get_pubkey(seckey, true);

const [tseckey] = Tap.getSecKey(seckey);
const [tpubkey] = Tap.getPubKey(pubkey);

const targetAddress = Address.p2tr.fromPubKey(tpubkey, "testnet");

const xop = "@moto:swap::cbrc-20:swap?ab=PIZZA-WAGMI&a=1&b=0.00000143";

const transactionSplitterBasic = async (utxo: string) => {
  const [txid, index] = utxo.split(":");

  const vouts = Array(200).fill({        // x200
    value: 5_000_000,                    // 0.05 BTC
    scriptPubKey: Address.toScriptPubKey(targetAddress),
  });

  const vin = [
    {
      txid,
      vout: Number(index),
      prevout: {
        value: 1_010_000_000,             // 10.1 BTC
        scriptPubKey: ["OP_1", tpubkey],
      },
    },
  ];

  const txnData = Tx.create({
    vin,
    vout: [...vouts],
  });

  const sig = Signer.taproot.sign(tseckey, txnData, 0);

  txnData.vin[0].witness = [sig];

  const txHex = Tx.encode(txnData).hex;

  const txId = await transactionSubmitter(txHex);

  return {
    inscriptionAddress: targetAddress,
    txId,
  };
};

const transactionSplitter = async (utxo: string) => {
  const [txid, index] = utxo.split(":");

  const inscribedXop = assembleScript(pubkey, xop);

  const tapleaf = Tap.encodeScript(inscribedXop);

  const [tspubkey, _] = Tap.getPubKey(pubkey, { target: tapleaf });

  const tsAddress = Address.p2tr.fromPubKey(tspubkey, "testnet");

  const vouts = Array(1000).fill({             // x1000
    value: 3_000,                              // 0.0003 BTC
    scriptPubKey: Address.toScriptPubKey(tsAddress),
  });

  const vin = [
    {
      txid,
      vout: Number(index),
      prevout: {
        value: 5_000_000,                      // 0.05 BTC
        scriptPubKey: ["OP_1", tpubkey],
      },
    },
  ];

  const txnData = Tx.create({
    vin,
    vout: [...vouts],
  });

  const sig = Signer.taproot.sign(tseckey, txnData, 0);

  txnData.vin[0].witness = [sig];

  const txHex = Tx.encode(txnData).hex;

  const txId = await transactionSubmitter(txHex);

  return {
    inscriptionAddress: tsAddress,
    txId,
  };
};

const createUtxo = (utxos: string) => {
  const [txid, index] = utxos.split(":");

  const inscribedXop = assembleScript(pubkey, xop);

  const tapleaf = Tap.encodeScript(inscribedXop);

  const [tpubkey, cblock] = Tap.getPubKey(pubkey, { target: tapleaf });

  const vin = [
    {
      txid,
      vout: Number(index),
      prevout: {
        value: 3_000,                                                // 0.0003 BTC
        scriptPubKey: ["OP_1", tpubkey],
      },
    },
  ];

  const vout = [
    {
      value: 463,
      scriptPubKey: Address.toScriptPubKey(targetAddress),
    },
  ];

  const txnData = Tx.create({
    vin,
    vout,
  });

  const sig = Signer.taproot.sign(seckey, txnData, 0, { extension: tapleaf });

  txnData.vin[0].witness = [sig, inscribedXop, cblock];

  const txHex = Tx.encode(txnData).hex;

  return txHex;
};

const transactionsCrafter = (txid: string) => {
  const utxos = Array.from({ length: 1000 }, (_, i) => `${txid}:${i}`);         // x1000

  utxos.forEach((utxo) => {
    const createdUtxo = createUtxo(utxo);

    fs.writeFileSync("./crafted-transactions.txt", `${createdUtxo}\n`, {
      flag: "a",
    });
  });
};

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
 }

 const splitSplitter = async (txid: string) => {
  const utxos = Array.from({ length: 200 }, (_, i) => `${txid}:${i}`);          // x200
 
  for (const utxo of utxos) {
    console.log(utxo)
     await transactionSplitter(utxo).then(data => {
       fs.appendFile('output_txns.txt', `${data['txId']}\n`, err => {
         if (err) {
           console.error('Error appending to file:', err);
         } else {
           console.log(data);
         }
       });
     });
     await sleep(500); // Sleep for 500ms before the next iteration
  }
 };

// ex: b4b8a2ec13703f22409cfe25dbfdf8052b5b02c259c1120f959c7ab9147fac81:0
const utxo = "utxo here:0";

// 1st step
//transactionSplitterBasic(utxo).then(console.log);

// 1.5 step
// take the txid from the previously created transaction and split-split the transactions
//splitSplitter("txid here")

// 2nd step
// take the txid from the previously created transaction and craft the transactions
// const filePath = 'output_txns.txt';

// // Create a readline interface
// const reader = readline.createInterface({
//  input: fs.createReadStream(filePath),
//  output: process.stdout,
//  terminal: false
// });

// // Listen for the 'line' event
// reader.on('line', (line) => {
//  // Perform your action on the line here
//  console.log(`Processing line: ${line}`);
//  transactionsCrafter(line)
// });

// // Handle the 'close' event
// reader.on('close', () => {
//  console.log('Finished reading the file.');
// });

// 3rd step
// execute relayer_no_redis.ts (npx tsx relayer_no_redis.ts)
