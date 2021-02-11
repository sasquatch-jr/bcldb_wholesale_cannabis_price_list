# BC Liquor Distribution Board Wholesale Price List FAQ

## How did you make this?
The BCLDB uses Shopify. Shopify helpfully exposes entire stores via an undocumented and unprotected API ([such as this](https://www.bccannabiswholesale.com/products.json)). This price list was made by parsing that JSON document. At no time did a retailer give me credentials and I have never actually logged into BC Cannabis Wholesale store. The [script used to generate this](https://github.com/sasquatch-jr/bcldb_wholesale_cannabis_price_list/blob/main/bccs_dump.py) is freely available and is not very complicated for anyone who understands basic programming or python. With the exception of the tag parsing to determine the brand name for each product and matching up wholesale and retail prices, this script is not even specific to this store and should work with any private Shopify powered store.

If you are a concerned employee with the BCLDB, please show the script to your IT person, dev team or Shopify contacts and they can verify that this was built without any unauthorized access to your systems. If your IT and dev teams are unable to determine that this did not require unauthorized access, you should find a competent IT/dev team.

## Can I get a wholesale price list for another province?
Maybe. I also checked the OCS wholesale store but it is not running on Shopify so the technique used here does not work. It is likely that at least one other province is using Shopify and it would not be much work to build a wholesale price list from their store. 

## Why is this so ugly?
I'm a backend engineer in my day job and try to avoid javascript, css and other front end work. If You would like to contribute a better layout I would be happy to integrate it.

## Who are you?
Just a nerd who loves coding and weed and likes to try to find ways to combine the two. I prefer to keep my real identity a secret, but you can find me at https://www.reddit.com/user/sasquatch_jr or sasquatch__jr@outlook.com.

## Warning for licensed BC cannabis retailers
According to the [terms of use](https://www.bccannabiswholesale.com/pages/website-use-terms) of the BC Cannabis Wholesale portal, retailers can get in trouble for sharing this information. There is a good chance you signed an NDA about Wholesale prices at some point too so be careful not to risk your license.

The terms however are very clear that the word "you" specifically refers to "...a holder of a cannabis retail store licence issued by the General Manager under the Cannabis Control and Licensing Act, SBC 2018, c.29." As a consumer with zero connections to the legal cannabis industry none of this applies to me and I am in no way violating the terms of service.

## Caveats
The links to product pages are machine generated based on my best guesses for how the system works under the hood. As I do not have a login for this site, I do not have any way to verify that they are correct. I can confirm that replacing `bccannabiswholesale` with `bccannabisstores` in those URLs takes you to the retail page for the same item.
