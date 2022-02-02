/* eslint-disable no-console */
const path = require('path')
const basePath = process.cwd()
const fs = require('fs')
const csv = require('csv-parser')

/*const dotenv = require('dotenv')
dotenv.config({
  path: path.join(basePath, '/.env'),
})*/

const generatorPath = '/Users/alfreddagenais/httpdocs/nftnlove/opensea_automatic_uploader'

const allMetadata = []

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function main() {
  const metasDatasFile = `${basePath}/data/nft_metadatas_sell.json`;
  try {
    fs.unlinkSync(metasDatasFile);
  } catch (error) {
    // No Error
  }

  const results = [];
  await fs.createReadStream(`${generatorPath}/datas/nft_metadatas_part4.csv`)
    .pipe(csv({
      separator: ';;\t ',
      mapHeaders: ({ header, index }) => header.toLowerCase().replace(' ', '')
    }))
    .on('data', (data) => results.push(data))
    .on('end', () => {
      console.log('results total', results.length);
      console.log('results0', results[0]);
      // [
      //   { NAME: 'Daffy Duck', AGE: '24' },
      //   { NAME: 'Bugs Bunny', AGE: '22' }
      // ]

      for (const result of results) {
        const resultUrl = result['nft_url'] || result.nft_url || null;
        if (!resultUrl || resultUrl === '' || resultUrl.substring(0, 5) !== 'https') {
          continue;
        }

        const randomPrice = getRandomInt(2, 9);
        const pricePrint = parseFloat(String(`0.0${randomPrice}`)).toFixed(2);

        const metaData = {
          "nft_url": String(resultUrl).trim(),
          "supply": 1,
          "blockchain": "Ethereum",
          "sale_type": "Fixed Price",
          "price": parseFloat(pricePrint),
          "method": "",
          "duration": [
            "01-02-2022 23:59", "28-02-2022 23:59"
          ],
          "specific_buyer": false,
          "quantity": 1,
        };

        allMetadata.push(metaData)
      }

      fs.writeFileSync(
        metasDatasFile,
        JSON.stringify({
          nft: allMetadata
        }, null, 2)
      )
    });
}

main()
