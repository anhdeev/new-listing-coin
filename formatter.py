from string import Template
import re

TEMPLATE=[
'⛓ Platform: $platform',
'💎 Name: $name ($symbol)',
'💎 <b>Address: $contract</b>',
'💎 Supply: $circulating_suply/$total_suply',
'💎 Marketcap: $market_cap',
'💎 Current Price: $current_price',
'💎 24h High: $high_24h',
'💎 24h Low: $low_24h',
'📈 <a href="https://www.coingecko.com/en/coins/$id">Coingecko</a>',
'📈 <a href="https://dex.guru/token/$contract">Dex.Guru</a>',
'📈 <a href="https://charts.bogged.finance/?token=$contract">BoggedChart</a>',
'📈 <a href="$explorer">Explorer</a>',
]

def formatString(obj):
    template=""
    for line in TEMPLATE:
        keys = [word for word in re.split(' |<|\'|\n|/|\"|=', line) if word.startswith('$')]
        if len(keys) and obj.get(keys[0][1:]):
            template+=line + "\n"

    t = Template(template)
    return t.substitute(**obj)
