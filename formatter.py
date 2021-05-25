from string import Template
import re
from sys import platform

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
'📈 <a href="$explorer">Explorer</a>',
]

CHART={
    'binance-smart-chain': '📈 <a href="https://charts.bogged.finance/?token=$contract">BoggedChart</a>',
    'ethereum': '📈 <a href="https://dex.guru/token/$contract">Dex.Guru</a>',
    'solana': None,
    'tron': None,
    'polkadot': None,
    'fantom': None,
    'blockchain': None
}

def formatString(obj):
    try:
        template=""

        if not obj['platform']:
            obj['platform'] = 'blockchain'

        for line in TEMPLATE:
            keys = [word for word in re.split(' |<|\'|\n|/|\"|=', line) if word.startswith('$')]
            if len(keys) and obj.get(keys[0][1:]):
                template+=line + "\n"

        if  CHART.get(obj['platform']):
            template += CHART[obj.get('platform')]

        t = Template(template)
        return t.substitute(**obj)
    except Exception as e:
        raise(e)
