# motogiga
 
- 1st step is to download the repo.
- 2nd step is to run `npm install` inside the repo folder.
- 3rd step is to put your private key exported from unisat at the top.
- 4th step is to create an unspent UTXO with 10.1 tBTC in it and get that txID.
- 5th step is to uncomment `transactionSplitterBasic(utxo).then(console.log);` and put your UTXO above it, then run `npx tsx index.ts`
- 6th step is to wait for that TX to confirm and copy the output TX ID and recomment out this step.
- 7th step is to put that tx ID in this line: `splitSplitter("txid here")`, then run `npx tsx index.ts`
- 8th step is to wait for all 200 of those TXNs to confirm and recomment out this step.
- 9th step is to uncomment all of the lines after 'step 2', so, the following:
  ```js
  const filePath = 'output_txns.txt';
  
  // Create a readline interface
  const reader = readline.createInterface({
   input: fs.createReadStream(filePath),
   output: process.stdout,
   terminal: false
  });
  
  // Listen for the 'line' event
  reader.on('line', (line) => {
   // Perform your action on the line here
   console.log(`Processing line: ${line}`);
   transactionsCrafter(line)
  });
  
  // Handle the 'close' event
  reader.on('close', () => {
   console.log('Finished reading the file.');
  });```
  Then run `npx tsx index.ts`
- 10th and final step is to run relayer_no_redis.ts using `npx tsx relayer_no_redis.ts`.
- Good job, you did it.