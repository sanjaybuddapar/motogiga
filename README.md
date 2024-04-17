# motogiga
 
- 1st step is to download the repo (Code > Download as ZIP / Github / Github Desktop / etc).
  - Place them into a single folder by extracting them, take note of where this folder is.
- 2nd step is to run `npm install` inside the folder (`cd folder` to get to the folder first).
  - Open a command terminal (cmd.exe on windows/terminal on mac/linux).
  - Type `cd folder-path-here` to open the folder.
  - Run `npm install` next after getting to the correct folder. 
- 3rd step is to put your private key exported from unisat at the top (Unisat > Account # > ... > Export > Hex Key).
  - The place to put it is inside `index.ts`, at the top of the file where it says `YOUR PRIVATE KEY HERE`. 
  - Please use a fresh wallet, I don't want anyone asking if this is malicious (Spoiler, it isn't malicious but still...).
  - Be smart and only use automation on fresh wallets, it's not worth the risk any other way.
- 4th step is to create a UTXO with 10.1 tBTC in it and get that txID (send yourself 10.1 tBTC and ***wait for confirm***).
  - By sending your own account 10.1 tBTC you are creating a new unspent UTXO.
  - Copy the ID from unisat wallet after hitting send by clicking "show in explorer" under the checkmark.
  - The TX ID is the hash at the top, so copy that, add `:0` to the end of it, and paste it into `index.ts`
- 5th step is to uncomment `transactionSplitterBasic(utxo).then(console.log);`, put your UTXO above it, then run `npx tsx index.ts`
  - This is located ***at the bottom*** of `index.ts`, to uncomment them remove the `//` before the line of code. 
- 6th step is to ***wait for that TX to confirm*** and copy the output TX ID and recomment out this step.
  - You can track the progress by going to `https://mempool.space/testnet` and pasting the TX_ID there.
- 7th step is to put that tx ID in this line under step 1.5: `splitSplitter("txid here")`, then run `npx tsx index.ts`
  - This is located ***at the bottom*** of `index.ts`, to uncomment them remove the `//` before the line of code.
- 8th step is to wait for all 200 of those TXNs to confirm and recomment out this step.
  - You can track the progress by copying one of those IDs and going to `https://mempool.space/testnet` again.
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
  });
  ```
  Then run `npx tsx index.ts`
  - This is located ***at the bottom*** of `index.ts`, to uncomment them remove the `//` before the line of code.
- 10th and final step is to run relayer_no_redis.ts using `npx tsx relayer_no_redis.ts`.
- Good job, you did it.

**Make sure to do the following if you're running this more than one time:**
- Rename or delete crafted-transactions.txt.
- Rename or delete output_txns.txt
- Re-comment out all the steps except the one you're running in `index.ts`.

You can edit the values that are sent to increase or decrease gas used. This is to send 200,000 transactions at ~15 sats/vb.
By changing the values and numbers inside each of the commented lines, you can achieve different number of transactions, and different gas amounts.
I won't get into detail on how to up the gas values, because it'd start a gas war... but if you're smart enough to figure it out, go nuts.

Full credit to https://github.com/cryptosalomao
I just made it do more txns, faster.
