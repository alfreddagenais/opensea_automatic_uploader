/* eslint-disable no-console */
const path = require('path')
const basePath = process.cwd()
const fs = require('fs')

/*const dotenv = require('dotenv')
dotenv.config({
  path: path.join(basePath, '/.env'),
})*/

const generatorPath = '/Users/alfreddagenais/httpdocs/nftnlove/nftnlove-create-nft-collection'

const allMetadata = []

async function main() {
  const metasDatasFile = `${basePath}/data/nft_metadatas.json`;
  try {
    fs.unlinkSync(metasDatasFile);
  } catch (error) {
    // No Error
  }

  const files = fs.readdirSync(`${generatorPath}/build/images`)
  files.sort(function (a, b) {
    return a.split('.')[0] - b.split('.')[0]
  })

  for (const file of files) {
    const fileName = parseInt(path.parse(file).name);
    if (fileName <= 1000) {
      continue;
    }

    const jsonFile = fs.readFileSync(`${generatorPath}/build/json/${fileName}.json`)
    const jsonMeta = JSON.parse(jsonFile)
    const metaData = {
      "file_path": `${generatorPath}/build/images/${fileName}.png`,
      "nft_name": jsonMeta.name,
      "external_link": `${jsonMeta.external_url}/nft/${fileName}`,
      "description": jsonMeta.description,
      "collection": "NFT & Love",
      "properties": [],
      "levels": [],
      "stats": [],
      "unlockable_content": [
        true,
        `Thank you for purchasing my ${jsonMeta.name}, you could now share your love around you!`
      ],
      "explicit_and_sensitive_content": false,
      "supply": 1,
      "blockchain": "Ethereum",
      "sale_type": "Fixed Price",
      "price": 0.02,
      "specific_buyer": [
        false
      ],
      "method": [
        "Sell to highest bidder",
        1
      ],
      "duration": [
        "01-02-2022 00:00", "28-02-2022 23:59"
      ],
      "quantity": 1,
    };

    const metaDataAttributes = [];
    for (const attribute of jsonMeta.attributes) {
      metaDataAttributes.push({
        type: attribute.trait_type,
        name: attribute.value,
      })
    }
    metaData.properties = metaDataAttributes;

    allMetadata.push(metaData)
  }

  fs.writeFileSync(
    metasDatasFile,
    JSON.stringify({
      nft: allMetadata
    }, null, 2)
  )
}

main()
