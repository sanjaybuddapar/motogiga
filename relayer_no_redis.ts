import fs from "fs";
import { transactionSubmitter } from "./helpers";

const TRANSACTIONS_FILE = "./crafted-transactions.txt";

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
 }

// Simple queue implementation
class SimpleQueue {
 constructor() {
    this.queue = [];
    this.isProcessing = false;
 }

 enqueue(item) {
    this.queue.push(item);
    this.processQueue();
 }

 async processQueue() {
    if (this.isProcessing || this.queue.length === 0) return;
    this.isProcessing = true;
    const item = this.queue.shift();
    await this.processItem(item);
    this.isProcessing = false;
    this.processQueue(); // Recursively process the next item
 }

 async processItem(item) {
    await new Promise((resolve) => setTimeout(resolve, 350));
    const data = await transactionSubmitter(item.tx);
    console.log(
      `Transaction [${item.id}] ::`,
      data,
      `${new Date().toLocaleTimeString()}`
    );
    await sleep(100);
 }
}

const queue = new SimpleQueue();

const transactions = fs.readFileSync(TRANSACTIONS_FILE, "utf8").split("\n");

transactions.forEach((tx, id) => {
 queue.enqueue({ tx, id });
});